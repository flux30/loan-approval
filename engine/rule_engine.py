"""
Main Rule Engine - Orchestrates forward and backward chaining
"""

from engine.rule_base import RuleBase
from engine.forward_chaining import ForwardChaining
from engine.backward_chaining import BackwardChaining
from engine.conflict_resolver import ConflictResolver
from config import Config

class RuleEngine:
    """
    Main inference engine that orchestrates both forward and backward chaining
    """
    
    def __init__(self, chaining_type='both'):
        """
        Initialize the rule engine
        
        Args:
            chaining_type (str): 'forward', 'backward', or 'both'
        """
        self.chaining_type = chaining_type
        self.rule_base = RuleBase()
        self.conflict_resolver = ConflictResolver()
        
        self.forward_chain = ForwardChaining(self.rule_base, self.conflict_resolver)
        self.backward_chain = BackwardChaining(self.rule_base, self.conflict_resolver)
    
    def evaluate_applicant(self, applicant):
        """
        Evaluate an applicant using selected chaining method(s)
        
        Args:
            applicant (Applicant): The applicant to evaluate
            
        Returns:
            dict: Result containing decision and trace information
        """
        results = {
            'applicant_id': applicant.applicant_id,
            'applicant_data': applicant.to_dict(),
            'forward_chaining': None,
            'backward_chaining': None,
            'final_decision': None,
            'reasoning': None
        }
        
        if self.chaining_type in ['forward', 'both']:
            fc_decision, fc_trace = self.forward_chain.infer(applicant)
            results['forward_chaining'] = {
                'decision': fc_decision,
                'trace': fc_trace
            }
        
        if self.chaining_type in ['backward', 'both']:
            bc_decision, bc_trace = self.backward_chain.infer(applicant)
            results['backward_chaining'] = {
                'decision': bc_decision,
                'trace': bc_trace
            }
        
        # Determine final decision
        if self.chaining_type == 'forward':
            results['final_decision'] = results['forward_chaining']['decision']
        elif self.chaining_type == 'backward':
            results['final_decision'] = results['backward_chaining']['decision']
        else:  # both
            # If both methods agree, use that decision
            fc_decision = results['forward_chaining']['decision']
            bc_decision = results['backward_chaining']['decision']
            
            if fc_decision == bc_decision:
                results['final_decision'] = fc_decision
                results['reasoning'] = 'Both forward and backward chaining agree'
            else:
                # Resolve disagreement - prioritize rejection
                decision_priority = {
                    'Reject Loan': 4,
                    'Manual Review': 3,
                    'Approve with Conditions': 2,
                    'Approve Loan': 1
                }
                
                if decision_priority[fc_decision] >= decision_priority[bc_decision]:
                    results['final_decision'] = fc_decision
                else:
                    results['final_decision'] = bc_decision
                
                results['reasoning'] = f'Forward chaining: {fc_decision}, Backward chaining: {bc_decision}'
        
        applicant.set_decision(results['final_decision'])
        
        return results
    
    def evaluate_batch(self, applicants):
        """
        Evaluate multiple applicants
        
        Args:
            applicants (list): List of Applicant objects
            
        Returns:
            list: List of evaluation results
        """
        results = []
        for applicant in applicants:
            result = self.evaluate_applicant(applicant)
            results.append(result)
        
        return results
    
    def get_rules(self):
        """Get all rules in the knowledge base"""
        return [rule.to_dict() for rule in self.rule_base.get_all_rules()]
    
    def get_rule_by_id(self, rule_id):
        """Get a specific rule"""
        rule = self.rule_base.get_rule_by_id(rule_id)
        return rule.to_dict() if rule else None
    
    def add_rule(self, rule):
        """Add a new rule to the knowledge base"""
        self.rule_base.add_rule(rule)
    
    def remove_rule(self, rule_id):
        """Remove a rule from the knowledge base"""
        self.rule_base.remove_rule(rule_id)
    
    def change_conflict_strategy(self, strategy):
        """Change the conflict resolution strategy"""
        self.conflict_resolver.strategy = strategy
    
    def get_statistics(self):
        """Get statistics about the rule base and inference"""
        rules = self.rule_base.get_all_rules()
        return {
            'total_rules': len(rules),
            'high_priority_rules': len([r for r in rules if r.priority == 'High']),
            'medium_priority_rules': len([r for r in rules if r.priority == 'Medium']),
            'low_priority_rules': len([r for r in rules if r.priority == 'Low']),
            'average_specificity': sum(r.specificity for r in rules) / len(rules) if rules else 0
        }
