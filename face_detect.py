from facenet_pytorch import MTCNN
from PIL import Image
import numpy as np

mtcnn = MTCNN(image_size=160, margin=0)

def extract_face(image_path):
    img = Image.open(image_path).convert("RGB")
    face_tensor = mtcnn(img)
    
    if face_tensor is None:
        raise ValueError("No face detected in image.")

    return face_tensor