"""Class for the command interpreter."""

prompt = "(hbnb) "

def default(self, line):
    """Catch commands if nothing else matches then."""
    self._precmd(line)

def _precmd(self, line):
    """Intercepts commands to test for class.syntax()"""
    match = re.search(r"^(\w*)\.(\w+)(?:\(([^)]*)\))$", line)
    if not match:
        return line
    classname = match.group(1)
    method = match.group(2)
    args = match.group(3)
    match_uid_and_args = re.search('^"([^"]*)"(?:, (.*))?$', args)
    if match_uid_and_args:
        uid = match_uid_and_args.group(1)
        attr_or_dict = match_uid_and_args.group(2)
    else:
        uid = args
        attr_or_dict = False

    attr_and_value = ""
    if method == "update" and attr_or_dict:
        match_dict = re.search('^({.*})$', attr_or_dict)
        if match_dict:
            self.update_dict(classname, uid, match_dict.group(1))
            return ""
        match_attr_and_value = re.search(
            '^(?:"([^"]*)")?(?:, (.*))?$', attr_or_dict)
        if match_attr_and_value:
            attr_and_value = (match_attr_and_value.group(
                1) or "") + " " + (match_attr_and_value.group(2) or "")
    command = method + " " + classname + " " + uid + " " + attr_and_value
    self.onecmd(command)
    return command

def update_dict(self, classname, uid, s_dict):
    """Helper method for update() with a dictionary."""
    s = s_dict.replace("'", '"')
    d = json.loads(s)
    if not classname:
        print("** class name missing **")
    elif classname not in storage.classes():
        print("** class doesn't exist **")
    elif uid is None:
        print("** instance id missing **")
    else:
        key = "{}.{}".format(classname, uid)
        if key not in storage.all():
            print("** no instance found **")
        else:
            attributes = storage.attributes()[classname]
            for attribute, value in d.items():
                if attribute in attributes:
                    value = attributes[attribute](value)
                setattr(storage.all()[key], attribute, value)
            storage.all()[key].save()

def do_EOF(self, line):
    """Handles End Of File character.
    """
    print()
    return True

def do_quit(self, line):
    """Exits the program.
    """
    return True

def emptyline(self):
    """Doesn't do anything on ENTER.
    """
    pass

def do_create(self, arg):
    """Creates a new instance of the class and saves it"""
    if not arg:
        print("** class name missing **")
        return
    try:
        new_instance = eval(arg)()
        new_instance.save()
        print(new_instance.id)
    except:
        print("** class doesn't exist **")

def do_show(self, arg):
    """Prints the string representation of an instance"""
    if not arg:
        print("** class name missing **")
        return
    args = arg.split()
    if len(args) < 2:
        print("** instance id missing **")
        return
    try:
        new_instance = storage

