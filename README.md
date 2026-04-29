[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/anandsharma2406/prompt-quality-agent/blob/main/notebook.ipynb)
# prompt-quality-agent
A LangChain agent that scores prompt quality across 5 criteria using Groq
# 🧠 Prompt Quality Scoring Agent

A LangChain agent that evaluates any LLM prompt across **5 quality criteria**,
assigns scores, and provides actionable improvement suggestions.
Powered by **Groq** (free, no billing required).

---

## 🎯 What It Does

| Input | Output |
|-------|--------|
| Any text prompt | Final score (0–10) |
| | Per-criterion scores |
| | Explanation of evaluation |
| | 2–3 improvement suggestions |

---

## 📊 Scoring Criteria

| # | Criterion | What It Checks |
|---|-----------|----------------|
| 1 | **Clarity** | Is the goal clear and unambiguous? |
| 2 | **Specificity** | Are sufficient details provided? |
| 3 | **Context** | Is background or audience mentioned? |
| 4 | **Output Format** | Is format, tone, or length specified? |
| 5 | **Persona** | Is a specific AI role assigned? |

**Final Score** = Average of all five criteria.

---

## 🚀 Setup

### 1. Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/prompt-quality-agent.git
cd prompt-quality-agent
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Get a free Groq API key
- Go to https://console.groq.com/keys
- Sign up for free (no credit card needed)
- Create an API key and copy it

### 4. Set your API key
```bash
export GROQ_API_KEY="gsk_..."
```

---

## 💻 Usage

### Evaluate a single prompt (Python)
```python
from agent import PromptQualityAgent

agent = PromptQualityAgent()
prompt = "Write something about dogs."
result = agent.evaluate(prompt)
print(agent.format_report(prompt, result))
```

### Run all 10 test prompts
```bash
python run_tests.py
```

---

## ☁️ Run on Google Colab

1. Open [colab.research.google.com](https://colab.research.google.com) → New notebook
2. Add `GROQ_API_KEY` to Colab Secrets (🔑 icon in left sidebar)
3. Run these cells in order:

```python
# Cell 1 — Install
!pip install langchain langchain-groq langchain-core groq pydantic -q

# Cell 2 — Load key
from google.colab import userdata
import os
os.environ["GROQ_API_KEY"] = userdata.get("GROQ_API_KEY")

# Cell 3 — Clone repo
!git clone https://github.com/YOUR_USERNAME/prompt-quality-agent.git
%cd prompt-quality-agent

# Cell 4 — Run
from agent import PromptQualityAgent
agent = PromptQualityAgent()
prompt = "Write something about dogs."
result = agent.evaluate(prompt)
print(agent.format_report(prompt, result))
```

---

## 🧪 Test Results

| # | Label | Clarity | Specificity | Context | Format | Persona | Final |
|---|-------|---------|-------------|---------|--------|---------|-------|
| 1 | Very Poor  | 3.0 | 1.0 | 0.0 | 0.0 | 0.0 | **0.8** |
| 2 | Poor       | 4.0 | 2.0 | 1.0 | 1.0 | 0.0 | **1.6** |
| 3 | Poor       | 4.0 | 2.0 | 1.0 | 1.0 | 0.0 | **1.6** |
| 4 | Average    | 6.0 | 5.0 | 3.0 | 5.0 | 0.0 | **3.8** |
| 5 | Average    | 7.0 | 5.0 | 4.0 | 3.0 | 0.0 | **3.8** |
| 6 | Good       | 7.0 | 6.0 | 6.0 | 5.0 | 7.0 | **6.2** |
| 7 | Good       | 8.0 | 7.0 | 6.0 | 8.0 | 2.0 | **6.2** |
| 8 | Very Good  | 8.0 | 8.0 | 8.0 | 8.0 | 8.0 | **8.0** |
| 9 | Excellent  | 9.0 | 9.0 | 8.0 | 9.0 | 9.0 | **8.8** |
|10 | Perfect    |10.0 |10.0 |10.0 |10.0 |10.0 |**10.0** |

---

## 🏗️ Project Structure
prompt-quality-agent/
├── agent.py          # Core PromptQualityAgent class
├── test_prompts.py   # 10 test prompts
├── run_tests.py      # Batch test runner
├── requirements.txt  # Dependencies
└── README.md

---

## 🔧 Available Groq Models

| Model | Speed | Quality |
|-------|-------|---------|
| `llama-3.3-70b-versatile` | Fast | Best (default) |
| `llama-3.1-8b-instant` | Fastest | Good |
| `mixtral-8x7b-32768` | Fast | Alternative |

---

## 📄 License
