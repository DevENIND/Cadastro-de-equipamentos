


################################################################################################################################################################################
################################################################################ CONEXAO COM BANCO DE DADOS ####################################################################
################################################################################################################################################################################

from calendar import month
from email.utils import formataddr
from logging.config import ConvertingDict
from time import strptime
from tkinter.tix import Form
from xmlrpc.client import DateTime
import mysql.connector

def mysql_connection(host, user, passwd, database=None):
    try:
        connection = mysql.connector.connect(
            host = host,
            user = user,
            passwd = passwd,
            database = database
        )
        return connection
    except Exception as inst:
        return False

def caputra_maior_dado(Tabela, banco_de_dados, dado):
    try:
        query = f'Select max({dado}) from {Tabela}'
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        return cursor
    except Exception as inst:
        return False

def caputra_maiorID(Tabela, banco_de_dados):
    try:
        query = f'Select max(id) from {Tabela}'
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        return cursor
    except Exception as inst:
        return False
    
def inserir_banco(Tabela, Dados, banco_de_dados):
    try: 
        query = f'INSERT INTO {Tabela} VALUES ({Dados})'
        print(query)
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        banco_de_dados.commit()
        return True
    except Exception as inst:
        return False
    
def delete_banco(Tabela, Condicao, banco_de_dados):
    try:
        query = f'DELETE FROM {Tabela} WHERE {Condicao}'
        print(query)
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        banco_de_dados.commit()
        return True
    except Exception as inst:
        return False
    
def seleciona_dados(dados, Tabela, Condicao, banco_de_dados):
    try:
        query = f'SELECT {dados} FROM {Tabela} WHERE {Condicao}'
        #print(query)
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        return cursor
    except Exception as inst:
        return False

def atualiza_dados(Campos_Dados, Tabela, Condicao, banco_de_dados):
    try:
        query = f"UPDATE {Tabela} SET {Campos_Dados} WHERE {Condicao}"
        print(query)
        cursor = banco_de_dados.cursor()
        cursor.execute(query)
        banco_de_dados.commit()
        return True
    except Exception as inst:
        return False

def analisa_texto(texto):
    NaoPermitidos = f"SELECT,DELETE,INSERT,',%,{chr(34)},TRUNCATE,DROP,JOIN,"
    palavras = NaoPermitidos.split(",")

    for palavra in palavras:
            if palavra in texto.upper():
                return False
    
    return True
    

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
    elif hora_agora >= 13 and hora_agora <= 18:
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

        Condicao = f'EMAIL = "{email}" and App = "CalibEqto"'
        registro = delete_banco('VALIDAEMAIL',Condicao, banco_de_dados)
        
        print('dados excluidos')
        
        records = caputra_maiorID('VALIDAEMAIL', banco_de_dados)
        records = records.fetchall()

        for row in records: myID = row[0]
            
        if myID is None: 
            myID = 0 
        else:
            myID = myID+1
        
        strtoken = ""
        strtoken = gera_token_email()
        print(strtoken)
        dados = f'{myID},"{email}",{codigo},"{strtoken}","CalibEqto"'
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

        dados = f'CODIGO, TOKEN'
        condicao = f'EMAIL = "{email}"'
        records = seleciona_dados(dados,'VALIDAEMAIL',condicao,banco_de_dados)

        Cod_Val = ""
        for row in records:
            Cod_Val = row[0]
            strToken = row[1]
            
        if Cod_Val == "": 
            print('Nao possui codigo cadastrado')
            return False, "Cadastro na tabela nao identificado", ""
        elif int(Cod_Val) == int(codigo):
            print('codigo correto')
            return True,"", strToken
        else:
            print('codigo nao corresponde')
            return False, "Codigo nao coincide com o do email",""

    except Exception as inst:
        print(f'houve um erro forra do escopo de programacao: {inst}')
        return False, inst, ""


def enviar_email(para, assunto, corpo):
    try:
        sender = 'NF@enind.com.br'
        password = 'Enind@2020'
        
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
            smtp_server.starttls()  # Protege a conexao
            smtp_server.ehlo()  # Pode ser omitido
            smtp_server.login(sender, password)
            smtp_server.sendmail(sender, para, raw)
            smtp_server.quit()


        return True, ""
    except Exception as inst:
       return False, inst
        
import string
import random

def gera_token_email(size=30, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
   strtoken = ''.join(random.choice(chars) for _ in range(size))
   return strtoken

def valida_token_email(strTokenEnv):
     try:
        servidor = 'bdnuvemwa.mysql.dbaas.com.br'
        bancodados = 'bdnuvemwa'
        usuario = "bdnuvemwa"
        senha = "W102030b!@"

        banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)

        dados = f'EMAIL'
        condicao = f'TOKEN = "{strTokenEnv}"'
        records = seleciona_dados(dados,'VALIDAEMAIL',condicao,banco_de_dados)

        for row in records:
            email = row[0]
     
        if email == "": 
            return False, "", ""
        else:
            return True, "", email
        
     except Exception as inst:
        print(f'houve um erro forra do escopo de programacao: {inst}')
        return False, inst, ""
     
"""
###############################################################################################################################################################################################################################
###############################################################################################################################################################################################################################
###############################################################################################################################################################################################################################
##################################################################################################### REGISTROS DOS EQUIPAMENTOS ##############################################################################################
############################################################################################################################################################################################################################### 
###############################################################################################################################################################################################################################
###############################################################################################################################################################################################################################
 """

def valida_log_edicao(email, OS):
     try:
        servidor = 'bdnuvemwa.mysql.dbaas.com.br'
        bancodados = 'bdnuvemwa'
        usuario = "bdnuvemwa"
        senha = "W102030b!@"

        banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)

        dados = f'tipo_us, OS'
        condicao = f'email = "{email}"'
        records = seleciona_dados(dados,'CalEqto_Us',condicao,banco_de_dados)

        for row in records:
            tipous = row[0]
            OS_perm = row[1]
            
        if tipous == "": 
            return False, "", ""
        else:
           if tipous == 'Usuario':
                if OS_perm == OS or OS == '':
                    return True, ""
                else:
                    return False, ""
           else:
               return True, ""
        
     except Exception as inst:
        print(f'houve um erro forra do escopo de programacao: {inst}')
        return False, inst,""
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% CAPITURA DAS INFORMACOES DO REGISTRO NO BANCO DE DADOS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def puxa_registro(ideqpto, email):

    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"

    banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)
    
    lista_retorno = []
    if ideqpto == 'new':
         id_eqpto =  caputra_maiorID('CalEqto_Eqtos',banco_de_dados)
         lista_retorno.append({
                "id": '',
                "Desc": '',
                "NumSerie": '',
                "Prefixo": '',
                "Status": '',
                "OS": '',
                "Certificado": '',
                "DataCert:": '',
                "DataProx": '',
                "Cam_Img": '',
            })
         validacao, msgerro = valida_log_edicao(email, '')
    else:
        dados = f'*'
        condicao = f'id = "{ideqpto}"'
        records = seleciona_dados(dados,'CalEqto_Eqtos',condicao,banco_de_dados)

        for eqto in records:
            if eqto['id'] == ideqpto:
                lista_retorno.append({
                    "id": eqto["id"],
                    "Desc": eqto[ "Desc"],
                    "NumSerie": eqto[ "Num_serie"],
                    "Tag": eqto["Tag"],
                    "Fabricante": eqto["Fabricante"],
                    "Status": eqto[ "Status"],
                    "OS": eqto["OS"],
                    "Certificadora": eqto["Certificadora"],
                    "DataCert:":  eqto["Data_calibracao"],
                    "DataProx": eqto["DataProx"],
                })
            
        validacao, msgerro = valida_log_edicao(email, lista_retorno[0]['OS'])
    
    return lista_retorno, validacao, msgerro

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% VERIFICA SE O REGISTRO ESTA PRONTO PARA SER REALIZADO %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


def valida_registro(registros):
    chvFal = []
    MsgErro = ""
    for chaves in registros[0].keys():
        if registros[0][chaves] == "":
            MsgErro =  MsgErro + f'{chaves} precisa ser preenchido {chr(10)}'
            
    if registros[0]['Status'] != 'Ativo' and registros[0]['Status'] != 'Inativo':
        MsgErro = MsgErro + f'Campo de Status precisa ser igual a Ativo ou Inativo {chr(10)}'

    if float(registros[0]['OS']) < 100:
        MsgErro = MsgErro + f'Campo OS precisa ser preenchido com valor superior a 100 {chr(10)}'
    
    if not float(registros[0]['OS']).is_integer():
        MsgErro = MsgErro + f'Campo OS deve ser inteiro apenas {chr(10)}'
    
    if float(registros[0]['OS']) > 9999:
        MsgErro = MsgErro + f'Campo OS tem o limite de 4 digitos ex.: OS 50000981 colocar OS 981 {chr(10)}'
        
    if float(registro[0]['QtdMeses']) < 0.033:
        MsgErro = MsgErro + f'Quantidade de meses deve ser superior a 0.033, um dia. {chr(10)}'
    
    DataAtual = datetime.datetime.now()
    DataCalibr = datetime.datetime.strptime(registro[0]["DataCalibracao"], "%d/%m/%Y")
    if DataCalibr > DataAtual:
        MsgErro = MsgErro + f'Data de calibracao esta superior a data atual. {chr(10)}'
      

    if MsgErro == "":
       return True,""
    else:
       return False, MsgErro
    
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% REALIZA REGISTROS DE ALTERACOES NO BANCO DE DADOS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

#Registra as alteracoes realizadas no banco de dados de alteracoes    
def registra_bd_alt(Campos, Valores, idEqto, email, referencia):
    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"
    
    banco_de_dados = mysql_connection(servidor, usuario,senha,bancodados)
    
    records = caputra_maior_dado('CalEqto_Alt', banco_de_dados, 'idAlt')
    records = records.fetchall()
    
    for row in records: myIDAlt = row[0]
            
    if myIDAlt is None: 
        myIDAlt = 0 
    else:
        myIDAlt = myIDAlt+1
    
    HoraAtual = date.today()
    HoraAtual = datetime.datetime.now()
    HoraAtual = format(HoraAtual,"%H:%M:%S")
    print(f'hora atual: {HoraAtual}')

    for x in range(len(Campos)):
        campo = Campos[x]
        valor = Valores[x]
        Msg = ''
        DataAtual = date.today()
        
        DataAtual = format(DataAtual,"%Y:%m:%d")

        #Condicao = f"idEqto = {idEqto} and dataAlt = '{DataAtual}' and campo = '{campo}' and valor = '{valor}' and email = '{email}'"
        #registro = delete_banco('CalEqto_Alt',Condicao, banco_de_dados)
        
        #if registro == True:
        #    print(f'Exclusao referente ao Eqto: {idEqto} campo: {campo}, valor: {valor} {chr(10)}')
            
        records = caputra_maiorID('CalEqto_Alt', banco_de_dados)
        records = records.fetchall()
    
        for row in records: myID = row[0]
            
        if myID is None: 
            myID = 0 
        else:
            myID = myID+1
        
        
        valores_bd = f"{myID},{myIDAlt},{idEqto},'{DataAtual}', '{HoraAtual}' ,'{campo}','{valor}','{email}', '{referencia}'"

        registroBD = inserir_banco('CalEqto_Alt',valores_bd, banco_de_dados)
        
        if registroBD == False:
            Msg = Msg + f'REGISTRO DE ALTERACAO - Uma alteracao nao foi inserida corretamente, referente ao Eqto: {idEqto} campo: {campo}, valor: {valor} {chr(10)}'
            print(f'REGISTRO DE ALTERACAO - Uma alteracao nao foi inserida corretamente, referente ao Eqto: {idEqto} campo: {campo}, valor: {valor}')
            
    if Msg != '':
        return False, Msg
    else:
        return True, Msg
    

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% EXECUTA O REGISTRO DO EQUIPAMENTO NO BANCO DE DADOS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
from datetime import date, timedelta

def realiza_registro(ideqpto, email, registros):

    Alteracao = False
    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"
    
    campos_alt= []
    valores_alt = []
    valores_antes_alt = []

    banco_de_dados = mysql_connection(servidor, usuario, senha, bancodados)
    
    Validacao, Msg = valida_registro(registros)

    if Validacao == False: return Validacao, Msg, ""
    
    lista_antes = []
    if ideqpto == 'new':
        
        validacao, msgerro = valida_log_edicao(email, registros[0]['OS'])
        
        if validacao == False:
            return False, 'Nao possui permissao para registrar nessa OS.',msgerro
        else:
            dados = "NumSerie"
            NumSerieReg = registros[0]["NumSerie"]
            condicao = f"NumSerie = '{NumSerieReg}'"
            records = seleciona_dados(dados,'CalEqto_Eqtos',condicao,banco_de_dados)
            
            numSerie = ""

            for eqto in records:
                numSerie = eqto[0]

            if numSerie != "": return False, 'Ja tem um equipamento com esse numero de serie.',msgerro
            
            Alteracao = True
         
    else:
        
        dados = f'*'
        condicao = f"id = {ideqpto}"
        records = seleciona_dados(dados,'CalEqto_Eqtos',condicao,banco_de_dados)

        for eqto in records:
            if eqto[0] == ideqpto:
                lista_antes.append({
                    "id": eqto[0],
                    "Desc": eqto[1],
                    "Tag": eqto[2],
                    "NumSerie": eqto[3],
                    "Fabricante": eqto[4],
                    "Status": eqto[5],
                    "OS": eqto[6],
                    "Certificadora": eqto[7],
                    "QtdMeses": eqto[8],
                    "DataCalibracao": format(eqto[9],"%Y-%m-%d"),
                })
        
        if lista_antes == []:
            return False, 'Equipamento nao registrado.',''
         
        validacao, msgerro = valida_log_edicao(email, lista_antes[0]['OS'])
           
        if validacao == False:
            return False, 'Seu login nao pode alterar arquivos dessa OS',''

        
        for chaves in registros[0].keys():
            if registros[0][chaves] != lista_antes[0][chaves]:
                if chaves.upper() != 'DATACALIBRACAO':
                    Alteracao = True
                    campos_alt.append(chaves)
                    valores_alt.append(registros[0][chaves])
                    campos_dados = f"{chaves} = '{registros[0][chaves]}'"
                else:
                    DataCalib =  datetime.datetime.strptime(registro[0]["DataCalibracao"], "%d/%m/%Y")
                    DataCalib = format(DataCalib,"%Y-%m-%d")
                    if DataCalib != lista_antes[0][chaves]:
                        Alteracao = True
                        campos_alt.append(chaves)
                        valores_alt.append(registros[0][chaves])
                        campos_dados = f"{chaves} = '{registros[0][chaves]}'"
        
    if Alteracao == False:
        if validacao == False:
            return validacao, msg, msgerro
        else:
            return False, 'O registro premaneceu com os dados anteriores.',''
    else:
        if ideqpto == 'new':
            records = caputra_maiorID('CalEqto_Eqtos', banco_de_dados)
            records = records.fetchall()
            ValoresBD = ''
            for row in records: myID = row[0]
            
            if myID is None: 
                myID = 0 
            else:
                myID = myID+1
                
            print(registro[0]["DataCalibracao"])
            DataCalib =  datetime.datetime.strptime(registro[0]["DataCalibracao"], "%m/%d/%Y")
            DiaVcto = DataCalib.day
            MesVcto = DataCalib.month + registro[0]["QtdMeses"] % 12
            
            AnoVcto = 0
            if MesVcto > 12: 
                MesVcto -= 12
                AnoVcto = 1
                
            if MesVcto < 10: MesVcto = "0" + str(MesVcto)
            if DiaVcto < 10: DiaVcto = "0" + str(DiaVcto)
                
            AnoVcto = AnoVcto + DataCalib.year + registro[0]["QtdMeses"] // 12
            
            DataVcto = '{}-{}-{}'.format(AnoVcto, MesVcto, DiaVcto)
            DataCalib = format(DataCalib,"%Y-%m-%d")
            
            ValoresBD = ""
            ValoresBD = ValoresBD + str(myID)

            for chaves in registros[0].keys():
                if chaves.upper() != 'ID' :
                    if chaves.upper() != 'DATACALIBRACAO':
                        if chaves.upper() != 'OS' and  chaves.upper() != 'QTDMESES':
                            ValoresBD = ValoresBD + f", '{registros[0][chaves]}'"
                    
                        else:
                            ValoresBD = ValoresBD + f", {registros[0][chaves]}"
                    campos_alt.append(chaves)
                    valores_alt.append(registros[0][chaves])
                        
            ValoresBD += f",'{DataCalib}', '{DataVcto}', null, null"
            print(ValoresBD)
            
            registroBD = inserir_banco('CalEqto_Eqtos',ValoresBD, banco_de_dados)
            
            if registroBD == False:
                return False, "Nao foi possivel realizar o registro desse item", msgerro

            strAlt = f'Registro'
            
            registroBD = registra_bd_alt(campos_alt,valores_alt,myID,email,strAlt)
            
            if registroBD == False:
                return False, "Nao foi possivel realizar o registro de alteracoes desse item", msgerro

            msg = 'Registro realizado com sucesso!'
        else:
            strAlt = f'Alteracao'
            condicao = f'id = {registros[0]["id"]}'
            registroBD = atualiza_dados(campos_dados,'CalEqto_Eqtos', condicao,banco_de_dados)
            
            if registroBD == False:
                return False, "Nao foi possivel deletar item", msgerro

            registroBD = registra_bd_alt(campos_alt,valores_alt,registros[0]["id"],email,strAlt)
            
            if registroBD == False:
                return False, "Nao realizar o registro das alteracoes desse item.", msgerro

            msg = 'Registro alterado com sucesso!'
            
        return validacao, msg, msgerro
    

def deleta_registro_eqto(ideqpto, email, OS):

    Alteracao = False
    servidor = 'bdnuvemwa.mysql.dbaas.com.br'
    bancodados = 'bdnuvemwa'
    usuario = "bdnuvemwa"
    senha = "W102030b!@"
    
    campos_alt= []
    valores_alt = []
    valores_antes_alt = []

    banco_de_dados = mysql_connection(servidor, usuario, senha, bancodados)
    validacao, msgerro = valida_log_edicao(email, OS)
           
    if validacao == False:
        return False, 'Seu login nao pode deletar itens dessa OS',''

    condicao = f"id = {ideqpto}"
    ValorDb = delete_banco('CalEqto_Eqtos', condicao, banco_de_dados)
    
    if ValorDb == False:
          return False, f'Nao foi possivel deletar a id {ideqto}',''

    condicao = f"idEqto = {ideqpto}"
    ValorDb = delete_banco('CalEqto_Alt',condicao, banco_de_dados)
    
    if ValorDb == False:
          return False, f'Nao foi possivel deletar as alteracoes dessa id',''

    
    msg = "Dado excluido com sucesso!"
    return validacao, msg, msgerro


if __name__ == '__main__':
   registro = []
   
   registro.append({
        "id": 'new',
        "Desc": 'NomeEqto3',
        "Tag": 'Tag3',
        "NumSerie": 'NumSerie3',
        "Fabricante": 'Nome Fabricante3',
        "Status": 'Ativo',
        "OS": 981,
        "Certificadora": 'CertificadoraEqto3',
        "QtdMeses":15,
        "DataCalibracao": "04/10/2024"
    })
   
   lista_retorno, validacao, msgerro = realiza_registro(registro[0]['id'], 'wagner.barreiro@enind.com.br', registro)
   #lista_retorno, validacao, msgerro = deleta_registro_eqto(registro[0]['id'], 'wagner.barreiro@enind.com.br', registro[0]['OS'])
   print(lista_retorno)
   print(validacao)
   print(msgerro)