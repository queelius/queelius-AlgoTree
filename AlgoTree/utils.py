from collections import deque
from typing import Any, Callable, Deque, List, Tuple, Type
from AlgoTree.treenode_api import TreeNodeApi

def visit(node: Any,
          func: Callable[[Any], bool],
          order: str = "post",
          max_hops: int = float("inf"),
          **kwargs) -> bool:
    """
    Visit the nodes in the tree rooted at `node` in a pre-order or post-order
    traversal. The procedure `proc` should have a side-effect you want to
    achieve, such as printing the node or mutating the node in some way.

    If `func` returns True, the traversal will stop and the traversal will
    return True immediately. Otherwise, it will return False after traversing
    all nodes.

    Requirement:

    - This function requires that the node has a `children` property that is
      iterable.

    :param node: The root node to start the traversal.
    :param func: The function to call on each node. The function should take a
                 single argument, the node. It should have some side-effect
                 you want to achieve. See `map` if you want to return a new
                 node to rewrite the sub-tree rooted at `node`.
    :param max_hops: The maximum number of hops to traverse.
    :param order: The order of traversal (`pre`, `post`, or `level`).
    :param kwargs: Additional keyword arguments to pass to `func`.
    :raises ValueError: If the order is not valid.
    :raises TypeError: If func is not callable.
    :raises AttributeError: If the node does not have a 'children'.
    """

    if not callable(func):
        raise TypeError("func must be callable")

    if order not in ("pre", "post", "level"):
        raise ValueError(f"Invalid order: {order}")

    if not hasattr(node, "children"):
        raise AttributeError("node must have a 'children' property")

    if order == "level":
        return breadth_first(node, func, **kwargs)

    s = deque([(node, 0)])
    while s:
        node, depth = s.pop()
        if max_hops < depth:
            continue

        if order == "pre":
            if func(node, **kwargs):
                return True

        s.extend([(c, depth + 1) for c in reversed(node.children)])
        if order == "post":
            if func(node, **kwargs):
                return True

    return False

def map(node: Any,
        func: Callable[[Any], Any],
        order: str = "post",
        **kwargs) -> Any:
    """
    Map a function over the nodes in the tree rooted at `node`. It is a map
    operation over trees. In particular, the function `func`, of type::

        func : Node -> Node,

    is called on each node in pre or post order traversal. The function should
    return a new node. The tree rooted at `node` will be replaced (in-place)
    with the tree rooted at the new node. The order of traversal can be
    specified as 'pre' or 'post'.

    Requirement:

    - This function requires that the node has a `children` property that is
      iterable and assignable, e.g., `node.children = [child1, child2, ...]`.

    :param node: The root node to start the traversal.
    :param func: The function to call on each node. The function should take a
                 single argument, the node, and return a new node (or
                 have some other side effect you want to achieve).
    :param order: The order of traversal (pre or post).
    :param kwargs: Additional keyword arguments to pass to `func`.
    :raises ValueError: If the order is not 'pre' or 'post'.
    :raises TypeError: If func is not callable.
    :return: The modified node. If `func` returns a new node, the tree rooted
             at `node` will be replaced with the tree rooted at the new node.
    """

    if not callable(func):
        raise TypeError("`func` must be callable")

    if order not in ("pre", "post"):
        raise ValueError(f"Invalid order: {order}")

    if not hasattr(node, "children"):
        raise AttributeError("node must have a 'children' property")

    if order == "pre":
        node = func(node, **kwargs)

    if node is None:
        return None

    if hasattr(node, "children"):
        node.children = [c for c in [map(c, func, order, **kwargs) for c in
                         node.children] if c is not None]

    if order == "post":
        node = func(node, **kwargs)

    return node


def descendants(node) -> List:
    """
    Get the descendants of a node.

    :param node: The root node.
    :return: List of descendant nodes.
    """
    results = []
    visit(node, lambda n: results.append(n) or False, order="pre")
    return results[1:]


def siblings(node) -> List:
    """
    Get the siblings of a node.

    :param node: The root node.
    :return: List of sibling nodes.d
    """
    return [] if is_root(node) else [
        c for c in node.parent.children if c != node
    ]


def leaves(node) -> List:
    """
    Get the leaves of a node.

    :param node: The root node.
    :return: List of leaf nodes.
    """
    results = []
    visit(
        node,
        lambda n: results.append(n) or False if not n.children else False,
        order="post",
    )
    return results


def height(node) -> int:
    """
    Get the height of a subtree (containing the node `node`, but any
    other node in the subtree would return the same height)

    :param node: The subtree containing `node`.
    :return: The height of the subtree.
    """
    def _height(n):
        return 0 if is_leaf(n) else 1 + max(_height(c) for c in n.children)
    
    return _height(node)


def depth(node) -> int:
    """
    Get the depth of a node in its subtree view.

    :param node: The node.
    :return: The depth of the node.
    """
    return 0 if is_root(node) else 1 + depth(node.parent)


def is_root(node) -> bool:
    """
    Check if a node is a root node.

    :param node: The node to check.
    :return: True if the node is a root node, False otherwise.
    """
    return node.parent is None


def is_leaf(node) -> bool:
    """
    Check if a node is a leaf node.

    :param node: The node to check.
    :return: True if the node is a leaf node, False otherwise.
    """
    return not is_internal(node)


def is_internal(node) -> bool:
    """
    Check if a node is an internal node.

    :param node: The node to check.
    :return: True if the node is an internal node, False otherwise.
    """
    return len(node.children) > 0


def is_ancestor(node, other) -> bool:
    """
    Check if `node` is an ancestor of `other`.

    :param node: The node to check.
    :param other: The other node.
    :return: True if the node is an ancestor of the other node, False otherwise.
    """
    return other in descendants(node)


def is_descendant(node, other) -> bool:
    """
    Check if node `node` is a descendant of node `other`.

    :param node: The node to check for being a descendant.
    :param other: The node to check for being a descendant of.
    :return: True if `node` is a descendant of `other`, False otherwise.
    """
    return node in descendants(other)


def is_sibling(node, other) -> bool:
    """
    Check if a node is a sibling of another node.

    :param node: The node to check.
    :param other: The other node.
    :return: True if the node is a sibling of the other node, False otherwise.
    """
    return node in siblings(other)


def breadth_first(node: Any,
                  func: Callable[[Any], bool],
                  max_lvl = None,
                  **kwargs) -> bool:
    """
    Traverse the tree in breadth-first order. The function `func` is called on
    each node and level. The function should have a side-effect you want to
    achieve, and if it returns True, the traversal will stop. The keyword
    arguments are passed to `func`.

    If `func` returns True, the traversal will stop and the traversal will
    return True immediately. Otherwise, it will return False after traversing
    all nodes. This is useful if you want to find a node that satisfies a
    condition, and you want to stop the traversal as soon as you find it.

    Requirement:

    - This function requires that the node has a `children` property that is
      iterable.

    - The function `func` should have the signature::

        func(node: Any, **kwargs) -> bool

    :param node: The root node.
    :param func: The function to call on each node and any additional keyword
                 arguments. We augment kwargs with a level key, too, which
                 specifies the level of the node in the tree.
    :param max_lvl: The maximum number of levels to descend. If None, the
                    traversal will continue until all nodes are visited
                    or until `func` returns True.
    :param kwargs: Additional keyword arguments to pass to `func`.
    :raises TypeError: If func is not callable.
    :raises AttributeError: If the node does not have a 'children'.
    :return: None
    """
    if not callable(func):
        raise TypeError("func must be callable")

    if not hasattr(node, "children"):
        raise AttributeError("node must have a 'children' property")

    q: Deque[Tuple[Any, int]] = deque([(node, 0)])
    while q:
        cur, lvl = q.popleft()
        if max_lvl is not None and lvl > max_lvl:
            continue

        kwargs["level"] = lvl
        if func(cur, **kwargs):
            return True

        for child in cur.children:
            q.append((child, lvl + 1))
    return False

def breadth_first_undirected(node, max_hops = float("inf")):
    """
    Traverse the tree in breadth-first order. It treats the tree as an
    undirected graph, where each node is connected to its parent and children.
    """
    within_hops = []
    q : Deque[Tuple[Any, int]] = deque([(node, 0)])
    visited = []
    while q:
        cur, depth = q.popleft()
        if depth > max_hops:
            continue
        if cur not in visited:            
            visited.append(cur)
            within_hops.append(cur)
            for child in cur.children:
                q.append((child, depth + 1))
            if cur.parent is not None:
                q.append((cur.parent, depth + 1))
    return within_hops



def find_nodes(node: Any, pred: Callable[[Any], bool], **kwargs) -> List[Any]:
    """
    Find nodes that satisfy a predicate.

    :param pred: The predicate function.
    :param kwargs: Additional keyword arguments to pass to `pred`.
    :return: List of nodes that satisfy the predicate.
    """
    nodes: List[Any] = []
    visit(
        node,
        lambda n, **kwargs: (nodes.append(n) or False
                             if pred(n, **kwargs) else False),
        order="pre",
    )
    return nodes


def find_node(node: Any, pred: Callable[[Any], bool], **kwargs) -> Any:
    """
    Find closest descendent node of `node` that satisfies a predicate (where
    distance is defined with respect to path length). Technically, an order
    defined by path length is a partial order, sine many desendents that
    satisfy the condition may be at the same distance from `node`. We leave
    it up to each implementation to define which among these nodes to return.
    Use `find_nodes` if you want to return all nodes that satisfy the condition
    (return all the nodes in the partial order).
    
    The predicate function `pred` should return True if the node satisfies the
    condition. It can also accept
    any additional keyword arguments, which are passed to the predicate. Note
    that we also augment the keyword arguments with a level key, which specifies
    the level of the node in the tree, so you can use this information in your
    predicate function.

    :param pred: The predicate function which returns True if the node satisfies
                 the condition.
    :param kwargs: Additional keyword arguments to pass to `pred`.
    :return: The node that satisfies the predicate.
    """
    result = None
    def _func(n, **kwargs):
        nonlocal result
        if pred(n, **kwargs):
            result = n
            return True
        else:
            return False

    breadth_first(node, _func, **kwargs)
    return result


def prune(node: Any, pred: Callable[[Any], bool], **kwargs) -> Any:
    """
    Prune the tree rooted at `node` by removing nodes that satisfy a predicate.
    The predicate function should return True if the node should be pruned. It
    can also accept any additional keyword arguments, which are passed to the
    predicate.

    :param node: The root node.
    :param pred: The predicate function which returns True if the node should be
                 pruned.
    :param kwargs: Additional keyword arguments to pass to `pred`.
    :return: The pruned tree.
    """
    return map(node=node,
               func=lambda n, **kwargs: None if pred(n, **kwargs) else n,
               order="pre",
               **kwargs)


def node_to_leaf_paths(node: Any) -> List:
    """
    List all node-to-leaf paths in a tree. Each path is a list of nodes from the
    current node `node` to a leaf node.

    Example: Suppose we have the following sub-tree structure for node `A`::

        A
        ├── B
        │   ├── D
        │   └── E
        └── C
            └── F
    
    Invoking `node_to_leaf_paths(A) enumerates the following list of paths::

        [[A, B, D], [A, B, E], [A, C, F]]
    
    :param node: The current node.
    :return: List of paths in the tree under the current node.
    """

    paths = []
    def _find_paths(n, path):
        if is_leaf(n):
            paths.append(path + [n])
        else:
            for c in n.children:
                _find_paths(c, path + [n])

    _find_paths(node, [])
    return paths


def find_path(source: Any, dest: Any) -> Any:
    """
    Find the path from a source node to a destination node.

    :param source: The source node.
    :param dest: The destination node.
    :return: The path from the source node to the destination node.
    """

    def _find_path(n, path):
        if n == dest:
            return path + [n]
        for c in n.children:
            p = _find_path(c, path + [n])
            if p:
                return p

    return _find_path(source, [])

def ancestors(node) -> List:
    """
    Get the ancestors of a node.

    We could have used the `path` function, but we want to show potentially
    more efficient use of the `parent` property. As a tree, each node has at
    most one parent, so we can traverse the tree by following the parent
    relationship without having to search for the path from the root to the
    node. If parent pointers are not available but children pointers are, we
    can use the `path` function. In our implementations of trees, we implement
    both parent and children pointers.

    :param node: The root node.
    :return: List of ancestor nodes.
    """
    def _ancestors(n):
        nonlocal anc
        if not is_root(n):
            anc.append(n.parent)
            _ancestors(n.parent)

    anc = []
    _ancestors(node)
    return anc


def path(node: Any) -> List:
    """
    Get the path from the root node to the given node.

    :param node: The node.
    :return: The path from the root node to the given node.
    """
    return find_path(node.root, node)

def size(node: Any) -> int:
    """
    Get the size of the subtree under the current node.

    :param node: The node.
    :return: The number of descendents of the node.
    """
    return len(descendants(node)) + 1

def lca(node1: Any, node2: Any) -> Any:
    """
    Find the lowest common ancestor of two nodes.

    :param node1: The first node.
    :param node2: The second node.
    :return: The lowest common ancestor of the two nodes.
    """
    path1 = path(node1)
    path2 = path(node2)
    lca_node = None
    for n1, n2 in zip(path1, path2):
        if n1 == n2:
            lca_node = n1
        else:
            break
    return lca_node

def distance(node1: Any, node2: Any) -> int:
    """
    Find the distance between two nodes.

    :param node1: The first node.
    :param node2: The second node.
    :return: The distance between the two nodes.
    """
    return depth(node1) + depth(node2) - 2 * depth(lca(node1, node2))

def subtree_rooted_at(node: Any, max_lvl: int) -> Any:
    """
    Get the subtree centered at a node within a certain number of hops
    from the node. We return a subtree rooted at some ancestor of the node,
    or the node itself, that contains all nodes within `max_hops` hops
    from the node.

    :param node: The node.
    :return: The subtree centered at the node.
    """
    
    within_hops = []
    def _helper(node, **kwargs):
        within_hops.append(node)
        return False
    breadth_first(node, _helper, max_lvl)

    def _build(n, par):
        new_node = type(n)(name=n.name, payload=n.payload, parent=par)
        #new_node = n.clone(par)
        for c in n.children:
            if c in within_hops:
                _build(c, new_node)
        return new_node
    
    return _build(node, None)


def subtree_centered_at(node: Any, max_hops: int) -> Any:
    """
    Get the subtree centered at a node within a certain number of hops
    from the node. We return a subtree rooted at some ancestor of the node,
    or the node itself, that contains all nodes within `max_hops` hops
    from the node.

    :param node: The node.
    :return: The subtree centered at the node.
    """
    
    within_hops = breadth_first_undirected(node, max_hops)
    root = node
    while root.parent is not None:
        print("Root: ", root.parent)
        if root.parent in within_hops:
            print(f"Making {root.parent} the root")
            root = root.parent

    print(f"Root: {root.name}")
    print([n.name for n in within_hops])

    def _build(n, par):
        #new_node = n.clone(par)
        new_node = type(n)(name=n.name, payload=n.payload, parent=par)
        for c in n.children:
            if c in within_hops:
                _build(c, new_node)
        return new_node
    
    return _build(root, None)


def node_stats(node,
               node_name: Callable = lambda node: node.name,
               payload: Callable = lambda node: node.payload):
    """
    Gather statistics about the current node and its subtree.

    :param node: The current node in the subtree.
    :param node_name: A function that returns the name of a node. Defaults to
                      returning the node's `name` property.
    :param payload: A function that returns the payload of a node. Defaults to
                    returning the node's `payload` property.
    :return: A dictionary containing the statistics.
    """
    #TreeNodeApi.check(node)
    return {
        "node_info": {
            "type": str(type(node)),
            "name": node_name(node),
            "payload": payload(node),
            "children": [node_name(n) for n in node.children],
            "parent": node_name(node.parent) if node.parent else None,
            "depth": depth(node),
            "is_root": is_root(node),
            "is_leaf": is_leaf(node),
            "is_internal": is_internal(node),
            "ancestors": [node_name(n) for n in ancestors(node)],
            "siblings": [node_name(n) for n in siblings(node)],
            "descendants": [node_name(n) for n in descendants(node)],
            "path": [node_name(n) for n in path(node)],
            "root_distance": distance(node.root, node),
            "leaves_under": [node_name(n) for n in leaves(node)]
        },
        "subtree_info": {
            "leaves": [node_name(n) for n in leaves(node.root)],
            "height": height(node),
            "root": node_name(node.root),
            "size": size(node)
        }
    }


def paths_to_tree(paths: List,
                  type: Type,
                  payload_func: Callable = None,
                  max_rename_tries: int = 10000):
    nodes = { }
    for p in paths:
        parent = None
        path = []
        for n in p:
            path.append(n)
            path_tuple = tuple(path)
            name = n.name if hasattr(n, "name") else str(n)
            if payload_func is None:
                payload = n.payload if hasattr(n, "payload") else {}
            else:
                payload = payload_func(n)

            if path_tuple not in nodes:
                tries = 0
                base_name = name
                retry = True
                while retry and tries < max_rename_tries:
                    try:
                        new_node = type(name=name, parent=parent, **payload)
                        retry = False
                    except KeyError as e:
                        name = f"{base_name}_{tries}"
                    tries += 1

                if tries == max_rename_tries:
                    raise ValueError(f"Failed to create node with name {base_name} after {max_rename_tries} suffixe tries")

                nodes[path_tuple] = new_node

            parent = nodes[path_tuple]
    return parent.root
