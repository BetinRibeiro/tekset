# -*- coding: utf-8 -*-




if auth.user:
    response.menu = [
        (T('Home'), False, URL('acs_empresa', 'index'), []),
#         (T('Empresas'), False, URL('acs_cliente', 'index'), []),
#         (T('Usuarios'), False, URL('acs_usuario', 'index'), []),
#         (T('Inventario'), False, URL('acs_sistema', 'index'), []),
#         (T('Registros'), False, URL('acs_registro_atividade','todos_registros'), []),
#         (T('Alterar'), False, URL('acs_empresa', 'alterar'), []),
    ]
else:
    
    response.menu = [
        (T('Home'), False, URL('default', 'index'), [])
    ]
