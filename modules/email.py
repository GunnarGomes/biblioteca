# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# import dotenv
# import os

# dotenv.load_dotenv()

# email = os.getenv("EMAIL")
# senha_email = os.getenv("SENHA_EMAIL")

# # email da biblioteca
# smtp_server = 'smtp.gmail.com'
# smtp_port = 587
# meu_email = email
# minha_senha = senha_email

# # email destino
# destinatario = '00001099296365sp@al.educacao.sp.gov.br'
# assunto = 'Redefinir senha' 
# mensagem = 'Clique no link para redefinir sua senha: https://seusite.com/redefinir-senha/token123'

# msg = MIMEMultipart()
# msg['From'] = meu_email
# msg['To'] = destinatario
# msg['Subject'] = assunto
# msg.attach(MIMEText(mensagem, 'plain'))

# try:
#     with smtplib.SMTP(smtp_server, smtp_port) as server:
#         server.starttls()
#         server.login(meu_email, minha_senha)
#         server.send_message(msg)
#     print("E-mail enviado com sucesso!")
# except Exception as e:
#     print(e)

