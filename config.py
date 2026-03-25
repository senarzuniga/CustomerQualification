import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL = "gpt-4-turbo-preview"
    LLM_TEMPERATURE = 0.3
    LLM_MAX_TOKENS = 2000
    
    REQUEST_TIMEOUT = 10
    MAX_RETRIES = 3
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    
    UPLOAD_FOLDER = "temp_uploads"
    OUTPUT_FOLDER = "generated_excels"
    MAX_FILE_SIZE_MB = 50
    ALLOWED_EXTENSIONS = {'xlsx', 'xls', 'pdf', 'csv'}
    
    COMPANY_FIELDS = [
        'Customer Name', 'Sector', 'Market Segment', 'Number of Employees',
        'Revenue', 'Economical Status', 'Fiscal report', 'Finance information',
        'Revenue variation last 3 years', 'Years operating', 'Main Market',
        'Produced Products', 'Main product', 'Used packaging substrates',
        'Main Challenges', 'How takes Decisions', 'Existing Solutions',
        'Competitors', 'Customer Needs and Preferences', 'Purchase History and Budget',
        'Geographic Location', 'Technological Readiness', 'Feedback and Reviews',
        'Company Email', 'Company Phone Number', 'Address'
    ]
    
    LOG_LEVEL = "INFO"
    LOG_FILE = "logs/customer_qualification.log"
    
    @classmethod
    def ensure_directories(cls):
        os.makedirs(cls.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(cls.OUTPUT_FOLDER, exist_ok=True)
        os.makedirs("logs", exist_ok=True)
