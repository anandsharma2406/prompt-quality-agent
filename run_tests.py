import time
from agent import PromptQualityAgent
from test_prompts import TEST_PROMPTS

agent = PromptQualityAgent(model="llama-3.3-70b-versatile")

print(f"{'#':<4} {'Label':<12} {'Score':>6}")
print("-" * 28)

for test in TEST_PROMPTS:
    result = agent.evaluate(test["prompt"])
    print(f"{test['id']:<4} {test['label']:<12} {result['final_score']:>5.1f}/10")
    time.sleep(2)

print("\nAll tests complete ✓")
