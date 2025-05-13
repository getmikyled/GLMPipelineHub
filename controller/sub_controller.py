from .controller import Controller

class SubController(Controller):
    """
    Acts as a child controller to any parent controllers. Allows you to access the parent controller directly.
    """

    def __init__(self, model, view, parent_controller):
        super().__init__(model, view)

        self.parent_controller = parent_controller