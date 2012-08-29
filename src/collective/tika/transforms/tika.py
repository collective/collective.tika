import os, subprocess
from logging import getLogger
from Products.PortalTransforms.libtransforms.utils import bodyfinder, scrubHTML
from Products.PortalTransforms.libtransforms.commandtransform import commandtransform
from Products.CMFPlone.utils import safe_unicode
from htmllaundry import utils as laundryutils
from htmllaundry import cleaners

log = getLogger('collective.tika.transforms')


allow_tags = ['pre', 'code', 'h2', 'h3', 'h1', 'h6', 'h4', 'h5', 'header', 'table', 'li',
    'span', 'img', 'title', 'tt', 'tr', 'mark', 'source', 'th', 'strike',
    'td', 'cite', 'thead', 'dl', 'blockquote', 'hr', 'dd', 'dt', 'b',
    'summary', 'p', 'div', 'em', 'figure', 'datalist', 'head', 'hgroup',
    'meta', 'video', 'tbody', 'rt', 'canvas', 'rp', 'ul', 'section', 'aside',
    'html', 'details', 'u', 'body', 'figcaption', 'base', 'br', 'article',
    'strong', 'a', 'ol', 'footer', 'i', 'caption', 'command', 'time', 'audio']

HTMLCleaner = cleaners.LaundryCleaner(
            page_structure = False,
            remove_unknown_tags = False,
            allow_tags = allow_tags,
            safe_attrs_only = True,
            add_nofollow = False,
            scripts = False,
            javascript = False,
            comments = False,
            style = False,
            links = False,
            meta = False,
            processing_instructions = False,
            frames = False,
            annoying_tags = False
            )

class document(commandtransform):

    file_ext = ''

    def __init__(self, name, data, exec_prefix=None):
        """ Initialization: create tmp work directory and copy the
        document into a file"""
        tika_path = 'tika'
        if exec_prefix is not None:
            tika_path = os.path.join(exec_prefix, 'tika-bin')
            if not os.path.exists(tika_path):
                tika_path = os.path.join(exec_prefix, 'tika')
                if not os.path.exists(tika_path):
                    log.warn('no tika-bin or tika found in exec-prefix: %s' % tika_path)
                    tika_path = 'tika'

        commandtransform.__init__(self, name, binary=tika_path)
        name = self.name()
        if not name.endswith(self.file_ext):
            name = name + self.file_ext
        self.tmpdir, self.fullname = self.initialize_tmpdir(data, filename=name)

    def convert(self):
        "Convert the document"
        tmpdir = self.tmpdir
        htmlfile = open("%s/%s.html" % (self.tmpdir, self.__name__), 'w')

        # for windows, install wvware from GnuWin32 at C:\Program Files\GnuWin32\bin
        # you can use:
        # wvware.exe -c ..\share\wv\wvHtml.xml --charset=utf-8 -d d:\temp d:\temp\test.doc > test.html

        if os.name == 'posix':
            try:
                subprocess.check_call([self.binary, self.fullname], stdout=htmlfile, cwd=tmpdir)
            except subprocess.CalledProcessError as cpe:
                log.warn('Could not transform %s: %s' % (self.fullname, cpe))
        htmlfile.close()

    def html(self):
        htmlfile = open("%s/%s.html" % (self.tmpdir, self.__name__), 'r')
        html = htmlfile.read()
        htmlfile.close()
        html = safe_unicode(html)
        try:
            html = laundryutils.sanitize(html, HTMLCleaner)
        except Exception, err:
            html = ''
        # scrubHTML is EVIL, takes ages!
        #html = scrubHTML(html)
        body = bodyfinder(html)
        body = body.encode('utf-8')
        return body

class tika_transform:

    output  = 'text/html'
    output_encoding = 'utf-8'

    def __init__(self, name=None, exec_prefix=None):
        self.config = { 'exec_prefix': exec_prefix, }
        self.config_metadata = { 'exec_prefix':
                                    ('string',
                                     'Executable Prefix',
                                     'Directory that holds the tika binary. Leave blank to search system path')
                               }

    def __getattr__(self, attr):
        if attr in self.config:
            return self.config[attr]
        raise AttributeError(attr)

    def name(self):
        return self.__name__

