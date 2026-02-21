"""
Configuration settings for Grievance Hub Flask Application
"""

import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'grievance-hub-secret-key-change-in-production')
    
    # Database
    DB_PATH = os.path.join(BASE_DIR, 'data', 'grievance.db')
    
    # Email
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USER = os.getenv('EMAIL_USER', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_FROM = os.getenv('EMAIL_FROM', os.getenv('EMAIL_USER', ''))
    
    # Gemini AI
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    GEMINI_MODEL = 'gemini-2.5-flash'
    
    # ML Models directory
    MODELS_DIR = os.path.join(BASE_DIR, 'ml_models')
    
    # Gemini classification prompt
    GEMINI_PROMPT = """
You are an intelligent grievance classification assistant for a citizen complaint management system.

You will receive a text complaint written in English (sometimes with small grammar or spelling errors).

Your tasks:
1. Identify the correct department that should handle it. Choose ONLY from:
   - CM Office (Miscellaneous)
   - Development Authority
   - Municipal
   - Police
   - Public Works Department
   - Transport
2. Determine whether the complaint is **Critical** or **Non-Critical**.
   - Critical means urgent or safety-related (accidents, fires, injuries, harassment, violence, death, etc.).
   - Non-Critical means routine issues (garbage, water, road maintenance, paperwork delays, etc.).
3. Return ONLY valid JSON in this exact format:
{
  "department": "<one of the 6 departments>",
  "criticality": "<Critical or Non-Critical>",
  "confidence_reason": "<short reason for your decision>"
}

If the input is unclear, meaningless, or too short to classify, return:
{
  "department": "Invalid",
  "criticality": "None",
  "confidence_reason": "Complaint not clear or incomplete"
}

Now classify the following complaint:
<<<USER_COMPLAINT>>>
"""


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
