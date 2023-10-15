#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
from models import storage
import re
from shlex import split
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.state import State
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(line):
    c_braces = re.search(r"\{(.*?)\}", line)
    sq_bracket = re.search(r"\[(.*?)\]", line)
    if c_braces is None:
        if sq_bracket is None:
            return [i.strip(",") for i in split(line)]
        else:
            l = split(line[:sq_bracket.span()[0]])
            rl = [i.strip(",") for i in l]
            rl.append(sq_bracket.group())
            return rl
    else:
        l = split(line[:c_braces.span()[0]])
        rl = [i.strip(",") for i in l]
        rl.append(c_braces.group())
        return rl

class HBNBCommand(cmd.Cmd):
    """it represents HBNBCommand interpreter class"""
    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
        }
    def emptyline(self):
        """If it's an empty line, do nothing"""
        pass

    def default(self, line):
        """Default impementation of cmd module if input is invalid"""
        linedict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
            }
        match = re.search(r"\((.*?)\)", argl[1])
        if match is not None:
            command = [argl[1][:match.span()[0]], match.group()[1:-1]]
            if command[0] in linedict.keys():
                c = "{} {}".format(argl[0], command[1])
                return linedict[command[0]](c)
        print("***Unknown syntax: {}".format(line))
        return False

    def do_quit(self, line):
        """exits the program"""
        return True
    
    def do_EOF(self, line):
        """exits the program"""
        print("")
        return True
    def do_create(self, line):
        """Creates new class instance and prints the id.
        Usage: create <class>
        """
        linel = parse(line)

        if len(linel) == 0:
            print("** class name missing **")
        elif linel[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(linel[0])().id)
            storage.save()

    def do_show(self, line):
        """displays string representation of a class instance of an id.
        Usage: show <class> <id> or <class>.show(<id>)
        """
        linel = parse(line)
        obj_dict = storage.all()
        if len(linel) == 0:
            print("** class name missing **")
        elif linel[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(linel) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(linel[0], linel[1]) not in obj_dict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(line[0], linel[1])])

    def do_destroy(self, line):
        """Deletes a class instance of an id.
        Usage: destroy <class> <id> or <class>.destroy(<id>)
        """
        linel = parse(line)
        obj_dict = storage.all()
        if len(linel) == 0:
            print("** class name missing **")
        elif linel[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(linel) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(linel[0], linel[1]) not in obj_dict.keys():
            print("** no instance found **")
        else:
            del obj_dict["{}.{}".format(linel[0], linel[1])]
            storage.save()

    def do_all(self, line):
        """Displays string representation of all instances of a class
        Usage: all or all <class> or <class>.all()
        """
        linel = parse(line)

        if len(linel) > 0 and linel[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            obj_l = []
            for obj in storage.all().values():
                if len(linel) > 0 and linel[0] == obj.__class__.__name__:
                    obj_l.append(obj.__str__())
                elif len(linel) == 0:
                    obj_l.append(obj.__str__())
            print(obj_l)

    def do_count(self, line):
        """It retrieves number of instances of a class.
        Usage: count <class> or <class>.count()
        """
        linel = parse(line)
        count = 0

        for o in storage.all().values():
            if linel[0] == o.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, line):
        """Updates a class instance of an id by adding or updating
        Usage: update <class> <id> <attribute_name> <attribute_value>or <class>.update(<id>, <dictionary>) or <class>.update(<id>, <attribute_name>, <attribute_value>)"""
        linel = parse(line)
        obj_dict = storage.all()

        if len(linel) == 0:
            print("** class name missing **")
            return False
        if linel[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(linel) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(linel[0], linel[1]) not in obj_dict.keys():
            print("** no instance found **")
            return False
        if len(linel) == 2:
            print("** attribute name missing **")
            return False
        if len(linel) == 3:
            try:
                type(eval(linel[2])) != dict
            except NameError:
                print("** value missing **")
                return False
        if len(linel) == 4:
            o = obj_dict["{}.{}".format(linel[0], linel[1])]
            if line[2] in o.__class__.__dict__.keys():
                valtype = type(o.__class__.__dict__[linel[2]])
                o.__dict__[linel[2]] = valtype(linel[3])
            else:
                o.__dict__[linel[2]] = linel[3]
        elif type(eval(linel[2])) == dict:
            o = obj_dict["{}.{}".format(linel[0], linel[1])]
            for k, v in eval(linel[2]).items():
                if (k in o.__class__.__dict__.keys() and type(o.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(o.__class__.__dict__[k])
                    o.__dict__[k] = valtype(v)
                else:
                    o.__dict__[k] = v
        storage.save()
                
            

if __name__ == "__main__":
    HBNBCommand().cmdloop()
    
