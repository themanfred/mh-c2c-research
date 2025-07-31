"""
MH‑C2C  —  Metropolis‑Hastings Critique‑to‑Consensus
Single‑file reference implementation ready to run with the OpenAI Python SDK.

Install‑time deps  ▸  pip install openai tiktoken tenacity python-dotenv
Make a .env file with  OPENAI_API_KEY="sk‑..."

Usage from the shell:
    python mh_c2c.py --task "Explain why the sky is blue." --m 3 --T 3 --beta 1.0

This demo uses a toy scoring function (brevity = better) so it’s safe to run
without external ground‑truth data.  Replace `score()` with your own metric
(unit‑tests passed, factuality score, etc.) for real work.
"""

from __future__ import annotations

import argparse
import math
import os
import random
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import List

from dotenv import load_dotenv
from tenacity import retry, wait_exponential, stop_after_attempt

# ──────────────────────────────────────────────────────────────────────────────
# 1. API client setup
# ──────────────────────────────────────────────────────────────────────────────

load_dotenv()
try:
    import openai  # lazily import so linting doesn’t fail w/out package
except ImportError as exc:  # pragma: no cover
    sys.stderr.write("\n[!] openai package not found.  pip install openai\n")
    raise exc

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:  # pragma: no cover
    sys.exit("[!] OPENAI_API_KEY not found in environment or .env file")

openai.api_key = OPENAI_API_KEY
MODEL_NAME: str = os.getenv("MH_C2C_MODEL", "gpt-4o-mini")
TEMPERATURE: float = float(os.getenv("MH_C2C_TEMP", "0.7"))

# ──────────────────────────────────────────────────────────────────────────────
# 2. LLM wrapper
# ──────────────────────────────────────────────────────────────────────────────

@retry(wait=wait_exponential(multiplier=1, min=1, max=20),
       stop=stop_after_attempt(6))
def call_llm(prompt: str, system_msg: str | None = None) -> str:
    """Send *prompt* to the chat model and return the raw assistant text."""
    messages = []
    if system_msg:
        messages.append({"role": "system", "content": system_msg})
    messages.append({"role": "user", "content": prompt})

    response = openai.ChatCompletion.create(
        model=MODEL_NAME,
        messages=messages,
        temperature=TEMPERATURE,
        max_tokens=1024,
    )
    return response.choices[0].message["content"].strip()

# ──────────────────────────────────────────────────────────────────────────────
# 3. Scoring function (replace with domain‑specific metric!)
# ──────────────────────────────────────────────────────────────────────────────

def score(text: str) -> float:
    """Toy metric: the shorter the answer, the higher the score."""
    return -len(text)

# ──────────────────────────────────────────────────────────────────────────────
# 4. Prompt helpers  (self‑critique • mutual‑critique • refinement)
# ──────────────────────────────────────────────────────────────────────────────

def self_critique(answer: str) -> str:
    prompt = (
        "Here is your answer:\n\n" + answer + "\n\n"
        "Task: List two specific weaknesses or potential errors and roast this answer."\
    )
    return call_llm(prompt)

def mutual_critique(answer: str, peers: List[str]) -> str:
    prompt = (
        "Candidate answer:\n\n" + answer + "\n\n"
        "Peer answers:\n" + "\n---\n".join(peers) + "\n\n"
        "Task: As an outside expert, identify two flaws in the candidate above."\
    )
    return call_llm(prompt)

def propose_refinement(answer: str, e_self: str, e_mut: str) -> str:
    prompt = (
        "Original answer:\n" + answer + "\n\n"
        "Self‑critique:\n" + e_self + "\n\n"
        "Peer critique:\n" + e_mut + "\n\n"
        "Task: Rewrite the answer, fully addressing every issue mentioned above."\
    )
    return call_llm(prompt)

# ──────────────────────────────────────────────────────────────────────────────
# 5. Data container + Metropolis gate
# ──────────────────────────────────────────────────────────────────────────────

@dataclass
class Chain:
    text: str
    score: float


def mh_accept(old_s: float, new_s: float, beta: float) -> bool:
    """Return True to accept the proposal via Metropolis–Hastings."""
    delta = new_s - old_s
    alpha = 1.0 if delta >= 0 else math.exp(beta * delta)
    return random.random() < alpha

# ──────────────────────────────────────────────────────────────────────────────
# 6. Main MH‑C2C loop
# ──────────────────────────────────────────────────────────────────────────────

def mh_c2c(task: str,
           m: int = 3,
           T: int = 3,
           beta: float = 1.0,
           eps: float = 1e-3,
           roles: List[str] | None = None,
           verbose: bool = True) -> Chain:
    """Run MH‑C2C and return the best Chain (answer + score)."""

    roles = roles or [f"Agent {i+1}" for i in range(m)]

    # ── Round 0: independent initial answers
    chains: List[Chain] = []
    for r in roles:
        init = call_llm(f"You are {r}.  Solve the problem below as best you can.\n\n{task}\n\nAnswer:")
        chains.append(Chain(init, score(init)))

    # ── Iterative MH‑C2C refinement
    for t in range(1, T + 1):
        if verbose:
            print(f"\n=== ROUND {t} ===")
        max_delta = 0.0

        for i, chain in enumerate(chains):
            peers = [c.text for j, c in enumerate(chains) if j != i]
            e_self = self_critique(chain.text)
            e_mut  = mutual_critique(chain.text, peers)
            prop   = propose_refinement(chain.text, e_self, e_mut)
            new_s  = score(prop)

            if mh_accept(chain.score, new_s, beta):
                if verbose:
                    print(f"  + Agent {i+1} accepted (dS={new_s - chain.score:.3f})")
                max_delta = max(max_delta, abs(new_s - chain.score))
                chain.text, chain.score = prop, new_s
            elif verbose:
                print(f"  - Agent {i+1} rejected (dS={new_s - chain.score:.3f})")

        if max_delta < eps:
            if verbose:
                print(f"Converged: max dS={max_delta:.4f} < eps={eps}")
            break

    best = max(chains, key=lambda c: c.score)
    if verbose:
        print(f"\nBest score: {best.score:.3f}\n")
    return best

# ──────────────────────────────────────────────────────────────────────────────
# 7. CLI util
# ──────────────────────────────────────────────────────────────────────────────

def main() -> None:  # pragma: no cover
    parser = argparse.ArgumentParser(description="Metropolis‑Hastings C2C demo")
    parser.add_argument("--task", required=True, help="Problem statement")
    parser.add_argument("--m", type=int, default=3, help="# of agents (paths)")
    parser.add_argument("--T", type=int, default=3, help="Max refinement rounds")
    parser.add_argument("--beta", type=float, default=1.0, help="Inverse temperature β")
    parser.add_argument("--eps", type=float, default=1e-3, help="Convergence threshold ε")
    args = parser.parse_args()

    best_chain = mh_c2c(task=args.task, m=args.m, T=args.T,
                        beta=args.beta, eps=args.eps, verbose=True)
    print("=== FINAL ANSWER ===\n")
    print(best_chain.text)

if __name__ == "__main__":  # pragma: no cover
    main()
