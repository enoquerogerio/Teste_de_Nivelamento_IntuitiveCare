import csv
import json
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


lista_operadoras = []
# Definição do caminho do arquivo CSV
arquivo_csv = Path("operadoras_ativas.csv")


# Função para carregar dados do arquivo CSV
def carregar_dados(arquivo_csv):
    try:
        with open(arquivo_csv, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            return list(reader)
    except Exception as e:
        print(f"Erro ao carregar o arquivo CSV: {e}")
        return []


lista_operadoras = carregar_dados(arquivo_csv)


@app.route("/api/operadoras/<cnpj>", methods=["GET"])
def get_operadora(cnpj):
    try:
        for operadora in lista_operadoras:
            if operadora["CNPJ"] == cnpj:
                return (
                    jsonify(
                        {
                            "Registro_ANS": operadora["Registro_ANS"],
                            "CNPJ": operadora["CNPJ"],
                            "Razao_Social": operadora["Razao_Social"],
                            "Modalidade": operadora["Modalidade"],
                            "Telefone": operadora["Telefone"],
                            "Logradouro": operadora["Logradouro"],
                            "Numero": operadora["Numero"],
                            "Bairro": operadora["Bairro"],
                            "Cidade": operadora["Cidade"],
                            "UF": operadora["UF"],
                            "CEP": operadora["CEP"],
                        }
                    ),
                    200,
                )

        return jsonify({"error": "Operadora not found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
