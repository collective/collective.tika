from tika import document

class documentPDF(document):
    file_ext = '.pdf'

def register():
    return documentPDF()
