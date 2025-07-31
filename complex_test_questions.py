"""
Complex reasoning tasks where MH-C2C's multi-agent critique should excel.
These questions require multiple perspectives, error detection, and iterative refinement.
"""

COMPLEX_TEST_QUESTIONS = [
    {
        "id": "logic_paradox_1",
        "question": "A barber in a town shaves only those people who do not shave themselves. Who shaves the barber? Explain the logical paradox and propose a resolution.",
        "category": "logic_paradox",
        "ground_truth": "Russell's paradox - the statement is self-contradictory and has no valid solution within classical logic",
        "difficulty": "very_hard",
        "why_mhc2c_good": "Multiple agents can identify different aspects of the paradox and critique initial oversimplified answers"
    },
    {
        "id": "multi_step_reasoning_1", 
        "question": "Alice, Bob, and Charlie are playing a game. Alice starts with 100 coins. In each round: Alice gives half her coins to Bob, then Bob gives half his total to Charlie, then Charlie gives half his total back to Alice. After 3 complete rounds, who has the most coins? Show your work step by step.",
        "category": "multi_step_math",
        "ground_truth": "Charlie has most with 175 coins (Alice: 100, Bob: 50, Charlie: 175)",
        "difficulty": "hard", 
        "why_mhc2c_good": "Easy to make calculation errors that peer review can catch"
    },
    {
        "id": "ethical_dilemma_1",
        "question": "An AI system controlling a city's traffic lights can prevent a major accident by redirecting traffic, but this will cause 50 people to be 30 minutes late for work, including 3 doctors going to perform surgeries. The accident would injure 2 people seriously but not fatally. What should the AI decide and why? Consider multiple ethical frameworks.",
        "category": "complex_ethics",
        "ground_truth": None,  # Subjective but should consider utilitarian, deontological, virtue ethics
        "difficulty": "very_hard",
        "why_mhc2c_good": "Requires considering multiple ethical frameworks that different agents might emphasize"
    },
    {
        "id": "causal_reasoning_1",
        "question": "A study shows that people who drink more coffee have fewer headaches. However, people who get more sleep also drink less coffee and have fewer headaches. People who are stressed drink more coffee, sleep less, and have more headaches. What can we conclude about the relationship between coffee and headaches? What additional data would help?",
        "category": "causal_reasoning", 
        "ground_truth": "Correlation vs causation - confounding variables (stress, sleep) make direct causal inference impossible",
        "difficulty": "hard",
        "why_mhc2c_good": "Easy to jump to wrong causal conclusions that peer critique can identify"
    },
    {
        "id": "creative_constraints_1",
        "question": "Write a coherent 4-sentence story where: (1) Each sentence has exactly 7 words, (2) The story includes a time traveler, robot, and philosopher, (3) The story explores the nature of consciousness, (4) Each sentence starts with a different letter (A, B, C, D in order).",
        "category": "creative_constraints",
        "ground_truth": None,  # Creative but has specific constraints
        "difficulty": "very_hard", 
        "why_mhc2c_good": "Multiple constraints easy to violate - agents can check different constraint types"
    },
    {
        "id": "scientific_reasoning_1",
        "question": "A new drug shows 90% effectiveness in clinical trials, but only 60% effectiveness in real-world use. The drug company claims this is due to patient non-compliance, while critics say the trials were biased. Design an experiment to determine which explanation is correct, and explain what potential confounding factors you'd control for.",
        "category": "scientific_method",
        "ground_truth": "Randomized controlled trial comparing compliance-monitored vs. standard treatment, controlling for selection bias, placebo effects, etc.",
        "difficulty": "hard",
        "why_mhc2c_good": "Multiple sources of bias and confounding factors that different agents might identify"
    },
    {
        "id": "recursive_reasoning_1", 
        "question": "If you know that 'I am lying' is a paradox, then explain whether this statement is true or false: 'This sentence contains exactly five words, and this entire statement is false.' Show your reasoning process.",
        "category": "recursive_logic",
        "ground_truth": "The statement is false - first part is false (8 words not 5), making second part true, creating no paradox",
        "difficulty": "very_hard",
        "why_mhc2c_good": "Easy to get confused by nested logic - multiple agents can check different parts"
    },
    {
        "id": "strategic_thinking_1",
        "question": "In a sealed-bid auction for a $100 item where you value it at $80, there are 4 other bidders. You know one values it at $90, one at $70, and two are unknown. What should you bid to maximize your expected profit? Explain your reasoning strategy.",
        "category": "game_theory",
        "ground_truth": "Bid slightly above $70 (around $71-75) to beat known competitors while preserving profit margin",
        "difficulty": "hard",
        "why_mhc2c_good": "Multiple strategic considerations and probability calculations that agents can critique"
    }
]

def get_complex_questions():
    """Return the complex test questions for evaluation."""
    return COMPLEX_TEST_QUESTIONS

def get_questions_by_difficulty(difficulty: str):
    """Filter questions by difficulty level."""
    return [q for q in COMPLEX_TEST_QUESTIONS if q["difficulty"] == difficulty]

def get_questions_by_category(category: str):
    """Filter questions by category."""
    return [q for q in COMPLEX_TEST_QUESTIONS if q["category"] == category]

if __name__ == "__main__":
    print("Complex Test Questions for MH-C2C Evaluation")
    print("=" * 50)
    
    for q in COMPLEX_TEST_QUESTIONS:
        print(f"\n{q['id']} ({q['category']}, {q['difficulty']}):")
        print(f"Q: {q['question'][:100]}...")
        print(f"Why MH-C2C good: {q['why_mhc2c_good']}")
    
    print(f"\nTotal: {len(COMPLEX_TEST_QUESTIONS)} complex questions")
    print(f"Categories: {set(q['category'] for q in COMPLEX_TEST_QUESTIONS)}")
    print(f"Difficulties: {set(q['difficulty'] for q in COMPLEX_TEST_QUESTIONS)}")