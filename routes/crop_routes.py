"""
Kisan Web Project - Seasonal Crops & Smart Recommendation Routes
Provides crop cycles, step-by-step workflows, and geo/climate recommendation algorithms.
"""
from flask import Blueprint, request, jsonify
from extensions import db
from models import Crop
from datetime import datetime

crop_bp = Blueprint('crops', __name__, url_prefix='/api/crops')

@crop_bp.route('', methods=['GET'])
def get_crops():
    """Retrieve seasonal crops with optional filtering."""
    season = request.args.get('season', '').strip().lower()
    category = request.args.get('category', '').strip().lower()

    query = Crop.query
    if season and season != 'all':
        query = query.filter(Crop.season.ilike(f'%{season}%'))
    if category and category != 'all':
        query = query.filter(Crop.crop_category.ilike(f'%{category}%'))

    crops = query.order_by(Crop.name.asc()).all()
    return jsonify({
        'count': len(crops),
        'crops': [c.to_dict() for c in crops]
    }), 200


@crop_bp.route('/<int:crop_id>', methods=['GET'])
def get_crop_detail(crop_id):
    """Retrieve single crop with detailed step-by-step workflow."""
    crop = Crop.query.get_or_404(crop_id)
    return jsonify({
        'crop': crop.to_dict()
    }), 200


@crop_bp.route('/recommend', methods=['POST'])
def recommend_crops():
    """
    Intelligent crop & hybrid recommendation engine based on:
    - Temperature (°C)
    - Monthly Rainfall (mm)
    - Soil Type (e.g. Alluvial, Loamy, Black, Clayey)
    - Current month / season
    """
    data = request.get_json() or {}
    temp = float(data.get('temperature', 25.0) or 25.0)
    rainfall = float(data.get('rainfall', 80.0) or 80.0)
    soil_query = str(data.get('soil_type', 'Loamy')).strip().lower()
    state = str(data.get('state', '')).strip().lower()

    # Determine current agricultural season based on month if not specified
    current_month = datetime.now().month
    if current_month in [6, 7, 8, 9, 10]:
        current_season = 'kharif'
    elif current_month in [11, 12, 1, 2, 3]:
        current_season = 'rabi'
    else:
        current_season = 'zaid'

    all_crops = Crop.query.all()
    scored_crops = []

    for crop in all_crops:
        score = 100.0

        # Temperature suitability
        if temp < crop.ideal_temp_min:
            score -= abs(crop.ideal_temp_min - temp) * 3.5
        elif temp > crop.ideal_temp_max:
            score -= abs(temp - crop.ideal_temp_max) * 3.5

        # Rainfall suitability
        if rainfall < crop.ideal_rainfall_min:
            score -= (crop.ideal_rainfall_min - rainfall) * 0.4
        elif rainfall > crop.ideal_rainfall_max:
            score -= (rainfall - crop.ideal_rainfall_max) * 0.25

        # Soil matching bonus
        if soil_query and soil_query in (crop.soil_type or '').lower():
            score += 15.0

        # Season match bonus
        if current_season in crop.season.lower():
            score += 10.0

        # Cap score between 10 and 99
        final_score = max(15.0, min(99.0, score))

        scored_crops.append({
            'crop': crop.to_dict(),
            'suitability_score': round(final_score, 1),
            'recommended_hybrids': crop.hybrid_varieties.split(',') if crop.hybrid_varieties else [],
            'reasoning': f"Thrives in {crop.ideal_temp_min}-{crop.ideal_temp_max}°C with {crop.soil_type} soil."
        })

    # Sort descending by suitability score
    scored_crops.sort(key=lambda x: x['suitability_score'], reverse=True)
    top_recommendations = scored_crops[:4]

    return jsonify({
        'current_season': current_season,
        'detected_climate': {
            'temperature': temp,
            'rainfall': rainfall,
            'soil_type': soil_query.title()
        },
        'recommendations': top_recommendations
    }), 200
