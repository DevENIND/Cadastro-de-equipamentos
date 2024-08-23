import mysql.connector

def mysql_connection(host, user, passwd, database=None):
    connection = mysql.connector.connect(
        host = host,
        user = user,
        passwd = passwd,
        database = database
    )
    return connection

def inserir_banco(Tabela, Dados, banco_de_dados):
    query = f'INSERT INTO {Tabela} VALUES {Dados}'
    cursor = banco_de_dados
    cursor.execute(query)
    banco_de_dados.commit()
    
def delete_banco(Tabela, Condicao, banco_de_dados):
    query = f'DELETE FROM {Tabela} WHERE {Condicao}'
    cursor = banco_de_dados.cursor()
    cursor.execute(query)
    banco_de_dados.commit()