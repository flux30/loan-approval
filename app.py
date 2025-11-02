"""
Flask Application - Rule-Based Expert System for Loan Approval
"""

import json
import os
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from config import Config
from engine.rule_engine import RuleEngine
from models.applicant import Applicant

# Initialize Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config.from_object(Config)
CORS(app)

# Initialize rule engine
rule_engine = RuleEngine(chaining_type='both')

# Load applicants data
def load_applicants_data():
    """Load applicants from JSON file"""
    try:
        json_path = os.path.join(os.path.dirname(__file__), 'data', 'applicants.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
            return data.get('applicants', [])
    except Exception as e:
        print(f"Error loading applicants: {str(e)}")
        return []

# ==================== ROUTES ====================

@app.route('/')
def index():
    """Render home page"""
    return render_template('index.html')

@app.route('/analysis')
def analysis():
    """Render analysis page"""
    return render_template('analysis.html')

@app.route('/documentation')
def documentation():
    """Render documentation page"""
    return render_template('documentation.html')

# ==================== API ENDPOINTS ====================

@app.route('/api/evaluate', methods=['POST'])
def evaluate_applicant():
    """
    Evaluate a single applicant
    """
    try:
        data = request.json
        
        # Create applicant object
        applicant = Applicant(
            applicant_id=data.get('applicant_id', 'CUSTOM'),
            income=int(data.get('income', 0)),
            credit_score=int(data.get('credit_score', 0)),
            employment_status=data.get('employment_status', 'Unemployed'),
            employment_duration=float(data.get('employment_duration', 0)),
            age=int(data.get('age', 0)),
            dependents=int(data.get('dependents', 0)),
            existing_debt=data.get('existing_debt', 'None')
        )
        
        # Evaluate using rule engine
        result = rule_engine.evaluate_applicant(applicant)
        
        return jsonify({
            'success': True,
            'data': result
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/evaluate-all', methods=['GET'])
def evaluate_all():
    """Evaluate all applicants in the dataset"""
    try:
        applicants_data = load_applicants_data()
        applicants = [Applicant.from_dict(data) for data in applicants_data]
        
        results = rule_engine.evaluate_batch(applicants)
        
        # Generate statistics
        decisions = {}
        for result in results:
            decision = result['final_decision']
            decisions[decision] = decisions.get(decision, 0) + 1
        
        return jsonify({
            'success': True,
            'data': results,
            'statistics': {
                'total_applicants': len(results),
                'decisions': decisions
            }
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/applicants', methods=['GET'])
def get_applicants():
    """Get all applicants from dataset"""
    try:
        applicants_data = load_applicants_data()
        return jsonify({
            'success': True,
            'data': applicants_data
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/rules', methods=['GET'])
def get_rules():
    """Get all rules in the knowledge base"""
    try:
        rules = rule_engine.get_rules()
        return jsonify({
            'success': True,
            'data': rules,
            'total': len(rules)
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/rule/<rule_id>', methods=['GET'])
def get_rule(rule_id):
    """Get a specific rule by ID"""
    try:
        rule = rule_engine.get_rule_by_id(rule_id)
        if rule:
            return jsonify({
                'success': True,
                'data': rule
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Rule {rule_id} not found'
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/statistics', methods=['GET'])
def get_statistics():
    """Get statistics about the rule engine"""
    try:
        stats = rule_engine.get_statistics()
        return jsonify({
            'success': True,
            'data': stats
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/change-strategy', methods=['POST'])
def change_strategy():
    """Change conflict resolution strategy"""
    try:
        data = request.json
        strategy = data.get('strategy', 'priority_specificity')
        
        rule_engine.change_conflict_strategy(strategy)
        
        return jsonify({
            'success': True,
            'message': f'Strategy changed to {strategy}'
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'success': True,
        'status': 'running',
        'version': '1.0.0'
    }), 200

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

# ==================== MAIN ====================

if __name__ == '__main__':
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )
