from nbconvert.utils.base import NbConvertBase
from bs4 import BeautifulSoup

from ...utils import extra_cells as utils
from ...utils.extra_cells import (is_singlechoice, is_multiplechoice, has_solution,
     is_form, get_choices, get_instructor_choices, get_form_answers)

class RenderExtraCell(NbConvertBase):

    def render_choicecell(self, source, cell):
        soup = BeautifulSoup(source, "html.parser")
        my_type = None
        if not soup.ul:
            return soup.prettify().replace("\n", "")
        if is_singlechoice(cell):
            my_type = "radio"
        elif is_multiplechoice(cell):
            my_type = "checkbox"
        form = soup.new_tag("form")
        form["class"] = "hbrs_checkbox"

        list_elems = soup.ul.find_all("li")
        for i in range(len(list_elems)):
            div = soup.new_tag("div")
            box = soup.new_tag("input")
            box["type"] = my_type
            box["value"] = i
            box["disabled"] = "disabled"
            if i in get_choices(cell):
                box["checked"] = "checked"
            div.append(box)
            children = [c for c in list_elems[i].children]
            for child in children:
                div.append(child)

            if has_solution(cell):
                check = soup.new_tag("span")
                if i in get_instructor_choices(cell):
                    check.string = "correct"
                    check["style"] = "color:green"
                else:
                    check.string = "false"
                    check["style"] = "color:red"
                div.append(check)
            form.append(div)
        soup.ul.replaceWith(form)
        return soup.prettify().replace("\n", "")

    def render_formcell(self, source, cell):
        soup = BeautifulSoup(source, "html.parser")

        choices = get_form_answers(cell)

        # Handle all input elements
        for input_elem in soup.find_all('input'):
            # Disable all input elements
            input_elem['disabled'] = 'disabled'

            # Set stored values
            name = input_elem.get('name', None)
            if name in choices:
                val = choices[name]['value']
                input_elem['value'] = val

        # Handle all select elements
        for select in soup.find_all('select'):
            # Disable all select elements
            select['disabled'] = 'disabled'

            # Set stored values
            name = select.get('name', None)
            if name in choices:
                for option in select.find_all('option'):
                    if option.get('value', None) == choices[name]['value']:
                        option['selected'] = 'selected'
                        break

        return soup.prettify().replace("\n", "")

    def __call__(self, source, cell=None):
        """
        Return a rendered version of the e2xgrader choice cell

        Parameters
        ----------
        source : str
            source of the cell
        cell : NotebookNode cell
            cell

        Returns
        -------
        out: string
            Output html of cell
        """
        if is_singlechoice(cell) or is_multiplechoice(cell):
            return self.render_choicecell(source, cell)
        elif is_form(cell):
            return self.render_formcell(source, cell)
        return source
