import base64
import json
import os
import subprocess
import tempfile

import requests


# ============================================================
# CONFIGURATION
# ============================================================

OLLAMA_URL = "http://localhost:11434/api/generate"

VISION_MODEL = "qwen2.5vl:3b"
TEXT_MODEL = "qwen3:8b"

VISION_TIMEOUT = 180
TEXT_TIMEOUT = 180

SUPPORTED_LANGUAGES = {
    "English": "English",
    "Hindi": "Hindi",
    "Bengali": "Bengali",
}

ALLOWED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".webm",
    ".mkv",
}

# Keep this small because video analysis runs locally.
MAX_FRAMES = 4


# ============================================================
# VIDEO INFORMATION
# ============================================================

def _get_video_duration(video_path):
    """
    Get video duration in seconds using FFprobe.
    """

    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "json",
        video_path,
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            check=True,
            timeout=30,
        )

        data = json.loads(result.stdout)

        duration = float(
            data["format"]["duration"]
        )

        if duration <= 0:
            raise ValueError(
                "Video duration is invalid."
            )

        return duration

    except FileNotFoundError as exc:
        raise RuntimeError(
            "FFprobe was not found. "
            "Make sure FFmpeg is installed and available in PATH."
        ) from exc

    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            "FFprobe took too long to inspect the video."
        ) from exc

    except (
        subprocess.CalledProcessError,
        KeyError,
        ValueError,
        json.JSONDecodeError,
    ) as exc:
        raise ValueError(
            "Unable to determine video duration."
        ) from exc


# ============================================================
# TIMESTAMP SELECTION
# ============================================================

def _choose_timestamps(duration):
    """
    Choose representative timestamps throughout the video.

    Exact beginning/end frames are avoided because they may
    contain black frames, transitions, or title screens.
    """

    if duration <= 2:
        return [duration / 2]

    frame_count = min(
        MAX_FRAMES,
        max(1, int(duration))
    )

    timestamps = []

    for index in range(frame_count):
        fraction = (
            (index + 1)
            / (frame_count + 1)
        )

        timestamp = duration * fraction

        timestamps.append(timestamp)

    return timestamps


# ============================================================
# FRAME EXTRACTION
# ============================================================

def _extract_frame(
    video_path,
    timestamp,
    output_path
):
    """
    Extract one representative frame using FFmpeg.
    """

    command = [
        "ffmpeg",
        "-y",
        "-ss",
        str(timestamp),
        "-i",
        video_path,
        "-frames:v",
        "1",
        "-vf",
        "scale='min(1280,iw)':-2",
        "-q:v",
        "3",
        output_path,
    ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode != 0:
            error_message = (
                result.stderr.strip()
                or "Unknown FFmpeg error."
            )

            raise RuntimeError(
                "FFmpeg could not extract a video frame. "
                f"{error_message}"
            )

        if not os.path.isfile(output_path):
            raise RuntimeError(
                "FFmpeg did not create the expected frame."
            )

        if os.path.getsize(output_path) == 0:
            raise RuntimeError(
                "FFmpeg created an empty frame."
            )

    except FileNotFoundError as exc:
        raise RuntimeError(
            "FFmpeg was not found. "
            "Make sure FFmpeg is installed and available in PATH."
        ) from exc

    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            "FFmpeg took too long to process the video."
        ) from exc


# ============================================================
# IMAGE ENCODING
# ============================================================

def _encode_image(image_path):
    """
    Convert an extracted frame to Base64 for Ollama.
    """

    try:
        with open(
            image_path,
            "rb"
        ) as image_file:

            return base64.b64encode(
                image_file.read()
            ).decode("utf-8")

    except OSError as exc:
        raise ValueError(
            f"Unable to read extracted video frame: {exc}"
        ) from exc


# ============================================================
# OLLAMA REQUEST HELPER
# ============================================================

def _send_ollama_request(
    payload,
    timeout
):
    """
    Send a request to Ollama and return the generated text.

    Includes the Ollama response body when an HTTP error occurs,
    which makes debugging easier.
    """

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=timeout
        )

    except requests.exceptions.ConnectionError as exc:
        raise RuntimeError(
            "Could not connect to Ollama. "
            "Make sure Ollama is running."
        ) from exc

    except requests.exceptions.Timeout as exc:
        raise RuntimeError(
            "Ollama took too long to respond."
        ) from exc

    except requests.exceptions.RequestException as exc:
        raise RuntimeError(
            f"Ollama request failed: {exc}"
        ) from exc

    if not response.ok:
        error_text = response.text.strip()

        raise RuntimeError(
            f"Ollama HTTP {response.status_code}: "
            f"{error_text}"
        )

    try:
        data = response.json()

    except ValueError as exc:
        raise RuntimeError(
            "Ollama returned an invalid HTTP response."
        ) from exc

    answer = str(
        data.get("response", "")
    ).strip()

    if not answer:
        raise RuntimeError(
            "Ollama returned an empty response."
        )

    return answer


# ============================================================
# SINGLE FRAME ANALYSIS
# ============================================================

def _analyze_frame(
    frame_base64,
    frame_number,
    timestamp
):
    """
    Analyze ONE extracted frame with qwen2.5vl:3b.

    Each frame is sent independently to avoid problems with
    multi-image requests.
    """

    prompt = f"""
You are analyzing one representative frame extracted from a video.

Frame number:
{frame_number}

Approximate timestamp:
{timestamp:.1f} seconds

Carefully inspect ONLY this image.

Describe the important visible information that may help another AI
understand what is happening in the complete video.

RULES:
- Describe the main subjects.
- Describe visible actions.
- Describe the environment or location when relevant.
- Mention important objects, machinery, crops, plants, animals,
  people, vehicles, buildings, text, or other visible content.
- If this is agricultural content, mention useful agricultural
  details that are actually visible.
- Do not invent anything that cannot be seen.
- Do not assume what happened before or after this frame.
- Do not claim to hear audio.
- If something is unclear, say that it is unclear.
- Keep the description concise but informative.

Return only the frame observation.
"""

    payload = {
        "model": VISION_MODEL,
        "prompt": prompt,
        "images": [frame_base64],
        "stream": False,
        "options": {
            "temperature": 0.1
        }
    }

    return _send_ollama_request(
        payload,
        VISION_TIMEOUT
    )


# ============================================================
# FINAL VIDEO INTERPRETATION
# ============================================================

def _generate_final_answer(
    observations,
    message,
    language,
    duration
):
    """
    Give the chronological frame observations to qwen3:8b
    and generate the final answer to the user's question.
    """

    response_language = (
        SUPPORTED_LANGUAGES[language]
    )

    observation_text = "\n\n".join(
        observations
    )

    prompt = f"""
You are KISAAN AI Assistant, a multimodal agricultural assistant
for farmers in India.

A user uploaded a video.

The video itself is NOT directly available to you.

A vision model inspected representative frames from the video in
chronological order. Those observations are provided below.

Your job is to use ONLY those observations to answer the user's
question.

Selected response language:
{response_language}

LANGUAGE RULES:
1. Always reply in {response_language}.
2. If Hindi is selected, use natural Hindi in Devanagari script.
3. If Bengali is selected, use natural Bengali script.
4. If English is selected, use clear simple English.
5. The user's question may be written in English, Hindi, Bengali,
   or mixed language.
6. Use natural agricultural terminology when appropriate.

VIDEO LIMITATIONS:
- The analysis is based on sampled video frames.
- Do not pretend that every frame of the video was inspected.
- Do not invent events between sampled frames.
- Do not claim that you heard the video's audio.
- Audio has not been analyzed.
- If the observations are insufficient to answer the question,
  clearly explain that limitation.
- If the observations conflict, mention the uncertainty.
- Do not assume the video is agricultural.

AGRICULTURAL SAFETY:
- You may explain visible agricultural activities.
- You may describe visible plant symptoms.
- Do not claim laboratory confirmation of a plant disease.
- Do not invent symptoms.
- Keep treatment recommendations conservative.
- Do not provide dangerous pesticide concentrations.
- When identification is uncertain, recommend expert confirmation
  where appropriate.

RESPONSE RULES:
- Answer the user's actual question directly.
- Do not introduce yourself unless asked.
- Keep the answer concise but useful.
- Do not list frame-by-frame observations unless that is useful
  for answering the question.
- Never invent information that is not supported by the
  observations.

Video duration:
{duration:.1f} seconds

VISION MODEL OBSERVATIONS:

{observation_text}

USER'S QUESTION:

{message}

Answer only the user's question in {response_language}.
"""

    payload = {
        "model": TEXT_MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2
        }
    }

    return _send_ollama_request(
        payload,
        TEXT_TIMEOUT
    )


# ============================================================
# PUBLIC VIDEO FUNCTION
# ============================================================

def generate_video_response(
    video_path,
    message="",
    language="English"
):
    """
    Analyze a video using representative frames.

    Pipeline:

    Video
        ↓
    FFprobe determines duration
        ↓
    FFmpeg extracts representative frames
        ↓
    qwen2.5vl:3b analyzes each frame separately
        ↓
    qwen3:8b combines the observations
        ↓
    Final answer in English / Hindi / Bengali

    Version 1 analyzes VISUAL content only.
    Audio is not transcribed or analyzed yet.
    """

    # --------------------------------------------------------
    # Validate video
    # --------------------------------------------------------

    if not video_path:
        raise ValueError(
            "Video path is required."
        )

    if not os.path.isfile(video_path):
        raise ValueError(
            "Video file was not found."
        )

    extension = os.path.splitext(
        video_path
    )[1].lower()

    if extension not in ALLOWED_VIDEO_EXTENSIONS:
        raise ValueError(
            "Unsupported video format. "
            "Please use MP4, MOV, WEBM, or MKV."
        )

    # --------------------------------------------------------
    # Validate language
    # --------------------------------------------------------

    if language not in SUPPORTED_LANGUAGES:
        language = "English"

    # --------------------------------------------------------
    # Prepare user question
    # --------------------------------------------------------

    message = str(
        message or ""
    ).strip()

    if not message:
        message = (
            "Describe what happens in this video."
        )

    # --------------------------------------------------------
    # Determine video duration
    # --------------------------------------------------------

    duration = _get_video_duration(
        video_path
    )

    # --------------------------------------------------------
    # Choose representative timestamps
    # --------------------------------------------------------

    timestamps = _choose_timestamps(
        duration
    )

    observations = []

    # --------------------------------------------------------
    # Extract and analyze each frame
    # --------------------------------------------------------

    with tempfile.TemporaryDirectory() as temp_dir:

        for index, timestamp in enumerate(
            timestamps
        ):
            frame_number = index + 1

            frame_path = os.path.join(
                temp_dir,
                f"frame_{frame_number}.jpg"
            )

            # Extract frame
            _extract_frame(
                video_path,
                timestamp,
                frame_path
            )

            # Convert frame to Base64
            frame_base64 = _encode_image(
                frame_path
            )

            print(
                f"[AI Video] Analyzing frame "
                f"{frame_number}/{len(timestamps)} "
                f"at {timestamp:.1f}s..."
            )

            # Analyze one image only
            frame_analysis = _analyze_frame(
                frame_base64,
                frame_number,
                timestamp
            )

            observations.append(
                (
                    f"Frame {frame_number} "
                    f"(approximately {timestamp:.1f} seconds):\n"
                    f"{frame_analysis}"
                )
            )

    if not observations:
        raise RuntimeError(
            "No video frames could be analyzed."
        )

    # --------------------------------------------------------
    # Generate final answer
    # --------------------------------------------------------

    print(
        "[AI Video] Combining frame observations "
        f"using {TEXT_MODEL}..."
    )

    final_answer = _generate_final_answer(
        observations=observations,
        message=message,
        language=language,
        duration=duration
    )

    return final_answer