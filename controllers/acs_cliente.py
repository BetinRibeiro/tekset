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
    total = db((db.empresa_cliente.empresa==empresa.id)&(db.empresa_cliente.excluido==False)).count()
    paginas = total//paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.empresa_cliente.empresa==empresa.id)&(db.empresa_cliente.excluido==False)).select(
      limitby=limites,orderby=~db.empresa_cliente.id|db.empresa_cliente.nome)
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa, usuario=usuario)

@auth.requires_login()
def cadastrar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)   
    if not 'Admi' in usuario.tipo:
        redirect(URL('index'))
    empresa =db.empresa(usuario.empresa)
    response.view = 'generic.html' # use a generic view
    request.function='Cadastro de empresa_cliente '
    db.empresa_cliente.empresa.default=usuario.empresa
    db.empresa_cliente.excluido.writable=False
    db.empresa_cliente.excluido.readable=False
    form = SQLFORM(db.empresa_cliente).process()
    if form.accepted:
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    return  dict(form=form)

@auth.requires_login()
def alterar():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not 'Admi' in usuario.tipo:
        redirect(URL('index'))
    empresa_cliente = db.empresa_cliente(request.args(0, cast=int))
    if empresa_cliente.empresa!=usuario.empresa:
        redirect(URL('index'))
    response.view = 'generic.html' # use a generic view
    request.function='Alterar empresa_cliente'
    form = SQLFORM(db.empresa_cliente, request.args(0, cast=int), deletable=False)
    if form.process().accepted:
        redirect(URL('index'))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    return dict(form=form)
