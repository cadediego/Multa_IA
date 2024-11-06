import openai
import os
from dotenv import load_dotenv
import base64

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API do GPT
openai.api_key = os.getenv("OPENAI_API_KEY")
client = openai

# Função para converter bytes de imagem para uma string base64
def image_to_base64(image_bytes):
    return base64.b64encode(image_bytes).decode('utf-8')


def extrair_dados_da_imagem(uploaded_file):
    try:
        # Lê os bytes da imagem
        img_bytes = uploaded_file.read()

        # Codifica a imagem para base64
        img_b64_str = image_to_base64(img_bytes)

        # Estrutura do prompt
        prompt = "Extrair as informações de multa, como número da placa, infração, pontos na carteira, data e hora, e elementos de trânsito (como semáforo)."

        # Requisição para a API com base64
        response = client.chat.completions.create(
            model="gpt-4-vision",  # Certifique-se de usar o modelo correto
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt,
                        },
                        {
                            "type": "image_url",
                            "image_url": f"data:image/jpeg;base64,{img_b64_str}",
                        },
                    ],
                }
            ],
        )

        return response.choices[0].message['content']  # Ajuste conforme o formato da resposta
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
