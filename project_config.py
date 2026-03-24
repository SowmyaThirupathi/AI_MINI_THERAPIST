"""
AI Mini Therapist - Project Configuration
Final Year Project 2025

This file contains all project configuration settings and constants.
"""

import os
from pathlib import Path

# Project Information
PROJECT_NAME = "AI Mini Therapist"
PROJECT_VERSION = "1.0.0"
PROJECT_AUTHOR = "Your Name"
PROJECT_YEAR = "2025"
PROJECT_COURSE = "Computer Science / AI"
PROJECT_UNIVERSITY = "Your University"

# Project Paths
PROJECT_ROOT = Path(__file__).parent.absolute()
DATA_DIR = PROJECT_ROOT / "data"
MODEL_DIR = PROJECT_ROOT / "models"
EXPORT_DIR = PROJECT_ROOT / "exports"
DOCS_DIR = PROJECT_ROOT / "docs"
TRAINING_DIR = PROJECT_ROOT / "training"
APPLICATION_DIR = PROJECT_ROOT / "application"

# Dataset Configuration
FER2013_EMOTIONS = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
FER2013_IMAGE_SIZE = (48, 48)
FER2013_NUM_CLASSES = 7
FER2013_TRAIN_SAMPLES_PER_EMOTION = 10
FER2013_TEST_SAMPLES_PER_EMOTION = 3

# Model Configuration
MODEL_NAME = "fer2013_trained_model.h5"
MODEL_PATH = MODEL_DIR / MODEL_NAME
CONFIDENCE_THRESHOLD = 0.4
BATCH_SIZE = 32
EPOCHS = 20
LEARNING_RATE = 0.001

# Camera Configuration
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
CAMERA_FPS = 20
FACE_DETECTION_SCALE_FACTOR = 1.1
FACE_DETECTION_MIN_NEIGHBORS = 5
MIN_FACE_SIZE = (30, 30)

# Application Configuration
WINDOW_TITLE = "AI Mini Therapist"
WINDOW_WIDTH = 1400
WINDOW_HEIGHT = 900
UPDATE_INTERVAL = 1000  # milliseconds
ANALYTICS_UPDATE_INTERVAL = 5000  # milliseconds

# Session Configuration
DEFAULT_SESSION_DURATION = 7200  # 2 hours in seconds
BREAK_REMINDER_INTERVAL = 1800  # 30 minutes in seconds
FOCUS_ALERT_INTERVAL = 300  # 5 minutes in seconds
STRESS_ALERT_COOLDOWN = 30  # seconds

# Stress Configuration
STRESS_LEVELS = {
    'Happy': 10,
    'Neutral': 20,
    'Surprise': 30,
    'Disgust': 50,
    'Sad': 60,
    'Fear': 70,
    'Angry': 80
}

STRESS_THRESHOLDS = {
    'low': 30,
    'medium': 50,
    'high': 70
}

# Focus and Productivity Configuration
FOCUS_BASELINE = 100
PRODUCTIVITY_BASELINE = 100
EYE_STRAIN_INCREASE_RATE = 2
POSTURE_VARIATION_RANGE = 10

# Colors for UI
UI_COLORS = {
    'primary': '#2c3e50',
    'secondary': '#3498db',
    'success': '#27ae60',
    'warning': '#f39c12',
    'danger': '#e74c3c',
    'info': '#9b59b6',
    'light': '#ecf0f1',
    'dark': '#34495e'
}

# Emotion Colors
EMOTION_COLORS = {
    'Happy': '#27ae60',
    'Neutral': '#3498db',
    'Sad': '#9b59b6',
    'Angry': '#e74c3c',
    'Fear': '#f39c12',
    'Surprise': '#e67e22',
    'Disgust': '#95a5a6'
}

# Logging Configuration
LOG_LEVEL = "INFO"
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE = DATA_DIR / "ai_therapist.log"

# CSV Configuration
CSV_HEADERS = [
    'Timestamp', 'Window_Title', 'Application', 'Website', 'Tab', 'Duration',
    'Emotion', 'Stress', 'Confidence', 'Focus', 'Productivity', 'Eye_Strain', 'Posture'
]

ACTIVITY_LOG_FILE = DATA_DIR / "enhanced_ai_therapist_log.csv"

# Report Configuration
REPORT_FILE_PREFIX = "enhanced_ai_therapist_report_"
REPORT_FILE_EXTENSION = ".json"

# System Requirements
MIN_PYTHON_VERSION = (3, 7)
REQUIRED_PACKAGES = [
    'opencv-python>=4.5.0',
    'tensorflow>=2.8.0',
    'numpy>=1.19.0',
    'pandas>=1.3.0',
    'matplotlib>=3.4.0',
    'scikit-learn>=1.0.0',
    'pillow>=8.0.0'
]

# Development Configuration
DEBUG_MODE = False
ENABLE_LOGGING = True
ENABLE_ANALYTICS = True
ENABLE_DESKTOP_ALERTS = True
ENABLE_BREAK_REMINDERS = True
ENABLE_FOCUS_ALERTS = True

# Performance Configuration
MAX_EMOTION_HISTORY = 1000
MAX_ACTIVITY_LOG_LINES = 40
MAX_ANALYTICS_POINTS = 50
AUTO_CLOSE_ALERT_TIMEOUT = 30000  # 30 seconds

# File Extensions
IMAGE_EXTENSIONS = ['.jpg', '.jpeg', '.png']
MODEL_EXTENSIONS = ['.h5', '.keras']
DATA_EXTENSIONS = ['.csv', '.json']

# Error Messages
ERROR_MESSAGES = {
    'camera_not_available': "Camera not available. Using simulation mode.",
    'model_not_found': "Trained model not found. Run training script first.",
    'tensorflow_not_available': "TensorFlow not available. Using simulation mode.",
    'training_failed': "Model training failed. Check logs for details.",
    'application_error': "Application error occurred. Please try again."
}

# Success Messages
SUCCESS_MESSAGES = {
    'training_completed': "Model training completed successfully!",
    'model_loaded': "Trained model loaded successfully!",
    'session_started': "Session started successfully!",
    'session_completed': "Session completed successfully!",
    'report_generated': "Report generated successfully!"
}

# Help Messages
HELP_MESSAGES = {
    'stress': "Monitor your stress levels and get real-time alerts when stress is high.",
    'focus': "Track your focus and productivity levels throughout the session.",
    'break': "Take regular breaks to maintain good health and productivity.",
    'analytics': "View detailed analytics and reports about your session.",
    'settings': "Customize alerts, reminders, and monitoring preferences."
}

# Intervention Messages
INTERVENTION_MESSAGES = [
    "Take 5 deep breaths and stretch",
    "Practice 2-minute mindfulness meditation",
    "Look away from screen for 30 seconds",
    "Do neck and shoulder stretches",
    "Drink water and walk around",
    "Practice progressive muscle relaxation",
    "Listen to calming music for 3 minutes",
    "Adjust your sitting posture",
    "Rest your eyes using 20-20-20 rule",
    "Take a short walk and refresh"
]

# Activity Templates for Simulation
ACTIVITY_TEMPLATES = [
    ("Chrome - AI Research Paper", "chrome.exe", "arXiv", "AI Research"),
    ("VS Code - enhanced_ai_therapist.py", "Code.exe", "Desktop Application", "Enhanced AI Therapist"),
    ("Chrome - Kaggle - AI Datasets", "chrome.exe", "Kaggle", "AI Datasets"),
    ("Chrome - GitHub - AI Models", "chrome.exe", "GitHub", "AI Models"),
    ("File Explorer - AI Project", "explorer.exe", "Desktop Application", "AI Project"),
    ("Chrome - Papers With Code - AI", "chrome.exe", "Papers With Code", "AI Papers"),
    ("Notepad - AI Notes.txt", "notepad.exe", "Desktop Application", "AI Notes"),
    ("Chrome - TensorFlow - AI Tutorial", "chrome.exe", "TensorFlow", "AI Tutorial"),
    ("Word - AI Report.docx", "WINWORD.EXE", "Desktop Application", "AI Report"),
    ("Excel - AI Analytics.xlsx", "EXCEL.EXE", "Desktop Application", "AI Analytics")
]

# Session Durations
SESSION_DURATIONS = {
    "30 minutes": 1800,
    "1 hour": 3600,
    "2 hours": 7200,
    "3 hours": 10800,
    "4 hours": 14400,
    "6 hours": 21600
}

# Validation Functions
def validate_project_structure():
    """Validate that all required directories exist"""
    required_dirs = [DATA_DIR, MODEL_DIR, EXPORT_DIR, DOCS_DIR, TRAINING_DIR, APPLICATION_DIR]
    
    for dir_path in required_dirs:
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
    
    return True

def get_project_info():
    """Get project information as dictionary"""
    return {
        'name': PROJECT_NAME,
        'version': PROJECT_VERSION,
        'author': PROJECT_AUTHOR,
        'year': PROJECT_YEAR,
        'course': PROJECT_COURSE,
        'university': PROJECT_UNIVERSITY
    }

def get_system_info():
    """Get system information"""
    import platform
    import sys
    
    return {
        'platform': platform.system(),
        'platform_version': platform.version(),
        'python_version': sys.version,
        'python_executable': sys.executable
    }

# Initialize project structure
if __name__ == "__main__":
    validate_project_structure()
    print(f"✅ {PROJECT_NAME} v{PROJECT_VERSION} configuration initialized")
    print(f"✅ Project directories validated")
    print(f"✅ Ready for final year project deployment")
