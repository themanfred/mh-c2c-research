# MH-C2C Setup and Testing Guide

## 1. Install Dependencies
```bash
pip install openai tiktoken tenacity python-dotenv
```

## 2. Create Environment File
Create a `.env` file in this directory with your OpenAI API key:
```
OPENAI_API_KEY="sk-your-api-key-here"
```

## 3. Basic Usage
```bash
python mh_c2c.py --task "Explain why the sky is blue." --m 3 --T 3 --beta 1.0
```

## 4. Parameters Explained
- `--task`: The problem/question to solve
- `--m`: Number of agents (default: 3)
- `--T`: Maximum refinement rounds (default: 3)  
- `--beta`: Inverse temperature for Metropolis-Hastings (default: 1.0)
- `--eps`: Convergence threshold (default: 0.001)

## 5. How It Works
1. **Initialize**: Each agent generates an independent answer
2. **Critique**: Each agent critiques itself and receives peer critiques
3. **Refine**: Agents propose improved answers based on critiques
4. **Accept/Reject**: Uses Metropolis-Hastings to accept/reject improvements
5. **Converge**: Stops when improvements are below threshold

## 6. Current Scoring Function
The demo uses a toy scoring function: `score = -len(text)` (shorter is better).
For real use, replace the `score()` function with domain-specific metrics.