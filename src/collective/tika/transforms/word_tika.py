from tika import document

class documentWord(document):
    file_ext = '.doc'

def register():
    return documentWord()
