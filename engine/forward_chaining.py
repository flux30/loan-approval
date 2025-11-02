"""
Forward Chaining - Bottom-up inference from facts to conclusions
"""

from utils.trace_logger import TraceLogger

class ForwardChaining:
    """
    Forward chaining inference engine
    Starts with known facts and applies rules to derive new facts
    """
    
    def __init__(self, rule_base, conflict_resolver):
        """
        Initialize forward chaining engine
        
        Args:
            rule_base (RuleBase): The knowledge base
            conflict_resolver (ConflictResolver): Conflict resolver
        """
        self.rule_base = rule_base
        self.conflict_resolver = conflict_resolver
        self.trace_logger = TraceLogger()
    
    def infer(self, applicant):
        """
        Perform forward chaining inference
        
        Args:
            applicant (Applicant): The applicant to evaluate
            
        Returns:
            tuple: (decision, trace)
        """
        self.trace_logger.start('Forward Chaining', applicant.applicant_id)
        
        # Initialize fact base with applicant data
        facts = self._initialize_facts(applicant)
        self.trace_logger.log('SYSTEM', f'Initial facts: {facts}')
        
        # Keep track of fired rules and their decisions
        rules_fired = []
        decisions = {}
        
        # Iterate until no new rules fire
        iteration = 0
        max_iterations = len(self.rule_base.get_all_rules()) * 2
        
        while iteration < max_iterations:
            iteration += 1
            rules_fired_this_iteration = []
            
            # Evaluate each rule
            for rule in self.rule_base.get_all_rules():
                # Check if rule hasn't already fired
                if rule.rule_id in [r.rule_id for r in rules_fired]:
                    continue
                
                # Evaluate rule
                if rule.evaluate(applicant):
                    self.trace_logger.log_rule_evaluation(rule.rule_id, True, rule.description)
                    rules_fired_this_iteration.append(rule)
                    
                    # Store decision
                    if rule.consequent not in decisions:
                        decisions[rule.consequent] = []
                    decisions[rule.consequent].append(rule)
                    
                    self.trace_logger.log_rule_fired(rule.rule_id, rule.consequent)
                else:
                    self.trace_logger.log_rule_evaluation(rule.rule_id, False, rule.description)
            
            rules_fired.extend(rules_fired_this_iteration)
            
            # If no new rules fired, stop
            if not rules_fired_this_iteration:
                break
        
        # Resolve conflicts if multiple decisions
        if len(decisions) > 1:
            final_decision = self.conflict_resolver.resolve_by_decision(decisions, self.trace_logger)
        elif len(decisions) == 1:
            final_decision = list(decisions.keys())[0]
        else:
            final_decision = 'Manual Review'  # Default if no rules fire
        
        self.trace_logger.log_decision(final_decision)
        trace = self.trace_logger.get_summary()
        
        applicant.set_decision(final_decision, trace['trace'])
        
        return final_decision, trace
    
    def _initialize_facts(self, applicant):
        """Initialize fact base from applicant data"""
        return {
            'income': applicant.income,
            'credit_score': applicant.credit_score,
            'employment_status': applicant.employment_status,
            'employment_duration': applicant.employment_duration,
            'age': applicant.age,
            'dependents': applicant.dependents,
            'existing_debt': applicant.existing_debt
        }
    
    def get_trace(self):
        """Get the inference trace"""
        return self.trace_logger.get_trace()
    
    def get_summary(self):
        """Get trace summary"""
        return self.trace_logger.get_summary()
