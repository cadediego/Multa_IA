import streamlit as st
from PIL import Image
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functions_open_ai import processar_imagem

# Show title and description.
st.title("💬 Saiba se Você Foi Multado Injustamente!")
st.write(
    "Carregue a foto ou cópia digital da sua multa de trânsito e nossa plataforma verificará automaticamente se há irregularidades nas informações."
    "Nossa análise irá verificar se há elementos ausentes na imagem, como a presença de semáforos, faixas de pedestre e sinalizações que justifiquem a multa. Você receberá um resumo indicando se alguma informação pode estar incorreta ou ausente."
)

# Configuração do SMTP
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL = "seu-email@gmail.com"  # Substitua pelo seu e-mail de envio
EMAIL_PASSWORD = "sua-senha"    # Substitua pela senha do seu e-mail de envio

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

    # Analisar a imagem
    if st.button("Analisar Imagem"):
        # Processa a imagem
        uploaded_file = image
        resultado = processar_imagem(uploaded_file)

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
