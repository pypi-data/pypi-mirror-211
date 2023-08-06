usage: taxOrder.py [-h] -t <path> -r str [--outfile [str]] [--format [str]] [--idmap [<path>]]

Returns list of species in a phylogenetic tree ordered by increasing taxonomic distance to a reference species


  -h, --help            show this help message and exit

  -t <path>, --tree <path>
                        Path to tree in Newick format

  -r , --reference str
                        Reference species

optional arguments:

  --outfile [str]       Save output to file

  --format [str]        Tree format as specified at: https://etetoolkit.org/docs/latest/tutorial/tutorial_trees.html#reading-and-writing-newick-trees (Default: 1)

  --idmap [<path>]      TaxOrder can map species names to taxids accepted by PhyloProfile if supplied with a tab-seperated file like: taxid name
