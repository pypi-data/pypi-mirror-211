from pygments import highlight, lexers, formatters
from bson import ObjectId
import glob
import json
import yaml
import subprocess
import os
import ast

from .parser_base import parser_base


class parser_ros2(parser_base):
    def __init__(self, logging) -> None:                                
        self.log = logging
        
        self.project = None


    def print(self, json_data):
        formatted_json = json.dumps(json_data, indent=4, default=str)
        self.log.info(formatted_json)
        # colorful_json = highlight(bytes(formatted_json, 'UTF-8'), lexers.JsonLexer(), formatters.TerminalFormatter())
        # self.log.debug(colorful_json)


    # Any lang
    def parse_xml(self, package_path):    
        import xml.etree.ElementTree as ET
        path_to_package_xml = f"{package_path}/package.xml"                
        tree = ET.parse(path_to_package_xml)
        root = tree.getroot()
        
        return {
            "package_xml": path_to_package_xml,
            
            "package_name": root.find("name").text,
            "version": root.find("version").text,
            "maintainer": root.find("maintainer").text,
            "maintainer_email": root.find("maintainer").attrib["email"],
            "description": root.find("description").text,
            "license": root.find("license").text,
            "nodes": [],
            "build_type": root.find("export").find("build_type").text,
        }
    

    ########################################### C / CPP ###########################################

    def parse_makefile(self, package_path):        
        import re
        path_to_cmake = f"{package_path}/CMakeLists.txt"        
        f = open(path_to_cmake, "r")
        package_py_content = f.read()          
        # nodes_list = re.search("(?<=install\(TARGETS)($[\S\s]*)(?=DESTINATION)", package_py_content)
        matches = re.finditer(r"install\(TARGETS([\S\s]*?)DESTINATION", package_py_content, re.MULTILINE)
        
        #(?<=install\(TARGETS)($[\S\s]*)(?=^\))
        nodes = []
        for matchNum, match in enumerate(matches, start=1):
            matches = match.groups()[0].split("\n")            
            for n in matches:   
                node = n.strip()                     
                if node == "":
                    continue             
                if node[0] == "#":
                    continue                
                nodes.append({                                    
                    "name": node,
                    "entry_point": "",                    
                    "path": "",
                    "parameters": []
                })        
        return {
            "cmake": path_to_cmake,
            "nodes": nodes 
        }               
    

    ########################################### Python ###########################################
 
    def extract_contents(self, node, global_scope):
        """
        Recursive helper function for parsing a variety of objects such as lists, function calls etc.
        Does not handle every case, such as nested functions etc. Returns None on failure.
        """
        if isinstance(node, ast.Str):
            return node.s
        elif isinstance(node, ast.Num):
            return node.n
        elif isinstance(node, ast.Name):
            return global_scope.get(node.id)
        elif isinstance(node, ast.List):
            return [self.extract_contents(item, global_scope) for item in node.elts]
        elif isinstance(node, ast.Tuple):
            return tuple(self.extract_contents(item, global_scope) for item in node.elts)
        elif isinstance(node, ast.Dict):
            return {self.extract_contents(key, global_scope): self.extract_contents(value, global_scope)
                    for key, value in zip(node.keys, node.values)}
        elif isinstance(node, ast.BinOp):
            return self.extract_contents(node.left, global_scope) + self.extract_contents(node.right, global_scope)
        elif isinstance(node, ast.Call):
            pos_args = tuple(self.extract_contents(arg, global_scope) for arg in node.args)
            kw_args = tuple(f"{kw.arg}={self.extract_contents(kw.value, global_scope)}" for kw in node.keywords)
            if isinstance(node.func, ast.Name):
                return f"{node.func.id}{pos_args+kw_args}"
            elif isinstance(node.func, ast.Attribute):
                return f"{node.func.attr}{pos_args+kw_args}"
        elif isinstance(node, ast.Constant):
            return node.s
        else:
            return None
    

    def extract_setup_parameters(self, tree, global_scope):
        for node in ast.walk(tree):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'setup':
                parameters = {}
                for keyword in node.keywords:
                    parameter_name = keyword.arg
                    parameter_value = self.extract_contents(keyword.value, global_scope)
                    parameters[parameter_name] = parameter_value
                return parameters
    
        return None
    

    def populate_global_scope(self, tree):
        global_scope = {}
        for node in tree.body:
            if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                target_name = node.targets[0].id
                target_value = self.extract_contents(node.value, global_scope)
                global_scope[target_name] = target_value
        return global_scope


    def parse_entry_point(self, ep):
        """
        Example of expected entrypoint format:
        analytic_dynamics = cannon_analytic.analytic_dynamics:main
        """
        try:
            node_name = ep.split('=')[0].strip()
            entry_point = ep.split('=')[1].strip()
            file_name = f"{entry_point.split(':')[0].split('.')[1]}.py"
        except Exception as e:
            self.log.error(f"Failed to parse entry point {ep}")
            return None,None,None

        return node_name, entry_point, file_name 


    def parse_setup_py(self, package_path):
        
        path_to_setup = f"{package_path}/setup.py"  

        try:
            with open(path_to_setup, 'r') as f:
                source = f.read()
        except FileNotFoundError as e:
            self.log.error(f"Failed to find {path_to_setup}")
            return {}

        tree = ast.parse(source)
        global_scope = self.populate_global_scope(tree)
        parameters = self.extract_setup_parameters(tree, global_scope)

        if not parameters:
            self.log.error("Failed to parse setup.py")
            return {}

        # possibly loop over the list of entry points if there is more than one.
        node_name, entry_point, file_name = self.parse_entry_point(parameters['entry_points']['console_scripts'][0])

        package_name = package_path.split("/")[-1]
            
        nodes = []
        nodes.append({                
            "name": node_name,
            "entry_point": entry_point,                
            "path": f"{package_path}/{package_name}/{file_name}",
            "parameters": []
        })

        return {
            "setup_py": path_to_setup,
            
            "package_name": package_name,
            "version": parameters["version"],
            "maintainer": parameters["maintainer"],
            "maintainer_email": parameters["maintainer_email"],
            "description": parameters["description"],
            "license": parameters["license"],
            "nodes": nodes
        }
    

    ########################################### Project ###########################################

    def get_file_hierarchy(self, root_dir, file_list):
        """
        Returns the file hierarchy of the given directory, and the contents of the given files.

        Args:
            root_dir: full path to the directory in question.
            file_list: list of file names which reside somewhere under root_dir, whose contents are 
                       required.

        The function returns two objects. 
        The first object is a dictionary that represents the file
        hierarchy of which root_dir is the root directory. At every level of the hierarchy, a file 
        will be represented by a key-value pair, such that the key will be the file name, and the 
        value will be the the full file path relative to root_dir. A directory will be represented 
        by a key-value pair such that the key will be the directory name, and the value will a 
        dictionary that represents the contents of the directory, recursively.
        The second object is a list of strings, representing the contents of the files whose names
        appear in file_list. If there is more than one file in the hierarchy with the same name
        (which appears in file_list), instead of file contents, the corresponding string in the
        output list will be "duplicate copies of <file name> were found", and a warning message will
        be given to the user.
        """
        hierarchy = {}
        file_contents = []

        file_count = {file_name: 0 for file_name in file_list}

        for dirpath, dirnames, filenames in os.walk(root_dir):
            dir_structure = hierarchy
            subdir_path = dirpath[len(root_dir):].split(os.sep)[1:]

            # generate empty directory structure.
            for subdir in subdir_path:
                if subdir not in dir_structure:
                    dir_structure[subdir] = {}
                dir_structure = dir_structure[subdir]

            # populate directory structure with file names/paths
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                relative_path = file_path[len(root_dir):]
                dir_structure[filename] = relative_path

                if filename in file_list:
                    file_count[filename] += 1
                    if file_count[filename] > 1:
                        self.log.warn(f"Duplicate copies of '{filename}' were found.")
                        file_contents[file_list.index(filename)] = f"Duplicate copies of '{filename}' were found."
                    else:
                        with open(file_path, 'r') as file:
                            file_contents.append(file.read())

        return hierarchy, file_contents


    def get_project_packages(self, project_path, workspace=""):                
        self.log.debug(f" + get_project_packages {project_path}/{workspace}")
        
        package_paths = glob.glob(f"{project_path}/src/*")                
        if workspace != "":
            package_paths = glob.glob(f"{project_path}/{workspace}/src/*") + package_paths            
        
        package_paths = [p for p in package_paths if 'ros2.' not in p]
        
        packages = []
        for package_path in package_paths:            
            # package_py = f"{'/'.join(package_path.split('/')[:-1])}/setup.py"
            self.log.debug(f"package_path: {package_path}")
            
            parsed_data = None     
            try:
                parsed_data = self.parse_xml(package_path)
            except Exception as e:
                print(f"{package_path} doesn't contain xml, probably not a package. skipping.")
                continue
            
            if parsed_data["build_type"] == "ament_python":                
                temp = self.parse_setup_py(package_path)
                parsed_data["nodes"] = temp["nodes"]                
                parsed_data["setup_py"] = temp["setup_py"]
                
            elif parsed_data["build_type"] == "ament_cmake":          
                temp = self.parse_makefile(package_path)
                parsed_data["nodes"] = temp["nodes"]
                parsed_data["cmake"] = temp["cmake"]                
                
            else:
                self.log.exception(f"Method {parsed_data['build_type']} not allowed")
                raise Exception(f"Method {parsed_data['build_type']} not allowed")

            node_parameters = {}
            try:
                path_to_config =  f"{package_path}/config/params.yaml"            
                with open(path_to_config, 'r') as config_file:
                    config = yaml.full_load(config_file)                    
                    
                for node_name, val in config.items():
                    par_dict = val["ros__parameters"]                    
                    node_parameters[node_name] = []
                    for key, val in par_dict.items():
                        node_parameters[node_name].append({                            
                            "name":key,
                            "parameterType": type(val).__name__, # TODO: Fix type
                            "value": val,
                            "description": "Parameter loaded from config.yaml",                            
                        })
                for node in parsed_data["nodes"]:
                    # print(f"adding parameters to [{node['name']}] node")                
                    node["parameters"] = node_parameters.get(node["name"], [])                    
            except Exception as e:
                self.log.exception(e)

            packages.append({
                # "id": uuid.uuid4(),                
                "name": parsed_data["package_name"],
                "cover": "",
                "path": package_path,
                "setup_py": parsed_data.get("setup_py", ""),
                "package_xml": parsed_data.get("package_xml"),
                "maintainer": parsed_data.get("maintainer"),
                "maintainer_email" : parsed_data.get("maintainer_email"),
                "description": parsed_data.get("description"),
                "license": parsed_data.get("license"),

                "readme": f"{package_path}/README.md",
                "git": "", #TODO
                
                "launches": self.get_project_launch_files(package_path),
                "nodes": parsed_data.get("nodes"),                
            })
        return packages


    def get_project_launch_files(self, package_path, workspace=""):
        #TODO: check if done. 
        launch_paths = glob.glob(f"{package_path}/launch/*.py")
        if workspace != "":
            launch_paths + glob.glob(f"{package_path}/{workspace}/src/*.py")
        
        launch_paths = [p for p in launch_paths if 'ros2.' not in p]
        
        launch_files = []
        for launch_path in launch_paths:
            launch_files.append({                
                "name": launch_path.split("/")[-1],
                "path": launch_path,

                # "tags": [],
                "description": "",                
            })
        return launch_files


    def get_git_remote_url(self, project_path):
        """
        Assumption: The user is using github as the remote backup, and the name of the remote is 'origin'.
        """
        try:
            command = 'echo $REMOTE_CONTAINERS'
            result = subprocess.check_output(command, shell=True, executable='/bin/bash').decode().strip()
            if result == "true":
                self.log.info("Inside devcontainer. Cannot communicate with github.")
                return ""

            os.chdir(project_path)
            result = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True).stdout.strip()
        except Exception as e:
            self.log.exception(e)
            return ""
        
        # sanity check
        if result.startswith("git@github.com:") and result.endswith(".git"):
            return result
        else:
            self.log.error("Could not obtain git remote url for path " + project_path)
            return ""
        

    def get_git_local_hash(self, project_path):
        os.chdir(project_path)
        result = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True)
        result = result.stdout.strip()

        # sanity check
        if len(result) == 40:
            return result
        else:
            self.log.error("Could not obtain git hash for local path " + project_path)
            return None
    

    def get_project_description(self, project_path):
        #TODO
        return ""


    def get_file_content(self, path):
        try:
            with open(path, 'r') as f:
                content = f.read()
            return content
        except FileNotFoundError as e:
            self.log.error(f"could not find file {path}")
            return ""        
    

    def parse(self, project_path, project_name, workspaces=["", "ros_ws"]):       
        packages = []
        launches = []

        # remove duplicates
        workspaces = list(set(workspaces))

        # remove non-existing workspaces
        workspaces = [ws for ws in workspaces if os.path.isdir(f"./{ws}")]
        
        for w in workspaces:
            packages = packages + self.get_project_packages(project_path, workspace=w)
            launches = launches + self.get_project_launch_files(project_path, workspace=w)
                        
        if not self.project:
            self.project = {                          
                "cover": "",
                "name": project_name,
                "image": project_name,
                "tags": [],
                "is_active": True,
                "description": "",                 
                "git": self.get_git_remote_url(project_path), 
                "path": project_path,    
                                
                "packages": None,                
                "launches": None,

                "readme": None,
                "license":None
            }
        
        self.project["description"] = self.get_project_description(project_path)
        self.project["packages"] = packages
        self.project["launches"] = launches
        self.project["readme"] = self.get_file_content(f"{project_path}/README.md")
        self.project["license"] = self.get_file_content(f"{project_path}/LICENSE")
        
        return self.project


