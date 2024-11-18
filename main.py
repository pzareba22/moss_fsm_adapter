import subprocess
import tempfile
import os


class MinerInterface:
    def __init__(self, miner_path="./miner"):
        self.miner_path = miner_path

    def run(self, input_file, output_file=None, **kwargs):
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
        if not output_file:
            output_file = tempfile.mktemp()

        command.append(output_file)

        output = None
        try:
            # Run the command and capture the output
            result = subprocess.run(command, capture_output=True, text=True)
            result.check_returncode()  # Raise an error if the command failed

            # Read and parse the output file
            with open(output_file, "r") as file:
                output = file.read()
            output = self.parse_output(output)
        except subprocess.CalledProcessError as e:
            print("Error running MoSS:", e.stderr)
        except Exception as e:
            print("An error occurred:", str(e))
        finally:
            if output_file and os.path.exists(output_file):
                os.remove(output_file)

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
    miner = MinerInterface()
    output = miner.run("./moss/data/example1.smi", jS=True, s=50, v=True)
    if output:
        print(output)
