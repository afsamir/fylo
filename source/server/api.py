from server import Server
from utils import logger

server = Server()


class API:
    @logger
    def handshake(username, timestamp):
        return "{0}{1}".format(username, timestamp)

    @logger
    def login(username, timestamp):
        return server.login(username, timestamp)

    def make_directory(current_dir, new_dir, token):
        return server.make_directory(current_dir, new_dir, token)

    def list_directory(dir, token):
        return server.list_directory(dir, token)

    def is_directory_valid(dir, sub_dir, token):
        return server.is_directory_valid(dir, sub_dir, token)
