import sqlite3

# =====================================================
# DATABASE CONNECTION
# =====================================================

conn = sqlite3.connect(
    "goals.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =====================================================
# EMPLOYEES TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT UNIQUE,

    password TEXT,

    role TEXT,

    manager_name TEXT
)
""")

# =====================================================
# GOALS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS goals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name TEXT,
    title TEXT,
    target INTEGER,
    weightage INTEGER,
    approved INTEGER DEFAULT 0,
    locked INTEGER DEFAULT 0,
    achievement INTEGER DEFAULT 0,
    status TEXT DEFAULT 'Not Started',
    manager_comments TEXT DEFAULT '',
    q1_achievement REAL DEFAULT 0,
    q1_status TEXT DEFAULT 'Not Started',
    q2_achievement REAL DEFAULT 0,
    q2_status TEXT DEFAULT 'Not Started',
    q3_achievement REAL DEFAULT 0,
    q3_status TEXT DEFAULT 'Not Started',
    q4_achievement REAL DEFAULT 0,
    q4_status TEXT DEFAULT 'Not Started'
)
""")


try:
    cursor.execute("""ALTER TABLE goals ADD COLUMN q1_status TEXT""")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("""ALTER TABLE goals ADD COLUMN q2_status TEXT""")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("""ALTER TABLE goals ADD COLUMN q3_status TEXT""")
except sqlite3.OperationalError:
    pass

try:
    cursor.execute("""ALTER TABLE goals ADD COLUMN q4_status TEXT""")
except sqlite3.OperationalError:
    pass

# =====================================================
# INSERT DEMO EMPLOYEES
# =====================================================

employees = [

    ('Rahul', '123', 'Employee', 'Priya'),

    ('Aman', '123', 'Employee', 'Priya'),

    ('Priya', '123', 'Manager', ''),

    ('Admin', 'admin', 'Admin', '')
]

cursor.executemany("""
    INSERT OR IGNORE INTO employees
    (name, password, role, manager_name)
    VALUES (?, ?, ?, ?)
""", employees)


# =====================================================
# SAVE CHANGES
# =====================================================

conn.commit()

print("Database Connected Successfully")