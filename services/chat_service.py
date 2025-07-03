from utils import db, qdrant_client, embedding_utils
from utils.openai_client import ask_openai  # Utilisation de ton client centralisé

async def handle_chat(question: str):
    # 1. Générer l'embedding de la question
    question_embedding = embedding_utils.generate_embedding(question)
    
    # 2. Recherche dans Qdrant les documents les plus pertinents
    search_result = qdrant_client.qdrant.search(
        collection_name="documents",
        query_vector=question_embedding,
        limit=3
    )

    # 3. Construire le contexte à partir des documents trouvés
    context = " ".join([hit.payload.get("filename", "") for hit in search_result])

    # 4. Construire les messages pour l'IA
    messages = [
        {"role": "system", "content": "You are an AI assistant helping users based on uploaded documents."},
        {"role": "user", "content": f"Context: {context}\nQuestion: {question}"}
    ]

    # 5. Appel à OpenAI via ton client
    answer = ask_openai(messages)

    # 6. Sauvegarder dans MongoDB
    db.db.chat_histories.insert_one({
        "question": question,
        "answer": answer,
        "context": context
    })

    # 7. Retourner la réponse
    return {"answer": answer}

