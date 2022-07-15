from colorama import Fore
from colorama import Style


class Display:
    @staticmethod
    def print_ls(files):
        names = list(map(lambda x: x[1].split("/")[-1], files))
        print(f"{Style.BRIGHT}{Fore.BLUE}" + "\t".join(names))

    @staticmethod
    def command_header(username, current_dir):
        return f"{Style.BRIGHT}{Fore.GREEN}{username}@fylo{Fore.WHITE}:{Fore.BLUE}{current_dir}{Style.NORMAL}{Fore.RESET}$ "

    @staticmethod
    def welcome():
        print(f"{Fore.YELLOW}Fylo v1.6{Fore.RESET}")

    @staticmethod
    def logged_in(username):
        print(
            f"{Fore.GREEN}Logged in as {Fore.BLUE}{username}{Fore.GREEN}.{Fore.RESET}"
        )

    @staticmethod
    def login_failed():
        print(f"{Fore.RED}Login failed. Try again.{Fore.RESET}")

    @staticmethod
    def session_expired():
        print(f"{Fore.RED}Session expired.{Fore.RESET}")
