import psycopg2
from psycopg2 import sql
import mysql.connector
from pathlib import Path
import csv


def conectar_mysql():
    connection = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="root",
        database="db_operadora",
    )

    if connection.is_connected():
        print("Conexão ao MySQL estabelecida com sucesso!")
        return connection


def conectar_postgres():
    connection = psycopg2.connect(
        host="localhost",
        port="5432",
        user="root",
        password="root",
        dbname="db_operadora",
    )

    print("Conexão ao PostgreSQL estabelecida com sucesso!")
    return connection


def criar_tabela_operadoras(conn):
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS operadoras (
        registro_ans VARCHAR(100) PRIMARY KEY,
        cnpj VARCHAR(100) NOT NULL,
        razao_social VARCHAR(255) NOT NULL,
        nome_fantasia VARCHAR(255),
        modalidade VARCHAR(255),
        logradouro VARCHAR(255),
        numero VARCHAR(50),
        complemento VARCHAR(255),
        bairro VARCHAR(255),
        cidade VARCHAR(255),
        uf CHAR(2),
        cep VARCHAR(50),
        ddd CHAR(2),
        telefone VARCHAR(50),
        fax VARCHAR(50),
        endereco_eletronico VARCHAR(255),
        representante VARCHAR(255),
        cargo_representante VARCHAR(255),
        regiao_de_comercializacao INT,
        data_registro_ans DATE
    );
    """

    cursor.execute(query)
    conn.commit()
    print("Tabela 'operadoras' criada com sucesso.")


def criar_tabela_demonstracoe(conn):
    cursor = conn.cursor()

    query = """
    CREATE TABLE IF NOT EXISTS demonstracoes (
        id SERIAL PRIMARY KEY,
        data DATE,
        reg_ans VARCHAR(15),
        cd_conta_contabil VARCHAR(15),
        descricao VARCHAR(255),
        vl_saldo_inicial DECIMAL(15, 2),
        vl_saldo_final DECIMAL(15, 2)
    );
    """

    cursor.execute(query)
    conn.commit()
    print("Tabela 'demonstracoe' criada com sucesso!")


def validar_tipo(valor, tipo):
    if tipo == "int":
        try:
            return int(valor) if valor != "" else None
        except ValueError:
            return None
    else:
        return valor


def importar_csv_operadoras_para_bd(conn, arquivo_csv):
    cursor = conn.cursor()

    with open(arquivo_csv, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)

        for row in reader:

            # Tratar os valores vazios em campos numéricos e converter para numerico
            row[18] = validar_tipo(row[18], "int")
            cursor.execute(
                """
            INSERT INTO operadoras (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, 
                                    complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, 
                                    representante, cargo_representante, regiao_de_comercializacao, data_registro_ans)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """,
                row,
            )

    conn.commit()
    print("Dados importados com sucesso para a tabela operadoras!")


def importar_csv_demonstracoes_para_bd(conn, arquivo_csv):
    cursor = conn.cursor()

    with open(arquivo_csv, "r", encoding="utf-8") as file:
        reader = csv.reader(file, delimiter=";")
        next(reader)  # Pular o cabeçalho

        for row in reader:

            # Remover espaços em branco nos campos
            data = row[0].strip()
            reg_ans = row[1].strip()
            cd_conta_contabil = row[2].strip()
            descricao = row[3].strip()

            # Ajuste para valor numérico
            vl_saldo_inicial = row[4].strip().replace(",", ".")
            vl_saldo_final = row[5].strip().replace(",", ".")

            # Garantir que os valores numéricos sejam do tipo FLOAT
            vl_saldo_inicial = float(vl_saldo_inicial) if vl_saldo_inicial else None
            vl_saldo_final = float(vl_saldo_inicial) if vl_saldo_inicial else None

            cursor.execute(
                """
            INSERT INTO demonstracoes (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final)
            VALUES (%s, %s, %s, %s, %s, %s);
            """,
                (
                    data,
                    reg_ans,
                    cd_conta_contabil,
                    descricao,
                    vl_saldo_inicial,
                    vl_saldo_final,
                ),
            )

        conn.commit()
        print("Dados importados com sucesso para a tabela 'demostracoe'!")


def get_top_10_operadoras_trimestre(conn):
    cursor = conn.cursor()

    query = """
    SELECT 
        o.razao_social,
        SUM(d.VL_SALDO_FINAL - d.VL_SALDO_INICIAL) AS total_despesas
    FROM 
        demonstracoes d
    JOIN 
        operadoras o ON d.REG_ANS = o.registro_ans
    WHERE 
        d.DESCRICAO LIKE '%EVENTOS%'
        AND d.DATA >= CURRENT_DATE - INTERVAL '3 months'
    GROUP BY 
        o.razao_social
    ORDER BY 
        total_despesas DESC
    LIMIT 10;
    """

    cursor.execute(query)
    top_10_operadoras = cursor.fetchall()

    # Fechar a conexão
    cursor.close()
    conn.close()

    for operadora in top_10_operadoras:
        print(operadora)


def get_top_10_operadoras_ano(conn):
    cursor = conn.cursor()

    query = """
    SELECT 
        o.razao_social,
        SUM(d.VL_SALDO_FINAL - d.VL_SALDO_INICIAL) AS total_despesas
    FROM 
        demonstracoes d
    JOIN 
        operadoras o ON d.REG_ANS = o.registro_ans
    WHERE 
        d.DESCRICAO LIKE '%EVENTOS%'
        AND d.DATA >= CURRENT_DATE - INTERVAL '1 year'
    GROUP BY 
        o.razao_social
    ORDER BY 
        total_despesas DESC
    LIMIT 10;
    """

    cursor.execute(query)
    top_10_operadoras = cursor.fetchall()

    # Fechar a conexão
    cursor.close()
    conn.close()

    for operadora in top_10_operadoras:
        print(operadora)


def main():
    operadoras_ativas_csv = Path("operadoras_ativas.csv")

    # Conectar ao MySQL
    # mysql_connection = conectar_mysql()

    # Conectar ao PostgreSQL
    postgres_connection = conectar_postgres()

    # Criar a tabela operadora
    criar_tabela_operadoras(postgres_connection)

    # Criar a tabela demonstações
    criar_tabela_demonstracoe(postgres_connection)

    # Importar os dados do csv para PostgreSQL
    importar_csv_operadoras_para_bd(postgres_connection, operadoras_ativas_csv)

    for i in range(1, 5):
        demonstracoe_csv = Path(f"demonstracoes_2023/{i}T2023.csv")
        importar_csv_demonstracoes_para_bd(postgres_connection, demonstracoe_csv)

    for i in range(1, 5):
        demonstracoe_csv = Path(f"demonstracoes_2024/{i}T2024.csv")
        importar_csv_demonstracoes_para_bd(postgres_connection, demonstracoe_csv)

    get_top_10_operadoras_trimestre(postgres_connection)
    get_top_10_operadoras_ano(postgres_connection)


if __name__ == "__main__":
    main()
