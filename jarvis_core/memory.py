import sqlite3
import datetime
import os

class MemoryManager:
    def __init__(self, db_path="assets/jarvis_memory.db"):
        os.makedirs("assets", exist_ok=True)
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Table for reminders
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                task TEXT,
                due_time TEXT,
                status TEXT DEFAULT 'pending'
            )
        ''')
        # Table for user preferences/facts
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_facts (
                fact_key TEXT PRIMARY KEY,
                fact_value TEXT
            )
        ''')
        self.conn.commit()

    def add_reminder(self, task: str, due_time: str) -> str:
        """Adds a reminder. due_time should be in ISO format or similar."""
        cursor = self.conn.cursor()
        cursor.execute("INSERT INTO reminders (task, due_time) VALUES (?, ?)", (task, due_time))
        self.conn.commit()
        return f"I've added that to your schedule, Sir: {task} at {due_time}."

    def get_reminders(self) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT task, due_time FROM reminders WHERE status = 'pending'")
        rows = cursor.fetchall()
        if not rows:
            return "You have no pending reminders, Sir."
        return "Here are your reminders, Sir: " + "; ".join([f"{r[0]} at {r[1]}" for r in rows])

    def store_fact(self, key: str, value: str):
        cursor = self.conn.cursor()
        cursor.execute("INSERT OR REPLACE INTO user_facts (fact_key, fact_value) VALUES (?, ?)", (key, value))
        self.conn.commit()
        return f"I'll keep that in mind, Sir."

    def get_fact(self, key: str) -> str:
        cursor = self.conn.cursor()
        cursor.execute("SELECT fact_value FROM user_facts WHERE fact_key = ?", (key,))
        row = cursor.fetchone()
        return row[0] if row else "I don't recall that, Sir."

# Export for Gemini
memory_manager = MemoryManager()
memory_tools = [memory_manager.add_reminder, memory_manager.get_reminders, memory_manager.store_fact, memory_manager.get_fact]
