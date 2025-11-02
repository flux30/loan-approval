"""
Backward Chaining - Top-down inference from goal to facts
"""

from utils.trace_logger import TraceLogger

class BackwardChaining:
    """
    Backward chaining inference engine
    Starts with a goal (desired conclusion) and works backward to verify if it can be proven
    """
    
    def __init__(self, rule_base, conflict_resolver):
        """
        Initialize backward chaining engine
        
        Args:
            rule_base (RuleBase): The knowledge base
            conflict_resolver (ConflictResolver): Conflict resolver
        """
        self.rule_base = rule_base
        self.conflict_resolver = conflict_resolver
        self.trace_logger = TraceLogger()
        self.proven_goals = set()
        self.failed_goals = set()
    
    def infer(self, applicant):
        """
        Perform backward chaining inference
        
        Args:
            applicant (Applicant): The applicant to evaluate
            
        Returns:
            tuple: (decision, trace)
        """
        self.trace_logger.start('Backward Chaining', applicant.applicant_id)
        self.proven_goals = set()
        self.failed_goals = set()
        
        # Define goals to prove (in order of preference)
        goals = ['Reject Loan', 'Approve Loan', 'Approve with Conditions', 'Manual Review']
        
        final_decision = None
        
        for goal in goals:
            self.trace_logger.log('SYSTEM', f'Attempting to prove goal: {goal}')
            
            if self._prove_goal(goal, applicant, depth=0):
                final_decision = goal
                self.trace_logger.log_decision(final_decision)
                break
        
        # If no goal proven, default to Manual Review
        if final_decision is None:
            final_decision = 'Manual Review'
            self.trace_logger.log_decision(final_decision)
        
        trace = self.trace_logger.get_summary()
        applicant.set_decision(final_decision, trace['trace'])
        
        return final_decision, trace
    
    def _prove_goal(self, goal, applicant, depth=0):
        """
        Recursively prove a goal
        
        Args:
            goal (str): The goal to prove
            applicant (Applicant): The applicant data
            depth (int): Current recursion depth
            
        Returns:
            bool: True if goal can be proven
        """
        indent = "  " * depth
        
        # Check if already proven
        if goal in self.proven_goals:
            self.trace_logger.log('SYSTEM', f'{indent}Goal already proven: {goal}')
            return True
        
        # Check if already failed
        if goal in self.failed_goals:
            self.trace_logger.log('SYSTEM', f'{indent}Goal already failed: {goal}')
            return False
        
        # Prevent deep recursion
        if depth > 10:
            self.trace_logger.log('SYSTEM', f'{indent}Max recursion depth reached')
            return False
        
        self.trace_logger.log('SYSTEM', f'{indent}Proving goal: {goal}')
        
        # Find rules that conclude with this goal
        rules_for_goal = self.rule_base.get_rules_by_consequent(goal)
        
        if not rules_for_goal:
            self.trace_logger.log('SYSTEM', f'{indent}No rules found for goal: {goal}')
            self.failed_goals.add(goal)
            return False
        
        # Try to satisfy each rule
        satisfied_rules = []
        
        for rule in rules_for_goal:
            self.trace_logger.log('SYSTEM', f'{indent}Checking rule {rule.rule_id}: {rule.description}')
            
            if rule.evaluate(applicant):
                self.trace_logger.log_rule_evaluation(rule.rule_id, True, rule.description)
                self.trace_logger.log_rule_fired(rule.rule_id, goal)
                satisfied_rules.append(rule)
            else:
                self.trace_logger.log_rule_evaluation(rule.rule_id, False, rule.description)
        
        if satisfied_rules:
            # If multiple rules satisfy the goal, resolve conflicts
            if len(satisfied_rules) > 1:
                winning_rule = self.conflict_resolver.resolve(satisfied_rules, self.trace_logger)
            else:
                winning_rule = satisfied_rules[0]
            
            self.trace_logger.log('SYSTEM', f'{indent}Goal {goal} proven by rule {winning_rule.rule_id}')
            self.proven_goals.add(goal)
            return True
        else:
            self.trace_logger.log('SYSTEM', f'{indent}Goal {goal} could not be proven')
            self.failed_goals.add(goal)
            return False
    
    def get_trace(self):
        """Get the inference trace"""
        return self.trace_logger.get_trace()
    
    def get_summary(self):
        """Get trace summary"""
        return self.trace_logger.get_summary()
