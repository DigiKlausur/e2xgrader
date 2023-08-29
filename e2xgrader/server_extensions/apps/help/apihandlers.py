import json
import os

from e2xcore import urljoin
from e2xcore.handlers import E2xApiHandler
from tornado import web


class ListFilesHandler(E2xApiHandler):
    def list_files(self, path_id, path):
        self.log.info(f"Listing files from {path}")
        if path is None or not os.path.exists(path):
            return []
        file_list = []
        exclude_dirs = []

        for root, dirs, files in os.walk(path):
            for name in dirs:
                if name.startswith("."):
                    exclude_dirs.append(name)
                elif os.path.isfile(os.path.join(root, name, "index.html")):
                    exclude_dirs.append(name)
                    file_list.append(
                        (
                            os.path.join(root, name),
                            os.path.join(root, name, "index.html"),
                        )
                    )

            dirs[:] = [d for d in dirs if d not in exclude_dirs]

            for name in files:
                file_list.append((os.path.join(root, name), os.path.join(root, name)))

        file_list = [
            (
                os.path.relpath(name, path),
                os.path.join(path_id, os.path.relpath(url, path)),
            )
            for name, url in file_list
        ]

        return file_list

    @web.authenticated
    def get(self):
        files = []
        for path_id, path in self.settings.get("e2xhelp_shared_dirs", dict()).items():
            files.extend(self.list_files(path_id, path))
        self.write(json.dumps(files))


api_url = urljoin("e2x", "help", "api")
default_handlers = [
    (urljoin(api_url, "files"), ListFilesHandler),
]
