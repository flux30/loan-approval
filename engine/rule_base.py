"""
Rule Base - Contains all the rules for the loan approval system
"""

from models.rule import Rule


class RuleBase:
    """Knowledge base containing all rules for loan approval"""
    
    def __init__(self):
        """Initialize the rule base with predefined rules"""
        self.rules = self._initialize_rules()
    
    def _initialize_rules(self):
        """Define all rules according to the problem statement"""
        rules = []
        
        # R1: income > 60,000 AND credit_score > 750
        rules.append(Rule(
            rule_id='R1',
            antecedents=[
                ('income', '>', 60000),
                ('credit_score', '>', 750)
            ],
            consequent='Approve Loan',
            priority='High',
            specificity=2,
            description='High income (>60K) AND excellent credit (>750)'
        ))
        
        # R2: 40,000 ≤ income ≤ 60,000 AND credit_score > 700 AND existing_debt = None
        rules.append(Rule(
            rule_id='R2',
            antecedents=[
                ('income', 'in_range', (40000, 60000)),
                ('credit_score', '>', 700),
                ('existing_debt', '==', 'None')
            ],
            consequent='Approve with Conditions',
            priority='Medium',
            specificity=3,
            description='Moderate income (40K-60K) AND good credit (>700) AND no debt'
        ))
        
        # R3: credit_score ≤ 650 AND existing_debt = High
        rules.append(Rule(
            rule_id='R3',
            antecedents=[
                ('credit_score', '<=', 650),
                ('existing_debt', '==', 'High')
            ],
            consequent='Reject Loan',
            priority='High',
            specificity=2,
            description='Poor credit (≤650) AND high existing debt'
        ))
        
        # R4: employment_status = Unemployed
        rules.append(Rule(
            rule_id='R4',
            antecedents=[
                ('employment_status', '==', 'Unemployed')
            ],
            consequent='Reject Loan',
            priority='High',
            specificity=1,
            description='Unemployed status'
        ))
        
        # R5: 30,000 ≤ income ≤ 50,000 AND 600 ≤ credit_score ≤ 700
        rules.append(Rule(
            rule_id='R5',
            antecedents=[
                ('income', 'in_range', (30000, 50000)),
                ('credit_score', 'in_range', (600, 700))
            ],
            consequent='Manual Review',
            priority='Low',
            specificity=2,
            description='Moderate income (30K-50K) AND fair credit (600-700)'
        ))
        
        # R6: age < 21
        rules.append(Rule(
            rule_id='R6',
            antecedents=[
                ('age', '<', 21)
            ],
            consequent='Reject Loan',
            priority='High',
            specificity=1,
            description='Applicant under 21 years old'
        ))
        
        # R7: dependents > 3 AND income < 45,000
        rules.append(Rule(
            rule_id='R7',
            antecedents=[
                ('dependents', '>', 3),
                ('income', '<', 45000)
            ],
            consequent='Manual Review',
            priority='Low',
            specificity=2,
            description='Many dependents (>3) AND low income (<45K)'
        ))
        
        # R8: employment_duration < 1 year AND credit_score < 700
        rules.append(Rule(
            rule_id='R8',
            antecedents=[
                ('employment_duration', '<', 1),
                ('credit_score', '<', 700)
            ],
            consequent='Manual Review',
            priority='Low',
            specificity=2,
            description='Short employment (<1 year) AND below-good credit (<700)'
        ))
        
        return rules
    
    def get_all_rules(self):
        """Return all rules in the knowledge base"""
        return self.rules
    
    def get_rule_by_id(self, rule_id):
        """Get a specific rule by its ID"""
        for rule in self.rules:
            if rule.rule_id == rule_id:
                return rule
        return None
    
    def get_rules_by_consequent(self, consequent):
        """Get all rules that lead to a specific consequent"""
        return [rule for rule in self.rules if rule.consequent == consequent]
    
    def add_rule(self, rule):
        """Add a new rule to the knowledge base"""
        self.rules.append(rule)
    
    def remove_rule(self, rule_id):
        """Remove a rule from the knowledge base"""
        self.rules = [rule for rule in self.rules if rule.rule_id != rule_id]
    
    def reset_fired_counts(self):
        """Reset the fired count for all rules"""
        for rule in self.rules:
            rule.fired_count = 0
