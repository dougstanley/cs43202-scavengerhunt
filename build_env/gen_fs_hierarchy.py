#!/usr/bin/python
import random
import math
import os.path
import sys

MAXDEPTH = 8
MAXOBJ = 20
MAXDIR = 5


def usage():
    print "Usage:"
    print "%s RANDOM_FILENAME_LIST" % sys.argv[0]
    print "Where:"
    print "RANDOM_FILENAME_LIST  - List of random words used to generate file"
    print "                        and directory names."

if len(sys.argv) != 2:
    print sys.argv
    usage()
    sys.exit(1)
else:
    random_names = sys.argv[1]

# make sure the file exists
if not os.path.exists(random_names):
    usage()
    sys.exit(1)

with open(random_names, 'r') as fp:
    filenames = set([f.strip() for f in fp])


class node(object):
    def __init__(self, name):
        self._name = name
        self._parent = None

    @property
    def parent(self):
        return self._parent

    @parent.setter
    def parent(self, parent):
        self._parent = parent

    @property
    def name(self):
        return self._name

    @property
    def depth(self):
        if self._parent is None:
            return 1
        else:
            return self._parent.depth + 1

    def __str__(self):
        return str(self._name)

    def __repr__(self):
        return self.__str__()


class leaf(node):
    pass


class branch(node):
    def __init__(self, name):
        super(self.__class__, self).__init__(name)
        self._children = []
        self._num_branches = 0

    def add_child(self, child):
        if self._parent is child:
            return
        if isinstance(child, branch):
            self._num_branches += 1
        child.parent = self
        self._children.append(child)

    @property
    def full(self):
        return (len(self._children) >= MAXOBJ or
                self._num_branches >= MAXDIR or
                self.depth > MAXDEPTH
                )

    @property
    def children(self):
        return self._children


class tree(object):
    def __init__(self):
        self.root = branch('/')


# get a random number of total directories to create
# between about a 1/3 and 1/2 of all the names available
total_objs = len(filenames)
min_branches = math.ceil(total_objs/3.3) - 1
max_branches = math.ceil(total_objs/2.2)+1
num_branches = random.randrange(min_branches, max_branches)
num_leaves = total_objs - num_branches

branches = set()
leaves = set()

branch_names = random.sample(filenames, num_branches)
leaf_names = filenames.difference(set(branch_names))

for name in branch_names:
    branches.add(branch(name))
for name in leaf_names:
    leaves.add(leaf(name))

root = branch('root')

# pick root's children
nd = random.randrange(3, MAXDIR)
for child in random.sample(branches, nd):
    root.add_child(child)
for child in random.sample(leaves, MAXOBJ-nd):
    root.add_child(child)

needs_parent = [b for b in branches if b.parent is None]
random.shuffle(needs_parent)
for o in needs_parent:
    p = random.choice([b for b in branches if (b.parent is not None and not b.full)])
    p.add_child(o)


needs_parent = [l for l in leaves if l.parent is None]
random.shuffle(needs_parent)
for l in needs_parent:
    p = random.choice([b for b in branches if not b.full])
    p.add_child(l)


# now we walk the tree?
def walk(n):
    if isinstance(n, leaf):
        print "touch "+n.name
        return
    elif isinstance(n, branch):
        print "mkdir "+n.name
        print "cd "+n.name
        for i in xrange(len(n.children)):
            walk(n.children[i])
        if n.parent is not None:
            print "cd .."
        else:
            print "echo Done"


walk(root)
