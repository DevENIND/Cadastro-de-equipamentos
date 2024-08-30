
################################################################################################################################################################################
################################################################################ CONEXÃO COM BANCO DE DADOS ####################################################################
################################################################################################################################################################################
import mysql.connector
def mysql_connection(host, user, passwd, database=None):
    connection = mysql.connector.connect(
        host = host,
        user = user,
        passwd = passwd,
        database = database
    )
    return connection

def caputra_maiorID(Tabela, banco_de_dados):
    query = f'Select max(id) from {Tabela}'
    cursor = banco_de_dados.cursor()
    cursor.execute(query)
    return cursor

def inserir_banco(Tabela, Dados, banco_de_dados):
    query = f'INSERT INTO {Tabela} VALUES ({Dados})'
    print(query)
    cursor = banco_de_dados.cursor()
    cursor.execute(query)
    banco_de_dados.commit()
    
def delete_banco(Tabela, Condicao, banco_de_dados):
    query = f'DELETE FROM {Tabela} WHERE {Condicao}'
    cursor = banco_de_dados.cursor()
    cursor.execute(query)
    banco_de_dados.commit()
    
def seleciona_dados(dados, Tabela, Condicao, banco_de_dados):
    query = f'SELECT {dados} FROM {Tabela} WHERE {Condicao}'
    cursor = banco_de_dados.cursor()
    cursor.execute(query)
    return cursor
    

################################################################################################################################################################################
################################################################################## PREPARANDO EMAILS ###########################################################################
################################################################################################################################################################################

import mimetypes

import smtplib
import getpass


from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random


import datetime

def prepara_corpo_email_Codigo(NumCod):
    agora = datetime.datetime.now()
    hora_agora = agora.time().hour
    
    if hora_agora > 0 and hora_agora <= 12:
        corpo = 'Bom Dia!'
    elif hora_agora > 13 and hora_agora <= 18:
        corpo = 'Boa Tarde!'
    elif hora_agora > 18:
        corpo = 'Boa Noite'
    

    corpo += f"<br><br>Segue o numero para acessar a pagina de equipamentos calibraveis da ENIND: {NumCod}<br><br>"
    corpo += f"<b>E-mail automatico, utilizado apenas para envio.</b>"
    corpo += f"<br> Atenciosamente,"

    return corpo


def registra_codigo_email(email):
    try:
        codigo = ""
        for x in range(6):
            aleatorio = random.randrange(0,9)
            codigo += str(aleatorio)
        
        print (codigo)

        servidor = 'bdnuvemwa.mysql.dbaas.com.br'
        bancodados = 'bdnuvemwa'
        usuario = "bdnuvemwa"
        senha = "W102030b!@"

        banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)

        Condicao = f'EMAIL = "{email}"'
        registro = delete_banco('VALIDAEMAIL',Condicao, banco_de_dados)
        
        print('dados excluidos')
        
        records = caputra_maiorID('VALIDAEMAIL', banco_de_dados)
        records = records.fetchall()

        for row in records: myID = row[0]
            
        if myID is None: 
            myID = 0 
        else:
            myID = myID+1
           
        dados = f'{myID},"{email}",{codigo}'
        registro = inserir_banco('VALIDAEMAIL',dados, banco_de_dados)
        
        print('dados inseridos')
        
        corpo_email = prepara_corpo_email_Codigo(codigo)
        print(corpo_email)
        assunto = "Codigo Calibragem de Equipamentos - ENIND"
        envio, MsgErro = enviar_email(email, assunto, corpo_email)
        
        if envio:
             print('email enviado com sucesso')
             return True, ""
        else:
            print(f'houve um erro ao enviar o email:{MsgErro}')
            return False, MsgErro
        return True
    except Exception as inst:
        print(f'houve um erro forra do escopo de programacao: {inst}')
        return False, inst
   
def valida_codigo(email, codigo):
    try:
        servidor = 'bdnuvemwa.mysql.dbaas.com.br'
        bancodados = 'bdnuvemwa'
        usuario = "bdnuvemwa"
        senha = "W102030b!@"

        banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)

        records = caputra_maiorID('VALIDAEMAIL', banco_de_dados)
        records = records.fetchall()

        dados = f'CODIGO'
        condicao = f'EMAIL = "{email}"'
        records = seleciona_dados(dados,'VALIDAEMAIL',condicao,banco_de_dados)

        Cod_Val = ""
        for row in records:
            Cod_Val = row[0]
            
        if Cod_Val == "": 
            print('Nao possui codigo cadastrado')
            return False, "Cadastro na tabela nao identificado"
        elif int(Cod_Val) == int(codigo):
            print('codigo correto')
            return True,""
        else:
            print('codigo nao corresponde')
            return False, "Codigo nao coincide com o do email"

    except Exception as inst:
        print(f'houve um erro forra do escopo de programacao: {inst}')
        return False, inst


def enviar_email(para, assunto, corpo):
    try:
        sender = 'naorespenind@hotmail.com'
        password = 'N102030p!@'
        
        msg = MIMEMultipart()
        msg['From'] = sender
        msg['To'] = para
        msg['Subject'] = assunto
        
        CaminhoGIF = "https://enind.com.br/wp-content/uploads/2024/03/Automacao-ENIND-4-1-1.gif"
        CorpoEmail = corpo +  f"<br><img src={chr(34)}{CaminhoGIF}{chr(34)}>" 
        
        # Corpo da mensagem
        msg.attach(MIMEText(CorpoEmail, 'html', 'utf-8'))

        raw = msg.as_string()


        with smtplib.SMTP('smtp-mail.outlook.com', 587) as smtp_server:
            smtp_server.ehlo()  # Pode ser omitido
            smtp_server.starttls()  # Protege a conexão
            smtp_server.ehlo()  # Pode ser omitido
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, para, raw)
            smtp_server.quit()

        return True, ""
    except Exception as inst:
       return False, inst
        

if __name__ == '__main__':
    x = valida_codigo('wagner.barreiro@enind.com.br',633153)
