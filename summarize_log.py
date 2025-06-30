import os
import google.generativeai as genai
import re

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("models/gemini-2.5-flash")

with open("live_log.txt", "r", encoding="utf-8") as f:
    log = f.read()

# Split log by Jenkins stage blocks
stages = re.split(r"(?=\\[Pipeline\\] stage)", log)
summaries = []

for i, stage in enumerate(stages):
    if not stage.strip():
        continue
    prompt = f"Summarize and suggest improvements for Jenkins pipeline stage log:\n{stage[:3000]}"
    try:
        response = model.generate_content(prompt)
        summaries.append(f"Stage {i+1} Summary:\n{response.text.strip()}\n")
    except Exception as e:
        summaries.append(f"Stage {i+1} Summary: Error - {e}\n")

summary_text = "\n---- GEMINI SUMMARIES ----\n\n" + "\n".join(summaries)

with open("summary.txt", "w", encoding="utf-8") as f:
    f.write(summary_text)

print(summary_text)
