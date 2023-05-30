# -*- coding: utf-8 -*-

db.define_table('registro_atividade',
                Field('empresa','reference empresa', writable=False, label='Empresa'),
                Field('sistema','reference sistema', writable=True, label='Sistema'),
                Field('circunspecto','reference auth_user', writable=True, label='Circunspecto'),
                Field('tipo', 'string', label='Tipo', writable=True),
                Field('referencia', 'string', label='Referência', writable=False),
                Field('data_inicial', 'date', label='Data', default=request.now),
#na versao do sistema não tem responsavel 
                Field('responsavel', 'string', label='Responsável'),
                Field('descricao', 'string', label='Descrição'),

#atributos somente no capa
                Field('identificacao_desvio_cm', 'string', label='Ident. Desvio ou CM'),

#atributo CONTROLE_MUDANCA

                Field('registro_mudanca', 'string', label='Reg. Mudança'),
#atributo CONTROLE_MUDANCA, REVISAO_PROCEDIMENTO
                Field('motivo', 'string', label='Motivo'),

#atributo CONTROLE_MUDANCA
                Field('procedimento_implantacao', 'string', label='Procedimento Implantacao'),

#atributo CONTROLE_MUDANCA
                Field('analise_critica', 'string', label='Analise Critica'),

#atributo BACKUPS
                Field('hora_processo', 'string', label='Hora'),

#atributo BACKUPS
                Field('local_backup', 'string', label='Local Backup'),
                
#atributo REVISAO_PROCEDIMENTO
                Field('identificacao_pop', 'string', label='Iden. POP'),
                
#atributo REVISAO_PROCEDIMENTO
                Field('motivo', 'string', label='Motivo'),
                
#atributo REGISTRO_DESVIO_QUALIDADE
                Field('area_desvio', 'string', label='Area do Desvio'),
                
#atributo REGISTRO_DESVIO_QUALIDADE
                Field('tipo_desvio', 'string', label='Tipo do Desvio'),
                
#atributo REGISTRO_DESVIO_QUALIDADE
                Field('avaliacao_criticidade', 'string', label='AV Criticidade'),
                
#atributo REGISTRO_DESVIO_QUALIDADE
                Field('ciente_desvio', 'string', label='Ciente do Desvio'),
#atributo REGISTRO_DESVIO_QUALIDADE
                Field('responsavel_acao', 'string', label='Resp. Ação'),
#atributo VERSAO_SISTEMA
                Field('versao_inicial', 'string', label='Versão Inicial'),
#atributo VERSAO_SISTEMA
                Field('nova_versao', 'string', label='Nova Versão'),
                
                
                
#atributo REVISAO_PROCEDIMENTO e VERSAO_SISTEMA
                Field('analise_critica_bpf', 'string', label='Analise Critica BPX'),
                
#atributo CAPA, CONTROLE_MUDANCA
                Field('eficaz', 'string', label='Eficaz'),
                Field('data_final', 'date', label='Data Final', default=request.now),
                
                
#atributo CAPA
                Field('responsavel_avaliacao', 'string', label='Responsável Av'),
#atributo CAPA
                Field('email_responsalvel', 'string', label='Email'),
                
                Field('observacao', 'text', label='Observação', writable=False, readable=False),
                Field('data_finalizacao', 'date', writable=False, readable=False, label='Data Finalização'),
                Field('finalizado', 'boolean', writable=True, readable=True, default=False),
                Field('excluido', 'boolean', writable=True, readable=True, default=False),
                auth.signature,
                format='%(descricao)s')

db.registro_atividade.id.writable=False
db.registro_atividade.id.readable=False
db.registro_atividade.data_inicial.requires = IS_DATE(format=('%d-%m-%Y'),
                   error_message='Padrão de data 28-08-1963')
db.registro_atividade.data_final.requires = IS_DATE(format=('%d-%m-%Y'),
                   error_message='Padrão de data 28-08-1963')

db.registro_atividade.data_finalizacao.requires = IS_DATE(format=('%d-%m-%Y'),
                   error_message='Padrão de data 28-08-1963')




db.define_table('gestao_de_risco',
                Field('empresa','reference empresa', writable=False, readable=False, label='empresa'),
                Field('registro_atividade','reference registro_atividade', writable=False, readable=True, label='CAPA'),
                Field('circunspecto','reference auth_user', writable=True, label='Circunspecto'),
                Field('cenario_risco', 'string', label='Cenario Risco',requires = IS_UPPER()),
                Field('efeito_risco', 'string', label='Efeito Risco',requires = IS_UPPER()),
                Field('severidade', 'string', label='Severidade'),
                Field('probabilidade', 'string', label='Probabilidade'),
                Field('classe_risco', 'string', writable=False, readable=False, label='Classe Risco'),
                Field('detectibilidade', 'string', label='Detectibilidade'),
                Field('prioridade', 'string', writable=False, readable=False, label='Prioridade'),
                Field('medidas', 'string', label='Medidas'),
                Field('responsavel_acao', 'string', label='Responsavel pela Ação'),
                Field('email_responsavel_acao', 'string', label='Email Responsavél'),
                Field('data_prevista', 'date', label='Data Prevista', default=request.now),

                Field('observacao', 'text', label='Observação', writable=True, readable=False),
                Field('ativo', 'boolean', writable=False, readable=False, default=True),
                Field('excluido', 'boolean', writable=False, readable=False, default=False),
                Field('solucionada', 'boolean', writable=True, readable=True, default=False),
                auth.signature,
                format='%(cenario_risco)s')

db.gestao_de_risco.id.writable=False
db.gestao_de_risco.id.readable=False
db.gestao_de_risco.data_prevista.requires = IS_DATE(format=('%d-%m-%Y'),
                   error_message='Padrão de data 28-08-1963')
db.sistema.id.writable=False
db.sistema.id.readable=False


db.gestao_de_risco.severidade.requires = IS_IN_SET(['1 - Baixa','2 - Média','3 - Alta'])
db.gestao_de_risco.probabilidade.requires = IS_IN_SET(['1 - Baixa','2 - Média','3 - Alta'])
db.gestao_de_risco.classe_risco.requires = IS_IN_SET(['A - Alta','B - Baixa','M - Média'])
db.gestao_de_risco.detectibilidade.requires = IS_IN_SET(['1 - Alta','2 - Média','3 - Baixa'])
db.gestao_de_risco.prioridade.requires = IS_IN_SET(['A - Alta','M - Média','B - Baixa'])
db.gestao_de_risco.email_responsavel_acao.requires = IS_EMAIL(error_message='Email Invalido!')
