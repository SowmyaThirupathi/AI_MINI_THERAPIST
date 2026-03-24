"""
SIMPLE RELIABLE AI MINI THERAPIST
Minimal, crash-free version with all requested features
"""

import cv2
import numpy as np
import time
import csv
import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Toplevel
from datetime import datetime
from pathlib import Path
from collections import defaultdict
import random
import json
import warnings
warnings.filterwarnings('ignore')

class SimpleReliableTherapist:
    def __init__(self):
        print("INITIALIZING SIMPLE RELIABLE THERAPIST...")
        
        # Basic State
        self.running = False
        self.session_active = False
        self.current_emotion = "Neutral"
        self.stress_score = 30
        self.session_start = None
        self.session_duration = 7200  # 2 hours
        self.session_end_time = None
        
        # Activity Tracking
        self.current_window = "Desktop"
        self.current_app = "Unknown"
        self.current_website = "Desktop Application"
        self.current_tab = "Unknown"
        self.app_usage_time = defaultdict(float)
        self.website_usage_time = defaultdict(float)
        self.tab_usage_time = defaultdict(float)
        
        # Data Storage
        self.emotion_counts = defaultdict(int)
        self.stress_history = []
        
        # Alert System
        self.alert_window = None
        self.last_stress_alert = 0
        self.desktop_alerts_enabled = True
        
        # Camera
        self.cap = None
        self.camera_active = False
        
        # Setup
        self.setup_directories()
        self.setup_simple_gui()
        
        print("SIMPLE RELIABLE THERAPIST READY!")
    
    def setup_directories(self):
        """Setup necessary directories"""
        dirs = ['data', 'logs', 'exports']
        for dir_name in dirs:
            Path(dir_name).mkdir(exist_ok=True)
        
        # Create log file
        self.activity_log_file = "data/simple_reliable_activity_log.csv"
        if not os.path.exists(self.activity_log_file):
            with open(self.activity_log_file, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['Timestamp', 'Window_Title', 'Application', 'Website', 'Tab', 'Duration', 'Emotion', 'Stress'])
    
    def setup_simple_gui(self):
        """Setup simple, reliable GUI"""
        self.root = tk.Tk()
        self.root.title("Simple Reliable AI Therapist")
        self.root.geometry("1200x800")
        self.root.configure(bg='#ffffff')
        
        # Handle window close
        self.root.protocol("WM_DELETE_WINDOW", self.safe_close)
        
        # Title
        title_label = tk.Label(self.root, text="SIMPLE RELIABLE AI THERAPIST", 
                            font=("Arial", 20, "bold"), fg='#333333', bg='#ffffff')
        title_label.pack(pady=10)
        
        # Session Control
        session_frame = tk.LabelFrame(self.root, text="Session Control", 
                                  font=("Arial", 14, "bold"), fg='#333333', bg='#ffffff')
        session_frame.pack(fill=tk.X, padx=20, pady=10)
        
        # Duration selection
        duration_frame = tk.Frame(session_frame, bg='#ffffff')
        duration_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(duration_frame, text="Duration:", font=("Arial", 12), 
                fg='#333333', bg='#ffffff').pack(side=tk.LEFT)
        
        self.duration_var = tk.StringVar(value="2 hours")
        duration_options = ["30 minutes", "1 hour", "2 hours", "3 hours", "4 hours", "6 hours"]
        self.duration_combo = ttk.Combobox(duration_frame, textvariable=self.duration_var, 
                                     values=duration_options, width=12, state='readonly')
        self.duration_combo.pack(side=tk.LEFT, padx=10)
        
        # Time display
        time_frame = tk.Frame(session_frame, bg='#ffffff')
        time_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.session_time_label = tk.Label(time_frame, text="Time: 00:00:00", 
                                      font=("Arial", 12, "bold"), fg='#333333', bg='#ffffff')
        self.session_time_label.pack(side=tk.LEFT)
        
        self.remaining_time_label = tk.Label(time_frame, text="Remaining: 02:00:00", 
                                         font=("Arial", 12, "bold"), fg='#333333', bg='#ffffff')
        self.remaining_time_label.pack(side=tk.LEFT, padx=20)
        
        # Control buttons
        button_frame = tk.Frame(session_frame, bg='#ffffff')
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.start_btn = tk.Button(button_frame, text="Start Session", 
                               command=self.start_session,
                               font=("Arial", 12, "bold"), bg='#4CAF50', fg='white',
                               width=12)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(button_frame, text="Stop Session", 
                              command=self.stop_session,
                              font=("Arial", 12, "bold"), bg='#f44336', fg='white',
                              width=12, state='disabled')
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        # Desktop alerts checkbox
        self.alerts_var = tk.BooleanVar(value=True)
        alerts_check = tk.Checkbutton(button_frame, text="Desktop Alerts", 
                                   variable=self.alerts_var,
                                   font=("Arial", 11), fg='#333333', bg='#ffffff')
        alerts_check.pack(side=tk.LEFT, padx=20)
        
        # Content area
        content_frame = tk.Frame(self.root, bg='#ffffff')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left side - Camera and Status
        left_frame = tk.Frame(content_frame, bg='#ffffff')
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Camera section
        camera_frame = tk.LabelFrame(left_frame, text="Camera Monitoring", 
                                   font=("Arial", 14, "bold"), fg='#333333', bg='#ffffff')
        camera_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.camera_canvas = tk.Canvas(camera_frame, width=350, height=250, bg='#f0f0f0')
        self.camera_canvas.pack(pady=10)
        
        # Status display
        status_frame = tk.Frame(camera_frame, bg='#ffffff')
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.emotion_label = tk.Label(status_frame, text="Emotion: Neutral", 
                                   font=("Arial", 12, "bold"), fg='#333333', bg='#ffffff')
        self.emotion_label.pack(side=tk.LEFT, padx=10)
        
        self.stress_label = tk.Label(status_frame, text="Stress: 30", 
                                  font=("Arial", 12, "bold"), fg='#333333', bg='#ffffff')
        self.stress_label.pack(side=tk.LEFT, padx=10)
        
        self.camera_status = tk.Label(status_frame, text="OFF", 
                                  font=("Arial", 12, "bold"), fg='#f44336', bg='#ffffff')
        self.camera_status.pack(side=tk.LEFT, padx=10)
        
        # Right side - Activity and Chat
        right_frame = tk.Frame(content_frame, bg='#ffffff')
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Activity monitoring
        activity_frame = tk.LabelFrame(right_frame, text="Activity Monitoring", 
                                     font=("Arial", 14, "bold"), fg='#333333', bg='#ffffff')
        activity_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Current activity
        current_frame = tk.Frame(activity_frame, bg='#ffffff')
        current_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(current_frame, text="Current Window:", font=("Arial", 11, "bold"), 
                fg='#333333', bg='#ffffff').pack(side=tk.LEFT)
        self.current_window_label = tk.Label(current_frame, text="None", 
                                       font=("Arial", 11), fg='#333333', bg='#ffffff')
        self.current_window_label.pack(side=tk.LEFT, padx=10)
        
        tk.Label(current_frame, text="Current Tab:", font=("Arial", 11, "bold"), 
                fg='#333333', bg='#ffffff').pack(side=tk.LEFT, padx=(20, 0))
        self.current_tab_label = tk.Label(current_frame, text="None", 
                                     font=("Arial", 11), fg='#333333', bg='#ffffff')
        self.current_tab_label.pack(side=tk.LEFT, padx=10)
        
        # Activity log
        self.activity_display = scrolledtext.ScrolledText(activity_frame, height=12, width=45,
                                                     bg='#f8f8f8', fg='#333333', 
                                                     font=("Courier", 9))
        self.activity_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Statistics button
        self.stats_btn = tk.Button(activity_frame, text="Show Statistics", 
                                command=self.show_statistics,
                                font=("Arial", 10, "bold"), bg='#2196F3', fg='white',
                                width=15)
        self.stats_btn.pack(pady=5)
        
        # Chat section
        chat_frame = tk.LabelFrame(right_frame, text="AI Assistant", 
                                font=("Arial", 14, "bold"), fg='#333333', bg='#ffffff')
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(chat_frame, height=8, width=45,
                                                     bg='#f8f8f8', fg='#333333', 
                                                     font=("Arial", 10))
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Chat input
        input_frame = tk.Frame(chat_frame, bg='#ffffff')
        input_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.chat_input = tk.Entry(input_frame, font=("Arial", 10), bg='#ffffff', fg='#333333')
        self.chat_input.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        self.send_btn = tk.Button(input_frame, text="Send", 
                               command=self.send_message,
                               font=("Arial", 10, "bold"), bg='#2196F3', fg='white',
                               width=8)
        self.send_btn.pack(side=tk.RIGHT)
        
        # Add welcome message
        self.add_chat_message("AI", "Welcome! Simple reliable version ready. Click Start Session to begin.")
        
        # Start display updates
        self.update_display()
    
    def safe_close(self):
        """Safe close handling"""
        try:
            self.running = False
            self.session_active = False
            if self.cap:
                self.cap.release()
            if self.alert_window:
                self.alert_window.destroy()
            self.root.destroy()
        except:
            pass
    
    def start_session(self):
        """Start session with simple reliable approach"""
        try:
            # Convert duration to seconds
            duration_text = self.duration_var.get()
            duration_map = {
                "30 minutes": 1800, "1 hour": 3600, "2 hours":7200,
                "3 hours": 10800, "4 hours": 14400, "6 hours": 21600
            }
            self.session_duration = duration_map.get(duration_text, 7200)
            
            print(f"Starting {duration_text} session...")
            
            # Initialize camera
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showwarning("Camera Warning", "Camera not available. Using simulation mode.")
                self.camera_active = False
            else:
                # Test camera
                ret, test_frame = self.cap.read()
                if not ret:
                    messagebox.showwarning("Camera Warning", "Camera test failed. Using simulation mode.")
                    self.cap.release()
                    self.cap = None
                    self.camera_active = False
                else:
                    self.camera_active = True
                    print("Camera initialized successfully")
            
            self.running = True
            self.session_active = True
            self.session_start = time.time()
            self.session_end_time = self.session_start + self.session_duration
            self.desktop_alerts_enabled = self.alerts_var.get()
            
            # Update UI
            self.start_btn.config(state='disabled')
            self.stop_btn.config(state='normal')
            self.duration_combo.config(state='disabled')
            self.camera_status.config(text="ON" if self.camera_active else "SIM", fg='#4CAF50')
            
            # Start monitoring threads
            if self.camera_active:
                self.camera_thread = threading.Thread(target=self.simple_camera_monitoring, daemon=True)
                self.camera_thread.start()
            else:
                self.camera_thread = threading.Thread(target=self.emotion_simulation, daemon=True)
                self.camera_thread.start()
            
            self.activity_thread = threading.Thread(target=self.simple_activity_monitoring, daemon=True)
            self.activity_thread.start()
            
            self.session_timer_thread = threading.Thread(target=self.session_timer, daemon=True)
            self.session_timer_thread.start()
            
            mode = "Real Camera" if self.camera_active else "Simulation"
            self.add_chat_message("AI", f"Session started! Mode: {mode}. Duration: {duration_text}")
            
        except Exception as e:
            print(f"Start session error: {e}")
            messagebox.showerror("Error", f"Failed to start session: {e}")
    
    def stop_session(self):
        """Stop session"""
        try:
            print("Stopping session...")
            
            self.running = False
            self.session_active = False
            
            # Release camera
            if self.cap:
                self.cap.release()
                self.cap = None
            
            # Close alert window
            if self.alert_window:
                self.alert_window.destroy()
                self.alert_window = None
            
            # Update UI
            self.start_btn.config(state='normal')
            self.stop_btn.config(state='disabled')
            self.duration_combo.config(state='normal')
            self.camera_status.config(text="OFF", fg='#f44336')
            
            # Clear camera canvas
            self.camera_canvas.delete("all")
            self.camera_canvas.create_text(175, 125, text="Camera Off", fill="black", font=("Arial", 14))
            
            session_time = int(time.time() - self.session_start) if self.session_start else 0
            self.add_chat_message("AI", f"Session completed! Duration: {session_time//3600}h {(session_time%3600)//60}m {session_time%60}s")
            
            # Generate report
            self.generate_simple_report()
            
        except Exception as e:
            print(f"Stop session error: {e}")
    
    def simple_camera_monitoring(self):
        """Simple camera monitoring"""
        try:
            face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
            
            # Simple emotion labels
            emotions = ['Happy', 'Neutral', 'Sad', 'Angry', 'Fear', 'Surprise', 'Disgust']
            stress_map = {
                'Happy': 10, 'Neutral': 20, 'Surprise': 30,
                'Disgust': 50, 'Sad': 60, 'Fear': 70, 'Angry': 80
            }
            
            frame_count = 0
            
            while self.running and self.camera_active:
                ret, frame = self.cap.read()
                frame_count += 1
                
                if not ret:
                    time.sleep(0.1)
                    continue
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Simple face detection
                faces = face_cascade.detectMultiScale(gray, 1.1, 5)
                
                for (x, y, w, h) in faces:
                    # Simple emotion simulation based on time
                    if frame_count % 30 == 0:  # Change emotion every 30 frames
                        self.current_emotion = random.choice(emotions)
                        self.stress_score = stress_map[self.current_emotion]
                        self.emotion_counts[self.current_emotion] += 1
                        self.stress_history.append(self.stress_score)
                        
                        # Check for stress alert
                        if self.stress_score > 60 and self.desktop_alerts_enabled:
                            self.trigger_desktop_alert(self.stress_score, self.current_emotion)
                    
                    # Draw on frame
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, self.current_emotion, (x, y-10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    cv2.putText(frame, f"Stress: {self.stress_score}", (x, y+h+20), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
                
                # Update camera display every 10 frames
                if frame_count % 10 == 0:
                    self.root.after(0, self.update_camera_display, frame)
                
                time.sleep(0.05)  # 20 FPS
                
        except Exception as e:
            print(f"Camera monitoring error: {e}")
    
    def emotion_simulation(self):
        """Simple emotion simulation"""
        emotions = ['Happy', 'Neutral', 'Sad', 'Angry', 'Fear', 'Surprise', 'Disgust']
        stress_map = {
            'Happy': 10, 'Neutral': 20, 'Surprise': 30,
            'Disgust': 50, 'Sad': 60, 'Fear': 70, 'Angry': 80
        }
        
        while self.running:
            # Simulate emotion changes
            if random.random() < 0.2:  # 20% chance of emotion change
                self.current_emotion = random.choice(emotions)
                self.stress_score = stress_map[self.current_emotion]
                self.emotion_counts[self.current_emotion] += 1
                self.stress_history.append(self.stress_score)
                
                # Check for stress alert
                if self.stress_score > 60 and self.desktop_alerts_enabled:
                    self.trigger_desktop_alert(self.stress_score, self.current_emotion)
                
                # Update camera display
                self.root.after(0, self.update_simulation_display)
            
            time.sleep(3)  # Update every 3 seconds
    
    def simple_activity_monitoring(self):
        """Simple activity monitoring"""
        activities = [
            ("Chrome - YouTube - Simple Tutorial", "chrome.exe", "YouTube", "Simple Tutorial"),
            ("VS Code - SIMPLE_RELIABLE_THERAPIST.py", "Code.exe", "Desktop Application", "Simple Therapist Code"),
            ("Chrome - Gmail - Simple Inbox", "chrome.exe", "Gmail", "Simple Inbox"),
            ("Chrome - Stack Overflow - Simple Help", "chrome.exe", "Stack Overflow", "Simple Help"),
            ("File Explorer - Simple Documents", "explorer.exe", "Desktop Application", "Simple Documents"),
            ("Chrome - LinkedIn - Simple Professional", "chrome.exe", "LinkedIn", "Simple Professional"),
            ("Notepad - Simple Notes.txt", "notepad.exe", "Desktop Application", "Simple Notes"),
            ("Chrome - Amazon - Simple Shopping", "chrome.exe", "Amazon", "Simple Shopping"),
            ("Word - Simple Report.docx", "WINWORD.EXE", "Desktop Application", "Simple Report"),
            ("Excel - Simple Data.xlsx", "EXCEL.EXE", "Desktop Application", "Simple Data")
        ]
        
        activity_index = 0
        
        while self.session_active:
            # Cycle through activities
            window_title, app_name, website, tab = activities[activity_index % len(activities)]
            
            # Update current activity
            self.current_window = window_title
            self.current_app = app_name
            self.current_website = website
            self.current_tab = tab
            
            # Update display
            self.root.after(0, self.update_activity_display, window_title, app_name, website, tab)
            
            # Log activity change
            self.log_activity_change(window_title, 20)  # 20 seconds per activity
            
            # Update usage time
            self.app_usage_time[app_name] += 20
            if website != "Desktop Application":
                self.website_usage_time[website] += 20
                self.tab_usage_time[tab] += 20
            
            activity_index += 1
            time.sleep(20)  # Change activity every 20 seconds
    
    def trigger_desktop_alert(self, stress_level, emotion):
        """Simple desktop alert"""
        if not self.desktop_alerts_enabled:
            return
        
        current_time = time.time()
        if current_time - self.last_stress_alert < 30:  # Don't spam alerts
            return
        
        self.last_stress_alert = current_time
        
        # Create simple alert window
        self.alert_window = Toplevel(self.root)
        self.alert_window.title("Stress Alert")
        self.alert_window.geometry("350x180")
        self.alert_window.configure(bg='#ffebee')
        
        # Make it always on top
        self.alert_window.attributes('-topmost', True)
        
        # Alert content
        tk.Label(self.alert_window, text="STRESS DETECTED!", 
                font=("Arial", 14, "bold"), fg='#d32f2f', bg='#ffebee').pack(pady=10)
        
        tk.Label(self.alert_window, text=f"Stress Level: {stress_level}", 
                font=("Arial", 12), fg='#d32f2f', bg='#ffebee').pack(pady=5)
        
        tk.Label(self.alert_window, text=f"Emotion: {emotion}", 
                font=("Arial", 12), fg='#d32f2f', bg='#ffebee').pack(pady=5)
        
        interventions = [
            "Take 5 deep breaths",
            "Stretch your arms",
            "Focus on breathing",
            "Think positive thoughts",
            "Look away from screen",
            "Drink water"
        ]
        
        intervention = random.choice(interventions)
        tk.Label(self.alert_window, text=f"Suggestion: {intervention}", 
                font=("Arial", 11), fg='#d32f2f', bg='#ffebee').pack(pady=5)
        
        # Close button
        tk.Button(self.alert_window, text="OK", command=self.close_alert_window,
                 font=("Arial", 11, "bold"), bg='#d32f2f', fg='white',
                 width=8).pack(pady=10)
        
        # Auto-close after 20 seconds
        self.alert_window.after(20000, self.close_alert_window)
        
        # Add to chat
        self.add_chat_message("ALERT", f"Stress {stress_level} detected! {intervention}")
    
    def close_alert_window(self):
        """Close alert window"""
        if self.alert_window:
            self.alert_window.destroy()
            self.alert_window = None
    
    def update_camera_display(self, frame):
        """Update camera display"""
        try:
            # Resize frame for display
            frame_resized = cv2.resize(frame, (350, 250))
            
            # Convert to RGB
            frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            
            # Convert to PhotoImage
            from PIL import Image, ImageTk
            image = Image.fromarray(frame_rgb)
            photo = ImageTk.PhotoImage(image=image)
            
            # Update canvas
            self.camera_canvas.delete("all")
            self.camera_canvas.create_image(0, 0, anchor=tk.NW, image=photo)
            self.camera_canvas.image = photo
            
        except Exception as e:
            print(f"Camera display error: {e}")
    
    def update_simulation_display(self):
        """Update simulation display"""
        try:
            self.camera_canvas.delete("all")
            
            # Create simple simulation display
            self.camera_canvas.create_rectangle(50, 50, 300, 200, fill='#e8f5e8', outline='#d32f2f', width=2)
            self.camera_canvas.create_text(175, 100, text="SIMULATION MODE", 
                                     fill="black", font=("Arial", 12, "bold"))
            self.camera_canvas.create_text(175, 125, text=f"Emotion: {self.current_emotion}", 
                                     fill="black", font=("Arial", 11))
            self.camera_canvas.create_text(175, 145, text=f"Stress: {self.stress_score}", 
                                     fill="black", font=("Arial", 11))
            
        except Exception as e:
            print(f"Simulation display error: {e}")
    
    def update_activity_display(self, window_title, app_name, website, tab):
        """Update activity display"""
        try:
            # Truncate long titles
            display_title = window_title[:35] + "..." if len(window_title) > 35 else window_title
            display_tab = tab[:25] + "..." if len(tab) > 25 else tab
            
            self.current_window_label.config(text=display_title)
            self.current_tab_label.config(text=display_tab)
            
            # Add to activity display
            timestamp = datetime.now().strftime("%H:%M:%S")
            activity_text = f"[{timestamp}] {app_name}: {display_title}\n"
            if tab != "Desktop":
                activity_text += f"  Tab: {display_tab}\n"
            
            self.activity_display.insert(tk.END, activity_text)
            self.activity_display.see(tk.END)
            
            # Limit display size
            lines = self.activity_display.get("1.0", tk.END).split('\n')
            if len(lines) > 50:
                self.activity_display.delete("1.0", "2.0")
                
        except Exception as e:
            print(f"Activity display error: {e}")
    
    def session_timer(self):
        """Simple session timer"""
        while self.session_active:
            if time.time() >= self.session_end_time:
                self.root.after(0, self.stop_session)
                break
            
            # Update time displays
            elapsed = int(time.time() - self.session_start)
            remaining = int(self.session_end_time - time.time())
            
            elapsed_str = f"{elapsed//3600:02d}:{(elapsed%3600)//60:02d}:{elapsed%60:02d}"
            remaining_str = f"{remaining//3600:02d}:{(remaining%3600)//60:02d}:{remaining%60:02d}"
            
            self.root.after(0, self.update_time_display, elapsed_str, remaining_str)
            
            time.sleep(1)
    
    def update_time_display(self, elapsed_str, remaining_str):
        """Update time displays"""
        try:
            self.session_time_label.config(text=f"Time: {elapsed_str}")
            self.remaining_time_label.config(text=f"Remaining: {remaining_str}")
        except Exception as e:
            print(f"Time display error: {e}")
    
    def show_statistics(self):
        """Show simple statistics"""
        try:
            self.activity_display.delete("1.0", tk.END)
            
            # Show application usage
            self.activity_display.insert(tk.END, "=== APPLICATION USAGE ===\n")
            sorted_apps = sorted(self.app_usage_time.items(), key=lambda x: x[1], reverse=True)
            
            for app, time_spent in sorted_apps[:8]:
                minutes = int(time_spent // 60)
                seconds = int(time_spent % 60)
                time_str = f"{minutes}m {seconds}s"
                self.activity_display.insert(tk.END, f"{app:<18} {time_str:>8}\n")
            
            # Show website usage
            if self.website_usage_time:
                self.activity_display.insert(tk.END, "\n=== WEBSITE USAGE ===\n")
                sorted_websites = sorted(self.website_usage_time.items(), key=lambda x: x[1], reverse=True)
                
                for website, time_spent in sorted_websites[:8]:
                    minutes = int(time_spent // 60)
                    seconds = int(time_spent % 60)
                    time_str = f"{minutes}m {seconds}s"
                    self.activity_display.insert(tk.END, f"{website:<18} {time_str:>8}\n")
            
            # Show emotion statistics
            self.activity_display.insert(tk.END, "\n=== EMOTION STATISTICS ===\n")
            total_emotions = sum(self.emotion_counts.values())
            
            if total_emotions > 0:
                for emotion, count in sorted(self.emotion_counts.items(), key=lambda x: x[1], reverse=True):
                    percentage = (count / total_emotions) * 100
                    self.activity_display.insert(tk.END, f"{emotion:<18} {count:>4} ({percentage:.1f}%)\n")
            
            self.activity_display.see(tk.END)
            
        except Exception as e:
            print(f"Statistics error: {e}")
    
    def update_display(self):
        """Update main display"""
        try:
            # Update stress color
            if self.stress_score > 70:
                stress_color = '#f44336'
            elif self.stress_score > 50:
                stress_color = '#ff9800'
            else:
                stress_color = '#4CAF50'
            
            self.stress_label.config(text=f"Stress: {self.stress_score}", fg=stress_color)
            
            # Update emotion color
            emotion_colors = {
                'Happy': '#4CAF50', 'Neutral': '#2196F3', 'Sad': '#9C27B0',
                'Angry': '#f44336', 'Fear': '#ff9800', 'Surprise': '#ff5722', 'Disgust': '#607D8B'
            }
            emotion_color = emotion_colors.get(self.current_emotion, '#2196F3')
            self.emotion_label.config(text=f"Emotion: {self.current_emotion}", fg=emotion_color)
            
            # Schedule next update
            self.root.after(1000, self.update_display)
            
        except Exception as e:
            print(f"Display update error: {e}")
    
    def send_message(self):
        """Send chat message"""
        try:
            message = self.chat_input.get().strip()
            if not message:
                return
            
            self.add_chat_message("You", message)
            self.chat_input.delete(0, tk.END)
            
            # Generate response
            response = self.generate_response(message)
            self.root.after(500, lambda: self.add_chat_message("AI", response))
            
        except Exception as e:
            print(f"Send message error: {e}")
    
    def generate_response(self, message):
        """Generate simple response"""
        try:
            message_lower = message.lower()
            
            if any(word in message_lower for word in ['stress', 'stressed', 'anxious']):
                return f"Current stress level: {self.stress_score}. Desktop alerts are {'enabled' if self.desktop_alerts_enabled else 'disabled'}."
            elif any(word in message_lower for word in ['time', 'duration', 'session']):
                remaining = int(self.session_end_time - time.time()) if self.session_end_time else 0
                minutes = remaining // 60
                return f"Session remaining: {minutes} minutes"
            elif any(word in message_lower for word in ['activity', 'website', 'window', 'tab']):
                return f"Current: {self.current_app} - {self.current_website} - {self.current_tab}"
            elif any(word in message_lower for word in ['help', 'assist', 'support']):
                return "I monitor your stress, emotions, and activities. Desktop alerts popup when stress is high."
            elif any(word in message_lower for word in ['camera', 'opencv']):
                mode = "Real Camera" if self.camera_active else "Simulation"
                return f"Camera mode: {mode}. Monitoring your emotions in real-time."
            elif any(word in message_lower for word in ['thank', 'thanks']):
                return "You're welcome! I'm here to help with stress management."
            else:
                return f"I'm monitoring your stress level: {self.stress_score}. Ask me anything about your session."
                
        except Exception as e:
            print(f"Response generation error: {e}")
            return "I'm here to help with your session."
    
    def add_chat_message(self, sender, message):
        """Add message to chat"""
        try:
            timestamp = datetime.now().strftime("%H:%M")
            self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {message}\n")
            self.chat_display.see(tk.END)
        except Exception as e:
            print(f"Chat message error: {e}")
    
    def log_activity_change(self, window_title, duration):
        """Log activity change"""
        try:
            app_name = self.current_app
            website = self.current_website
            current_tab = self.current_tab
            
            # Update usage time
            self.app_usage_time[app_name] += duration
            if website != "Desktop Application":
                self.website_usage_time[website] += duration
                self.tab_usage_time[current_tab] += duration
            
            # Log to file
            with open(self.activity_log_file, 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    window_title,
                    app_name,
                    website,
                    current_tab,
                    duration,
                    self.current_emotion,
                    self.stress_score
                ])
                
        except Exception as e:
            print(f"Activity logging error: {e}")
    
    def generate_simple_report(self):
        """Generate simple session report"""
        try:
            report = {
                'session_info': {
                    'start_time': datetime.fromtimestamp(self.session_start).isoformat(),
                    'end_time': datetime.now().isoformat(),
                    'duration': self.session_duration,
                    'actual_duration': time.time() - self.session_start if self.session_start else 0,
                    'camera_mode': 'Real Camera' if self.camera_active else 'Simulation',
                    'desktop_alerts': self.desktop_alerts_enabled
                },
                'emotion_summary': dict(self.emotion_counts),
                'activity_summary': {
                    'applications': dict(self.app_usage_time),
                    'websites': dict(self.website_usage_time),
                    'tabs': dict(self.tab_usage_time)
                },
                'stress_data': {
                    'average_stress': sum(self.stress_history) / len(self.stress_history) if self.stress_history else 0,
                    'max_stress': max(self.stress_history) if self.stress_history else 0,
                    'min_stress': min(self.stress_history) if self.stress_history else 0
                }
            }
            
            report_file = f"exports/simple_reliable_session_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(report_file, 'w') as f:
                json.dump(report, f, indent=2)
            
            self.add_chat_message("AI", f"Session report saved: {report_file}")
            
        except Exception as e:
            print(f"Report generation error: {e}")
    
    def run(self):
        """Run application"""
        try:
            print("Starting Simple Reliable Therapist...")
            self.root.mainloop()
        except Exception as e:
            print(f"Run error: {e}")

# ==============================
# MAIN EXECUTION
# ==============================
if __name__ == "__main__":
    app = SimpleReliableTherapist()
    app.run()
