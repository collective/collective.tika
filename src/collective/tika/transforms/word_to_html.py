from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implements

EXTRACT_BODY  = 1
EXTRACT_STYLE = 0

FIX_IMAGES    = 1
IMAGE_PREFIX  = "img_"

import os
from tika import tika_transform
from word_tika import documentWord

import os.path

class word_to_html(tika_transform):
    implements(ITransform)

    __name__ = "word_to_html"
    inputs   = ('application/msword', 
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document', )
    output  = 'text/html'
    output_encoding = 'utf-8'

    tranform_engine = documentWord.__module__

    def convert(self, data, cache, **kwargs):
        orig_file = 'unknown.doc'
        doc = None
        try:
            doc = documentWord(orig_file, data, exec_prefix=self.config['exec_prefix'])
            doc.convert()
            html = doc.html()

            path, images = doc.subObjects(doc.tmpdir)
            objects = {}
            if images:
                doc.fixImages(path, images, objects)

            cache.setData(html)
            cache.setSubObjects(objects)
            return cache
        finally:
            if doc is not None:
                doc.cleanDir(doc.tmpdir)

def register():
    return word_to_html()
