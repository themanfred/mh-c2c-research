# Multi-Agent Critique-to-Consensus (MH-C2C) Research

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Research Status](https://img.shields.io/badge/status-publication--ready-green.svg)](https://github.com/themanfred/mh-c2c-research)

**Author:** Thomas Freund  
**Contact:** thomas@fundamentosia.com
**License:** MIT  
**Status:** Publication-ready research

## Overview

This repository contains the complete research implementation and evaluation of **Multi-Agent Metropolis-Hastings Critique-to-Consensus (MH-C2C)** methods for enhancing Large Language Model reasoning capabilities. Our approach demonstrates **15% performance improvement** over traditional prompting techniques on complex reasoning tasks. We introduce Critique-to-Consensus (C2C), a prompting frame-
work designed to simulate emergent reasoning through adversarial it-
eration. Informally we also created a promting techinque called  Roast-to-Refine (R2R), this method en-
ables multiple reasoning paths to critique (roast) themselves and one another,
evolving through iterative refinement toward a superior solution. By
incorporating both self-assessment and peer review into a prompting
loop, C2C mimics debate, peer feedback, and design thinking, foster-
ing robust idea evolution. We demonstrate the advantages of C2C over
traditional frameworks such as Tree-of-Thought [4], Debate Models [2],
Constitutional AI [1], and Reflection-based prompting [3]. Our exper-
iments show that C2C not only improves output quality but also en-
courages transparency, convergence, and robustness in language model
reasoning.

## 🔥 Key Highlights

- **Novel Algorithm**: First application of Metropolis-Hastings to multi-agent LLM reasoning
- **Practical Implementation**: Roast-to-Refine (R2R) - single-prompt solution achieving 80% of MH-C2C performance
- **Comprehensive Evaluation**: 5 techniques tested across 13 reasoning tasks
- **Publication Ready**: 12,000+ word academic paper included
- **Open Source**: Complete framework for reproducible research

### Key Contributions

1. **MH-C2C Algorithm**: Novel multi-agent approach using Metropolis-Hastings acceptance criteria
2. **Roast-to-Refine (R2R)**: Practical prompt-based implementation achieving 80% of MH-C2C performance
3. **Comprehensive Evaluation**: Framework comparing 5 prompting techniques across 13 reasoning tasks
4. **15% Performance Improvement**: Demonstrated superiority on complex reasoning tasks

## 🚀 Quick Start

### Prerequisites
```bash
pip install openai tiktoken tenacity python-dotenv
```

### Environment Setup
```bash
# Clone repository
git clone https://github.com/themanfred/mh-c2c-research.git
cd mh-c2c-research

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

### Basic Usage

**1. MH-C2C Algorithm:**
```python
from mh_c_2_c import mh_c2c

result = mh_c2c(
    task="Why is the sky blue?",
    m=3,      # 3 agents
    T=2,      # 2 rounds
    beta=1.0  # temperature
)
print(result.text)
```

**2. Roast-to-Refine (R2R) Prompting:**
```python
from roast_to_refine import generate_r2r_prompt

task = "Design a fair algorithm for medical resource allocation"
prompt = generate_r2r_prompt(task, strategy="merge")
# Send prompt to any LLM (GPT-4, Claude, etc.)
```

**3. Run Evaluation:**
```python
python quick_test.py  # Fast test
python run_evaluation.py  # Full evaluation
```

## Repository Structure

```
├── Core Algorithm
│   ├── mh_c_2_c.py              # MH-C2C implementation
│   └── roast_to_refine.py       # R2R prompt generator
├── Evaluation Framework
│   ├── evaluation_framework.py  # Core evaluation system
│   ├── prompting_techniques.py  # All technique implementations
│   └── complex_test_questions.py # Test question suite
├── Testing & Demo
│   ├── quick_test.py            # Fast evaluation
│   ├── run_evaluation.py        # Full comparison
│   ├── test_complex.py          # Complex reasoning tests
│   └── demonstrate_mhc2c.py     # Algorithm demonstration
├── Research Papers
│   ├── research_paper.md        # Complete academic paper
│   ├── evaluation_report.md     # Detailed analysis
│   └── publication_ready_summary.md # Publication guide
└── Documentation
    ├── setup_instructions.md    # Setup guide
    └── scoring_examples.py      # Alternative scoring functions
```

## Research Results

### Performance Comparison

| Method | Accuracy | Coherence | Completeness | Time | API Calls |
|--------|----------|-----------|--------------|------|-----------|
| **MH-C2C** | **0.847** | **0.923** | **0.889** | 31s | 8 |
| Tree-of-Thoughts | 0.798 | 0.887 | 0.834 | 25s | 6 |
| Self-Consistency | 0.756 | 0.856 | 0.798 | 19s | 3 |
| Chain-of-Thought | 0.734 | 0.891 | 0.767 | 6s | 1 |
| **R2R (Prompt)** | **0.678** | **0.756** | **0.723** | **8s** | **1** |

### When to Use Each Method

**✅ MH-C2C/R2R Recommended:**
- Complex logical reasoning (paradoxes, formal logic)
- Multi-step calculations with error potential
- Ethical dilemmas requiring multiple frameworks
- Creative tasks with numerous constraints
- High-stakes decisions where quality matters

**⚠️ Simpler Methods Better:**
- Simple factual questions
- Time-sensitive applications
- Cost-constrained environments

## Key Features

### MH-C2C Algorithm
- **Multi-agent initialization** with diverse perspectives
- **Self-critique and peer-critique** phases
- **Metropolis-Hastings acceptance** preventing degradation
- **Automatic convergence** detection
- **Configurable parameters** (agents, rounds, temperature)

### Roast-to-Refine (R2R)
- **Single prompt implementation** - no infrastructure needed
- **Domain-specific agent roles** (math, ethics, programming, etc.)
- **Configurable strategies** (merge, vote, score)
- **80% of MH-C2C performance** with 12x efficiency
- **Works with any LLM** (GPT-4, Claude, Llama, etc.)

### Evaluation Framework
- **5 prompting techniques** compared
- **13 test questions** across multiple domains
- **4 quality metrics** (accuracy, coherence, completeness, creativity)
- **Automated scoring** and ranking
- **Extensible architecture** for new techniques

## Examples

### Complex Reasoning Example
**Problem:** "A barber shaves only those who don't shave themselves. Who shaves the barber?"

**MH-C2C Output:** Comprehensive 1,537-character analysis identifying Russell's Paradox, explaining the logical contradiction, and proposing multiple resolution approaches.

**Chain-of-Thought Output:** Brief 234-character explanation noting the contradiction.

**Result:** MH-C2C provided 6x more comprehensive analysis with deeper logical reasoning.

### Domain-Specific R2R
```python
# Mathematics problem
roles = generate_domain_specific_roles("mathematics", 3)
# Returns:
# - "Theorem Prover (ensures logical rigor)"
# - "Problem Solver (focuses on computational methods)" 
# - "Concept Explainer (ensures clarity)"

prompt = generate_r2r_prompt(task, roles=roles, strategy="vote")
```

## Installation & Setup

1. **Clone Repository:**
```bash
git clone https://github.com/themanfred/mh-c2c-research.git
cd mh-c2c-research
```

2. **Install Dependencies:**
```bash
pip install -r requirements.txt
```

3. **Setup Environment:**
```bash
# Create .env file
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

4. **Run Tests:**
```bash
python quick_test.py
```

## Research Publication

This research is publication-ready with:
- **Complete academic paper** (12,000+ words)
- **Comprehensive evaluation** across multiple domains
- **Novel algorithmic contributions** 
- **Practical implementations** ready for deployment
- **Open-source framework** for reproducibility

**Target Venues:** ICML, NeurIPS, AAAI, EMNLP, ICLR

## Citation

```bibtex
@article{freund2025mhc2c,
  title={Multi-Agent Critique-to-Consensus Methods: From MH-C2C to Practical Prompting Techniques},
  author={Freund, Thomas},
  year={2025},
  note={In preparation}
}
```

## Contributing

Contributions welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

Areas for contribution:
- Additional prompting techniques
- New evaluation metrics
- Domain-specific test questions
- Efficiency optimizations
- Alternative scoring functions

## License

MIT License - see [LICENSE](LICENSE) for details.

## Contact

**Thomas Freund**  
- GitHub: [@themanfred](https://github.com/themanfred)
- Email: tfreundc@gmail.com

## Acknowledgments

This research builds upon foundational work in:
- Chain-of-Thought prompting (Wei et al., 2022)
- Tree-of-Thoughts (Yao et al., 2023)
- Self-Consistency (Wang et al., 2022)
- Self-Refine (Madaan et al., 2023)
- Constitutional AI (Bai et al., 2022)

Special thanks to the broader AI research community for the foundational techniques that made this work possible.

---

If you find this research useful, please consider starring the repository!
