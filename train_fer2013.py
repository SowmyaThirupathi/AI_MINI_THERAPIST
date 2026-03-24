"""
FER2013 DATASET TRAINING SCRIPT
Train emotion recognition model on FER2013 dataset
"""

import cv2
import numpy as np
import os
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout, BatchNormalization
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class FER2013Trainer:
    def __init__(self):
        print("INITIALIZING FER2013 TRAINER...")
        
        # FER2013 emotion labels
        self.emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']
        self.num_classes = 7
        
        # Dataset paths
        self.dataset_path = "fer2013_dataset"
        self.train_path = os.path.join(self.dataset_path, "train")
        self.test_path = os.path.join(self.dataset_path, "test")
        
        # Model parameters
        self.img_size = (48, 48)
        self.batch_size = 64
        self.epochs = 50
        
        print("FER2013 TRAINER READY!")
    
    def setup_dataset_directories(self):
        """Create FER2013 dataset directory structure"""
        print("Setting up FER2013 dataset directories...")
        
        # Create main dataset directory
        os.makedirs(self.dataset_path, exist_ok=True)
        
        # Create train and test directories
        os.makedirs(self.train_path, exist_ok=True)
        os.makedirs(self.test_path, exist_ok=True)
        
        # Create emotion subdirectories
        for emotion in self.emotion_labels:
            os.makedirs(os.path.join(self.train_path, emotion.lower()), exist_ok=True)
            os.makedirs(os.path.join(self.test_path, emotion.lower()), exist_ok=True)
        
        print("FER2013 dataset directories created successfully!")
        
        # Show structure
        print("\nFER2013 Dataset Structure:")
        print("fer2013_dataset/")
        print("├── train/")
        print("│   ├── angry/")
        print("│   ├── disgust/")
        print("│   ├── fear/")
        print("│   ├── happy/")
        print("│   ├── sad/")
        print("│   ├── surprise/")
        print("│   └── neutral/")
        print("└── test/")
        print("    ├── angry/")
        print("    ├── disgust/")
        print("    ├── fear/")
        print("    ├── happy/")
        print("    ├── sad/")
        print("    ├── surprise/")
        print("    └── neutral/")
    
    def load_fer2013_data(self):
        """Load FER2013 dataset from directories"""
        print("Loading FER2013 dataset...")
        
        X_train, y_train = [], []
        X_test, y_test = [], []
        
        # Load training data
        for emotion_idx, emotion in enumerate(self.emotion_labels):
            emotion_path = os.path.join(self.train_path, emotion.lower())
            if os.path.exists(emotion_path):
                for img_file in os.listdir(emotion_path):
                    if img_file.endswith(('.jpg', '.jpeg', '.png')):
                        img_path = os.path.join(emotion_path, img_file)
                        try:
                            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                            if img is not None:
                                img_resized = cv2.resize(img, self.img_size)
                                X_train.append(img_resized)
                                y_train.append(emotion_idx)
                        except Exception as e:
                            print(f"Error loading {img_path}: {e}")
        
        # Load test data
        for emotion_idx, emotion in enumerate(self.emotion_labels):
            emotion_path = os.path.join(self.test_path, emotion.lower())
            if os.path.exists(emotion_path):
                for img_file in os.listdir(emotion_path):
                    if img_file.endswith(('.jpg', '.jpeg', '.png')):
                        img_path = os.path.join(emotion_path, img_file)
                        try:
                            img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                            if img is not None:
                                img_resized = cv2.resize(img, self.img_size)
                                X_test.append(img_resized)
                                y_test.append(emotion_idx)
                        except Exception as e:
                            print(f"Error loading {img_path}: {e}")
        
        # Convert to numpy arrays
        X_train = np.array(X_train)
        X_test = np.array(X_test)
        y_train = np.array(y_train)
        y_test = np.array(y_test)
        
        # Normalize and reshape
        X_train = X_train / 255.0
        X_test = X_test / 255.0
        
        X_train = X_train.reshape(X_train.shape[0], 48, 48, 1)
        X_test = X_test.reshape(X_test.shape[0], 48, 48, 1)
        
        # One-hot encode labels
        y_train = to_categorical(y_train, self.num_classes)
        y_test = to_categorical(y_test, self.num_classes)
        
        print(f"Training data shape: {X_train.shape}")
        print(f"Test data shape: {X_test.shape}")
        print(f"Training labels shape: {y_train.shape}")
        print(f"Test labels shape: {y_test.shape}")
        
        return X_train, X_test, y_train, y_test
    
    def create_fer_model(self):
        """Create FER2013 CNN model"""
        print("Creating FER2013 CNN model...")
        
        model = Sequential([
            # First block
            Conv2D(32, (3, 3), activation='relu', padding='same', input_shape=(48, 48, 1)),
            BatchNormalization(),
            Conv2D(32, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Second block
            Conv2D(64, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(64, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Third block
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(128, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Fourth block
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            Conv2D(256, (3, 3), activation='relu', padding='same'),
            BatchNormalization(),
            MaxPooling2D(2, 2),
            Dropout(0.25),
            
            # Dense layers
            Flatten(),
            Dense(512, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(256, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(128, activation='relu'),
            BatchNormalization(),
            Dropout(0.5),
            Dense(7, activation='softmax')  # 7 FER2013 emotions
        ])
        
        model.compile(
            optimizer='adam',
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        model.summary()
        return model
    
    def train_model(self, X_train, X_test, y_train, y_test):
        """Train FER2013 model"""
        print("Training FER2013 model...")
        
        # Create model
        model = self.create_fer_model()
        
        # Data augmentation
        datagen = tf.keras.preprocessing.image.ImageDataGenerator(
            rotation_range=10,
            width_shift_range=0.1,
            height_shift_range=0.1,
            zoom_range=0.1,
            horizontal_flip=True,
            fill_mode='nearest'
        )
        
        # Train model
        history = model.fit(
            datagen.flow(X_train, y_train, batch_size=self.batch_size),
            epochs=self.epochs,
            validation_data=(X_test, y_test),
            verbose=1
        )
        
        # Save model
        model_path = "models/fer2013_trained_model.h5"
        os.makedirs("models", exist_ok=True)
        model.save(model_path)
        print(f"Model saved to: {model_path}")
        
        # Evaluate model
        test_loss, test_acc = model.evaluate(X_test, y_test, verbose=0)
        print(f"Test accuracy: {test_acc:.4f}")
        
        return model, history
    
    def generate_sample_data(self):
        """Generate sample FER2013 data for testing"""
        print("Generating sample FER2013 data...")
        
        # Create sample images for each emotion
        for emotion in self.emotion_labels:
            emotion_path = os.path.join(self.train_path, emotion.lower())
            test_emotion_path = os.path.join(self.test_path, emotion.lower())
            
            # Generate 20 training samples per emotion
            for i in range(20):
                # Create random grayscale image
                img = np.random.randint(0, 256, (48, 48), dtype=np.uint8)
                
                # Add some patterns to make it more realistic
                if emotion.lower() == 'happy':
                    # Add smile pattern
                    img[20:30, 15:35] = 200
                elif emotion.lower() == 'angry':
                    # Add angry pattern
                    img[10:20, 15:35] = 100
                elif emotion.lower() == 'sad':
                    # Add sad pattern
                    img[25:35, 15:35] = 50
                elif emotion.lower() == 'surprise':
                    # Add surprise pattern
                    img[15:25, 20:30] = 250
                elif emotion.lower() == 'fear':
                    # Add fear pattern
                    img[10:20, 20:30] = 80
                elif emotion.lower() == 'disgust':
                    # Add disgust pattern
                    img[20:30, 20:30] = 120
                elif emotion.lower() == 'neutral':
                    # Add neutral pattern
                    img[15:35, 15:35] = 128
                
                # Save training image
                train_img_path = os.path.join(emotion_path, f"{emotion.lower()}_train_{i:03d}.png")
                cv2.imwrite(train_img_path, img)
            
            # Generate 5 test samples per emotion
            for i in range(5):
                img = np.random.randint(0, 256, (48, 48), dtype=np.uint8)
                
                # Add similar patterns for test data
                if emotion.lower() == 'happy':
                    img[20:30, 15:35] = 200
                elif emotion.lower() == 'angry':
                    img[10:20, 15:35] = 100
                elif emotion.lower() == 'sad':
                    img[25:35, 15:35] = 50
                elif emotion.lower() == 'surprise':
                    img[15:25, 20:30] = 250
                elif emotion.lower() == 'fear':
                    img[10:20, 20:30] = 80
                elif emotion.lower() == 'disgust':
                    img[20:30, 20:30] = 120
                elif emotion.lower() == 'neutral':
                    img[15:35, 15:35] = 128
                
                # Save test image
                test_img_path = os.path.join(test_emotion_path, f"{emotion.lower()}_test_{i:03d}.png")
                cv2.imwrite(test_img_path, img)
        
        print("Sample FER2013 data generated successfully!")
    
    def run_training(self):
        """Main training process"""
        try:
            print("=== FER2013 TRAINING PROCESS ===")
            
            # Setup directories
            self.setup_dataset_directories()
            
            # Check if dataset exists
            if not os.path.exists(self.train_path) or not os.listdir(self.train_path):
                print("No dataset found. Generating sample data...")
                self.generate_sample_data()
            
            # Load data
            X_train, X_test, y_train, y_test = self.load_fer2013_data()
            
            if len(X_train) == 0:
                print("No training data found. Please add FER2013 dataset images to the directories.")
                print("Or use the generated sample data for testing.")
                return
            
            # Train model
            model, history = self.train_model(X_train, X_test, y_train, y_test)
            
            print("=== FER2013 TRAINING COMPLETED ===")
            print("Model saved to: models/fer2013_trained_model.h5")
            print("Ready for use in AI Mini Therapist!")
            
        except Exception as e:
            print(f"Training error: {e}")

# ==============================
# MAIN EXECUTION
# ==============================
if __name__ == "__main__":
    trainer = FER2013Trainer()
    trainer.run_training()
