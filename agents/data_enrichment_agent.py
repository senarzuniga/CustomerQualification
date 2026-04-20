import json


FALLBACK = {
    "company_name": "",
    "sector": "Industria General",
    "subsector": "Manufactura",
    "company_type": "Empresa Privada",
    "age_years": 15,
    "size": "Mediana empresa",
    "locations": ["Espana"],
    "organizational_structure": "Estructura funcional",
    "products_services": ["Productos industriales"],
    "market_positioning": "Posicionamiento medio",
    "website": "N/A",
    "founded_year": 2010,
    "employees": 200,
    "country": "Espana",
    "reliability": "BAJA",
    "data_quality": "BAJA",
}


class DataEnrichmentAgent:
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
        fb = FALLBACK.copy()
        fb["company_name"] = company_name
        if self.client is None:
            return fb

        prompt = (
            f"Eres un analista empresarial experto. Construye un perfil completo de la empresa '{company_name}'.\n"
            f"Contexto: {json.dumps(context, ensure_ascii=False)[:500]}\n\n"
            f"Devuelve un JSON con exactamente estos campos:\n"
            f'{{"company_name": str, "sector": str, "subsector": str, "company_type": str, '
            f'"age_years": int, "size": str, "locations": [str], "organizational_structure": str, '
            f'"products_services": [str], "market_positioning": str, "website": str, '
            f'"founded_year": int, "employees": int, "country": str, "reliability": "ALTA/MEDIA/BAJA", "data_quality": "ALTA/MEDIA/BAJA"}}\n\n'
            f"Usa tu conocimiento real de la empresa. Si no tienes datos seguros, estima de forma razonable.\n"
            f"Responde SOLO con el JSON."
        )
        raw = self._chat(prompt)
        return self._parse_json(raw, fb)
