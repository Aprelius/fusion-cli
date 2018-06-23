def SetupInstallCommand(commands):
    command = commands.add_parser('install', help='Install the project.')
    return command


def RunInstall(args):
    return False