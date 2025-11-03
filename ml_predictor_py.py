"""
ML-Enhanced Corrosion Rate Predictor
Hybrid Physics-ML Engine for improved prediction fidelity
"""

import numpy as np
import pickle
import os
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler

class MLCorrosionPredictor:
    """
    Machine Learning model to refine corrosion rate predictions
    Uses Random Forest to predict correction factors based on interacting variables
    """
    
    def __init__(self):
        self.model = None
        self.scaler = None
        self.is_trained = False
        
        # Try to load pre-trained model
        self._load_or_train_model()
    
    def _generate_synthetic_training_data(self, n_samples=1000):
        """
        Generate synthetic training data based on empirical corrosion knowledge
        In production, this would be replaced with real field data
        """
        np.random.seed(42)
        
        # Input features: temperature, h2s_pressure, coating_quality, material_grade, flow_velocity
        X = []
        y = []
        
        for _ in range(n_samples):
            temp = np.random.uniform(20, 150)  # °C
            h2s = np.random.uniform(0, 2.0)     # bar
            coating_quality = np.random.uniform(0.5, 1.0)  # 0.5=degraded, 1.0=perfect
            material_grade = np.random.choice([1, 2, 3])   # 1=carbon steel, 2=316SS, 3=duplex
            flow_velocity = np.random.uniform(0.5, 5.0)    # m/s
            
            # Physics-informed synthetic response
            # Base corrosion multiplier starts at 1.0
            multiplier = 1.0
            
            # Temperature effect (Arrhenius)
            temp_factor = np.exp(0.05 * (temp - 25) / 25)
            multiplier *= temp_factor
            
            # H2S effect (logarithmic)
            if h2s > 0.01:
                h2s_factor = 1 + 0.5 * np.log10(h2s * 100 + 1)
                multiplier *= h2s_factor
            
            # Coating degradation (inverse relationship)
            coating_factor = 2.0 - coating_quality  # Poor coating = higher multiplier
            multiplier *= coating_factor
            
            # Material resistance
            material_factors = {1: 1.0, 2: 0.3, 3: 0.15}
            multiplier *= material_factors[material_grade]
            
            # Flow velocity (erosion-corrosion)
            if flow_velocity > 3.0:
                velocity_factor = 1 + 0.2 * (flow_velocity - 3.0)
                multiplier *= velocity_factor
            
            # Add some realistic noise
            multiplier *= np.random.uniform(0.85, 1.15)
            
            X.append([temp, h2s, coating_quality, material_grade, flow_velocity])
            y.append(multiplier)
        
        return np.array(X), np.array(y)
    
    def _load_or_train_model(self):
        """Load existing model or train a new one"""
        model_path = 'ml_corrosion_model.pkl'
        scaler_path = 'ml_scaler.pkl'
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            try:
                with open(model_path, 'rb') as f:
                    self.model = pickle.load(f)
                with open(scaler_path, 'rb') as f:
                    self.scaler = pickle.load(f)
                self.is_trained = True
                return
            except:
                pass
        
        # Train new model
        X, y = self._generate_synthetic_training_data()
        
        # Scale features
        self.scaler = StandardScaler()
        X_scaled = self.scaler.fit_transform(X)
        
        # Train Random Forest
        self.model = RandomForestRegressor(
            n_estimators=100,
            max_depth=10,
            random_state=42,
            n_jobs=-1
        )
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        # Save model
        try:
            with open(model_path, 'wb') as f:
                pickle.dump(self.model, f)
            with open(scaler_path, 'wb') as f:
                pickle.dump(self.scaler, f)
        except:
            pass  # OK if can't save
    
    def predict_corrosion_multiplier(self, params):
        """
        Predict corrosion rate multiplier using ML
        
        Args:
            params: dict with keys:
                - temperature: float (°C)
                - h2s_pressure: float (bar)
                - coating: str (coating type)
                - material: str (material type)
                - flow_velocity: float (m/s, optional)
        
        Returns:
            float: ML-predicted corrosion rate multiplier
        """
        if not self.is_trained:
            return 1.0  # Fallback
        
        # Convert coating to quality score
        coating_quality_map = {
            'none': 0.5,
            'epoxy': 0.75,
            'fbe': 0.85,
            'polyethylene': 0.85,
            '3lpe': 0.95,
            'sacrificial_anode': 0.90
        }
        coating_quality = coating_quality_map.get(params.get('coating', 'none'), 0.7)
        
        # Convert material to grade
        material_grade_map = {
            'carbon_steel': 1,
            'stainless_steel_316': 2,
            'duplex_stainless': 3
        }
        material_grade = material_grade_map.get(params.get('material', 'carbon_steel'), 1)
        
        # Extract other features
        temp = params.get('temperature', 60)
        h2s = params.get('h2s_pressure', 0.5)
        flow_velocity = params.get('flow_velocity', 2.0)  # Default moderate velocity
        
        # Prepare feature vector
        X = np.array([[temp, h2s, coating_quality, material_grade, flow_velocity]])
        X_scaled = self.scaler.transform(X)
        
        # Predict
        multiplier = self.model.predict(X_scaled)[0]
        
        # Ensure reasonable bounds
        multiplier = np.clip(multiplier, 0.1, 5.0)
        
        return multiplier
    
    def get_feature_importance(self):
        """Get feature importance for explainability"""
        if not self.is_trained or self.model is None:
            return {}
        
        feature_names = ['Temperature', 'H2S Pressure', 'Coating Quality', 
                        'Material Grade', 'Flow Velocity']
        importances = self.model.feature_importances_
        
        return dict(zip(feature_names, importances))
    
    def get_prediction_confidence(self, params):
        """
        Estimate prediction confidence using ensemble variance
        Returns confidence score between 0 and 1
        """
        if not self.is_trained:
            return 0.5
        
        # Get predictions from all trees
        coating_quality_map = {
            'none': 0.5, 'epoxy': 0.75, 'fbe': 0.85,
            'polyethylene': 0.85, '3lpe': 0.95, 'sacrificial_anode': 0.90
        }
        material_grade_map = {
            'carbon_steel': 1, 'stainless_steel_316': 2, 'duplex_stainless': 3
        }
        
        coating_quality = coating_quality_map.get(params.get('coating', 'none'), 0.7)
        material_grade = material_grade_map.get(params.get('material', 'carbon_steel'), 1)
        temp = params.get('temperature', 60)
        h2s = params.get('h2s_pressure', 0.5)
        flow_velocity = params.get('flow_velocity', 2.0)
        
        X = np.array([[temp, h2s, coating_quality, material_grade, flow_velocity]])
        X_scaled = self.scaler.transform(X)
        
        # Get predictions from individual trees
        tree_predictions = [tree.predict(X_scaled)[0] for tree in self.model.estimators_]
        
        # Calculate variance (lower variance = higher confidence)
        variance = np.var(tree_predictions)
        
        # Convert to confidence score (0-1)
        confidence = 1.0 / (1.0 + variance)
        
        return confidence
