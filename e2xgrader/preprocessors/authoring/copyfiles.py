import os
import shutil
import glob
import filecmp
import nbformat
from .preprocessor import Preprocessor


class CopyFiles(Preprocessor):

    def rename(self, task, old_name, new_name):
        old_file_name = os.path.split(old_name)[1]
        new_file_name = os.path.split(new_name)[1]
        for nb_file in glob.glob(os.path.join(task, '*.ipynb')):
            nb = nbformat.read(nb_file, as_version=4)
            for cell in nb.cells:
                cell.source = cell.source.replace(old_name, new_name)
                if old_file_name != new_file_name:
                    cell.source = cell.source.replace(old_file_name, new_file_name)
            nbformat.write(nb, nb_file)

    def get_new_name(self, file, dst):
        suffix = 1
        name, extension = os.path.splitext(file)
        new_name = '{}_{}{}'.format(name, suffix, extension)
        while os.path.exists(os.path.join(dst, new_name)):
            suffix += 1
            new_name = '{}_{}{}'.format(name, suffix, extension)
        return new_name

    def get_files(self, task):
        finds = []
        for subdir in ['img', 'data']:
            for root, dirs, files in os.walk(os.path.join(task, subdir)):
                dirs[:] = [d for d in dirs if d not in ['.ipynb_checkpoints']]
                for file in files:
                    finds.append(os.path.relpath(os.path.join(root, file), task))
        return finds

    def copyfile(self, src, dst):
        '''
        Copy file

        Arguments:
            src -- source file
            dst -- destination file
        Returns:
            status -- True if dst does not exists or is equal to src,
                      False if dst exists and differs from src.
                      In this case nothing is copied
        '''
        if os.path.exists(dst):
            return filecmp.cmp(src, dst)
        dirs = os.path.split(dst)[0]
        os.makedirs(dirs, exist_ok=True)
        shutil.copyfile(src, dst)
        return True

    def copyfiles(self, src, dst, resources):
        exercise_base = '{}_files'.format(resources['exercise'])
        for file in self.get_files(src):
            src_file = os.path.join(src, file)
            dst_file = os.path.join(dst, file)
            new_name = os.path.join(exercise_base, file)
            if not self.copyfile(src_file, dst_file):
                # File with that name already exists
                renamed = self.get_new_name(file, dst)
                self.copyfile(src_file, os.path.join(dst, renamed))
                new_name = os.path.join(exercise_base, renamed)
            # Rename in notebook
            self.rename(src, file, new_name)

    def preprocess(self, resources):
        file_folder = os.path.join(
            resources['course_prefix'],
            resources['source_dir'],
            resources['assignment'],
            '{}_files'.format(resources['exercise'])
        )
        os.makedirs(file_folder, exist_ok=True)

        for task_dict in resources['tasks']:
            task = os.path.join(task_dict['pool'], task_dict['task'])
            task_path = os.path.join(
                resources['tmp_dir'],
                'tasks',
                task
            )
            self.copyfiles(task_path, file_folder, resources)

        template_path = os.path.join(
            resources['tmp_dir'],
            'template',
            resources['template']
        )
        self.copyfiles(template_path, file_folder, resources)
