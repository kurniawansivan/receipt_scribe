import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Configuration
    PROJECT_NAME: str = "ReceiptScribe API"
    VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"
    
    # OpenAI
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    
    # CORS - Update with your Flutter app ports
    ALLOWED_ORIGINS: list = [
        "http://localhost",
        "http://localhost:8000", 
        "http://localhost:3000",
        "http://10.0.2.2:8000",  # Android emulator
    ]
    
    # File Upload
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_FILE_TYPES: list = ["image/jpeg", "image/png", "image/webp"]
    
    # Database
    DATABASE_PATH: str = "receipts.db"

settings = Settings()