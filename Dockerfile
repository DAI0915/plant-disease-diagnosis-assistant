FROM python:3.11-slim

WORKDIR /app

COPY requirements-api.txt .

RUN pip install --no-cache-dir \
    --index-url https://download.pytorch.org/whl/cpu \
    torch torchvision

RUN pip install --no-cache-dir \
    transformers Pillow fastapi uvicorn python-multipart

COPY app ./app
COPY src ./src
COPY data ./data
COPY models/resnet18_best.pth ./models/resnet18_best.pth
COPY models/intent_classifier ./models/intent_classifier

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]