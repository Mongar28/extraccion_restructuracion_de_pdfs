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

lista_actas: list = PDF_parser()

df  = pd.DataFrame()
df['texto'] = lista_actas

df.to_csv('actas_concejo.csv')
print(f'La longitud del df es de: {len(df)}')