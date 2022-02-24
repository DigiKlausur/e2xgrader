import os
import pickle
from nbgrader.preprocessors import NbGraderPreprocessor
from nbformat.notebooknode import NotebookNode
from nbformat.v4 import new_code_cell
from nbconvert.exporters.exporter import ResourcesDict
from traitlets import Bool
from typing import Tuple
from e2xgrader.utils.nbgrader_cells import grade_id, is_solution_cell
from e2xgrader.utils.extra_cells import is_extra_cell
from textwrap import dedent


class AddAutogradingInfo(NbGraderPreprocessor):
    def create_notebook_dict(self, nb: NotebookNode, resources: ResourcesDict):
        """
        Save information about cells in an external file
        and load it in the first cell of the notebook

        This way you access the source for standard solution cells or
        the metadata for extra cells in a dictionary called __cells
        """
        autograded_path = resources["metadata"]["path"]
        dict_path = os.path.join(autograded_path, "grading_dict")

        grading_dict = dict()

        for cell in nb.cells:
            if is_solution_cell(cell):
                if is_extra_cell(cell):
                    grading_dict[grade_id(cell)] = cell.metadata.extended_cell
                else:
                    grading_dict[grade_id(cell)] = cell.source

        os.makedirs(dict_path, exist_ok=True)
        with open(
            os.path.join(dict_path, f'{resources["nbgrader"]["notebook"]}.pkl'), "wb"
        ) as f:
            f.write(pickle.dumps(grading_dict))

        autograding_cell = new_code_cell(
            source=dedent(
                f"""
            import os
            import pickle

            grading_dict_path = os.path.join('grading_dict', '{resources["nbgrader"]["notebook"]}.pkl')
            with open(grading_dict_path, 'rb') as f:
                __cells = pickle.loads(f.read())
            """
            )
        )
        nb.cells = [autograding_cell] + nb.cells

    def preprocess(
        self, nb: NotebookNode, resources: ResourcesDict
    ) -> Tuple[NotebookNode, ResourcesDict]:
        if nb.metadata.language_info.name == "python":
            self.create_notebook_dict(nb, resources)
        else:
            self.log.info(
                "Autograding information can only be added for Python notebooks!"
            )
        return nb, resources
