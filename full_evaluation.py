"""
Full evaluation including all techniques and complex reasoning tasks.
"""

from evaluation_framework import EvaluationFramework, TEST_QUESTIONS
from prompting_techniques import create_all_techniques
from complex_test_questions import get_complex_questions
import json
from datetime import datetime

def main():
    """Run comprehensive evaluation on both basic and complex questions."""
    print("=" * 70)
    print("COMPREHENSIVE MH-C2C EVALUATION")
    print("Basic Questions + Complex Reasoning Tasks")
    print("=" * 70)
    
    # Combine basic and complex questions
    all_questions = TEST_QUESTIONS + get_complex_questions()
    
    # Override questions in framework
    import evaluation_framework
    evaluation_framework.TEST_QUESTIONS = all_questions
    
    framework = EvaluationFramework()
    
    # Add all techniques
    techniques = create_all_techniques()
    for technique in techniques:
        framework.add_technique(technique)
        print(f"✓ Added: {technique.name}")
    
    print(f"\nEvaluating {len(techniques)} techniques on {len(all_questions)} questions")
    print("(5 basic + 8 complex reasoning tasks)")
    print("\nThis will take 15-30 minutes due to comprehensive API testing...")
    print("Press Ctrl+C to interrupt if needed.\n")
    
    try:
        report = framework.run_comparison()
        
        # Save detailed results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"comprehensive_evaluation_{timestamp}.json"
        framework.save_results(report, filename)
        
        # Print comprehensive analysis
        print_comprehensive_analysis(report, all_questions)
        
        print(f"\n💾 Detailed results saved to: {filename}")
        
    except KeyboardInterrupt:
        print("\n⚠️ Evaluation interrupted by user")
    except Exception as e:
        print(f"❌ Evaluation failed: {e}")
        import traceback
        traceback.print_exc()

def print_comprehensive_analysis(report, questions):
    """Print detailed analysis of results."""
    print("\n" + "=" * 70)
    print("COMPREHENSIVE ANALYSIS")
    print("=" * 70)
    
    # Overall rankings
    print("\n🏆 OVERALL TECHNIQUE RANKINGS:")
    for technique, rank in sorted(report.technique_rankings.items(), key=lambda x: x[1]):
        print(f"  {rank}. {technique}")
    
    # Detailed performance metrics
    print("\n📊 DETAILED PERFORMANCE METRICS:")
    for technique, stats in report.summary_stats.items():
        print(f"\n{technique}:")
        print(f"  🎯 Accuracy:     {stats['avg_accuracy']:.3f}")
        print(f"  🧠 Coherence:    {stats['avg_coherence']:.3f}")
        print(f"  📝 Completeness: {stats['avg_completeness']:.3f}")
        print(f"  🎨 Creativity:   {stats['avg_creativity']:.3f}")
        print(f"  ⚡ Avg Time:     {stats['avg_time']:.1f}s")
        print(f"  📞 API Calls:    {stats['total_api_calls']}")
        print(f"  💰 Est. Cost:    ${stats['total_cost']:.3f}")
    
    # Category-specific analysis
    analyze_by_category(report, questions)
    
    # MH-C2C specific insights
    analyze_mhc2c_performance(report, questions)

def analyze_by_category(report, questions):
    """Analyze performance by question category."""
    print("\n📋 PERFORMANCE BY QUESTION CATEGORY:")
    
    # Group results by category
    category_results = {}
    for result in report.results:
        question = next(q for q in questions if q["id"] == result.question_id)
        category = question["category"]
        
        if category not in category_results:
            category_results[category] = {}
        
        if result.technique not in category_results[category]:
            category_results[category][result.technique] = []
        
        category_results[category][result.technique].append(result)
    
    # Calculate average scores by category
    for category, techniques in category_results.items():
        print(f"\n  {category.upper()}:")
        
        technique_scores = {}
        for technique, results in techniques.items():
            avg_score = sum(r.accuracy_score + r.coherence_score + 
                          r.completeness_score + r.creativity_score 
                          for r in results) / (len(results) * 4)
            technique_scores[technique] = avg_score
        
        # Rank techniques for this category
        ranked = sorted(technique_scores.items(), key=lambda x: x[1], reverse=True)
        for i, (technique, score) in enumerate(ranked, 1):
            print(f"    {i}. {technique}: {score:.3f}")

def analyze_mhc2c_performance(report, questions):
    """Analyze where MH-C2C performs best and worst."""
    print("\n🤖 MH-C2C DETAILED ANALYSIS:")
    
    mhc2c_results = [r for r in report.results if r.technique == "MH-C2C"]
    
    if not mhc2c_results:
        print("  No MH-C2C results found!")
        return
    
    # Find best and worst performing questions
    mhc2c_scores = []
    for result in mhc2c_results:
        composite_score = (result.accuracy_score + result.coherence_score + 
                         result.completeness_score + result.creativity_score) / 4
        mhc2c_scores.append((result.question_id, composite_score, result))
    
    mhc2c_scores.sort(key=lambda x: x[1], reverse=True)
    
    print(f"\n  🎯 Best Performance:")
    for question_id, score, result in mhc2c_scores[:3]:
        question = next(q for q in questions if q["id"] == question_id)
        print(f"    {question_id} ({question['category']}): {score:.3f}")
        print(f"      Accuracy: {result.accuracy_score:.3f}, "
              f"Coherence: {result.coherence_score:.3f}")
    
    print(f"\n  📉 Worst Performance:")
    for question_id, score, result in mhc2c_scores[-3:]:
        question = next(q for q in questions if q["id"] == question_id)
        print(f"    {question_id} ({question['category']}): {score:.3f}")
        print(f"      Accuracy: {result.accuracy_score:.3f}, "
              f"Coherence: {result.coherence_score:.3f}")
    
    # Efficiency analysis
    mhc2c_stats = report.summary_stats.get("MH-C2C", {})
    if mhc2c_stats:
        print(f"\n  ⚡ Efficiency Analysis:")
        print(f"    Average time per question: {mhc2c_stats['avg_time']:.1f}s")
        print(f"    API calls per question: {mhc2c_stats['total_api_calls'] / len(mhc2c_results):.1f}")
        print(f"    Cost per question: ${mhc2c_stats['total_cost'] / len(mhc2c_results):.3f}")

if __name__ == "__main__":
    main()