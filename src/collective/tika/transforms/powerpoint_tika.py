from tika import document

class documentPowerpoint(document):
    file_ext = '.ppt'

def register():
    return documentPowerpoint()
