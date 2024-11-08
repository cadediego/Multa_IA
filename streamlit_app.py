import streamlit as st
import pytesseract
from PIL import Image
import io
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from functions_open_ai import processar_imagem
from readfiles import processar_imagem_completa

# Show title and description.
st.title("💬 Saiba se Você Foi Multado Injustamente!")
st.write(
    "Carregue a foto ou cópia digital da sua multa de trânsito e nossa plataforma verificará automaticamente se há irregularidades nas informações."
    "Nossa análise irá verificar se há elementos ausentes na imagem, como a presença de semáforos, faixas de pedestre e sinalizações que justifiquem a multa. Você receberá um resumo indicando se alguma informação pode estar incorreta ou ausente."
)


# Upload da imagem
uploaded_file = st.file_uploader("Escolha uma imagem", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    testimage = Image.open(uploaded_file)
    # Redimensiona a imagem para reduzir o tamanho e aplica compressão
    #image = image.resize((400, 400))  # Experimente um tamanho menor
    st.image(image, caption="Imagem da multa", use_column_width=True)
    texto_extraido = pytesseract.image_to_string(testimage, lang='por')
    st.code(texto_extraido, language='Text')

    # Converte a imagem para bytes com compressão JPEG
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=image.format)
    #image.save(img_byte_arr, format='JPEG', quality=50)  # Ajuste a qualidade conforme necessário
    img_byte_arr = img_byte_arr.getvalue()

    # Analisar a imagem
    if st.button("Analisar Imagem"):
        # Processa a imagem
        uploaded_file = image
        resultado = processar_imagem_completa(img_byte_arr)

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
                #enviar_email(email, assunto, resultado)
                st.success("Relatório enviado com sucesso!")
    else:
        st.error("Não foi possível analisar a imagem.")
