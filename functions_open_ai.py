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
        prompt = """
        
        
Extraia todos os textos de maneira estruturada

**Cabeçalho da notificação:**
- Código RENAINF
- Data da infração 
- Placa
- Município e UF
- Código e descrição da infração
- Número do Auto de Infração (AIT)
- Prazo para apresentação do condutor

**Detalhes adicionais da notificação:**
- Veículo: placa, cor, marca/modelo, espécie e tipo de veículo
- Data de emissão da notificação
- Local, data e hora da infração
- Observações
- Código de enquadramento e base legal da infração
- Pontuação associada à infração
- Descrição completa da infração
- Velocidade regulamentada, velocidade medida e velocidade considerada
- Data de aferição do equipamento de fiscalização
- Município da infração e UF
- Identificação do agente de trânsito
- Número e marca/modelo do equipamento
- Município autuador e código do órgão autuador

Não inclua informações pessoais ou dados de contato do proprietário do veículo."""


        # Envia a imagem e o prompt para o modelo
        response = client.chat.completions.create(
            model="gpt-4o",  # Confirme se esse modelo específico está disponível para seu uso
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