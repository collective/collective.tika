from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implements

EXTRACT_BODY  = 1
EXTRACT_STYLE = 0

FIX_IMAGES    = 1
IMAGE_PREFIX  = "img_"

import os
from tika import tika_transform
from pdf_tika import documentPDF

import os.path

class pdf_to_html(tika_transform):
    implements(ITransform)

    __name__ = "pdf_to_html"
    inputs   = ('application/pdf',)
    output  = 'text/html'
    output_encoding = 'utf-8'

    tranform_engine = documentPDF.__module__

    def name(self):
        return self.__name__

    def convert(self, data, cache, **kwargs):
        orig_file = 'unknown.pdf'
        pdf = None
        try:
            pdf = documentPDF(orig_file, data, exec_prefix=self.config['exec_prefix'])
            pdf.convert()
            html = pdf.html()

            path, images = pdf.subObjects(pdf.tmpdir)
            objects = {}
            if images:
                pdf.fixImages(path, images, objects)

            cache.setData(html)
            cache.setSubObjects(objects)
            return cache
        finally:
            if pdf is not None:
                pdf.cleanDir(pdf.tmpdir)

def register():
    return pdf_to_html()
