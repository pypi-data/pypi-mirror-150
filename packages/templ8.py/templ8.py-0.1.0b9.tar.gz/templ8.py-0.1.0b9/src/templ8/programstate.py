import os
from templ8.blessing import makedir
from templ8.blessing import mod_replaces

class ProgramState:
    def __init__(self):
        self.deity_path = r"d8y"
        self.basehtml_path = r"basehtml"
        self.replacements_path = r"repl8ce"
        self.txignore_path = r"txignore"
        self.replacements = {}

        self.input_folder = r"input"
        self.output_folder = r"output"
                
        
        # Load d8y
        if not os.path.exists(self.deity_path):
            raise Exception("No " + self.deity_path + " file found")
        
        # Core Renaming
        with open(self.deity_path, "r") as d8y_file:
            for line in d8y_file.readlines():
                keyval = line.split("=")
                if len(keyval) != 2:
                    raise Exception("Error in d8y file format:\n   " + line)
                if keyval[0] == "input" and keyval[1]:
                    self.input_folder = keyval[1]
                elif keyval[0] == "output" and keyval[1]:
                    self.output_folder = keyval[1]
                elif keyval[0] == "replace" and keyval[1]):
                    self.replacements_path = keyval[1]
                elif keyval[0] == "basehtml":
                    self.basehtml_path = keyval[1]
                elif keyval[0] == "txignore" and keyval[1]:
                    self.txignore_path = keyval[1]
        
        
        self.input_folder = os.path.normpath(self.input_folder)
        self.output_folder = os.path.normpath(self.output_folder)
        self.replacements_path = os.path.normpath(self.replacements_path)
        self.basehtml_path = os.path.normpath(self.basehtml_path)
        self.txignore_path = os.path.normpath(self.txignore_path)

        if not os.path.exists(self.basehtml_path):
            raise Exception("No " + self.basehtml_path + " file found")

        self.basehtml_content = open(self.basehtml_path, "r").read()

        
        # Make input and output folder if they don't yet exist
        makedir(self.input_folder, "No input directory found, creating one")
        makedir(self.output_folder, "No output directory found, creating one")

        # Load the replacements from repl8ce
        if os.path.exists(self.replacements_path):
            replacement_text = open(self.replacements_path, "r").read()
            mod_replaces(self.replacements, replacement_text)
        else:
            print("WARNING: No " + self.replacements_path + " file found, continuing")

        
        # Load txignore
        self.txignore = []
        if os.path.exists(self.txignore_path):
            self.txignore = open(self.txignore_path, "r").readlines()