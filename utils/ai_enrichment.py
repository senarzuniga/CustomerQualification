import pandas as pd

class AIEnrichment:
    def __init__(self, api_key=None):
        self.api_key = api_key
    
    def enrich_companies(self, df, options):
        return df