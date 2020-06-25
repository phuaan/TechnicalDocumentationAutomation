import re

bannedKeywords = ["(void)", "(instancetype)", "(nonnull instancetype)", "(nullable instancetype)"]


def regex_substitute(input_string, pattern, new_string=""):
    return re.sub(pattern, new_string, input_string)


def remove_comments(input_string):
    temp_input = "" + input_string
    return regex_substitute(input_string=temp_input, pattern="//.*")


def cleanup_objc_import(input_string):
    temp_input = "" + remove_comments(input_string)
    temp_input = re.findall("\".*\"", temp_input)
    output = temp_input[0]
    output = output.replace("\"", "")
    output = output.replace(".h", "")
    return output


def cleanup_objc_method_class_diag(input_string, modifier):
    temp_input = "" + remove_comments(input_string)
    temp_input = temp_input.replace(" {", "")
    temp_input = temp_input.replace("\n", "")
    string_no_nsswiftname = regex_substitute(input_string=temp_input, pattern="NS_SWIFT_NAME.*;")
    string_no_nsswiftname = regex_substitute(input_string=string_no_nsswiftname, pattern="^. ")
    string_no_return_type = regex_substitute(input_string=string_no_nsswiftname, pattern=r"^\([^\(\)]+\)")
    string_no_parameters = regex_substitute(input_string=string_no_return_type, pattern=r"(\([^:]*)*\([^\(\)]*\)(\))*")

    if ":" in string_no_parameters:
        string_no_parameters = regex_substitute(input_string=string_no_parameters, pattern="([a-zA-Z]+ )|([a-zA-Z]*;)")

    string_with_fixed_return_type = string_no_parameters.replace(" ;", ";").replace(";", ": ").replace(" ", "")
    string_with_fixed_return_type = regex_substitute(input_string=string_with_fixed_return_type, pattern=":[^:]+$",
                                                     new_string=":")
    return_type = re.findall(r'^\([^()]+\)', string_no_nsswiftname)
    return_string = ""

    if len(return_type) > 0:
        return_string = return_type[0]

    output = modifier + " " + string_with_fixed_return_type + clean_up_return_type(return_string)
    return output


def cleanup_objc_method_docum(input_string, modifier):
    temp_input = "" + remove_comments(input_string)
    temp_input = temp_input.replace(" {", ";")
    temp_input = temp_input.replace("\n", "")
    string_no_nsswiftname = regex_substitute(input_string=temp_input, pattern="NS_SWIFT_NAME.*;")
    string_no_nsswiftname = regex_substitute(input_string=string_no_nsswiftname, pattern="^. ")
    # string_no_return_type = regex_substitute(input_string=string_no_nsswiftname, pattern=r"^\([^\(\)]+\)")
    string_no_parameters = regex_substitute(input_string=string_no_nsswiftname, pattern=r"(\([^:]*)*\([^\(\)]*\)(\))*")

    if ":" in string_no_parameters:
        string_no_parameters = regex_substitute(input_string=string_no_parameters, pattern="([a-zA-Z]+ )|([a-zA-Z]*;)")

    string_with_fixed_return_type = string_no_parameters.replace(" ;", ";").replace(";", ": ").replace(" ", "")
    string_with_fixed_return_type = regex_substitute(input_string=string_with_fixed_return_type, pattern=":[^:]+$", new_string=":")
    return_type = re.findall(r'^\([^()]+\)', string_no_nsswiftname)
    return_string = ""

    if len(return_type) > 0:
        return_string = return_type[0]

    output = modifier + " " + return_string + string_with_fixed_return_type
    return output


def get_return_value(input_string):
    temp_input = "" + remove_comments(input_string)
    temp_input = regex_substitute(input_string=temp_input, pattern="^. ")
    return_type = re.findall(r'^\([^()]+\)', temp_input)
    return_string = ""

    if len(return_type) > 0:
        return_string = return_type[0]

    output = clean_up_return_type(return_string)
    output = output.replace("(): ", "")
    output = output.replace("()", "")
    return output


def get_objc_method_param(input_string):
    temp_input = "" + remove_comments(input_string)
    temp_input = temp_input.replace(" {", "")
    temp_input = temp_input.replace("{", "")
    temp_input = temp_input.replace("\n", "")
    temp_input = temp_input.replace(";", "")
    string_no_nsswiftname = regex_substitute(input_string=temp_input, pattern="NS_SWIFT_NAME.*;")
    string_no_nsswiftname = regex_substitute(input_string=string_no_nsswiftname, pattern="^. ")
    string_no_return_type = regex_substitute(input_string=string_no_nsswiftname, pattern=r"^\([^\(\)]+\)")
    string_no_parameters = regex_substitute(input_string=string_no_return_type, pattern=r"(\([^:]*)*\([^\(\)]*\)(\))*")

    if ":" in string_no_parameters:
        string_no_parameters = regex_substitute(input_string=string_no_parameters, pattern="[a-zA-Z]*:")
    else:
        string_no_parameters = regex_substitute(input_string=string_no_parameters, pattern="^[^:]+$")

    string_no_parameters = regex_substitute(input_string=string_no_parameters, pattern="^ ")

    output = string_no_parameters.split(sep=" ")

    if len(output) == 1:
        if output[0] == '':
            return []

    return output


def cleanup_objc_property(input_string, modifier):
    temp_input = "" + remove_comments(input_string)
    temp_input = temp_input.replace("@property ", "")
    temp_input = temp_input.replace("\n", "")
    temp_input = regex_substitute(input_string=temp_input, pattern=r"\(.*\) ")
    names = re.findall(r' [^>\n]*;', temp_input)
    name = "" + names[0]
    name = name.replace(" ", "")
    name = name.replace(";", "")
    name = name.replace("*", "")
    data_type = regex_substitute(input_string=temp_input, pattern=r'\ [^>\n]*;')
    output = modifier + " " + name + ": " + data_type
    return output


def clean_up_return_type(input_string):
    if input_string in bannedKeywords:
        input_string = "()"
    else:
        input_string = input_string.replace("(", "").replace(")", "").replace(" *", "")
        input_string = "(): " + input_string
    return input_string


def get_line_type(input_string):
    # check if comments
    comment = re.search("^//", input_string)
    variable = re.search("^@property", input_string)
    method = re.search(r"^([+-])", input_string)
    imprt = re.search("^#import \"", input_string)
    if comment:
        return "comment"
    if variable:
        return "property"
    if method:
        return "method"
    if imprt:
        return "import"
