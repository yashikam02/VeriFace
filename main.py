import streamlit as st
from PIL import Image
import io
import cv2
import numpy as np

from utils.ocr import extract_text_and_dob
from utils.age_check import is_above_18
from utils.face_compare import compare_faces

st.title("🛂 Aadhar Identity & Age Verification")

# Upload
aadhar_file = st.file_uploader("📄 Upload Aadhar Image", type=["jpg", "jpeg", "png"])
selfie_file = st.camera_input("📷 Take a Selfie")

#Quality check
def is_blurry(image_pil, threshold=100.0):
    gray = np.array(image_pil.convert("L"))
    variance = cv2.Laplacian(gray, cv2.CV_64F).var()
    return variance < threshold, variance

def is_too_dark(image_pil, brightness_threshold=50):
    gray = np.array(image_pil.convert("L"))
    brightness = np.mean(gray)
    return brightness < brightness_threshold, brightness


if aadhar_file and selfie_file:
    with open("aadhar.jpg", "wb") as f:
        f.write(aadhar_file.read())

    selfie_bytes = selfie_file.getvalue()
    selfie_img = Image.open(io.BytesIO(selfie_bytes)).convert("RGB")
    selfie_img.save("selfie.jpg")

    # Feedback
    blurry, sharpness = is_blurry(selfie_img)
    dark, brightness = is_too_dark(selfie_img)

    if blurry:
        st.warning(f"📷 The selfie looks a bit blurry (sharpness: {sharpness:.2f}). Try holding the camera steady.")
    if dark:
        st.warning(f"💡 The selfie looks dark (brightness: {brightness:.2f}). Try better lighting.")

    #DOB Check
    text, dob = extract_text_and_dob("aadhar.jpg")
    if dob:
        st.success(f"🗓️ Extracted DOB: {dob}")
        if is_above_18(dob):
            st.success("✅ Age is 18+")
        else:
            st.error("❌ Age is below 18")
    else:
        st.error("⚠️ Date of Birth could not be detected.")

    #Face Matchi and confidence check
    try:
        confidence = compare_faces("aadhar.jpg", "selfie.jpg")
        st.metric("Face Match Confidence", f"{confidence:.2f}")
        if confidence > 0.6:
            st.success("✅ Faces Match")
        else:
            st.error("❌ Faces Do Not Match")
    except Exception as e:
        st.error(f"⚠️ Face comparison failed: {e}")

else:
    st.info("📥 Please upload an Aadhar image and take a selfie to begin.")

