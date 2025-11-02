"""
Applicant Model - Represents a loan applicant with their details
"""

class Applicant:
    """Represents a loan applicant with their financial and personal details"""
    
    def __init__(self, applicant_id, income, credit_score, employment_status, 
                 employment_duration, age, dependents, existing_debt):
        """
        Initialize an applicant
        
        Args:
            applicant_id (str): Unique identifier (e.g., 'A1')
            income (int): Annual income
            credit_score (int): Credit score (300-850)
            employment_status (str): 'Employed' or 'Unemployed'
            employment_duration (float): Years of employment
            age (int): Age in years
            dependents (int): Number of dependents
            existing_debt (str): 'None', 'Low', 'Medium', or 'High'
        """
        self.applicant_id = applicant_id
        self.income = income
        self.credit_score = credit_score
        self.employment_status = employment_status
        self.employment_duration = employment_duration
        self.age = age
        self.dependents = dependents
        self.existing_debt = existing_debt
        self.decision = None
        self.reasoning_trace = []
        
    def set_decision(self, decision, trace=None):
        """Set the final decision and reasoning trace"""
        self.decision = decision
        if trace:
            self.reasoning_trace = trace
    
    def to_dict(self):
        """Convert applicant to dictionary representation"""
        return {
            'applicant_id': self.applicant_id,
            'income': self.income,
            'credit_score': self.credit_score,
            'employment_status': self.employment_status,
            'employment_duration': self.employment_duration,
            'age': self.age,
            'dependents': self.dependents,
            'existing_debt': self.existing_debt,
            'decision': self.decision,
            'reasoning_trace': self.reasoning_trace
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create an applicant from dictionary"""
        return cls(
            applicant_id=data.get('applicant_id', ''),
            income=data.get('income', 0),
            credit_score=data.get('credit_score', 0),
            employment_status=data.get('employment_status', 'Unemployed'),
            employment_duration=data.get('employment_duration', 0),
            age=data.get('age', 0),
            dependents=data.get('dependents', 0),
            existing_debt=data.get('existing_debt', 'None')
        )
    
    def __str__(self):
        return f"Applicant {self.applicant_id}: Income={self.income}, Credit Score={self.credit_score}, Age={self.age}"
    
    def __repr__(self):
        return self.__str__()
