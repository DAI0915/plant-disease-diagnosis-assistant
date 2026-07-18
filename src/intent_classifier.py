import torch

def predict_intent(question, model, tokenizer, device):
    model.eval()
    encoded = tokenizer(
        question, 
        truncation=True, 
        max_length=512, 
        return_tensors="pt"
    )
    
    input_ids = encoded["input_ids"].to(device)
    attention_mask = encoded["attention_mask"].to(device)
    with torch.no_grad():
        outputs = model(
            input_ids=input_ids, 
            attention_mask=attention_mask
        )
        
        logits = outputs.logits
        probabilities = torch.softmax(logits, dim=1)
        confidence, predicted_ids = probabilities.max(1)
    
    predicted_ids = predicted_ids.item()
    confidence = confidence.item()
    
    return {
        "intent_id": predicted_ids,
        "intent": model.config.id2label[predicted_ids],
        "confidence": confidence,
        "probabilities": probabilities.squeeze(0).cpu()
    }