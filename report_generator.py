class ReportGenerator:
    """
    Generate audit reports with risk assessment and recommendations
    """
    
    @staticmethod
    def assess_risk(params, results):
        """Determine risk level and generate message"""
        design_life = params['design_life']
        time_to_failure = results['time_to_failure']
        
        if time_to_failure < design_life:
            return {
                'level': 'critical',
                'message': 'CRITICAL: Material will fail before design life. Immediate design revision required.'
            }
        elif time_to_failure < design_life * 1.2:
            return {
                'level': 'high',
                'message': 'HIGH RISK: Minimal safety margin. Enhanced corrosion control measures strongly recommended.'
            }
        elif time_to_failure < design_life * 1.5:
            return {
                'level': 'moderate',
                'message': 'MODERATE RISK: Consider enhanced corrosion control for improved reliability.'
            }
        else:
            return {
                'level': 'low',
                'message': 'Design is adequate for specified service life with acceptable safety margin.'
            }
    
    @staticmethod
    def generate_recommendations(params, results, risk_level):
        """Generate engineering recommendations based on analysis"""
        recommendations = []
        time_to_failure = results['time_to_failure']
        
        # Critical recommendations
        if risk_level in ['critical', 'high']:
            # Material upgrade
            if params['material'] == 'carbon_steel':
                recommendations.append({
                    'priority': 'URGENT',
                    'category': 'Material Selection',
                    'recommendation': 'Upgrade to Duplex Stainless Steel or Corrosion Resistant Alloy (CRA)',
                    'impact': 'Can extend service life by 300-500%'
                })
            
            # Coating improvement
            if params['coating'] == 'none':
                recommendations.append({
                    'priority': 'URGENT',
                    'category': 'Corrosion Protection',
                    'recommendation': 'Implement 3-layer polyethylene (3LPE) coating system',
                    'impact': 'Reduces corrosion rate by 90-95%'
                })
            
            # Wall thickness increase
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Design Modification',
                'recommendation': f'Increase wall thickness from {params["initial_thickness"]}mm to {params["initial_thickness"] * 1.4:.1f}mm',
                'impact': f'Extends predicted life to {time_to_failure * 1.4:.1f} years'
            })
        
        # Environment-specific recommendations
        if 'sour' in params['environment']:
            priority = 'URGENT' if risk_level == 'critical' else 'MEDIUM'
            recommendations.append({
                'priority': priority,
                'category': 'Chemical Treatment',
                'recommendation': 'Implement continuous corrosion inhibitor injection system (minimum 100 ppm)',
                'impact': 'Reduces H2S-induced corrosion by 60-80%'
            })
        
        # Monitoring recommendations
        inspection_freq = '2' if risk_level == 'critical' else '3' if risk_level == 'high' else '5'
        recommendations.append({
            'priority': 'MEDIUM' if risk_level in ['critical', 'high'] else 'LOW',
            'category': 'Inspection & Monitoring',
            'recommendation': f'Implement ultrasonic thickness monitoring every {inspection_freq} years',
            'impact': 'Early detection of unexpected corrosion trends'
        })
        
        # Temperature recommendations
        if params['temperature'] > 60:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Operating Conditions',
                'recommendation': 'Consider temperature reduction through process optimization or thermal insulation',
                'impact': 'Each 10°C reduction decreases corrosion rate by approximately 15%'
            })
        
        # Cathodic protection
        if params['coating'] != 'sacrificial_anode' and params['environment'] in ['subsea', 'sour_high']:
            recommendations.append({
                'priority': 'HIGH' if risk_level in ['critical', 'high'] else 'MEDIUM',
                'category': 'Cathodic Protection',
                'recommendation': 'Install impressed current or sacrificial anode cathodic protection system',
                'impact': 'Provides secondary protection layer, extends life by 50-100%'
            })
        
        # Design life extension
        if risk_level == 'moderate':
            recommendations.append({
                'priority': 'LOW',
                'category': 'Design Optimization',
                'recommendation': 'Consider reducing design life requirement or increasing corrosion allowance',
                'impact': 'Balances safety margin with economic considerations'
            })
        
        return recommendations
    
    @staticmethod
    def generate_report(params, results):
        """Generate complete audit report"""
        risk = ReportGenerator.assess_risk(params, results)
        recommendations = ReportGenerator.generate_recommendations(params, results, risk['level'])
        
        return {
            'risk_level': risk['level'],
            'risk_message': risk['message'],
            'recommendations': recommendations
        }
    
    @staticmethod
    def generate_text_report(params, results, report):
        """Generate downloadable text report"""
        lines = []
        lines.append("="*80)
        lines.append("CORROSION CONTROL DOCUMENT - SIMULATION AUDIT REPORT")
        lines.append("="*80)
        lines.append("")
        
        # Risk Summary
        lines.append("RISK ASSESSMENT")
        lines.append("-" * 80)
        lines.append(f"Risk Level: {report['risk_level'].upper()}")
        lines.append(f"Assessment: {report['risk_message']}")
        lines.append("")
        
        # Key Metrics
        lines.append("KEY METRICS")
        lines.append("-" * 80)
        lines.append(f"Design Life Requirement:        {params['design_life']} years")
        lines.append(f"Predicted Service Life:         {results['time_to_failure']:.1f} years")
        lines.append(f"Safety Margin:                  {((results['time_to_failure']/params['design_life'] - 1) * 100):.1f}%")
        lines.append(f"Calculated Corrosion Rate:      {results['corrosion_rate']:.3f} mm/year")
        lines.append("")
        
        # Extracted Parameters
        lines.append("EXTRACTED DESIGN PARAMETERS")
        lines.append("-" * 80)
        lines.append(f"Material:                       {params['material'].replace('_', ' ').title()}")
        lines.append(f"Coating System:                 {params['coating'].replace('_', ' ').title()}")
        lines.append(f"Operating Environment:          {params['environment'].replace('_', ' ').title()}")
        lines.append(f"Operating Temperature:          {params['temperature']}°C")
        lines.append(f"H2S Partial Pressure:           {params['h2s_pressure']} bar")
        lines.append(f"Initial Wall Thickness:         {params['initial_thickness']} mm")
        lines.append(f"Minimum Wall Thickness:         {params['min_thickness']} mm")
        lines.append(f"Design Life:                    {params['design_life']} years")
        lines.append("")
        
        # Recommendations
        lines.append("ENGINEERING RECOMMENDATIONS")
        lines.append("-" * 80)
        for i, rec in enumerate(report['recommendations'], 1):
            lines.append(f"\n{i}. [{rec['priority']}] {rec['category']}")
            lines.append(f"   Recommendation: {rec['recommendation']}")
            lines.append(f"   Expected Impact: {rec['impact']}")
        
        lines.append("")
        lines.append("="*80)
        lines.append("END OF REPORT")
        lines.append("="*80)
        
        return "\n".join(lines)
