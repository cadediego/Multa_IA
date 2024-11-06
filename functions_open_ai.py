import openai
import os
from dotenv import load_dotenv
import base64
import io

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API do GPT
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai

def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')

def extrair_dados_da_imagem(image_bytes):
    """
    Função para usar GPT Vision para analisar a imagem e extrair dados estruturados.
    """
    try:
        # Converte a imagem para base64
        img_b64_str = image_to_base64(image_bytes)

        # Define o prompt para a análise da imagem
        prompt = "Extrair informações da multa de trânsito,sem pegar informações pessoais, quero apenas, infração, pontos na carteira, data e hora, e verificar a presença de elementos de trânsito (como semáforo e faixa de pedestre)."

        # Envia a imagem e o prompt para o modelo
        response = client.chat.completions.create(
            model="gpt-4o-mini",  # Confirme se esse modelo específico está disponível para seu uso
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_b64_str}"
                            },
                        },
                    ]
                }
            ],
            #max_tokens=300
        )

        # Processa e retorna a resposta da análise
        return response.choices[0].message.content
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