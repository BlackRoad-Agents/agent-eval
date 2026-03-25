<!-- BlackRoad SEO Enhanced -->

# agent eval

> Part of **[BlackRoad OS](https://blackroad.io)** — Sovereign Computing for Everyone

[![BlackRoad OS](https://img.shields.io/badge/BlackRoad-OS-ff1d6c?style=for-the-badge)](https://blackroad.io)
[![BlackRoad Agents](https://img.shields.io/badge/Org-BlackRoad-Agents-2979ff?style=for-the-badge)](https://github.com/BlackRoad-Agents)
[![License](https://img.shields.io/badge/License-Proprietary-f5a623?style=for-the-badge)](LICENSE)

**agent eval** is part of the **BlackRoad OS** ecosystem — a sovereign, distributed operating system built on edge computing, local AI, and mesh networking by **BlackRoad OS, Inc.**

## About BlackRoad OS

BlackRoad OS is a sovereign computing platform that runs AI locally on your own hardware. No cloud dependencies. No API keys. No surveillance. Built by [BlackRoad OS, Inc.](https://github.com/BlackRoad-OS-Inc), a Delaware C-Corp founded in 2025.

### Key Features
- **Local AI** — Run LLMs on Raspberry Pi, Hailo-8, and commodity hardware
- **Mesh Networking** — WireGuard VPN, NATS pub/sub, peer-to-peer communication
- **Edge Computing** — 52 TOPS of AI acceleration across a Pi fleet
- **Self-Hosted Everything** — Git, DNS, storage, CI/CD, chat — all sovereign
- **Zero Cloud Dependencies** — Your data stays on your hardware

### The BlackRoad Ecosystem
| Organization | Focus |
|---|---|
| [BlackRoad OS](https://github.com/BlackRoad-OS) | Core platform and applications |
| [BlackRoad OS, Inc.](https://github.com/BlackRoad-OS-Inc) | Corporate and enterprise |
| [BlackRoad AI](https://github.com/BlackRoad-AI) | Artificial intelligence and ML |
| [BlackRoad Hardware](https://github.com/BlackRoad-Hardware) | Edge hardware and IoT |
| [BlackRoad Security](https://github.com/BlackRoad-Security) | Cybersecurity and auditing |
| [BlackRoad Quantum](https://github.com/BlackRoad-Quantum) | Quantum computing research |
| [BlackRoad Agents](https://github.com/BlackRoad-Agents) | Autonomous AI agents |
| [BlackRoad Network](https://github.com/BlackRoad-Network) | Mesh and distributed networking |
| [BlackRoad Education](https://github.com/BlackRoad-Education) | Learning and tutoring platforms |
| [BlackRoad Labs](https://github.com/BlackRoad-Labs) | Research and experiments |
| [BlackRoad Cloud](https://github.com/BlackRoad-Cloud) | Self-hosted cloud infrastructure |
| [BlackRoad Forge](https://github.com/BlackRoad-Forge) | Developer tools and utilities |

### Links
- **Website**: [blackroad.io](https://blackroad.io)
- **Documentation**: [docs.blackroad.io](https://docs.blackroad.io)
- **Chat**: [chat.blackroad.io](https://chat.blackroad.io)
- **Search**: [search.blackroad.io](https://search.blackroad.io)

---


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
