import json


FALLBACK = {
    "competitors": [
        {"name": "Competidor A", "strengths": ["Marca conocida", "Escala"], "weaknesses": ["Alto coste", "Rigidez"], "market_share": "~20%"},
        {"name": "Competidor B", "strengths": ["Precio competitivo"], "weaknesses": ["Menos calidad"], "market_share": "~15%"},
    ],
    "competitive_map": "Mercado fragmentado con 2-3 actores dominantes",
    "competitive_advantages": ["Especializacion", "Relaciones con clientes"],
    "competitive_risks": ["Entrada de nuevos jugadores", "Guerra de precios"],
    "market_position": "Seguidor del mercado",
}


class CompetitiveIntelligenceAgent:
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
                max_tokens=2500
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
            f"Eres un analista de inteligencia competitiva. Analiza la competencia de '{company_name}' en el sector '{sector}'.\n"
            f"Contexto: {json.dumps(context, ensure_ascii=False)[:500]}\n\n"
            f"Devuelve un JSON con exactamente estos campos:\n"
            f'{{"competitors": [{{"name": str, "strengths": [str], "weaknesses": [str], "market_share": str}}], '
            f'"competitive_map": str, "competitive_advantages": [str], '
            f'"competitive_risks": [str], "market_position": str}}\n\n'
            f"Identifica 3-5 competidores reales. Responde SOLO con el JSON."
        )
        raw = self._chat(prompt)
        return self._parse_json(raw, FALLBACK.copy())
