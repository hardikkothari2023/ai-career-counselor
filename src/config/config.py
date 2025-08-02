import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
ASSETS_DIR = BASE_DIR / "streamlit_app" / "assets"

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY", "")

# Model Configuration
MODEL_CONFIG = {
    "resume_parser": {
        "model_name": "en_core_web_sm",
        "confidence_threshold": 0.7
    },
    "career_predictor": {
        "model_name": "career_predictor_model",
        "batch_size": 32
    }
}

# Application Configuration
APP_CONFIG = {
    "debug": os.getenv("DEBUG", "False").lower() == "true",
    "host": os.getenv("HOST", "0.0.0.0"),
    "port": int(os.getenv("PORT", "8501")),
    "max_upload_size": 5 * 1024 * 1024  # 5MB
}

# Logging Configuration
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
        "file": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.FileHandler",
            "filename": BASE_DIR / "logs" / "app.log",
            "mode": "a",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": True
        }
    }
}

# Career Prediction Configuration
CAREER_CONFIG = {
    "min_confidence": 0.6,
    "max_recommendations": 5,
    "skills_weight": 0.4,
    "personality_weight": 0.3,
    "education_weight": 0.3
}

# Resume Parser Configuration
RESUME_PARSER_CONFIG = {
    "allowed_extensions": [".pdf", ".doc", ".docx"],
    "max_file_size": 5 * 1024 * 1024,  # 5MB
    "required_sections": ["education", "experience", "skills"]
} 