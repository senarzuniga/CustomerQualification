import json
from datetime import datetime


FALLBACK = {
    "revenue": 50.0,
    "revenue_currency": "EUR",
    "net_profit": 5.0,
    "ebitda": 8.0,
    "employees": 250,
    "growth_rate": 5.0,
    "margin": 10.0,
    "debt_ratio": 0.4,
    "revenue_trend_3y": [42.0, 46.0, 50.0],
    "data_source": "Estimacion sin API Key",
    "reliability": "BAJA",
    "year": datetime.now().year - 1,
    "is_estimated": True,
    "notes": "Datos estimados - Sin API Key disponible",
}


class FinancialIntelligenceAgent:
    def __init__(self, openai_client, hypothesis_engine):
        self.client = openai_client
        self.engine = hypothesis_engine

    def _chat(self, prompt: str) -> str:
        if self.client is None:
            return ""
        try:
            resp = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=2000
            )
            return resp.choices[0].message.content
        except Exception:
            return ""

    def _parse_json(self, text: str, fallback: dict) -> dict:
        if not text:
            return fallback
        try:
            start = text.find("{")
            end = text.rfind("}") + 1
            if start == -1:
                return fallback
            return json.loads(text[start:end])
        except Exception:
            return fallback

    def run(self, company_name: str, context: dict = None) -> dict:
        if context is None:
            context = {}
        current_year = datetime.now().year
        fb = FALLBACK.copy()
        fb["year"] = current_year - 1
        if self.client is None:
            return fb

        prompt = (
            f"Eres un analista financiero experto. Analiza los datos financieros de la empresa '{company_name}'.\n"
            f"Contexto: {json.dumps(context, ensure_ascii=False)[:500]}\n\n"
            f"Devuelve un JSON con exactamente estos campos:\n"
            f'{{"revenue": float (millones EUR), "revenue_currency": "EUR", "net_profit": float (millones EUR), '
            f'"ebitda": float (millones EUR), "employees": int, "growth_rate": float (% anual), '
            f'"margin": float (% margen neto), "debt_ratio": float (0-1), '
            f'"revenue_trend_3y": [float, float, float] (ultimos 3 anios en millones), '
            f'"data_source": str, "reliability": "ALTA/MEDIA/BAJA", "year": {current_year - 1}, '
            f'"is_estimated": bool, "notes": str}}\n\n'
            f"Usa datos reales si los conoces. Si no, estima con is_estimated=true.\n"
            f"Responde SOLO con el JSON."
        )
        raw = self._chat(prompt)
        return self._parse_json(raw, fb)
