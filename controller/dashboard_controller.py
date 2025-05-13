from .sub_controller import SubController

class DashboardController(SubController):

    def __init__(self, model, view, parent_controller):
        """Initializes the DashboardController class."""
        super().__init__(model, view, parent_controller)