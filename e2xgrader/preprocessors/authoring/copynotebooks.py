import os
import shutil
from .preprocessor import Preprocessor

class CopyNotebooks(Preprocessor):
    
    def preprocess(self, resources):
        for task_dict in resources['tasks']:
            task = task_dict['task']
            pool = task_dict['pool']
            task = os.path.join(pool, task)
            src = os.path.join(resources['course_prefix'], self.task_path, task)
            dst = os.path.join(resources['tmp_dir'], 'tasks', task)
            shutil.copytree(src, dst)
        src = os.path.join(resources['course_prefix'], self.template_path, resources['template'])
        dst = os.path.join(resources['tmp_dir'], 'template', resources['template'])
        shutil.copytree(src, dst)
        return resources