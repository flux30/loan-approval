# LoanExpert AI

A rule-based expert system implementing dual-chain inference (forward and backward chaining) for automated loan approval decisions. Features 8 production rules, intelligent conflict resolution, and transparent reasoning traces.

<img width="1805" height="925" alt="image" src="https://github.com/user-attachments/assets/7a76e12b-2015-4ffd-bfe6-1d0bf4bce790" />

## Overview

Demonstrates expert system principles with:
- **Forward Chaining**: Data-driven bottom-up inference
- **Backward Chaining**: Goal-driven top-down reasoning
- **Conflict Resolution**: Priority and specificity-based rule arbitration
- **Transparency**: Complete audit trails with step-by-step reasoning traces

## Quick Start

### Prerequisites
- Python 3.8+
- pip

### Installation
`git clone https://github.com/flux30/loan-approval.git`

`cd loan-approval`

`python -m venv venv`

*Windows*: `venv\Scripts\activate`

*macOS/Linux*: `source venv/bin/activate`

`pip install -r requirements.txt`

`python app.py`


Visit `http://localhost:5000`

Or use startup scripts:
Windows: `./run.bat`

macOS/Linux: `chmod +x run.sh`
`./run.sh`


## API Endpoints

**Evaluation**
- `POST /api/evaluate` - Single applicant evaluation
- `GET /api/evaluate-all` - Batch evaluation

**Knowledge Base**
- `GET /api/rules` - All rules
- `GET /api/rule/<id>` - Specific rule
- `GET /api/statistics` - System metrics

## Testing
`python -m pytest tests/test_engine.py -v`


## Features

- Professional dark-themed UI with gradient backgrounds
- Real-time applicant evaluation dashboard
- Interactive reasoning trace visualization
- Responsive design with GSAP animations
- 8 expert production rules with metadata

## Tech Stack

**Backend**: Flask 3.0.0, Python 3.8+  
**Frontend**: HTML5, CSS3, JavaScript  
**Animations**: GSAP 3.12.2  
**Typography**: Lexend font family

## Evaluation Dataset

| ID | Income | Credit | Employment | Decision |
|----|--------|--------|------------|----------|
| A1 | $70K | 760 | Employed | Approve |
| A2 | $50K | 720 | Employed | Conditional |
| A3 | $35K | 640 | Employed | Manual Review |
| A4 | $20K | 580 | Employed | Reject |
| A5 | $55K | 680 | Unemployed | Reject |

## Performance

- Single evaluation: ~50ms
- Batch (5 applicants): ~250ms
- Per-rule: <1ms

## License

MIT License

