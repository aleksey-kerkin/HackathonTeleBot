import sqlite3


def init_db():
    conn = sqlite3.connect("vacation_planner.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vacations (
            user_id INTEGER PRIMARY KEY,
            destination TEXT,
            tasks TEXT,
            days_left INTEGER
            );
        """)
    conn.commit()
    conn.close()


def save_vacation_plan(user_id, destination, tasks, days_left):
    conn = sqlite3.connect("vacation_planner.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT OR REPLACE INTO vacations (user_id, destination, tasks, days_left)
        VALUES (?, ?, ?, ?);
        """,
        (user_id, destination, tasks, days_left),
    )
    conn.commit()
    conn.close()


def get_vacation_plan(user_id):
    conn = sqlite3.connect("vacation_planner.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM vacations WHERE user_id = ?;", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result
