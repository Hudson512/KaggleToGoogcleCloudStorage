#!/bin/bash
# Uso: ./download_from_kaggle.sh moltean/fruits meu-projeto-gcp

DATASET_NAME=$1
PROJECT_ID=$2
BUCKET_NAME="${PROJECT_ID}-dataset"

# Instalar dependências
sudo apt update && sudo apt install -y python3 python3-pip unzip wget
pip3 install --upgrade kaggle

# Configurar Kaggle API
mkdir -p ~/.kaggle
cp kaggle.json ~/.kaggle/
chmod 600 ~/.kaggle/kaggle.json

# Baixar o dataset
echo "⬇️ Baixando dataset $DATASET_NAME ..."
kaggle datasets download -d $DATASET_NAME

# Extrair os arquivos
echo "📂 Extraindo arquivos..."
unzip -q fruits.zip -d fruits

# Criar bucket no GCS
echo "☁️ Criando bucket gs://$BUCKET_NAME ..."
gcloud config set project $PROJECT_ID
gsutil mb -p $PROJECT_ID gs://$BUCKET_NAME/

# Enviar imagens
echo "📤 Enviando imagens ao GCS..."
gsutil -m cp -r fruits/fruits-360/Training/* gs://$BUCKET_NAME/images/

# Gerar CSV
echo "📝 Gerando CSV localmente..."
python3 <<EOF
import csv, os
bucket = "$BUCKET_NAME"
path = "dataset.csv"
with open(path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["SET", "IMAGE_PATH", "LABEL"])
    base = "fruits/fruits-360/Training"
    for label in os.listdir(base):
        folder = os.path.join(base, label)
        if os.path.isdir(folder):
            for img in os.listdir(folder):
                w.writerow(["TRAIN", f"gs://{bucket}/images/{label}/{img}", label])
EOF

# Enviar CSV
echo "📤 Enviando CSV ao GCS..."
gsutil cp dataset.csv gs://$BUCKET_NAME/

echo "✅ Concluído!"
