
 #####    ####
 #    #  #
 #    #   ####
 #    #       #
 #    #  #    #
 #####    ####
 
class DisjointSet:

  class Node:

    _rank = -1
    _val = None
    _parent = None


    def __init__(self, val):

      self._rank = 1
      self._val = val
      self._parent = self


    @property
    def val(self):

      return self.val


  _sets = {}


  def __init__(self):

    self._sets = {}


  def makeSet(self, val):

    if val not in self._sets:
      self._sets[val] = self.Node(val)


  def join(self, valLhs, valRhs):

    lhs = self._sets[valLhs]
    rhs = self._sets[valRhs]
    lhsParent = self.find(lhs)
    rhsParent = self.find(rhs)

    if lhsParent == rhsParent:
      return

    parent = lhsParent
    child = rhsParent
    if lhsParent._rank < rhsParent._rank: # path compress
      parent = rhsParent
      child = lhsParent
    child._parent = parent
    parent._rank = max(parent._rank, child._rank+1)


  def find(self, node):

    nodes = [node]
    while node._parent != node:
      nodes.append(node)
      node = node._parent

    # path compress trick
    for i in range(1, len(nodes)):
      nodes[-i]._parent = nodes[-i+1]._parent

    return nodes[0]._parent

  def findVal(self, val):

    return self.find(self._sets[val])
