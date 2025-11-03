"""
Financial Impact Analyzer
Calculates Cost of Failure (CoF) and Return on Investment (ROI) for recommendations
"""

import numpy as np

class FinancialAnalyzer:
    """
    Quantifies financial impact of corrosion-related failures
    Provides business case for design improvements
    """
    
    # Industry-standard cost parameters (in USD)
    COST_PARAMS = {
        # Material costs per ton
        'material_costs': {
            'carbon_steel': 800,
            'stainless_steel_316': 4500,
            'duplex_stainless': 8000
        },
        
        # Coating costs per m²
        'coating_costs': {
            'none': 0,
            'epoxy': 25,
            'fbe': 35,
            'polyethylene': 30,
            '3lpe': 45,
            'sacrificial_anode': 50
        },
        
        # Downtime costs per day (varies by asset type)
        'downtime_costs': {
            'pipeline': 150000,
            'refinery_unit': 500000,
            'offshore_platform': 1000000,
            'subsea_pipeline': 800000
        },
        
        # Repair/replacement multipliers
        'repair_multiplier': 1.5,  # 50% overhead on material costs
        'emergency_multiplier': 2.5,  # Emergency repairs cost 2.5x
        'environmental_cleanup': 500000,  # Average environmental incident
        
        # Inspection costs
        'inspection_cost_per_year': 50000,
        
        # Installation/welding costs per meter
        'installation_cost_per_meter': 500
    }
    
    @staticmethod
    def estimate_asset_type(params):
        """Infer asset type from parameters"""
        if 'subsea' in params.get('environment', '').lower():
            return 'subsea_pipeline'
        elif 'offshore' in params.get('environment', '').lower():
            return 'offshore_platform'
        elif any(word in str(params).lower() for word in ['refinery', 'distillation', 'amine']):
            return 'refinery_unit'
        else:
            return 'pipeline'
    
    @staticmethod
    def calculate_material_cost(params, length_meters=1000):
        """Calculate material cost for pipeline/equipment"""
        material = params.get('material', 'carbon_steel')
        thickness = params.get('initial_thickness', 12.7) / 1000  # Convert mm to m
        diameter = params.get('diameter', 0.3)  # Assume 300mm if not specified
        
        # Calculate volume (cylinder)
        volume = np.pi * diameter * thickness * length_meters  # m³
        
        # Steel density ~7850 kg/m³
        mass_tons = volume * 7.85
        
        # Get unit cost
        unit_cost = FinancialAnalyzer.COST_PARAMS['material_costs'].get(material, 800)
        
        return mass_tons * unit_cost
    
    @staticmethod
    def calculate_coating_cost(params, surface_area=1000):
        """Calculate coating cost"""
        coating = params.get('coating', 'none')
        unit_cost = FinancialAnalyzer.COST_PARAMS['coating_costs'].get(coating, 0)
        
        return surface_area * unit_cost
    
    @staticmethod
    def calculate_downtime_cost(params, downtime_days):
        """Calculate production loss due to downtime"""
        asset_type = FinancialAnalyzer.estimate_asset_type(params)
        daily_cost = FinancialAnalyzer.COST_PARAMS['downtime_costs'][asset_type]
        
        return daily_cost * downtime_days
    
    @staticmethod
    def calculate_cost_of_failure(params, results, length_meters=1000, surface_area=1000):
        """
        Calculate total Cost of Failure (CoF)
        
        Returns:
            dict with breakdown of costs
        """
        risk_level = 'low'
        if results['time_to_failure'] < params['design_life']:
            risk_level = 'critical'
        elif results['time_to_failure'] < params['design_life'] * 1.2:
            risk_level = 'high'
        elif results['time_to_failure'] < params['design_life'] * 1.5:
            risk_level = 'moderate'
        
        # Base costs
        material_cost = FinancialAnalyzer.calculate_material_cost(params, length_meters)
        coating_cost = FinancialAnalyzer.calculate_coating_cost(params, surface_area)
        installation_cost = length_meters * FinancialAnalyzer.COST_PARAMS['installation_cost_per_meter']
        
        # Repair costs (includes labor, mobilization, etc.)
        repair_cost = (material_cost + coating_cost + installation_cost) * \
                      FinancialAnalyzer.COST_PARAMS['repair_multiplier']
        
        # If failure occurs, it's likely emergency
        if risk_level in ['critical', 'high']:
            repair_cost *= FinancialAnalyzer.COST_PARAMS['emergency_multiplier']
        
        # Downtime estimation based on risk
        downtime_days_map = {
            'critical': 30,  # Major failure, complete shutdown
            'high': 14,      # Significant repair
            'moderate': 7,   # Planned maintenance
            'low': 3         # Minor intervention
        }
        downtime_days = downtime_days_map[risk_level]
        downtime_cost = FinancialAnalyzer.calculate_downtime_cost(params, downtime_days)
        
        # Environmental/safety costs (for severe failures)
        environmental_cost = 0
        if risk_level in ['critical', 'high']:
            environmental_cost = FinancialAnalyzer.COST_PARAMS['environmental_cleanup']
            if 'sour' in params.get('environment', ''):
                environmental_cost *= 2  # H2S release is more serious
        
        # Regulatory fines and reputation damage (estimated)
        regulatory_cost = 0
        if risk_level == 'critical':
            regulatory_cost = 1000000  # Average regulatory fine
        
        # Additional inspection costs due to premature failure
        years_early = max(0, params['design_life'] - results['time_to_failure'])
        additional_inspections = years_early / 2  # Inspections every 2 years
        inspection_cost = additional_inspections * FinancialAnalyzer.COST_PARAMS['inspection_cost_per_year']
        
        # Total CoF
        total_cof = (
            repair_cost + 
            downtime_cost + 
            environmental_cost + 
            regulatory_cost + 
            inspection_cost
        )
        
        return {
            'total_cof': total_cof,
            'repair_cost': repair_cost,
            'downtime_cost': downtime_cost,
            'environmental_cost': environmental_cost,
            'regulatory_cost': regulatory_cost,
            'inspection_cost': inspection_cost,
            'downtime_days': downtime_days,
            'risk_level': risk_level
        }
    
    @staticmethod
    def calculate_roi_for_upgrade(current_params, upgraded_params, current_results, 
                                   upgraded_results, length_meters=1000, surface_area=1000):
        """
        Calculate ROI for upgrading material or coating
        
        Returns:
            dict with ROI analysis
        """
        # Current design CoF
        current_cof = FinancialAnalyzer.calculate_cost_of_failure(
            current_params, current_results, length_meters, surface_area
        )
        
        # Upgraded design CoF
        upgraded_cof = FinancialAnalyzer.calculate_cost_of_failure(
            upgraded_params, upgraded_results, length_meters, surface_area
        )
        
        # Cost of upgrade (difference in initial capital)
        current_material_cost = FinancialAnalyzer.calculate_material_cost(current_params, length_meters)
        upgraded_material_cost = FinancialAnalyzer.calculate_material_cost(upgraded_params, length_meters)
        
        current_coating_cost = FinancialAnalyzer.calculate_coating_cost(current_params, surface_area)
        upgraded_coating_cost = FinancialAnalyzer.calculate_coating_cost(upgraded_params, surface_area)
        
        upgrade_capex = (upgraded_material_cost - current_material_cost) + \
                       (upgraded_coating_cost - current_coating_cost)
        
        # Savings from avoiding failure
        avoided_cost = current_cof['total_cof'] - upgraded_cof['total_cof']
        
        # ROI calculation
        if upgrade_capex > 0:
            roi_ratio = avoided_cost / upgrade_capex
            roi_percentage = (avoided_cost - upgrade_capex) / upgrade_capex * 100
            payback_period = upgrade_capex / (avoided_cost / current_params['design_life'])
        else:
            roi_ratio = float('inf')
            roi_percentage = float('inf')
            payback_period = 0
        
        # Net Present Value (simple, no discounting for hackathon)
        npv = avoided_cost - upgrade_capex
        
        return {
            'upgrade_capex': upgrade_capex,
            'current_cof': current_cof['total_cof'],
            'upgraded_cof': upgraded_cof['total_cof'],
            'avoided_cost': avoided_cost,
            'roi_ratio': roi_ratio,
            'roi_percentage': roi_percentage,
            'payback_period': payback_period,
            'npv': npv,
            'recommendation': 'HIGHLY RECOMMENDED' if roi_ratio > 3 else 
                            'RECOMMENDED' if roi_ratio > 1.5 else 
                            'CONSIDER' if roi_ratio > 1 else 'NOT RECOMMENDED'
        }
    
    @staticmethod
    def generate_financial_summary(params, results, length_meters=1000, surface_area=1000):
        """
        Generate complete financial impact summary
        """
        cof = FinancialAnalyzer.calculate_cost_of_failure(params, results, length_meters, surface_area)
        
        # Calculate probability of failure over design life
        if results['time_to_failure'] < params['design_life']:
            probability_of_failure = 1.0  # Will fail
        else:
            # Simple probability model based on safety margin
            safety_factor = results['time_to_failure'] / params['design_life']
            probability_of_failure = max(0, 1 - (safety_factor - 1) / 2)
        
        # Expected Monetary Value (EMV)
        emv = cof['total_cof'] * probability_of_failure
        
        return {
            'cof': cof,
            'probability_of_failure': probability_of_failure,
            'expected_monetary_value': emv,
            'severity': 'EXTREME' if emv > 5000000 else
                       'HIGH' if emv > 2000000 else
                       'MODERATE' if emv > 500000 else 'LOW'
        }
