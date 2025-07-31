"""
Implementation of various prompting techniques for comparison with MH-C2C.
Includes ToT, CoT, Self-Consistency, and MH-C2C wrapper.
"""

import os
import json
import random
import openai
from typing import List, Dict, Any
from evaluation_framework import PromptingTechnique
from mh_c_2_c import mh_c2c, Chain, call_llm

# Import from existing MH-C2C implementation
from dotenv import load_dotenv
load_dotenv()

class TreeOfThoughtsTechnique(PromptingTechnique):
    """
    Tree of Thoughts implementation.
    Generates multiple thought paths and selects the best one.
    """
    
    def __init__(self, num_thoughts: int = 3, depth: int = 2):
        super().__init__("Tree-of-Thoughts")
        self.num_thoughts = num_thoughts
        self.depth = depth
    
    def solve(self, question: str) -> str:
        """Solve using Tree of Thoughts approach."""
        # Step 1: Generate initial thoughts
        initial_thoughts = self._generate_thoughts(question, "")
        
        # Step 2: Evaluate and expand best thoughts
        best_path = self._search_best_path(question, initial_thoughts)
        
        # Step 3: Generate final answer from best path
        final_answer = self._generate_final_answer(question, best_path)
        
        return final_answer
    
    def _generate_thoughts(self, question: str, context: str) -> List[str]:
        """Generate multiple thoughts for the current step."""
        prompt = f"""
Problem: {question}
Context: {context}

Generate {self.num_thoughts} different ways to approach this problem. 
Each approach should be a clear, distinct reasoning step.

Format your response as:
1. [First approach]
2. [Second approach]  
3. [Third approach]
"""
        
        response = call_llm(prompt)
        self.api_calls += 1
        
        # Parse numbered responses
        thoughts = []
        for line in response.split('\n'):
            line = line.strip()
            if line and (line[0].isdigit() or line.startswith('-')):
                # Remove numbering and extract thought
                thought = line.split('.', 1)[-1].strip()
                if thought:
                    thoughts.append(thought)
        
        return thoughts[:self.num_thoughts]
    
    def _evaluate_thoughts(self, question: str, thoughts: List[str]) -> List[float]:
        """Evaluate thoughts and return scores."""
        scores = []
        
        for thought in thoughts:
            prompt = f"""
Problem: {question}
Proposed approach: {thought}

Rate this approach on a scale of 1-10 for:
- Likelihood of leading to correct answer
- Logical soundness
- Completeness

Provide only a single number (1-10) as your response.
"""
            
            response = call_llm(prompt)
            self.api_calls += 1
            
            try:
                score = float(response.strip())
                scores.append(score)
            except ValueError:
                scores.append(5.0)  # Default score
        
        return scores
    
    def _search_best_path(self, question: str, initial_thoughts: List[str]) -> List[str]:
        """Search for the best reasoning path."""
        current_thoughts = initial_thoughts
        path = []
        
        for depth in range(self.depth):
            # Evaluate current thoughts
            scores = self._evaluate_thoughts(question, current_thoughts)
            
            # Select best thought
            best_idx = scores.index(max(scores))
            best_thought = current_thoughts[best_idx]
            path.append(best_thought)
            
            # Generate next level thoughts if not at max depth
            if depth < self.depth - 1:
                context = " -> ".join(path)
                current_thoughts = self._generate_thoughts(question, context)
        
        return path
    
    def _generate_final_answer(self, question: str, path: List[str]) -> str:
        """Generate final answer from the best reasoning path."""
        reasoning_chain = " -> ".join(path)
        
        prompt = f"""
Problem: {question}
Reasoning path: {reasoning_chain}

Based on this reasoning path, provide a clear, comprehensive final answer.
"""
        
        response = call_llm(prompt)
        self.api_calls += 1
        
        return response

class ChainOfThoughtTechnique(PromptingTechnique):
    """
    Chain of Thought implementation.
    Encourages step-by-step reasoning.
    """
    
    def __init__(self):
        super().__init__("Chain-of-Thought")
    
    def solve(self, question: str) -> str:
        """Solve using Chain of Thought prompting."""
        prompt = f"""
{question}

Let's think step by step to solve this problem systematically.

Step 1: Understand the problem
Step 2: Identify key information
Step 3: Apply relevant knowledge/reasoning
Step 4: Arrive at conclusion

Please work through each step clearly and provide your final answer.
"""
        
        response = call_llm(prompt)
        self.api_calls += 1
        
        return response

class SelfConsistencyTechnique(PromptingTechnique):
    """
    Self-Consistency implementation.
    Generates multiple CoT responses and selects most common answer.
    """
    
    def __init__(self, num_samples: int = 5):
        super().__init__("Self-Consistency")
        self.num_samples = num_samples
    
    def solve(self, question: str) -> str:
        """Solve using Self-Consistency approach."""
        # Generate multiple reasoning chains
        responses = []
        
        for i in range(self.num_samples):
            prompt = f"""
{question}

Let's think step by step to solve this problem. Show your reasoning clearly.
"""
            
            response = call_llm(prompt)
            self.api_calls += 1
            responses.append(response)
        
        # For now, return the longest response as it's likely most complete
        # In a full implementation, you'd extract final answers and vote
        return max(responses, key=len)

class MHC2CTechnique(PromptingTechnique):
    """
    Wrapper for MH-C2C technique to fit evaluation framework.
    """
    
    def __init__(self, m: int = 3, T: int = 2, beta: float = 1.0):
        super().__init__("MH-C2C")
        self.m = m
        self.T = T
        self.beta = beta
    
    def solve(self, question: str) -> str:
        """Solve using MH-C2C algorithm."""
        # Use the existing mh_c2c function
        result = mh_c2c(
            task=question,
            m=self.m,
            T=self.T,
            beta=self.beta,
            verbose=False  # Disable verbose for cleaner evaluation
        )
        
        # Estimate API calls (rough): m initial + m*T*3 for critiques/refinements
        self.api_calls = self.m + (self.m * self.T * 3)
        
        return result.text

class BaselineTechnique(PromptingTechnique):
    """
    Simple baseline - direct prompting without special techniques.
    """
    
    def __init__(self):
        super().__init__("Baseline")
    
    def solve(self, question: str) -> str:
        """Solve using direct prompting."""
        response = call_llm(question)
        self.api_calls += 1
        return response

# Factory function to create all techniques
def create_all_techniques() -> List[PromptingTechnique]:
    """Create instances of all prompting techniques for evaluation."""
    return [
        BaselineTechnique(),
        ChainOfThoughtTechnique(),
        SelfConsistencyTechnique(num_samples=3),  # Reduced for cost
        TreeOfThoughtsTechnique(num_thoughts=3, depth=2),
        MHC2CTechnique(m=3, T=2, beta=1.0)
    ]

if __name__ == "__main__":
    # Test one technique
    print("Testing Tree of Thoughts technique...")
    tot = TreeOfThoughtsTechnique(num_thoughts=2, depth=1)  # Small test
    
    try:
        answer = tot.solve("Why is the sky blue?")
        print(f"Answer: {answer}")
        print(f"API calls: {tot.api_calls}")
    except Exception as e:
        print(f"Error: {e}")