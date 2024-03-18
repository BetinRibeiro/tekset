# -*- coding: utf-8 -*-

lista_registro_atividade = [
	'1001 - CAPA - AÇÕES CORRETIVAS E PREVENTIVAS',
	'1002 - CM   - CONTROLE DE MUDANÇA',
	'1003 - BK   - BACKUPS',
	'1004 - RT   - REGISTRO DE TREINAMENTO',
	'1005 - RP   - REVISÃO DE PROCEDIMENTO',
	'1006 - RDQ  - REGISTRO DE DESVIO DA QUALIDADE',
	'1007 - VS   - VERSÃO DO SISTEMA',
	'1008 - RVP  - REVISÃO PERIODICA']

def retorna_atividade(tipo):
    tipo = str(tipo)
    
    # Procurar o tipo na lista e retornar a atividade correspondente
    for row in lista_registro_atividade:
        if tipo in row:
            return row
    
    # Caso o tipo não seja encontrado, retornar None
    return None
