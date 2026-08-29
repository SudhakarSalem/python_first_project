# Python code​​​​​‌​​​​​​​‌​​‌‌‌‌‌​​​‌‌‌‌‌‌​ below
class NonIntArgumentException(Exception):
    pass

    def handleNonIntArguments(func):
        def wrapper(*args):
            for item in args:
                if type(item) is not int:
                    raise NonIntArgumentException()
            return func(*args)

        return wrapper


