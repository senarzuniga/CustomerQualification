import json


FALLBACK = {
    "market_size_bn": 5.0,
    "market_growth_rate": 4.0,
    "trends": ["Digitalizacion creciente", "Sostenibilidad", "Consolidacion del sector"],
    "entry_barriers": ["Capital inicial elevado", "Regulacion sectorial", "Relaciones establecidas"],
    "regulatory_risks": ["Cambios normativos", "Compliance"],
    "market_attractiveness": "Media",
    "competition_level": "Alta",
    "opportunities": ["Expansion geografica", "Nuevos segmentos", "Innovacion tecnologica"],
}


class MarketIntelligenceAgent:
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

    def run(self, company_name: str, sector: str, context: dict = None) -> dict:
        if context is None:
            context = {}
        if self.client is None:
            return FALLBACK.copy()

        prompt = (
            f"Eres un analista de mercado experto. Analiza el mercado para la empresa '{company_name}' en el sector '{sector}'.\n"
            f"Contexto: {json.dumps(context, ensure_ascii=False)[:500]}\n\n"
            f"Devuelve un JSON con exactamente estos campos:\n"
            f'{{"market_size_bn": float (tamano mercado en miles de millones EUR), '
            f'"market_growth_rate": float (% crecimiento anual), "trends": [str], '
            f'"entry_barriers": [str], "regulatory_risks": [str], '
            f'"market_attractiveness": str, "competition_level": str, "opportunities": [str]}}\n\n'
            f"Responde SOLO con el JSON."
        )
        raw = self._chat(prompt)
        return self._parse_json(raw, FALLBACK.copy())
