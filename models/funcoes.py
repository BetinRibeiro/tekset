# -*- coding: utf-8 -*-
import datetime

def form_num(number):
    return "{:02d}".format(number)

def gerar_referencia():
    hoje = datetime.date.today()
    total = db(db.registro_atividade.id>0).count()
    if total==0:
        total=1000000
    else:
        ultimo = db(db.registro_atividade.id>0).select().last()
        total = ultimo.id+1000000
    
    codigo = f'{hoje.year}{form_num(hoje.month)}{form_num(hoje.day)}{str(total).zfill(7)}'
    return codigo


def atualiza_nomes_usuarios(id_empresa):
    rows = db(db.usuario_empresa.empresa==id_empresa).select()
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