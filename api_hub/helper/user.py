import json
import string

class UsernameCharError(ValueError):
    @staticmethod
    def getMessage():
        return "Username does not contain valid characters"
class UsernameFirstError(ValueError):
    @staticmethod
    def getMessage():
        return "Username first character is not valid"
class UsernameLetterError(ValueError):
    @staticmethod
    def getMessage():
        return "Username does not contain any letters"
class UsernameLengthError(ValueError):
    @staticmethod
    def getMessage():
        return "Username length invalid"

class IncorrectPasswordError(ValueError):
    @staticmethod
    def getMessage():
        return "Incorrect Password"

class User:
    def __init__(self, userData):
        '''

        :param userData (dict): Dictionary of user data.
        Format:
        {
        'username': str,
        'email': str,
        'password': str,
        }
        '''
        self.playerData = userData

    # Check characters are allowed [a-zA-Z0-9_]
    # Check includes at least 1 letter
    # Check first character isn't underscore (_)
    # Check username length is valid (0<len<16)

    def CheckUsernameValid(self):
        username = self.playerData['username']
        flag_letter = False
        flag_chars = True
        flag_first = False
        flag_length = False
        for i in username:
            if i.isalpha():
                flag_letter = True
            if not (i.isalnum() or i == '_'):
                flag_chars = False
        if username[0].isalnum():
            flag_first = True
        if 0 <= len(username) < 16:
            flag_length = True
        if not flag_letter:
            raise UsernameLetterError()
        if not flag_chars:
            raise UsernameCharError()
        if not flag_first:
            raise UsernameFirstError()
        if not flag_length:
            raise UsernameLengthError()
        return flag_letter and flag_chars and flag_first and flag_length

    def passwordValid(password):
        if (password):
            return "error"
        # Check password length is valid (len>4,len<20)
        # Check password contains at least 1 letter, 1 number, 1 special character (!?_@£€$%&)