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
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

def image_to_base64(image_bytes):
    """Converte a imagem em base64. A função tenta garantir a compatibilidade para JPEG."""
    try:
        # Verifique o tipo da imagem e converta para base64
        img = Image.open(io.BytesIO(image_bytes))
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')  # Salva em JPEG
        img_byte_arr = img_byte_arr.getvalue()
        return base64.b64encode(img_byte_arr).decode('utf-8')
    except Exception as e:
        return f"Erro ao converter imagem para base64: {str(e)}"

def extrair_texto_com_ocr(image_bytes):
    """Extrai texto da imagem usando OCR com Tesseract."""
    try:
        img = Image.open(io.BytesIO(image_bytes))
        texto_extraido = pytesseract.image_to_string(img, lang='por')
        return texto_extraido
    except Exception as e:
        return f"Erro ao processar a imagem: {str(e)}"

def analisar_imagem_do_carro(image_bytes):
    """Análise visual da imagem usando OpenAI."""
    try:
        img_b64_str = image_to_base64(image_bytes)
        if "Erro" in img_b64_str:
            return img_b64_str  # Retorna o erro de conversão base64 se houver

        prompt = """
        Analise a imagem fornecida e identifique qualquer elemento visual relacionado a infrações de trânsito.
        Verifique a presença de:
        - Semáforos
        - Faixas de pedestre
        - Placas de sinalização
        - Estacionamento proibido ou outros sinais de infração de trânsito
        Descreva de maneira estruturada os elementos encontrados.
        """
        
        response = client.chat_completions.create(
            model="gpt-4-vision",  # Confirme se o modelo visual correto está configurado
            messages=[{
                "role": "user",
                "content": prompt
            }],
            images=[{"image": img_b64_str}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Erro ao analisar a imagem do carro: {str(e)}"

def processar_imagem_completa(uploaded_file):
    """Processa a imagem para extração de texto e análise de elementos visuais."""
    img_bytes = uploaded_file
    texto_extraido = extrair_texto_com_ocr(img_bytes)
    #analise_imagem_carro = analisar_imagem_do_carro(img_bytes)
    return {
        "texto_extraido": texto_extraido
        #"analise_imagem_carro": analise_imagem_carro
    }
