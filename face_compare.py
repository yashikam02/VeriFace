import torch
from torchvision import transforms
from facenet_pytorch import InceptionResnetV1
from utils.face_detect import extract_face
import numpy as np

resnet = InceptionResnetV1(pretrained='vggface2').eval()

transform = transforms.Compose([
    transforms.ToTensor(),
    transforms.Resize((160, 160)),
    transforms.Normalize([0.5], [0.5])
])

def get_embedding(face_tensor):
    if face_tensor.ndim == 3:
        face_tensor = face_tensor.unsqueeze(0)
    with torch.no_grad():
        embedding = resnet(face_tensor)
    return embedding[0]

def cosine_similarity(a, b):
    return torch.nn.functional.cosine_similarity(a.unsqueeze(0), b.unsqueeze(0)).item()

def compare_faces(image1_path, image2_path):
    face1 = extract_face(image1_path)
    face2 = extract_face(image2_path)
    emb1 = get_embedding(face1)
    emb2 = get_embedding(face2)
    return cosine_similarity(emb1, emb2)
