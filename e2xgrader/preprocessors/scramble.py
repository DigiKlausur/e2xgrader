import base64
import copy
import pickle
import random
import re

import nbformat
from nbgrader.preprocessors import NbGraderPreprocessor


class Scramble(NbGraderPreprocessor):
    def __init__(self, **kw):
        self.__seed = random.randint(0, 10000000)
        self.__random = random.Random(self.__seed)
        self.__p_define = re.compile(
            r"^#define +(?P<fun>\w+)\((?P<args>[^(]*)\) +(?P<body>.*)"
        )
        self.__p_set = re.compile(r"^#set +(?P<name>\w+) += +(?P<options>.*)")
        self.__p_random = re.compile(r"^#random +(?P<vars>.*) +in +(?P<sets>.*)")
        self.__p_replace = re.compile(r"#replace +(?P<name>\w+) +(?P<replace_with>.*)")
        self.__p_lambda = re.compile("^#lambda +(?P<name>[^ ]+) +(?P<lambda>.*)")
        if kw and "seed" in kw:
            self.__random = random.Random(kw["seed"])
            self.__seed = kw["seed"]

    def parse_define(self, line):
        match = self.__p_define.search(line)
        f_name = match.group("fun")
        f_args = [arg.strip() for arg in match.group("args").split(",")]
        f_body = match.group("body")
        return f_name, f_args, f_body

    def parse_set(self, line):
        match = self.__p_set.search(line)
        if match:
            return match.group("name"), match.group("options")
        return None

    def parse_random(self, line, sets):
        match = self.__p_random.search(line)
        if not match:
            return None
        opts = [s.strip() for s in match.group("sets").split(",")]
        var_str = match.group("vars")
        if "!=" in var_str:
            rand_vars = [s.strip() for s in var_str.split("!=")]
            var_groups = [[v.strip() for v in s.split(",")] for s in rand_vars]
            return var_groups, "!=", opts
        else:
            rand_vars = [s.strip() for s in var_str.split("==")]
            var_groups = [[v.strip() for v in s.split(",")] for s in rand_vars]
            return var_groups, "==", opts

    def parse_replace(self, line):
        match = self.__p_replace.search(line)
        if not match:
            return None
        return match.group("name"), match.group("replace_with")

    def parse_lambda(self, line):
        match = self.__p_lambda.search(line)
        if not match:
            return None
        return match.group("name"), "lambda " + match.group("lambda")

    def replace(self, text, macro):
        p_macro = re.compile(r"(?P<fun>{}\((?P<args>[^)]*)\))".format(macro[0]))
        processed = text
        for match in p_macro.finditer(text):
            args = [arg.strip() for arg in match.group("args").split(",")]
            assert len(macro[1]) == len(
                args
            ), "Wrong number of arguments for macro {} with args {}".format(
                macro[0], args
            )
            replacement = macro[2]
            for i in range(len(args)):
                replacement = replacement.replace(macro[1][i], args[i])
            processed = processed.replace(match.group("fun"), replacement)
        return processed

    def replace_lambdas(self, text, name, expr):
        p_macro = re.compile(r"(?P<fun>{}\((?P<args>[^)]*)\))".format(name))
        processed = text
        for match in p_macro.finditer(text):
            args = [arg.strip() for arg in match.group("args").split(",")]

            replacement = expr(*args)
            processed = processed.replace(match.group("fun"), str(replacement))
        return processed

    def sample(self, groups, constraint, sets_names, set_dict):
        sets = [set_dict[sets_name] for sets_name in sets_names]
        rand_dict = {}
        if constraint == "==":
            k = 1
            sampled_idx = self.__random.sample(range(len(sets[0])), k=k)
            for g_idx in range(len(groups)):
                group = groups[g_idx]
                for set_idx in range(len(group)):
                    rand_dict[group[set_idx]] = sets[set_idx][sampled_idx[0]]
            return rand_dict

        if constraint == "!=":
            k = len(groups)
            sampled_idx = self.__random.sample(range(len(sets[0])), k=k)
            for g_idx in range(len(groups)):
                group = groups[g_idx]
                for set_idx in range(len(group)):
                    rand_dict[group[set_idx]] = sets[set_idx][sampled_idx[g_idx]]
            return rand_dict

    def sample_config(self, config):
        lines = config.split("\n")
        new_lines = []
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            while line.endswith("\\"):
                line = line[:-1]
                line += lines[i + 1].strip()
                i += 1
            i += 1

            new_lines.append(line)
        lines = new_lines

        macros = []
        sets = {}
        rands = []
        rand_vars = {}
        replaces = {}
        lambdas = {}
        for line in lines:
            line = line.strip()
            if line.startswith("#define"):
                macros.append(list(self.parse_define(line)))
            elif line.startswith("#set"):
                name, opts = self.parse_set(line)
                sets[name] = [opt.strip() for opt in opts.split("||")]
            elif line.startswith("#random"):
                rands.append(self.parse_random(line, sets))
            elif line.startswith("#replace"):
                name, replace_with = self.parse_replace(line)
                replaces[name] = replace_with
            elif line.startswith("#lambda"):
                name, lambda_expr = self.parse_lambda(line)
                lambdas[name] = eval(lambda_expr)

        for i in range(len(macros)):
            for j in range(i + 1, len(macros)):
                macros[j][2] = self.replace(macros[j][2], macros[i])
            for set_name in sets:
                sets[set_name] = [self.replace(s, macros[i]) for s in sets[set_name]]
            for r_name in replaces:
                replaces[r_name] = self.replace(replaces[r_name], macros[i])

        for rand in rands:
            rand_vars.update(self.sample(rand[0], rand[1], rand[2], sets))

        for rand in rand_vars:
            for r_name in replaces:
                replaces[r_name] = replaces[r_name].replace(rand, rand_vars[rand])

        for rand in rand_vars:
            for r_name in replaces:
                replaces[r_name] = replaces[r_name].replace(rand, rand_vars[rand])

        for rand in rand_vars:
            for r_name in replaces:
                replaces[r_name] = replaces[r_name].replace(rand, rand_vars[rand])

        for lambda_expr in lambdas:
            for r_name in replaces:
                replaces[r_name] = self.replace_lambdas(
                    replaces[r_name], lambda_expr, lambdas[lambda_expr]
                )

        return {
            "seed": self.__seed,
            "macros": macros,
            "sets": sets,
            "rands": rand_vars,
            "replace": replaces,
        }

    def obscure(self, my_dict):
        byte_str = pickle.dumps(my_dict)
        obscured = base64.b85encode(byte_str)
        return obscured

    def preprocess(self, nb, resources):
        if len(nb.cells) < 1 or not nb.cells[0].source.startswith("%% scramble"):
            return nb, resources
        config = self.sample_config(nb.cells[0].source)
        replacement_variables = config["replace"]
        scrambled_nb = nbformat.v4.new_notebook()
        scrambled_nb.cells = copy.deepcopy(nb.cells[1:])
        for cell in scrambled_nb.cells:
            for replacement_variable in replacement_variables:
                cell.source = cell.source.replace(
                    "{{" + replacement_variable + "}}",
                    replacement_variables[replacement_variable],
                )
        scrambled_nb.metadata["scramble_config"] = {
            "seed": config["seed"],
            "config": self.obscure(replacement_variables),
        }
        return scrambled_nb, resources
