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

def extrair_dados_da_imagem(image_bytes):
    """
    Função para usar GPT Vision para analisar a imagem e extrair dados estruturados.
    """
    try:
        # Converte a imagem para base64
        img_b64_str = image_to_base64(image_bytes)

        # Verifica o comprimento da string base64 gerada (para debug)
        if len(img_b64_str) < 100:  # Se for muito curto, pode estar errado
            lenght =  len(img_b64_str)
            return f"Erro: A string base64 gerada é muito curta. Verifique a imagem. {lenght}"

        prompt = "Extrair as informações de multa, como número da placa, infração, pontos na carteira, data e hora, e elementos de trânsito (como semáforo)."
        
        # Cria a mensagem de entrada com a imagem em base64
        response = client.chat.completions.create(
            model="gpt-4-turbo",  # Ajuste o modelo conforme necessário
            messages=[
                {
                    "role": "user",
                    "content": prompt
                },
                {
                    "role": "user",
                    "content": f"data:image/png;base64,{img_b64_str}"
                }
            ]
        )

        # Processa a resposta da análise
        return response
    except Exception as e:
        return f"Erro: {str(e)}"

def processar_imagem(uploaded_file):
    """
    Função para processar uma imagem carregada e extrair os dados estruturados.
    """
    # Lê os bytes da imagem
    img_bytes = uploaded_file.read()

    # Chama a função para extrair os dados da imagem
    dados_extraidos = extrair_dados_da_imagem(img_bytes)

    # Retorna os dados extraídos ou erro
    return dados_extraidos
