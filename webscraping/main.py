import requests
import os
from bs4 import BeautifulSoup
from zipfile import ZipFile
import shutil


def download_pdf(pdf_url, nome_arquivo, folder_name):
    response = requests.get(pdf_url)

    if response.status_code == 200:
        print("Baixando...")

        # Salvar o caminho do arquivo PDF
        file_path = os.path.join(folder_name, nome_arquivo)
        with open(file_path, "wb") as f:
            f.write(response.content)
        print(f"Arquivo {nome_arquivo} baixado com sucesso!")
        return file_path
    else:
        print(f"Erro ao baixar {nome_arquivo}")
        return None


def filtrar_e_baixar_pdfs_anexos(pdf_links, folder_name):
    downloaded_files = []  # Lista para armazenar os arquivos baixados
    for link in pdf_links:
        href = link.get("href")
        texto_link = link.get_text()

        # Verificar se o link contém o texto Anexo I ou II e se é um PDF
        if ("Anexo I" in texto_link and ".pdf" in href) or (
            "Anexo II" in texto_link and ".pdf" in href
        ):

            # Extrair o nome do arquivo do URL
            nome_arquivo = href.split("/")[-1]

            # Baixar o PDF
            file_path = download_pdf(href, nome_arquivo, folder_name)
            if file_path:
                downloaded_files.append(file_path)

    return downloaded_files


def compactar_ficheiros_para_zip(zip_filename, downloaded_files):
    with ZipFile(zip_filename, "w") as zip:
        for file_path in downloaded_files:
            zip.write(file_path, os.path.basename(file_path))

    print(f"Arquivos comprimidos em {zip_filename}")


def apagar_pasta_temporaria(folder_name):
    if os.path.exists(folder_name):
        shutil.rmtree(folder_name)


def main():
    # URL do site que contém os PDFs
    link = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"
    response = requests.get(link)
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = soup.find_all("a", href=True)
    zip_filename = "anexos_comprimidos.zip"

    # Pasta para salvar os arquivos temporariamente
    folder_name = "anexos"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    downloaded_files = filtrar_e_baixar_pdfs_anexos(pdf_links, folder_name)
    compactar_ficheiros_para_zip(zip_filename, downloaded_files)
    apagar_pasta_temporaria(folder_name)


if __name__ == "__main__":
    main()
