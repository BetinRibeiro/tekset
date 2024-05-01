# -*- coding: utf-8 -*-
import datetime

#otimizada
def form_num(number):
    return "{:02d}".format(number)

#função enterior a otimização
# def gerar_referencia():
#     hoje = datetime.date.today()
#     total = db(db.registro_atividade.id>0).count()
#     if total==0:
#         total=1000000
#     else:
#         ultimo = db(db.registro_atividade.id>0).select().last()
#         total = ultimo.id+1000000
#     codigo = f'{hoje.year}{form_num(hoje.month)}{form_num(hoje.day)}{str(total).zfill(7)}'
#     return codigo

#otimizada
def gerar_referencia():
    hoje = datetime.date.today()

    # Obter o último ID ou atribuir o valor padrão caso não haja registros
    ultimo_id = db(db.registro_atividade.id>0).select(db.registro_atividade.id.max()).first()[db.registro_atividade.id.max()] or 0

    # Calcular o total somando o último ID com o valor fixo
    total = ultimo_id + 1000000

    # Concatenar os elementos da referência
    codigo = f'{hoje.year}{hoje.month:02d}{hoje.day:02d}{str(total).zfill(7)}'
    return codigo



def atualiza_nomes_usuarios(id_empresa):
    rows = db(db.usuario_empresa.empresa==id_empresa).select()
    for row in rows:
        usuario = db.auth_user(row.usuario)
        row.nome=f'{usuario.first_name.upper()} {usuario.last_name.upper()}'
        row.update_record()
    rows = db(db.usuario_empresa.nome==None).select()
    for row in rows:
        usuario = db.auth_user(row.usuario)
        row.nome=f'{usuario.first_name.upper()} {usuario.last_name.upper()}'
        row.update_record()
    return True


def verifica_possibilidade_validacao(id_sistema):
    sistema = db.sistema(id_sistema)
    if ("S" in sistema.controle_acesso) and ("S" in sistema.trilha_auditoria):
        sistema.possibilidade_validacao="VALIDAVEL"
    else:
        sistema.possibilidade_validacao="NECESSITA DE UPGRADE"
    sistema.update_record()
    return True

def calcula_classe_risco_prioridade(id_gestao_risco):
    gestao_de_risco = db.gestao_de_risco(id_gestao_risco)
    severidade = int(gestao_de_risco.severidade[0:1])
    probabilidade = int(gestao_de_risco.probabilidade[0:1])
    resultado = severidade*probabilidade
    if resultado<=2:
        classe_risco= 'B - Baixa'
        resultado=1
    elif resultado<=4:
        classe_risco= 'M - Média'
        resultado=2
    else:
        classe_risco= 'A - Alta'
        resultado=3
    gestao_de_risco.classe_risco=classe_risco
    detectibilidade = int(gestao_de_risco.detectibilidade[0:1])
    resultado = detectibilidade*resultado
    if resultado<=2:
        prioridade= 'B - Baixa'
    elif resultado<=4:
        prioridade= 'M - Média'
    else:
        prioridade= 'A - Alta'
    gestao_de_risco.prioridade=prioridade
    gestao_de_risco.update_record()
    return True


def calcula_revisao(id_sistema):
    sistema = db.sistema(id_sistema)
    dias_para_revisar = 0 
    if sistema.quantidade_usuarios<6:
        dias_para_revisar = 3*365
    elif sistema.quantidade_usuarios<36:
        dias_para_revisar = 2*365
    else:
        dias_para_revisar = 365
#     data_criacao= str(sistema.created_on)
#     data_prox_revisao = date.fromordinal(data_criacao.toordinal()+dias_para_revisar)

    return (dias_para_revisar)



def gerar_revisao_periodica(id_sistema):
    try:
        total = db((db.registro_atividade.sistema==id_sistema)&(db.registro_atividade.tipo.contains("1008"))).count()
        if total==0:
            sistema = db.sistema(id_sistema)
            from datetime import date
            proxima_data = date.fromordinal(sistema.data_prox_revisao.toordinal()+calcula_revisao(id_sistema))
            
            registro = db.registro_atividade.insert(empresa=sistema.empresa,sistema=sistema.id,tipo=lista_registro_atividade[7], referencia=gerar_referencia(), data_inicial = sistema.data_prox_revisao,data_final=proxima_data)
    except:
        return False
    return True

#antes da otimização
# def total_atividade(id_empresa, tipo):
#     rows = db(db.gestao_de_risco.empresa==None).select()
#     for row in rows:
#         registro_atividade = db.registro_atividade(row.registro_atividade)
#         row.empresa=registro_atividade.empresa
#         row.update_record()
#     if 'total' in tipo:
#         total = db((db.registro_atividade.empresa==id_empresa)&(db.registro_atividade.excluido==False)).count()
#     elif 'concluido' in tipo:
#         total = db((db.registro_atividade.empresa==id_empresa)&(db.registro_atividade.finalizado==True)&(db.registro_atividade.excluido==False)).count()
#     elif 'pendente' in tipo:
#         total = db((db.registro_atividade.empresa==id_empresa)&(db.registro_atividade.finalizado==False)&(db.registro_atividade.excluido==False)).count()
#     elif 'gr' in tipo:
#         total = db((db.gestao_de_risco.empresa==id_empresa)&(db.gestao_de_risco.excluido==False)).count()
#     return total

#otimizado
def total_atividade(id_empresa, tipo):
    if 'total' in tipo:
        total = db((db.registro_atividade.empresa == id_empresa) & (db.registro_atividade.excluido == False)).select(db.registro_atividade.id.count()).first()[db.registro_atividade.id.count()]
    elif 'concluido' in tipo:
        total = db((db.registro_atividade.empresa == id_empresa) & (db.registro_atividade.finalizado == True) & (db.registro_atividade.excluido == False)).select(db.registro_atividade.id.count()).first()[db.registro_atividade.id.count()]
    elif 'pendente' in tipo:
        total = db((db.registro_atividade.empresa == id_empresa) & (db.registro_atividade.finalizado == False) & (db.registro_atividade.excluido == False)).select(db.registro_atividade.id.count()).first()[db.registro_atividade.id.count()]
    elif 'gr' in tipo:
        total = db((db.gestao_de_risco.empresa == id_empresa) & (db.gestao_de_risco.excluido == False)).select(db.gestao_de_risco.id.count()).first()[db.gestao_de_risco.id.count()]
    else:
        total = 0

    return total
