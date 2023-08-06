# все классы ошибок, которые используются в коде

class ConfigInitError(Exception):
    def __str__(self) -> str:
        return 'You should use init_config() before other functions!'

class WrongPathError(Exception):
    def __str__(self) -> str:
        return 'You have specified the wrong file path.'