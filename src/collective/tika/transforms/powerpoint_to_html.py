from Products.PortalTransforms.interfaces import ITransform
from zope.interface import implements

EXTRACT_BODY  = 1
EXTRACT_STYLE = 0

FIX_IMAGES    = 1
IMAGE_PREFIX  = "img_"

import os
from tika import tika_transform
from powerpoint_tika import documentPowerpoint

import os.path

class powerpoint_to_html(tika_transform):
    implements(ITransform)

    __name__ = "powerpoint_to_html"
    inputs   = ('application/vnd.ms-powerpoint',
                'application/vnd.openxmlformats-officedocument.presentationml.presentation', )
    output  = 'text/html'
    output_encoding = 'utf-8'

    tranform_engine = documentPowerpoint.__module__

    def convert(self, data, cache, **kwargs):
        orig_file = 'unknown.ppt'
        doc = None
        try:
            doc = documentPowerpoint(orig_file, data, exec_prefix=self.config['exec_prefix'])
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
    return powerpoint_to_html()
