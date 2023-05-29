# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(destinatario, assunto, texto):
    remetente = "ljn141001@outlook.com"  # Insira o endereço de e-mail do remetente
    senha = "141516 leo"  # Insira a senha do remetente


    # Configurar a mensagem
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    corpo_mensagem = MIMEText(texto, "plain")
    mensagem.attach(corpo_mensagem)

    try:
        # Estabelecer a conexão com o servidor SMTP 
        servidor_smtp = smtplib.SMTP("smtp.outlook.com", 587)
        servidor_smtp.starttls()

        # Autenticar com o servidor
        servidor_smtp.login(remetente, senha)

        # Enviar e-mail
        servidor_smtp.sendmail(remetente, destinatario, mensagem.as_string())

        return ("E-mail enviado com sucesso!")
    except Exception as e:
        return (f"Erro ao enviar e-mail: {str(e)}")
    finally:
        # Encerrar a conexão com o servidor SMTP
        servidor_smtp.quit()
        
    return True