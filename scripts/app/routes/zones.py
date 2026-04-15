"""Zones and areas routes"""

from flask import Blueprint, request, jsonify
from app.models.database import get_db_connection

bp = Blueprint('zones', __name__, url_prefix='/api')

@bp.route('/zones', methods=['GET'])
def get_zones():
    """Get all zones"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT z.id, z.zone_number, z.zone_name,
                   COUNT(DISTINCT c.id) as circle_count,
                   COUNT(DISTINCT a.id) as area_count
            FROM zones z
            LEFT JOIN circles c ON c.zone_id = z.id
            LEFT JOIN areas a ON a.zone_id = z.id
            GROUP BY z.id
            ORDER BY z.zone_number
        ''')
        
        zones = []
        for row in cursor.fetchall():
            zones.append({
                'id': row['id'],
                'zone_number': row['zone_number'],
                'zone_name': row['zone_name'],
                'circle_count': row['circle_count'],
                'area_count': row['area_count']
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'zones': zones
        })
    
    except Exception as e:
        print(f"[v0] Error fetching zones: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/areas', methods=['GET'])
def get_all_areas():
    """Get all areas/localities with search support"""
    try:
        search = request.args.get('search', '').strip()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        if search:
            cursor.execute('''
                SELECT a.id, a.area_name, a.ward_number, a.zone_id,
                       z.zone_name, z.zone_number, c.circle_name
                FROM areas a
                JOIN zones z ON z.id = a.zone_id
                JOIN circles c ON c.id = a.circle_id
                WHERE a.area_name LIKE ?
                ORDER BY a.area_name
                LIMIT 50
            ''', (f'%{search}%',))
        else:
            cursor.execute('''
                SELECT a.id, a.area_name, a.ward_number, a.zone_id,
                       z.zone_name, z.zone_number, c.circle_name
                FROM areas a
                JOIN zones z ON z.id = a.zone_id
                JOIN circles c ON c.id = a.circle_id
                ORDER BY z.zone_number, a.area_name
            ''')
        
        areas = []
        for row in cursor.fetchall():
            areas.append({
                'id': row['id'],
                'area_name': row['area_name'],
                'ward_number': row['ward_number'],
                'zone_id': row['zone_id'],
                'zone_name': row['zone_name'],
                'zone_number': row['zone_number'],
                'circle_name': row['circle_name'],
                'display_name': f"{row['area_name']} - Zone {row['zone_number']} ({row['zone_name']})"
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'areas': areas,
            'count': len(areas)
        })
    
    except Exception as e:
        print(f"[v0] Error fetching areas: {e}")
        return jsonify({'error': str(e)}), 500

@bp.route('/areas/<int:zone_id>', methods=['GET'])
def get_areas_by_zone(zone_id):
    """Get areas for a specific zone"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT a.id, a.area_name, a.ward_number, c.circle_name, c.id as circle_id
            FROM areas a
            JOIN circles c ON c.id = a.circle_id
            WHERE a.zone_id = ?
            ORDER BY a.area_name
        ''', (zone_id,))
        
        areas = []
        for row in cursor.fetchall():
            areas.append({
                'id': row['id'],
                'area_name': row['area_name'],
                'ward_number': row['ward_number'],
                'circle_name': row['circle_name'],
                'circle_id': row['circle_id']
            })
        
        conn.close()
        
        return jsonify({
            'success': True,
            'areas': areas
        })
    
    except Exception as e:
        print(f"[v0] Error fetching areas for zone: {e}")
        return jsonify({'error': str(e)}), 500
