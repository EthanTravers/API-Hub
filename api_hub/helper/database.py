class DatabaseContainsUsernameError(ValueError):
    @staticmethod
    def getMessage():
        return "Username already exists in database"

class DatabaseDoesNotContainUsernameError(ValueError):
    @staticmethod
    def getMessage():
        return "Username does not exist in database"

def CosmosHttpResponseErrorMessage() -> str:
    return "Issue connecting to the Cosmos Database"

