"""
Trace Logger - Logs the reasoning process for transparency
"""

from datetime import datetime

class TraceLogger:
    """Logs the reasoning trace for inference processes"""
    
    def __init__(self, max_depth=50):
        """
        Initialize the trace logger
        
        Args:
            max_depth (int): Maximum number of trace entries to store
        """
        self.max_depth = max_depth
        self.trace = []
        self.start_time = None
        self.end_time = None
    
    def start(self, chaining_type, applicant_id):
        """Start a new trace"""
        self.trace = []
        self.start_time = datetime.now()
        self.log('SYSTEM', f'Starting {chaining_type} for applicant {applicant_id}')
    
    def log(self, level, message, rule_id=None):
        """
        Log a trace entry
        
        Args:
            level (str): Log level - 'SYSTEM', 'RULE_EVAL', 'RULE_FIRE', 'CONFLICT', 'DECISION'
            message (str): Log message
            rule_id (str): Optional rule ID
        """
        if len(self.trace) < self.max_depth:
            entry = {
                'timestamp': datetime.now().isoformat(),
                'level': level,
                'message': message,
                'rule_id': rule_id
            }
            self.trace.append(entry)
    
    def log_rule_evaluation(self, rule_id, matched, description):
        """Log rule evaluation"""
        status = 'MATCHED' if matched else 'NOT MATCHED'
        self.log('RULE_EVAL', f'{rule_id}: {description} - {status}', rule_id)
    
    def log_rule_fired(self, rule_id, consequent):
        """Log when a rule fires"""
        self.log('RULE_FIRE', f'{rule_id} fired → {consequent}', rule_id)
    
    def log_conflict(self, conflicting_rules, winner):
        """Log conflict resolution"""
        rule_ids = [r.rule_id for r in conflicting_rules]
        self.log('CONFLICT', f'Conflict between {", ".join(rule_ids)} → Winner: {winner.rule_id}')
    
    def log_decision(self, decision):
        """Log final decision"""
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        self.log('DECISION', f'Final Decision: {decision} (Time: {duration:.3f}s)')
    
    def get_trace(self):
        """Get the complete trace"""
        return self.trace
    
    def get_summary(self):
        """Get a summary of the trace"""
        rule_fires = [entry for entry in self.trace if entry['level'] == 'RULE_FIRE']
        conflicts = [entry for entry in self.trace if entry['level'] == 'CONFLICT']
        
        return {
            'total_entries': len(self.trace),
            'rules_fired': len(rule_fires),
            'conflicts_resolved': len(conflicts),
            'trace': self.trace
        }
    
    def clear(self):
        """Clear the trace"""
        self.trace = []
        self.start_time = None
        self.end_time = None
