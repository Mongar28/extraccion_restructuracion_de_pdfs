import os
import pandas as pd
from io import StringIO
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from unidecode import unidecode
import re


def PDF_parser()->list:
    # Path of the folder containing the pdfs
    folder_path = "PDF"

    # We create a list empty which will contain the text extracted from the pdfs
    texts_pdf = []

    # We create an empty list which will contain the name of the files.
    nombres_archivos = []

    contador =0

    # We iterate over the pdfs files that are inside the folder.
    for pdf_file in os.listdir(folder_path):
        if pdf_file.endswith('.pdf'):
            try:
                output_string = StringIO()
                with open(os.path.join(folder_path, pdf_file), 'rb') as in_file:
                    parser = PDFParser(in_file)
                    doc = PDFDocument(parser)
                    rsrcmgr = PDFResourceManager()
                    device = TextConverter(rsrcmgr, output_string, laparams=LAParams())
                    interpreter = PDFPageInterpreter(rsrcmgr, device)
                    for page in PDFPage.create_pages(doc):
                        interpreter.process_page(page)
            except:
                print("Error processing file:", pdf_file)

            print("{:<2}---> PDF:{:->64}{:->20}".format(contador, pdf_file,'> processed'))
            texts_pdf.append(unidecode(output_string.getvalue()))
            contador += 1

    print(f"A total of {len(texts_pdf)} were processed")
    
    return texts_pdf

def txt_list():
    nombre_archivo = "motor_de_busqueda/extractor_pdf/actas_concejo.txt"
    mi_lista: list = []
    # Abre el archivo en modo lectura
    with open(nombre_archivo, 'r') as archivo:
        # Lee cada línea del archivo y agrega el elemento a la lista
        for linea in archivo:
            mi_lista.append(linea.strip())
    return mi_lista


def liss_txt(lista_actas):
    # Nombre del archivo
    nombre_archivo = "actas_concejo.txt"

    # Abre el archivo en modo escritura
    with open(nombre_archivo, 'w') as archivo:
        # Escribe cada elemento de la lista en una línea separada
        for elemento in lista_actas:
            archivo.write(elemento + "\n")

    print(f"Se ha creado el archivo '{nombre_archivo}' con éxito.")


def limpiador1(texto:str)-> str:
    texto = re.sub(r'\n\d{1,3}', '', texto)
    texto = re.sub(r'\.\s\n\n', '. @@@ ', texto)
    texto = re.sub(r'\n\.', '', texto)
    texto = re.sub(r'\s\n\s', ' ', texto)
    texto = re.sub(r'\n{1,100}', ' ', texto)
    #SESION PLENARIA ORDINARIA 4
    texto = re.sub(r'SESION PLENARIA ORDINARIA [0-9]{1,3}', '  ', texto)
    texto = re.sub(r'\d{1,3} SESION PLENARIA ORDINARIA', '  ', texto)
    texto = re.sub(r'\s{2,100}', ' ', texto)

    texto = re.sub(r'Intervino', '___Intervino', texto)
    return texto
