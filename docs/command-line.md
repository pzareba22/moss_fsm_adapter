### Command Line Options
MoSS supports a variety of options, with which the search for frequent substructures can be controlled. For the command line version, these options may be specified in any place on the command line (before, between, or after the normal program arguments). In the graphical user interface, which is described here, these options are specified in the dialog window.

Format Options control the format of the molecule descriptions for the seed and in the input and output files (see Molecule Description Languages).

-i#  	input data format (default: smiles)
-o#  	substructure output format (default: smiles)
-f#  	seed format (line notation) (default: smiles)
Possible formats include smiles and smi for the SMILES format, sln for the SLN format, ctab, mdl and sdf for the SDfile format, linog and lng for the LiNoG (Linear Notation for Graphs) format and finally list, nelist and nel for the node/edge list format. Unfortunately the last two formats, which allow processing arbitrary graphs, are not yet described in this documentation. However, the source package contains example input files in these formats (see the directory moss/data).

Seed Option is used to specify the seed structure to start the search from.

-j#  	seed structure to start the search from
By default it is expected to be in SMILES format, but this may be changed with the option -f#. If this option is not given, an empty seed is used.

Exclusion Options allow to restrict the set of node/atom types (chemical elements) that are considered in the search

-x#  	node types to exclude (as a graph in seed format, default: H)
-y#  	seed types to exclude (as a graph in seed format, default: none)
Split Options control how the graph/molecule database is split into the focus part and the complement part.

-t#  	threshold value for the split (default: 0.5)
-z  	invert split (> versus <= instead of <= versus >)
If one does not want to find discriminative fragments, the complement part should be empty. This can be achieved by specifying a threshold that is larger than any value associated with a molecule in the database.

Size Options control the size a substructure must have in order to be reported.

-m#  	minimum size of a substructure (default: 1)
-n#  	maximum size of a substructure (default: no limit)
Support Options control the minimum frequency for the focus and the maximum frequency for the complement with which a substructure must occur in order to be reported.

-s#  	minimum support in focus (default: 10.0%)
-S#  	maximum support in complement (default: 2.0%)
-k#  	support type (1:MIS, 2:HO, 3:MNI) (default: 0:graphs)
-G  	do not use greedy algorithm for MIS computation (slower)
-C  	do not restrict the output to closed substructures
Note that the support values are interpreted as percentages (of the number of graphs or the total number of nodes, depending on the chosen support type) if they are positive and as absolute numbers if they are negative.

Details about other support types than the number of containing graphs/molecules can be found in [Fiedler and Borgelt 2007].

Matching Options control how atoms and bonds in the molecules are matched by substructures. In particular, they control which atom and bond types are seen as equivalent.

+/-a 	match/ignore aromaticity of atoms (default: ignore/-)
+/-c 	match/ignore charge of atoms (default: ignore/-)
+/-d 	match/ignore atom type (default: match/+)
+/-D 	match/ignore atom type in rings (default: match/+)
+/-: 	upgrade/downgrade aromatic bonds (default: extra type)
+/-b 	match/ignore bond type (default: match/+)
+/-B 	match/ignore bond type in rings (default: match/+)
An atom is aromatic if it is part of an aromatic ring. Downgrading an aromatic bond means treating it as a single bond, upgrading means treating it as a double bond. The option -B only has an effect if rings are marked with the option -r (see below) and then only for the marked rings.

Ring Mining Options lead to rings (or at least ring bonds) being treated differently from other bonds. In addition, they allow switching to extensions by full rings rather than individual bonds in one step (see [Hofer et al. 2004] and [Borgelt 2006]).

-K  	do not convert Kekulé representations to aromatic rings
-r#:# 	mark rings of size # to # bonds (default: no marking)
-R  	extend with rings of marked sizes (default: indiv. bonds)
-E  	bond-by-bond support-filtered ring extensions (includes -O)
-O  	do not record fragments with open rings of marked sizes
In a Kekulé representation an aromatic ring has alternating single and double bonds. In order to avoid mismatches due to a different representation of aromatic rings it is recommended to convert all Kekulé representations to rings with aromatic bonds.

Carbon Chain Option allows to find and match chains of varying length that consist only of carbon atoms that are connected by single bonds and do not have any branches.

-H   	find and match variable length chains of carbon atoms
Extension Options switch between different restricted extensions that are used in the search. Details about restricted extensions can be found in [Borgelt 2005].

-g   	use rightmost path extensions (default: max. source)
Rightmost path extensions are the extension type used in the gSpan algorithm [Yan and Han 2002] and its extension CloseGraph [Yan and Han 2003]. Hence, by specifying -g one can switch to these algorithms. The MoSS/MoFa algorithm, which is the default, uses maximum source index extensions, see [Borgelt 2005].

Pruning Options control the pruning of the search tree. The default is usually the best choice. For details about the pruning methods, see [Borgelt 2005] (canonical form pruning) and [Borgelt et al. 2004] (other pruning methods).

+/-P 	partial perfect extension pruning (default: no/-)
+/-p 	full perfect extension pruning (default: yes/+)
+/-e 	equivalent sibling pruning (default: no/-)
+/-q 	canonical form pruning (default: yes/+)
+/-h 	filter extensions with orbits (default: yes/+)
If canonical form pruning is not used, duplicate substructures are found and eliminated with the help of a repository of already processed substructures.

Embedding Options control how the embeddings of substructures are handled during the search.

-u#  	use embeddings only from level # (default: use always)
(< 0: do not use embeddings at all, 0: use always)
-M#  	maximal number of embeddings per molecule (to save memory)
-U  	unembed siblings of current search tree node (to save memory)
These options can reduce the amount of memory needed in the search, but usually slow down the search process. Not using embeddings at all is advantageous if the graph data set contains (very) few labels.

Debug Options have been introduced for debugging purposes, but may also be useful for testing the program and understanding how the algorithms work.

-N   	normalize fragment output form (for result comparisons)
-v   	verbose output during search (show search tree)
-T   	do not print search statistic
Conversion Options allow to convert data files between different formats. If any of them is given, no substructure search is carried out.

-l   	do not search, only convert input to the output format
-L   	do not search, only convert input to a logic format