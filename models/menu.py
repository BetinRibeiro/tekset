# -*- coding: utf-8 -*-


response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]


if auth.user:
    response.menu = [
        (T('Empresa'), False, URL('acs_empresa', 'index'), []),
        (T('Clientes'), False, URL('acs_cliente', 'index'), []),
        (T('Colaboradores'), False, URL('acs_usuario', 'index'), []),
        (T('Sistemas'), False, URL('acs_sistema', 'index'), []),
    ]
