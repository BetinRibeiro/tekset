# -*- coding: utf-8 -*-



db.define_table('sistema',
                Field('empresa','reference empresa', writable=False, readable=False, label='Empresa'),
                Field('empresa_cliente','reference empresa_cliente', writable=False, readable=False, label='Empresa'),
                Field('referencia', 'string', writable=False, label='Referencia'),
                Field('nome', 'string', label='Nome do Sistema',requires = IS_UPPER()),
                Field('versao', 'string', label='Versão',requires = IS_UPPER()),
                Field('versao_atual', 'string', label='Versão atual',requires = IS_UPPER()),
                Field('equipamento', 'string', label='Equipamento',requires = IS_UPPER()),
                Field('tag', 'string', label='TAG',requires = IS_UPPER()),
                Field('setor', 'string', label='Setor',requires = IS_UPPER()),
                Field('fornecedor', 'string', label='Fornecedor',requires = IS_UPPER()),
                Field('dono_sistema', 'string', label='Dono Sistema',requires = IS_UPPER()),
                Field('dono_processo', 'string', label='Dono Processo',requires = IS_UPPER()),
                Field('classificacao_software', 'string', label='Classificação Software',default="Configurado"),
                Field('classificacao_hardware', 'string', label='Classificação Hardware',default="Componentes Padrão de Hardware"),
                Field('status_sistema', 'string', label='Status Sistema',default="Em uso"),
                Field('status_validacao', 'string', label='Status Validação',default="Em validação"),
                Field('tipo_sistema', 'string', label='Tipo Sistema',default="EMBARCADO"),
                Field('tipo_validacao', 'string', label='Tipo Validação',default="Concorrente"),
                Field('controle_acesso', 'string', label='Controle de Acesso'),
                Field('trilha_auditoria', 'string', label='Trilha Auditoria'),
                Field('interface_externa', 'string', label='Interface Externa'),
                Field('quantidade_usuarios', 'integer', label='Quantidade Usuários',default="0"),
                Field('impacto', 'string', label='Impacto na Qualidade do Produto',default="N/A"),
                Field('possibilidade_validacao', 'string', label='Possibilidade de Validação', writable=False,default="NÃO NECESSIDADE DE VALIDAÇÃO"),
                Field('data_relatorio', 'date', writable=True, readable=True, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                #perguntas uma lista nos validadores
                Field('p01', 'string', writable=False, readable=False, default="NÃO"),
                Field('p02', 'string', writable=False, readable=False, default="NÃO"),
                Field('p03', 'string', writable=False, readable=False, default="NÃO"),
                Field('p04', 'string', writable=False, readable=False, default="NÃO"),
                Field('p05', 'string', writable=False, readable=False, default="NÃO"),
                Field('p06', 'string', writable=False, readable=False, default="NÃO"),
                Field('p07', 'string', writable=False, readable=False, default="NÃO"),
                Field('p08', 'string', writable=False, readable=False, default="NÃO"),
                Field('p09', 'string', writable=False, readable=False, default="NÃO"),
                Field('p10', 'string', writable=False, readable=False, default="NÃO"),
                Field('p11', 'string', writable=False, readable=False, default="NÃO"),
                Field('p12', 'string', writable=False, readable=False, default="NÃO"),
                Field('p13', 'string', writable=False, readable=False, default="NÃO"),
                Field('p14', 'string', writable=False, readable=False, default="NÃO"),
                Field('p15', 'string', writable=False, readable=False, default="NÃO"),

                Field('necessidade_validacao', 'string', writable=False, readable=True, label='Validação e Revista Periodica',default="VALIDAR"),
                Field('data_prox_revisao', 'date', writable=False, readable=False, default=request.now, requires = IS_DATE(format=('%d-%m-%Y'))),
                Field('observacao', 'text', label='Observação', writable=True, readable=False),
                Field('ativo', 'boolean', writable=True, readable=True, default=True),
                Field('excluido', 'boolean', writable=True, readable=True, default=False),
                auth.signature,
                format='%(nome)s')

db.sistema.id.writable=False
db.sistema.id.readable=False

db.sistema.classificacao_software.requires = IS_IN_SET(['Infraestrutura','Não-Configurado','Configurado','Customizado'])
db.sistema.classificacao_hardware.requires = IS_IN_SET(['Componentes Padrão de Hardware','Componentes Customizados Embutidos de Hardware', 'Outros'])
db.sistema.status_sistema.requires = IS_IN_SET(['Em implementacao','Em uso','Em upgrade','Descontinuado'])
db.sistema.status_validacao.requires = IS_IN_SET(['Em validação','Não validado','Em Upgrade','Validado'])
db.sistema.tipo_sistema.requires = IS_IN_SET(['CDS','CRM','EMBARCADO','ERP','LIMS','MES','STAND ALONE','WMS'])
db.sistema.tipo_validacao.requires = IS_IN_SET(['Prospectiva','Retrospectiva','Concorrente','Periodica'])
db.sistema.controle_acesso.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.trilha_auditoria.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.interface_externa.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.impacto.requires = IS_IN_SET(['INDIRETO','DIRETO','N/A'])
db.sistema.possibilidade_validacao.requires = IS_IN_SET(['VALIDAVEL','NECESSITA DE UPGRADE'])
db.sistema.necessidade_validacao.requires = IS_IN_SET(['NÃO NECESSIDADE DE VALIDAÇÃO','VALIDAR'])

db.sistema.p01.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p02.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p03.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p04.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p05.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p06.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p07.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p08.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p09.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p10.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p11.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p12.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p13.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p14.requires = IS_IN_SET(['SIM','NÃO'])
db.sistema.p15.requires = IS_IN_SET(['SIM','NÃO'])


db.sistema.p01.readable=False
db.sistema.p02.readable=False
db.sistema.p03.readable=False
db.sistema.p04.readable=False
db.sistema.p05.readable=False
db.sistema.p06.readable=False
db.sistema.p07.readable=False
db.sistema.p08.readable=False
db.sistema.p09.readable=False
db.sistema.p10.readable=False
db.sistema.p11.readable=False
db.sistema.p12.readable=False
db.sistema.p13.readable=False
db.sistema.p14.readable=False
db.sistema.p15.readable=False

db.sistema.p01.writable=False
db.sistema.p02.writable=False
db.sistema.p03.writable=False
db.sistema.p04.writable=False
db.sistema.p05.writable=False
db.sistema.p06.writable=False
db.sistema.p07.writable=False
db.sistema.p08.writable=False
db.sistema.p09.writable=False
db.sistema.p10.writable=False
db.sistema.p11.writable=False
db.sistema.p12.writable=False
db.sistema.p13.writable=False
db.sistema.p14.writable=False
db.sistema.p15.writable=False
