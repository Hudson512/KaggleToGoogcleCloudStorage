# 📦 Dataset Downloader para Vertex AI (Google Cloud)

Este repositório contém um script que automatiza o processo de:

1. Baixar datasets do Kaggle.
2. Extrair os arquivos.
3. Enviar imagens para um bucket no Google Cloud Storage (GCS).
4. Gerar um arquivo CSV de anotação no formato esperado pelo **Vertex AI AutoML**.

> ✅ Ideal para datasets organizados em subpastas por classe (ex: classificação de imagens como frutas, animais, etc).

---

## 📁 Estrutura esperada do dataset

O script espera que o dataset tenha a seguinte estrutura após extração:
Training/
├── Class1/
│ ├── image1.jpg
│ ├── image2.jpg
├── Class2/
│ ├── image1.jpg
│ ├── image2.jpg

(Ou com outras pastas como `Test/` ou `Validation/`, se quiser gerar CSV com múltiplos conjuntos.)

---

## ⚙️ Pré-requisitos

- Ambiente configurado com **Google Cloud SDK**
- Ativar a **Vertex AI API**
- Ter permissão de escrita no bucket do GCS
- Conta no [Kaggle](https://www.kaggle.com/) com `kaggle.json`

---

## 🚀 Como usar

1. **Faça upload do seu `kaggle.json`** para o Cloud Shell (ou instância Jupyter/VM).

2. **Edite o script `d_kaggle.py` ou `sh` para inserir:**
   - Nome do dataset do Kaggle (ex: `moltean/fruits`)
   - Nome do seu bucket do GCS (ex: `meu-dataset-bucket`)

3. **Execute o script no Cloud Shell ou Vertex AI Notebook:**

### Com Bash:
```bash
chmod +x download_from_kaggle.sh
./download_from_kaggle.sh moltean/fruits meu-projeto-gcp
```
### Com Python (no Vertex Notebook):
!python3 d_kaggle.py

### 📄 Sobre o CSV gerado
O arquivo dataset.csv será gerado no seguinte formato:
| SET   | IMAGE\_PATH                               | LABEL  |
| ----- | ----------------------------------------- | ------ |
| TRAIN | gs\://meu-bucket/images/Class1/image1.jpg | Class1 |
| TRAIN | gs\://meu-bucket/images/Class2/image2.jpg | Class2 |
| ...   | ...                                       | ...    |

Este CSV pode ser usado diretamente no AutoML do Vertex AI para importar dados rotulados.

### ☁️ Upload para o GCS
O script realiza o upload automático:

De todas as imagens em Training/

Do arquivo CSV de anotações
```bash
gsutil -m cp -r fruits/fruits-360/Training/* gs://meu-bucket/images/
gsutil cp dataset.csv gs://meu-bucket/
```
### ❗ Erros comuns
| Erro                             | Solução                                       |
| -------------------------------- | --------------------------------------------- |
| `PermissionError: /root/.kaggle` | Use `~/.kaggle` em vez de `/root`             |
| `No space left on device`        | Use o Vertex AI Notebook (tem mais espaço)    |
| `FileNotFoundError: kaggle`      | Verifique se a API foi instalada corretamente |


### 📌 Observações
Ambos scripts assumem que o arquivo kaggle.json está no mesmo diretório de execução.

O script .sh é ideal para execução rápida no Cloud Shell.

O script .py é ideal para execução em ambientes como Vertex AI Notebooks (com mais armazenamento e controle).

### ✍️ Autor
Feito por Seu Hudson
Contribuições são bem-vindas!
