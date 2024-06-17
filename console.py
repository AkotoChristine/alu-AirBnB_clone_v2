#!/usr/bin/python3
"""This module contains the entry point of the command interpreter"""

import cmd
import models


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb) "

    def do_quit(self, arg):
        """
        Quit the console.

        Usage:
            quit
            q
            exit
        """
        return True

    do_q = do_quit
    do_exit = do_quit

    def do_EOF(self, arg):
        """
        Quit the console.

        Usage:
            EOF
        """
        return True

    def emptyline(self):
        """
        An empty line + ENTER shouldn't execute anything
        """
        pass

    def do_create(self, arg):
        """
        Creates a new inst of BaseModel, saves it, and prints the id.

        Usage: create <class_name>

        Args:
            arg (str): The argument should contain the <class_name>.
        """

        class_name = arg.split(" ")[0]

        if not class_name:
            print("** class name missing **")
        elif class_name not in models.classes:
            print("** class doesn't exist **")
        else:
            instance = models.classes[class_name]()
            instance.save()
            print(instance.id)

    def do_show(self, arg):
        """
        Displays the string representation of an instance.

        Usage: create <class_name> <instance_id>

        Args:
            arg (str): Argument should contain <class_name> <instance_id>.
        """

        split_args = arg.split(" ")
        class_name = split_args[0] if len(split_args) > 0 else None
        obj_id = split_args[1] if len(split_args) > 1 else None

        if not class_name:
            print("** class name missing **")
        elif class_name not in models.classes:
            print("** class doesn't exist **")
        elif not obj_id:
            print("** instance id missing **")
        else:
            key = f"{class_name}.{obj_id}"
            if key in models.loaded_objects:
                print(models.loaded_objects[key])
            else:
                print("** no instance found **")

    def do_destroy(self, arg):
        """
        Deletes an instance based on the class name and id.

        Usage: destroy <class_name> <instance_id>

        Args:
            arg (str): Argument should contain <class_name> <instance_id>.
        """

        split_args = arg.split(" ")
        class_name = split_args[0] if len(split_args) > 0 else None
        obj_id = split_args[1] if len(split_args) > 1 else None

        if not class_name:
            print("** class name missing **")
        elif class_name not in models.classes:
            print("** class doesn't exist **")
        elif not obj_id:
            print("** instance id missing **")
        else:
            key = f"{class_name}.{obj_id}"
            if key in models.loaded_objects:
                del models.loaded_objects[key]
                models.storage.save()
            else:
                print("** no instance found **")

    do_delete = do_destroy

    def do_all(self, arg):
        """
        Prints all string representation of all instances.

        Usage:
            all
            all <class_name>

        Args:
            arg (str): The argument should contain <class_name>.
        """

        split_args = arg.split(" ")
        class_name = split_args[0] if len(split_args) > 0 else None

        if not class_name:
            print([str(obj) for obj in models.loaded_objects.values()])
        elif class_name not in models.classes:
            print("** class doesn't exist **")
        else:
            print([str(obj) for obj in models.loaded_objects.values()
                   if type(obj) == models.classes[class_name]])

    def remove_quotes(self, arg):
        """
        Removes the quotes from the argument.
        """
        rules = {"\"": "", "\'": ""}
        for key, value in rules.items():
            arg = arg.replace(key, value)
        return arg

    def do_update(self, arg):
        """
        Updates an instance based on the class name and id.

        Usage: update <class_name> <instance_id> <attr_name> "<attr_value>"

        Args:
            arg (str): <class_name> <instance_id> <attr_name> <attr_value>.
        """

        split_args = arg.split(" ")
        class_name = split_args[0] if len(split_args) > 0 else None
        obj_id = split_args[1] if len(split_args) > 1 else None
        attr_name = split_args[2] if len(split_args) > 2 else None
        attr_value = split_args[3] if len(split_args) > 3 else None

        if not class_name:
            print("** class name missing **")
        elif class_name not in models.classes:
            print("** class doesn't exist **")
        elif not obj_id:
            print("** instance id missing **")
        elif not attr_name:
            print("** attribute name missing **")
        elif not attr_value:
            print("** value missing **")
        else:
            key = f"{class_name}.{obj_id}"
            forbidden_attrs = ['id', 'created_at', 'updated_at']
            if key in models.loaded_objects:
                if attr_name not in forbidden_attrs:
                    setattr(models.loaded_objects[key], attr_name,
                            self.remove_quotes(attr_value))
                    models.storage.save()
                else:
                    print(f"** Can't update the {attr_name} attribute **")
            else:
                print("** no instance found **")

if __name__ == '__main__':
    HBNBCommand().cmdloop()
