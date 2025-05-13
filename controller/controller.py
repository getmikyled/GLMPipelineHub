
class Controller:

    def __init__(self, model, view):
        """Initializes the controller"""

        # Cache the controller's associated model and view
        self.model = model
        self.view = view