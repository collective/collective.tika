from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implements

EXTRACT_BODY  = 1
EXTRACT_STYLE = 0

FIX_IMAGES    = 1
IMAGE_PREFIX  = "img_"

import os
from tika import tika_transform
from excel_tika import documentExcel

import os.path

class excel_to_html(tika_transform):
    implements(ITransform)

    __name__ = "excel_to_html"
    inputs   = ('application/vnd.ms-excel',
                'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', )
    output  = 'text/html'
    output_encoding = 'utf-8'

    tranform_engine = documentExcel.__module__

    def convert(self, data, cache, **kwargs):
        orig_file = 'unknown.xls'
        pdf = None
        try:
            pdf = documentExcel(orig_file, data, exec_prefix=self.config['exec_prefix'])
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
    return excel_to_html()
