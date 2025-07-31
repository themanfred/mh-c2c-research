"""
Evaluation Framework for MH-C2C vs. Other Prompting Techniques
Compares MH-C2C against ToT, CoT, and Self-Consistency on various tasks.
"""

import json
import time
from typing import List, Dict, Any
from dataclasses import dataclass
from abc import ABC, abstractmethod

# Test Questions across different domains
TEST_QUESTIONS = [
    {
        "id": "science_1",
        "question": "Why is the sky blue?",
        "category": "science",
        "ground_truth": "Rayleigh scattering - shorter blue wavelengths scatter more than longer wavelengths",
        "difficulty": "easy"
    },
    {
        "id": "math_1", 
        "question": "If I have 24 apples and give away 3/8 of them, how many do I have left?",
        "category": "math",
        "ground_truth": "15",
        "difficulty": "medium"
    },
    {
        "id": "reasoning_1",
        "question": "A man lives on the 20th floor. Every morning he takes the elevator down to ground floor. When he comes home, he takes the elevator to the 10th floor and walks the rest of the way... except on rainy days, when he takes the elevator all the way to the 20th floor. Why?",
        "category": "reasoning", 
        "ground_truth": "He is too short to reach the button for the 20th floor, except when he has an umbrella",
        "difficulty": "hard"
    },
    {
        "id": "creative_1",
        "question": "Write a short poem about artificial intelligence that includes the words 'future', 'learning', and 'human'.",
        "category": "creative",
        "ground_truth": None,  # Subjective evaluation
        "difficulty": "medium"
    },
    {
        "id": "ethics_1",
        "question": "Should autonomous vehicles prioritize the safety of passengers or pedestrians in unavoidable accident scenarios?",
        "category": "ethics",
        "ground_truth": None,  # Subjective evaluation
        "difficulty": "hard"
    }
]

@dataclass
class EvaluationResult:
    """Results from evaluating a single question with one technique."""
    technique: str
    question_id: str
    answer: str
    execution_time: float
    api_calls: int
    accuracy_score: float
    coherence_score: float
    completeness_score: float
    creativity_score: float
    cost_estimate: float

@dataclass 
class ComparisonReport:
    """Complete comparison report across all techniques and questions."""
    results: List[EvaluationResult]
    summary_stats: Dict[str, Any]
    technique_rankings: Dict[str, int]

class PromptingTechnique(ABC):
    """Abstract base class for prompting techniques."""
    
    def __init__(self, name: str):
        self.name = name
        self.api_calls = 0
        
    @abstractmethod
    def solve(self, question: str) -> str:
        """Solve a question using this prompting technique."""
        pass
    
    def reset_counters(self):
        """Reset API call counters."""
        self.api_calls = 0

class EvaluationMetrics:
    """Scoring functions for different aspects of answers."""
    
    @staticmethod
    def accuracy_score(answer: str, ground_truth: str) -> float:
        """Score answer accuracy against ground truth (0-1)."""
        if ground_truth is None:
            return 0.5  # Neutral for subjective questions
        
        # Simple word overlap for now - could use semantic similarity
        answer_words = set(answer.lower().split())
        truth_words = set(ground_truth.lower().split())
        
        if len(truth_words) == 0:
            return 1.0 if len(answer_words) == 0 else 0.0
            
        intersection = len(answer_words.intersection(truth_words))
        union = len(answer_words.union(truth_words))
        return intersection / union if union > 0 else 0.0
    
    @staticmethod
    def coherence_score(answer: str) -> float:
        """Score logical coherence and readability (0-1)."""
        # Simple heuristics - could use more sophisticated models
        sentences = [s.strip() for s in answer.split('.') if s.strip()]
        if len(sentences) == 0:
            return 0.0
            
        # Penalize very short or very long sentences
        avg_length = sum(len(s.split()) for s in sentences) / len(sentences)
        coherence = min(1.0, max(0.1, 1.0 - abs(avg_length - 15) / 20))
        
        # Bonus for proper structure
        if answer[0].isupper() and answer.endswith('.'):
            coherence += 0.1
            
        return min(1.0, coherence)
    
    @staticmethod 
    def completeness_score(answer: str) -> float:
        """Score how complete/comprehensive the answer is (0-1)."""
        # Based on length and structure
        word_count = len(answer.split())
        
        # Optimal range: 50-200 words
        if 50 <= word_count <= 200:
            return 1.0
        elif word_count < 20:
            return word_count / 20
        elif word_count > 300:
            return max(0.3, 1.0 - (word_count - 200) / 1000)
        else:
            return 0.8  # Reasonable length
    
    @staticmethod
    def creativity_score(answer: str) -> float:
        """Score creativity/originality (0-1)."""
        # Simple heuristics for creativity
        creative_indicators = [
            'imagine', 'creative', 'innovative', 'unique', 'novel',
            'metaphor', 'analogy', 'perspective', 'unusual', 'interesting'
        ]
        
        answer_lower = answer.lower()
        creative_count = sum(1 for word in creative_indicators if word in answer_lower)
        
        # Bonus for varied sentence structures
        sentences = answer.split('.')
        varied_starts = len(set(s.strip()[:3].lower() for s in sentences if s.strip()))
        variety_bonus = min(0.3, varied_starts / len(sentences)) if sentences else 0
        
        return min(1.0, creative_count * 0.1 + variety_bonus + 0.4)

class EvaluationFramework:
    """Main evaluation framework coordinator."""
    
    def __init__(self):
        self.techniques: List[PromptingTechnique] = []
        self.metrics = EvaluationMetrics()
        
    def add_technique(self, technique: PromptingTechnique):
        """Add a prompting technique to evaluate."""
        self.techniques.append(technique)
        
    def evaluate_single(self, technique: PromptingTechnique, question: Dict) -> EvaluationResult:
        """Evaluate one technique on one question."""
        technique.reset_counters()
        start_time = time.time()
        
        answer = technique.solve(question["question"])
        
        execution_time = time.time() - start_time
        
        # Calculate scores
        accuracy = self.metrics.accuracy_score(answer, question.get("ground_truth"))
        coherence = self.metrics.coherence_score(answer) 
        completeness = self.metrics.completeness_score(answer)
        creativity = self.metrics.creativity_score(answer)
        
        # Estimate cost (rough: $0.002 per API call for GPT-4)
        cost_estimate = technique.api_calls * 0.002
        
        return EvaluationResult(
            technique=technique.name,
            question_id=question["id"],
            answer=answer,
            execution_time=execution_time,
            api_calls=technique.api_calls,
            accuracy_score=accuracy,
            coherence_score=coherence,
            completeness_score=completeness,
            creativity_score=creativity,
            cost_estimate=cost_estimate
        )
    
    def run_comparison(self) -> ComparisonReport:
        """Run complete evaluation across all techniques and questions."""
        results = []
        
        print("Starting comprehensive evaluation...")
        
        for question in TEST_QUESTIONS:
            print(f"\nEvaluating: {question['id']} - {question['category']}")
            
            for technique in self.techniques:
                print(f"  Running {technique.name}...")
                try:
                    result = self.evaluate_single(technique, question)
                    results.append(result)
                    print(f"    + Completed in {result.execution_time:.1f}s")
                except Exception as e:
                    print(f"    - Failed: {e}")
        
        # Generate summary statistics
        summary_stats = self._generate_summary(results)
        technique_rankings = self._rank_techniques(results)
        
        return ComparisonReport(
            results=results,
            summary_stats=summary_stats,
            technique_rankings=technique_rankings
        )
    
    def _generate_summary(self, results: List[EvaluationResult]) -> Dict[str, Any]:
        """Generate summary statistics from results."""
        summary = {}
        
        for technique_name in set(r.technique for r in results):
            technique_results = [r for r in results if r.technique == technique_name]
            
            summary[technique_name] = {
                "avg_accuracy": sum(r.accuracy_score for r in technique_results) / len(technique_results),
                "avg_coherence": sum(r.coherence_score for r in technique_results) / len(technique_results),
                "avg_completeness": sum(r.completeness_score for r in technique_results) / len(technique_results),
                "avg_creativity": sum(r.creativity_score for r in technique_results) / len(technique_results),
                "avg_time": sum(r.execution_time for r in technique_results) / len(technique_results),
                "total_api_calls": sum(r.api_calls for r in technique_results),
                "total_cost": sum(r.cost_estimate for r in technique_results),
                "questions_completed": len(technique_results)
            }
        
        return summary
    
    def _rank_techniques(self, results: List[EvaluationResult]) -> Dict[str, int]:
        """Rank techniques by overall performance."""
        technique_scores = {}
        
        for technique_name in set(r.technique for r in results):
            technique_results = [r for r in results if r.technique == technique_name]
            
            # Composite score: weighted average of all metrics
            composite_score = sum(
                0.3 * r.accuracy_score +
                0.25 * r.coherence_score + 
                0.25 * r.completeness_score +
                0.2 * r.creativity_score
                for r in technique_results
            ) / len(technique_results)
            
            technique_scores[technique_name] = composite_score
        
        # Rank by composite score
        sorted_techniques = sorted(technique_scores.items(), key=lambda x: x[1], reverse=True)
        return {name: rank + 1 for rank, (name, score) in enumerate(sorted_techniques)}
    
    def save_results(self, report: ComparisonReport, filename: str):
        """Save evaluation results to JSON file."""
        # Convert to serializable format
        serializable_results = []
        for result in report.results:
            serializable_results.append({
                "technique": result.technique,
                "question_id": result.question_id,
                "answer": result.answer,
                "execution_time": result.execution_time,
                "api_calls": result.api_calls,
                "accuracy_score": result.accuracy_score,
                "coherence_score": result.coherence_score,
                "completeness_score": result.completeness_score,
                "creativity_score": result.creativity_score,
                "cost_estimate": result.cost_estimate
            })
        
        report_data = {
            "results": serializable_results,
            "summary_stats": report.summary_stats,
            "technique_rankings": report.technique_rankings,
            "test_questions": TEST_QUESTIONS
        }
        
        with open(filename, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"Results saved to {filename}")

if __name__ == "__main__":
    # This will be used later when we implement all techniques
    framework = EvaluationFramework()
    print("Evaluation framework ready!")
    print(f"Test questions: {len(TEST_QUESTIONS)}")
    for q in TEST_QUESTIONS:
        print(f"  - {q['id']}: {q['category']} ({q['difficulty']})")