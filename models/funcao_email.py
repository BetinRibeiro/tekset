# -*- coding: utf-8 -*-

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def enviar_email(destinatario, assunto, texto):
    remetente = "tekset.app@outlook.com"  # Insira o endereço de e-mail do remetente
    senha = "142536@tekset"  # Insira a senha do remetente


    # Configurar a mensagem
    mensagem = MIMEMultipart()
    mensagem["From"] = remetente
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    corpo_mensagem = MIMEText(texto, 'html', 'utf-8')
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


def disparar_email(id_registro):
    try:
        registro_atividade = db.registro_atividade(id_registro)
        usuario = db.auth_user(registro_atividade.circunspecto)
        r_email = usuario.email
        assunto = registro_atividade.tipo[13:]
        texto = f'''
        <div class="col-md-12" >
        <br>
        <h2 class="lead">Prezado {usuario.first_name},</h2>
        <p class="lead">Esperamos que esta mensagem o encontre bem. Em nome da equipe da TekSet.app, gostaríamos de fornecer um aviso importante sobre uma atividade pela qual você é responsável.</p>
        <p class="lead">Gostaríamos de lembrá-lo de que a atividade {registro_atividade.tipo[13:]} está programada para ser executada. Essa atividade é de extrema importância para o andamento do projeto e, portanto, é essencial que seja concluída dentro do prazo estabelecido.</p>

              <p class="lead">Caso você enfrente qualquer problema ou precise de suporte adicional para a conclusão da atividade, não hesite em entrar em contato com seu coordenador. Estamos aqui para ajudá-lo e garantir o sucesso dessa iniciativa.</p>
              <p class="lead">Contamos com a sua dedicação e profissionalismo para que a atividade seja realizada conforme planejado, contribuindo assim para o progresso geral do projeto.</p>
              <p class="lead">Agradecemos antecipadamente pelo seu empenho e colaboração. Caso tenha alguma dúvida, não hesite em nos contatar.</p>
              <p class="lead">Segue o link de mais detalhes da atividade: <a href="https://www.tekset.app.br/gmev/acs_registro_atividade/relatorio/{registro_atividade.id}">Relatório da Atividade</a></p>
              <p class="lead">Atenciosamente,&nbsp;Equipe TekSet.app</p>
            </div>
        '''
        msg=enviar_email(r_email, assunto, texto)
    except:
        msg="ERRO"
    return msg

def disparar_email_gr(id_gestao):
    gestao_de_risco = db.gestao_de_risco(id_gestao)
    registro_atividade = db.registro_atividade(gestao_de_risco.registro_atividade)
    usuario = db.auth_user(gestao_de_risco.circunspecto)
    r_email = usuario.email
    assunto = 'Gestão de Risco'
    texto = f'''
    <div class="col-md-12" >
    <br>
    <h2 class="lead">Prezado {usuario.first_name},</h2>
    <p class="lead">Esperamos que esta mensagem o encontre bem. Em nome da equipe da TekSet.app, gostaríamos de fornecer um aviso importante sobre uma atividade pela qual você é responsável.</p>
    <p class="lead">Gostaríamos de lembrá-lo de que a atividade {assunto} está programada para ser executada. Essa atividade é de extrema importância para o andamento do projeto e, portanto, é essencial que seja concluída dentro do prazo estabelecido.</p>

          <p class="lead">Caso você enfrente qualquer problema ou precise de suporte adicional para a conclusão da atividade, não hesite em entrar em contato com seu coordenador. Estamos aqui para ajudá-lo e garantir o sucesso dessa iniciativa.</p>
          <p class="lead">Contamos com a sua dedicação e profissionalismo para que a atividade seja realizada conforme planejado, contribuindo assim para o progresso geral do projeto.</p>
          <p class="lead">Agradecemos antecipadamente pelo seu empenho e colaboração. Caso tenha alguma dúvida, não hesite em nos contatar.</p>
          <p class="lead">Segue o link de mais detalhes da atividade: <a href="https://www.tekset.app.br/gmev/acs_registro_atividade/relatorio/{registro_atividade.id}">Relatório da Atividade</a></p>
          <p class="lead">Atenciosamente,&nbsp;Equipe TekSet.app</p>
        </div>
    '''
    try:
        msg=enviar_email(r_email, assunto, texto)
    except:
        msg="ERRO"
    return msg
