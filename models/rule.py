"""
Rule Model - Represents a single rule in the expert system
"""


class Rule:
    """Represents an IF-THEN rule with priority and specificity"""
    
    def __init__(self, rule_id, antecedents, consequent, priority='Medium', specificity=1, description=''):
        """
        Initialize a rule
        
        Args:
            rule_id (str): Unique identifier for the rule (e.g., 'R1')
            antecedents (list): List of condition functions or tuples (attribute, operator, value)
            consequent (str): The decision/action to take
            priority (str): Priority level - 'High', 'Medium', or 'Low'
            specificity (int): Number indicating rule specificity (higher = more specific)
            description (str): Human-readable description of the rule
        """
        self.rule_id = rule_id
        self.antecedents = antecedents
        self.consequent = consequent
        self.priority = priority
        self.specificity = specificity
        self.description = description
        self.fired_count = 0
        
    def evaluate(self, applicant):
        """
        Evaluate if this rule's conditions match the applicant
        
        Args:
            applicant (Applicant): The applicant to evaluate
            
        Returns:
            bool: True if all antecedents are satisfied
        """
        try:
            for condition in self.antecedents:
                if callable(condition):
                    if not condition(applicant):
                        return False
                else:
                    attr, operator, value = condition
                    if not self._evaluate_condition(applicant, attr, operator, value):
                        return False
            return True
        except Exception as e:
            print(f"Error evaluating rule {self.rule_id}: {str(e)}")
            return False
    
    def _evaluate_condition(self, applicant, attr, operator, value):
        """Evaluate a single condition"""
        applicant_value = getattr(applicant, attr, None)
        
        if applicant_value is None:
            return False
        
        if operator == '>':
            return applicant_value > value
        elif operator == '>=':
            return applicant_value >= value
        elif operator == '<':
            return applicant_value < value
        elif operator == '<=':
            return applicant_value <= value
        elif operator == '==':
            return applicant_value == value
        elif operator == '!=':
            return applicant_value != value
        elif operator == 'in_range':
            return value[0] <= applicant_value <= value[1]
        else:
            return False
    
    def fire(self):
        """Mark this rule as fired"""
        self.fired_count += 1
        return self.consequent
    
    def get_priority_score(self):
        """Get numeric priority score"""
        priority_map = {'High': 3, 'Medium': 2, 'Low': 1}
        return priority_map.get(self.priority, 0)
    
    def __str__(self):
        return f"Rule {self.rule_id}: IF {self.description} THEN {self.consequent} (Priority: {self.priority}, Specificity: {self.specificity})"
    
    def __repr__(self):
        return self.__str__()
    
    def to_dict(self):
        """Convert rule to dictionary representation"""
        return {
            'rule_id': self.rule_id,
            'description': self.description,
            'consequent': self.consequent,
            'priority': self.priority,
            'specificity': self.specificity,
            'fired_count': self.fired_count
        }
