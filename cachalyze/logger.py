from cachalyze.config import Config


class Logger:
    @staticmethod
    def info(message):
        if Config.VERBOSE:
            print(f'Info:\t\t\t{message}')

    @staticmethod
    def warning(message):
        print(f'Warning:\t\t{message}')

    @staticmethod
    def error(message):
        print(f'Error:\t\t\t{message}')
        exit()
