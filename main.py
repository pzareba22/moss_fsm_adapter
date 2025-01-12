import subprocess
import tempfile
import os
import sys
from collections import defaultdict


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
        base_file_name = tempfile.mktemp() if not output_file else output_file
        output_file_name = base_file_name + "_output.txt"
        identifiers_file_name = base_file_name + "_ids.txt"

        command.append(output_file_name)
        command.append(identifiers_file_name)

        output1 = None
        output2 = None
        try:
            # Run the command and capture the output
            # print(f"command being executed: {command}")
            result = subprocess.run(command, capture_output=True, text=True)
            result.check_returncode()  # Raise an error if the command failed

            # Read and parse the output file
            with open(output_file_name, "r") as file:
                output1 = self.parse_output(file.read()) # TODO refactor this somehow

            with open(identifiers_file_name, "r") as file:
                output2 = self.parse_output(file.read()) # TODO refactor this somehow

        except subprocess.CalledProcessError as e:
            print("Error running MoSS:", e.stderr)
        except Exception as e:
            print("An error occurred:", str(e))
        finally:
            if not output_file and os.path.exists(output_file_name):
                os.remove(output_file_name)

            return {
                "substructures": output1["substructures"],
                "molecule_identifiers": output2["molecule_identifiers"]
            }


    def parse_output_but_cooler(self, substucture_data, molecular_id_data):
        result = defaultdict(list)
        substucture_lines = substucture_data.strip().split("\n")[1:]
        molecular_lines = molecular_id_data.strip().split("\n")[1:]

        assert(len(substucture_lines) == len(molecular_lines))

        for substructure_line, molecular_line in zip(substucture_lines, molecular_lines):
            entities = molecular_line.split(':')[1].split(',')
            smile = substructure_line.split(',')[1]
            for entity in entities:
                result[entity].append(smile)

        # for line in molecular_lines:
        #     assert(len(line.split(':')) == 2)
        #
        #     sub_id, line = line.split(':')
        #     entities = line.split(',')
        #
        #     for entity in entities:
        #         result[entity].append(int(sub_id.strip()))
        #
        # result = dict(result)
        #
        # for line in substucture_lines:
        #     sub_id, smile = line.split(',')[0], line.split(',')[1] 
        #     for entity, substructures in result.items():
        #         result[entity] = [smile if x == sub_id else x for x in substructures]

        return dict(result)

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
                    "subid": subid.strip(),
                    "graphids": [gid.strip() for gid in graphids.split(",")],
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

    example_output = """
        id:list
        1:Chlorimuron-ethyl (ph 7),Sulfanilamide,Bensulide,Indapamide,Metolazone,Ethoxyzolamide,acetazolamide,sulfaguanidine,Perfluidone,piroxicam,hydrochlorothiazide,Quinethazone,p-Toluenesulfonamide,Trichlomethiazide,Bendroflumethiazide,chlorothiazide,Xipamide,oryzalin,Mefluidide,Chlorthalidone
        2:Chlorimuron-ethyl (ph 7),Sulfanilamide,Bensulide,Indapamide,Metolazone,Ethoxyzolamide,acetazolamide,acetyl sulfisoxazole,sulfaguanidine,Perfluidone,piroxicam,hydrochlorothiazide,Quinethazone,p-Toluenesulfonamide,Trichlomethiazide,Bendroflumethiazide,chlorothiazide,Xipamide,oryzalin,Mefluidide,Chlorthalidone
    """


    dupa = """
        id,description,nodes,edges,s_abs,s_rel,c_abs,c_rel
        1,S(-N)(-C)(=O)=O,5,4,20,2.0703933,0,0.0
        2,S(-N)(-C)=O,4,3,21,2.173913,0,0.0
    """
    res = miner.parse_output_but_cooler(dupa, example_output)
    print(res)

    # output = miner.run(
    #     input_file,
    #     output_file="./output",
    #     jS=True,
    #     s=2, # TODO reconsider
    #     v=True,
    # )
    # print(output)
