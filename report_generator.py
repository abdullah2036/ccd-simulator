class ReportGenerator:
    """
    Generate audit reports with risk assessment, recommendations, and financial analysis
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
        """Generate engineering recommendations with financial ROI"""
        recommendations = []
        time_to_failure = results['time_to_failure']
        
        # Material upgrade recommendation with ROI
        if risk_level in ['critical', 'high']:
            if params['material'] == 'carbon_steel':
                # Calculate ROI for upgrade
                try:
                    from financial_analyzer import FinancialAnalyzer
                    from copy import deepcopy
                    
                    upgraded_params = deepcopy(params)
                    upgraded_params['material'] = 'duplex_stainless'
                    
                    # Estimate upgraded performance
                    upgraded_results = deepcopy(results)
                    upgraded_results['time_to_failure'] = time_to_failure * 4  # Duplex lasts ~4x longer
                    upgraded_results['corrosion_rate'] = results['corrosion_rate'] * 0.25
                    
                    roi = FinancialAnalyzer.calculate_roi_for_upgrade(
                        params, upgraded_params, results, upgraded_results
                    )
                    
                    recommendations.append({
                        'priority': 'URGENT',
                        'category': 'Material Selection',
                        'recommendation': 'Upgrade to Duplex Stainless Steel or CRA',
                        'impact': f'Extends life by 300-500%',
                        'financial': f'ROI: {roi["roi_ratio"]:.1f}x | Payback: {roi["payback_period"]:.1f} years | NPV: ${roi["npv"]/1e6:.2f}M'
                    })
                except:
                    recommendations.append({
                        'priority': 'URGENT',
                        'category': 'Material Selection',
                        'recommendation': 'Upgrade to Duplex Stainless Steel or CRA',
                        'impact': 'Can extend service life by 300-500%',
                        'financial': 'High ROI expected (detailed analysis available)'
                    })
            
            # Coating improvement
            if params['coating'] == 'none':
                recommendations.append({
                    'priority': 'URGENT',
                    'category': 'Corrosion Protection',
                    'recommendation': 'Implement 3-layer polyethylene (3LPE) coating system',
                    'impact': 'Reduces corrosion rate by 90-95%',
                    'financial': 'Typical ROI: 8-12x over asset life'
                })
            
            # Wall thickness increase
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Design Modification',
                'recommendation': f'Increase wall thickness from {params["initial_thickness"]}mm to {params["initial_thickness"] * 1.4:.1f}mm',
                'impact': f'Extends predicted life to {time_to_failure * 1.4:.1f} years',
                'financial': 'Material cost increase: ~40% | Failure cost avoided: 100%'
            })
        
        # Environment-specific recommendations
        if 'sour' in params['environment']:
            priority = 'URGENT' if risk_level == 'critical' else 'MEDIUM'
            recommendations.append({
                'priority': priority,
                'category': 'Chemical Treatment',
                'recommendation': 'Implement continuous corrosion inhibitor injection system (minimum 100 ppm)',
                'impact': 'Reduces H2S-induced corrosion by 60-80%',
                'financial': 'Opex: ~$50K/year | Prevents failures: $2-5M+'
            })
        
        # Monitoring recommendations
        inspection_freq = '2' if risk_level == 'critical' else '3' if risk_level == 'high' else '5'
        recommendations.append({
            'priority': 'MEDIUM' if risk_level in ['critical', 'high'] else 'LOW',
            'category': 'Inspection & Monitoring',
            'recommendation': f'Implement ultrasonic thickness monitoring every {inspection_freq} years',
            'impact': 'Early detection of unexpected corrosion trends',
            'financial': f'Inspection cost: ${int(inspection_freq)*10}K/cycle | Prevents catastrophic failure'
        })
        
        # Temperature recommendations
        if params['temperature'] > 60:
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Operating Conditions',
                'recommendation': 'Consider temperature reduction through process optimization or thermal insulation',
                'impact': 'Each 10°C reduction decreases corrosion rate by approximately 15%',
                'financial': 'Energy cost tradeoff vs extended asset life'
            })
        
        # Cathodic protection
        if params['coating'] != 'sacrificial_anode' and params['environment'] in ['subsea', 'sour_high']:
            recommendations.append({
                'priority': 'HIGH' if risk_level in ['critical', 'high'] else 'MEDIUM',
                'category': 'Cathodic Protection',
                'recommendation': 'Install impressed current or sacrificial anode cathodic protection system',
                'impact': 'Provides secondary protection layer, extends life by 50-100%',
                'financial': 'Capex: $200-500K | Prevents $5-20M replacement'
            })
        
        return recommendations
    
    @staticmethod
    def generate_report(params, results):
        """Generate complete audit report with financial analysis"""
        risk = ReportGenerator.assess_risk(params, results)
        recommendations = ReportGenerator.generate_recommendations(params, results, risk['level'])
        
        # Add financial analysis
        financial_summary = None
        try:
            from financial_analyzer import FinancialAnalyzer
            financial_summary = FinancialAnalyzer.generate_financial_summary(params, results)
        except:
            pass
        
        return {
            'risk_level': risk['level'],
            'risk_message': risk['message'],
            'recommendations': recommendations,
            'financial_summary': financial_summary
        }
    
    @staticmethod
    def generate_text_report(params, results, report):
        """Generate downloadable text report with financial analysis"""
        lines = []
        lines.append("="*80)
        lines.append("CORROSION CONTROL DOCUMENT - SIMULATION AUDIT REPORT")
        lines.append("Hybrid Physics-ML Analysis with Financial Impact Assessment")
        lines.append("="*80)
        lines.append("")
        
        # Analysis method
        lines.append("ANALYSIS METHOD")
        lines.append("-" * 80)
        lines.append(f"Prediction Method: {results.get('method', 'physics').upper()}")
        if results.get('ml_confidence', 0) > 0:
            lines.append(f"ML Model Confidence: {results['ml_confidence']*100:.1f}%")
        lines.append("")
        
        # Risk Summary
        lines.append("RISK ASSESSMENT")
        lines.append("-" * 80)
        lines.append(f"Risk Level: {report['risk_level'].upper()}")
        lines.append(f"Assessment: {report['risk_message']}")
        lines.append("")
        
        # Financial Impact
        if report.get('financial_summary'):
            fin = report['financial_summary']
            lines.append("FINANCIAL IMPACT ANALYSIS")
            lines.append("-" * 80)
            lines.append(f"Cost of Failure (CoF):          ${fin['cof']['total_cof']:,.0f}")
            lines.append(f"  - Repair Costs:               ${fin['cof']['repair_cost']:,.0f}")
            lines.append(f"  - Downtime Costs:             ${fin['cof']['downtime_cost']:,.0f} ({fin['cof']['downtime_days']} days)")
            if fin['cof']['environmental_cost'] > 0:
                lines.append(f"  - Environmental/Cleanup:      ${fin['cof']['environmental_cost']:,.0f}")
            if fin['cof']['regulatory_cost'] > 0:
                lines.append(f"  - Regulatory Fines:           ${fin['cof']['regulatory_cost']:,.0f}")
            lines.append(f"Probability of Failure:         {fin['probability_of_failure']*100:.1f}%")
            lines.append(f"Expected Monetary Value:        ${fin['expected_monetary_value']:,.0f}")
            lines.append(f"Financial Severity:             {fin['severity']}")
            lines.append("")
        
        # Key Metrics
        lines.append("KEY METRICS")
        lines.append("-" * 80)
        lines.append(f"Design Life Requirement:        {params['design_life']} years")
        lines.append(f"Predicted Service Life:         {results['time_to_failure']:.1f} years")
        lines.append(f"Safety Margin:                  {((results['time_to_failure']/params['design_life'] - 1) * 100):.1f}%")
        lines.append(f"Calculated Corrosion Rate:      {results['corrosion_rate']:.3f} mm/year")
        if results.get('physics_rate'):
            lines.append(f"Physics-Only Rate:              {results['physics_rate']:.3f} mm/year")
            lines.append(f"ML-Enhanced Adjustment:         {(results['corrosion_rate']/results['physics_rate']-1)*100:+.1f}%")
        lines.append("")
        
        # Extracted Parameters
        lines.append("EXTRACTED DESIGN PARAMETERS")
        lines.append("-" * 80)
        lines.append(f"Material:                       {params['material'].replace('_', ' ').title()}")
        lines.append(f"Coating System:                 {params['coating'].replace('_', ' ').title()}")
        lines.append(f"Operating Environment:          {params['environment'].replace('_', ' ').title()}")
        lines.append(f"Operating Temperature:          {params['temperature']}°C")
        lines.append(f"H2S Partial Pressure:           {params['h2s_pressure']} bar")
        lines.append(f"Flow Velocity:                  {params.get('flow_velocity', 'N/A')} m/s")
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
            lines.append(f"   Technical Impact: {rec['impact']}")
            if 'financial' in rec:
                lines.append(f"   Financial Impact: {rec['financial']}")
        
        lines.append("")
        lines.append("="*80)
        lines.append("BUSINESS CASE SUMMARY")
        lines.append("="*80)
        if report.get('financial_summary'):
            if report['risk_level'] in ['critical', 'high']:
                lines.append(f"⚠️  URGENT ACTION REQUIRED")
                lines.append(f"Potential financial exposure: ${report['financial_summary']['expected_monetary_value']:,.0f}")
                lines.append(f"Recommended immediate investment in mitigation measures")
                lines.append(f"Typical ROI for upgrades: 5-15x over asset lifetime")
            else:
                lines.append(f"✓ Current design acceptable with monitoring")
                lines.append(f"Consider optimization opportunities for enhanced reliability")
        
        lines.append("")
        lines.append("="*80)
        lines.append("END OF REPORT")
        lines.append("="*80)
        
        return "\n".join(lines)
