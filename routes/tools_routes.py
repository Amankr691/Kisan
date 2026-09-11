"""
Kisan Web Project - Agricultural Tools & Machinery Routes
Showcases modern farm machinery, specifications, subsidy availability, and video demos.
"""
from flask import Blueprint, request, jsonify
from extensions import db
from models import AgriculturalTool

tools_bp = Blueprint('tools', __name__, url_prefix='/api/tools')

@tools_bp.route('', methods=['GET'])
def get_tools():
    """List modern agricultural tools with category filtering."""
    category = request.args.get('category', '').strip().lower()

    query = AgriculturalTool.query
    if category and category != 'all':
        query = query.filter_by(category=category)

    tools = query.order_by(AgriculturalTool.id.asc()).all()
    return jsonify({
        'count': len(tools),
        'tools': [t.to_dict() for t in tools]
    }), 200


@tools_bp.route('/<int:tool_id>', methods=['GET'])
def get_tool_detail(tool_id):
    """Retrieve details for a specific agricultural machine."""
    tool = AgriculturalTool.query.get_or_404(tool_id)
    return jsonify({'tool': tool.to_dict()}), 200
