"""Categories endpoint"""

from flask import Blueprint, jsonify
from app.config import DEPARTMENTS

bp = Blueprint('categories', __name__, url_prefix='/api')

@bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all categories"""
    return jsonify({
        'success': True,
        'categories': DEPARTMENTS
    })
