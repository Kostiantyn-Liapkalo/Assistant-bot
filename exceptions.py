from Classes import LetterInPhoneError, WrongLengthPhoneError

# Exception decorator
def input_error(func):

    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except KeyError:
            return "This record is not exist"
        except ValueError:
            return "This record is not correct!"
        except IndexError:
            return "This command is wrong"
        except LetterInPhoneError:
            return "There is letter in phone number!"
        except WrongLengthPhoneError:
            return "Length of phone's number is wrong!"
    return wrapper
