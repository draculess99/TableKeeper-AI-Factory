from flask import Flask, render_template, request, jsonify
from datetime import datetime, timedelta, timezone
import sqlite3
import os

app = Flask(__name__)
app.config['ENV'] = os.getenv('FLASK_ENV', 'production')
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'false').lower() == 'true'

DB_PATH = 'tablekeeper.db'

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='restaurants'")
    if c.fetchone():
        conn.close()
        return

    c.execute('''CREATE TABLE restaurants
                 (id INTEGER PRIMARY KEY, name TEXT UNIQUE, timezone TEXT DEFAULT 'UTC')''')

    c.execute('''CREATE TABLE tables
                 (id INTEGER PRIMARY KEY, restaurant_id INTEGER, table_number INTEGER, capacity INTEGER,
                  FOREIGN KEY (restaurant_id) REFERENCES restaurants(id),
                  UNIQUE(restaurant_id, table_number))''')

    c.execute('''CREATE TABLE reservations
                 (id INTEGER PRIMARY KEY, table_id INTEGER, party_size INTEGER,
                  start_time TEXT, end_time TEXT, customer_name TEXT,
                  FOREIGN KEY (table_id) REFERENCES tables(id))''')

    conn.execute('CREATE INDEX idx_reservations_table_time ON reservations(table_id, start_time, end_time)')

    c.execute("INSERT INTO restaurants (id, name) VALUES (1, 'The Golden Fork')")
    c.execute("INSERT INTO restaurants (id, name) VALUES (2, 'Sunset Bistro')")

    c.execute("INSERT INTO tables (restaurant_id, table_number, capacity) VALUES (1, 1, 2)")
    c.execute("INSERT INTO tables (restaurant_id, table_number, capacity) VALUES (1, 2, 4)")
    c.execute("INSERT INTO tables (restaurant_id, table_number, capacity) VALUES (1, 3, 6)")
    c.execute("INSERT INTO tables (restaurant_id, table_number, capacity) VALUES (2, 1, 2)")
    c.execute("INSERT INTO tables (restaurant_id, table_number, capacity) VALUES (2, 2, 4)")

    now = datetime.now(timezone.utc)
    later = now + timedelta(hours=2)
    c.execute("INSERT INTO reservations (table_id, party_size, start_time, end_time, customer_name) VALUES (1, 2, ?, ?, 'Alice')",
              (now.isoformat(), later.isoformat()))

    conn.commit()
    conn.close()

def times_overlap(s1, e1, s2, e2):
    def as_utc(value):
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value.astimezone(timezone.utc)

    s1, e1, s2, e2 = map(as_utc, (s1, e1, s2, e2))
    return s1 < e2 and s2 < e1


def check_conflict(table_id, start_time, end_time, exclude_reservation_id=None):
    conn = get_db()
    c = conn.cursor()

    c.execute(
        "SELECT id, start_time, end_time FROM reservations WHERE table_id = ?",
        (table_id,)
    )
    for row in c.fetchall():
        if exclude_reservation_id and row['id'] == exclude_reservation_id:
            continue
        if times_overlap(start_time, end_time, row['start_time'], row['end_time']):
            conn.close()
            return True

    conn.close()
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/restaurants', methods=['GET'])
def get_restaurants():
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, name FROM restaurants")
    restaurants = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(restaurants)

@app.route('/api/tables/<int:restaurant_id>', methods=['GET'])
def get_tables(restaurant_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("SELECT id, table_number, capacity FROM tables WHERE restaurant_id = ? ORDER BY table_number", (restaurant_id,))
    tables = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(tables)

@app.route('/api/reservations', methods=['GET'])
def get_reservations():
    restaurant_id = request.args.get('restaurant_id', type=int)
    table_id = request.args.get('table_id', type=int)

    conn = get_db()
    c = conn.cursor()

    if table_id:
        c.execute("""SELECT r.id, r.table_id, r.party_size, r.start_time, r.end_time, r.customer_name,
                           t.table_number, rst.name as restaurant_name
                    FROM reservations r
                    JOIN tables t ON r.table_id = t.id
                    JOIN restaurants rst ON t.restaurant_id = rst.id
                    WHERE r.table_id = ?
                    ORDER BY r.start_time""", (table_id,))
    elif restaurant_id:
        c.execute("""SELECT r.id, r.table_id, r.party_size, r.start_time, r.end_time, r.customer_name,
                           t.table_number, rst.name as restaurant_name
                    FROM reservations r
                    JOIN tables t ON r.table_id = t.id
                    JOIN restaurants rst ON t.restaurant_id = rst.id
                    WHERE t.restaurant_id = ?
                    ORDER BY r.start_time""", (restaurant_id,))
    else:
        c.execute("""SELECT r.id, r.table_id, r.party_size, r.start_time, r.end_time, r.customer_name,
                           t.table_number, rst.name as restaurant_name
                    FROM reservations r
                    JOIN tables t ON r.table_id = t.id
                    JOIN restaurants rst ON t.restaurant_id = rst.id
                    ORDER BY r.start_time""")

    reservations = [dict(row) for row in c.fetchall()]
    conn.close()
    return jsonify(reservations)

@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    data = request.json

    try:
        table_id = int(data['table_id'])
        party_size = int(data['party_size'])
        start_time = data['start_time']
        end_time = data['end_time']
        customer_name = data.get('customer_name', 'Guest').strip()
    except (ValueError, KeyError) as e:
        return jsonify({'error': 'Invalid input data'}), 400

    if not customer_name:
        return jsonify({'error': 'Customer name is required'}), 400

    try:
        start = datetime.fromisoformat(start_time)
        end = datetime.fromisoformat(end_time)
    except ValueError:
        return jsonify({'error': 'Invalid date/time format'}), 400

    if start >= end:
        return jsonify({'error': 'Start time must be before end time'}), 400

    if end - start > timedelta(hours=4):
        return jsonify({'error': 'Reservation cannot exceed 4 hours'}), 400

    if party_size < 1 or party_size > 20:
        return jsonify({'error': 'Party size must be between 1 and 20'}), 400

    conn = get_db()
    c = conn.cursor()

    c.execute("SELECT capacity FROM tables WHERE id = ?", (table_id,))
    table = c.fetchone()
    if not table:
        conn.close()
        return jsonify({'error': 'Table not found'}), 404

    if party_size > table['capacity']:
        conn.close()
        return jsonify({'error': f"Party size exceeds table capacity ({table['capacity']})"}), 400

    if check_conflict(table_id, start, end):
        conn.close()
        return jsonify({'error': 'Table is already booked for this time period'}), 409

    try:
        c.execute("""INSERT INTO reservations (table_id, party_size, start_time, end_time, customer_name)
                     VALUES (?, ?, ?, ?, ?)""",
                  (table_id, party_size, start_time, end_time, customer_name))
        conn.commit()
        reservation_id = c.lastrowid
        conn.close()
        return jsonify({'id': reservation_id, 'message': 'Reservation created successfully'}), 201
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/reservations/<int:reservation_id>', methods=['DELETE'])
def delete_reservation(reservation_id):
    conn = get_db()
    c = conn.cursor()
    c.execute("DELETE FROM reservations WHERE id = ?", (reservation_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Reservation deleted'}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=app.config['DEBUG'], port=int(os.getenv('PORT', 5000)))
