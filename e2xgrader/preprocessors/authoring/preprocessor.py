from traitlets.config import LoggingConfigurable
from traitlets import Unicode

class Preprocessor(LoggingConfigurable):
    
    template_path = Unicode('templates')
    task_path = Unicode('pools')
    
    def preprocess(self, resources):
        raise NotImplementedError