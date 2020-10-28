def is_nbgrader_cell(cell):
    return 'nbgrader' in cell.metadata

def is_solution_cell(cell):
    return is_nbgrader_cell(cell) and cell.metadata.nbgrader.solution

def grade_id(cell):
    if is_nbgrader_cell(cell):
        return cell.metadata.nbgrader.grade_id

def get_tasks(nb):
    task_ids = [grade_id(cell) for cell in nb.cells 
                if is_solution_cell(cell)]
    associated = dict()
    checked = dict()

    for task_id in task_ids:
        checked[task_id] = False
        associated[task_id] = []
        for cell in nb.cells:
            if is_nbgrader_cell(cell) and task_id in grade_id(cell):
                associated[task_id].append(grade_id(cell))

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
            if is_nbgrader_cell(cell) and grade_id(cell) in group:
                cell_group.append(i)
        cell_groups.append(cell_group)

    return cell_groups