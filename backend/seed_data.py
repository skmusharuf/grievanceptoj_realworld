"""
Database Seeding Script for Grievance System (ORM version).
Seeds the database with Hyderabad zones, circles, areas and admin users.
Based on 2025 Delimitation: 12 zones, 60 circles, 300 wards.

Usage:
    python seed_data.py
"""
import hashlib
import os
from app import create_app
from app.extensions import db
from app.models.zone import Zone
from app.models.circle import Circle
from app.models.area import Area
from app.models.admin import Admin


def hash_password(password):
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode()).hexdigest()


def seed_database():
    """Seed the database with zones, circles, areas and admins"""

    app = create_app()

    with app.app_context():
        os.makedirs('instance', exist_ok=True)
        db.create_all()

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

        for zone_number, zone_name in zones_data:
            existing = Zone.query.filter_by(zone_number=zone_number).first()
            if not existing:
                db.session.add(Zone(zone_number=zone_number, zone_name=zone_name))

        db.session.commit()
        print("Zones seeded successfully")

        # ====================
        # SEED CIRCLES (60 circles, 5 per zone)
        # ====================
        circles_data = [
            (1, "Keesara", 1), (2, "Alwal", 1), (3, "Bowenpally", 1),
            (4, "Moula Ali", 1), (5, "Malkajgiri", 1),
            (6, "Ghatkesar", 2), (7, "Kapra", 2), (8, "Nacharam", 2),
            (9, "Uppal", 2), (10, "Boduppal", 2),
            (11, "Nagole", 3), (12, "Saroornagar", 3), (13, "L.B. Nagar", 3),
            (14, "Hayathnagar", 3), (15, "Karmanghat", 3),
            (16, "Adibatla", 4), (17, "Badangpet", 4), (18, "Jalpally", 4),
            (19, "Shamshabad", 4), (20, "Tukkuguda", 4),
            (21, "Rajendranagar", 5), (22, "Attapur", 5), (23, "Bahadurpura", 5),
            (24, "Falaknuma", 5), (25, "Chandrayan Gutta", 5),
            (26, "Santoshnagar", 6), (27, "Yakutpura", 6), (28, "Malakpet", 6),
            (29, "Charminar", 6), (30, "Moosarambagh", 6),
            (31, "Goshamahal", 7), (32, "Karwan", 7), (33, "Golconda", 7),
            (34, "Mehdipatnam", 7), (35, "Masab Tank", 7),
            (36, "Khairatabad", 8), (37, "Jubilee Hills", 8), (38, "Borabanda", 8),
            (39, "Yousufguda", 8), (40, "Ameerpet", 8),
            (41, "Kavadiguda", 9), (42, "Musheerabad", 9), (43, "Amberpet", 9),
            (44, "Tarnaka", 9), (45, "Mettuguda", 9),
            (46, "Narsingi", 10), (47, "Patancheruvu", 10), (48, "Ameenpur", 10),
            (49, "Miyapur", 10), (50, "Serilingampally", 10),
            (51, "Madhapur", 11), (52, "Allwyn Colony", 11), (53, "Kukatpally", 11),
            (54, "Moosapet", 11), (55, "KPHB", 11),
            (56, "Chintal", 12), (57, "Jeedimetla", 12), (58, "Kompally", 12),
            (59, "Gajularamaram", 12), (60, "Nizampet", 12),
        ]

        for circle_number, circle_name, zone_id in circles_data:
            existing = Circle.query.filter_by(circle_number=circle_number).first()
            if not existing:
                db.session.add(Circle(
                    circle_number=circle_number,
                    circle_name=circle_name,
                    zone_id=zone_id
                ))

        db.session.commit()
        print("Circles seeded successfully")

        # ====================
        # SEED AREAS/LOCALITIES
        # ====================
        areas_data = [
            # Zone 1: Malkajgiri
            ("Keesara", 1, 1, 1), ("Chandrapuri Colony", 2, 1, 1), ("Jawaharnagar", 3, 1, 1),
            ("Dammaiguda", 4, 1, 1), ("Yapral", 189, 1, 1), ("Shamirpet", 300, 1, 1),
            ("Turakapally", 190, 2, 1), ("Macha Bollaram", 191, 2, 1), ("Alwal", 192, 2, 1),
            ("Venkatapuram", 193, 2, 1), ("Bhudevi Nagar", 194, 2, 1), ("Kanajiguda", 195, 2, 1),
            ("Monda Market", 196, 3, 1), ("Fateh Nagar", 260, 3, 1), ("Prakash Nagar", 261, 3, 1),
            ("Old Bowenpally", 262, 3, 1), ("Hasmathpet", 264, 3, 1),
            ("Balram Nagar", 184, 4, 1), ("Vinayak Nagar", 185, 4, 1), ("Moula Ali", 186, 4, 1),
            ("Kakatiya Nagar", 187, 4, 1), ("Neredmet", 188, 4, 1),
            ("East Anandbagh", 180, 5, 1), ("Mirjalguda", 181, 5, 1), ("Gautham Nagar", 182, 5, 1),
            ("Malkajgiri", 183, 5, 1),
            # Zone 2: Uppal
            ("Nagaram", 5, 6, 2), ("Ghatkesar", 6, 6, 2), ("Edulabad", 7, 6, 2), ("Pocharam", 8, 6, 2),
            ("Vampuguda", 13, 7, 2), ("Kapra", 14, 7, 2), ("A. S. Rao Nagar", 15, 7, 2),
            ("Kushaiguda", 16, 7, 2), ("Cherlapally", 17, 7, 2),
            ("Shakthi Sai Nagar", 18, 8, 2), ("H. B. Colony", 19, 8, 2), ("Mallapur", 20, 8, 2),
            ("Nacharam", 21, 8, 2), ("HMT Nagar", 22, 8, 2),
            ("Chilkanagar", 23, 9, 2), ("Beerappagadda", 24, 9, 2), ("Habsiguda", 25, 9, 2),
            ("Ramanthapur", 26, 9, 2), ("Venkat Reddy Nagar", 27, 9, 2), ("Uppal", 28, 9, 2),
            ("Medipally", 9, 10, 2), ("Peerzadiguda", 10, 10, 2), ("Boduppal", 11, 10, 2),
            ("Chengicherla", 12, 10, 2),
            # Zone 3: L.B. Nagar
            ("Nagole", 29, 11, 3), ("Mansoorabad", 45, 11, 3), ("Lecturers Colony", 47, 11, 3),
            ("Kuntloor", 51, 11, 3), ("Pedda Amberpet", 52, 11, 3),
            ("Kothapet", 30, 12, 3), ("Chaitanyapuri", 31, 12, 3), ("Gaddiannaram", 32, 12, 3),
            ("Saroornagar", 33, 12, 3), ("Doctors Colony", 34, 12, 3), ("Rama Krishna Puram", 35, 12, 3),
            ("NTR Nagar", 36, 12, 3),
            ("Lingojiguda", 37, 13, 3), ("Champapet", 38, 13, 3), ("Karmanghat", 39, 13, 3),
            ("Bairamalguda", 40, 13, 3), ("Hastinapuram", 41, 13, 3),
            ("BN Reddy Nagar", 42, 14, 3), ("Vanasthalipuram", 43, 14, 3), ("Chintalakunta", 44, 14, 3),
            ("High Court Colony", 48, 14, 3), ("Sahebnagar", 49, 14, 3), ("Hayathnagar", 50, 14, 3),
            ("L.B. Nagar", 46, 13, 3),
            # Zone 4: Shamshabad
            ("Thorrur", 53, 16, 4), ("Kongara Kalan", 54, 16, 4), ("Adibatla", 55, 16, 4),
            ("Turkayamjal", 56, 16, 4),
            ("Nadergul", 57, 17, 4), ("Prasanthi Hills", 58, 17, 4), ("Jillelguda", 59, 17, 4),
            ("Meerpet", 60, 17, 4), ("Badangpet", 61, 17, 4), ("Balapur", 62, 17, 4),
            ("Shaheen Nagar", 63, 18, 4), ("Pahari Sharif", 64, 18, 4), ("Jalpally", 65, 18, 4),
            ("Tukkuguda", 66, 19, 4), ("Mankhal", 67, 19, 4), ("Shamshabad", 118, 19, 4),
            ("Kothwalguda", 119, 19, 4),
            # Zone 5: Rajendranagar
            ("Rajendranagar", 120, 21, 5), ("Bandlaguda Jagir", 121, 21, 5), ("Kismatpur", 122, 21, 5),
            ("Hydershahkote", 123, 21, 5),
            ("Attapur", 112, 22, 5), ("Hyderguda", 113, 22, 5), ("Suleman Nagar", 114, 22, 5),
            ("Shastripuram", 115, 22, 5), ("Katedan", 116, 22, 5), ("Mailardevpally", 117, 22, 5),
            ("Doodh Bowli", 103, 23, 5), ("Teegal Kunta", 108, 23, 5), ("Chandu Lal Baradari", 109, 23, 5),
            ("Ramnasthpura", 110, 23, 5), ("Kishanbagh", 111, 23, 5),
            ("Shah-Ali-Banda", 104, 24, 5), ("Falaknuma", 105, 24, 5), ("Jahanuma", 106, 24, 5),
            ("Nawab Saheb Kunta", 107, 24, 5),
            ("Bandlaguda", 68, 25, 5), ("Noori Nagar", 69, 25, 5), ("Barkas", 70, 25, 5),
            ("Kanchanbagh", 71, 25, 5), ("Chandrayan Gutta", 72, 25, 5),
            # Zone 6: Charminar
            ("Bhanu Nagar", 84, 26, 6), ("Santoshnagar", 85, 26, 6), ("IS SADAN", 86, 26, 6),
            ("Saraswathi Nagar", 87, 26, 6),
            ("Gowlipura", 78, 27, 6), ("Talab Chanchalam", 79, 27, 6), ("Yakutpura", 80, 27, 6),
            ("Dabirpura", 81, 27, 6), ("Rein Bazar", 82, 27, 6), ("Madannapet", 83, 27, 6),
            ("Saidabad", 88, 28, 6), ("Asmangadh", 89, 28, 6), ("Akberbagh", 93, 28, 6),
            ("Chawani", 94, 28, 6),
            ("Purani Haveli", 97, 29, 6), ("Pathargatti", 98, 29, 6), ("Hari Bowli", 99, 29, 6),
            ("Qazipura", 100, 29, 6), ("Ghansi Bazar", 101, 29, 6), ("Purana Pul", 102, 29, 6),
            ("Moosarambagh", 90, 30, 6), ("Old Malakpet", 91, 30, 6), ("MCH Colony", 92, 30, 6),
            ("Kala Dera", 95, 30, 6), ("Azampura", 96, 30, 6),
            # Zone 7: Golconda
            ("Dattatreya Nagar", 148, 31, 7), ("Manghalhat", 149, 31, 7), ("Goshamahal", 150, 31, 7),
            ("Begum Bazaar", 151, 31, 7), ("Jambagh", 152, 31, 7), ("Exhibition Grounds", 153, 31, 7),
            ("Langar Houz", 134, 32, 7), ("Gudimalkapur", 135, 32, 7), ("Karwan", 136, 32, 7),
            ("Tappachabutra", 137, 32, 7), ("Jiyaguda", 138, 32, 7),
            ("Nizam Colony", 129, 33, 7), ("Nanalnagar", 130, 33, 7), ("Tolichowki", 131, 33, 7),
            ("Golconda", 132, 33, 7), ("Ibrahimbagh", 133, 33, 7), ("Shaikpet", 223, 33, 7),
            ("OU Colony", 224, 33, 7),
            ("Asif Nagar", 139, 34, 7), ("Padmanabha Nagar", 140, 34, 7), ("Mehdipatnam", 141, 34, 7),
            ("Syed Nagar", 142, 34, 7),
            ("Vijayanagar Colony", 143, 35, 7), ("Ahmed Nagar", 144, 35, 7), ("Shanthi Nagar", 145, 35, 7),
            ("Mallepally", 147, 35, 7),
            # Zone 8: Khairatabad
            ("Red Hills", 146, 36, 8), ("Gunfoundry", 154, 36, 8), ("Irrum Manzil", 217, 36, 8),
            ("Somajiguda", 218, 36, 8), ("Khairatabad", 219, 36, 8), ("Himayatnagar", 220, 36, 8),
            ("Jubilee Hills", 215, 37, 8), ("Venkateswara Colony", 216, 37, 8), ("Banjara Hills", 221, 37, 8),
            ("Film Nagar", 222, 37, 8),
            ("Krishna Nagar", 210, 38, 8), ("Rahmath Nagar", 211, 38, 8), ("Karmika Nagar", 212, 38, 8),
            ("Rajeev Nagar", 213, 38, 8), ("Borabanda", 214, 38, 8),
            ("Erragadda", 205, 39, 8), ("Vengal Rao Nagar", 206, 39, 8), ("Srinagar Colony", 207, 39, 8),
            ("Yousufguda", 208, 39, 8), ("AG Colony", 209, 39, 8),
            ("Begumpet", 200, 40, 8), ("Ameerpet", 201, 40, 8), ("S. R. Nagar", 202, 40, 8),
            ("BK Guda", 203, 40, 8), ("Sanathnagar", 204, 40, 8),
            # Zone 9: Secunderabad
            ("Gandhi Nagar", 165, 41, 9), ("Kavadiguda", 166, 41, 9), ("Bakaram", 167, 41, 9),
            ("Bholakpur", 168, 41, 9), ("Padmarao Nagar", 197, 41, 9), ("Bansilalpet", 198, 41, 9),
            ("Ramgopalpet", 199, 41, 9),
            ("Adikmet", 163, 42, 9), ("Bagh Lingampally", 164, 42, 9), ("Musheerabad", 169, 42, 9),
            ("Ramnagar", 170, 42, 9), ("Bapuji Nagar", 171, 42, 9),
            ("Barkatpura", 155, 43, 9), ("Kachiguda", 156, 43, 9), ("Golnaka", 157, 43, 9),
            ("Patel Nagar", 158, 43, 9), ("Amberpet", 159, 43, 9), ("Bagh Amberpet", 160, 43, 9),
            ("Tilak Nagar", 161, 43, 9), ("Nallakunta", 162, 43, 9),
            ("Boudha Nagar", 172, 44, 9), ("Tarnaka", 173, 44, 9), ("Sitaphalmandi", 174, 44, 9),
            ("Chilkalguda", 175, 44, 9),
            ("Mettuguda", 176, 45, 9), ("Lalapet", 177, 45, 9), ("North Lallaguda", 178, 45, 9),
            ("Addagutta", 179, 45, 9),
            # Zone 10: Serilingampally
            ("Narsingi", 124, 46, 10), ("Kokapet", 125, 46, 10), ("Gandipet", 126, 46, 10),
            ("Manikonda", 127, 46, 10), ("Neknampur", 128, 46, 10),
            ("Tellapur", 263, 47, 10), ("Muthangi", 265, 47, 10), ("Patancheruvu", 266, 47, 10),
            ("JP Colony", 267, 47, 10),
            ("Ramachandrapuram", 268, 48, 10), ("Bharathi Nagar", 269, 48, 10), ("Beeramguda", 270, 48, 10),
            ("Ameenpur", 271, 48, 10), ("IDA Bollaram", 272, 48, 10),
            ("Hafeezpet", 236, 49, 10), ("Madeenaguda", 237, 49, 10), ("Chanda Nagar", 238, 49, 10),
            ("Deepthisri Nagar", 239, 49, 10), ("Miyapur", 240, 49, 10), ("Maktha Mahabubpet", 241, 49, 10),
            ("Gachibowli", 225, 50, 10), ("Nallagandla", 226, 50, 10), ("Serilingampally", 227, 50, 10),
            ("Masjid Banda", 228, 50, 10), ("Sri Ram Nagar", 229, 50, 10), ("Kondapur", 234, 50, 10),
            # Zone 11: Kukatpally
            ("Anjaiah Nagar", 230, 51, 11), ("HITEC City", 231, 51, 11), ("Madhapur", 232, 51, 11),
            ("Izzat Nagar", 233, 51, 11), ("Matrusri Nagar", 235, 51, 11), ("Mayuri Nagar", 242, 51, 11),
            ("Hyder Nagar", 243, 52, 11), ("Bhagya Nagar Colony", 244, 52, 11), ("Shamshiguda", 245, 52, 11),
            ("Allwyn Colony", 246, 52, 11), ("Vivekananda Nagar Colony", 247, 52, 11), ("Venkateswara Nagar", 248, 52, 11),
            ("Kukatpally", 249, 53, 11), ("Balaji Nagar", 250, 53, 11), ("Vasanth Nagar", 251, 53, 11),
            ("KPHB Colony", 252, 53, 11), ("Kaithalapur", 253, 53, 11), ("Gayatri Nagar", 254, 53, 11),
            ("Allapur", 255, 54, 11), ("Moti Nagar", 256, 54, 11), ("Moosapet", 257, 54, 11),
            ("Prashanth Nagar", 258, 54, 11), ("Balanagar", 259, 54, 11),
            # Zone 12: Quthbullapur
            ("Rodamestri Nagar", 279, 56, 12), ("Jagathgiri Gutta", 280, 56, 12), ("Ranga Reddy Nagar", 281, 56, 12),
            ("Chintal", 282, 56, 12), ("Giri Nagar", 283, 56, 12),
            ("Ganesh Nagar", 284, 57, 12), ("Padma Nagar", 285, 57, 12), ("Quthbullapur", 286, 57, 12),
            ("Pet Basheerabad", 287, 57, 12),
            ("Kompally", 288, 58, 12), ("Dulapally", 289, 58, 12), ("Subhash Nagar", 290, 58, 12),
            ("Saibaba Nagar", 292, 58, 12),
            ("Mahadevpuram", 277, 59, 12), ("Gajularamaram", 278, 59, 12), ("Shapur Nagar", 291, 59, 12),
            ("Suraram", 293, 59, 12),
            ("Nizampet", 273, 60, 12), ("Bachupally", 274, 60, 12), ("Pragathinagar", 275, 60, 12),
            ("Suchitra", 276, 60, 12), ("Medchal", 294, 60, 12), ("Dundigal", 295, 60, 12),
            ("Gundlapochampalli", 296, 60, 12), ("Bolarum", 297, 60, 12), ("Thumkunta", 298, 60, 12),
            ("Kompally Junction", 299, 60, 12),
        ]

        for area_name, ward_number, circle_id, zone_id in areas_data:
            existing = Area.query.filter_by(area_name=area_name, zone_id=zone_id).first()
            if not existing:
                db.session.add(Area(
                    area_name=area_name,
                    ward_number=ward_number,
                    circle_id=circle_id,
                    zone_id=zone_id
                ))

        db.session.commit()
        print(f"Areas seeded successfully: {len(areas_data)} localities")

        # ====================
        # SEED ADMIN USERS
        # ====================

        # 1 Super Admin
        if not Admin.query.filter_by(admin_id="SA001").first():
            db.session.add(Admin(
                admin_id="SA001",
                email="superadmin@grievancehub.com",
                password_hash=hash_password("superadmin@123"),
                name="Super Administrator",
                phone="9876543210",
                role="super_admin"
            ))

        # 12 Sub Admins (1 per zone)
        zone_names = ["Malkajgiri", "Uppal", "L.B. Nagar", "Shamshabad", "Rajendranagar",
                      "Charminar", "Golconda", "Khairatabad", "Secunderabad", "Serilingampally",
                      "Kukatpally", "Quthbullapur"]

        for i, zone_name in enumerate(zone_names, 1):
            admin_id = f"ZA{i:03d}"
            if not Admin.query.filter_by(admin_id=admin_id).first():
                db.session.add(Admin(
                    admin_id=admin_id,
                    email=f"zone{i}admin@grievancehub.com",
                    password_hash=hash_password(f"zone{i}admin@123"),
                    name=f"Zone {i} Administrator - {zone_name}",
                    phone=f"98765{i:05d}",
                    role="sub_admin",
                    zone_id=i
                ))

        db.session.commit()

        # 60 Department Admins (1 per circle)
        departments = ["Municipal", "Police", "Public Works Department", "Transport", "CM Office (Miscellaneous)"]
        circles = Circle.query.order_by(Circle.zone_id, Circle.circle_number).all()
        admin_counter = 1

        for circle in circles:
            dept_idx = (circle.circle_number - 1) % 5
            department = departments[dept_idx]
            admin_id = f"DA{admin_counter:03d}"

            if not Admin.query.filter_by(admin_id=admin_id).first():
                db.session.add(Admin(
                    admin_id=admin_id,
                    email=f"dept{admin_counter}@grievancehub.com",
                    password_hash=hash_password(f"dept{admin_counter}admin@123"),
                    name=f"Department Admin - {circle.circle_name}",
                    phone=f"91234{admin_counter:05d}",
                    role="department_admin",
                    department=department,
                    zone_id=circle.zone_id,
                    circle_id=circle.id
                ))
            admin_counter += 1

        # Backward-compatible admins
        original_admins = [
            ("ADMIN001", "admin1@grievancehub.com", "securepassword123", "Admin One", "9999999991"),
            ("ADMIN002", "admin2@grievancehub.com", "differentpassword456", "Admin Two", "9999999992"),
            ("ADMIN003", "supervisor@grievancehub.com", "supervisorpass789", "Supervisor", "9999999993"),
        ]

        for aid, aemail, apwd, aname, aphone in original_admins:
            if not Admin.query.filter_by(admin_id=aid).first():
                db.session.add(Admin(
                    admin_id=aid,
                    email=aemail,
                    password_hash=hash_password(apwd),
                    name=aname,
                    phone=aphone,
                    role="super_admin"
                ))

        db.session.commit()

        # Print summary
        zone_count = Zone.query.count()
        circle_count = Circle.query.count()
        area_count = Area.query.count()
        super_admin_count = Admin.query.filter_by(role='super_admin').count()
        sub_admin_count = Admin.query.filter_by(role='sub_admin').count()
        dept_admin_count = Admin.query.filter_by(role='department_admin').count()

        print("\n" + "=" * 50)
        print("DATABASE SEEDING COMPLETE")
        print("=" * 50)
        print(f"\nZones: {zone_count}")
        print(f"Circles: {circle_count}")
        print(f"Areas/Localities: {area_count}")
        print(f"\nAdmin Users:")
        print(f"  - Super Admins: {super_admin_count}")
        print(f"  - Sub Admins (Zone Level): {sub_admin_count}")
        print(f"  - Department Admins (Circle Level): {dept_admin_count}")
        print(f"  - Total: {super_admin_count + sub_admin_count + dept_admin_count}")
        print("\n" + "=" * 50)
        print("\nSample Login Credentials:")
        print("-" * 50)
        print("Super Admin:")
        print("  Email: superadmin@grievancehub.com")
        print("  Password: superadmin@123")
        print("\nZone 1 (Malkajgiri) Sub Admin:")
        print("  Email: zone1admin@grievancehub.com")
        print("  Password: zone1admin@123")
        print("\nDepartment Admin (Circle 1):")
        print("  Email: dept1@grievancehub.com")
        print("  Password: dept1admin@123")
        print("\nOriginal Admin (Backward Compatible):")
        print("  Email: admin1@grievancehub.com")
        print("  Password: securepassword123")
        print("=" * 50)


if __name__ == '__main__':
    seed_database()
