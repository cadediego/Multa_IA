from PIL import Image
import io
import openai
import os
from dotenv import load_dotenv  # Carregar variáveis do arquivo .env

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()
# Configuração da API do GPT


openai.api_key = os.getenv("OPENAI_API_KEY")
# Substitua pela sua chave de API

def extrair_dados_da_imagem(img_bytes):
    """
    Função para usar GPT Vision para analisar a imagem e extrair dados estruturados.
    A função retorna as informações da multa como um dicionário estruturado.
    """
    try:
        # Enviar a imagem para o GPT Vision para análise
        response = openai.Image.create(
            model="gpt-4-vision",  # Substitua pelo modelo correto se necessário
            input={"image": img_bytes}
        )

        # Processa a resposta da análise
        if response and "text" in response:
            texto = response["text"]

            # Define o prompt para solicitar a extração e estruturação dos dados
            prompt = f"""
            Com base no seguinte texto extraído de uma imagem de multa de trânsito, extraia as seguintes informações e estruture-as em formato JSON:
            - Número da placa
            - Infração
            - Quantidade de pontos na carteira
            - Data e hora
            - Informações do equipamento de registro
            - Elementos de trânsito (semáforo, faixa de pedestre, sinalização) que aparecerem na imagem no canto inferior direito.
            - Se há ou não irregularidade.

            Texto extraído:
            {texto}
            """
            
            # Solicita ao GPT a extração e estruturação dos dados
            structured_data_response = openai.Completion.create(
                model="gpt-4-turbo",  # Usando o modelo para estruturação de dados
                prompt=prompt,
                max_tokens=500
            )

            structured_data = structured_data_response.choices[0].text.strip()
            return structured_data
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