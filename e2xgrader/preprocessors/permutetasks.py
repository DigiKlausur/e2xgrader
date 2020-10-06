import random
from nbgrader.preprocessors import NbGraderPreprocessor

class PermuteTasks(NbGraderPreprocessor):
    
    def __init__(self, **kw):
        self.rand = random.Random()
        if kw and 'seed' in kw:
            self.rand = random.Random(kw['seed'])

    
    def is_nbgrader_cell(self, cell):
        return 'nbgrader' in cell.metadata
    
    def is_solution_cell(self, cell):
        return self.is_nbgrader_cell(cell) and cell.metadata.nbgrader.solution
    
    def get_header(self, nb, task_ids):
        header_idx = []
        for i in range(len(nb.cells)):
            cell = nb.cells[i]
            if not self.is_nbgrader_cell(cell):
                header_idx.append(i)
            else:
                grade_id = cell.metadata.nbgrader.grade_id
                if not any(task_id in grade_id for task_id in task_ids):
                    header_idx.append(i)
        return header_idx
    
    def get_tasks(self, nb, task_ids):
        associated = dict()
        checked = dict()
        
        for task_id in task_ids:
            checked[task_id] = False
            associated[task_id] = []
            for cell in nb.cells:
                if self.is_nbgrader_cell(cell):
                    grade_id = cell.metadata.nbgrader.grade_id
                    if task_id in grade_id:
                        associated[task_id].append(grade_id)

        groups = []
        for i in range(len(task_ids)):
            task_id = task_ids[i]
            if checked[task_id]:
                continue
            new_group = set(associated[task_id])
            for j in range(i+1, len(task_ids)):
                task_idj = task_ids[j]
                if any(t in associated[task_idj] for t in associated[task_id]):
                    new_group.update(associated[task_idj])
                    checked[task_idj] = True
            groups.append(new_group)

        cell_groups = []
        for group in groups:
            cell_group = []
            for i in range(len(nb.cells)):
                cell = nb.cells[i]
                if self.is_nbgrader_cell(cell) and cell.metadata.nbgrader.grade_id in group:
                    cell_group.append(i)
            cell_groups.append(cell_group)
            
        return cell_groups
    
    def preprocess(self, nb, resources):
        # Extract ids of solution cells
        task_ids = [cell.metadata.nbgrader.grade_id for cell in nb.cells
                    if self.is_solution_cell(cell)]
        # Get indices of header
        header_idx = self.get_header(nb, task_ids)
        # Get indices of tasks
        tasks = self.get_tasks(nb, task_ids)
        self.rand.shuffle(tasks)
        ids = header_idx
        for task in tasks:
            ids.extend(task)
            
        cells = [nb.cells[i] for i in ids]
        nb.cells = cells
        return nb, resources