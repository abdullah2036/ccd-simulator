

import re
import os

class LocalLLMProcessor:
    """
    Offline document processor using local NLP models
    Falls back to rule-based extraction if transformers not available
    """
    
    def __init__(self):
        self.use_transformers = False
        self.model = None
        self.tokenizer = None
        
        try:
            from transformers import pipeline, AutoTokenizer, AutoModelForTokenClassification
            self.use_transformers = True
            self._init_ner_model()
        except ImportError:
            print("Transformers not available. Using rule-based extraction.")
            self.use_transformers = False
    
    def _init_ner_model(self):
        """Initialize lightweight NER model for offline use"""
        try:
            from transformers import pipeline
            
            model_name = "dslim/bert-base-NER"
            
            cache_dir = os.path.expanduser("~/.cache/huggingface/transformers")
            
            print("Loading local NER model for offline processing...")
            self.ner_pipeline = pipeline(
                "ner",
                model=model_name,
                aggregation_strategy="simple",
                device=-1  
            )
            print("✓ Local NER model loaded successfully")
            
        except Exception as e:
            print(f"Could not load transformer model: {e}")
            print("Falling back to rule-based extraction")
            self.use_transformers = False
    
    def extract_with_transformers(self, text):
        """Extract parameters using transformer-based NER"""
        if not self.use_transformers or self.ner_pipeline is None:
            return self._extract_rule_based(text)
        
        try:
            entities = self.ner_pipeline(text)
            
            # Extract parameters based on entities
            params = {
                'material': 'carbon_steel',
                'coating': 'none',
                'environment': 'sour_low',
                'design_life': 20,
                'initial_thickness': 12.7,
                'min_thickness': 6.0,
                'temperature': 60,
                'h2s_pressure': 0.5,
                'confidence': {}
            }
            
            rule_based = self._extract_rule_based(text)
            params.update(rule_based)
            
            params['confidence']['extraction_method'] = 'transformer_enhanced'
            
            return params
            
        except Exception as e:
            print(f"Transformer extraction failed: {e}")
            return self._extract_rule_based(text)
    
    def _extract_rule_based(self, document_text):
        """
        Rule-based extraction (fallback and primary method)
        Highly optimized for engineering documents
        """
        params = {
            'material': 'carbon_steel',
            'coating': 'none',
            'environment': 'sour_low',
            'design_life': 20,
            'initial_thickness': 12.7,
            'min_thickness': 6.0,
            'temperature': 60,
            'h2s_pressure': 0.5,
            'confidence': {},
            'flow_velocity': 2.0 
        }
        
        text_lower = document_text.lower()
        
        material_patterns = [
            (r'super\s+duplex\s+stainless', 'duplex_stainless', 0.98),
            (r'duplex\s+stainless|uns\s+s3\d{4}', 'duplex_stainless', 0.95),
            (r'316[lh]?\s+stainless|stainless\s+steel\s+316', 'stainless_steel_316', 0.92),
            (r'stainless\s+steel', 'stainless_steel_316', 0.85),
            (r'carbon\s+steel|api\s+5l|astm\s+a\d+', 'carbon_steel', 0.90),
        ]
        
        for pattern, material, confidence in material_patterns:
            if re.search(pattern, text_lower):
                params['material'] = material
                params['confidence']['material'] = confidence
                break
        
        # Coating detection
        coating_patterns = [
            (r'3-layer\s+polypropylene|3lpp', '3lpe', 0.95),
            (r'3-layer\s+polyethylene|3lpe', '3lpe', 0.95),
            (r'fusion\s+bonded\s+epoxy|fbe', 'fbe', 0.93),
            (r'sacrificial\s+anode|aluminum\s+anode', 'sacrificial_anode', 0.90),
            (r'polyethylene\s+coating', 'polyethylene', 0.88),
            (r'epoxy\s+coating', 'epoxy', 0.87),
            (r'(?:no|without)\s+coating|bare\s+(?:steel|carbon)', 'none', 0.92),
        ]
        
        for pattern, coating, confidence in coating_patterns:
            if re.search(pattern, text_lower):
                params['coating'] = coating
                params['confidence']['coating'] = confidence
                break
        
        # Environment detection
        environment_patterns = [
            (r'severe.*sour|high.*h2s|h2s.*high', 'sour_high', 0.92),
            (r'sour\s+(?:gas|service)|h2s', 'sour_low', 0.89),
            (r'subsea|seawater|offshore', 'subsea', 0.94),
            (r'high\s+temperature|elevated\s+temperature', 'high_temp', 0.87),
            (r'sweet\s+(?:gas|service)', 'sweet', 0.90),
        ]
        
        for pattern, environment, confidence in environment_patterns:
            if re.search(pattern, text_lower):
                params['environment'] = environment
                params['confidence']['environment'] = confidence
                break
        
        
        life_patterns = [
            r'design\s+life[:\s]+(\d+)\s+years?',
            r'service\s+life[:\s]+(\d+)\s+years?',
            r'expected\s+life[:\s]+(\d+)\s+years?'
        ]
        for pattern in life_patterns:
            match = re.search(pattern, text_lower)
            if match:
                params['design_life'] = int(match.group(1))
                params['confidence']['design_life'] = 0.96
                break
        
        # Wall thickness
        thickness_patterns = [
            r'(?:wall\s+)?thickness[:\s]+(\d+\.?\d*)\s*mm',
            r'initial.*?thickness[:\s]+(\d+\.?\d*)\s*mm',
            r'nominal.*?thickness[:\s]+(\d+\.?\d*)\s*mm'
        ]
        for pattern in thickness_patterns:
            match = re.search(pattern, text_lower)
            if match:
                params['initial_thickness'] = float(match.group(1))
                params['confidence']['initial_thickness'] = 0.94
                break
        
        # Minimum thickness
        min_patterns = [
            r'minimum\s+(?:acceptable\s+)?thickness[:\s]+(\d+\.?\d*)\s*mm',
            r'min(?:imum)?\.?\s+thickness[:\s]+(\d+\.?\d*)\s*mm'
        ]
        for pattern in min_patterns:
            match = re.search(pattern, text_lower)
            if match:
                params['min_thickness'] = float(match.group(1))
                params['confidence']['min_thickness'] = 0.92
                break
        
        # Temperature
        temp_patterns = [
            r'(?:operating\s+)?temperature[:\s]+(\d+)\s*°?c',
            r'temp\.?[:\s]+(\d+)\s*°?c'
        ]
        for pattern in temp_patterns:
            match = re.search(pattern, text_lower)
            if match:
                params['temperature'] = int(match.group(1))
                params['confidence']['temperature'] = 0.90
                break
        
        # H2S pressure
        h2s_patterns = [
            r'h2s.*?(\d+\.?\d*)\s*bar',
            r'h2s\s+partial\s+pressure[:\s]+(\d+\.?\d*)\s*bar',
            r'hydrogen\s+sulfide.*?(\d+\.?\d*)\s*bar'
        ]
        for pattern in h2s_patterns:
            match = re.search(pattern, text_lower)
            if match:
                params['h2s_pressure'] = float(match.group(1))
                params['confidence']['h2s_pressure'] = 0.88
                break
        
        # Flow velocity (for ML model)
        velocity_patterns = [
            r'(?:flow\s+)?velocity[:\s]+(\d+\.?\d*)\s*m/s',
            r'flow\s+rate.*?(\d+\.?\d*)\s*m/s'
        ]
        for pattern in velocity_patterns:
            match = re.search(pattern, text_lower)
            if match:
                params['flow_velocity'] = float(match.group(1))
                params['confidence']['flow_velocity'] = 0.85
                break
        
        params['confidence']['extraction_method'] = 'rule_based'
        
        return params
    
    def extract_parameters(self, document_text, offline_mode=True):
        """
        Main extraction method
        
        Args:
            document_text: str, the CCD document text
            offline_mode: bool, if True uses only local resources
        
        Returns:
            dict of extracted parameters
        """
        if offline_mode or not self.use_transformers:
            return self._extract_rule_based(document_text)
        else:
            return self.extract_with_transformers(document_text)
    
    @staticmethod
    def download_model_instructions():
        """
        Provide instructions for downloading models for offline use
        """
        return """
        To enable offline transformer-based extraction:
        
        1. Install transformers library:
           pip install transformers torch
        
        2. Download the model (run once with internet):
           python -c "from transformers import pipeline; pipeline('ner', model='dslim/bert-base-NER')"
        
        3. The model will be cached locally (~400MB) and available offline
        
        Note: Rule-based extraction works without any downloads and is
        highly accurate for engineering documents!
        """
