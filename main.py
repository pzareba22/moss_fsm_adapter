import subprocess
import tempfile
import os
import sys


class Miner:
    def __init__(self, miner_path="./miner"):
        self.miner_path = miner_path

    def run(self, input_file, output_file=None, **kwargs):
        """
        Execute the MoSS miner with specified options.

        Parameters:
            - input_file (str): Path to the input file containing molecule data.
            - output_file (str, optional): Path to the output file to store results. If not provided, a temporary file is used.
            - kwargs: Additional command-line options for the miner.

        For detailed command-line options, refer to the documentation:
        [Command Line Options](./docs/command-line-options.md)

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
    input_file = sys.argv[1]
    miner = Miner()
    output = miner.run(
        input_file,
        jS=True,
        s=50,
        v=True,
    )
    print(output)
