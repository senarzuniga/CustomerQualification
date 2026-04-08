import pandas as pd
import numpy as np


class Analytics:
    @staticmethod
    def calculate_lead_score(lead: dict) -> int:
        """
        Score a lead 0-100 based on data completeness and presence of key CRM fields.
        Returns an integer score.
        """
        score = 0

        # Up to 50 pts for overall completeness
        total_fields = len(lead)
        filled_fields = sum(
            1 for v in lead.values() if v and str(v).strip() != ""
        )
        if total_fields > 0:
            score += int((filled_fields / total_fields) * 50)

        # Bonus points for high-value fields
        key_fields = {
            "email": 10,
            "phone": 8, "telefono": 8, "tel": 8,
            "company": 8, "empresa": 8, "compania": 8,
            "name": 5, "nombre": 5,
            "website": 5, "web": 5, "sitio": 5,
            "industry": 5, "industria": 5, "sector": 5,
            "country": 3, "pais": 3, "region": 3,
        }
        lead_lower = {k.lower(): v for k, v in lead.items()}
        for field, points in key_fields.items():
            val = lead_lower.get(field)
            if val and str(val).strip() != "":
                score += points

        return min(score, 100)

    @staticmethod
    def calculate_completeness(df: pd.DataFrame) -> pd.Series:
        """Return completeness percentage (0-100) per column."""
        return df.replace("", pd.NA).notna().mean().mul(100).round(1)

    @staticmethod
    def detect_key_columns(df: pd.DataFrame) -> dict:
        """
        Detect which columns likely correspond to common CRM fields.
        Returns a dict mapping semantic role -> actual column name.
        """
        candidates = {
            "name": ["name", "nombre", "full_name", "nombre_completo", "contact"],
            "email": ["email", "correo", "e_mail", "mail"],
            "phone": ["phone", "telefono", "tel", "mobile", "celular"],
            "company": ["company", "empresa", "compania", "organization", "org"],
            "industry": ["industry", "industria", "sector", "vertical"],
            "country": ["country", "pais", "region", "ciudad"],
            "score": ["score", "puntuacion", "calificacion", "rating", "rank"],
        }
        result = {}
        cols_lower = {c.lower(): c for c in df.columns}
        for role, keywords in candidates.items():
            for kw in keywords:
                if kw in cols_lower:
                    result[role] = cols_lower[kw]
                    break
        return result

    @staticmethod
    def score_dataframe(df: pd.DataFrame) -> pd.Series:
        """Apply calculate_lead_score to every row in a DataFrame."""
        return df.apply(
            lambda row: Analytics.calculate_lead_score(row.to_dict()), axis=1
        )