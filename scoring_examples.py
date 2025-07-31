"""
Alternative scoring functions for real-world use cases.
Replace the toy score() function in mh_c2c.py with one of these.
"""

def accuracy_score(text: str, ground_truth: str) -> float:
    """Score based on similarity to ground truth answer."""
    # Simple word overlap - use semantic similarity for better results
    text_words = set(text.lower().split())
    truth_words = set(ground_truth.lower().split())
    intersection = len(text_words.intersection(truth_words))
    union = len(text_words.union(truth_words))
    return intersection / union if union > 0 else 0.0

def complexity_score(text: str) -> float:
    """Score based on explanation complexity and depth."""
    sentences = text.split('.')
    avg_sentence_length = sum(len(s.split()) for s in sentences) / len(sentences)
    return min(avg_sentence_length / 20, 1.0)  # Cap at 1.0

def factuality_score(text: str) -> float:
    """Placeholder for factuality scoring using external model."""
    # In practice, use a fact-checking model or API
    # For now, penalize obviously false claims
    false_indicators = ['aliens built', 'flat earth', 'vaccines cause']
    penalty = sum(1 for indicator in false_indicators if indicator in text.lower())
    return 1.0 - (penalty * 0.3)

def readability_score(text: str) -> float:
    """Score based on readability (Flesch Reading Ease approximation)."""
    words = text.split()
    sentences = text.split('.')
    if len(sentences) == 0 or len(words) == 0:
        return 0.0
    
    avg_sentence_length = len(words) / len(sentences)
    # Simplified readability score
    return max(0, min(1, (30 - avg_sentence_length) / 30))

def composite_score(text: str, ground_truth: str = None) -> float:
    """Combine multiple scoring metrics."""
    scores = []
    
    # Readability component
    scores.append(readability_score(text) * 0.3)
    
    # Complexity component  
    scores.append(complexity_score(text) * 0.3)
    
    # Factuality component
    scores.append(factuality_score(text) * 0.4)
    
    # Accuracy component (if ground truth available)
    if ground_truth:
        scores.append(accuracy_score(text, ground_truth) * 0.5)
    
    return sum(scores) / len(scores)