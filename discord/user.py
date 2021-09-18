from munch import Munch

class User(Munch):
    """Represents a User in Discord.

    Args:
        user (dict): The dictionary containing the User's data.
    """
    def __init__(self, user):
        super(User, self).__init__(user)