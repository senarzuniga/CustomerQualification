try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

from agents.hypothesis_engine import HypothesisEngine
from agents.data_enrichment_agent import DataEnrichmentAgent
from agents.financial_intelligence_agent import FinancialIntelligenceAgent
from agents.market_intelligence_agent import MarketIntelligenceAgent
from agents.competitive_intelligence_agent import CompetitiveIntelligenceAgent
from agents.strategic_analysis_agent import StrategicAnalysisAgent
from agents.valuation_exit_agent import ValuationExitAgent
from agents.report_generation_agent import ReportGenerationAgent


class AnalysisOrchestrator:
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self._client = None
        if api_key and OpenAI:
            try:
                self._client = OpenAI(api_key=api_key)
            except Exception:
                self._client = None

        self.hypothesis_engine = HypothesisEngine(self._client)
        self.enrichment_agent = DataEnrichmentAgent(self._client, self.hypothesis_engine)
        self.financial_agent = FinancialIntelligenceAgent(self._client, self.hypothesis_engine)
        self.market_agent = MarketIntelligenceAgent(self._client, self.hypothesis_engine)
        self.competitive_agent = CompetitiveIntelligenceAgent(self._client, self.hypothesis_engine)
        self.strategic_agent = StrategicAnalysisAgent(self._client, self.hypothesis_engine)
        self.valuation_agent = ValuationExitAgent(self._client, self.hypothesis_engine)
        self.report_agent = ReportGenerationAgent(self._client)

        self._status = {k: "pending" for k in ["enrichment", "financial", "market", "competitive", "strategic", "valuation", "report"]}

    def get_analysis_status(self) -> dict:
        return self._status.copy()

    def run_full_analysis(self, company_name: str, sector: str = "", country: str = "") -> dict:
        results = {"company_name": company_name}

        self._status["enrichment"] = "running"
        try:
            enrichment = self.enrichment_agent.run(company_name, {"sector": sector, "country": country})
            results["enrichment"] = enrichment
            if not sector:
                sector = enrichment.get("sector", "")
            if not country:
                country = enrichment.get("country", "")
            self._status["enrichment"] = "completed"
        except Exception as e:
            results["enrichment"] = {"error": str(e), "company_name": company_name}
            self._status["enrichment"] = "error"

        self._status["financial"] = "running"
        try:
            results["financial"] = self.financial_agent.run(company_name, {"sector": sector, "country": country})
            self._status["financial"] = "completed"
        except Exception as e:
            results["financial"] = {"error": str(e)}
            self._status["financial"] = "error"

        self._status["market"] = "running"
        try:
            results["market"] = self.market_agent.run(company_name, sector, {"country": country})
            self._status["market"] = "completed"
        except Exception as e:
            results["market"] = {"error": str(e)}
            self._status["market"] = "error"

        self._status["competitive"] = "running"
        try:
            results["competitive"] = self.competitive_agent.run(company_name, sector, {"country": country, "market": results.get("market", {})})
            self._status["competitive"] = "completed"
        except Exception as e:
            results["competitive"] = {"error": str(e)}
            self._status["competitive"] = "error"

        self._status["strategic"] = "running"
        try:
            ctx = {k: results.get(k, {}) for k in ["financial", "market", "competitive", "enrichment"]}
            results["strategic"] = self.strategic_agent.run(company_name, ctx)
            self._status["strategic"] = "completed"
        except Exception as e:
            results["strategic"] = {"error": str(e)}
            self._status["strategic"] = "error"

        self._status["valuation"] = "running"
        try:
            ctx = {k: results.get(k, {}) for k in ["financial", "market", "competitive", "strategic", "enrichment"]}
            results["valuation"] = self.valuation_agent.run(company_name, ctx)
            self._status["valuation"] = "completed"
        except Exception as e:
            results["valuation"] = {"error": str(e)}
            self._status["valuation"] = "error"

        self._status["report"] = "running"
        try:
            results["executive_summary"] = self.report_agent.generate_executive_summary(results)
            results["report_text"] = self.report_agent.generate_full_report_text(company_name, results)
            self._status["report"] = "completed"
        except Exception as e:
            results["executive_summary"] = f"Error generando resumen: {e}"
            results["report_text"] = f"# Informe: {company_name}\n\nError en generacion: {e}"
            self._status["report"] = "error"

        return results
