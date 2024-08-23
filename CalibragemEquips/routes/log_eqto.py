from ast import Global
from flask import Blueprint, render_template, request

log_eqto_route = Blueprint('log_eqto', __name__)


@log_eqto_route.route('/')
def abrir_pagina():
    #Abre a página de login
        nome_btn='Enviar'
        return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "")

@log_eqto_route.route('/conferencia')
def verificar_email():
    return "Validacao do Email"


@log_eqto_route.route('/', methods=['POST'])
def enviar_email():
    
    prefixoemail = request.form.get("CmplEmail")
    email = request.form.get("email")
    codigo = request.form.get("Codigo")
    nome_btn =  request.form.get("btnEnviar")

    #Verificando se a página deu algum retorno!
    if prefixoemail is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o prefixo de email")
    
    if email is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o dominio do email")
    
    if codigo is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o codigo")
    
    if nome_btn is None:
            return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o codigo")

    NaoPermitidos = f"SELECT,DELETE,INSERT,',*,%,{chr(34)},(,),TRUNCATE,DROP"
    palavras = NaoPermitidos.split(",")

    for palavra in palavras:
            if palavra in email.upper():
                mensagem = 'e-mail invalido.'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo, tipoalerta= "alert alert-warning", msg=mensagem)   
             
            elif palavra in prefixoemail.upper():
                mensagem = 'e-mail invalido.'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo,tipoalerta= "alert alert-warning",  msg=mensagem)
             
        
    if email != "@enind.com.br" and email != "@enindservicos.com.br":
            mensagem = 'e-mail invalido, por gentileza utilizar os disponiveis nas caixas.'
            return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo, msg=mensagem, tipoalerta= "alert alert-warning")

    
    if nome_btn == 'Enviar':
            nome_btn = "Validar"    
            mensagem = "Email enviado com sucesso!"    
            return render_template('log_eqto.html', prefemail=prefixoemail, nomebtn="Validar", cod_usado = codigo, msg=mensagem, tipoalerta= "alert alert-success")
    
    else:
           for palavra in palavras:
                if palavra in codigo.upper():
                    mensagem = 'Codigo invalido.'
                    return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo,tipoalerta= "alert alert-warning",  msg=mensagem)
                
           if not codigo.isnumeric():
                mensagem = 'Codigo inserido invalido'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo, msg=mensagem,tipoalerta= "alert alert-warning")


           if len(codigo) != 6:
                mensagem = 'Codigo inserido esta superior ou inferior a 6 digitos'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo,  msg=mensagem, tipoalerta= "alert alert-warning")   
           
#########################################################################################################################################################################
#################################################################### REENVIO DE E-MAIL ##################################################################################
#########################################################################################################################################################################           

@log_eqto_route.route('/reenvio', methods=['POST'])
def reenviar_email():
    
    prefixoemail = request.form.get("CmplEmail")
    email = request.form.get("email")
    codigo = request.form.get("Codigo")

    #Verificando se a página deu algum retorno!
    if prefixoemail is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o prefixo de email")
    
    if email is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o dominio do email")
    
    if codigo is None:
          return render_template('log_eqto.html', prefemail="", cod_usado = "", nomebtn= nome_btn, tipoalerta= "alert alert-light", msg = "Nao foi possivel pegar o codigo")
    
    NaoPermitidos = f"SELECT, DELETE, INSERT,',*,%,{chr(34)},(,)"
    palavras = NaoPermitidos.split(",")

    for palavra in palavras:
            if palavra in email.upper():
                mensagem = 'e-mail invalido.'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo, tipoalerta= "alert alert-warning", msg=mensagem)   
             
            elif palavra in prefixoemail.upper():
                mensagem = 'e-mail invalido.'
                return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo,tipoalerta= "alert alert-warning",  msg=mensagem)
             
        
    if email != "@enind.com.br" and email != "@enindservicos.com.br":
            mensagem = 'e-mail invalido, por gentileza utilizar os disponiveis nas caixas.'
            return render_template('log_eqto.html', prefemail=prefixoemail, cod_usado = codigo, msg=mensagem, tipoalerta= "alert alert-warning")

    
   
    nome_btn = "Validar"    
    mensagem = "Email enviado com sucesso!"    
    return render_template('log_eqto.html', prefemail=prefixoemail, nomebtn="Validar", cod_usado = codigo, msg=mensagem, tipoalerta= "alert alert-success")