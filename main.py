import subprocess
import tempfile
import os
import sys
from collections import defaultdict
from typing import Union


class Miner:
    def __init__(self, miner_path="./miner", base_file_name: Union[None, str] = None, verbose: bool = False):
        self.miner_path = miner_path
        self.verbose = verbose
        self.base_file_name = tempfile.mktemp() if not base_file_name else base_file_name
        self.input_file_name = self.base_file_name + "_input"
        self.substructure_file_name = self.base_file_name + "_output.txt"
        self.identifiers_file_name = self.base_file_name + "_ids.txt"


    def runButCooler(self, x: list[str], **kwargs):
        self.save_input_to_file(x)
        command = self.build_command(**kwargs)
        success = self.run_miner(command)
        if success is True:
            result = self.parse_output_but_cooler()
            return result

    def save_input_to_file(self, x: list[str]) -> None:
        with open(self.input_file_name, 'w') as input_file:
            for smile in x:
                line = f"{smile},0,{smile}\n"
                input_file.write(line)

    def build_command(self, **kwargs) -> list[str]:
        command = [self.miner_path, self.input_file_name]
        for key, value in kwargs.items():
            if isinstance(value, bool):
                if value:
                    command.append(f"-{key}")
            else:
                command.append(f"-{key}{value}")

        command.append(self.substructure_file_name)
        command.append(self.identifiers_file_name)

        return command

    def run_miner(self, command: list[str]) -> bool:
        try:
            result = subprocess.run(command, capture_output=self.verbose, text=True)
            result.check_returncode()

        except subprocess.CalledProcessError as e:
            print("Error running MoSS:", e.stderr)
            return False
        except Exception as e:
            print("An error occurred:", str(e))
            return False
        return True

    def parse_output_but_cooler(self) -> dict[str, list[str]]:
        result = defaultdict(list)
        with open(self.substructure_file_name, "r") as substructure_file, open(self.identifiers_file_name, "r") as identifiers_file:
            substucture_lines = substructure_file.read().strip().split("\n")[1:]
            molecular_lines = identifiers_file.read().strip().split("\n")[1:]

            assert(len(substucture_lines) == len(molecular_lines))

            for substructure_line, molecular_line in zip(substucture_lines, molecular_lines):
                entities = molecular_line.split(':')[1].split(',')
                smile = substructure_line.split(',')[1]
                for entity in entities:
                    result[entity].append(smile)

        return dict(result)






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
        base_file_name = tempfile.mktemp() if not output_file else output_file
        substructure_file_name = base_file_name + "_output.txt"
        identifiers_file_name = base_file_name + "_ids.txt"

        command.append(substructure_file_name)
        command.append(identifiers_file_name)

        output = None
        try:
            # Run the command and capture the output
            # print(f"command being executed: {command}")
            result = subprocess.run(command, capture_output=True, text=True)
            result.check_returncode()  # Raise an error if the command failed

            # Read and parse the output file
            with open(substructure_file_name, "r") as substructure_file, open(identifiers_file_name, "r") as identifiers_file:
                output = self.parse_output(substructure_file.read(), identifiers_file.read()) # TODO refactor this somehow


        except subprocess.CalledProcessError as e:
            print("Error running MoSS:", e.stderr)
        except Exception as e:
            print("An error occurred:", str(e))
        finally:
            if not output_file and os.path.exists(substructure_file_name):
                os.remove(substructure_file_name)

            return output



    def parse_output(self, substucture_data, molecular_id_data):
        result = defaultdict(list)
        substucture_lines = substucture_data.strip().split("\n")[1:]
        molecular_lines = molecular_id_data.strip().split("\n")[1:]

        assert(len(substucture_lines) == len(molecular_lines))

        for substructure_line, molecular_line in zip(substucture_lines, molecular_lines):
            entities = molecular_line.split(':')[1].split(',')
            smile = substructure_line.split(',')[1]
            for entity in entities:
                result[entity].append(smile)

        return dict(result)

# Example usage
if __name__ == "__main__":
    input_file = sys.argv[1]
    miner = Miner(base_file_name="test")

    output = miner.run(
        input_file,
        output_file="./output",
        jS=True,
        s=2, # TODO reconsider
        v=True,
    )
    print(output)
