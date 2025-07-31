"""
Quick test of the evaluation system with reduced scope.
"""

from evaluation_framework import EvaluationFramework
from prompting_techniques import BaselineTechnique, ChainOfThoughtTechnique, MHC2CTechnique

# Simplified test questions
QUICK_TEST_QUESTIONS = [
    {
        "id": "science_1",
        "question": "Why is the sky blue?",
        "category": "science",
        "ground_truth": "Rayleigh scattering",
        "difficulty": "easy"
    },
    {
        "id": "math_1", 
        "question": "What is 15 + 27?",
        "category": "math",
        "ground_truth": "42",
        "difficulty": "easy"
    }
]

def main():
    """Run quick evaluation test."""
    print("Quick Evaluation Test")
    print("=" * 40)
    
    # Override test questions in framework
    import evaluation_framework
    evaluation_framework.TEST_QUESTIONS = QUICK_TEST_QUESTIONS
    
    framework = EvaluationFramework()
    
    # Add only 3 techniques for speed
    techniques = [
        BaselineTechnique(),
        ChainOfThoughtTechnique(), 
        MHC2CTechnique(m=2, T=1, beta=1.0)  # Reduced parameters
    ]
    
    for technique in techniques:
        framework.add_technique(technique)
        print(f"Added: {technique.name}")
    
    print(f"\nTesting {len(techniques)} techniques on {len(QUICK_TEST_QUESTIONS)} questions")
    
    try:
        report = framework.run_comparison()
        
        print("\n" + "=" * 40)
        print("RESULTS")
        print("=" * 40)
        
        print("\nRankings:")
        for technique, rank in report.technique_rankings.items():
            print(f"{rank}. {technique}")
        
        print("\nSample Results:")
        for result in report.results[:3]:  # Show first 3
            print(f"\n{result.technique} on {result.question_id}:")
            print(f"  Answer: {result.answer[:100]}...")
            print(f"  Accuracy: {result.accuracy_score:.3f}")
            print(f"  Time: {result.execution_time:.1f}s")
            print(f"  API calls: {result.api_calls}")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()