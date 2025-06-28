'''
This file will contain the functions and variables that can halpe with handling type hinting better
'''
import typing as t
import inspect
import tokenize
import io


class Type_Helper():
    def __init__(self) -> None:
        pass
        
    def get_typed_dict_definition_content(self, typed_dict: t.Type[t.Any], trail_lines: int = 5) -> str:



        # 1. Get file and source lines
        source_file = inspect.getfile(typed_dict)
        with open(source_file, "r") as f:
            all_lines = f.readlines()

        # 2. Get class lines + extra trailing lines
        class_start_line = inspect.getsourcelines(typed_dict)[1] - 1
        class_lines = all_lines[class_start_line:class_start_line + trail_lines + 20]  # generous window

        # 3. Try to capture until next top-level def/class or EOF
        output_lines: t.List[str] = []
        indent = None
        for line in class_lines:
            stripped = line.strip()
            if stripped.startswith("class ") or stripped.startswith("def "):
                if output_lines:  # stop if this is a new block after the one we're collecting
                    break
            if indent is None and stripped:
                indent = len(line) - len(line.lstrip())
            output_lines.append(line)

        # Remove any comments contents in the lines 
        output_lines = self._strip_comments(output_lines)

        return "".join(output_lines)

    def _strip_comments(self, lines: t.List[str]) -> t.List[t.Any]:
        source = ''.join(lines)
        out = []
        prev_end = (1, 0)
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for toknum, tokval, start, end, line in tokens:
            if toknum == tokenize.COMMENT:
                # skip comment tokens
                continue
            # add whitespace between tokens
            row, col = start
            prow, pcol = prev_end
            if row > prow:
                out.append('\n' * (row - prow))
                out.append(' ' * col)
            else:
                out.append(' ' * (col - pcol))
            out.append(tokval)
            prev_end = end
        return ''.join(out).splitlines(keepends=True)