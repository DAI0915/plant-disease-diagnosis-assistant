from pathlib import Path
import argparse
import json

import torch
import torch.nn as nn
from torchvision import models as tv_models
from torchvision import transforms
from transformers import AutoTokenizer, DistilBertForSequenceClassification

from src.image_inference import predict_image
from src.diagnosis import load_disease_database
from src.qa import answer_user_question


def load_class_names(path="data/class_names.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_resnet18_model(model_path, num_classes, device):
    model = tv_models.resnet18(weights=None)
    model.fc = nn.Linear(model.fc.in_features, num_classes)

    model.load_state_dict(
        torch.load(model_path, map_location=device)
    )

    model.to(device)
    model.eval()

    return model


def load_intent_classifier(model_dir, device):
    tokenizer = AutoTokenizer.from_pretrained(model_dir)

    model = DistilBertForSequenceClassification.from_pretrained(
        model_dir
    ).to(device)

    model.eval()

    return model, tokenizer


def main():
    parser = argparse.ArgumentParser(
        description="Run plant disease diagnosis and question answering demo."
    )

    parser.add_argument(
        "--image",
        type=str,
        required=True,
        help="Path to a leaf image."
    )

    parser.add_argument(
        "--question",
        type=str,
        default="How can I treat it?",
        help="User question about the predicted disease."
    )

    args = parser.parse_args()

    device = torch.device(
        "mps" if torch.backends.mps.is_available()
        else "cuda" if torch.cuda.is_available()
        else "cpu"
    )

    class_names = load_class_names()
    disease_database = load_disease_database(
        "data/plantvillage_disease_database.json"
    )

    image_transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    image_model_path = Path("models/resnet18_best.pth")
    intent_model_dir = Path("models/intent_classifier")

    if not image_model_path.exists():
        raise FileNotFoundError(
            "models/resnet18_best.pth was not found. "
            "Train the model first or place saved weights under models/."
        )

    if not intent_model_dir.exists():
        raise FileNotFoundError(
            "models/intent_classifier was not found. "
            "Train the intent classifier first or place saved weights under models/."
        )

    image_model = load_resnet18_model(
        model_path=image_model_path,
        num_classes=len(class_names),
        device=device
    )

    intent_model, tokenizer = load_intent_classifier(
        model_dir=intent_model_dir,
        device=device
    )

    image_result = predict_image(
        image=args.image,
        model=image_model,
        class_names=class_names,
        device=device,
        transform=image_transform
    )

    response = answer_user_question(
        question=args.question,
        image_result=image_result,
        bert_model=intent_model,
        tokenizer=tokenizer,
        disease_database=disease_database,
        device=device
    )

    print("Device:", device)
    print("\nImage classification result")
    print("Predicted class:", image_result["class_name"])
    print(f'Confidence: {image_result["confidence"] * 100:.2f}%')

    print("\nQuestion")
    print(args.question)

    print("\nPredicted intent")
    print(response["intent"])

    print("\nAnswer")
    print(response["answer"])


if __name__ == "__main__":
    main()