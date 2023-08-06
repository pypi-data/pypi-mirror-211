import argparse
import os
from ordering import order_taxa



def check_file(f):
    if not os.path.isfile(f):
        raise ValueError(f'File not found at: {f}')


def main():
    parser = argparse.ArgumentParser(
        description='Returns list of species in a phylogenetic tree ordered '
                    'by increasing taxonomic distance to a reference species'
    )
    parser.add_argument(
        '-t', '--tree', metavar='<path>', type=str, required=True,
        help='Path to tree in Newick format'
    )
    parser.add_argument(
        '-r', '--reference', metavar='str', type=str, required=True,
        help='Reference species'
    )
    parser.add_argument(
        '--outfile', metavar='str', type=str, nargs='?', const='', default='',
        help=(
            'Save output to file'
        )
    )
    parser.add_argument(
        '--format', metavar='str', type=int, nargs='?', const=1, default=1,
        help=(
            'Tree format as specified at: \n'
            'https://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#reading-and-writing-newick-trees\n'
            '(Default: 1)'
        )
    )
    parser.add_argument(
        '--idmap', metavar='<path>', type=str, nargs='?', const='', default='',
        help=(
            'TaxOrder can map species names to taxids accepted by '
            'PhyloProfile if supplied with a tab-seperated file like:\n'
            'taxid\tname'
        )
    )


    args = parser.parse_args()
    for file in [args.tree, args.idmap, args.outfile]:
        if file:
            check_file(file)
            
    # work    
    outnames = order_taxa(args.tree, args.reference, format=args.format, idmap=args.idmap)

    # output
    if args.outfile:
        with open(args.outfile, 'w') as of:
            for name in outnames:
                of.write(f'{name}\n')
    for name in outnames:
        print(name)


if __name__ == "__main__":
    main()
