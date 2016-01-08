import os


class Console:
    @staticmethod
    def cls():
        os.system('cls' if os.name == 'nt' else 'clear')
