#!/usr/bin/env python3
"""
BlackRoad Agent Evaluation Framework
Tests agent responses against a test suite and scores accuracy, latency, relevance.
"""

import json
import sys
import time
import subprocess
import argparse
from datetime import datetime


DEFAULT_MODEL = "llama3.2"
OLLAMA_HOST = "http://localhost:11434"

DEFAULT_PERSONAS = {
    "road": "You are Road, the fleet commander of BlackRoad OS.",
    "coder": "You are Coder, a software engineer. Write clean, working code.",
    "scholar": "You are Scholar, a researcher. Provide accurate, well-sourced analysis.",
    "pascal": "You are Pascal, a mathematician. Be rigorous and precise.",
    "writer": "You are Writer, a content creator. Write clearly and concisely.",
    "cipher": "You are Cipher, a security specialist. Think about threats and defenses.",
    "tutor": "You are Tutor, an educator. Explain things clearly for beginners.",
    "alice": "You are Alice, a network operations specialist.",
    "cecilia": "You are Cecilia, an AI inference specialist.",
    "octavia": "You are Octavia, a DevOps engineer.",
    "lucidia": "You are Lucidia, a web hosting specialist.",
    "aria": "You are Aria, a monitoring specialist.",
}


def query_ollama(model, system_prompt, user_prompt, host=OLLAMA_HOST):
    """Query Ollama and return response text and latency."""
    payload = json.dumps({
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "stream": False
    })

    start = time.time()
    try:
        result = subprocess.run(
            ["curl", "-s", "-X", "POST", f"{host}/api/chat",
             "-H", "Content-Type: application/json",
             "-d", payload],
            capture_output=True, text=True, timeout=120
        )
        latency = round(time.time() - start, 2)

        if result.returncode != 0:
            return None, latency, f"curl failed: {result.stderr.strip()}"

        data = json.loads(result.stdout)
        content = data.get("message", {}).get("content", "")
        return content, latency, None
    except subprocess.TimeoutExpired:
        return None, 120.0, "Timeout after 120s"
    except json.JSONDecodeError:
        return None, round(time.time() - start, 2), "Invalid JSON from Ollama"
    except Exception as e:
        return None, round(time.time() - start, 2), str(e)


def score_keywords(response, expected_keywords):
    """Score how many expected keywords appear in the response. Returns 0.0-1.0."""
    if not response or not expected_keywords:
        return 0.0

    response_lower = response.lower()
    hits = sum(1 for kw in expected_keywords if kw.lower() in response_lower)
    return round(hits / len(expected_keywords), 3)


def score_relevance(response, prompt):
    """Heuristic relevance score based on response quality signals."""
    if not response:
        return 0.0

    score = 0.0

    # Non-empty response
    if len(response.strip()) > 20:
        score += 0.3

    # Reasonable length (not too short, not too long)
    word_count = len(response.split())
    if 20 <= word_count <= 500:
        score += 0.2
    elif word_count > 10:
        score += 0.1

    # Contains structured content (lists, code blocks, paragraphs)
    if any(marker in response for marker in ['\n-', '\n*', '```', '\n1.', '\n\n']):
        score += 0.2

    # Doesn't contain error indicators
    error_phrases = ['i cannot', 'i am unable', 'as an ai', 'i do not have']
    if not any(phrase in response.lower() for phrase in error_phrases):
        score += 0.15

    # Contains question-specific terms from the prompt
    prompt_tokens = set(prompt.lower().split())
    response_tokens = set(response.lower().split())
    overlap = prompt_tokens & response_tokens - {'the', 'a', 'an', 'is', 'are', 'to', 'in', 'of', 'and', 'or'}
    if len(overlap) > 2:
        score += 0.15

    return round(min(score, 1.0), 3)


def run_eval(test_cases, model=DEFAULT_MODEL, host=OLLAMA_HOST, verbose=False):
    """
    Run evaluation on a list of test cases.

    Each test case: {agent, prompt, expected_keywords}
    Returns evaluation report dict.
    """
    results = []
    total_accuracy = 0.0
    total_relevance = 0.0
    total_latency = 0.0
    passed = 0
    failed = 0

    print(f"\nRunning {len(test_cases)} test cases with model '{model}'...\n")
    print(f"{'#':>3}  {'Agent':<10} {'Accuracy':>8} {'Relevance':>9} {'Latency':>8}  Status")
    print("-" * 65)

    for i, tc in enumerate(test_cases):
        agent_id = tc.get("agent", "road")
        prompt = tc.get("prompt", "")
        expected = tc.get("expected_keywords", [])
        persona = DEFAULT_PERSONAS.get(agent_id, "You are a helpful assistant.")

        response, latency, error = query_ollama(model, persona, prompt, host)

        if error:
            accuracy = 0.0
            relevance = 0.0
            status = "ERROR"
            failed += 1
        else:
            accuracy = score_keywords(response, expected)
            relevance = score_relevance(response, prompt)
            # Pass threshold: at least 50% keyword accuracy
            if accuracy >= 0.5:
                status = "PASS"
                passed += 1
            else:
                status = "FAIL"
                failed += 1

        total_accuracy += accuracy
        total_relevance += relevance
        total_latency += latency

        result = {
            "test_id": i + 1,
            "agent": agent_id,
            "prompt": prompt,
            "expected_keywords": expected,
            "accuracy": accuracy,
            "relevance": relevance,
            "latency_seconds": latency,
            "status": status,
            "error": error
        }
        if verbose and response:
            result["response_preview"] = response[:300]

        results.append(result)
        print(f"{i+1:>3}  {agent_id:<10} {accuracy:>8.1%} {relevance:>9.1%} {latency:>7.1f}s  {status}")

    n = len(test_cases) or 1
    avg_accuracy = round(total_accuracy / n, 3)
    avg_relevance = round(total_relevance / n, 3)
    avg_latency = round(total_latency / n, 2)

    print("-" * 65)
    print(f"{'AVG':<14} {avg_accuracy:>8.1%} {avg_relevance:>9.1%} {avg_latency:>7.1f}s  {passed}/{n} passed")

    report = {
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "model": model,
        "total_tests": n,
        "passed": passed,
        "failed": failed,
        "pass_rate": round(passed / n, 3),
        "avg_accuracy": avg_accuracy,
        "avg_relevance": avg_relevance,
        "avg_latency_seconds": avg_latency,
        "results": results
    }

    return report


def main():
    parser = argparse.ArgumentParser(description="BlackRoad Agent Evaluation Framework")
    parser.add_argument("--tests", default="test_cases.json",
                        help="Path to test cases JSON file")
    parser.add_argument("--model", default=DEFAULT_MODEL,
                        help="Ollama model to use")
    parser.add_argument("--host", default=OLLAMA_HOST,
                        help="Ollama API host")
    parser.add_argument("--output", default=None,
                        help="Output file for JSON report")
    parser.add_argument("--verbose", action="store_true",
                        help="Include response previews in output")
    parser.add_argument("--agent", default=None,
                        help="Filter tests to a specific agent")

    args = parser.parse_args()

    try:
        with open(args.tests) as f:
            test_cases = json.load(f)
    except FileNotFoundError:
        print(f"Error: Test file '{args.tests}' not found.", file=sys.stderr)
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in '{args.tests}'.", file=sys.stderr)
        sys.exit(1)

    if args.agent:
        test_cases = [tc for tc in test_cases if tc.get("agent") == args.agent]
        if not test_cases:
            print(f"No test cases found for agent '{args.agent}'.", file=sys.stderr)
            sys.exit(1)

    report = run_eval(test_cases, model=args.model, host=args.host, verbose=args.verbose)

    if args.output:
        with open(args.output, "w") as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to {args.output}")
    else:
        print(f"\nPass rate: {report['pass_rate']:.0%} ({report['passed']}/{report['total_tests']})")


if __name__ == "__main__":
    main()
