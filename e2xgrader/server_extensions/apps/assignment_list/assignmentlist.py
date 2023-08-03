from e2xcore import BaseApp

from .handlers import E2xAssignmentList, default_handlers


class AssignmentList(BaseApp):
    def load_app(self):
        self.log.info("Loading the assignment list app")
        self.log.info(self.parent.notebook_dir)
        lister = E2xAssignmentList(parent=self.parent)
        if self.parent.name == "jupyter-notebook":
            lister.root_dir = self.parent.notebook_dir
        else:
            lister.root_dir = self.parent.root_dir

        self.update_tornado_settings(dict(assignment_list_manager=lister))

        self.add_handlers(default_handlers)
