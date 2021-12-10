import typing
from nbgrader.validator import Validator
from nbgrader import utils
from nbformat.notebooknode import NotebookNode
from .utils.extra_cells import (
    is_extra_cell,
    is_multiplechoice,
    is_singlechoice,
    is_attachment_cell,
    get_choices,
)


class E2XValidator(Validator):
    def _get_failed_cells(self, nb: NotebookNode) -> typing.List[NotebookNode]:
        failed = []
        for cell in nb.cells:
            if not (self.validate_all or utils.is_grade(cell) or utils.is_locked(cell)):
                continue

            # if it's a grade cell, the check the grade
            if utils.is_grade(cell):
                score, max_score = utils.determine_grade(cell, self.log)

                if is_extra_cell(cell):
                    # if it's an extra cell, check if an answer was given
                    score = None
                    if (
                        (is_multiplechoice(cell)
                        or is_singlechoice(cell))
                        and len(get_choices(cell)) < 1
                    ) or (
                        is_attachment_cell(cell)
                        and len(cell.get("attachments", {})) < 1
                    ):
                        score = 0

                # it's a markdown cell, so we can't do anything
                if score is None:
                    pass
                elif score < max_score:
                    failed.append(cell)
            elif self.validate_all and cell.cell_type == "code":
                for output in cell.outputs:
                    if (
                        output.output_type == "error"
                        or output.output_type == "stream"
                        and output.name == "stderr"
                    ):
                        failed.append(cell)
                        break

        return failed
