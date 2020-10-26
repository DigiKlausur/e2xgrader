import random
from nbgrader.preprocessors import NbGraderPreprocessor

class UnpermuteTasks(NbGraderPreprocessor):
    
    def preprocess(self, nb, resources):
        if 'permutation' in nb.metadata:
            perm = nb.metadata.permutation
            keys = sorted(range(len(perm)), key=perm.__getitem__)
            reorder_cells = [nb.cells[i] for i in keys]
            nb.cells = reorder_cells
        return nb, resources