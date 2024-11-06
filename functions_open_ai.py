import openai
import os
from dotenv import load_dotenv
import base64
import io

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API do GPT
openai.api_key = os.getenv("OPENAI_API_KEY")

def extrair_dados_da_imagem(image_bytes):
    """
    Função para usar GPT-4 Vision para analisar a imagem e extrair dados estruturados.
    """
    try:
        # Abre a imagem em modo binário
        image_file = io.BytesIO(image_bytes)
        
        # Gera o prompt
        prompt = "Extrair as informações de multa, como número da placa, infração, pontos na carteira, data e hora, e elementos de trânsito (como semáforo)."
        
        # Envia a imagem diretamente para o modelo GPT-4 Vision
        response = openai.Image.create(
            model="gpt-4-turbo-vision",
            prompt=prompt,
            file=image_file
        )

        # Retorna a resposta da análise
        return response['data']
    except Exception as e:
        return f"Erro: {str(e)}"

def processar_imagem(uploaded_file):
    """
    Função para processar uma imagem carregada e extrair os dados estruturados.
    """
    # Lê os bytes da imagem
    img_bytes = uploaded_file

    # Chama a função para extrair os dados da imagem
    dados_extraidos = extrair_dados_da_imagem(img_bytes)

    # Retorna os dados extraídos ou erro
    return dados_extraidos