# -*- coding: utf-8 -*-

@auth.requires_login()
def index():
    usuario = db.usuario_empresa(db.usuario_empresa.usuario==auth.user.id)
    empresa =db.empresa(usuario.empresa)
    if usuario.ativo==False:
        redirect(URL('acs_mensagem','usuario_bloqueado'))
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
    total = db((db.registro_atividade.circunspecto==auth.user.id)&(db.registro_atividade.excluido==False)).count()
    paginas = total//paginacao
    if total%paginacao:
        paginas+=1
    if total==0:
        paginas=1
    if pagina > paginas:
        redirect(URL(args=[paginas]))
    limites = (paginacao*(pagina-1), (paginacao*pagina))
    registros = db((db.registro_atividade.circunspecto==auth.user.id)&(db.registro_atividade.excluido==False)).select(
      limitby=limites,orderby=db.registro_atividade.finalizado|~db.registro_atividade.id)
    return dict(rows=registros, pagina=pagina, paginas=paginas, total=total, empresa=empresa)
