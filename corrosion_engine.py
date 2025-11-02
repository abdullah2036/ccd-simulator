import math

class CorrosionEngine:
    """
    Physics-based corrosion rate calculation engine
    Based on NACE/API empirical models
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
    def calculate_corrosion_rate(params):
        """Calculate effective corrosion rate"""
        material = params['material']
        environment = params['environment']
        
        # Get base rate
        base_rate = 0.5  # Default fallback
        if material in CorrosionEngine.BASE_RATES:
            if environment in CorrosionEngine.BASE_RATES[material]:
                base_rate = CorrosionEngine.BASE_RATES[material][environment]
        
        # Apply correction factors
        temp_factor = CorrosionEngine.temp_correction(params['temperature'])
        h2s_factor = CorrosionEngine.h2s_correction(params['h2s_pressure'])
        coating_factor = CorrosionEngine.coating_factor(params['coating'])
        
        # Calculate effective rate
        effective_rate = base_rate * temp_factor * h2s_factor * coating_factor
        
        return effective_rate
    
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
    def calculate_corrosion(params):
        """Main calculation function"""
        # Calculate corrosion rate
        corrosion_rate = CorrosionEngine.calculate_corrosion_rate(params)
        
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
            'time_to_failure': time_to_failure,
            'time_series': time_series
        }
