from e2xcore import BaseApp

from .handlers import E2xAssignmentList, default_handlers


class AssignmentList(BaseApp):
    def load_app(self):
        self.log.info("Loading the e2x assignment list app")
        lister = E2xAssignmentList(parent=self.parent)
        lister.root_dir = self.webapp.settings["root_dir"]

        self.update_tornado_settings(dict(assignment_list_manager=lister))

        self.add_handlers(default_handlers)
