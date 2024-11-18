import subprocess
import tempfile
import os


class Miner:
    def __init__(self, miner_path="./miner"):
        self.miner_path = miner_path

    def run(self, input_file, output_file=None, **kwargs):
        """
        Execute the MoSS miner with specified options.

        Parameters:
            - input_file (str): Path to the input file containing molecule data.
            - output_file (str, optional): Path to the output file to store results. If not provided, a temporary file is used.
            - kwargs: Additional command-line options for the miner. Supported options include:

        Format Options:
            - i (str): Input data format (default: smiles).
            - o (str): Substructure output format (default: smiles).
            - f (str): Seed format (line notation) (default: smiles).

        Seed Option:
            - j (str): Seed structure to start the search from.

        Exclusion Options:
            - x (str): Node types to exclude (default: H).
            - y (str): Seed types to exclude (default: none).

        Split Options:
            - t (float): Threshold value for the split (default: 0.5).
            - z (bool): Invert split.

        Size Options:
            - m (int): Minimum size of a substructure (default: 1).
            - n (int): Maximum size of a substructure (default: no limit).

        Support Options:
            - s (float): Minimum support in focus (default: 10.0%).
            - S (float): Maximum support in complement (default: 2.0%).
            - k (int): Support type (1:MIS, 2:HO, 3:MNI) (default: 0:graphs).
            - G (bool): Do not use greedy algorithm for MIS computation.
            - C (bool): Do not restrict the output to closed substructures.

        Matching Options:
            - a (bool): Match/ignore aromaticity of atoms.
            - c (bool): Match/ignore charge of atoms.
            - d (bool): Match/ignore atom type.
            - D (bool): Match/ignore atom type in rings.
            - : (bool): Upgrade/downgrade aromatic bonds.
            - b (bool): Match/ignore bond type.
            - B (bool): Match/ignore bond type in rings.

        Ring Mining Options:
            - K (bool): Do not convert Kekulé representations to aromatic rings.
            - r (str): Mark rings of size # to # bonds.
            - R (bool): Extend with rings of marked sizes.
            - E (bool): Bond-by-bond support-filtered ring extensions.
            - O (bool): Do not record fragments with open rings of marked sizes.

        Carbon Chain Option:
            - H (bool): Find and match variable length chains of carbon atoms.

        Extension Options:
            - g (bool): Use rightmost path extensions.

        Pruning Options:
            - P (bool): Partial perfect extension pruning.
            - p (bool): Full perfect extension pruning.
            - e (bool): Equivalent sibling pruning.
            - q (bool): Canonical form pruning.
            - h (bool): Filter extensions with orbits.

        Embedding Options:
            - u (int): Use embeddings only from level #.
            - M (int): Maximal number of embeddings per molecule.
            - U (bool): Unembed siblings of current search tree node.

        Debug Options:
            - N (bool): Normalize fragment output form.
            - v (bool): Verbose output during search.
            - T (bool): Do not print search statistic.

        Conversion Options:
            - l (bool): Do not search, only convert input to the output format.
            - L (bool): Do not search, only convert input to a logic format.

        Returns:
            - dict: Parsed output containing substructures and molecule identifiers.
        """

        # Build the command with the provided arguments
        command = [self.miner_path, input_file]

        # Add additional command-line arguments
        for key, value in kwargs.items():
            if isinstance(value, bool):
                if value:
                    command.append(f"-{key}")
            else:
                command.append(f"-{key}{value}")

        # Add the output file if specified
        file_name = tempfile.mktemp() if not output_file else output_file

        command.append(file_name)

        output = None
        try:
            # Run the command and capture the output
            result = subprocess.run(command, capture_output=True, text=True)
            result.check_returncode()  # Raise an error if the command failed

            # Read and parse the output file
            with open(file_name, "r") as file:
                output = self.parse_output(file.read())
        except subprocess.CalledProcessError as e:
            print("Error running MoSS:", e.stderr)
        except Exception as e:
            print("An error occurred:", str(e))
        finally:
            if not output_file and os.path.exists(file_name):
                os.remove(file_name)

            return output

    def parse_output(self, output):
        # Split the output into lines
        lines = output.strip().split("\n")

        # Initialize lists to store parsed data
        substructures = []
        molecule_identifiers = []

        # Determine the type of file based on the first line
        if lines[0].startswith("id,description,nodes,edges,s_abs,s_rel,c_abs,c_rel"):
            # Parse substructure file
            for line in lines[1:]:
                parts = line.split(",")
                substructure = {
                    "id": int(parts[0].strip()),
                    "description": parts[1].strip(),
                    "nodes": int(parts[2].strip()),
                    "edges": int(parts[3].strip()),
                    "s_abs": int(parts[4].strip()),
                    "s_rel": float(parts[5].strip()),
                    "c_abs": int(parts[6].strip()),
                    "c_rel": float(parts[7].strip()),
                }
                substructures.append(substructure)
        elif lines[0].startswith("id:list"):
            # Parse molecule identifier file
            for line in lines[1:]:
                subid, graphids = line.split(":")
                molecule_identifier = {
                    "subid": int(subid.strip()),
                    "graphids": [int(gid.strip()) for gid in graphids.split(",")],
                }
                molecule_identifiers.append(molecule_identifier)

        # Return parsed data
        return {
            "substructures": substructures,
            "molecule_identifiers": molecule_identifiers,
        }


# Example usage
if __name__ == "__main__":
    miner = Miner()
    output = miner.run(
        "./moss/data/example1.smi",
        jS=True,
        s=50,
        v=True,
    )
    print(output)
