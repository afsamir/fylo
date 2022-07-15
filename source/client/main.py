from command_handler import CommandHandler
from session import Session

session = Session()
commands = CommandHandler(session)

commands.run()