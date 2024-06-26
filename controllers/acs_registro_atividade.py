# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa =db.empresa(usuario.empresa)
    tipo = int(request.args[0])
    tipo_descricao = retorna_atividade(tipo)
    if usuario.ativo==False:
        redirect(URL('default','index'))
    paginacao = 35
    if len(request.args) == 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL(args=[tipo,1]))
    if pagina <= 0:
        pagina = 1
    total = db((db.registro_atividade.empresa==empresa.id)&(db.registro_atividade.excluido==False)&(db.registro_atividade.tipo.contains(tipo))).count()
    paginas = total//paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[tipo,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.registro_atividade.empresa==empresa.id)&(db.registro_atividade.excluido==False)&(db.registro_atividade.tipo.contains(tipo))).select(
      limitby=limites,orderby=db.registro_atividade.finalizado|db.registro_atividade.data_inicial|db.registro_atividade.id)
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, tipo=tipo,tipo_descricao=tipo_descricao)



@auth.requires_login()
def cadastrar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa =db.empresa(usuario.empresa)
    response.view = 'generic.html' # use a generic view
    tipo = int(request.args[0])
    db.registro_atividade.empresa.default=usuario.empresa
    db.registro_atividade.excluido.writable=False
    db.registro_atividade.excluido.readable=False
    db.registro_atividade.circunspecto.writable=True
    db.registro_atividade.circunspecto.readable=True
    
    db.registro_atividade.circunspecto.requires = IS_IN_DB(db((db.usuario_empresa.empresa==usuario.empresa)&(db.usuario_empresa.ativo==True)), 'usuario_empresa.usuario', '%(nome)s')
    db.registro_atividade.sistema.requires = IS_IN_DB(db((db.sistema.empresa==usuario.empresa)&(db.sistema.ativo==True)&(db.sistema.excluido==False)), 'sistema.id', '%(nome_empresa)s - %(nome)s')
    atualiza_nomes_usuarios(usuario.empresa)
    db.registro_atividade.responsavel_avaliacao.requires = IS_IN_DB(db((db.usuario_empresa.empresa==usuario.empresa)&(db.usuario_empresa.ativo==True)), 'usuario_empresa.nome', '%(nome)s')
    db.registro_atividade.responsavel_acao.requires = IS_IN_DB(db((db.usuario_empresa.empresa==usuario.empresa)&(db.usuario_empresa.ativo==True)), 'usuario_empresa.nome', '%(nome)s')
    valor_tipo = retorna_atividade(tipo)
    request.function=f'Cadastro {valor_tipo[11:]} '
    validador(tipo)
    db.registro_atividade.tipo.default=valor_tipo
    referencia = gerar_referencia()
    db.registro_atividade.referencia.default=referencia
    form = SQLFORM(db.registro_atividade).process()
    if form.accepted:
        disparar_email(form.vars.id)
        redirect(URL('index',args=tipo))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    return  dict(form=form)



@auth.requires_login()
def alterar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    registro_atividade = db.registro_atividade(request.args(0, cast=int))
    tipo = registro_atividade.tipo[:4]
    if registro_atividade.empresa!=usuario.empresa:
        redirect(URL('index',args=tipo))
    response.view = 'generic.html' # use a generic view
    request.function=f'Alterar {registro_atividade.tipo[11:]}'
    validador(tipo)
    atualiza_nomes_usuarios(usuario.empresa)
    db.registro_atividade.responsavel_avaliacao.requires = IS_IN_DB(db((db.usuario_empresa.empresa==usuario.empresa)&(db.usuario_empresa.ativo==True)), 'usuario_empresa.nome', '%(nome)s')
    db.registro_atividade.responsavel_acao.requires = IS_IN_DB(db((db.usuario_empresa.empresa==usuario.empresa)&(db.usuario_empresa.ativo==True)), 'usuario_empresa.nome', '%(nome)s')
    db.registro_atividade.sistema.requires = IS_IN_DB(db((db.sistema.empresa==usuario.empresa)&(db.sistema.ativo==True)), 'sistema.id', '%(nome)s')
    
    db.registro_atividade.circunspecto.writable=True
    db.registro_atividade.circunspecto.readable=True
    
    db.registro_atividade.circunspecto.requires = IS_IN_DB(db((db.usuario_empresa.empresa==usuario.empresa)&(db.usuario_empresa.ativo==True)), 'usuario_empresa.usuario', '%(nome)s')
    
    total = db((db.gestao_de_risco.registro_atividade==registro_atividade.id)&(db.gestao_de_risco.solucionada==False)).count()
    
    if total==0 and ("1001" in registro_atividade.tipo):
        db.registro_atividade.eficaz.writable=True
        db.registro_atividade.eficaz.readable=True
    else:
        db.registro_atividade.eficaz.writable=False
        db.registro_atividade.eficaz.readable=False
    if registro_atividade.finalizado==True:
        bloqueia_altreracoes()
        db.registro_atividade.data_finalizacao.writable=True
        db.registro_atividade.data_finalizacao.readable=True
    else:
        db.registro_atividade.data_finalizacao.writable=False
        db.registro_atividade.data_finalizacao.readable=False
        

    db.registro_atividade.sistema.writable=False
    db.registro_atividade.sistema.readable=True
    db.registro_atividade.excluido.writable=False
    db.registro_atividade.excluido.readable=False
    form = SQLFORM(db.registro_atividade, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        disparar_email(form.vars.id)
        redirect(URL('index',args=tipo))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    return dict(form=form)


@auth.requires_login()
def gestao_risco():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario.empresa)
    registro_atividade = db.registro_atividade(request.args(0, cast=int))
    if registro_atividade.empresa!=empresa.id:
        redirect(URL('default','index'))
    if not "CAPA" in registro_atividade.tipo:
        redirect(URL('index', args="1001"))
    paginacao = 50
    if len(request.args)==1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL(args=[registro_atividade.id,1]))
    #2
    if pagina<=0:
        pagina=1
    #150
    total = db(db.gestao_de_risco.registro_atividade==registro_atividade.id).count()
    #3
    paginas = total//paginacao
    if total%paginacao:
        paginas +=1
    if total==0:
        paginas=1
    if pagina>paginas:
        redirect(URL(args[registro_atividade.id,paginas]))
    limites = (paginacao*(pagina-1),paginacao*(pagina))
    registros = db(db.gestao_de_risco.registro_atividade==registro_atividade.id).select(limitby=limites, orderby=~db.gestao_de_risco.id)
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, registro_atividade=registro_atividade,usuario=usuario)


@auth.requires_login()
def cadastrar_gr():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario.empresa)
    registro_atividade = db.registro_atividade(request.args(0, cast=int))
    if registro_atividade.empresa!=empresa.id:
        redirect(URL('default','index'))
    if not "CAPA" in registro_atividade.tipo:
        redirect(URL('index', args="1001"))
    response.view = "generic.html"
    request.function="Cadastrar Gestão de Risco"
    db.gestao_de_risco.registro_atividade.default = registro_atividade.id
    
    db.gestao_de_risco.circunspecto.writable=True
    db.gestao_de_risco.circunspecto.readable=True
    
    db.gestao_de_risco.circunspecto.requires = IS_IN_DB(db((db.usuario_empresa.empresa==usuario.empresa)&(db.usuario_empresa.ativo==True)), 'usuario_empresa.usuario', '%(nome)s')
    form = SQLFORM(db.gestao_de_risco).process()
    if form.accepted:
        calcula_classe_risco_prioridade(form.vars.id)
        a=disparar_email_gr(form.vars.id)
        redirect(URL('gestao_risco',args=[registro_atividade.id,a]))
    elif form.errors:
        response.flash="Formulario Não Aceito"
    return dict(form=form)

@auth.requires_login()
def alterar_gr():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa = db.empresa(usuario.empresa)
    gestao_de_risco = db.gestao_de_risco(request.args(0, cast=int))
    registro_atividade = db.registro_atividade(gestao_de_risco.registro_atividade)
    if registro_atividade.empresa!=empresa.id:
        redirect(URL('default','index'))
    response.view = "generic.html"
    request.function="Alterar Gestão de Risco"
    
    db.gestao_de_risco.circunspecto.writable=True
    db.gestao_de_risco.circunspecto.readable=True
    
    db.gestao_de_risco.circunspecto.requires = IS_IN_DB(db((db.usuario_empresa.empresa==usuario.empresa)&(db.usuario_empresa.ativo==True)), 'usuario_empresa.usuario', '%(nome)s')
    form = SQLFORM(db.gestao_de_risco, request.args(0, cast=int))
    if form.process().accepted:
        calcula_classe_risco_prioridade(form.vars.id)
        a=disparar_email_gr(form.vars.id)
        redirect(URL('gestao_risco',args=[registro_atividade.id,1,a]))
    elif form.errors:
        response.flash="Formulario Não Aceito"
    return dict(form=form)


@auth.requires_login()
def relatorio():
    registro_atividade = db.registro_atividade(request.args(0, cast=int))
    lista_gr = db(db.gestao_de_risco.registro_atividade == registro_atividade.id).select()
    layout = f'relatorio/{registro_atividade.tipo[:4]}.html'
    return locals()



@auth.requires_login()
def todos_registros():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa =db.empresa(usuario.empresa)
    if usuario.ativo==False:
        redirect(URL('default','index'))
    paginacao = 35
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL(args=[1]))
    if pagina <= 0:
        pagina = 1
    total = db((db.registro_atividade.empresa==empresa.id)&(db.registro_atividade.excluido==False)).count()
    paginas = total//paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[tipo,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.registro_atividade.empresa==empresa.id)&(db.registro_atividade.excluido==False)).select(
      limitby=limites,orderby=~db.registro_atividade.id|db.registro_atividade.descricao)
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)


@auth.requires_login()
def modificar_status():
    #recebe a gestãod e risco pelo argumento 0
    gestao_de_risco = db.gestao_de_risco(request.args(0, cast=int))
    #verifica se a gestão de risco esta verdadeira
    if gestao_de_risco.solucionada==True:
        #modifica para false
        gestao_de_risco.solucionada=False
    #caso contrario 
    else:
        #modifica para True
        gestao_de_risco.solucionada=True
    #salva no banco de dados a alteração feira
    gestao_de_risco.update_record()
    #o retorno é um redirecionamento para a lista de gr passando como argumento o
    #registro de atividade CAPA como arumento ZERO
    return redirect(URL('gestao_risco',args=[gestao_de_risco.registro_atividade]))


def especifica():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa =db.empresa(usuario.empresa)
    paginacao = 35
    if len(request.args) == 0:
        pagina = 1
    else:
        try:
            pagina = int(request.args[0])
        except ValueError:
            redirect(URL(args=[1]))
    if pagina <= 0:
        pagina = 1
    total = db((db.registro_atividade.modified_by==usuario.id)|(db.registro_atividade.created_by==usuario.id)).count()
    paginas = total//paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[tipo,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.registro_atividade.modified_by==usuario.id)|(db.registro_atividade.created_by==usuario.id)).select(
      limitby=limites,orderby=db.registro_atividade.finalizado|db.registro_atividade.data_inicial|db.registro_atividade.id)
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)
