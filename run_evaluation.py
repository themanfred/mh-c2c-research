"""
Main script to run comprehensive evaluation of MH-C2C vs other prompting techniques.
"""

from evaluation_framework import EvaluationFramework, TEST_QUESTIONS
from prompting_techniques import create_all_techniques
import json
import os
from datetime import datetime

def main():
    """Run the complete evaluation suite."""
    print("=" * 60)
    print("MH-C2C vs. Prompting Techniques Evaluation")
    print("=" * 60)
    
    # Initialize framework
    framework = EvaluationFramework()
    
    # Add all techniques
    techniques = create_all_techniques()
    for technique in techniques:
        framework.add_technique(technique)
        print(f"Added technique: {technique.name}")
    
    print(f"\nEvaluating {len(techniques)} techniques on {len(TEST_QUESTIONS)} questions")
    print("This may take several minutes due to API calls...")
    
    # Run evaluation
    try:
        report = framework.run_comparison()
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"evaluation_results_{timestamp}.json"
        framework.save_results(report, filename)
        
        # Print summary
        print("\n" + "=" * 60)
        print("EVALUATION COMPLETE")
        print("=" * 60)
        
        print("\nTECHNIQUE RANKINGS:")
        for technique, rank in report.technique_rankings.items():
            print(f"{rank}. {technique}")
        
        print("\nDETAILED RESULTS:")
        for technique, stats in report.summary_stats.items():
            print(f"\n{technique}:")
            print(f"  Average Accuracy: {stats['avg_accuracy']:.3f}")
            print(f"  Average Coherence: {stats['avg_coherence']:.3f}")
            print(f"  Average Completeness: {stats['avg_completeness']:.3f}")
            print(f"  Average Creativity: {stats['avg_creativity']:.3f}")
            print(f"  Average Time: {stats['avg_time']:.1f}s")
            print(f"  Total API Calls: {stats['total_api_calls']}")
            print(f"  Estimated Cost: ${stats['total_cost']:.3f}")
        
        print(f"\nDetailed results saved to: {filename}")
        
        # Generate insights
        generate_insights(report)
        
    except Exception as e:
        print(f"Evaluation failed: {e}")
        raise

def generate_insights(report):
    """Generate key insights from the evaluation results."""
    print("\n" + "=" * 60)
    print("KEY INSIGHTS")
    print("=" * 60)
    
    # Find best technique overall
    best_technique = min(report.technique_rankings.items(), key=lambda x: x[1])
    print(f"🏆 Best Overall: {best_technique[0]}")
    
    # Find most cost-effective
    cost_efficiency = {}
    for technique, stats in report.summary_stats.items():
        if stats['total_cost'] > 0:
            # Composite score / cost
            composite = (stats['avg_accuracy'] + stats['avg_coherence'] + 
                        stats['avg_completeness'] + stats['avg_creativity']) / 4
            cost_efficiency[technique] = composite / stats['total_cost']
    
    if cost_efficiency:
        most_efficient = max(cost_efficiency.items(), key=lambda x: x[1])
        print(f"💰 Most Cost-Effective: {most_efficient[0]}")
    
    # Find fastest
    fastest = min(report.summary_stats.items(), key=lambda x: x[1]['avg_time'])
    print(f"⚡ Fastest: {fastest[0]} ({fastest[1]['avg_time']:.1f}s avg)")
    
    # MH-C2C specific analysis
    mhc2c_stats = report.summary_stats.get('MH-C2C')
    if mhc2c_stats:
        mhc2c_rank = report.technique_rankings.get('MH-C2C', 'N/A')
        print(f"\n🤖 MH-C2C Performance:")
        print(f"   Rank: #{mhc2c_rank} out of {len(report.technique_rankings)}")
        print(f"   Strong in: ", end="")
        
        # Find MH-C2C's best metrics
        metrics = {
            'Accuracy': mhc2c_stats['avg_accuracy'],
            'Coherence': mhc2c_stats['avg_coherence'], 
            'Completeness': mhc2c_stats['avg_completeness'],
            'Creativity': mhc2c_stats['avg_creativity']
        }
        best_metrics = sorted(metrics.items(), key=lambda x: x[1], reverse=True)[:2]
        print(", ".join([f"{metric} ({score:.3f})" for metric, score in best_metrics]))

if __name__ == "__main__":
    main()