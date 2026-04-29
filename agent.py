import json, re, os
from typing import Optional
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage

SYSTEM_PROMPT = """You are an expert prompt engineer and evaluator. Analyze the given prompt and score it across 5 quality criteria.

Scoring Criteria:
1. clarity (0-10): Is the goal clear and unambiguous?
2. specificity (0-10): Are sufficient details and requirements provided?
3. context (0-10): Is background info, audience, or use case mentioned?
4. output_format (0-10): Is expected format, tone, or length specified?
5. persona (0-10): Is a specific AI role or persona assigned?

Respond ONLY with a valid JSON object. No markdown, no backticks, no explanation outside the JSON.

{
  "criteria_scores": {
    "clarity": <float 0-10>,
    "specificity": <float 0-10>,
    "context": <float 0-10>,
    "output_format": <float 0-10>,
    "persona": <float 0-10>
  },
  "final_score": <average of the 5 scores>,
  "explanation": "<2-3 sentence summary>",
  "suggestions": ["<suggestion 1>", "<suggestion 2>", "<suggestion 3>"]
}"""


class PromptQualityAgent:
    def __init__(self, model="llama-3.3-70b-versatile", api_key=None):
        self.llm = ChatGroq(
            model=model,
            groq_api_key=api_key or os.environ.get("GROQ_API_KEY"),
            temperature=0.1,
        )

    def _extract_text(self, content):
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            return " ".join(
                block.get("text", "") if isinstance(block, dict) else str(block)
                for block in content
            )
        return str(content)

    def evaluate(self, prompt_text):
        messages = [
            SystemMessage(content=SYSTEM_PROMPT),
            HumanMessage(content="Evaluate this prompt:\n\n---\n" + prompt_text + "\n---"),
        ]
        response = self.llm.invoke(messages)

        raw_text = self._extract_text(response.content)
        raw_text = re.sub(r"```(?:json)?", "", raw_text).strip().rstrip("`").strip()

        try:
            result = json.loads(raw_text)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw_text, re.DOTALL)
            if match:
                result = json.loads(match.group())
            else:
                raise ValueError("Could not parse JSON:\n" + raw_text[:500])

        s = result["criteria_scores"]
        result["final_score"] = round(
            (s["clarity"] + s["specificity"] + s["context"] +
             s["output_format"] + s["persona"]) / 5, 2
        )
        return result

    def format_report(self, prompt_text, result):
        scores = result["criteria_scores"]
        bar = lambda s: "█" * int(s) + "░" * (10 - int(s))
        lines = []
        lines.append("╔══════════════════════════════════════════════════════╗")
        lines.append("║         PROMPT QUALITY EVALUATION REPORT             ║")
        lines.append("╚══════════════════════════════════════════════════════╝")
        lines.append("")
        lines.append("📝 PROMPT:")
        lines.append(prompt_text[:200] + ("..." if len(prompt_text) > 200 else ""))
        lines.append("")
        lines.append("──────────────────────────────────────────────────────")
        lines.append(" CRITERIA SCORES")
        lines.append("──────────────────────────────────────────────────────")
        lines.append(" Clarity          [" + bar(scores['clarity'])       + "] " + f"{scores['clarity']:4.1f}/10")
        lines.append(" Specificity      [" + bar(scores['specificity'])   + "] " + f"{scores['specificity']:4.1f}/10")
        lines.append(" Context          [" + bar(scores['context'])       + "] " + f"{scores['context']:4.1f}/10")
        lines.append(" Output Format    [" + bar(scores['output_format']) + "] " + f"{scores['output_format']:4.1f}/10")
        lines.append(" Persona Defined  [" + bar(scores['persona'])       + "] " + f"{scores['persona']:4.1f}/10")
        lines.append("──────────────────────────────────────────────────────")
        lines.append(" FINAL SCORE      [" + bar(result['final_score'])   + "] " + f"{result['final_score']:4.1f}/10")
        lines.append("══════════════════════════════════════════════════════")
        lines.append("")
        lines.append("💡 EXPLANATION:")
        lines.append(result['explanation'])
        lines.append("")
        lines.append("🔧 IMPROVEMENT SUGGESTIONS:")
        for i, s in enumerate(result["suggestions"], 1):
            lines.append("  " + str(i) + ". " + s)
        return "\n".join(lines)
