import json


class HypothesisEngine:
    def __init__(self, openai_client):
        self.client = openai_client

    def _chat(self, messages: list, temperature: float = 0.3) -> str:
        if self.client is None:
            return ""
        try:
            resp = self.client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                temperature=temperature,
                max_tokens=2000
            )
            return resp.choices[0].message.content
        except Exception:
            return ""

    def _parse_json(self, text: str, fallback):
        if not text:
            return fallback
        try:
            bracket = "[" if isinstance(fallback, list) else "{"
            end_bracket = "]" if isinstance(fallback, list) else "}"
            start = text.find(bracket)
            end = text.rfind(end_bracket) + 1
            if start == -1 or end == 0:
                return fallback
            return json.loads(text[start:end])
        except Exception:
            return fallback

    def generate_hypotheses(self, question: str, context: dict, num: int = 3) -> list:
        if self.client is None:
            return [
                {"id": i + 1, "hypothesis": f"Hipotesis {i + 1} (sin API)", "approach": "Analisis general", "data_sources": ["Datos internos"]}
                for i in range(num)
            ]
        prompt = (
            f"Genera {num} hipotesis analiticas para responder la siguiente pregunta de negocio.\n"
            f"Pregunta: {question}\n"
            f"Contexto disponible: {json.dumps(context, ensure_ascii=False)[:800]}\n\n"
            f"Devuelve un JSON array con exactamente {num} objetos, cada uno con:\n"
            f"- id (int)\n- hypothesis (str)\n- approach (str)\n- data_sources (list)\n\n"
            f"Responde SOLO con el JSON array."
        )
        raw = self._chat([{"role": "user", "content": prompt}])
        fallback = [
            {"id": i + 1, "hypothesis": f"Hipotesis {i + 1}", "approach": "Analisis general", "data_sources": ["Datos del mercado"]}
            for i in range(num)
        ]
        return self._parse_json(raw, fallback)

    def evaluate_hypothesis(self, hypothesis: dict, result: dict) -> dict:
        if self.client is None:
            return {"score": 0.7, "data_quality": "MEDIA", "relevance": "Alta", "reliability": "MEDIA", "justification": "Evaluacion sin API"}
        prompt = (
            f"Evalua la calidad de esta hipotesis y su resultado:\n"
            f"Hipotesis: {json.dumps(hypothesis, ensure_ascii=False)}\n"
            f"Resultado: {json.dumps(result, ensure_ascii=False)[:800]}\n\n"
            f"Devuelve un JSON con: score (float 0-1), data_quality (ALTA/MEDIA/BAJA), "
            f"relevance (str), reliability (ALTA/MEDIA/BAJA), justification (str).\n"
            f"Responde SOLO con el JSON."
        )
        raw = self._chat([{"role": "user", "content": prompt}])
        return self._parse_json(raw, {"score": 0.5, "data_quality": "MEDIA", "relevance": "Media", "reliability": "MEDIA", "justification": "Error en evaluacion"})

    def select_best(self, hypotheses_with_results: list) -> dict:
        if not hypotheses_with_results:
            return {}
        scored = sorted(hypotheses_with_results, key=lambda x: x.get("evaluation", {}).get("score", 0), reverse=True)
        best = scored[0]
        best["selection_justification"] = "Hipotesis seleccionada por mayor puntuacion combinada"
        return best

    def run_analysis(self, question: str, context: dict, executor_fn, num_hypotheses: int = 3) -> dict:
        hypotheses = self.generate_hypotheses(question, context, num_hypotheses)
        results = []
        for hyp in hypotheses:
            try:
                result = executor_fn(hyp)
            except Exception as e:
                result = {"error": str(e)}
            evaluation = self.evaluate_hypothesis(hyp, result)
            results.append({"hypothesis": hyp, "result": result, "evaluation": evaluation})
        best = self.select_best(results)
        return {
            "question": question,
            "hypotheses_evaluated": len(results),
            "best": best,
            "all_results": results
        }
