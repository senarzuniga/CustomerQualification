import json


FALLBACK = {
    "valuation": {
        "estimated_value_m": 25.0,
        "min_value_m": 18.0,
        "max_value_m": 35.0,
        "confidence": "Media",
        "method": "Multiplos EV/EBITDA (estimacion)",
        "multiples_used": {"ebitda_multiple": "4-6x", "revenue_multiple": "0.5x"},
    },
    "sale_propensity": {
        "probability": "Media",
        "main_reasons": ["Mercado en consolidacion", "Oportunidad de salida favorable"],
        "buyer_types": ["Estrategico", "Private Equity"],
        "recommendation": "Preparar venta",
        "financial_indicators": {"crecimiento": "moderado", "margen": "bajo"},
        "strategic_indicators": {"diferenciacion": "media", "posicion": "seguidor"},
        "organizational_indicators": {"dependencia_fundador": "alta"},
        "contextual_indicators": {"consolidacion_sector": "activa"},
    },
}


class ValuationExitAgent:
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
            f"Eres un experto en valoracion de empresas y M&A. Valora la empresa '{company_name}' y evalua su propension a la venta.\n"
            f"Datos disponibles: {json.dumps(context, ensure_ascii=False)[:1500]}\n\n"
            f"Devuelve un JSON con exactamente estos campos:\n"
            f'{{"valuation": {{"estimated_value_m": float, "min_value_m": float, "max_value_m": float, '
            f'"confidence": str, "method": str, "multiples_used": {{"ebitda_multiple": str, "revenue_multiple": str}}}}, '
            f'"sale_propensity": {{"probability": "Alta/Media/Baja", "main_reasons": [str], '
            f'"buyer_types": [str], "recommendation": "Vender ahora/Preparar venta/No vender", '
            f'"financial_indicators": {{str: str}}, "strategic_indicators": {{str: str}}, '
            f'"organizational_indicators": {{str: str}}, "contextual_indicators": {{str: str}}}}}}\n\n'
            f"Sé preciso con la valoracion. Responde SOLO con el JSON."
        )
        raw = self._chat(prompt)
        return self._parse_json(raw, FALLBACK.copy())
