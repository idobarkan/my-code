import xml.dom.minidom as dom
from util import DTO

class Dumper(object):
    def __init__(self):
        self.dct_dumpers = {
            dict : self._dump_mapping,
            list : self._dump_sequence,
            tuple : self._dump_sequence,
            set : self._dump_set,
            DTO : self._dump_DTO,
        }

    def _dump_simple(self,obj,node,name,fabric): #@UnusedVariable
        node.attributes["text"] = str(obj)

    def _dump_mapping(self, dct, node, name, fabric):
        if not dct:
            self._dump_simple(dct,node,name,fabric)
            return

        node.attributes["length"] = str(len(dct))

        for key, value in dct.iteritems():
            child = self.dump(value,"item",fabric)
            child.attributes["index"] = str(key)
            child.attributes["type"] = 'key=%s, value=%s' % (type(key).__name__,type(value).__name__)
            node.appendChild(child)

    def _dump_sequence(self, seq, node, name, fabric):
        if not seq:
            self._dump_simple(seq,node,name,fabric)
            return

        node.attributes["length"] = str(len(seq))

        for index,item in enumerate(seq):
            child = self.dump(item, "item", fabric)
            child.attributes["index"] = str(index)
            node.appendChild(child)

    def _dump_set(self, st, node, name, fabric):
        if not st:
            self._dump_simple(st,node,name,fabric)
            return

        node.attributes["length"] = str(len(st))

        for item in st:
            child = self.dump(item, "item", fabric)
            child.attributes["index"] = "item"
            node.appendChild(child)

    def _dump_DTO(self, obj, node, name, fabric):
        for name in obj._DTO_members:
            val = getattr(obj, name)
            node.appendChild(self.dump(val, name, fabric))

    def _dump_generic(self,obj,node,name,fabric):
        try:
            d = obj.__dict__
        except:
            d = None

        if d is not None:
            for name,val in d.iteritems():
                if name.startswith('_'):
                    continue # don't show private members
                node.appendChild(self.dump(val, name, fabric))
        else:
            self._dump_simple(obj,node,name,fabric)

    def dump(self, obj, name="root", fabric=None):
        if fabric is None:
            fabric = dom.Document()

        node = fabric.createElement(name)
        node.attributes["type"] = type(obj).__name__

        if hasattr(obj,'_dump_one_line'):
            self._dump_simple(obj,node,name,fabric)
            return node

        for tp,dumper in self.dct_dumpers.iteritems():
            if isinstance(obj,tp):
                dumper(obj,node,name,fabric)
                return node

        self._dump_generic(obj,node,name,fabric)
        return node

Dumper = Dumper()        

#########################################
class A(DTO):
    def __init__(self,x,y):
        super(A,self).__init__(locals())

def main():
    obj = ['my string',{1:True},A(11,A('a','b')),666]
    node = Dumper.dump(obj)
    print node.toprettyxml()        
if __name__ == '__main__': main()