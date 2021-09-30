from nbgrader.preprocessors import NbGraderPreprocessor


class FilterCellsById(NbGraderPreprocessor):
    def filter_cells(self, cells, keyword):
        new_cells = []
        for cell in cells:
            metadata = cell["metadata"]
            if (
                ("nbgrader" in metadata)
                and ("grade_id" in metadata["nbgrader"])
                and (keyword in cell["metadata"]["nbgrader"]["grade_id"])
            ):
                new_cells.append(cell)
        return new_cells

    def preprocess(self, nb, resources):
        if "keyword" in resources:
            nb.cells = self.filter_cells(nb.cells, resources["keyword"])
        return nb, resources
