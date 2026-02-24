from flask import Blueprint, request, jsonify
from app import db
from app.models import Zone, Area, Circle

bp = Blueprint('zones', __name__, url_prefix='/api')

@bp.route('/zones', methods=['GET'])
def get_zones():
    """Get all zones with statistics"""
    try:
        zones = Zone.query.order_by(Zone.zone_number).all()
        
        zones_data = []
        for zone in zones:
            zones_data.append({
                'id': zone.id,
                'zone_number': zone.zone_number,
                'zone_name': zone.zone_name,
                'circle_count': len(zone.circles),
                'area_count': len(zone.areas)
            })
        
        return jsonify({
            'success': True,
            'zones': zones_data
        })
    
    except Exception as e:
        print(f"[v0] Error fetching zones: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/areas', methods=['GET'])
def get_all_areas():
    """Get all areas/localities with search support"""
    try:
        search = request.args.get('search', '').strip()
        
        if search:
            areas = Area.query.filter(
                Area.area_name.ilike(f'%{search}%')
            ).limit(50).all()
        else:
            areas = Area.query.order_by(Zone.zone_number, Area.area_name).all()
        
        areas_data = []
        for area in areas:
            areas_data.append({
                'id': area.id,
                'area_name': area.area_name,
                'ward_number': area.ward_number,
                'zone_id': area.zone_id,
                'zone_name': area.zone.zone_name,
                'zone_number': area.zone.zone_number,
                'circle_name': area.circle.circle_name,
                'display_name': f"{area.area_name} - Zone {area.zone.zone_number} ({area.zone.zone_name})"
            })
        
        return jsonify({
            'success': True,
            'areas': areas_data,
            'count': len(areas_data)
        })
    
    except Exception as e:
        print(f"[v0] Error fetching areas: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/areas/<int:zone_id>', methods=['GET'])
def get_areas_by_zone(zone_id):
    """Get areas for a specific zone"""
    try:
        areas = Area.query.filter_by(zone_id=zone_id).order_by(Area.area_name).all()
        
        areas_data = []
        for area in areas:
            areas_data.append({
                'id': area.id,
                'area_name': area.area_name,
                'ward_number': area.ward_number,
                'circle_id': area.circle_id,
                'circle_name': area.circle.circle_name
            })
        
        return jsonify({
            'success': True,
            'areas': areas_data
        })
    
    except Exception as e:
        print(f"[v0] Error fetching areas for zone: {e}")
        return jsonify({'error': str(e)}), 500
