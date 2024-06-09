from docxtpl import DocxTemplate
from datetime import date

import comtypes.client


def Red_docx(docx_path, dates, gov_marker, name):
    doc = DocxTemplate(docx_path)
    list_date = dates.split(' ')
    context = {
        'dd': list_date[0],
        'mmmm': list_date[1],
        'yyyy': list_date[2],
        'gov_marker': gov_marker,
        'Name': name}

    doc.render(context)
    current_date = date.today()
    title_file = f"{current_date}_Пропуск_Авто_{name}"
    doc.save(f"/data/{title_file}.docx")
    return title_file


def Docx_to_pdf(title_file):
    wdFormatPDF = 17
    in_file = f"/data/{title_file}.docx"
    out_file: str = f"/data/{title_file}.pdf"

    word = comtypes.client.CreateObject('Word.Application')
    doc = word.Documents.Open(in_file)
    doc.SaveAs(out_file, FileFormat=wdFormatPDF)
    doc.Close()
    word.Quit()
    return out_file
