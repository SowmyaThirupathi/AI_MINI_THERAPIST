#!/usr/bin/env python3
"""
AI Mini Therapist - Final Year Project
Main Entry Point

Author: [Your Name]
Date: 2025
Course: [Your Course]
University: [Your University]

This is the main entry point for the AI Mini Therapist application.
It provides a menu-driven interface to access different modules.
"""

import os
import sys
import subprocess
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent
sys.path.insert(0, str(PROJECT_ROOT))

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Print project banner"""
    banner = """
===========================================================
                    AI MINI THERAPIST                          
                 Final Year Project 2025                      
===========================================================
  An intelligent emotion detection and mental health         
  monitoring system using FER2013 dataset and real-time      
  computer vision for stress management and wellness       
===========================================================
"""
    print(banner)

def print_menu():
    """Print main menu"""
    menu = """
===========================================================
                        MAIN MENU                             
===========================================================
  1. Train FER2013 Model                                    
  2. Run Enhanced AI Therapist                              
  3. Run Legacy Version                                      
  4. View Project Documentation                              
  5. System Requirements Check                                
  6. About Project                                          
  0. Exit                                                   
===========================================================
"""
    print(menu)

def check_system_requirements():
    """Check system requirements"""
    print("\n" + "="*60)
    print("SYSTEM REQUIREMENTS CHECK")
    print("="*60)
    
    # Check Python version
    python_version = sys.version_info
    print(f"Python Version: {python_version.major}.{python_version.minor}.{python_version.micro}")
    
    if python_version.major < 3 or (python_version.major == 3 and python_version.minor < 7):
        print("ERROR: Python 3.7+ required")
        return False
    else:
        print("OK: Python version compatible")
    
    # Check required packages
    required_packages = [
        'cv2', 'tensorflow', 'numpy', 'pandas', 
        'matplotlib', 'tkinter', 'scikit-learn'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'tkinter':
                import tkinter
                print(f"OK: {package} installed")
            elif package == 'cv2':
                import cv2
                print(f"OK: {package} installed")
            elif package == 'tensorflow':
                import tensorflow
                print(f"OK: {package} installed")
            elif package == 'numpy':
                import numpy
                print(f"OK: {package} installed")
            elif package == 'pandas':
                import pandas
                print(f"OK: {package} installed")
            elif package == 'matplotlib':
                import matplotlib
                print(f"OK: {package} installed")
            elif package == 'scikit-learn':
                import sklearn
                print(f"OK: {package} installed")
        except ImportError:
            print(f"MISSING: {package} missing")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\nMissing packages: {', '.join(missing_packages)}")
        print("Install with: pip install " + " ".join(missing_packages))
        return False
    
    # Check camera access
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            print("OK: Camera access available")
            cap.release()
        else:
            print("WARNING: Camera not available (simulation mode)")
    except:
        print("WARNING: Camera check failed (simulation mode)")
    
    print("\nOK: System requirements check completed")
    input("Press Enter to continue...")
    return True

def train_model():
    """Run model training"""
    print("\n" + "="*60)
    print("TRAINING FER2013 MODEL")
    print("="*60)
    
    training_script = PROJECT_ROOT / "training" / "train_fer2013.py"
    
    if not training_script.exists():
        print("ERROR: Training script not found!")
        input("Press Enter to continue...")
        return
    
    print("Starting FER2013 model training...")
    print("This may take several minutes...")
    
    try:
        # Change to training directory and run script
        os.chdir(PROJECT_ROOT / "training")
        subprocess.run([sys.executable, "train_fer2013.py"], check=True)
        print("\nOK: Training completed successfully!")
    except subprocess.CalledProcessError:
        print("\nERROR: Training failed!")
    except Exception as e:
        print(f"\nERROR: Error during training: {e}")
    finally:
        # Return to project root
        os.chdir(PROJECT_ROOT)
    
    input("Press Enter to continue...")

def run_enhanced_therapist():
    """Run enhanced AI therapist"""
    print("\n" + "="*60)
    print("ENHANCED AI THERAPIST")
    print("="*60)
    
    app_script = PROJECT_ROOT / "application" / "enhanced_ai_therapist.py"
    
    if not app_script.exists():
        print("ERROR: Enhanced therapist script not found!")
        input("Press Enter to continue...")
        return
    
    print("Starting Enhanced AI Therapist...")
    print("Features: Real-time analytics, break reminders, focus monitoring")
    
    try:
        # Change to application directory and run script
        os.chdir(PROJECT_ROOT / "application")
        subprocess.run([sys.executable, "enhanced_ai_therapist.py"], check=True)
    except subprocess.CalledProcessError:
        print("\nERROR: Enhanced therapist failed to start!")
    except KeyboardInterrupt:
        print("\nEnhanced therapist stopped by user")
    except Exception as e:
        print(f"\nERROR: {e}")
    finally:
        # Return to project root
        os.chdir(PROJECT_ROOT)
    
    input("Press Enter to continue...")

def run_legacy_therapist():
    """Run legacy AI therapist"""
    print("\n" + "="*60)
    print("LEGACY AI THERAPIST")
    print("="*60)
    
    legacy_script = PROJECT_ROOT / "SIMPLE_RELIABLE_THERAPIST.py"
    
    if not legacy_script.exists():
        print("ERROR: Legacy therapist script not found!")
        input("Press Enter to continue...")
        return
    
    print("Starting Legacy AI Therapist...")
    print("Basic version with core functionality")
    
    try:
        # Run legacy script
        subprocess.run([sys.executable, "SIMPLE_RELIABLE_THERAPIST.py"], check=True)
    except subprocess.CalledProcessError:
        print("\nERROR: Legacy therapist failed to start!")
    except KeyboardInterrupt:
        print("\nLegacy therapist stopped by user")
    except Exception as e:
        print(f"\nERROR: {e}")
    
    input("Press Enter to continue...")

def view_documentation():
    """View project documentation"""
    print("\n" + "="*60)
    print("PROJECT DOCUMENTATION")
    print("="*60)
    
    readme_file = PROJECT_ROOT / "README.md"
    
    if readme_file.exists():
        try:
            with open(readme_file, 'r', encoding='utf-8') as f:
                content = f.read()
                print(content)
        except Exception as e:
            print(f"ERROR: Error reading documentation: {e}")
    else:
        print("ERROR: Documentation file not found!")
    
    input("\nPress Enter to continue...")

def about_project():
    """Display project information"""
    about_text = """
===========================================================
                    ABOUT PROJECT                             
===========================================================

  Project Title: AI Mini Therapist
  Type: Final Year Project
  Year: 2025

  Description:
  An intelligent emotion detection and mental health
  monitoring system that uses computer vision and
  machine learning to detect emotions in real-time.

  Key Features:
  • Real-time emotion detection using FER2013 dataset
  • Stress level monitoring and alerts
  • Activity tracking and productivity analysis
  • Break reminders and health monitoring
  • Comprehensive analytics and reporting

  Technologies Used:
  • Python 3.7+
  • TensorFlow/Keras
  • OpenCV
  • Tkinter
  • Matplotlib
  • Scikit-learn

  Dataset:
  • FER2013 (Facial Expression Recognition 2013)
  • 7 emotion classes: Angry, Disgust, Fear, Happy, Sad,
    Surprise, Neutral
  • 48x48 grayscale facial images

===========================================================
"""
    print(about_text)
    input("Press Enter to continue...")

def main():
    """Main function"""
    while True:
        clear_screen()
        print_banner()
        print_menu()
        
        try:
            choice = input("\nEnter your choice (0-6): ").strip()
            
            if choice == '0':
                print("\n👋 Thank you for using AI Mini Therapist!")
                print("Final Year Project 2025 - All rights reserved")
                break
            elif choice == '1':
                train_model()
            elif choice == '2':
                run_enhanced_therapist()
            elif choice == '3':
                run_legacy_therapist()
            elif choice == '4':
                view_documentation()
            elif choice == '5':
                check_system_requirements()
            elif choice == '6':
                about_project()
            else:
                print("\nInvalid choice! Please enter a number between 0-6")
                input("Press Enter to continue...")
                
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}")
            input("Press Enter to continue...")

if __name__ == "__main__":
    main()
