import pytesseract
from PIL import Image
import io
import openai
import os
from dotenv import load_dotenv
import base64

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai


def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')



def extrair_texto_com_ocr(image_bytes):

    try:
        img = Image.open(io.BytesIO(image_bytes))
        texto_extraido = pytesseract.image_to_string(img, lang='por')  # 'por' para português
        return texto_extraido
    except Exception as e:
        return f"Erro ao processar a imagem: {str(e)}"

def analisar_imagem_do_carro(image_bytes):
    try:
        img_b64_str = image_to_base64(image_bytes)

        # Define o prompt para a análise visual da imagem
        prompt = """
        Analise a imagem fornecida e identifique qualquer elemento visual relacionado a infrações de trânsito.
        Verifique a presença de:
        - Semáforos
        - Faixas de pedestre
        - Placas de sinalização
        - Estacionamento proibido ou outros sinais de infração de trânsito
        Descreva de maneira estruturada os elementos encontrados.
        """
        response = client.chat.completions.create(
            model="gpt-4",  # Utilize o modelo adequado para seu caso
            messages=[{
                "role": "user",
                "content": prompt
            }],
        )

        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao analisar a imagem do carro: {str(e)}"



def processar_imagem_completa(uploaded_file):

    img_bytes = uploaded_file
    texto_extraido = extrair_texto_com_ocr(img_bytes)
    return {
        "texto_extraido": texto_extraido
        #"analise_imagem_carro": imagem_do_carro
    }
