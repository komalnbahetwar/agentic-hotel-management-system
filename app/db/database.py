import sqlite3
# --- SQLite DB ---
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(BASE_DIR, 'hotel_6.db')

def init_db():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    cur = conn.cursor()

    cur.execute("""
    DROP TABLE IF EXISTS rooms """)

    cur.execute("""
    DROP TABLE IF EXISTS reservations """)

    cur.execute("""
    DROP TABLE IF EXISTS menu """)

    cur.execute("""
    DROP TABLE IF EXISTS orders  """)


    # rooms table
    cur.execute("""
    CREATE TABLE rooms (
        room_number INTEGER UNIQUE PRIMARY KEY,
        status TEXT
    )
    """)
    
    # reservations table
    cur.execute("""
    CREATE TABLE reservations (
        reservation_id INTEGER PRIMARY KEY,
        guest_name TEXT,
        room_number INTEGER,
        FOREIGN KEY(room_number) REFERENCES rooms(room_number)
    )
    """)

    # menu table
    cur.execute("""
    CREATE TABLE menu  (
        item_name TEXT UNIQUE PRIMARY KEY,
        cuisine TEXT,
        price REAL NOT NULL,
        availability TEXT        
    )
    """)
    
    # orders table
    cur.execute("""
    CREATE TABLE orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        item_name TEXT NOT NULL,
        quantity INTEGER NOT NULL,
        room_number INTEGER NOT NULL,
    
        FOREIGN KEY(room_number) REFERENCES reservations(room_number)
        FOREIGN KEY (item_name) REFERENCES menu(item_name)
    )
    """)

    
    # Insert sample rooms
    cur.executemany("""
    INSERT OR IGNORE INTO rooms (room_number, status)
    VALUES (?, ?)
    """, [
        (101,"available"),
        (102,"occupied"),
        (103, "available"),
        (104, "available"),
        (105, "available"),
        (106, "occupied"),
        (201, "available"),
        (202, "occupied"),
        (203, "available"),
    ])

    # Insert sample menu
    cur.executemany("""
    INSERT OR IGNORE INTO menu (item_name, cuisine, price, availability)
    VALUES (?, ?, ?, ?)
    """, [
        ("Paneer Butter Masala + 2 Roti","North Indian",450,"available"),
        ("2 Idli + 2 Wada","South Indian",200,"available"),
        ("North Indian Thali","North Indian",510,"available"),
        ("South Indian Thali","South Indian",510,"available"),
        ("Pav Bhaji","North Indian",175,"available"),
        ("Manchurian","Chinese",310,"not available"),
        ("Pasta","Italian",360,"available"),
        ("Noodles","Chinese",310,"available"),
        ("Pizza","Italian",410,"not available"),
        
    ])

    
    conn.commit()
    conn.close()

    print("Hotel DB initialized.")