from typing import List, Union

from nbformat.notebooknode import NotebookNode
from nbgrader import utils
from nbgrader.validator import Validator

from ....utils.extra_cells import (
    get_choices,
    is_attachment_cell,
    is_extra_cell,
    is_multiplechoice,
    is_singlechoice,
)


class E2XValidator(Validator):
    def validate_extra_cell(self, cell: NotebookNode) -> Union[None, float]:
        if (
            (is_multiplechoice(cell) or is_singlechoice(cell))
            and len(get_choices(cell)) < 1
        ) or (is_attachment_cell(cell) and len(cell.get("attachments", {})) < 1):
            return 0

    def code_cell_errored(self, cell: NotebookNode) -> bool:
        for output in cell.outputs:
            if (
                output.output_type == "error"
                or output.output_type == "stream"
                and output.name == "stderr"
            ):
                return True
        return False

    def _get_failed_cells(self, nb: NotebookNode) -> List[NotebookNode]:
        failed = []
        for cell in nb.cells:
            if self._should_skip_cell(cell):
                continue

            # if it's a grade cell, the check the grade
            if utils.is_grade(cell):
                score, max_score = utils.determine_grade(cell, self.log)

                if is_extra_cell(cell):
                    score = self.validate_extra_cell(cell)

                # it's a markdown cell, so we can't do anything
                if score is not None and score < max_score:
                    failed.append(cell)
            elif (
                self.validate_all
                and cell.cell_type == "code"
                and self.code_cell_errored(cell)
            ):
                failed.append(cell)

        return failed

    def _should_skip_cell(self, cell: NotebookNode) -> bool:
        return not (self.validate_all or utils.is_grade(cell) or utils.is_locked(cell))
