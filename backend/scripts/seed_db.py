"""
Database Seeding Script for Grievance System
Seeds the database with Hyderabad zones, circles, areas and admin users
Based on 2025 Delimitation: 12 zones, 60 circles, 300 wards
"""

from app import db
from app.models import Zone, Circle, Area, Admin
from app.utils import generate_admin_id

def seed_database():
    """Seed the database with zones, circles, areas and admins"""
    
    # ====================
    # SEED ZONES (12 zones based on 2025 delimitation)
    # ====================
    zones_data = [
        (1, "Malkajgiri"),
        (2, "Uppal"),
        (3, "L.B. Nagar"),
        (4, "Shamshabad"),
        (5, "Rajendranagar"),
        (6, "Charminar"),
        (7, "Golconda"),
        (8, "Khairatabad"),
        (9, "Secunderabad"),
        (10, "Serilingampally"),
        (11, "Kukatpally"),
        (12, "Quthbullapur"),
    ]
    
    zones = {}
    for zone_number, zone_name in zones_data:
        existing = Zone.query.filter_by(zone_number=zone_number).first()
        if not existing:
            zone = Zone(zone_number=zone_number, zone_name=zone_name)
            db.session.add(zone)
            db.session.flush()
            zones[zone_number] = zone
        else:
            zones[zone_number] = existing
    
    # ====================
    # SEED CIRCLES (5 circles per zone = 60 circles)
    # ====================
    circles = {}
    for zone_number, zone_obj in zones.items():
        for circle_num in range(1, 6):
            circle_name = f"Circle {circle_num}, Zone {zone_number}"
            
            existing = Circle.query.filter_by(
                zone_id=zone_obj.id,
                circle_number=circle_num
            ).first()
            
            if not existing:
                circle = Circle(
                    circle_number=circle_num,
                    circle_name=circle_name,
                    zone_id=zone_obj.id
                )
                db.session.add(circle)
                db.session.flush()
                circles[(zone_number, circle_num)] = circle
            else:
                circles[(zone_number, circle_num)] = existing
    
    # ====================
    # SEED AREAS/LOCALITIES (5 areas per circle = 300 areas)
    # ====================
    for zone_number, zone_obj in zones.items():
        for circle_num in range(1, 6):
            circle_obj = circles[(zone_number, circle_num)]
            
            for area_num in range(1, 6):
                area_name = f"Area {area_num}, Circle {circle_num}, Zone {zone_number}"
                ward_number = (zone_number * 100) + (circle_num * 10) + area_num
                
                existing = Area.query.filter_by(
                    circle_id=circle_obj.id,
                    area_name=area_name
                ).first()
                
                if not existing:
                    area = Area(
                        area_name=area_name,
                        ward_number=ward_number,
                        circle_id=circle_obj.id,
                        zone_id=zone_obj.id
                    )
                    db.session.add(area)
    
    # ====================
    # SEED SUPER ADMIN
    # ====================
    super_admin_email = 'superadmin@grievancehub.com'
    existing_super = Admin.query.filter_by(email=super_admin_email).first()
    
    if not existing_super:
        super_admin = Admin(
            admin_id=generate_admin_id(),
            email=super_admin_email,
            name='Super Administrator',
            phone='9999999999',
            role='super_admin',
            department='All',
            is_active=True
        )
        super_admin.set_password('SuperAdmin@123')
        db.session.add(super_admin)
    
    # ====================
    # SEED SUB ADMINS (one per zone)
    # ====================
    for zone_number, zone_obj in zones.items():
        admin_email = f'subadmin_zone{zone_number}@grievancehub.com'
        existing = Admin.query.filter_by(email=admin_email).first()
        
        if not existing:
            sub_admin = Admin(
                admin_id=generate_admin_id(),
                email=admin_email,
                name=f'Sub Administrator - {zone_obj.zone_name}',
                phone=f'999999{str(zone_number).zfill(4)}',
                role='sub_admin',
                department=zone_obj.zone_name,
                zone_id=zone_obj.id,
                is_active=True
            )
            sub_admin.set_password('SubAdmin@123')
            db.session.add(sub_admin)
    
    # ====================
    # SEED DEPARTMENT ADMINS (one per circle)
    # ====================
    circle_count = 0
    for zone_number, zone_obj in zones.items():
        for circle_num in range(1, 6):
            circle_obj = circles[(zone_number, circle_num)]
            circle_count += 1
            
            admin_email = f'deptadmin_circle{circle_count}@grievancehub.com'
            existing = Admin.query.filter_by(email=admin_email).first()
            
            if not existing:
                dept_admin = Admin(
                    admin_id=generate_admin_id(),
                    email=admin_email,
                    name=f'Department Administrator - Circle {circle_num}',
                    phone=f'888888{str(circle_count).zfill(4)}',
                    role='department_admin',
                    department='Municipal',
                    zone_id=zone_obj.id,
                    circle_id=circle_obj.id,
                    is_active=True
                )
                dept_admin.set_password('DeptAdmin@123')
                db.session.add(dept_admin)
    
    db.session.commit()
    
    print("=" * 50)
    print("DATABASE SEEDING COMPLETE")
    print("=" * 50)
    print(f"Zones: {len(zones)}")
    print(f"Circles: {len(circles)}")
    print("Areas: 300 (5 per circle)")
    print("Admin Users:")
    print("  - 1 Super Admin")
    print("  - 12 Sub Admins (1 per zone)")
    print("  - 60 Department Admins (1 per circle)")
    print("\nDefault Credentials:")
    print("  Super Admin: superadmin@grievancehub.com / SuperAdmin@123")
    print("  Sub Admin: subadmin_zone1@grievancehub.com / SubAdmin@123")
    print("  Dept Admin: deptadmin_circle1@grievancehub.com / DeptAdmin@123")
    print("=" * 50)
    
    return True

if __name__ == '__main__':
    from app import create_app
    app = create_app()
    with app.app_context():
        seed_database()
