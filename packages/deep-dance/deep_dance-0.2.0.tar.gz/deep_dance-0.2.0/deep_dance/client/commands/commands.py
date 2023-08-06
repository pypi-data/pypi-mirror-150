from cleo import Command, option
import os 
from subprocess import call
import time 

""""
class DeepDanceRun(Command):

    name = "run-deep-dance"
    description = "Run the DeepDANCE algorithm implementation."
    arguments = []
    options = [
        option(long_name="--config_path", value_required=True),
        option(long_name="--unknowns_supplied", default=True),
        option(long_name="--file_paths_supplied", value_required=True),
        option(long_name="--output_directory", default=os.getcwd()),
        option(long_name="--domain_type", default="open"),  # implement later
    ]

    def handle(self):
        config_path = self.option("--config_path")
        unk_sup = self.option("--unknowns_supplied")
        file_pth_sup = self.option("--file_paths_supplied")
        if self.option("--output_directory"):
            output_dir = self.option("--output_directory")

        #   0. Check if the config path is valid.
        #   1. Check that all the config path arguments make sense.
        self.overwrite(config_path, unk_sup)
        if file_pth_sup:
            rc = call(f"./scripts/run_obda.sh $0 {config_path}")
        else:
            self.write(file_pth_sup)
            rc = call(f"./scripts/run_obda.sh $0 {config_path}")


        # Check if the output directory exists
"""

class DeepDanceDemoRun(Command):

    name = "run_deep_dance_demo"
    description = "Run the DeepDANCE algorithm implementation."
    arguments = []
    options = [
        option(long_name="config-path", value_required=True),
        option(long_name="unknowns-supplied"),
        option(long_name="file-paths-supplied", value_required=True),
        option(long_name="output-directory"),
        option(long_name="--domain-type"),  # implement later
    ]

    def handle(self):
        config_path = self.option("config-path")
        unk_sup = self.option("unknowns-supplied")
        file_pth_sup = self.option("file-paths-supplied")
        output_dir = self.option("output-directory")

        #   0. Write the configuration options entered by the user.
        self.write(f" Configuration parameters are as follows: \n Config Path: {config_path} \n Number of Unknowns Supplied?: {unk_sup} \n File Paths Supplied?: {file_pth_sup} \n Output Directory: {output_dir}")
        
        #   1. Check for valid config path.
        self.write(f"Checking that the path {config_path} exists.\n")
        time.sleep(1)
        self.overwrite(f"Path exists!\n")
        #   2. If number of unknowns supplied, update the config file.
        self.write("Updating config file to account for whether your unknowns are supplied.\n")
        time.sleep(4)
        #   3. Check for valid output directory.
        self.write(f"Checking that the path {output_dir} exists. If not, one will be created.\n")
        if not os.path.exists("records"):
            os.mkdir("records")
        #   4. If file path not supplied, run util to make the file path txt file.
        self.write(f"File Path Supplied is False. One will be configured for you. Please ensure folders are in correct format.\n")
        time.sleep(5)
        self.write("File path text file configured successfully!\n")
        #   5. Check that all the config path arguments make sense.
        self.write(f"Ensuring valid config path structure...\n")
        time.sleep(7)
        self.overwrite(f"Configuration path secured!\n")
        #   6. Begin training ... print out ETA and progress bar.
        self.write(f"Beginning training!\n")
        time.sleep(9)
        #   7. Training ends.
        self.overwrite(f"Training has completed! Output files will be placed their designated folders in {output_dir}.\n")
        time.sleep(3)
        #   8. Output loss, accuracy, t-SNE files.
        self.write(f"Output files, saved models, and t-SNE window available! Please exit t-SNE window to cease function.\n")
        time.sleep(5)

        #   9. Output saved models. 
        self.overwrite(config_path, unk_sup)
        if file_pth_sup:
            rc = call(f"./scripts/run_obda.sh $0 {config_path}")
        else:
            self.write(file_pth_sup)
            rc = call(f"./scripts/run_obda.sh $0 {config_path}")



