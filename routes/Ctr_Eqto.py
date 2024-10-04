from flask import Blueprint, redirect, render_template, request
from database.equipamentos import lista_equipamentos
import funcoes.emails
from math import ceil


Ctr_Eqto_route = Blueprint('Ctr_Eqto', __name__)

@Ctr_Eqto_route.route('/<idlog>')
def lista_eqtos(idlog):
    #Lista os equipamentos
    validacao, msgerro, EndEmail = funcoes.emails.valida_token_email(idlog)
    
    global strToken
    strToken = idlog

    if validacao == True:
        qtdTotal = len(lista_equipamentos)
        qtdLinhas = int(ceil(qtdTotal / 3))
        return render_template('Ctr_Eqto.html', email=EndEmail, qtd_linhas=qtdLinhas, qtd_total=qtdTotal, equipamentos=lista_equipamentos)
    else:
        return redirect(f'/log_eqto')

@Ctr_Eqto_route.route('/<idlog>/edit/<ideqpto>')
def Editar(idlog, ideqpto):
    validacao, msgerro, EndEmail = funcoes.emails.valida_token_email(idlog)
    print(EndEmail)
    strToken = idlog
    if validacao == True:
        # A segunda validação serve para saber se o e-mail em questão está apto a realizar alterações
        listaEqtpo, validacao, msgerro = funcoes.emails.puxa_registro(ideqpto, EndEmail)
        
        print(listaEqtpo)
        print(validacao)
        print(msgerro)
        
        caminho_url = f'/Ctr_Eqto/{idlog}/edit/{ideqpto}'
        return render_template('Cad_Eqto.html', idlog = idlog, ideqpto = ideqpto ,  equipamentos = listaEqtpo, valid = validacao, email = EndEmail)
        
    else:
        return redirect(f'/log_eqto')

@Ctr_Eqto_route.route('/<idlog>/delete/<ideqpto>')
def Deletar(idlog, ideqpto):
    validacao, msgerro, EndEmail = funcoes.emails.valida_token_email(idlog)
    print(EndEmail)
    strToken = idlog
    if validacao == True:
        # A segunda validação serve para saber se o e-mail em questão está apto a realizar alterações
        listaEqtpo, validacao, msgerro = funcoes.emails.puxa_registro(ideqpto, EndEmail)
        
        print(listaEqtpo)
        print(validacao)
        print(msgerro)
        
        caminho_url = f'/Ctr_Eqto/{idlog}/edit/{ideqpto}'
        return render_template('Cad_Eqto.html', idlog = idlog, ideqpto = ideqpto ,  equipamentos = listaEqtpo, valid = validacao, email = EndEmail)
        
    else:
        return redirect(f'/log_eqto')

@Ctr_Eqto_route.route('/<idlog>/edit/<ideqpto>', methods=['POST'])
def Registrar_Eqpto(idlog, ideqpto):
    
    reqID = request.form.get("txtID")
    reqNome = request.form.get("txtNome")
    reqNumOS = request.form.get("txtNumOS")
    reqTag = request.form.get("txtTag")
    reqNumSerie =  request.form.get("txtNumSerie")
    reqStatus =  request.form.get("cboxStatus")
    reqMeses = request.form.get("txtMeses")
    reqCert = request.form.get("txtNomeCert")
    
    registro =[]
    registro.append({
        "id": request.form.get("txtID"),
        "Desc": request.form.get("txtNome"),
        "NumSerie": request.form.get("txtNumSerie"),
        "Tag": request.form.get("txtTag"),
        "Fabricante": eqto["Fabricante"],
        "Status": request.form.get("cboxStatus"),
        "OS": request.form.get("txtNumOS"),
        "Certificadora": request.form.get("txtNomeCert"),
        "QtdMeses": request.form.get("txtMeses"),

      })
    
    print('passou pela fase do registro')

    validacao, msgerro, EndEmail = funcoes.emails.valida_token_email(idlog)
    print(EndEmail)
    strToken = idlog
    if validacao == True:
        # A segunda validação serve para saber se o e-mail em questão está apto a realizar alterações
        listaEqtpo, validacao, msgerro = funcoes.emails.puxa_registro(ideqpto, EndEmail)
        
        print(listaEqtpo)
        print(validacao)
        print(msgerro)
        
        caminho_url = f'/Ctr_Eqto/{idlog}/edit/{ideqpto}'
        return render_template('Cad_Eqto.html', idlog = idlog, ideqpto = ideqpto ,  equipamentos = listaEqtpo, valid = validacao, email = EndEmail)
        
    else:
        return redirect(f'/log_eqto')