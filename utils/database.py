import sqlite3
import json
import os
from datetime import datetime
from pathlib import Path

DB_PATH = str(Path(__file__).parent.parent / "data" / "companies.db")


def _get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _init_db():
    conn = _get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS companies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sector TEXT DEFAULT '',
            country TEXT DEFAULT '',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS analyses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company_id INTEGER NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
            analysis_type TEXT NOT NULL,
            data TEXT NOT NULL,
            created_at TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


_init_db()


class CompanyDatabase:
    def save_company(self, name: str, sector: str = "", country: str = "") -> int:
        conn = _get_conn()
        now = datetime.utcnow().isoformat()
        cur = conn.execute(
            "INSERT INTO companies (name, sector, country, created_at, updated_at) VALUES (?, ?, ?, ?, ?)",
            (name, sector, country, now, now)
        )
        company_id = cur.lastrowid
        conn.commit()
        conn.close()
        return company_id

    def get_company(self, company_id: int) -> dict:
        conn = _get_conn()
        row = conn.execute("SELECT * FROM companies WHERE id = ?", (company_id,)).fetchone()
        conn.close()
        return dict(row) if row else {}

    def get_all_companies(self) -> list:
        conn = _get_conn()
        rows = conn.execute("SELECT * FROM companies ORDER BY created_at DESC").fetchall()
        conn.close()
        return [dict(r) for r in rows]

    def save_analysis(self, company_id: int, analysis_type: str, data_dict: dict) -> int:
        conn = _get_conn()
        now = datetime.utcnow().isoformat()
        cur = conn.execute(
            "INSERT INTO analyses (company_id, analysis_type, data, created_at) VALUES (?, ?, ?, ?)",
            (company_id, analysis_type, json.dumps(data_dict, ensure_ascii=False), now)
        )
        analysis_id = cur.lastrowid
        conn.commit()
        conn.close()
        return analysis_id

    def get_analyses(self, company_id: int, analysis_type: str = None) -> list:
        conn = _get_conn()
        if analysis_type:
            rows = conn.execute(
                "SELECT * FROM analyses WHERE company_id = ? AND analysis_type = ? ORDER BY created_at DESC",
                (company_id, analysis_type)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM analyses WHERE company_id = ? ORDER BY created_at DESC",
                (company_id,)
            ).fetchall()
        conn.close()
        results = []
        for r in rows:
            d = dict(r)
            try:
                d["data"] = json.loads(d["data"])
            except Exception:
                pass
            results.append(d)
        return results

    def get_latest_analysis(self, company_id: int, analysis_type: str) -> dict:
        rows = self.get_analyses(company_id, analysis_type)
        return rows[0]["data"] if rows else None

    def delete_company(self, company_id: int):
        conn = _get_conn()
        conn.execute("DELETE FROM analyses WHERE company_id = ?", (company_id,))
        conn.execute("DELETE FROM companies WHERE id = ?", (company_id,))
        conn.commit()
        conn.close()
