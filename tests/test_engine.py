"""
Unit Tests for Rule-Based Expert System
"""

import unittest
from engine.rule_engine import RuleEngine
from models.applicant import Applicant
from engine.rule_base import RuleBase
from engine.conflict_resolver import ConflictResolver

class TestRuleEngine(unittest.TestCase):
    """Test cases for the rule engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = RuleEngine(chaining_type='both')
        self.rule_base = RuleBase()
    
    def test_engine_initialization(self):
        """Test rule engine initialization"""
        self.assertIsNotNone(self.engine.rule_base)
        self.assertIsNotNone(self.engine.forward_chain)
        self.assertIsNotNone(self.engine.backward_chain)
    
    def test_applicant_creation(self):
        """Test applicant object creation"""
        applicant = Applicant(
            applicant_id='TEST1',
            income=70000,
            credit_score=760,
            employment_status='Employed',
            employment_duration=5,
            age=30,
            dependents=2,
            existing_debt='Low'
        )
        
        self.assertEqual(applicant.applicant_id, 'TEST1')
        self.assertEqual(applicant.income, 70000)
        self.assertEqual(applicant.credit_score, 760)
    
    def test_applicant_a1_approval(self):
        """Test A1 - Should be approved"""
        applicant = Applicant(
            applicant_id='A1',
            income=70000,
            credit_score=760,
            employment_status='Employed',
            employment_duration=5,
            age=30,
            dependents=2,
            existing_debt='Low'
        )
        
        result = self.engine.evaluate_applicant(applicant)
        self.assertEqual(result['final_decision'], 'Approve Loan')
    
    def test_applicant_a2_conditional_approval(self):
        """Test A2 - Should be conditionally approved"""
        applicant = Applicant(
            applicant_id='A2',
            income=50000,
            credit_score=720,
            employment_status='Employed',
            employment_duration=2,
            age=25,
            dependents=1,
            existing_debt='None'
        )
        
        result = self.engine.evaluate_applicant(applicant)
        self.assertEqual(result['final_decision'], 'Approve with Conditions')
    
    def test_applicant_a3_manual_review(self):
        """Test A3 - Should go to manual review"""
        applicant = Applicant(
            applicant_id='A3',
            income=35000,
            credit_score=640,
            employment_status='Employed',
            employment_duration=0.5,
            age=23,
            dependents=4,
            existing_debt='Medium'
        )
        
        result = self.engine.evaluate_applicant(applicant)
        self.assertIn(result['final_decision'], ['Manual Review', 'Reject Loan'])
    
    def test_applicant_a4_rejection(self):
        """Test A4 - Should be rejected"""
        applicant = Applicant(
            applicant_id='A4',
            income=20000,
            credit_score=580,
            employment_status='Employed',
            employment_duration=3,
            age=22,
            dependents=2,
            existing_debt='High'
        )
        
        result = self.engine.evaluate_applicant(applicant)
        self.assertEqual(result['final_decision'], 'Reject Loan')
    
    def test_applicant_a5_unemployment_rejection(self):
        """Test A5 - Should be rejected due to unemployment"""
        applicant = Applicant(
            applicant_id='A5',
            income=55000,
            credit_score=680,
            employment_status='Unemployed',
            employment_duration=0,
            age=28,
            dependents=2,
            existing_debt='Low'
        )
        
        result = self.engine.evaluate_applicant(applicant)
        self.assertEqual(result['final_decision'], 'Reject Loan')
    
    def test_age_under_21_rejection(self):
        """Test age restriction - should reject under 21"""
        applicant = Applicant(
            applicant_id='TEST_AGE',
            income=100000,
            credit_score=800,
            employment_status='Employed',
            employment_duration=5,
            age=20,
            dependents=0,
            existing_debt='None'
        )
        
        result = self.engine.evaluate_applicant(applicant)
        self.assertEqual(result['final_decision'], 'Reject Loan')
    
    def test_batch_evaluation(self):
        """Test batch evaluation of multiple applicants"""
        applicants = [
            Applicant('B1', 70000, 760, 'Employed', 5, 30, 2, 'Low'),
            Applicant('B2', 50000, 720, 'Employed', 2, 25, 1, 'None'),
            Applicant('B3', 20000, 580, 'Employed', 3, 22, 2, 'High'),
        ]
        
        results = self.engine.evaluate_batch(applicants)
        self.assertEqual(len(results), 3)
    
    def test_rule_base_loading(self):
        """Test rule base initialization"""
        rules = self.rule_base.get_all_rules()
        self.assertEqual(len(rules), 8)  # Should have 8 rules
    
    def test_get_rule_by_id(self):
        """Test retrieving specific rule"""
        rule = self.rule_base.get_rule_by_id('R1')
        self.assertIsNotNone(rule)
        self.assertEqual(rule.rule_id, 'R1')
    
    def test_get_rules_by_consequent(self):
        """Test retrieving rules by consequent"""
        approve_rules = self.rule_base.get_rules_by_consequent('Approve Loan')
        self.assertGreater(len(approve_rules), 0)
    
    def test_conflict_resolution_priority(self):
        """Test conflict resolution by priority"""
        resolver = ConflictResolver(strategy='priority')
        
        rule1 = self.rule_base.get_rule_by_id('R1')  # High priority
        rule2 = self.rule_base.get_rule_by_id('R5')  # Low priority
        
        winner = resolver.resolve([rule2, rule1])
        self.assertEqual(winner.rule_id, 'R1')
    
    def test_conflict_resolution_specificity(self):
        """Test conflict resolution by specificity"""
        resolver = ConflictResolver(strategy='specificity')
        
        rule1 = self.rule_base.get_rule_by_id('R1')  # Specificity 2
        rule2 = self.rule_base.get_rule_by_id('R2')  # Specificity 3
        
        winner = resolver.resolve([rule1, rule2])
        self.assertEqual(winner.rule_id, 'R2')
    
    def test_forward_chaining_trace(self):
        """Test forward chaining trace output"""
        applicant = Applicant(
            applicant_id='TRACE_TEST',
            income=70000,
            credit_score=760,
            employment_status='Employed',
            employment_duration=5,
            age=30,
            dependents=2,
            existing_debt='Low'
        )
        
        decision, trace = self.engine.forward_chain.infer(applicant)
        
        self.assertIsNotNone(trace)
        self.assertIn('total_entries', trace)
        self.assertGreater(trace['total_entries'], 0)
    
    def test_backward_chaining_trace(self):
        """Test backward chaining trace output"""
        applicant = Applicant(
            applicant_id='TRACE_TEST',
            income=70000,
            credit_score=760,
            employment_status='Employed',
            employment_duration=5,
            age=30,
            dependents=2,
            existing_debt='Low'
        )
        
        decision, trace = self.engine.backward_chain.infer(applicant)
        
        self.assertIsNotNone(trace)
        self.assertIn('total_entries', trace)
    
    def test_applicant_to_dict(self):
        """Test applicant serialization"""
        applicant = Applicant(
            applicant_id='DICT_TEST',
            income=50000,
            credit_score=700,
            employment_status='Employed',
            employment_duration=2,
            age=28,
            dependents=1,
            existing_debt='None'
        )
        
        data = applicant.to_dict()
        self.assertEqual(data['applicant_id'], 'DICT_TEST')
        self.assertEqual(data['income'], 50000)
    
    def test_applicant_from_dict(self):
        """Test applicant deserialization"""
        data = {
            'applicant_id': 'FROM_DICT',
            'income': 60000,
            'credit_score': 720,
            'employment_status': 'Employed',
            'employment_duration': 3,
            'age': 35,
            'dependents': 2,
            'existing_debt': 'Low'
        }
        
        applicant = Applicant.from_dict(data)
        self.assertEqual(applicant.applicant_id, 'FROM_DICT')
        self.assertEqual(applicant.income, 60000)
    
    def test_engine_statistics(self):
        """Test engine statistics"""
        stats = self.engine.get_statistics()
        
        self.assertIn('total_rules', stats)
        self.assertIn('high_priority_rules', stats)
        self.assertIn('medium_priority_rules', stats)
        self.assertIn('low_priority_rules', stats)
        self.assertGreater(stats['total_rules'], 0)

class TestEdgeCases(unittest.TestCase):
    """Test edge cases and boundary conditions"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = RuleEngine(chaining_type='both')
    
    def test_zero_income(self):
        """Test applicant with zero income"""
        applicant = Applicant(
            applicant_id='EDGE1',
            income=0,
            credit_score=700,
            employment_status='Employed',
            employment_duration=1,
            age=30,
            dependents=0,
            existing_debt='None'
        )
        
        result = self.engine.evaluate_applicant(applicant)
        self.assertIsNotNone(result['final_decision'])
    
    def test_minimum_credit_score(self):
        """Test with minimum credit score"""
        applicant = Applicant(
            applicant_id='EDGE2',
            income=50000,
            credit_score=300,
            employment_status='Employed',
            employment_duration=1,
            age=30,
            dependents=0,
            existing_debt='None'
        )
        
        result = self.engine.evaluate_applicant(applicant)
        self.assertEqual(result['final_decision'], 'Reject Loan')
    
    def test_maximum_dependents(self):
        """Test with many dependents"""
        applicant = Applicant(
            applicant_id='EDGE3',
            income=30000,
            credit_score=650,
            employment_status='Employed',
            employment_duration=1,
            age=40,
            dependents=10,
            existing_debt='None'
        )
        
        result = self.engine.evaluate_applicant(applicant)
        self.assertIsNotNone(result['final_decision'])
    
    def test_new_employment(self):
        """Test with very new employment"""
        applicant = Applicant(
            applicant_id='EDGE4',
            income=50000,
            credit_score=700,
            employment_status='Employed',
            employment_duration=0.1,
            age=30,
            dependents=0,
            existing_debt='None'
        )
        
        result = self.engine.evaluate_applicant(applicant)
        self.assertIn(result['final_decision'], 
                     ['Manual Review', 'Approve with Conditions', 'Reject Loan'])

if __name__ == '__main__':
    unittest.main()
