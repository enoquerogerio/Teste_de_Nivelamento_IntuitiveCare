import tabula
import pandas as pd
import os
from pathlib import Path
from zipfile import ZipFile


def compactar_ficheiros_para_zip(zip_filename, file_path):
    with ZipFile(zip_filename, "w") as zip:
        zip.write(file_path, os.path.basename(file_path))

    print(f"Arquivos comprimidos em {zip_filename}")


def extrair_tabelas_pdf(path_pdf, start_page, end_page, output_file):
    try:
        range_page = f"{start_page}-{end_page}"
        print(
            f"Iniciando a extração das tabelas da página {start_page} até {end_page}..."
        )
        tables = tabula.read_pdf(
            path_pdf, pages=range_page, multiple_tables=True, encoding="utf-8"
        )

        for table in tables:
            if "OD" in table.columns:
                table.rename(columns={"OD": "Ortopedia"}, inplace=True)
            if "AMB" in table.columns:
                table.rename(columns={"AMB": "Ambulatório"}, inplace=True)

        if tables:

            combined_df = pd.concat(tables, ignore_index=True)

            combined_df.to_csv(output_file, index=False, encoding="utf-8-sig")

            print(f"Tabelas extraídas com sucesso! Arquivo salvo em: {output_file}")
            zip_filename = "Teste_EnoqueRogerio.zip"
            compactar_ficheiros_para_zip(zip_filename, Path(output_file))
        else:
            print(f"Nenhuma tabela encontrada nas páginas {start_page} até {end_page}.")
    except Exception as e:
        print(f"Erro ao extrair tabelas do PDF: {e}")


# Caminho do arquivo pdf
path_pdf = Path("AnexoI.pdf")

# Intervalo de páginas para extração de tabelas
start_page = 3
end_page = 181

output_file = "Anexo_I.csv"

extrair_tabelas_pdf(path_pdf, start_page, end_page, output_file)
