# Copyright 2010, Kovid Goyal <kovid at kovidgoyal.net>
# Copyright 2011 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "GPL v3" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/gplv3_license

class TOC(list):

    def __init__(self, href=None, fragment=None, text=None, parent=None, play_order=0,
                 type='unknown', author=None, description=None):
        self.href = href
        self.fragment = fragment
        if not self.fragment:
            self.fragment = None
        self.text = text
        self.parent = parent
        self.play_order = play_order
        self.type = type
        self.author = author
        self.description = description

    def __str__(self):
        lines = ['TOC: %s#%s'%(self.href, self.fragment)]
        for child in self:
            c = str(child).splitlines()
            for l in c:
                lines.append('\t'+l)
        return '\n'.join(lines)

    def count(self, type):
        return len([i for i in self.flat() if i.type == type])

    def purge(self, types, max=0):
        remove = []
        for entry in self.flat():
            if entry.type in types:
                remove.append(entry)
        remove = remove[max:]
        for entry in remove:
            if entry.parent is None:
                continue
            entry.parent.remove(entry)
        return remove

    def remove(self, entry):
        list.remove(self, entry)
        entry.parent = None

    def add_item(self, href, fragment, text, play_order=None, type='unknown',
            author=None, description=None):
        if play_order is None:
            play_order = (self[-1].play_order if len(self) else self.play_order) + 1
        self.append(TOC(href=href, fragment=fragment, text=text, parent=self,
                        play_order=play_order, type=type, author=author, description=description))
        return self[-1]

    def top_level_items(self):
        for item in self:
            if item.text is not None:
                yield item

    def depth(self):
        depth = 1
        for obj in self:
            c = obj.depth()
            if c > depth - 1:
                depth = c + 1
        return depth

    def flat(self):
        'Depth first iteration over the tree rooted at self'
        yield self
        for obj in self:
            for i in obj.flat():
                yield i
