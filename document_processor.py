import re
import random

class DocumentProcessor:
    """
    Document processor with offline LLM capability
    """
    
    @staticmethod
    def extract_parameters(document_text, offline_mode=True, use_local_llm=True):
        """
        Extract parameters from CCD document
        
        Args:
            document_text: str, document content
            offline_mode: bool, whether to use offline processing
            use_local_llm: bool, whether to attempt local LLM (vs rule-based only)
        
        Returns:
            dict of extracted parameters
        """
        if use_local_llm:
            try:
                from local_llm_processor import LocalLLMProcessor
                processor = LocalLLMProcessor()
                return processor.extract_parameters(document_text, offline_mode)
            except Exception as e:
                print(f"Local LLM not available: {e}")
                # Fall through to rule-based
        
        # Rule-based extraction (always available as fallback)
        return DocumentProcessor._extract_rule_based(document_text)
    
    @staticmethod
    def _extract_rule_based(document_text):
        """Rule-based extraction - highly reliable for engineering documents"""
        params = {
            'material': 'carbon_steel',
            'coating': 'none',
            'environment': 'sour_low',
            'design_life': 20,
            'initial_thickness': 12.7,
            'min_thickness': 6.0,
            'temperature': 60,
            'h2s_pressure': 0.5,
            'flow_velocity': 2.0,
            'confidence': {}
        }
        
        text_lower = document_text.lower()
        
        # Material detection
        if re.search(r'duplex\s+stainless', text_lower):
            params['material'] = 'duplex_stainless'
            params['confidence']['material'] = 0.95
        elif re.search(r'316\s+stainless|stainless\s+steel', text_lower):
            params['material'] = 'stainless_steel_316'
            params['confidence']['material'] = 0.90
        elif re.search(r'carbon\s+steel', text_lower):
            params['material'] = 'carbon_steel'
            params['confidence']['material'] = 0.92
        
        # Coating detection
        if re.search(r'3-layer\s+polyethylene|3lpe', text_lower):
            params['coating'] = '3lpe'
            params['confidence']['coating'] = 0.93
        elif re.search(r'fbe|fusion\s+bonded\s+epoxy', text_lower):
            params['coating'] = 'fbe'
            params['confidence']['coating'] = 0.91
        elif re.search(r'sacrificial\s+anode', text_lower):
            params['coating'] = 'sacrificial_anode'
            params['confidence']['coating'] = 0.88
        elif re.search(r'polyethylene', text_lower):
            params['coating'] = 'polyethylene'
            params['confidence']['coating'] = 0.85
        elif re.search(r'epoxy', text_lower):
            params['coating'] = 'epoxy'
            params['confidence']['coating'] = 0.87
        
        # Environment detection
        if re.search(r'sour\s+gas|h2s', text_lower):
            if re.search(r'high.*h2s|severe.*sour', text_lower):
                params['environment'] = 'sour_high'
            else:
                params['environment'] = 'sour_low'
            params['confidence']['environment'] = 0.89
        elif re.search(r'subsea', text_lower):
            params['environment'] = 'subsea'
            params['confidence']['environment'] = 0.94
        elif re.search(r'high\s+temperature', text_lower):
            params['environment'] = 'high_temp'
            params['confidence']['environment'] = 0.87
        elif re.search(r'sweet', text_lower):
            params['environment'] = 'sweet'
            params['confidence']['environment'] = 0.90
        
        # Extract numeric values
        design_life_match = re.search(r'design\s+life[:\s]+(\d+)\s+years?', text_lower)
        if design_life_match:
            params['design_life'] = int(design_life_match.group(1))
            params['confidence']['design_life'] = 0.96
        
        thickness_match = re.search(r'(?:wall\s+)?thickness[:\s]+(\d+\.?\d*)\s*mm', text_lower)
        if thickness_match:
            params['initial_thickness'] = float(thickness_match.group(1))
            params['confidence']['initial_thickness'] = 0.94
        
        min_thickness_match = re.search(r'minimum[:\s]+(\d+\.?\d*)\s*mm', text_lower)
        if min_thickness_match:
            params['min_thickness'] = float(min_thickness_match.group(1))
            params['confidence']['min_thickness'] = 0.92
        
        temp_match = re.search(r'temperature[:\s]+(\d+)\s*°?c', text_lower)
        if temp_match:
            params['temperature'] = int(temp_match.group(1))
            params['confidence']['temperature'] = 0.90
        
        h2s_match = re.search(r'h2s.*?(\d+\.?\d*)\s*bar', text_lower)
        if h2s_match:
            params['h2s_pressure'] = float(h2s_match.group(1))
            params['confidence']['h2s_pressure'] = 0.88
        
        velocity_match = re.search(r'velocity[:\s]+(\d+\.?\d*)\s*m/s', text_lower)
        if velocity_match:
            params['flow_velocity'] = float(velocity_match.group(1))
            params['confidence']['flow_velocity'] = 0.85
        
        return params
    
    @staticmethod
    def generate_sample_document(risk_level='moderate'):
        """Generate a random sample CCD document"""
        
        pipeline_id = f"{random.choice(['A', 'B', 'C', 'D'])}-{random.randint(100, 999)}"
        
        if risk_level == 'critical':
            materials = ['Carbon Steel API 5L X65', 'Carbon Steel API 5L X52']
            coatings = ['None (Internal lining only)', 'Epoxy coating']
            environments = ['Sour gas service with H2S partial pressure 1.2 bar',
                          'Sour gas service with high H2S concentration']
            design_lives = [25, 30]
            thicknesses = [12.7, 10.0, 11.5]
            min_thicknesses = [6.0, 5.0]
            temps = [85, 95, 75]
            pressures = [70, 80, 90]
            velocities = [3.5, 4.0, 4.5]
            
        elif risk_level == 'moderate':
            materials = ['316 Stainless Steel', 'Carbon Steel with corrosion allowance']
            coatings = ['Fusion Bonded Epoxy (FBE)', 'Polyethylene coating']
            environments = ['Sour service, low H2S concentration',
                          'High temperature service']
            design_lives = [20, 25]
            thicknesses = [10.0, 12.0, 15.0]
            min_thicknesses = [5.0, 6.0]
            temps = [60, 70, 55]
            pressures = [45, 50, 60]
            velocities = [2.5, 3.0, 2.0]
            
        else:  # acceptable
            materials = ['Duplex Stainless Steel UNS S31803', 'Super Duplex Stainless Steel']
            coatings = ['3-layer Polyethylene (3LPE) external coating',
                       'FBE with cathodic protection']
            environments = ['Subsea service, seawater exposure',
                          'Sweet service, non-corrosive']
            design_lives = [30, 35, 40]
            thicknesses = [15.0, 18.0, 20.0]
            min_thicknesses = [8.0, 10.0]
            temps = [40, 35, 45]
            pressures = [150, 120, 100]
            velocities = [1.5, 2.0, 1.0]
        
        material = random.choice(materials)
        coating = random.choice(coatings)
        environment = random.choice(environments)
        design_life = random.choice(design_lives)
        thickness = random.choice(thicknesses)
        min_thickness = random.choice(min_thicknesses)
        temp = random.choice(temps)
        pressure = random.choice(pressures)
        velocity = random.choice(velocities)
        
        sections = ['Pipeline', 'Process Piping', 'Subsea Pipeline', 'Flowline']
        section = random.choice(sections)
        
        inspection_intervals = [2, 3, 5, 7] if risk_level == 'critical' else [5, 7, 10]
        inspection = random.choice(inspection_intervals)
        
        document = f"""CORROSION CONTROL DOCUMENT - {section} {pipeline_id}

Material: {material}
Coating: {coating}
Environment: {environment}
Design Life: {design_life} years
Wall Thickness: {thickness} mm
Minimum Acceptable Thickness: {min_thickness} mm
Operating Temperature: {temp}°C
Pressure: {pressure} bar
Flow Velocity: {velocity} m/s

"""
        
        if risk_level == 'critical':
            document += f"""Corrosion mitigation relies on chemical inhibitor injection at {random.choice([50, 75, 100])} ppm.
Critical service classification requires enhanced monitoring protocols.
Regular inspection intervals every {inspection} years with ultrasonic testing.
H2S partial pressure: {random.uniform(0.5, 1.5):.2f} bar

Notes: High risk environment requires immediate attention to corrosion control measures.
"""
        elif risk_level == 'moderate':
            document += f"""Regular inspection intervals every {inspection} years with ultrasonic testing.
Chemical injection system installed for corrosion inhibition.
Cathodic protection monitoring quarterly.

Notes: Standard corrosion control measures in place.
"""
        else:
            document += f"""Cathodic protection system with sacrificial anodes installed at {random.choice([300, 500, 800])}m intervals.
Comprehensive coating system provides primary corrosion protection.
Regular inspection intervals every {inspection} years with ultrasonic testing.
Design includes {random.choice([15, 20, 25])}% corrosion allowance.

Notes: Robust corrosion control system with multiple protection layers.
"""
        
        document += f"""
Asset ID: {pipeline_id}
Document Version: 1.{random.randint(0, 9)}
Date: 2024-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}
Prepared by: Engineering Department
"""
        
        return document
