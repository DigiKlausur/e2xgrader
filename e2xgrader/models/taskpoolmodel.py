import os
import shutil

from traitlets import Unicode

from .basemodel import BaseModel


class TaskPoolModel(BaseModel):

    directory = Unicode("pools", help="The directory where the task pools go.")

    def new(self, **kwargs):
        name = kwargs["name"]
        if self.is_valid_name(name):
            path = os.path.join(self.base_path(), name)
            if os.path.exists(path):
                return {
                    "success": False,
                    "error": f"A pool with the name {name} already exists!",
                }
            else:
                os.makedirs(path, exist_ok=True)
                return {"success": True, "path": path}
        else:
            return {"success": False, "error": "Invalid name"}

    def remove(self, **kwargs):
        name = kwargs["name"]
        path = os.path.join(self.base_path(), name)
        shutil.rmtree(path)

    def get(self, **kwargs):
        name = kwargs["name"]
        tasks = self.__get_pool_info(name)
        return {
            "name": name,
            "tasks": tasks,
            "link": os.path.join("taskcreator", "pools", name),
        }

    def list(self, **kwargs):
        if not os.path.isdir(self.base_path()):
            os.makedirs(self.base_path(), exist_ok=True)
        poolfolders = os.listdir(self.base_path())
        pools = []
        for poolfolder in poolfolders:
            if poolfolder.startswith("."):
                continue
            tasks = self.__get_pool_info(poolfolder)
            pools.append(
                {
                    "name": poolfolder,
                    "tasks": tasks,
                    "link": os.path.join("taskcreator", "pools", poolfolder),
                }
            )

        return pools

    def __get_pool_info(self, name):
        return len(os.listdir(os.path.join(self.base_path(), name)))
