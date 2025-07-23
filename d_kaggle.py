import os
import subprocess
import zipfile
import csv

# Configurações
KAGGLE_DATASET = "moltean/fruits"           # <-- Modifique aqui
BUCKET_NAME = "dataset_download"            # <-- Modifique aqui
KAGGLE_DIR = os.path.expanduser("~/.kaggle")
LOCAL_DIR = "fruits"
CSV_PATH = "dataset.csv"
KAGGLE_JSON = "kaggle.json"

# Configurar Kaggle API
print("📦 Configurando Kaggle API...")
os.makedirs(KAGGLE_DIR, exist_ok=True)
subprocess.run(["cp", KAGGLE_JSON, os.path.join(KAGGLE_DIR, "kaggle.json")])
os.chmod(os.path.join(KAGGLE_DIR, "kaggle.json"), 0o600)

# Baixar o dataset
print(f"⬇️ Baixando dataset {KAGGLE_DATASET}...")
subprocess.run(["kaggle", "datasets", "download", "-d", KAGGLE_DATASET])

# Extrair
print("📂 Extraindo fruits.zip...")
with zipfile.ZipFile("fruits.zip", 'r') as zip_ref:
    zip_ref.extractall(LOCAL_DIR)

# Enviar imagens ao GCS (modo recursivo e paralelo)
print("☁️ Enviando imagens ao GCS...")
subprocess.run(["gsutil", "-m", "cp", "-r",
                os.path.join(LOCAL_DIR, "fruits-360/Training/*"),
                f"gs://{BUCKET_NAME}/images/"])

# Gerar CSV
print("📝 Gerando arquivo CSV...")
with open(CSV_PATH, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["SET", "IMAGE_PATH", "LABEL"])
    train_path = os.path.join(LOCAL_DIR, "fruits-360/Training")
    for label in os.listdir(train_path):
        class_dir = os.path.join(train_path, label)
        if os.path.isdir(class_dir):
            for image in os.listdir(class_dir):
                image_path = f"gs://{BUCKET_NAME}/images/{label}/{image}"
                writer.writerow(["TRAIN", image_path, label])

# Enviar CSV ao GCS
print("☁️ Enviando CSV ao GCS...")
subprocess.run(["gsutil", "cp", CSV_PATH, f"gs://{BUCKET_NAME}/"])

print("✅ Processo finalizado com sucesso.")
