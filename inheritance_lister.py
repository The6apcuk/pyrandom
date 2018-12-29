class _Node:
    def __init__(self, cur):
        self.cur = cur
        self.children = []

    def add_child(self, child):
        self.children.append(child)


def _create_tree(obj):
    node = _Node(str(obj))

    try:
        supers = getattr(obj,'__bases__')
    except:
        supers = obj.__class__.__bases__

    for super_ in supers:
        node.add_child(_create_tree(super_))

    return node


def _draw_tree(root_node, indent=0):
    pointer = ''
    if root_node.children:
        pointer = '---|'

    line = '| ---> {}{}'.format(str(root_node.cur), pointer)

    cur_len = len(line)-2
    print(' ' * indent + line)

    for child in root_node.children:
        _draw_tree(child, (indent + 1) + cur_len)


def print_tree(obj):
    _draw_tree(_create_tree(obj))


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
        pass

    print_tree(F)
