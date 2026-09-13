import os
import pickle
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report, accuracy_score
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def generate_synthetic_data(samples=1000):
    """Generate synthetic face geometry data based on established rules."""
    np.random.seed(42)
    features = []
    labels = []
    
    shapes = ['oval', 'round', 'square', 'oblong', 'heart', 'diamond']
    
    for _ in range(samples):
        shape = np.random.choice(shapes)
        
        # Base dimensions
        width = 1.0
        
        if shape == 'oval':
            length = np.random.uniform(1.15, 1.35)
            forehead = np.random.uniform(0.7, 0.9)
            cheekbone = np.random.uniform(0.8, 1.0)
            jaw = np.random.uniform(0.6, 0.8)
        elif shape == 'round':
            length = np.random.uniform(0.9, 1.15)
            forehead = np.random.uniform(0.8, 0.95)
            cheekbone = np.random.uniform(0.9, 1.0)
            jaw = np.random.uniform(0.7, 0.9)
        elif shape == 'square':
            length = np.random.uniform(0.9, 1.15)
            forehead = np.random.uniform(0.85, 1.0)
            cheekbone = np.random.uniform(0.85, 1.0)
            jaw = np.random.uniform(0.85, 1.0) # prominent jaw
        elif shape == 'oblong':
            length = np.random.uniform(1.35, 1.6)
            forehead = np.random.uniform(0.7, 0.9)
            cheekbone = np.random.uniform(0.7, 0.9)
            jaw = np.random.uniform(0.7, 0.9)
        elif shape == 'heart':
            length = np.random.uniform(1.1, 1.3)
            forehead = np.random.uniform(0.9, 1.0)
            cheekbone = np.random.uniform(0.8, 0.9)
            jaw = np.random.uniform(0.5, 0.7) # narrow jaw
        else: # diamond
            length = np.random.uniform(1.1, 1.3)
            cheekbone = 1.0 # widest
            forehead = np.random.uniform(0.7, 0.85)
            jaw = np.random.uniform(0.6, 0.75)

        chin_width = jaw * 0.5
        
        f = [
            length, width, forehead, cheekbone, jaw, chin_width,
            length/width, jaw/width, forehead/width
        ]
        features.append(f)
        labels.append(shape)
        
    return np.array(features), np.array(labels)

def train_face_shape_model():
    logger.info("Generating synthetic training data...")
    X, y = generate_synthetic_data(5000)
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    logger.info("Training Random Forest Classifier with Grid Search...")
    param_grid = {
        'n_estimators': [50, 100, 200],
        'max_depth': [None, 10, 20],
        'min_samples_split': [2, 5]
    }
    
    rf = RandomForestClassifier(random_state=42)
    clf = GridSearchCV(rf, param_grid, cv=5)
    clf.fit(X_train_scaled, y_train)
    
    best_model = clf.best_estimator_
    y_pred = best_model.predict(X_test_scaled)
    
    logger.info(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
    logger.info("\n" + classification_report(y_test, y_pred))
    
    os.makedirs('../saved_models', exist_ok=True)
    save_path = '../saved_models/face_shape_model.pkl'
    
    with open(save_path, 'wb') as f:
        pickle.dump({'model': best_model, 'scaler': scaler}, f)
        
    logger.info(f"Saved model and scaler to {save_path}")

if __name__ == "__main__":
    train_face_shape_model()
