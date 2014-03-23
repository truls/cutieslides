
import os
from PIL import Image
import mimetypes

from PyQt4.QtCore import QObject, pyqtSignal

class NotReadyException(Exception):
    pass

class RecursionDepthReached(Exception):
    pass

# Types
class types:
    class Video:
        pass
    class Image:
        pass
    class Anim:
        pass
    video = Video()
    image = Image()
    anim = Anim()
    

class CommonResource(object):

    def __init__(self, r, properties, parent):
        self.properties = properties
        self.parent = parent

        # Make sure we haven't cought ourselves in an infinite loop
        self._check_depth()

        self.descendants = []
        self.resource = r
        self.file = ''
    
    def _find_type(self, path):
        ext = os.path.splitext(path)[1]
        try:
            mimetype = mimetypes.types_map[ext]
        except KeyError:
            print("Could not find mimetype for extension")
            return -1
            
        print("Found mimetype: ", mimetype)

        if "image/" in mimetype:
            # Special-case for animated gifs
            if ext == "gif":
                gif = Image.open(path)
                try:
                    gif.seek(1)
                    return types.anim
                except EOFError:
                    pass
                finally:
                    gif.close()
                
            return types.image
        elif "video/" in mimetype:
            return types.video
        else:
            print("Unknown mimetype")

    def _check_depth(self):
        # Prevent infinite recursions
        if self.parent:
            if self.parent.depth > 9:
                raise RecursionDepthReached
            self.depth = self.parent.depth + 1

    def get_children(self):
        clist = []
        if len(self.descendants) > 0:
            for c in self.descendants:
                clist.append(c.get_children())
        else:
            return self
        return clist

class FilesystemResource(QObject, CommonResource):
    """
    Resource handler for local files and folders
    """
    
    def __init__(self, f, properties, parent):
        super(CommonResource, self).__init__(f, properties, parent)

    def _expand_directory(self, el):
        if not "directory" in el:
            return [el]
        l = []
        d = el['directory']
        d_tmp = os.path.join(self.config['basepath'], d)
        try:
            dirlist = os.listdir(d_tmp)
            #print(d_tmp, dirlist)
        except OSError:
            # FIXME: Print contents of OSError exception
            print("Directory", d_tmp, "not found")
            return []
        for f in dirlist:
            nl = {'file': os.path.join(d, f),
                  'caption': el['caption'],
                  'delay': el['delay'],
                  'frequency': el['frequency']}
            l.append(nl)
        #print(l)
        return l

class UrlResource(QObject, CommonResource):
    """
    Class for holding a content object. This class holds parameters of the content objects
    and figures out how to aquire the content. This class is responsible for figuring out the type
    of content (image, video, etc...) and matching the content URL against handlers
    """
    download_complete = pyqtSignal()
    
    def __init__(self, url, handlers, properties = None, parent = None):
        super(UrlResource, self).__init__()
        CommonResource.__init__(self, url, properties, parent = parent)

        self.download_complete.connect(self._set_ready)
        
        self.depth = 0
        
        self.done = False
        
        self.handlers = handlers
        self.url = url
        self._caption = "Caption"
        self.descendants = []

        self._file = "foo"

        self._add_resource()

    def _add_resource(self):
        handler = self.handlers.get(self.resource)
        #FIXME: Handle handler not found
        h = handler()
        print("Got handler", h)
        rs = h.get(self.url)

        if isinstance(rs, list) and len(rs) > 1:
            for r in rs:
                print("Adding child", r)
                # TODO: Handle max recursion depth
                self.descendants.append(
                    UrlResource(r[0], self.handlers,
                                properties = self.properties.clone(caption=r[1])))
        else:
            # FIXME: This shouldn't fail if somebody mixes up and
            # returns a single element in a list instead of a tuple
            if isinstance(rs, list) and len(rs) == 1:
                rs = rs[0]
            self.url = rs[0]
            if rs[1]:
                self.caption = rs[1]

            print("set final", rs)

    def cache(self):
        pass


    @property
    def file(self):
        #if not self.done:
        #    raise NotReadyException
        return self._file
    @file.setter
    def file(self, v):
        self._file = v

    @property
    def caption(self):
        #if not self.done:
        #    raise NotReadyException
        return self.properties.caption
    @caption.setter
    def caption(self, v):
        self.properties.caption = v
            
    def __repr__(self):
        return "(%s, %s)" % (self.url, self.caption)
        
    @property
    def ready(self):
        return self.done

    def _set_ready(self):
        self.done = True

    

