"""
Conflict Resolver - Handles conflicts when multiple rules fire
"""

from config import Config


class ConflictResolver:
    """Resolves conflicts when multiple rules produce different conclusions"""
    
    def __init__(self, strategy=None):
        """
        Initialize the conflict resolver
        
        Args:
            strategy (str): Resolution strategy - 'priority', 'specificity', or 'priority_specificity'
        """
        self.strategy = strategy or Config.CONFLICT_RESOLUTION_STRATEGY
        self.priority_levels = Config.PRIORITY_LEVELS
    
    def resolve(self, fired_rules, trace_logger=None):
        """
        Resolve conflict among fired rules
        
        Args:
            fired_rules (list): List of Rule objects that fired
            trace_logger (TraceLogger): Optional logger for tracing
            
        Returns:
            Rule: The winning rule based on resolution strategy
        """
        if not fired_rules:
            return None
        
        if len(fired_rules) == 1:
            return fired_rules[0]
        
        # Log conflict
        if trace_logger:
            trace_logger.log('CONFLICT', f'Multiple rules fired: {", ".join([r.rule_id for r in fired_rules])}')
        
        # Apply resolution strategy
        if self.strategy == 'priority':
            winner = self._resolve_by_priority(fired_rules)
        elif self.strategy == 'specificity':
            winner = self._resolve_by_specificity(fired_rules)
        elif self.strategy == 'priority_specificity':
            winner = self._resolve_by_priority_specificity(fired_rules)
        else:
            winner = fired_rules[0]
        
        # Log winner
        if trace_logger:
            trace_logger.log_conflict(fired_rules, winner)
        
        return winner
    
    def _resolve_by_priority(self, rules):
        """Resolve conflict using priority level"""
        try:
            return max(rules, key=lambda r: (
                self.priority_levels.get(r.priority, 0),
                r.specificity,
                r.rule_id
            ))
        except (TypeError, AttributeError):
            return rules[0]
    
    def _resolve_by_specificity(self, rules):
        """Resolve conflict using specificity (more specific rules win)"""
        try:
            return max(rules, key=lambda r: (
                r.specificity,
                self.priority_levels.get(r.priority, 0),
                r.rule_id
            ))
        except (TypeError, AttributeError):
            return rules[0]
    
    def _resolve_by_priority_specificity(self, rules):
        """Resolve conflict using combined priority and specificity"""
        try:
            return max(rules, key=lambda r: (
                self.priority_levels.get(r.priority, 0),
                r.specificity,
                r.rule_id
            ))
        except (TypeError, AttributeError):
            return rules[0]
    
    def resolve_by_decision(self, rules_by_decision, trace_logger=None):
        """
        Resolve when rules lead to different decisions
        
        Args:
            rules_by_decision (dict): Dictionary mapping decisions to lists of rules
            trace_logger (TraceLogger): Optional logger
            
        Returns:
            str: The final decision
        """
        # Prioritize decisions
        decision_priority = {
            'Reject Loan': 4,
            'Manual Review': 3,
            'Approve with Conditions': 2,
            'Approve Loan': 1
        }
        
        # Find the decision with highest priority rules
        best_decision = None
        best_score = -1
        
        for decision, rules in rules_by_decision.items():
            if not rules:
                continue
            
            try:
                # Get the best rule for this decision
                best_rule = self.resolve(rules, trace_logger)
                decision_score = (
                    decision_priority.get(decision, 0),
                    self.priority_levels.get(best_rule.priority, 0),
                    best_rule.specificity
                )
                
                if decision_score > best_score:
                    best_score = decision_score
                    best_decision = decision
            except (TypeError, AttributeError):
                continue
        
        return best_decision or 'Manual Review'


class ConflictResolutionStrategy:
    """Enum-like class for conflict resolution strategies"""
    PRIORITY = 'priority'
    SPECIFICITY = 'specificity'
    PRIORITY_SPECIFICITY = 'priority_specificity'
    
    @staticmethod
    def get_all():
        """Get all available strategies"""
        return [
            ConflictResolutionStrategy.PRIORITY,
            ConflictResolutionStrategy.SPECIFICITY,
            ConflictResolutionStrategy.PRIORITY_SPECIFICITY
        ]
