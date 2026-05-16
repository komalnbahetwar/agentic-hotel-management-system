import sqlite3
from app.db.database import DB_FILE

from langchain_core.tools import tool


@tool
def check_availability_tool() -> str:
    """Check which rooms are available in the hotel."""
    print(f" CALLING Tool: check_availability_tool()")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM rooms WHERE status='available'")
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "No rooms available."
    print(f"Tool Output: {rows}")
    return f"Available rooms: {', '.join(str(r[0]) for r in rows)}"


@tool
def book_room_tool(guest_name: str, room_number: int) -> str:
    """Book the SPECIFIC room requested by the guest. 
    The `room_number` argument MUST always be passed exactly as the user asked.
    First check if the room_number is available,
    If that room is not available, return an error message instead of booking another room."""

    print(f" CALLING Tool: book_room_tool()")
    print(f" PARAMS: guest_name='{guest_name}', room_number={room_number}")

    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    if room_number:
        # Book specific room
        cursor.execute("SELECT * FROM rooms WHERE room_number=? AND status='available'", (room_number,))
        room = cursor.fetchone()
        if not room:
            conn.close()
            return f"Room {room_number} is not available."
        target_room = room_number
    else:
        return f"Room {room_number} is not a valid room number."
    
    cursor.execute("UPDATE rooms SET status='occupied' WHERE room_number=?", (target_room,))
    cursor.execute("INSERT INTO reservations (guest_name, room_number) VALUES (?, ?)",
                   (guest_name, target_room))
    conn.commit()
    conn.close()
    print(f"Tool Output: Room {target_room} booked for {guest_name}.")
    return f"Room {target_room} booked for {guest_name}."


@tool
def get_menu() -> str:
    """Get the current menu with availability."""
    print(f" CALLING Tool: get_menu() Tool")

    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT item_name, cuisine, price FROM menu WHERE availability = 'available' ")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return "Menu is currently empty."

    menu_str = "\n".join(
        [f"{name} ({cuisine}) - ₹{price}]"
         for name, cuisine, price in rows]
    )
    print(f"Tool Output: Today's Menu:\n  {menu_str}")
    return "Today's Menu:\n" + menu_str


@tool
def order_food(item_name: str, quantity: int, room_number: int) -> str:
    """Place a food order for a guest (linked to room)."""

    print(f" CALLING Tool: order_food()")
    print(f" PARAMS: item_name='{item_name}', quantity='{quantity}', room_number={room_number}")

    
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    # Validate room
    c.execute("SELECT status FROM rooms WHERE room_number = ?", (room_number,))
    room = c.fetchone()
    if not room:
        conn.close()
        return f"Room {room_number} does not exist."
    if room[0] != "occupied":
        conn.close()
        return f"Room {room_number} is not occupied."

    # Validate dish
    c.execute("SELECT availability FROM menu WHERE item_name = ?", (item_name,))
    row = c.fetchone()
    if not row:
        conn.close()
        return f"Item Name '{item_name}' not found in menu."
    if row[0] == "not available":
        conn.close()
        return f"Sorry, '{item_name}' is not available right now."

    # Insert order
    c.execute("INSERT INTO orders (item_name, quantity, room_number) VALUES (?, ?, ?)",
              (item_name, quantity, room_number))
    order_id = c.lastrowid
    conn.commit()
    conn.close()

    print(f"Tool Output => Order placed: {quantity} x {item_name} for Room {room_number}. Order ID: {order_id}.")

    return f"Order placed: {quantity} x {item_name} for Room {room_number}. Order ID: {order_id}."



@tool
def get_food_bill(room_number: int) -> str:
    """Calculate the total food bill for a room."""

    print(f" CALLING Tool: get_food_bill()")
    print(f" PARAMS: room_number={room_number}")


    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
        SELECT o.item_name, o.quantity, m.price
        FROM orders o
        JOIN menu m ON o.item_name = m.item_name
        WHERE o.room_number = ?
    """, (room_number,))
    rows = c.fetchall()
    conn.close()

    if not rows:
        return f"No active food orders found for Room {room_number}."

    total = 0
    bill_lines = []
    for dish, quantity, price in rows:
        subtotal = quantity * price
        total += subtotal
        bill_lines.append(f"{dish} x {quantity} = ₹{subtotal}")

    bill = "\n".join(bill_lines) + f"\n\n Total Bill: ₹{total}"

    print(f"Tool Output {bill}")
    return bill





