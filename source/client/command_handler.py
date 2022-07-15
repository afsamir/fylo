from datetime import datetime
import sys, os, tempfile, platform
from getpass import getpass
from subprocess import call, Popen
from session import Session
from display import Display

sys.path.append("../server")
from api import API
from exceptions import AlreadyExistsException


class CommandHandler:
    def __init__(self, session: Session):
        self.session = session
        self.current_dir = "/"
        self.commands_map = {
            "mkdir": self.make_directory,
            "touch": self.make_file,
            "ls": self.list_directory,
            "cd": self.change_directory,
            "mv": self.move_file,
            "rm": self.remove_file,
            "edit": self.edit_file,
        }

    def run(self):
        Display.welcome()
        while True:
            while self.session.username is not None:
                command = input(
                    Display.command_header(self.session.username, self.current_dir)
                )
                self.process_command(command.split())
            self.login_prompt()

    def login_prompt(self):
        username = input("Username:")
        password = getpass("Password:")
        try:
            self.session.login(username, password)
            Display.logged_in(username)
        except Exception:
            Display.login_failed()

    @Session.check_access
    def process_command(self, command_tokens):
        if len(command_tokens) == 0:
            return
        func = self.commands_map.get(command_tokens[0])
        if func is not None:
            func(command_tokens[1:])
        else:
            print("'{}': command not found".format(command_tokens[0]))

    # command functions

    def move_file(self, args):
        pass

    def remove_file(self, args):
        pass

    def change_directory(self, args):
        if len(args) < 1:
            print("cd: needs more arguments")
            return
        new_dir = args[0]
        if API.is_directory_valid(self.current_dir, new_dir, self.session.session_key):
            self.current_dir = os.path.normpath(os.path.join(self.current_dir, new_dir))
        else:
            print("{0}: no such directory".format(new_dir))

    def make_file(self, args):
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
            self.open_editor(tf.name)

    def list_directory(self, args):
        dir = self.current_dir
        files = API.list_directory(dir, self.session.session_key)
        Display.print_ls(files)

    def make_directory(self, args):
        if len(args) < 1:
            print(f"mkdir: needs more arguments")
            return
        for new_dir in args:
            try:
                API.make_directory(self.current_dir, new_dir, self.session.session_key)
            except AlreadyExistsException:
                print("{}: already exists.".format(new_dir))

    def edit_file(self, args):
        with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
            self.open_editor(tf.name)

    def open_editor(self, filepath):
        if platform.system() == "Darwin":
            call(("open", filepath))
        elif platform.system() == "Windows":
            os.startfile(filepath)
        else:
            call(("editor", filepath))
