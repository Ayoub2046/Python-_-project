import sqlite3

def create_connection():
    conn = sqlite3.connect('employees.db')
    return conn

def create_table():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS employees (
                       id INTEGER PRIMARY KEY,
                       name TEXT NOT NULL,
                       phone TEXT NOT NULL,
                       role TEXT NOT NULL,
                       gender TEXT NOT NULL,
                       salary REAL NOT NULL)''')
    conn.commit()
    conn.close()

def insert_employee(employee):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO employees (id, name, phone, role, gender, salary) VALUES (?, ?, ?, ?, ?, ?)', employee)
    conn.commit()
    conn.close()

def fetch_all_employees():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM employees')
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_employee(employee):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''UPDATE employees SET name=?, phone=?, role=?, gender=?, salary=? WHERE id=?''',
                   (employee[1], employee[2], employee[3], employee[4], employee[5], employee[0]))
    conn.commit()
    conn.close()

def delete_employee(employee_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees WHERE id=?', (employee_id,))
    conn.commit()
    conn.close()

def delete_all_employees():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM employees')
    conn.commit()
    conn.close()
