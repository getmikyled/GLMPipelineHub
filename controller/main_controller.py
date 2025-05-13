from view import MainWindow
from view.dashboard_view import DashboardView
from .controller import Controller
from .dashboard_controller import DashboardController


class MainController(Controller):
    """
    Acts as the main controller class for the window and application, as well as the parent
    controller for any children controllers.
    """

    def __init__(self):
        """Initializes the Main Controller. Caches model and view. Creates the application's window."""
        model = None
        view = MainWindow()
        Controller.__init__(self, model, view)

        # Create dashboard view
        self.dashboard_view = DashboardView(self.view.stack)
        self.dashboard_controller = DashboardController(model=self.model, view=self.dashboard_view, parent_controller=self)