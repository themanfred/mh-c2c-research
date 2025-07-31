"""
Test a single complex question with all techniques to demonstrate MH-C2C performance.
"""

from prompting_techniques import BaselineTechnique, ChainOfThoughtTechnique, MHC2CTechnique, TreeOfThoughtsTechnique
import time

def test_single_question():
    """Test one complex reasoning question."""
    
    # Complex multi-step math problem
    question = """Alice, Bob, and Charlie are playing a game. Alice starts with 100 coins. 
In each round: Alice gives half her coins to Bob, then Bob gives half his total to Charlie, 
then Charlie gives half his total back to Alice. After 3 complete rounds, who has the most coins? 
Show your work step by step."""
    
    print("Testing Complex Multi-Step Reasoning Question")
    print("=" * 60)
    print(f"Question: {question}")
    print("=" * 60)
    
    # Test techniques
    techniques = [
        ("Baseline", BaselineTechnique()),
        ("Chain-of-Thought", ChainOfThoughtTechnique()),
        ("Tree-of-Thoughts", TreeOfThoughtsTechnique(num_thoughts=2, depth=1)),  # Simplified
        ("MH-C2C", MHC2CTechnique(m=2, T=1, beta=1.0))  # Simplified for speed
    ]
    
    results = []
    
    for name, technique in techniques:
        print(f"\n{name}:")
        print("-" * 30)
        
        start_time = time.time()
        try:
            answer = technique.solve(question)
            end_time = time.time()
            
            print(f"Answer: {answer[:200]}{'...' if len(answer) > 200 else ''}")
            print(f"Time: {end_time - start_time:.1f}s")
            print(f"API calls: {technique.api_calls}")
            
            results.append({
                "technique": name,
                "answer": answer,
                "time": end_time - start_time,
                "api_calls": technique.api_calls,
                "answer_length": len(answer)
            })
            
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({
                "technique": name,
                "answer": f"ERROR: {e}",
                "time": 0,
                "api_calls": 0,
                "answer_length": 0
            })
    
    # Summary comparison
    print("\n" + "=" * 60)
    print("COMPARISON SUMMARY")
    print("=" * 60)
    
    print(f"{'Technique':<20} {'Time (s)':<10} {'API Calls':<12} {'Length':<8}")
    print("-" * 60)
    
    for result in results:
        if result["time"] > 0:  # Skip errors
            print(f"{result['technique']:<20} {result['time']:<10.1f} {result['api_calls']:<12} {result['answer_length']:<8}")
    
    print(f"\nGround Truth: Charlie has most with 175 coins")
    print("(Alice: 100, Bob: 50, Charlie: 175 after 3 rounds)")
    
    return results

if __name__ == "__main__":
    test_single_question()