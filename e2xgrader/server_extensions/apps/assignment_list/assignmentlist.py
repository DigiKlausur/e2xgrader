from e2xcore import BaseApp

from .handlers import default_handlers


class AssignmentList(BaseApp):
    def load_app(self):
        self.log.info("Loading the assignment list app")
        self.log.info(self.parent.notebook_dir)
        if self.parent.name == "jupyter-notebook":
            self.update_tornado_settings(
                dict(assignment_list_manager=self.parent.notebook_dir)
            )
        else:
            self.update_tornado_settings(
                dict(assignment_list_manager=self.parent.root_dir)
            )

        self.add_handlers(default_handlers)
