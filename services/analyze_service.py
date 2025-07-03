from utils import db
from utils.openai_client import ask_openai  # ✅ On utilise le client centralisé

async def handle_chat_analysis(file):
    # 1. Lire le contenu du fichier
    content = (await file.read()).decode('utf-8')

    # 2. Construire les messages pour le modèle
    messages = [
        {"role": "system", "content": "You are a professional customer support evaluator. Provide actionable feedback on the quality of the human agent's responses, including suggestions for improvement."},
        {"role": "user", "content": f"Please analyze the following chat transcript and provide feedback:\n\n{content}"}
    ]

    # 3. Appeler OpenAI via le client central
    feedback = ask_openai(messages)

    # 4. Enregistrer l’analyse dans MongoDB
    db.db.agent_feedbacks.insert_one({
        "transcript": content,
        "feedback": feedback
    })

    # 5. Retourner la réponse
    return {"feedback": feedback}

