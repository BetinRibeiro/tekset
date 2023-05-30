# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
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
    total = db((db.sistema.empresa==empresa.id)&(db.sistema.excluido==False)).count()
    paginas = total//paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.sistema.empresa==empresa.id)&(db.sistema.excluido==False)).select(
      limitby=limites,orderby=~db.sistema.id|db.sistema.nome)
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, usuario=usuario)

@auth.requires_login()
def cadastrar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa =db.empresa(usuario.empresa)
    response.view = 'generic.html' # use a generic view
    request.function='Cadastro de sistema '
    db.sistema.empresa.default=usuario.empresa
    referencia = gerar_referencia()
    db.sistema.empresa_cliente.writable=False
    db.sistema.empresa_cliente.readable=False
    db.sistema.empresa_cliente.requires = IS_IN_DB(db((db.empresa_cliente.empresa==usuario.empresa)&(db.empresa_cliente.ativo==True)), 'empresa_cliente.id', '%(nome)s')
    db.sistema.referencia.readable=False
    db.sistema.referencia.default=referencia
    db.sistema.excluido.writable=False
    db.sistema.excluido.readable=False
    form = SQLFORM(db.sistema).process()
    if form.accepted:
        verifica_possibilidade_validacao(form.vars.id)
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    return  dict(form=form)

@auth.requires_login()
def alterar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    sistema = db.sistema(request.args(0, cast=int))
    if sistema.empresa!=usuario.empresa:
        redirect(URL('index'))
    response.view = 'generic.html' # use a generic view
    request.function='Alterar sistema'
    if 'Admi' in usuario.tipo:
        db.sistema.empresa_cliente.writable=True
        db.sistema.empresa_cliente.readable=True
        db.sistema.nome.writable=True
        db.sistema.nome.readable=True
        db.sistema.empresa_cliente.requires = IS_IN_DB(db((db.empresa_cliente.empresa==usuario.empresa)&(db.empresa_cliente.ativo==True)), 'empresa_cliente.id', '%(nome)s')
    else:
#         redirect(URL('index'))
        db.sistema.empresa_cliente.writable=False
        db.sistema.empresa_cliente.readable=True
        db.sistema.nome.writable=False
        db.sistema.nome.readable=True
#     db.sistema.empresa_cliente.writable=True
#     db.sistema.empresa_cliente.readable=True
#     db.sistema.empresa_cliente.requires = IS_IN_DB(db((db.empresa_cliente.empresa==usuario.empresa)&(db.empresa_cliente.ativo==True)), 'empresa_cliente.id', '%(nome)s')
    db.sistema.excluido.writable=False
    db.sistema.excluido.readable=False
    form = SQLFORM(db.sistema, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        verifica_possibilidade_validacao(form.vars.id)
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    return dict(form=form)

@auth.requires_login()
def analise():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    sistema = db.sistema(request.args(0, cast=int))
    if sistema.empresa!=usuario.empresa:
        redirect(URL('index'))
    return locals()

@auth.requires_login()
def mudat_status():
    response.view = 'generic.html' # use a generic view
    sistema = db.sistema(request.args(0, cast=int))
    variavel = request.args(1, cast=str)
    if "N" in sistema[variavel]:
        sistema[variavel]="SIM"
    else:
        sistema[variavel]="NÃO"
    sistema.update_record()

    return redirect(URL('analise', args=sistema.id))

@auth.requires_login()
def relatorio():
    sistema=db.sistema(request.args(0, cast=int))
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if usuario.empresa != sistema.empresa:
        redirect(URL('index'))
    return dict(sistema = sistema)


@auth.requires_login()
def registros_atividade():
    sistema = db.sistema(request.args(0, cast=int))
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    
    empresa = db.empresa(usuario.empresa)
    if sistema.empresa!=empresa.id:
        redirect(URL('index'))
        
    paginacao = 35
    if len(request.args) == 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL('erro', vars={
                  'msg':'Numero da página inválido'
                  }))
    if pagina <= 0:
        pagina = 1
    total = db((db.registro_atividade.sistema==sistema.id)).count()
    paginas = total//paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[colaborador.id,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.registro_atividade.sistema==sistema.id)).select(
      limitby=limites,orderby=~db.registro_atividade.id)
    consul=(request.args(1))
    liberado=True
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, consul=consul, liberado=liberado,empresa=empresa,sistema=sistema)




@auth.requires_login()
def acessar_cliente():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa =db.empresa(usuario.empresa)
    empresa_cliente = db.empresa_cliente(request.args(0, cast=int))
    if usuario.empresa!=empresa_cliente.empresa:
        redirect(URL('default','index'))
    paginacao = 35
    if len(request.args) == 1:
        pagina = 1
    else:
        try:
            pagina = int(request.args[1])
        except ValueError:
            redirect(URL(args=[empresa_cliente.id,1]))
    if pagina <= 0:
        pagina = 1
    total = db((db.sistema.empresa_cliente==empresa_cliente.id)&(db.sistema.excluido==False)).count()
    paginas = total//paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.sistema.empresa_cliente==empresa_cliente.id)&(db.sistema.excluido==False)).select(
      limitby=limites,orderby=~db.sistema.id|db.sistema.nome)
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa_cliente=empresa_cliente)
    

def cadastrar_com_cliente():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa =db.empresa(usuario.empresa)
    empresa_cliente = db.empresa_cliente(request.args(0, cast=int))
    if usuario.empresa!=empresa_cliente.empresa:
        redirect(URL('default','index'))
    response.view = 'generic.html' # use a generic view
    request.function='Cadastro de sistema '
    db.sistema.empresa.default=usuario.empresa
    referencia = gerar_referencia()
    db.sistema.empresa_cliente.readable=True
    db.sistema.empresa_cliente.default = empresa_cliente.id
    db.sistema.referencia.readable=False
    db.sistema.referencia.default=referencia
    db.sistema.excluido.writable=False
    db.sistema.excluido.readable=False
    form = SQLFORM(db.sistema).process()
    if form.accepted:
        verifica_possibilidade_validacao(form.vars.id)
        redirect(URL('acessar_cliente', args=empresa_cliente.id))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    return  dict(form=form)
