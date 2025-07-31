"""
Test MH-C2C on complex reasoning tasks only.
"""

from evaluation_framework import EvaluationFramework
from prompting_techniques import BaselineTechnique, ChainOfThoughtTechnique, MHC2CTechnique
from complex_test_questions import get_complex_questions

def main():
    """Test on complex questions only."""
    print("Testing MH-C2C on Complex Reasoning Tasks")
    print("=" * 50)
    
    # Use only complex questions
    complex_questions = get_complex_questions()[:3]  # Test first 3 for speed
    
    # Override questions in framework
    import evaluation_framework
    evaluation_framework.TEST_QUESTIONS = complex_questions
    
    framework = EvaluationFramework()
    
    # Add 3 techniques for comparison
    techniques = [
        BaselineTechnique(),
        ChainOfThoughtTechnique(),
        MHC2CTechnique(m=3, T=2, beta=1.0)
    ]
    
    for technique in techniques:
        framework.add_technique(technique)
        print(f"+ Added: {technique.name}")
    
    print(f"\nTesting {len(techniques)} techniques on {len(complex_questions)} complex questions:")
    for q in complex_questions:
        print(f"  - {q['id']}: {q['category']} ({q['difficulty']})")
    
    print("\nRunning evaluation...")
    
    try:
        report = framework.run_comparison()
        
        print("\n" + "=" * 50)
        print("COMPLEX REASONING RESULTS")
        print("=" * 50)
        
        # Rankings
        print("\nTechnique Rankings:")
        for technique, rank in sorted(report.technique_rankings.items(), key=lambda x: x[1]):
            print(f"  {rank}. {technique}")
        
        # Detailed results for each question
        print("\nDetailed Results by Question:")
        for q in complex_questions:
            print(f"\n{q['id']} ({q['category']}):")
            question_results = [r for r in report.results if r.question_id == q['id']]
            
            for result in sorted(question_results, key=lambda x: x.accuracy_score, reverse=True):
                print(f"  {result.technique}:")
                print(f"    Accuracy: {result.accuracy_score:.3f}")
                print(f"    Coherence: {result.coherence_score:.3f}")
                print(f"    Time: {result.execution_time:.1f}s")
                print(f"    API calls: {result.api_calls}")
        
        # MH-C2C Analysis
        mhc2c_results = [r for r in report.results if r.technique == "MH-C2C"]
        if mhc2c_results:
            print(f"\nMH-C2C Analysis:")
            avg_accuracy = sum(r.accuracy_score for r in mhc2c_results) / len(mhc2c_results)
            avg_time = sum(r.execution_time for r in mhc2c_results) / len(mhc2c_results)
            total_calls = sum(r.api_calls for r in mhc2c_results)
            
            print(f"  Average accuracy: {avg_accuracy:.3f}")
            print(f"  Average time per question: {avg_time:.1f}s")
            print(f"  Total API calls: {total_calls}")
            print(f"  Questions where MH-C2C ranked #1: {sum(1 for q in complex_questions if max([r for r in report.results if r.question_id == q['id']], key=lambda x: x.accuracy_score).technique == 'MH-C2C')}")
        
    except Exception as e:
        print(f"Test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()