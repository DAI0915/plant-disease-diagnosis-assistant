from src.intent_classifier import predict_intent

def answer_user_question(question, image_result, bert_model, tokenizer, disease_database, device):
    intent_result = predict_intent(
        question=question,
        model=bert_model,
        tokenizer=tokenizer,
        device=device
    )

    class_name = image_result["class_name"]
    intent = intent_result["intent"]

    disease_info = disease_database[class_name]

    if intent == "general":
        answer = (
            f"The predicted condition is "
            f"{disease_info['condition']}. "
            f"{disease_info['warning']}"
        )
    else:
        answer = disease_info[intent]

        if isinstance(answer, list):
            answer = "\n".join(
                f"- {item}"
                for item in answer
            )

    return {
        "question": question,
        "intent": intent,
        "intent_confidence": intent_result["confidence"],
        "answer": answer
    }