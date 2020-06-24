from ObjectiveCHelper import *
import fnmatch
import os


class ClassDiagramContainer:
    def __init__(self, name):
        self.name = name
        self.mLocation = ""
        self.hLocation = ""
        self.name = ""
        self.private_properties = []
        self.private_methods = []
        self.private_method_attributes = {}
        self.public_properties = []
        self.public_methods = []
        self.public_method_attributes = {}
        self.imports = []


class ObjectiveC:
    def __init__(self, basedir):
        # .h files
        self.h_files = {}
        # .m files
        self.m_files = {}
        # filenames no extensions
        self.file_names = {}
        # base directory
        self.basedir = basedir

    def prepare(self, operation_type):
        self.h_files = {}
        self.m_files = {}
        self.file_names = {}
        self.scan_files()
        self.prepare_output_directory()
        for file in self.file_names:
            if self.h_files.get(file):
                self.file_names.get(file).hLocation = self.h_files[file]
            if self.m_files.get(file):
                self.file_names.get(file).mLocation = self.m_files[file]
        for file in self.file_names:
            if self.file_names.get(file).hLocation != "":
                f = open(self.file_names.get(file).hLocation, "r")
                for line in f:
                    get_line_type(line)
                    if get_line_type(line) == "method":
                        if operation_type == "class diagram":
                            self.file_names.get(file).public_methods.append(cleanup_objc_method_class_diag(line, "+"))
                        elif operation_type == "documentation":
                            temp_key = cleanup_objc_method_docum(line, "+")
                            self.file_names.get(file).public_methods.append(temp_key)
                            self.file_names.get(file).public_method_attributes[temp_key] = get_objc_method_param(line)
                    elif get_line_type(line) == "property":
                        if operation_type == "class diagram":
                            self.file_names.get(file).public_properties.append(cleanup_objc_property(line, "+"))
                        elif operation_type == "documentation":
                            self.file_names.get(file).public_properties.append(line)
                    elif get_line_type(line) == "import":
                        if operation_type == "class diagram":
                            self.file_names.get(file).imports.append(cleanup_objc_import(line))

                f.close()
            if self.file_names.get(file).mLocation != "":
                f = open(self.file_names.get(file).mLocation, "r")
                for line in f:
                    get_line_type(line)
                    if get_line_type(line) == "method":
                        if operation_type == "class diagram":
                            self.file_names.get(file).private_methods.append(cleanup_objc_method_class_diag(line, "-"))
                        elif operation_type == "documentation":
                            temp_key = cleanup_objc_method_docum(line, "-")
                            self.file_names.get(file).private_methods.append(temp_key)
                            self.file_names.get(file).private_method_attributes[temp_key] = get_objc_method_param(line)
                    elif get_line_type(line) == "property":
                        if operation_type == "class diagram":
                            self.file_names.get(file).private_properties.append(cleanup_objc_property(line, "-"))
                        elif operation_type == "documentation":
                            self.file_names.get(file).public_properties.append(line)
                    elif get_line_type(line) == "import":
                        if operation_type == "class diagram":
                            self.file_names.get(file).imports.append(cleanup_objc_import(line))

                f.close()
            try:
                self.file_names.get(file).imports.remove(file)
            except ValueError:
                pass

    def add_file_name(self, name):
        temp_input = "" + name
        temp_file_name = (temp_input.split(sep="."))
        # file_names.add(file_name[0])
        self.file_names[temp_file_name[0]] = ClassDiagramContainer(temp_file_name[0])
        return temp_file_name[0]

    def scan_files(self):
        for dirpath, dirnames, files in os.walk(self.basedir):
            for file_name in files:
                if fnmatch.fnmatch(file_name, '*.h'):
                    temp_file_name = self.add_file_name(name=file_name)
                    self.h_files[temp_file_name] = dirpath + "/" + file_name
                elif fnmatch.fnmatch(file_name, '*.m'):
                    temp_file_name = self.add_file_name(name=file_name)
                    self.m_files[temp_file_name] = dirpath + "/" + file_name

    def prepare_output_directory(self):
        if not os.path.exists(self.basedir + "/output"):
            os.mkdir(self.basedir + "/output")
            print("Directory ", self.basedir + "/output", " Created ")
        else:
            print("Directory ", self.basedir + "/output", " already exists")

    def generate_class_diagram_image(self):
        os.system("java -jar plantuml.jar \"" + self.basedir + "\"/output")
        os.system("open \"" + self.basedir + "\"/output")

    def generate_class_diagram(self):
        self.prepare(operation_type="class diagram")
        class_diagram = open(self.basedir + "/output/classDiagram.txt", "w+")
        class_diagram.write("@startuml\n")
        class_diagram.write("skinparam classAttributeIconSize 0\n")

        for file in self.file_names:
            class_diagram.write("\n")
            for relationship in self.file_names.get(file).imports:
                class_diagram.write("\"" + file + "\"" + " <|-- \"" + relationship + "\"\n")
            class_diagram.write("\n")

        for file in self.file_names:
            class_diagram.write("\n\n")
            class_diagram.write("class \"" + file + "\"{\n")
            for private_properties in self.file_names.get(file).private_properties:
                class_diagram.write("\t{field} " + private_properties + "\n")
            for public_properties in self.file_names.get(file).public_properties:
                class_diagram.write("\t{field} " + public_properties + "\n")
            class_diagram.write("===\n")
            for private_methods in self.file_names.get(file).private_methods:
                class_diagram.write("\t{method} " + private_methods + "\n")
            for public_methods in self.file_names.get(file).public_methods:
                class_diagram.write("\t{method} " + public_methods + "\n")
            class_diagram.write("}\n")

        class_diagram.write("@enduml")
        class_diagram.close()
        self.generate_class_diagram_image()

    def generate_documentation(self):
        self.prepare(operation_type="documentation")
        technical_documentation = open(self.basedir + "/output/TechnicalDocumentation.md", "w+")
        technical_documentation.write("## Getting Started" + "\n\n")
        technical_documentation.write("[todo] add simple description" + "\n\n")

        technical_documentation.write("## Dependencies" + "\n\n")
        technical_documentation.write("| Dependency | Version | Description |" + "\n")
        technical_documentation.write("| ---------- | ------- | ----------- |" + "\n")
        technical_documentation.write("| [todo] | [todo] | [todo] |" + "\n\n")

        technical_documentation.write("## UML Class Diagram" + "\n")
        technical_documentation.write("![todo]()" + "\n")
        technical_documentation.write("## Sequence Diagram" + "\n")
        technical_documentation.write("![todo]()" + "\n")
        technical_documentation.write("## API Reference" + "\n")
        technical_documentation.write("### Classes [todo] sort class into public and private" + "\n")

        for file in self.file_names:
            technical_documentation.write("### " + file + "\n")

            technical_documentation.write("#### Public Methods" + "\n")
            for public_methods in self.file_names.get(file).public_methods:
                technical_documentation.write("##### " + public_methods + "\n\n")
                technical_documentation.write("```objective-c" + "\n\n")
                technical_documentation.write("" + "\n\n")
                technical_documentation.write("```" + "\n\n")
                technical_documentation.write("[todo] method description" + "\n")
                technical_documentation.write("###### Parameters" + "\n")
                temp_list = self.file_names.get(file).public_method_attributes.get(public_methods)
                if isinstance(temp_list, list):
                    if len(temp_list) > 0:
                        technical_documentation.write("| Parameter | Description |" + "\n")
                        technical_documentation.write("| ---------- | ------- |" + "\n")
                        for attributes in temp_list:
                            technical_documentation.write("| " + attributes + " | [todo] add desc |" + "\n")
                        technical_documentation.write("\n")
                    else:
                        technical_documentation.write("This method does not have parameters" + "\n")
                technical_documentation.write("###### Returns" + "\n")
                temp_return = get_return_value(public_methods)
                if temp_return == "":
                    technical_documentation.write("This method does not have return values." + "\n\n")
                else:
                    technical_documentation.write("This method returns" + temp_return + "[todo] add desc" + "\n\n")

            technical_documentation.write("#### Private Methods" + "\n")
            for private_methods in self.file_names.get(file).private_methods:
                technical_documentation.write("##### " + private_methods + "\n")
                technical_documentation.write("```objective-c" + "\n")
                technical_documentation.write("" + "\n")
                technical_documentation.write("```" + "\n")
                technical_documentation.write("[todo] method description" + "\n")
                technical_documentation.write("###### Parameters" + "\n")
                temp_list = self.file_names.get(file).private_method_attributes.get(private_methods)
                if isinstance(temp_list, list):
                    if len(temp_list) > 0:
                        technical_documentation.write("| Parameter | Description |" + "\n")
                        technical_documentation.write("| ---------- | ------- |" + "\n")
                        for attributes in temp_list:
                            technical_documentation.write("| " + attributes + " | [todo] add desc |" + "\n")
                        technical_documentation.write("\n")
                    else:
                        technical_documentation.write("This method does not have parameters" + "\n")
                technical_documentation.write("###### Returns" + "\n")
                temp_return = get_return_value(private_methods)
                if temp_return == "":
                    technical_documentation.write("This method does not have return values." + "\n\n")
                else:
                    technical_documentation.write("This method returns" + temp_return + "[todo] add desc" + "\n\n")

            technical_documentation.write("#### Class Params" + "\n")
            for private_properties in self.file_names.get(file).private_properties:
                technical_documentation.write("##### " + private_properties + "\n")
                technical_documentation.write("```objective-c" + "\n\n")
                technical_documentation.write("\t" + private_properties + "\n")
                technical_documentation.write("```" + "\n\n")
                technical_documentation.write("[todo] property desc" + "\n")
            for public_properties in self.file_names.get(file).public_properties:
                technical_documentation.write("##### " + public_properties + "\n\n")
                technical_documentation.write("```objective-c" + "\n\n")
                technical_documentation.write("\t" + public_properties + "\n")
                technical_documentation.write("```" + "\n\n")
                technical_documentation.write("[todo] property desc" + "\n")
        technical_documentation.close()
        os.system("open \"" + self.basedir + "\"/output")

