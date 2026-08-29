from fastapi import FastAPI, UploadFile, File
from PIL import Image
import io
import json

import torch
import torch.nn as nn
from torchvision import models, transforms

from src.image_inference import predict_image
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification

from src.qa import answer_user_question


app = FastAPI(
    title="Plant-Disease-Assistant",
    version="1.0.0"
)


# -------------------------
# Device
# -------------------------

if torch.cuda.is_available():
    device = torch.device("cuda")
elif torch.backends.mps.is_available():
    device = torch.device("mps")
else:
    device = torch.device("cpu")


# -------------------------
# Load class names
# -------------------------

with open("data/class_names.json", "r") as f:
    class_names = json.load(f)

num_classes = len(class_names)

with open("data/plantvillage_disease_database.json", "r") as f:
    disease_database = json.load(f)

# -------------------------
# Load ResNet18
# -------------------------

model = models.resnet18(weights=None)

model.fc = nn.Linear(
    model.fc.in_features,
    num_classes
)

state_dict = torch.load(
    "models/resnet18_best.pth",
    map_location=device
)

model.load_state_dict(state_dict)

model = model.to(device)
model.eval()


# -------------------------
# Load DistilBERT
# -------------------------


intent_model_path = "models/intent_classifier"

tokenizer = AutoTokenizer.from_pretrained(intent_model_path)

bert_model = AutoModelForSequenceClassification.from_pretrained(
    intent_model_path
)

bert_model = bert_model.to(device)
bert_model.eval()

# -------------------------
# Image transform
# -------------------------

transform = transforms.Compose([
    transforms.Resize(257),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])


class AskRequest(BaseModel):
    class_name: str
    question: str

# -------------------------
# Endpoints
# -------------------------



@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    contents = await file.read()

    image = Image.open(
        io.BytesIO(contents)
    ).convert("RGB")

    result = predict_image(
        image=image,
        model=model,
        class_names=class_names,
        device=device,
        transform=transform
    )

    return result


@app.post("/ask")
def ask(request: AskRequest):
    image_result = {
        "class_name": request.class_name
    }

    result = answer_user_question(
        question=request.question,
        image_result=image_result,
        bert_model=bert_model,
        tokenizer=tokenizer,
        disease_database=disease_database,
        device=device
    )

    return result