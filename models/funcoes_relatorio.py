# -*- coding: utf-8 -*-


def retorno_registro(id_sistema, tipo):
    
    return db((db.registro_atividade.sistema==id_sistema)&(db.registro_atividade.tipo.contains(tipo))).select()


def grs(id_registro):
    return db(db.gestao_de_risco.registro_atividade==id_registro).select()
