import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_file='projects.db'):
        self.db_file = db_file

    def get_connection(self):
        conn = sqlite3.connect(self.db_file)
        conn.row_factory = sqlite3.Row
        return conn

    def setup(self):
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    command TEXT NOT NULL,
                    status TEXT NOT NULL,
                    github_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')

    def create_project(self, name, command, status, github_url):
        with self.get_connection() as conn:
            conn.execute('''
                INSERT INTO projects (name, command, status, github_url)
                VALUES (?, ?, ?, ?)
            ''', (name, command, status, github_url))

    def get_all_projects(self):
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT * FROM projects ORDER BY created_at DESC')
            return [dict(row) for row in cursor.fetchall()]

    def get_project(self, project_id):
        with self.get_connection() as conn:
            cursor = conn.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def update_project(self, project_id, command):
        with self.get_connection() as conn:
            conn.execute('''
                UPDATE projects
                SET command = ?, status = 'Updated'
                WHERE id = ?
            ''', (command, project_id))

    def delete_project(self, project_id):
        with self.get_connection() as conn:
            conn.execute('DELETE FROM projects WHERE id = ?', (project_id,))
