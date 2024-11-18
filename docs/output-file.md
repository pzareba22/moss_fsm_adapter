Formats of the Output Files
MoSS writes one or two output files, depending on how many file names were provided on the command line: a substructure file (always written) and an graph/molecule identifier file (optional).

Substructure File
The substructure output file contains the found substructures. This file may either be an SDfile or a text file with one substructure per line, together with some additional information. Each found substructure is described by six fields.

The first line of such an output file is always

id,description,nodes,edges,s_abs,s_rel,c_abs,c_rel
which indicates the meaning of the fields in the following lines.
Consequently the following lines have the general form

<id> , <desc> , <nodes> , <edges> , <s_abs> , <s_rel> , <c_abs> , <c_rel>
<id>  	is an identifier for the substructure, which is a simple consecutive number, starting with 1 for the first substructure. Note that the order in which substructures are reported depends on the search process and may differ depending on the selected search mode.
<desc>  	is a description of the substructure in either SMILES or SLN format (see Molecule Description Languages) or LiNoG or NEList formal (for general graphs). By default SMILES is used, but this may be changed using the option -o#.
<nodes>  	is the number of nodes/atoms of the substructure.
<edges>  	is the number of edges/bonds of the substructure.
<s_abs>  	is the absolute support of the substructure in the focus part of the database, that is, the number of graphs/molecules in the focus part that contain this substructure.
<s_rel>  	is the relative support of the substructure in the focus part of the database, that is, the percentage of graphs/molecules in the focus part that contain this substructure.
<c_abs>  	is the absolute support of the substructure in the complement part of the database, that is, the number of graphs/molecules in the complement part that contain this substructure.
<c_rel>  	is the relative support of the substructure in the complement part of the database, that is, the percentage of graphs/molecules in the complement part that contain this substructure.
If the output file is an SDfile, the support information is stored together with the field name "support", in two lines: one for the support in the focus (first the absolute support, than the relative supprt) and one for the support in the complement (ditto).

Molecule Identifier File
The molecule identifier output file contains, for each found substructure, a list of the graphs/molecules the substructure is contained in. Each line corresponds to one substructure, which is referred to by its identifier (see above). The containing graphs/molecules are also referred to by their identifiers as they were specified in the input file (see Input File).

The first line of such an identifier file is always

id:list
Each line of this output file has the general format

<subid> : <graphid> [ , <graphid> ]*
where

<subid>  	is the identifier of a substructure as it is specified in the substructure output file, that is, a number between 1 and the number of found substructures.
<graphid>  	is the identifier of a graph/molecule that contains the substructure as it was specified in the input file.
The order in which the graphs/molecules are listed is the same as the order in the input file, with the only exception that the graphs/molecules in the focus part of the database precede the molecules in the complement part.

