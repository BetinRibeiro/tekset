# -*- coding: utf-8 -*-
@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('acs_empresa','cadastrar'))
    elif usuario.tipo=="Atendente":
        redirect(URL('acs_registro','index'))
    elif usuario.tipo=="Representante":
        redirect(URL('acs_representante','index'))
    empresa = db.empresa(usuario.empresa)
    empresa_cliente= db.empresa_cliente(request.args(0, cast=int))
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
    total = db((db.usuario_empresa.empresa_cliente==empresa_cliente.id)).count()
    paginas = total//paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[empresa_cliente.id,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.usuario_empresa.empresa_cliente==empresa_cliente.id)).select(
      limitby=limites,orderby=~db.usuario_empresa.id)
    consul=(request.args(1))
    liberado=True
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, consul=consul, liberado=liberado,empresa=empresa,usuario=usuario,empresa_cliente=empresa_cliente)


@auth.requires_login()
def cadastrar():
    response.view = 'generic.html' # use a generic view
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if not usuario:
        redirect(URL('acs_empresa','cadastrar'))
    empresa_cliente= db.empresa_cliente(request.args(0, cast=int))
    
            
            
    empresa = db.empresa(usuario.empresa)
    form = SQLFORM(db.auth_user).process()
    if form.accepted:
        response.flash = 'Formulario aceito'
        redirect(URL('vincular_login', args=[empresa_cliente.id,form.vars.id]))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    else:
        response.flash = 'Preencha o formulario'
    #2 consultas no banco
    return  dict(form=form)

@auth.requires_login()
def alterar():
    try:
        response.view = 'generic.html' # use a generic view
        request.function='Alterar'
        usuario_empresa= db.usuario_empresa(request.args(0, cast=int))
        usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if not "Admin" in usuario.tipo:
            if not "Coor" in usuario.tipo:
                response.flash = 'Você não tem autorização'
                redirect(URL('index'))
        form = SQLFORM(db.usuario_empresa, request.args(0, cast=int), deletable=False)
        if form.process().accepted:
            redirect(URL('alterar_user', args=usuario_empresa.usuario))
        elif form.errors:
            response.flash = 'Formulario não aceito'
    except:
        redirect(URL('alterar_user', args=usuario_empresa.usuario))
    return dict(form=form)

@auth.requires_login()
def alterar_user():
    try:
        response.view = 'generic.html' # use a generic view
        request.function='Alterar'
        usuario = db.auth_user(request.args(0, cast=int))
        usuario_retorno = db.usuario_empresa(db.usuario_empresa.usuario==usuario.id)
        usuario_empresa = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
        if not "Admin" in usuario_empresa.tipo:
            response.flash = 'Você não tem autorização'
            redirect(URL('index'))
        form = SQLFORM(db.auth_user, request.args(0, cast=int), deletable=False)
        if form.process().accepted:
            redirect(URL('index'))
        elif form.errors:
            response.flash = 'Formulario não aceito'
    except:
        redirect(URL('index', args=usuario_retorno.empresa_cliente))
    return dict(form=form)

@auth.requires_login()
def vincular_login():
    response.view = 'generic.html' # use a generic view
    empresa_cliente = db.empresa_cliente(request.args(0, cast=int))
    usuario = db.auth_user(request.args(1, cast=int))
    db.usuario_empresa.empresa_cliente.default = request.args(0, cast=int)
    db.usuario_empresa.usuario.default = request.args(1, cast=int)
    db.usuario_empresa.tipo.default = "Analista Cliente"
    
    

    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    if 'Coordenador' in usuario.tipo:
        if 'Empresa' in usuario.tipo:
            db.usuario_empresa.tipo.requires = IS_IN_SET(['Analista Empresa', 'Analista Cliente'])
            db.usuario_empresa.tipo.deafult='Analista Empresa'
        else:
            db.usuario_empresa.tipo.requires = IS_IN_SET(['Analista Cliente'])
            db.usuario_empresa.tipo.deafult='Analista Cliente'
    db.usuario_empresa.tipo.requires = IS_IN_SET(['Coordenador Cliente', 'Analista Cliente'])
    form = SQLFORM(db.usuario_empresa).process()
    if form.accepted:
        redirect(URL('index', args=request.args(0, cast=int)))
    elif form.errors:
        response.flash = 'Formulario não aceito'
    #2 consultas no banco
    return  dict(form=form)


@auth.requires_login()
def registros_atividade():
    colaborador = db.usuario_empresa(request.args(0, cast=int))
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    
    empresa = db.empresa(usuario.empresa)
        
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
    total = db((db.registro_atividade.modified_by==colaborador.usuario)).count()
    paginas = total//paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[colaborador.id,paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.registro_atividade.modified_by==colaborador.usuario)).select(
      limitby=limites,orderby=~db.registro_atividade.id)
    consul=(request.args(1))
    liberado=True
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, consul=consul, liberado=liberado,empresa=empresa,usuario=colaborador)
