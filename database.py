import sqlite3

from config import DB_NAME, TABLE_NAME


def create_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER UNIQUE,
            start_date DATE,
            end_date DATE,
            is_approved BOOLEAN DEFAULT FALSE,
            places_to_visit TEXT,
            tasks TEXT,
            tickets_booked BOOLEAN DEFAULT FALSE
        )
    """)
    conn.commit()
    conn.close()


def save_vacation(chat_id, vacation):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        f"""
        INSERT OR REPLACE INTO {TABLE_NAME}
        (chat_id, start_date, end_date, is_approved, places_to_visit, tasks, tickets_booked)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """,  # noqa: E501
        (
            chat_id,
            vacation["start_date"],
            vacation["end_date"],
            vacation["is_approved"],
            vacation.get("places_to_visit", ""),
            vacation.get("tasks", ""),
            vacation["tickets_booked"],
        ),
    )
    conn.commit()
    conn.close()


def get_vacations(chat_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {TABLE_NAME} WHERE chat_id = ?", (chat_id,))
    result = cursor.fetchone()
    conn.close()
    return result if result else None
