"""
Demonstrate MH-C2C on a complex reasoning task to show its multi-agent critique benefits.
"""

from mh_c_2_c import mh_c2c

def demonstrate_complex_reasoning():
    """Show MH-C2C solving a complex multi-step problem."""
    
    # Complex problem where multiple agents can catch errors
    question = """A barber in a town shaves only those people who do not shave themselves. 
Who shaves the barber? Explain the logical paradox and propose a resolution."""
    
    print("MH-C2C Demonstration: Complex Logical Paradox")
    print("=" * 60)
    print(f"Question: {question}")
    print("=" * 60)
    print("\nRunning MH-C2C with 3 agents, 2 rounds...")
    print("(This shows the multi-agent critique process)")
    
    try:
        # Run with verbose output to show the process
        result = mh_c2c(
            task=question,
            m=3,  # 3 agents
            T=2,  # 2 rounds of critique
            beta=1.0,
            verbose=True  # Show the process
        )
        
        print("\n" + "=" * 60)
        print("FINAL RESULT FROM MH-C2C:")
        print("=" * 60)
        print(result.text)
        print(f"\nFinal Score: {result.score}")
        
    except Exception as e:
        print(f"Error: {e}")

def demonstrate_simple_comparison():
    """Show simple before/after comparison."""
    
    simple_question = "What is 15 + 27?"
    
    print("\n" + "=" * 60)
    print("Simple Comparison: Basic Math")
    print("=" * 60)
    
    try:
        result = mh_c2c(
            task=simple_question,
            m=2,  # 2 agents
            T=1,  # 1 round
            beta=1.0,
            verbose=True
        )
        
        print(f"\nFinal Answer: {result.text}")
        print(f"Score: {result.score}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    demonstrate_complex_reasoning()
    demonstrate_simple_comparison()