"""
AI Mini Therapist - Setup Script
Final Year Project 2025

This script allows for professional installation and distribution
of the AI Mini Therapist project.
"""

from setuptools import setup, find_packages
import os
from pathlib import Path

# Read project configuration
PROJECT_ROOT = Path(__file__).parent

# Read README for long description
def read_readme():
    readme_path = PROJECT_ROOT / "README.md"
    if readme_path.exists():
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "AI Mini Therapist - Final Year Project"

# Read requirements
def read_requirements():
    requirements_path = PROJECT_ROOT / "requirements.txt"
    if requirements_path.exists():
        with open(requirements_path, "r", encoding="utf-8") as f:
            requirements = []
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("-"):
                    requirements.append(line)
            return requirements
    return []

setup(
    name="ai-mini-therapist",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@university.edu",
    description="An intelligent emotion detection and mental health monitoring system",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/ai-mini-therapist",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/ai-mini-therapist/issues",
        "Documentation": "https://github.com/yourusername/ai-mini-therapist/wiki",
        "Source Code": "https://github.com/yourusername/ai-mini-therapist",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Education",
        "Intended Audience :: Healthcare",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "sphinx>=4.0.0",
        ],
        "monitoring": [
            "psutil>=5.8.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "ai-therapist=main:main",
            "train-fer2013=training.train_fer2013:main",
            "run-therapist=application.enhanced_ai_therapist:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.md", "*.txt", "*.json", "*.csv", "*.h5"],
    },
    data_files=[
        ("docs", ["README.md", "LICENSE"]),
        ("models", []),
        ("data", []),
        ("exports", []),
    ],
    zip_safe=False,
    keywords="artificial intelligence, emotion detection, mental health, computer vision, machine learning, tensorflow, opencv, fer2013",
    platforms=["any"],
    license="MIT",
)
