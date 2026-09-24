import os
import tempfile

from flask import Blueprint, jsonify, request

from ai.assistant_service import generate_assistant_response
from ai.assistant_vision_service import generate_image_response
from ai.assistant_video_service import generate_video_response


assistant_bp = Blueprint(
    "assistant",
    __name__,
    url_prefix="/api/assistant"
)


SUPPORTED_LANGUAGES = [
    "English",
    "Hindi",
    "Bengali"
]

ALLOWED_IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp"
}

ALLOWED_VIDEO_EXTENSIONS = {
    ".mp4",
    ".mov",
    ".webm",
    ".mkv"
}


# ============================================================
# HEALTH
# ============================================================

@assistant_bp.get("/health")
def assistant_health():
    return jsonify({
        "status": "ready",
        "languages": SUPPORTED_LANGUAGES
    }), 200


# ============================================================
# TEXT CHAT
# ============================================================

@assistant_bp.post("/chat")
def assistant_chat():
    data = request.get_json(silent=True) or {}

    message = str(
        data.get("message", "")
    ).strip()

    language = str(
        data.get("language", "English")
    ).strip()

    if not message:
        return jsonify({
            "error": "Message is required."
        }), 400

    if language not in SUPPORTED_LANGUAGES:
        return jsonify({
            "error": "Unsupported language."
        }), 400

    try:
        answer = generate_assistant_response(
            message=message,
            language=language
        )

        return jsonify({
            "status": "success",
            "language": language,
            "response": answer
        }), 200

    except Exception as exc:
        return jsonify({
            "status": "error",
            "error": str(exc)
        }), 500


# ============================================================
# IMAGE CHAT
# ============================================================

@assistant_bp.post("/image")
def assistant_image():
    """
    Analyze an uploaded image using the KISAAN
    AI Assistant vision service.
    """

    image = request.files.get("image")

    message = str(
        request.form.get("message", "")
    ).strip()

    language = str(
        request.form.get("language", "English")
    ).strip()

    if image is None or not image.filename:
        return jsonify({
            "error": "Image is required."
        }), 400

    if language not in SUPPORTED_LANGUAGES:
        return jsonify({
            "error": "Unsupported language."
        }), 400

    extension = os.path.splitext(
        image.filename
    )[1].lower()

    if extension not in ALLOWED_IMAGE_EXTENSIONS:
        return jsonify({
            "error": (
                "Unsupported image format. "
                "Please use JPG, JPEG, PNG, or WEBP."
            )
        }), 400

    temp_path = None

    try:
        # Save uploaded image temporarily.
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            image.save(temp_file.name)
            temp_path = temp_file.name

        answer = generate_image_response(
            image_path=temp_path,
            message=message,
            language=language
        )

        return jsonify({
            "status": "success",
            "language": language,
            "response": answer
        }), 200

    except Exception as exc:
        return jsonify({
            "status": "error",
            "error": str(exc)
        }), 500

    finally:
        # Always remove temporary image.
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass


# ============================================================
# VIDEO CHAT
# ============================================================

@assistant_bp.post("/video")
def assistant_video():
    """
    Analyze an uploaded video using the KISAAN
    AI Assistant video service.

    Current version analyzes visual video content only.
    Audio transcription will be added separately.
    """

    video = request.files.get("video")

    message = str(
        request.form.get("message", "")
    ).strip()

    language = str(
        request.form.get("language", "English")
    ).strip()

    # --------------------------------------------------------
    # Validate video
    # --------------------------------------------------------

    if video is None or not video.filename:
        return jsonify({
            "error": "Video is required."
        }), 400

    # --------------------------------------------------------
    # Validate language
    # --------------------------------------------------------

    if language not in SUPPORTED_LANGUAGES:
        return jsonify({
            "error": "Unsupported language."
        }), 400

    # --------------------------------------------------------
    # Validate extension
    # --------------------------------------------------------

    extension = os.path.splitext(
        video.filename
    )[1].lower()

    if extension not in ALLOWED_VIDEO_EXTENSIONS:
        return jsonify({
            "error": (
                "Unsupported video format. "
                "Please use MP4, MOV, WEBM, or MKV."
            )
        }), 400

    temp_path = None

    try:
        # ----------------------------------------------------
        # Save uploaded video temporarily
        # ----------------------------------------------------

        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=extension
        ) as temp_file:

            video.save(temp_file.name)
            temp_path = temp_file.name

        # ----------------------------------------------------
        # Analyze video
        # ----------------------------------------------------

        answer = generate_video_response(
            video_path=temp_path,
            message=message,
            language=language
        )

        # ----------------------------------------------------
        # Return response
        # ----------------------------------------------------

        return jsonify({
            "status": "success",
            "language": language,
            "response": answer
        }), 200

    except Exception as exc:
        return jsonify({
            "status": "error",
            "error": str(exc)
        }), 500

    finally:
        # ----------------------------------------------------
        # Always delete temporary uploaded video
        # ----------------------------------------------------

        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except OSError:
                pass