import math

class CorrosionEngine:
    """
    Hybrid Physics-ML Corrosion Rate Calculation Engine
    Combines empirical models with ML-enhanced predictions
    """
    
    # Base corrosion rates (mm/year) for different materials in various environments
    BASE_RATES = {
        'carbon_steel': {
            'sweet': 0.15,
            'sour_low': 0.8,
            'sour_high': 2.5,
            'subsea': 0.12,
            'high_temp': 0.5
        },
        'stainless_steel_316': {
            'sweet': 0.02,
            'sour_low': 0.15,
            'sour_high': 0.6,
            'subsea': 0.01,
            'high_temp': 0.08
        },
        'duplex_stainless': {
            'sweet': 0.01,
            'sour_low': 0.05,
            'sour_high': 0.25,
            'subsea': 0.005,
            'high_temp': 0.04
        }
    }
    
    @staticmethod
    def temp_correction(temp):
        """Temperature correction factor (Arrhenius-based)"""
        base_temp = 25
        if temp <= base_temp:
            return 1.0
        return math.exp(0.05 * (temp - base_temp))
    
    @staticmethod
    def h2s_correction(h2s_pressure):
        """H2S partial pressure correction"""
        if h2s_pressure < 0.01:
            return 1.0
        return 1 + math.log10(h2s_pressure * 100)
    
    @staticmethod
    def coating_factor(coating_type):
        """Coating effectiveness factor"""
        factors = {
            'none': 1.0,
            '3lpe': 0.05,
            'fbe': 0.08,
            'polyethylene': 0.06,
            'epoxy': 0.10,
            'sacrificial_anode': 0.15
        }
        return factors.get(coating_type, 1.0)
    
    @staticmethod
    def calculate_corrosion_rate(params, use_ml=True):
        """
        Calculate effective corrosion rate
        
        Args:
            params: dict of parameters
            use_ml: bool, whether to use ML enhancement
        
        Returns:
            dict with rate, method used, and confidence
        """
        material = params['material']
        environment = params['environment']
        
        # Get base rate (physics-based)
        base_rate = 0.5  # Default fallback
        if material in CorrosionEngine.BASE_RATES:
            if environment in CorrosionEngine.BASE_RATES[material]:
                base_rate = CorrosionEngine.BASE_RATES[material][environment]
        
        # Apply standard correction factors
        temp_factor = CorrosionEngine.temp_correction(params['temperature'])
        h2s_factor = CorrosionEngine.h2s_correction(params['h2s_pressure'])
        coating_factor = CorrosionEngine.coating_factor(params['coating'])
        
        # Calculate physics-based rate
        physics_rate = base_rate * temp_factor * h2s_factor * coating_factor
        
        # ML Enhancement
        ml_rate = physics_rate
        ml_confidence = 0.0
        method = 'physics'
        
        if use_ml:
            try:
                from ml_predictor import MLCorrosionPredictor
                
                ml_model = MLCorrosionPredictor()
                ml_multiplier = ml_model.predict_corrosion_multiplier(params)
                ml_confidence = ml_model.get_prediction_confidence(params)
                
                # Hybrid approach: blend physics and ML
                # Weight more towards ML if confidence is high
                blend_weight = ml_confidence * 0.6  # Max 60% ML influence
                ml_rate = physics_rate * ((1 - blend_weight) + blend_weight * ml_multiplier)
                method = 'hybrid_physics_ml'
                
            except Exception as e:
                print(f"ML enhancement unavailable: {e}")
                method = 'physics'
        
        return {
            'rate': ml_rate,
            'physics_rate': physics_rate,
            'method': method,
            'ml_confidence': ml_confidence
        }
    
    @staticmethod
    def generate_time_series(initial_thickness, corrosion_rate, design_life):
        """Generate time-series data for wall thickness degradation"""
        data = []
        steps = 50
        time_step = design_life * 1.5 / steps  # Extend beyond design life
        
        for i in range(steps + 1):
            time = i * time_step
            thickness = initial_thickness - (corrosion_rate * time)
            data.append({
                'year': round(time, 1),
                'thickness': round(thickness, 2)
            })
        
        return data
    
    @staticmethod
    def calculate_corrosion(params, use_ml=True):
        """
        Main calculation function with ML enhancement
        
        Returns:
            dict with comprehensive results
        """
        # Calculate corrosion rate
        rate_result = CorrosionEngine.calculate_corrosion_rate(params, use_ml)
        corrosion_rate = rate_result['rate']
        
        # Calculate time to minimum thickness
        thickness_loss_allowed = params['initial_thickness'] - params['min_thickness']
        time_to_failure = thickness_loss_allowed / corrosion_rate
        
        # Generate time series
        time_series = CorrosionEngine.generate_time_series(
            params['initial_thickness'],
            corrosion_rate,
            params['design_life']
        )
        
        return {
            'corrosion_rate': corrosion_rate,
            'physics_rate': rate_result['physics_rate'],
            'time_to_failure': time_to_failure,
            'time_series': time_series,
            'method': rate_result['method'],
            'ml_confidence': rate_result['ml_confidence']
        }
