import json


class ReportGenerationAgent:
    def __init__(self, openai_client):
        self.client = openai_client

    def _chat(self, prompt: str, max_tokens: int = 3000) -> str:
        if self.client is None:
            return ""
        try:
            resp = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.4,
                max_tokens=max_tokens
            )
            return resp.choices[0].message.content
        except Exception:
            return ""

    def generate_executive_summary(self, all_analysis: dict) -> str:
        company = all_analysis.get("company_name", "la empresa")
        if self.client is None:
            fin = all_analysis.get("financial", {})
            val = all_analysis.get("valuation", {}).get("valuation", {})
            sale = all_analysis.get("valuation", {}).get("sale_propensity", {})
            return (
                f"**{company}** es una empresa analizada mediante el sistema de inteligencia empresarial.\n\n"
                f"Los datos financieros muestran ingresos estimados de {fin.get('revenue', 'N/D')} M EUR "
                f"con un EBITDA de {fin.get('ebitda', 'N/D')} M EUR. "
                f"La valoracion estimada oscila entre {val.get('min_value_m', 'N/D')} y {val.get('max_value_m', 'N/D')} M EUR.\n\n"
                f"**Recomendacion**: {sale.get('recommendation', 'Pendiente de analisis con API Key')}."
            )

        context_summary = json.dumps({
            "financial": all_analysis.get("financial", {}),
            "market": all_analysis.get("market", {}),
            "competitive": all_analysis.get("competitive", {}),
            "strategic": all_analysis.get("strategic", {}),
            "valuation": all_analysis.get("valuation", {}),
        }, ensure_ascii=False)[:2500]

        prompt = (
            f"Eres un consultor senior de McKinsey. Escribe un Executive Summary profesional para el informe de '{company}'.\n"
            f"Datos del analisis: {context_summary}\n\n"
            f"El resumen debe:\n"
            f"- Tener 4-5 parrafos concisos\n"
            f"- Destacar los hallazgos clave: situacion financiera, posicion competitiva, valoracion, propension a venta\n"
            f"- Terminar con la recomendacion principal\n"
            f"- Nivel: consultoría de alto nivel, claro y accionable\n"
            f"- Idioma: espanol\n"
            f"Escribe el resumen directamente, sin titulos adicionales."
        )
        result = self._chat(prompt, max_tokens=1500)
        if not result:
            return f"Analisis completado para {company}. Ver secciones detalladas del informe."
        return result

    def generate_full_report_text(self, company_name: str, all_analysis: dict) -> str:
        if self.client is None:
            return self._build_static_report(company_name, all_analysis)

        context = json.dumps(all_analysis, ensure_ascii=False)[:3000]
        prompt = (
            f"Eres un consultor senior. Genera un informe estrategico completo en Markdown para '{company_name}'.\n"
            f"Datos: {context}\n\n"
            f"Estructura obligatoria (usa ## para secciones):\n"
            f"1. Executive Summary\n2. Company Overview\n3. Financial Analysis\n"
            f"4. Product & Business Model\n5. Market Analysis\n6. Competitive Analysis\n"
            f"7. Strategic Analysis (incluye SWOT)\n8. Valuation\n9. Exit / Sale Analysis\n"
            f"10. Future Scenarios (5 y 10 anos)\n11. Recommendations\n\n"
            f"Estilo: McKinsey/Bain. Claro, accionable, sin relleno. Idioma: espanol."
        )
        result = self._chat(prompt, max_tokens=4000)
        if not result:
            return self._build_static_report(company_name, all_analysis)
        return result

    def _build_static_report(self, company_name: str, data: dict) -> str:
        fin = data.get("financial", {})
        mkt = data.get("market", {})
        comp = data.get("competitive", {})
        strat = data.get("strategic", {})
        val = data.get("valuation", {})
        swot = strat.get("swot", {})
        valuation = val.get("valuation", {})
        sale = val.get("sale_propensity", {})
        enrich = data.get("enrichment", {})

        lines = [
            f"# Informe Estrategico: {company_name}",
            "",
            "## 1. Executive Summary",
            data.get("executive_summary", "Ver analisis detallado a continuacion."),
            "",
            "## 2. Company Overview",
            f"- **Sector**: {enrich.get('sector', 'N/D')}",
            f"- **Pais**: {enrich.get('country', 'N/D')}",
            f"- **Empleados**: {enrich.get('employees', 'N/D')}",
            f"- **Tipo**: {enrich.get('company_type', 'N/D')}",
            "",
            "## 3. Financial Analysis",
            f"- **Ingresos**: {fin.get('revenue', 'N/D')} M EUR",
            f"- **EBITDA**: {fin.get('ebitda', 'N/D')} M EUR",
            f"- **Margen neto**: {fin.get('margin', 'N/D')}%",
            f"- **Crecimiento**: {fin.get('growth_rate', 'N/D')}%",
            f"- **Fiabilidad datos**: {fin.get('reliability', 'N/D')}",
            "",
            "## 4. Market Analysis",
            f"- **Tamano mercado**: {mkt.get('market_size_bn', 'N/D')} Bn EUR",
            f"- **Crecimiento mercado**: {mkt.get('market_growth_rate', 'N/D')}%",
            f"- **Atractivo**: {mkt.get('market_attractiveness', 'N/D')}",
            "",
            "## 5. Competitive Analysis",
            f"- **Posicion**: {comp.get('market_position', 'N/D')}",
            f"- **Mapa competitivo**: {comp.get('competitive_map', 'N/D')}",
            "",
            "## 6. Strategic Analysis (SWOT)",
            "**Fortalezas**: " + ", ".join(swot.get("strengths", [])),
            "**Debilidades**: " + ", ".join(swot.get("weaknesses", [])),
            "**Oportunidades**: " + ", ".join(swot.get("opportunities", [])),
            "**Amenazas**: " + ", ".join(swot.get("threats", [])),
            "",
            "## 7. Valuation",
            f"- **Valor estimado**: {valuation.get('estimated_value_m', 'N/D')} M EUR",
            f"- **Rango**: {valuation.get('min_value_m', 'N/D')} - {valuation.get('max_value_m', 'N/D')} M EUR",
            f"- **Metodo**: {valuation.get('method', 'N/D')}",
            f"- **Confianza**: {valuation.get('confidence', 'N/D')}",
            "",
            "## 8. Exit / Sale Analysis",
            f"- **Propension a venta**: {sale.get('probability', 'N/D')}",
            f"- **Recomendacion**: {sale.get('recommendation', 'N/D')}",
            f"- **Compradores potenciales**: {', '.join(sale.get('buyer_types', []))}",
            "",
            "## 9. Future Scenarios",
            "**5 Anos - Mas probable**: " + strat.get("scenario_5y", {}).get("most_likely", "N/D"),
            "**10 Anos - Mas probable**: " + strat.get("scenario_10y", {}).get("most_likely", "N/D"),
            "",
            "## 10. Recommendations",
            f"Recomendacion principal: {sale.get('recommendation', 'Analisis con API Key para recomendaciones detalladas')}",
        ]
        return "\n".join(lines)
