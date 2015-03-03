import os
from graph import DirectedGraph, Node, Edge


def files_valid(content_file, cites_file):
    if not os.path.isfile(content_file) or not os.path.isfile(cites_file):
        return False

    return True


def parse_content_file(file_path):
    content_file = open(file_path, 'r')
    file_content = []
    class_labels = []

    for line in content_file:
        content_array = line.split('\t')
        paper_content = {
            'paper_id': content_array[0],
            'class_label': content_array[-1].strip(),
            'word_attributes': content_array[1:-1],
        }
        class_labels.append(content_array[-1].strip())
        file_content.append(paper_content)

    return file_content, set(class_labels)


def parse_cites_file(file_path):
    cites_file = open(file_path, 'r')
    citations = dict()

    for line in cites_file:
        citation_array = line.split('\t')

        citing_paper = citation_array[1].strip()
        cited_paper = citation_array[0].strip()

        if citing_paper in citations:
            citations[citing_paper].append(cited_paper)
        else:
            citations[citing_paper] = [cited_paper]

    return citations


def add_nodes(graph, content_file):
    content, class_labels = parse_content_file(content_file)

    for paper in content:
        new_node = Node(paper['paper_id'], paper['word_attributes'], paper['class_label'])
        graph.add_node(new_node)

    return class_labels


def add_edges(graph, cites_file):
    citations = parse_cites_file(cites_file)

    for citing_paper, cited_papers in citations.iteritems():
        for cited_paper in cited_papers:
            new_edge = Edge(citing_paper, cited_paper)
            graph.add_edge(new_edge)


def load_linqs_data(content_file, cites_file):
    """
    Create a DirectedGraph object and add Nodes and Edges
    This is specific to the data files provided at http://linqs.cs.umd.edu/projects/projects/lbc/index.html
    Return two items 1. graph object, 2. the list of domain labels (e.g., ['AI', 'IR'])
    """
    if not files_valid(content_file, cites_file):
        raise IOError('Input Files Not Valid')
        return

    graph = DirectedGraph()

    class_labels = add_nodes(graph, content_file)
    add_edges(graph, cites_file)

    return graph, class_labels