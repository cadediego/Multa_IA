from PIL import Image 
import io
import openai
import os
from dotenv import load_dotenv  # Carregar variáveis do arquivo .env

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da API do GPT
openai.api_key = os.getenv("OPENAI_API_KEY")

def extrair_dados_da_imagem(image_bytes):
    """
    Função para usar GPT Vision para analisar a imagem e extrair dados estruturados.
    A função retorna as informações da multa como um dicionário estruturado.
    """
    try:
        # Enviar a imagem para a API do GPT-4 com visão (por exemplo, usando a função de análise de imagens)
        response = openai.Image.create(
            model="gpt-4-vision",  # Modelo de GPT com capacidade de visão
            prompt="Extrair informações estruturadas da seguinte imagem de multa de trânsito. Por favor, identifique e extraia as seguintes informações:\n"
                   "- Número da placa\n"
                   "- Infração\n"
                   "- Quantidade de pontos na carteira\n"
                   "- Data e hora\n"
                   "- Informações do equipamento de registro\n"
                   "- Elementos de trânsito (semáforo, faixa de pedestre, sinalização)\n",
            image=image_bytes  # Envia a imagem
        )

        # Processa a resposta da análise
        if response and "data" in response:
            result = response['data'][0].get('text', 'Não foi possível processar a imagem.')
            return result
        else:
            return "Erro: Não foi possível processar a imagem."
    
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
