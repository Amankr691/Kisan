"""
Kisan Web Project - Government Schemes & Kisan Loan Portals
Provides structured data on official agricultural subsidies, KCC credit portals, and insurance.
"""
from flask import Blueprint, request, jsonify
from extensions import db
from models import Scheme

schemes_bp = Blueprint('schemes', __name__, url_prefix='/api/schemes')

@schemes_bp.route('', methods=['GET'])
def get_schemes():
    """Retrieve government schemes and agricultural loans with category filtering."""
    category = request.args.get('category', '').strip().lower()

    query = Scheme.query
    if category and category != 'all':
        query = query.filter_by(category=category)

    schemes = query.order_by(Scheme.id.asc()).all()
    return jsonify({
        'count': len(schemes),
        'schemes': [s.to_dict() for s in schemes]
    }), 200


@schemes_bp.route('/<int:scheme_id>', methods=['GET'])
def get_scheme_detail(scheme_id):
    """Retrieve details for a specific scheme."""
    scheme = Scheme.query.get_or_404(scheme_id)
    return jsonify({'scheme': scheme.to_dict()}), 200
