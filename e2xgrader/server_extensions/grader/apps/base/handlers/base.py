from notebook.base.handlers import IPythonHandler


class E2xHandler(IPythonHandler):
    @property
    def e2xgrader_settings(self):
        return self.settings["e2xgrader"]

    @property
    def jinja_env(self):
        return self.e2xgrader_settings["jinja_env"]

    @property
    def menu(self):
        return self.e2xgrader_settings["menu"]

    def render(self, name, **ns):
        template = self.jinja_env.get_template(name)
        return template.render(**ns)
