import io
import os
import numpy as np
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
from tensorflow.keras.models import load_model
from PIL import Image
from skimage import filters
import uvicorn

# Configuración
IMAGE_SIZE = (128, 128)
NORMALIZAR = False
MODEL_PATH = os.getenv("MODEL_PATH")

if MODEL_PATH is None:
    raise ValueError("La variable de entorno MODEL_PATH no está definida.")

# Inicializar FastAPI
app = FastAPI(title="Pneumonia Detection API")

# Cargar modelo
model = load_model(MODEL_PATH)

def preprocess_image(content_bytes):
    try:
        image = Image.open(io.BytesIO(content_bytes)).convert("L")
        image = image.resize(IMAGE_SIZE)

        image_array = np.asarray(image, dtype=np.float32) / 255.0

        if NORMALIZAR:
            mean = image_array.mean()
            std = image_array.std()
            if std > 0:
                image_array = (image_array - mean) / std

        return image_array.reshape(-1)
    except Exception as e:
        print(f"Error procesando imagen: {e}")
        return None

def reconstruir_imagen(row):
    return row.astype(np.float32).reshape(IMAGE_SIZE)

def aplicar_filtros(imagen_2d):
    if imagen_2d.max() > 1.0:
        imagen_2d = imagen_2d / 255.0

    sobel_x = filters.sobel_h(imagen_2d)
    sobel_y = filters.sobel_v(imagen_2d)
    laplacian = filters.laplace(imagen_2d)
    scharr = filters.scharr(imagen_2d)
    gaussian = filters.gaussian(imagen_2d, sigma=1)

    return np.stack([imagen_2d, sobel_x, sobel_y, laplacian, scharr, gaussian], axis=-1)

@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    if not file.filename.lower().endswith((".jpeg", ".jpg")):
        return JSONResponse(status_code=400, content={"error": "Solo se permiten imágenes .jpeg o .jpg"})

    try:
        content = await file.read()
        pixels = preprocess_image(content)        
        img_2d = reconstruir_imagen(pixels)
        img_multi = aplicar_filtros(img_2d)
        img_multi = np.expand_dims(img_multi, axis=0)

        prediction = model.predict(img_multi)
        probs = prediction[0]
        label_index = int(np.argmax(probs))
        label = "NORMAL" if label_index == 0 else "PNEUMONIA"
        probability = float(probs[label_index])

        return {
            "filename": file.filename,
            "prediction": label,
            "probability": round(probability, 4)
        }

    except Exception as e:
        print(f"[ERROR] Predicción fallida: {e}")
        return JSONResponse(status_code=500, content={"error": str(e)})

if __name__ == "__main__":
    uvicorn.run("deploy:app", host="0.0.0.0", port=8000, reload=False)