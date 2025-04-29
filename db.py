import pymysql
import config

def salvar_evento(texto_reconhecido, interprete, tipo_visitante='desconhecido', acao_tomada=None):
    connection = pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        port=config.DB_PORT
    )

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO eventos_voz (texto_reconhecido, interprete, tipo_visitante, acao_tomada) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (texto_reconhecido, interprete, tipo_visitante, acao_tomada))
        connection.commit()
    finally:
        connection.close()

def salvar_audio_no_banco(nome_arquivo):
    connection = pymysql.connect(
        host=config.DB_HOST,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
        port=config.DB_PORT
    )

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO audios (nome_arquivo, data_hora) VALUES (%s, NOW())"
            cursor.execute(sql, (nome_arquivo,))
        connection.commit()
    finally:
        connection.close()
