import json


FALLBACK = {
    "swot": {
        "strengths": ["Equipo experimentado", "Base de clientes solida"],
        "weaknesses": ["Limitada escala", "Dependencia del fundador"],
        "opportunities": ["Expansion digital", "Nuevos mercados"],
        "threats": ["Competencia creciente", "Cambios regulatorios"],
    },
    "current_situation": "Empresa en fase de consolidacion con posicion estable en el mercado.",
    "trajectory": "Crecimiento moderado con presion competitiva al alza.",
    "key_risks": ["Perdida de clientes clave", "Competencia de actores globales"],
    "scenario_5y": {
        "best": "Crecimiento de dos digitos via expansion geografica y digital.",
        "worst": "Estancamiento por presion de precios y entrada de competidores.",
        "most_likely": "Crecimiento moderado del 5-8% anual con mejora de margenes.",
    },
    "scenario_10y": {
        "best": "Liderazgo regional y posible salida a bolsa o venta estrategica.",
        "worst": "Erosion significativa de cuota de mercado.",
        "most_likely": "Consolidacion como actor relevante en su nicho con posible M&A.",
    },
}


class StrategicAnalysisAgent:
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
                max_tokens=3000
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
        if self.client is None:
            return FALLBACK.copy()

        prompt = (
            f"Eres un consultor estrategico senior. Realiza un analisis estrategico completo de '{company_name}'.\n"
            f"Datos disponibles: {json.dumps(context, ensure_ascii=False)[:1200]}\n\n"
            f"Devuelve un JSON con exactamente estos campos:\n"
            f'{{"swot": {{"strengths": [str], "weaknesses": [str], "opportunities": [str], "threats": [str]}}, '
            f'"current_situation": str, "trajectory": str, "key_risks": [str], '
            f'"scenario_5y": {{"best": str, "worst": str, "most_likely": str}}, '
            f'"scenario_10y": {{"best": str, "worst": str, "most_likely": str}}}}\n\n'
            f"Nivel consultoría McKinsey/Bain. Responde SOLO con el JSON."
        )
        raw = self._chat(prompt)
        return self._parse_json(raw, FALLBACK.copy())
