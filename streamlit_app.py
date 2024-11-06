import streamlit as st
from PIL import Image
import openai
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functions_open_ai import processar_imagem   # Importa a função do arquivo externo

# Show title and description.
st.title("💬 Saiba se Você Foi Multado Injustamente!")
st.write(
    "Carregue a foto ou cópia digital da sua multa de trânsito e nossa plataforma verificará automaticamente se há irregularidades nas informações."
    "Nossa análise irá verificar se há elementos ausentes na imagem, como a presença de semáforos, faixas de pedestre e sinalizações que justifiquem a multa. Você receberá um resumo indicando se alguma informação pode estar incorreta ou ausente."
)

# Configuração da API do GPT
openai.api_key = "sua-chave"

# Configuração do SMTP (por exemplo, usando Gmail)
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "seu-email@gmail.com"  # Insira o e-mail de envio
EMAIL_PASSWORD = "sua-senha"    # Insira a senha do e-mail de envio

def enviar_email(destinatario, assunto, corpo):
    msg = MIMEMultipart()
    msg['From'] = EMAIL
    msg['To'] = destinatario
    msg['Subject'] = assunto
    msg.attach(MIMEText(corpo, 'plain'))

    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()
    server.login(EMAIL, EMAIL_PASSWORD)
    server.send_message(msg)
    server.quit()

# Upload da imagem
uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Imagem da multa", use_column_width=True)

    # Converte a imagem para bytes para enviar para o GPT
    img_bytes = io.BytesIO()
    image.save(img_bytes, format="PNG")
    img_bytes = img_bytes.getvalue()

    # Analisar a imagem
    if st.button("Analisar Imagem"):
       
        # Processa a resposta
        resultado = processar_imagem(img_bytes)  # Passa a imagem em bytes para a função

        # Exibe os dados extraídos
        st.subheader("Resultado da Análise")
        st.write(resultado)

        # Verifica se há irregularidades
        if "irregularidade" in resultado.lower():
            st.warning("Foi detectada uma possível irregularidade!")
            
            # Pede o e-mail para envio do relatório
            email = st.text_input("Digite seu e-mail para receber o relatório completo das irregularidades:")
            
            if email and st.button("Enviar Relatório por E-mail"):
                assunto = "Relatório de Verificação de Multas"
                enviar_email(email, assunto, resultado)
                st.success("Relatório enviado com sucesso!")
    else:
        st.error("Não foi possível analisar a imagem.")