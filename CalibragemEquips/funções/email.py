
import mimetypes

import smtplib
import getpass
import sys

from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random
import banco_dados 



def registra_codigo_email(email):
    try:
        codigo = ""
        for x in range(0,5):
            aleatorio = random.randrange(0,9)
            codigo += str(aleatorio)
        
        servidor = 'bdnuvemwa.mysql.dbaas.com.br'
        bancodados = 'bdnuvemwa'
        usuario = "bdnuvemwa"
        senha = "W102030b!@"

        banco_de_dados = banco_dados.mysql_connection(servidor, usuario,senha,bancodados)
        
        print(codigo)

        Condicao = f'EMAIL = {email}'
        registro = banco_dados.delete_banco('VALIDAEMAIL',Condicao, banco_de_dados)
        
        print('dados excluidos')
        
        dados = f'EMAL = {email}, CODIGO = {codigo}'
        registro = banco_dados.inserir_banco('VALIDAEMAIL',dados, banco_de_dados)
        
        print('dados inseridos')

        if registro == False:
            return False,"Nao foi possivel acessar ao banco de dados."
        

    
        return True
    except:
        return False
   
if __name__ == '__main__':
    x = registra_codigo_email('wagner.barreiro@enind.com.br')


def envia_email(para, assunto, arquivos, corpo):
    try:
        sender = 'naorespenind@hotmail.com'
        password = 'N102030p!@'
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = para
        msg['Subject'] = assunto

        CorpoEmail = "\n".join(corpo)
        
        # Corpo da mensagem
        msg.attach(MIMEText(CorpoEmail, 'html', 'utf-8'))

        if arquivos != []:
            MtzAnexo = arquivos.split("|")

            # Arquivos anexos.
            for arquivo in MtzAnexo:
                arquivored = arquivo[1:]
                arquivored = arquivored.replace("\n", "")
                adiciona_anexo(msg, arquivored)

        raw = msg.as_string()


        with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp_server:
            smtp_server.ehlo()  # Pode ser omitido
            smtp_server.starttls()  # Protege a conexão
            smtp_server.ehlo()  # Pode ser omitido
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, para, raw)
            smtp_server.quit()

        return True
    except Exception as inst:
            return False
        
def adiciona_anexo(msg, filename):
    if not os.path.isfile(filename):
        return

    ctype, encoding = mimetypes.guess_type(filename)

    if ctype is None or encoding is not None:
        ctype = 'application/octet-stream'

    maintype, subtype = ctype.split('/', 1)

    if maintype == 'text':
        with open(filename) as f:
            mime = MIMEText(f.read(), _subtype=subtype)
    elif maintype == 'image':
        with open(filename, 'rb') as f:
            mime = MIMEImage(f.read(), _subtype=subtype)
    elif maintype == 'audio':
        with open(filename, 'rb') as f:
            mime = MIMEAudio(f.read(), _subtype=subtype)
    else:
        with open(filename, 'rb') as f:
            mime = MIMEBase(maintype, subtype)
            mime.set_payload(f.read())

        encoders.encode_base64(mime)

    mime.add_header('Content-Disposition', 'attachment', filename=filename.split("\\")[-1])
    msg.attach(mime)
