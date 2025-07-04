from utils import db
from utils.openai_client import ask_openai  

async def handle_chat_analysis(file):
   
    content = (await file.read()).decode('utf-8')

   
    messages = [
        {"role": "system", "content": "You are a professional customer support evaluator. Provide actionable feedback on the quality of the human agent's responses, including suggestions for improvement."},
        {"role": "user", "content": f"Please analyze the following chat transcript and provide feedback:\n\n{content}"}
    ]

   
    feedback = ask_openai(messages)

    
    db.db.agent_feedbacks.insert_one({
        "transcript": content,
        "feedback": feedback
    })

    # 5. Retourner la réponse
    return {"feedback": feedback}

