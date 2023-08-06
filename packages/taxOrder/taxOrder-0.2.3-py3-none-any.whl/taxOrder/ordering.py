import ete3 as ete


def initial_list(t, reference):
    copylist = []
    node = t.search_nodes(name=reference)[0]
    while node:
        for subnode in node:
            copylist.append(subnode.name)
        node = node.up
    return copylist


def order_species(ilist):
    specorder = []
    for name in ilist:
        if name not in specorder:
            specorder.append(name)
    return specorder


def parse_mappingfile(path):
    n2t = {}
    with open(path) as sh:
        for line in sh:
            taxid, name = line.strip().split()
            n2t[name] = f'ncbi{taxid}'
            if len(name.split('_')) > 2:
                shortname = '_'.join(name.split('_')[:2])
                n2t[shortname] = f'ncbi{taxid}'
    return n2t


def order_taxa(tree, reference, format=1, idmap=''):
    tree = ete.Tree(tree, format=format)
    initial = initial_list(tree, reference)
    specorder = order_species(initial)
    # mapping
    if idmap:
        name2taxid = parse_mappingfile(idmap)
        outnames = [name2taxid[name] for name in specorder]
    else:
        outnames = specorder
    return outnames
