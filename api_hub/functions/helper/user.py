import json

def usernameValid(username):
    # Check characters are allowed [a-zA-Z0-9_]
    # Check includes at least 1 letter
    # Check first character isnt underscore (_)
    # Check username length is valid (len<15)
    if (username):
        return "error"
def passwordValid(password):
    if(password):
        return "error"
    # Check password length is valid (len>4,len<20)
    # Check password contains at least 1 letter, 1 number, 1 special character (!?_@£€$%&)

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