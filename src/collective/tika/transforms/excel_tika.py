from tika import document

class documentExcel(document):
    file_ext = '.xls'

def register():
    return documentExcel()
