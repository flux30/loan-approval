"""
Configuration file for the Rule-Based Expert System
"""

class Config:
    """Application configuration"""
    
    # Flask Configuration
    SECRET_KEY = 'your-secret-key-here-change-in-production'
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
    
    # Rule Base Configuration
    CONFLICT_RESOLUTION_STRATEGY = 'priority_specificity'  # Options: priority, specificity, priority_specificity
    
    # Logging Configuration
    ENABLE_TRACE_LOGGING = True
    MAX_TRACE_DEPTH = 50
    
    # Decision Options
    DECISIONS = ['Approve Loan', 'Approve with Conditions', 'Reject Loan', 'Manual Review']
    
    # Priority Levels
    PRIORITY_LEVELS = {
        'High': 3,
        'Medium': 2,
        'Low': 1
    }
