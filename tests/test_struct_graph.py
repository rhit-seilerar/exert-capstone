from  exert.usermode.struct_graph import TASK_STRUCT, Graph, Node

def test_graph_is_acyclic():
    def helper(graph, visited, node):
        visited = visited.copy()
        visited.append(node)
        for child_id in node.children:
            child = graph.nodes[child_id]
            assert child not in visited
            helper(graph, visited, child)
    helper(TASK_STRUCT, [], TASK_STRUCT.root)

def test_graph_is_complete():
    def helper(graph, visited, node):
        if node in visited:
            return
        visited.append(node)
        for child_id in node.children:
            helper(graph, visited, graph.nodes[child_id])
    graph = TASK_STRUCT
    visited = []
    helper(graph, visited, graph.root)
    assert len(visited) == len(graph.nodes)

def test_graph_data_is_valid():
    def helper(graph, visited, node):
        if node in visited:
            return
        visited.append(node)
        assert isinstance(node, Node)
        assert node is not None
        assert isinstance(node.name, str)
        assert isinstance(node.type, str)
        assert isinstance(node.is_pointer, bool)
        assert isinstance(node.is_optional, bool)
        for child_id in node.children:
            helper(graph, visited, graph.nodes[child_id])
    assert isinstance(TASK_STRUCT, Graph)
    assert isinstance(TASK_STRUCT.name, str)
    helper(TASK_STRUCT, [], TASK_STRUCT.root)
