from utils.langchain_client import llm
from langchain.prompts import PromptTemplate
from utils.db import db
from utils import document_reader
from datetime import datetime
from collections import defaultdict
import json

prompt = PromptTemplate.from_template("""
You are an expert customer support evaluator.

Given the following chat transcript:
{transcript}

Provide a JSON response with:

1. summary: A 1-2 sentence summary of the agent’s performance.

2. kpis: {{
   response_time: (number, in seconds),
   satisfaction_score_estimation: (number, 0 to 1),
   resolution_status: "Resolved" or "Unresolved"
}}

3. performance: {{
   response_time: (0–100),
   accuracy: (0–100),
   satisfaction: (0–100),
   resolution: (0–100),
   empathy: (0–100),
   professionalism: (0–100)
}}

4. suggestions: array of 3 objects with:
   - area: string
   - priority: "high" | "medium" | "low"
   - current: value
   - target: value
   - recommendation: 1 short sentence

Return valid JSON only. DO NOT use markdown formatting like ```json.
""")

async def handle_chat_analysis(file, agent=None):
    file_bytes = await file.read()
    try:
        content = document_reader.extract_text_from_file(file_bytes, file.filename)
    except Exception:
        content = file_bytes.decode('utf-8')

    chain = prompt | llm
    feedback_raw = chain.invoke({"transcript": content})
    feedback_text = feedback_raw.content if hasattr(feedback_raw, "content") else feedback_raw
    feedback_text = feedback_text.strip()

    if feedback_text.startswith("```json") or feedback_text.startswith("```"):
        feedback_text = feedback_text.strip("`").split("json", 1)[-1].strip()

    try:
        feedback = json.loads(feedback_text)
    except Exception:
        feedback = feedback_text

    db["agents_feedbacks"].insert_one({
        "transcript": content,
        "analysis": feedback,
        "timestamp": datetime.utcnow(),
        "agent": agent or "Unknown",
    })

    return {"feedback": feedback}

async def handle_batch_upload(files, agent=None):
    results = []
    for file in files:
        file_bytes = await file.read()
        try:
            content = document_reader.extract_text_from_file(file_bytes, file.filename)
        except Exception:
            content = file_bytes.decode('utf-8')

        chain = prompt | llm
        feedback_raw = chain.invoke({"transcript": content})
        feedback_text = feedback_raw.content if hasattr(feedback_raw, "content") else feedback_raw
        feedback_text = feedback_text.strip()
        if feedback_text.startswith("```json") or feedback_text.startswith("```"):
            feedback_text = feedback_text.strip("`").split("json", 1)[-1].strip()

        try:
            feedback = json.loads(feedback_text)
        except Exception:
            feedback = feedback_text

        db["agents_feedbacks"].insert_one({
            "transcript": content,
            "analysis": feedback,
            "timestamp": datetime.utcnow(),
            "agent": agent or "Unknown"
        })

        results.append({"filename": file.filename, "feedback": feedback})

    return {"results": results}

async def get_dashboard_data():
    chats = list(db["agents_feedbacks"].find({}))

    total_response_time = 0
    satisfaction_scores = []
    resolution_counts = defaultdict(int)
    agents_scores = defaultdict(list)
    monthly_data = defaultdict(lambda: {"response_time": [], "satisfaction": [], "resolution": []})

    for chat in chats:
        try:
            data = json.loads(chat["analysis"]) if isinstance(chat["analysis"], str) else chat["analysis"]
        except Exception:
            data = {}

        agent = chat.get("agent", "Unknown")
        timestamp = chat.get("timestamp", datetime.utcnow())
        month = timestamp.strftime("%B")

        kpis = data.get("kpis", {}) if isinstance(data, dict) else {}

        total_response_time += kpis.get("response_time", 0)
        satisfaction_scores.append(kpis.get("satisfaction_score_estimation", 0) * 20)
        resolution = kpis.get("resolution_status", "Unknown")
        resolution_counts[resolution] += 1
        agents_scores[agent].append(kpis.get("satisfaction_score_estimation", 0) * 20)

        monthly_data[month]["response_time"].append(kpis.get("response_time", 0))
        monthly_data[month]["satisfaction"].append(kpis.get("satisfaction_score_estimation", 0) * 20)
        monthly_data[month]["resolution"].append(1 if resolution == "Resolved" else 0)

    n = len(chats)
    if n == 0:
        return {"error": "No data found"}

    resolved = resolution_counts["Resolved"]
    tickets = n
    avg_response_time = round(total_response_time / n / 60, 2)
    avg_satisfaction = round(sum(satisfaction_scores) / n, 2)
    resolution_rate = round((resolved / n) * 100, 2)

    agent_scores = {agent: round(sum(scores)/len(scores), 2) for agent, scores in agents_scores.items() if scores}

    monthly_trends = {}
    for month, values in monthly_data.items():
        monthly_trends[month] = {
            "response_time": round(sum(values["response_time"])/len(values["response_time"]), 2) if values["response_time"] else 0,
            "satisfaction": round(sum(values["satisfaction"])/len(values["satisfaction"]), 2) if values["satisfaction"] else 0,
            "resolution": round(sum(values["resolution"])/len(values["resolution"]) * 100, 2) if values["resolution"] else 0
        }

    overall_performance = {
        "response_time": 80,
        "accuracy": 76,
        "satisfaction": avg_satisfaction,
        "resolution": resolution_rate,
        "empathy": 70,
        "professionalism": 82
    }

    suggestion_prompt = PromptTemplate.from_template("""
Given the following customer support KPIs:
- Average Response Time: {response_time} minutes
- Satisfaction Rate: {satisfaction}%
- Resolution Rate: {resolution}%

Generate 3 improvement suggestions with:
- area (string)
- priority (high/medium/low)
- current (value)
- target (value)
- recommendation (1 short sentence)

Return valid JSON array. DO NOT use markdown formatting.
""")

    chain = suggestion_prompt | llm
    suggestions_raw = chain.invoke({
        "response_time": avg_response_time,
        "satisfaction": avg_satisfaction,
        "resolution": resolution_rate
    })

    suggestions_text = suggestions_raw.content if hasattr(suggestions_raw, "content") else suggestions_raw
    suggestions_text = suggestions_text.strip()
    if suggestions_text.startswith("```json") or suggestions_text.startswith("```"):
        suggestions_text = suggestions_text.strip("`").split("json", 1)[-1].strip()

    try:
        suggestions = json.loads(suggestions_text)
    except Exception:
        suggestions = suggestions_text

    return {
        "global_kpis": {
            "avg_response_time": avg_response_time,
            "satisfaction_rate": avg_satisfaction,
            "tickets_resolved": tickets,
            "resolution_rate": resolution_rate
        },
        "overall_performance": overall_performance,
        "agent_scores": agent_scores,
        "monthly_trends": monthly_trends,
        "ai_suggestions": suggestions
    }


