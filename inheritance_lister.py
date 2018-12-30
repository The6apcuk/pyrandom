colors_dict = {"yellow": '\033[94m',
               "green": '\033[0;32m',
               "red": "\033[31m",
               "blue": "\033[34m",
               "regular": '\033[0m'}


class _Node:
    def __init__(self, cur):
        self.cur = cur
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def _create_tree(obj):
    node = _Node(obj)

    import sys
    if sys.version_info[:2] > (2,7):
        class_types = (type,)
    else:
        import types
        class_types = (types.TypeType, types.ClassType)

    if isinstance(obj, class_types):
        supers = obj.__bases__
    else:
        supers = (obj.__class__,)

    for super_ in supers:
        node.add_child(_create_tree(super_))

    return node


def _draw_tree(root_node, indent=0, attr_list=False):
    pointer = ''
    if root_node.children:
        pointer = '---|'

    if attr_list:
        attrs = root_node.cur.__dict__.items()
        for name, value in attrs:
            print("{}|{} = {}".format(' ' * indent, name, value))


    line = '| ---> {}{}'.format(str(root_node.cur), pointer)

    cur_len = len(line)-2
    print(' ' * indent + colors_dict['blue'] + line + colors_dict['regular'])


    for child in root_node.children:
        _draw_tree(child, (indent + 1) + cur_len, attr_list=attr_list)


def print_tree(obj, attr_list=False):
    _draw_tree(_create_tree(obj), attr_list=attr_list)


if __name__ == '__main__':
    class A():
        pass
    class B(A):
        pass
    class C(A):
        pass
    class D(B):
        pass
    class E(C):
        pass
    class F(D,E):
        'aaa'
        a=1
        pass

    f=F()
    f.b=1
    print_tree(f, True)
