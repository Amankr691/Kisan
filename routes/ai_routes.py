"""
Kisan Web Project - AI Crop Disease Diagnostic Routes

Handles:
- Crop leaf image uploads
- AI-powered disease diagnosis using local Ollama/Qwen2.5-VL
- Heuristic fallback diagnosis if Ollama is unavailable
- Disease diagnosis history
- Database logging
"""

import os
import uuid

from flask import Blueprint, request, jsonify, current_app, session
from PIL import Image, ImageStat

from extensions import db
from models import DiseaseLog
from ai.vision_service import diagnose_leaf


ai_bp = Blueprint("ai", __name__, url_prefix="/api/ai")


# ============================================================
# FALLBACK DISEASE KNOWLEDGE BASE
# ============================================================

DISEASE_KNOWLEDGE_BASE = [
    {
        "disease_name": "Early Blight (Alternaria solani)",
        "crop_name": "Tomato / Potato",
        "severity": "Medium",
        "confidence_base": 80.0,
        "symptoms": [
            "Concentric circular brown-to-black spots resembling a target board.",
            "Yellow halos may appear around necrotic lesions.",
            "Lower mature leaves may drop prematurely.",
        ],
        "organic_treatment": (
            "Remove infected leaves and apply Neem oil or "
            "Trichoderma-based bio-fungicide according to label directions."
        ),
        "chemical_treatment": (
            "Consult an agricultural expert before applying a registered "
            "fungicide such as Mancozeb or Chlorothalonil."
        ),
        "youtube_tutorial_id": "4k3zS4h2nVU",
    },

    {
        "disease_name": "Late Blight (Phytophthora infestans)",
        "crop_name": "Potato / Tomato",
        "severity": "High",
        "confidence_base": 80.0,
        "symptoms": [
            "Rapidly expanding irregular dark or water-soaked lesions.",
            "White fungal growth may appear on leaf undersides in humid conditions.",
            "Severe infection may cause stems and foliage to collapse.",
        ],
        "organic_treatment": (
            "Remove severely infected plant material and avoid prolonged "
            "leaf wetness. Copper-based treatments may be considered."
        ),
        "chemical_treatment": (
            "Consult an agricultural expert regarding registered late-blight "
            "fungicides appropriate for the crop and region."
        ),
        "youtube_tutorial_id": "6Yk7S0gQoB8",
    },

    {
        "disease_name": "Powdery Mildew",
        "crop_name": "Vegetables / Wheat / Cucurbits",
        "severity": "Medium",
        "confidence_base": 78.0,
        "symptoms": [
            "White powder-like patches on leaf surfaces.",
            "Leaves may become yellow or curled.",
            "Severe infection can reduce photosynthesis and crop growth.",
        ],
        "organic_treatment": (
            "Improve air circulation and consider appropriate biological "
            "or low-risk treatments recommended for the crop."
        ),
        "chemical_treatment": (
            "Use only a fungicide registered for the specific crop and disease, "
            "following label directions."
        ),
        "youtube_tutorial_id": "8W9D8Z7t1nM",
    },

    {
        "disease_name": "Yellow Rust / Stripe Rust",
        "crop_name": "Wheat / Barley",
        "severity": "High",
        "confidence_base": 82.0,
        "symptoms": [
            "Yellow or orange pustules appear in linear stripes.",
            "Rust-like powder may be visible on the leaf surface.",
            "Severe infection can reduce grain development.",
        ],
        "organic_treatment": (
            "Use resistant varieties where available and maintain balanced "
            "crop nutrition."
        ),
        "chemical_treatment": (
            "Consult local agricultural guidance for a registered rust fungicide "
            "appropriate to the crop."
        ),
        "youtube_tutorial_id": "J8m7Q9X2t8A",
    },

    {
        "disease_name": "Bacterial Leaf Spot",
        "crop_name": "Chilli / Pepper / Tomato",
        "severity": "Medium",
        "confidence_base": 76.0,
        "symptoms": [
            "Small dark or water-soaked spots on leaves.",
            "Lesions may become brown and papery.",
            "Severe infection may cause leaf or blossom drop.",
        ],
        "organic_treatment": (
            "Remove badly infected material, avoid overhead irrigation, "
            "and maintain good field sanitation."
        ),
        "chemical_treatment": (
            "Consult an agricultural expert before using registered "
            "copper-based bactericides."
        ),
        "youtube_tutorial_id": "5mJ7Pq1z0oE",
    },

    {
        "disease_name": "Healthy Foliage",
        "crop_name": "Unknown",
        "severity": "Low",
        "confidence_base": 85.0,
        "symptoms": [
            "Leaf appears predominantly green.",
            "No obvious severe lesions detected.",
            "No obvious widespread discoloration detected.",
        ],
        "organic_treatment": (
            "No disease-specific treatment indicated. Continue good crop care."
        ),
        "chemical_treatment": (
            "No chemical treatment recommended based solely on this analysis."
        ),
        "youtube_tutorial_id": None,
    },
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def allowed_image_extension(filename):
    """Check whether uploaded image extension is supported."""

    if "." not in filename:
        return False

    extension = filename.rsplit(".", 1)[1].lower()

    return extension in {
        "jpg",
        "jpeg",
        "png",
        "webp",
    }


def heuristic_diagnosis(file_path):
    """
    Fallback diagnosis.

    This is used only when the local Ollama AI model cannot
    perform the diagnosis.
    """

    with Image.open(file_path) as img:
        img_rgb = img.convert("RGB")

        stat = ImageStat.Stat(img_rgb)

        mean_r, mean_g, mean_b = stat.mean[:3]

        green_ratio = mean_g / (mean_r + mean_b + 1e-5)

        brightness = (
            mean_r
            + mean_g
            + mean_b
        ) / 3.0

        if (
            green_ratio > 0.85
            and mean_g > 100
            and mean_r < 110
        ):
            selected = DISEASE_KNOWLEDGE_BASE[5]

        elif (
            mean_r > mean_g
            and mean_r > 130
        ):
            selected = DISEASE_KNOWLEDGE_BASE[3]

        elif (
            mean_r > 110
            and mean_g > 100
            and brightness > 140
        ):
            selected = DISEASE_KNOWLEDGE_BASE[2]

        elif (
            mean_r < 80
            and mean_g < 90
        ):
            selected = DISEASE_KNOWLEDGE_BASE[1]

        elif abs(mean_r - mean_g) < 25:
            selected = DISEASE_KNOWLEDGE_BASE[0]

        else:
            selected = DISEASE_KNOWLEDGE_BASE[4]

    return {
        "disease_name": selected["disease_name"],
        "crop_name": selected["crop_name"],
        "confidence": selected["confidence_base"],
        "severity": selected["severity"],
        "symptoms": selected["symptoms"],
        "organic_treatment": selected["organic_treatment"],
        "chemical_treatment": selected["chemical_treatment"],
        "youtube_tutorial_id": selected["youtube_tutorial_id"],
        "analysis_source": "fallback",
    }


def normalize_confidence(value):
    """Ensure AI confidence is a number between 0 and 100."""

    try:
        value = float(value)
    except (TypeError, ValueError):
        return 0.0

    return max(
        0.0,
        min(value, 100.0)
    )


def normalize_symptoms(value):
    """Ensure symptoms are always stored as a list."""

    if isinstance(value, list):
        return [
            str(item)
            for item in value
            if item
        ]

    if isinstance(value, str):
        return [value]

    return []


# ============================================================
# AI DIAGNOSIS
# ============================================================

@ai_bp.route("/diagnose", methods=["POST"])
def diagnose_crop_disease():
    """
    Diagnose a crop disease from an uploaded leaf image.

    Primary system:
        Ollama + Qwen2.5-VL

    Fallback:
        Pillow RGB heuristic analysis
    """

    # --------------------------------------------------------
    # Validate upload
    # --------------------------------------------------------

    if "image" not in request.files:
        return jsonify({
            "status": "error",
            "error": "No image file uploaded.",
        }), 400

    file = request.files["image"]

    if not file or file.filename == "":
        return jsonify({
            "status": "error",
            "error": "Selected file has no filename.",
        }), 400

    if not allowed_image_extension(file.filename):
        return jsonify({
            "status": "error",
            "error": (
                "Unsupported image format. "
                "Please upload JPG, JPEG, PNG or WEBP."
            ),
        }), 400

    # --------------------------------------------------------
    # Save uploaded image
    # --------------------------------------------------------

    upload_dir = os.path.join(
        current_app.root_path,
        "static",
        "uploads",
    )

    os.makedirs(
        upload_dir,
        exist_ok=True,
    )

    extension = (
        file.filename
        .rsplit(".", 1)[1]
        .lower()
    )

    unique_filename = (
        f"scan_{uuid.uuid4().hex[:12]}.{extension}"
    )

    file_path = os.path.join(
        upload_dir,
        unique_filename,
    )

    file.save(file_path)

    crop_input = (
        request.form
        .get("crop_name", "")
        .strip()
    )

    # --------------------------------------------------------
    # Try real AI diagnosis first
    # --------------------------------------------------------

    analysis_source = "ollama-qwen2.5vl"

    try:

        current_app.logger.info(
            "Starting AI disease diagnosis for %s",
            unique_filename,
        )

        diagnosis = diagnose_leaf(
            image_path=file_path,
            crop_name=crop_input or None,
        )

        if not isinstance(diagnosis, dict):
            raise ValueError(
                "AI diagnosis returned invalid response."
            )

        if not diagnosis.get("disease_name"):
            raise ValueError(
                "AI diagnosis did not return disease_name."
            )

        diagnosis["analysis_source"] = (
            analysis_source
        )

        current_app.logger.info(
            "AI diagnosis completed: %s",
            diagnosis.get("disease_name"),
        )

    # --------------------------------------------------------
    # Fallback if Ollama fails
    # --------------------------------------------------------

    except Exception as exc:

        current_app.logger.warning(
            "Ollama diagnosis failed. "
            "Using fallback image analysis. Error: %s",
            exc,
        )

        analysis_source = "fallback"

        try:

            diagnosis = heuristic_diagnosis(
                file_path
            )

        except Exception as fallback_error:

            current_app.logger.exception(
                "Fallback diagnosis failed."
            )

            return jsonify({
                "status": "error",
                "error": (
                    "Unable to analyse the uploaded image."
                ),
                "details": str(fallback_error),
            }), 500

    # --------------------------------------------------------
    # Normalize AI response
    # --------------------------------------------------------

    disease_name = str(
        diagnosis.get(
            "disease_name",
            "Unknown",
        )
    )

    diagnosed_crop = str(
        diagnosis.get(
            "crop_name",
            "",
        )
        or crop_input
        or "Unknown"
    )

    confidence = normalize_confidence(
        diagnosis.get(
            "confidence",
            0,
        )
    )

    severity = str(
        diagnosis.get(
            "severity",
            "Unknown",
        )
    )

    symptoms = normalize_symptoms(
        diagnosis.get(
            "symptoms",
            []
        )
    )

    organic_treatment = str(
        diagnosis.get(
            "organic_treatment",
            "Consult a qualified agricultural expert.",
        )
    )

    chemical_treatment = str(
        diagnosis.get(
            "chemical_treatment",
            (
                "Consult a qualified agricultural expert "
                "before applying pesticides or fungicides."
            ),
        )
    )

    youtube_tutorial_id = diagnosis.get(
        "youtube_tutorial_id"
    )

    # --------------------------------------------------------
    # Store diagnosis in database
    # --------------------------------------------------------

    user_id = session.get("user_id")

    try:

        log = DiseaseLog(
            user_id=user_id,
            crop_name=diagnosed_crop,
            image_path=(
                f"/static/uploads/{unique_filename}"
            ),
            disease_name=disease_name,
            confidence=confidence,
            severity=severity,
            organic_treatment=organic_treatment,
            chemical_treatment=chemical_treatment,
            youtube_tutorial_id=youtube_tutorial_id,
        )

        log.symptoms = symptoms

        db.session.add(log)

        db.session.commit()

    except Exception as db_error:

        db.session.rollback()

        current_app.logger.exception(
            "Failed to save disease diagnosis."
        )

        return jsonify({
            "status": "error",
            "error": (
                "Diagnosis completed but could "
                "not be saved to the database."
            ),
            "details": str(db_error),
        }), 500

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return jsonify({

        "status": "success",

        "diagnostic_id": log.id,

        "analysis_source": analysis_source,

        "image_url": log.image_path,

        "disease_name": log.disease_name,

        "crop_name": log.crop_name,

        "confidence": log.confidence,

        "severity": log.severity,

        "symptoms": log.symptoms,

        "organic_treatment": (
            log.organic_treatment
        ),

        "chemical_treatment": (
            log.chemical_treatment
        ),

        "youtube_tutorial_id": (
            log.youtube_tutorial_id
        ),

        "analyzed_at": (
            log.created_at.strftime(
                "%b %d, %Y - %I:%M %p"
            )
            if log.created_at
            else "Just now"
        ),

    }), 200


# ============================================================
# DIAGNOSIS HISTORY
# ============================================================

@ai_bp.route("/history", methods=["GET"])
def get_diagnostic_history():
    """
    Retrieve the latest crop disease diagnoses.
    """

    user_id = session.get("user_id")

    query = DiseaseLog.query

    if user_id:
        query = query.filter_by(
            user_id=user_id
        )

    logs = (
        query
        .order_by(
            DiseaseLog.created_at.desc()
        )
        .limit(10)
        .all()
    )

    return jsonify({

        "status": "success",

        "count": len(logs),

        "logs": [
            log.to_dict()
            for log in logs
        ],

    }), 200