# Plant Disease Diagnosis Assistant

## Overview

This project is a plant disease diagnosis assistant that classifies plant leaf images and provides explanation-based responses about symptoms, causes, treatment, and prevention.

The system combines image classification models with a structured plant disease information database and a question intent classifier.

## Features

- Plant leaf disease classification from images
- Custom CNN model training
- Transfer learning with ResNet18 and MobileNetV3
- Hyperparameter tuning with Optuna
- Model comparison using accuracy, macro F1 score, model size, and inference latency
- Disease explanation database including symptoms, causes, treatment, and prevention
- Question intent classification using DistilBERT
- Intent-aware question answering using DistilBERT and a structured disease database
- REST API for model serving using FastAPI
- Containerized deployment using Docker

## Dataset

This project uses the PlantVillage dataset.

The raw image dataset is not included in this repository because of its size.

Expected dataset directory:

```text
PlantVillage-Dataset/raw/color
```

The dataset contains plant leaf images across multiple plant species and disease classes.

## Project Structure

```text
plant-disease-diagnosis-assistant/
├── README.md
├── requirements.txt
├── .dockerignore
├── Dockerfile
├── .gitignore
├── demo.py
├── app/
│   ├── __init__.py
│   └── main.py
├── notebooks/
│   └── Plant Health AI Assistant.ipynb
├── src/
│   ├── image_inference.py
│   ├── diagnosis.py
│   ├── intent_classifier.py
│   ├── qa.py
│   └── models.py
├── data/
│   ├── plantvillage_disease_database.json
│   ├── plant_intent_dataset_500.csv
│   └── class_names.json
├── results/
│   ├── loss.png
│   ├── accuracy.png
│   ├── bert_intent_results.csv
│   ├── flexible_cnn_loss.png 
│   ├── image_model_comparison.csv
│   ├── mobilenetv3_loss.png
│   ├── resnet18_loss.png
│   └── sample_qa_output.md
├── logs/
│   └── training_log.csv
├── sample_images/
│   └── sample_leaf.jpg
└── models/
    ├── flexible_cnn_best.pth
    ├── resnet18_best.pth
    ├── mobilenet_v3_best.pth
    └── intent_classifier/
```
## Models

This project compares the following image classification models.

### FlexibleCNN

FlexibleCNN is a custom convolutional neural network with tunable architecture parameters, including:

- number of convolutional layers
- number of filters
- kernel sizes
- dropout rate
- fully connected layer size

### ResNet18

ResNet18 is used as a pretrained transfer learning model and fine-tuned for plant disease classification.

### MobileNetV3

MobileNetV3 is used as a lightweight pretrained transfer learning model.

It is included as a smaller and faster model candidate for efficient inference.

## Question Answering Pipeline

The assistant answers user questions using the following pipeline:

```text
Leaf image
↓
Image classification model
↓
Predicted plant disease
↓
Disease information database
↓
User question
↓
DistilBERT intent classifier
↓
Answer about symptoms, cause, treatment, prevention, or general diagnosis
```

The question intent classifier predicts one of the following categories:

```text
symptoms
cause
treatment
prevention
general
```

## API

The project provides a REST API built with FastAPI for plant disease
classification and intent-aware question answering.

### Endpoints

#### Health Check

```http
GET /health
```

Returns the status of the API.

#### Disease Prediction

```http
POST /predict
```

Upload a plant leaf image to receive the predicted disease class,
confidence score, and class probabilities.

Example response:

```json
{
  "class_index": 30,
  "class_name": "Tomato___Late_blight",
  "confidence": 0.99,
  "probabilities": [0.001, 0.002, 0.997, ....]
}
```

#### Question Answering
The class_name returned by /predict can be passed to /ask together with a user question.

```http
POST /ask
```

Example request:

```json
{
  "class_name": "Tomato___Late_blight",
  "question": "How can I prevent this disease?"
}
```

Example response:

```json
{
  "question": "How can I prevent this disease?",
  "intent": "prevention",
  "intent_confidence": 0.98,
  "answer": "- Use healthy transplants\n- Destroy volunteer tomatoes and potatoes\n- Monitor disease alerts"
}
```


## Example Output

Example question:

```text
How can I treat it?
```

Example answer:

```text
Prediction: Tomato - Early blight

Recommended actions:
- Remove infected lower leaves
- Mulch and improve airflow
- Use local fungicide guidance

Note: Image-based classification is not a definitive diagnosis. Confirm important cases with a local plant-health professional.
```

## Results

### Image Classification Results

| Model | Test Accuracy | Macro Recall | Macro F1 | Model Size (MB) | Mean Latency (ms) |
|---|---:|---:|---:|---:|---:|
| FlexibleCNN2 | 96.15% |  96.15% | 96.44% | 1.025886 | 1.706617 |
| ResNet18 Stage2 | 99.39% | 99.39% | 99.44% | 42.783763 | 6.037270 |
| MobileNetV3 Stage2 | 97.45% | 97.45% | 97.64% | 6.064086 | 6.337007 |

### Intent Classification Results

| Model | Test Accuracy | Test Precision | Test Recall | Test F1 |
|---|---:|---:|---:|---:|
| DistilBERT | 94.92% | 95.38% | 95.00% | 94.85% |

### Training Curves

Training and validation loss curves are saved in:

```text
results/loss.png
```

Validation accuracy curves are saved in:

```text
results/accuracy.png
```

## Model Weights

Saved model weights are not included in this repository because the `models/` directory is ignored by `.gitignore`.

To reproduce the results, run the training notebook or place trained weights under the `models/` directory.

Expected local structure:

```text
models/
├── flexible_cnn_best.pth
├── resnet18_best.pth
├── mobilenet_v3_best.pth
└── intent_classifier/
```


## How to Run

### 1. Clone the repository

```bash
git clone https://github.com/DAI0915/plant-disease-diagnosis-assistant.git
cd plant-disease-diagnosis-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Prepare the dataset

The raw PlantVillage dataset is not included in this repository.

Download the PlantVillage dataset and place it in the following local directory:

```text
PlantVillage-Dataset/
└── raw/
    └── color/
        ├── Apple___Apple_scab/
        ├── Grape___Black_rot/
        ├── Tomato___Early_blight/
        └── ...
```

The notebook expects the dataset path to be:

```text
PlantVillage-Dataset/raw/color
```

### 4. Prepare model weights

Saved model weights are not included in this repository because the `models/` directory is ignored by `.gitignore`.

To reproduce the results, either run the training notebook or place trained weights under the `models/` directory.

Expected local structure:

```text
models/
├── flexible_cnn_best.pth
├── resnet18_best.pth
├── mobilenet_v3_best.pth
└── intent_classifier/
```

If you want to train models from scratch, set the execution flags in the notebook as follows:

```python
RUN_TRAINING = True
LOAD_SAVED_MODELS = False
```

If you want to skip training and use saved models, set:

```python
RUN_TRAINING = False
LOAD_SAVED_MODELS = True
```

### 5. Run the experiment notebook

Open the main notebook:

```text
notebooks/Plant Health AI Assistant.ipynb
```

The notebook includes:

- dataset loading and preprocessing
- train / validation / test split
- custom FlexibleCNN training
- Optuna-based hyperparameter tuning
- ResNet18 and MobileNetV3 fine-tuning
- model evaluation and efficiency comparison
- disease database construction
- DistilBERT intent classification
- diagnosis and question answering experiments
- saving results under `results/` and `logs/`

### 6. Prepare a sample image for the demo

Place a leaf image under the `sample_images/` directory.

For example, if you have the PlantVillage dataset locally, you can copy one image as follows:

```bash
mkdir -p sample_images

cp "PlantVillage-Dataset/raw/color/Grape___Black_rot/0e143d33-adc0-41af-92e2-d0bb712d7b72___FAM_B.Rot 5047.JPG" sample_images/sample_leaf.jpg
```

Expected local structure:

```text
sample_images/
└── sample_leaf.jpg
```

### 7. Run the demo script

After preparing the saved model weights and a sample image, run:

```bash
python demo.py --image sample_images/sample_leaf.jpg --question "How can I treat it?"
```

Example output:

```text
Image classification result
Predicted class: Grape___Black_rot
Confidence: ...

Question
How can I treat it?

Predicted intent
treatment

Answer
- Remove mummified berries and infected debris
- Improve canopy airflow
- Follow local fungicide timing guidance
```

### 8. Run the FastAPI server

After preparing the required model weights, start the API server:

```bash
uvicorn app.main:app --reload
```

Open the interactive API documentation at:

```text
http://127.0.0.1:8000/docs
```

The API provides:

```text
GET  /health
POST /predict
POST /ask
```

### 9. Run with Docker
Before building the Docker image, place the required trained model weights under:

```text
models/
├── resnet18_best.pth
└── intent_classifier/
```


The API can also be run inside a Docker container.

Build the Docker image:

```bash
docker build -t plant-disease-api .
```

Run the container:

```bash
docker run --rm -p 8000:8000 plant-disease-api
```

Then open:

```text
http://127.0.0.1:8000/docs
```

The Docker image packages the application code, Python dependencies,
PyTorch models, FastAPI server, and disease database into a reproducible
runtime environment.

## Main Files

### `notebooks/Plant Health AI Assistant.ipynb`

Main experiment notebook containing model training, evaluation, and analysis.

### `src/image_inference.py`

Image inference functions.

### `src/diagnosis.py`

Functions for loading disease information and generating diagnosis explanations.

### `src/intent_classifier.py`

Question intent classification using DistilBERT.

### `src/qa.py`

Question answering logic based on predicted disease and user intent.

### `src/models.py`

Model definitions and fine-tuning utilities.

### `app/main.py`

FastAPI application exposing REST endpoints for health checks, image-based
disease prediction, and intent-aware question answering.

### `Dockerfile`

Defines the containerized runtime environment for serving the FastAPI
application and trained ML models.

## Limitations

This project is for educational and experimental purposes.

The predictions are based only on image classification and should not be treated as a definitive professional diagnosis.

For serious plant disease cases, users should consult a local extension service, agricultural specialist, or plant-health professional.

## Future Improvements

- Add a web interface using Gradio or Streamlit
- Improve robustness on real-world leaf images outside the PlantVillage dataset
- Add top-3 prediction display
- Add confidence-based warning messages
- Improve question answering with more diverse user questions
- Add model weight download instructions