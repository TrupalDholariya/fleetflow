"""
🚛 Fleet Management Database - SQLite ONLY
NO extra installs required!
"""

import sqlite3
from datetime import datetime
from typing import List, Dict, Any

# ========================================
# DATABASE CONFIG - SQLite Only
# ========================================
DATABASE_CONFIG = {
    "database": "fleet_system.db"  # Auto-created!
}

# ========================================
# TABLES (Auto-create)
# ========================================
TABLES = {
    "vehicles": """
    CREATE TABLE IF NOT EXISTS vehicles (
        id TEXT PRIMARY KEY,
        capacity_kg INTEGER,
        fuel_level_percent INTEGER,
        status TEXT,
        current_lat REAL,
        current_lng REAL,
        last_update TEXT,
        driver_score REAL
    )
    """,
    "drivers": """
    CREATE TABLE IF NOT EXISTS drivers (
        id TEXT PRIMARY KEY,
        name TEXT,
        availability TEXT,
        driver_score REAL,
        hours_driven_today REAL,
        phone TEXT
    )
    """,
    "orders": """
    CREATE TABLE IF NOT EXISTS orders (
        id TEXT PRIMARY KEY,
        pickup_lat REAL,
        pickup_lng REAL,
        dest_lat REAL,
        dest_lng REAL,
        load_kg INTEGER,
        status TEXT,
        created_at TEXT
    )
    """,
    "trips": """
    CREATE TABLE IF NOT EXISTS trips (
        id TEXT PRIMARY KEY,
        vehicle_id TEXT,
        driver_id TEXT,
        order_id TEXT,
        status TEXT,
        started_at TEXT,
        completed_at TEXT
    )
    """
}

class FleetDatabase:
    """🚛 SQLite Database - Plug & Play!"""
    
    def __init__(self, database_file="fleet_system.db"):
        self.database_file = database_file
        self.conn = sqlite3.connect(database_file, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row  # Dict-like rows
        self.create_tables()
        print(f"✅ SQLite ready: {database_file}")
    
    def create_tables(self):
        """Auto-create all tables"""
        cursor = self.conn.cursor()
        for sql in TABLES.values():
            cursor.execute(sql)
        self.conn.commit()
    
    def get_vehicles(self) -> List[Dict]:
        """Get all vehicles"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vehicles")
        return [dict(row) for row in cursor.fetchall()]
    
    def get_vehicle(self, vehicle_id: str) -> Dict:
        """Get single vehicle"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM vehicles WHERE id = ?", (vehicle_id,))
        row = cursor.fetchone()
        return dict(row) if row else {}
    
    def update_vehicle(self, vehicle_id: str, data: Dict):
        """Driver GPS/fuel update"""
        cursor = self.conn.cursor()
        set_parts = [f"{k} = ?" for k in data.keys()]
        values = list(data.values()) + [datetime.now().isoformat(), vehicle_id]
        cursor.execute(
            f"UPDATE vehicles SET {', '.join(set_parts)}, last_update = ? WHERE id = ?",
            values
        )
        self.conn.commit()
    
    def get_drivers(self) -> List[Dict]:
        """Get all drivers"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM drivers")
        return [dict(row) for row in cursor.fetchall()]
    
    def update_driver(self, driver_id: str, data: Dict):
        """Driver status update"""
        cursor = self.conn.cursor()
        set_parts = [f"{k} = ?" for k in data.keys()]
        values = list(data.values()) + [driver_id]
        cursor.execute(
            f"UPDATE drivers SET {', '.join(set_parts)} WHERE id = ?",
            values
        )
        self.conn.commit()
    
    def add_order(self, order_data: Dict) -> Dict:
        """User adds order"""
        order_id = f"ORD_{int(datetime.now().timestamp())}"
        order = {
            **order_data,
            "id": order_id,
            "status": "pending",
            "created_at": datetime.now().isoformat()
        }
        
        cursor = self.conn.cursor()
        columns = ", ".join(order.keys())
        placeholders = ", ".join("?" * len(order))
        cursor.execute(f"INSERT INTO orders ({columns}) VALUES ({placeholders})", 
                      list(order.values()))
        self.conn.commit()
        return order
    
    def get_orders(self, status: str = None) -> List[Dict]:
        """Get orders by status"""
        cursor = self.conn.cursor()
        if status:
            cursor.execute("SELECT * FROM orders WHERE status = ?", (status,))
        else:
            cursor.execute("SELECT * FROM orders ORDER BY created_at DESC")
        return [dict(row) for row in cursor.fetchall()]
    
    def assign_trip(self, vehicle_id: str, driver_id: str, order_id: str) -> Dict:
        """Assign trip"""
        trip_id = f"TRIP_{int(datetime.now().timestamp())}"
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO trips (id, vehicle_id, driver_id, order_id, status, started_at)
            VALUES (?, ?, ?, ?, 'assigned', ?)
        """, (trip_id, vehicle_id, driver_id, order_id, datetime.now().isoformat()))
        
        # Update statuses
        cursor.execute("UPDATE vehicles SET status = 'in_transit' WHERE id = ?", (vehicle_id,))
        cursor.execute("UPDATE drivers SET availability = 'busy' WHERE id = ?", (driver_id,))
        cursor.execute("UPDATE orders SET status = 'assigned' WHERE id = ?", (order_id,))
        
        self.conn.commit()
        return {"id": trip_id, "status": "assigned"}

# ========================================
# READY INSTANCE
# ========================================
db = FleetDatabase()

if __name__ == "__main__":
    print("🚛 Database ready!")
    print(f"File: fleet_system.db (auto-created)")
    print("Use: from mock_data import db")
