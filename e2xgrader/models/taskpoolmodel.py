import os
import nbformat
import shutil
from .basemodel import BaseModel
from traitlets import Unicode

class TaskPoolModel(BaseModel):

    directory = Unicode(
        'pools',
        help='The directory where the task pools go.'
    )

    def new(self, name):
        path = os.path.join(self.base_path(), name)
        os.makedirs(path, exist_ok=True)
        return path

    def remove(self, name):
        path = os.path.join(self.base_path(), name)
        shutil.rmtree(path)

    def get(self, name):
        tasks = self.__get_pool_info(name)
        return {
            'name': name,
            'tasks': tasks,
            'link': os.path.join('taskcreator', 'pools', poolfolder)
        }
    
    def list(self):
        if not os.path.isdir(self.base_path()):
            os.makedirs(self.base_path(), exist_ok=True)
        poolfolders = os.listdir(self.base_path())
        pools = []
        for poolfolder in poolfolders:
            if poolfolder.startswith('.'):
                continue
            tasks = self.__get_pool_info(poolfolder)
            pools.append({
                'name': poolfolder,
                'tasks': tasks,
                'link': os.path.join('taskcreator', 'pools', poolfolder)
            })
        
        return pools

    def __get_pool_info(self, name):
        return len(os.listdir(os.path.join(self.base_path(), name)))