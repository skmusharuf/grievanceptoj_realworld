from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.zone import Zone
from app.models.circle import Circle
from app.models.area import Area

zone_bp = Blueprint('zone', __name__)


@zone_bp.route('/zones', methods=['GET'])
def get_zones():
    """Get all zones"""
    try:
        zones = db.session.query(
            Zone.id,
            Zone.zone_number,
            Zone.zone_name,
            db.func.count(db.distinct(Circle.id)).label('circle_count'),
            db.func.count(db.distinct(Area.id)).label('area_count')
        ).outerjoin(Circle, Circle.zone_id == Zone.id) \
         .outerjoin(Area, Area.zone_id == Zone.id) \
         .group_by(Zone.id) \
         .order_by(Zone.zone_number) \
         .all()

        zones_list = []
        for z in zones:
            zones_list.append({
                'id': z.id,
                'zone_number': z.zone_number,
                'zone_name': z.zone_name,
                'circle_count': z.circle_count,
                'area_count': z.area_count
            })

        return jsonify({
            'success': True,
            'zones': zones_list
        })

    except Exception as e:
        print(f"[v0] Error fetching zones: {e}")
        return jsonify({'error': str(e)}), 500


@zone_bp.route('/areas', methods=['GET'])
def get_all_areas():
    """Get all areas/localities with search support"""
    try:
        search = request.args.get('search', '').strip()

        query = db.session.query(
            Area.id,
            Area.area_name,
            Area.ward_number,
            Area.zone_id,
            Zone.zone_name,
            Zone.zone_number,
            Circle.circle_name
        ).join(Zone, Zone.id == Area.zone_id) \
         .join(Circle, Circle.id == Area.circle_id)

        if search:
            query = query.filter(Area.area_name.ilike(f'%{search}%'))
            query = query.order_by(Area.area_name).limit(50)
        else:
            query = query.order_by(Zone.zone_number, Area.area_name)

        results = query.all()

        areas = []
        for row in results:
            areas.append({
                'id': row.id,
                'area_name': row.area_name,
                'ward_number': row.ward_number,
                'zone_id': row.zone_id,
                'zone_name': row.zone_name,
                'zone_number': row.zone_number,
                'circle_name': row.circle_name,
                'display_name': f"{row.area_name} - Zone {row.zone_number} ({row.zone_name})"
            })

        return jsonify({
            'success': True,
            'areas': areas,
            'count': len(areas)
        })

    except Exception as e:
        print(f"[v0] Error fetching areas: {e}")
        return jsonify({'error': str(e)}), 500


@zone_bp.route('/areas/<int:zone_id>', methods=['GET'])
def get_areas_by_zone(zone_id):
    """Get areas for a specific zone"""
    try:
        results = db.session.query(
            Area.id,
            Area.area_name,
            Area.ward_number,
            Circle.circle_name,
            Circle.id.label('circle_id')
        ).join(Circle, Circle.id == Area.circle_id) \
         .filter(Area.zone_id == zone_id) \
         .order_by(Area.area_name) \
         .all()

        areas = []
        for row in results:
            areas.append({
                'id': row.id,
                'area_name': row.area_name,
                'ward_number': row.ward_number,
                'circle_name': row.circle_name,
                'circle_id': row.circle_id
            })

        return jsonify({
            'success': True,
            'areas': areas
        })

    except Exception as e:
        print(f"[v0] Error fetching areas for zone: {e}")
        return jsonify({'error': str(e)}), 500
