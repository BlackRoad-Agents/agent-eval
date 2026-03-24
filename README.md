# agent-eval

Evaluation framework for BlackRoad OS agents. Tests agent responses against a suite of test cases and scores accuracy, latency, and relevance.

## What This Is

A Python evaluation harness that sends prompts to agents via Ollama, compares responses against expected keywords, and produces a scored report. Used to validate that agents respond correctly and consistently.

## Requirements

- Python 3.6+
- Ollama running locally (or specify --host)
- curl

## Usage

```bash
# Run all 20 test cases
python3 eval.py

# Use a specific model
python3 eval.py --model codellama

# Test only one agent
python3 eval.py --agent coder

# Save report to file
python3 eval.py --output eval-report.json --verbose

# Custom test file
python3 eval.py --tests my_tests.json
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--tests` | test_cases.json | Path to test cases file |
| `--model` | llama3.2 | Ollama model to evaluate |
| `--host` | http://localhost:11434 | Ollama API endpoint |
| `--output` | stdout | Output file for JSON report |
| `--verbose` | false | Include response previews |
| `--agent` | all | Filter to specific agent |

## Test Case Format

```json
[
  {
    "agent": "coder",
    "prompt": "Write a Python function that checks if a number is prime.",
    "expected_keywords": ["def", "prime", "return", "True", "False"]
  }
]
```

## Scoring

- **Accuracy**: Percentage of expected keywords found in the response (0-100%)
- **Relevance**: Heuristic score based on response length, structure, and prompt overlap (0-100%)
- **Latency**: Wall-clock time for the Ollama request in seconds
- **Pass/Fail**: A test passes if keyword accuracy >= 50%

## Included Test Cases

20 test cases across 10 agents covering code generation, research, math, writing, security, teaching, networking, DevOps, inference, and monitoring.

Part of BlackRoad-Agents. Remember the Road. Pave Tomorrow. Incorporated 2025.
