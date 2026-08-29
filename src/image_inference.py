import torch
from PIL import Image
from pathlib import Path

def predict_image(image, model, class_names, device, transform=None):
    """
    Predict a plant disease class from an image.

    Args:
        image: image path, PIL image, or already-transformed torch.Tensor
        model: trained image classification model
        class_names: list of class names
        device: torch device
        transform: torchvision transform used for PIL images

    Returns:
        dict containing class index, class name, confidence, and probabilities
    """

    model.eval()

    if isinstance(image, (str, Path)):
        image = Image.open(image).convert("RGB")
        if transform is None:
            raise ValueError("transform must be provided when image is a file path.")
        image_tensor = transform(image)

    elif isinstance(image, Image.Image):
        image = image.convert("RGB")
        if transform is None:
            raise ValueError("transform must be provided when image is a PIL image.")
        image_tensor = transform(image)

    elif torch.is_tensor(image):
        image_tensor = image

    else:
        raise TypeError("image must be a file path, PIL image, or torch.Tensor.")

    if image_tensor.dim() == 3:
        image_tensor = image_tensor.unsqueeze(0)

    image_tensor = image_tensor.to(device)

    with torch.inference_mode():
        logits = model(image_tensor)
        probabilities = torch.softmax(logits, dim=1)
        confidence, predicted_idx = probabilities.max(1)

    predicted_idx = predicted_idx.item()
    confidence = confidence.item()

    return {
        "class_index": predicted_idx,
        "class_name": class_names[predicted_idx],
        "confidence": confidence,
        "probabilities": probabilities.squeeze(0).cpu().tolist()
    }
