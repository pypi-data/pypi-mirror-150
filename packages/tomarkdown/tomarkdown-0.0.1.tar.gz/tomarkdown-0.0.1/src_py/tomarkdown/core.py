from .token import *

import pathlib

from typing import Any


# TODO: command line


def py_source_to_token(path_from: pathlib.Path) -> list[list[Token]]:
    with open(path_from, mode = 'r') as in_stream:
        txt_source = in_stream.readlines()

    line_no: int = -1
    txt_line: str = 'xxx'
    new_txt_source: list[str] = []
    while True:  # line_no < len(txt_source):
        if (line_no := line_no + 1) >= len(txt_source): break
        else: txt_line = txt_source[line_no]

        '''
            gather py_line, cleanse it and restore code-linebreaks
            ======================================================
        '''
        txt_line = txt_line.rstrip()  # strip of actual linebreaks: \n (but ignore those in string-vars within py_line)
        while True:  # repair code-linebreaks
            if not txt_line.endswith('\\'): break
            txt_line = txt_line[:-1].rstrip()
            if (line_no := line_no + 1) >= len(txt_source): break
            txt_line += ' ' + txt_source[line_no].lstrip()
            txt_line = txt_line.rstrip()
        txt_line = txt_line.rstrip()

        new_txt_source.append(txt_line)

    line_no: int = -1
    txt_source = new_txt_source
    py_lines: list[list[Token]] = []
    while True:  # line_no < len(txt_source):
        if (line_no := line_no + 1) >= len(txt_source): break
        else: txt_line = txt_source[line_no]

        curr_indent: int = len(txt_line) - len(txt_line.lstrip(' '))
        py_line: list[Token] = [IndentationToken(curr_indent, line_no = line_no)]

        letter_no: int = -1
        letter: str = 'xxx'
        skip_to_next_line: bool = False
        while True:
            '''
                grab next letter/char (within a txt_line)
                -----------------------------------------
            '''
            if (letter_no := letter_no + 1) >= len(txt_line): break
            else: letter = txt_line[letter_no]

            '''
                skip whitespaces and tabulators
                -------------------------------
            '''
            while letter in ' \t':
                if (letter_no := letter_no + 1) >= len(txt_line): break
                else: letter = txt_line[letter_no]

            '''
                identify & tokenize regular and special operation/operator symbols
                ------------------------------------------------------------------
            '''
            contiue_on: bool = False
            for sym, _Token in [('...', EllipsisToken),
                                ('//=', FloorDivAssignToken),
                                ('**=', PowAssignToken),
                                ('>>=', RShiftAssignToken),
                                ('<<=', LShiftAssignToken),
                                ('&=', AndAssignToken),
                                ('|=', OrAssignToken),
                                ('^=', XOrAssignToken),
                                ('+=', AddAssignToken),
                                ('-=', SubAssignToken),
                                ('*=', MulAssignToken),
                                ('/=', TrueDivAssignToken),
                                ('@=', MatMulAssignToken),
                                ('%=', ModuloAssignToken),
                                ('->', ArrowToken),
                                ('==', EqToken),
                                ('!=', NeqToken),
                                ('>=', GeToken),
                                ('<=', LeToken),
                                (':=', WalrusToken),
                                ('//', FloorDivToken),
                                # ('**', PowToken),  # special treatment
                                ('>>', RShiftToken),
                                ('<<', LShiftToken),
                                ('&', AndToken),
                                ('|', OrToken),
                                ('^', XOrToken),
                                ('+', AddToken),
                                ('-', SubToken),
                                ('*', MulToken),
                                ('/', TrueDivToken),
                                # ('@', MatMulToken),  # special treatment
                                ('~', InvertToken),
                                ('%', ModuloToken),
                                (',', SeperatorToken),
                                ('.', AttribToken),
                                (':', ColonToken),
                                ('=', AssignToken),
                                ('(', LParamToken), (')', RParamToken),
                                ('[', LBracToken), (']', RBracToken),
                                ('{', LCurBToken), ('}', RCurBToken)]:
                if txt_line[letter_no:letter_no + len(sym)] == sym:
                    if not (_Token is None): py_line.append(_Token(line_no = line_no, letter_no = letter_no))
                    letter_no += len(sym) - 1  # -1 because continue will invoke +1
                    contiue_on = True
                    break
            if contiue_on: continue
            del contiue_on

            '''
                special treatment of "@" and "**"
                ---------------------------------
                 - @ can be mattrix multiplication (dealt wth here) or initiating a decorator (see identifiers)
                 - ** can be the power function (dealt with here) or keywords (see identifiers)
            '''
            buf: bool = len(py_line) > 0
            num_or_ident: bool = isinstance(py_line[-1], (IdentToken, NumToken))
            if (letter == '@') and buf and num_or_ident:
                py_line.append(MatMulToken(line_no = line_no, letter_no = letter_no))
                continue
            elif (txt_line[letter_no:letter_no + 1] == '**') and buf and num_or_ident:
                py_line.append(PowToken(line_no = line_no, letter_no = letter_no))
                continue
            del buf

            '''
                identify & tokenize numbers (int & float)
                -----------------------------------------
            '''
            digits: str = '0123456789'
            num: str = ''
            if letter in f'-{digits}':
                num += letter
                if (letter_no := letter_no + 1) >= len(txt_line): break
                else: letter = txt_line[letter_no]
                while letter in f'{digits}._':
                    if (letter == '_') and (len(num) > 0) and (num[-1] == '.'):
                        raise AssertionError(f"[err:{line_no}] _ can't follow .")
                    if (letter == '.') and (len(num) > 0) and (num[-1] == '_'):
                        raise AssertionError(f"[err:{line_no}] . can't follow _")
                    num += letter
                    if (letter_no := letter_no + 1) >= len(txt_line): break
                    else: letter = txt_line[letter_no]
                else:
                    if num == '-': num = ''
                letter_no -= 1
                letter = txt_line[letter_no]
                if len(num) > 0:
                    py_line.append(NumToken(val = num, line_no = line_no, letter_no = letter_no))
                    continue

            '''
                identify & tokenize most identifiers (variable-names, function-names) & keywords
                --------------------------------------------------------------------------------
            '''
            specials: str = ' \t()[]{}:+-/\'.<>&|#~";=,^'  # removed @/*
            word: str = ''
            while not (letter in specials):
                if (len(word) == 1) and (word[0] != '*') and (letter == '*'): break
                word += letter
                if '@' in specials: specials = f'{specials}*'
                specials = f'{specials}@'
                if (letter_no := letter_no + 1) >= len(txt_line): break
                else: letter = txt_line[letter_no]
            if (len(word) == 1) and word in '@*':
                word = ''
                letter_no -= 1
                letter = txt_line[letter_no]
            if (len(word) > 0) and (((not (word[0] in '@*')) and (word[:2] != '**') and word.isidentifier()) or
                                    ((word[:2] == '**') and word[2:].isidentifier()) or
                                    ((word[0] in '@*') and word[1:].isidentifier())): pass
            elif len(word) > 0:
                print(txt_line)
                raise AssertionError(f'[err:{line_no}] >>{word}<< | letter_no: {letter_no}')
            if len(word) > 0:
                if word == 'def': py_line.append(DefToken(line_no = line_no, letter_no = letter_no))
                elif word == 'class': py_line.append(ClassToken(line_no = line_no, letter_no = letter_no))
                elif word[0] == '@': py_line.append(DecoratorToken(word[1:], line_no = line_no, letter_no = letter_no))
                elif word == 'pass': py_line.append(PassToken(line_no = line_no, letter_no = letter_no))
                else: py_line.append(IdentToken(word, line_no = line_no, letter_no = letter_no))
                letter_no -= 1
                continue
            if letter_no >= len(txt_line): break

            '''
                identify & tokenize strings, doc-strings
                ----------------------------------------
            '''
            break_outer_for_and_continue: bool = False
            for q_sym in '"\'':
                times: int = 0
                letter = txt_line[letter_no]
                while (letter == q_sym) and (times < 3):
                    times += 1
                    if (letter_no := letter_no + 1) >= len(txt_line): break
                    else: letter = txt_line[letter_no]

                content: str = ''
                if times == 0: continue
                if times == 1:
                    try: letter = txt_line[letter_no]
                    except IndexError: raise AssertionError(f'[err:{line_no}] multline string!')
                    while True:
                        if letter == q_sym: break
                        content += letter
                        if (letter_no := letter_no + 1) >= len(txt_line):
                            raise AssertionError(f'[err:{line_no}] multline string!')
                        else: letter = txt_line[letter_no]
                    py_line.append(StringToken(content, q_sym = q_sym, line_no = line_no, letter_no = letter_no))
                    break_outer_for_and_continue = True
                elif times == 2:
                    py_line.append(StringToken(content, q_sym = q_sym, line_no = line_no, letter_no = letter_no))
                    continue
                elif times == 3:
                    while True:
                        next_line: bool = True
                        while True:
                            try: letter = txt_line[letter_no]
                            except IndexError: break
                            if txt_line[letter_no:letter_no + 3] == q_sym*3:
                                next_line = False
                                letter_no += 2
                                break
                            content += letter
                            if (letter_no := letter_no + 1) >= len(txt_line): break
                            else: letter = txt_line[letter_no]
                        if next_line:
                            letter_no = curr_indent  # 0
                            content += '\n'
                            if (line_no := line_no + 1) >= len(txt_source): break
                            else: txt_line = txt_source[line_no]
                        else: break
                    py_line.append(DocStringToken(content, q_sym = q_sym, line_no = line_no, letter_no = letter_no))
                    break_outer_for_and_continue = True
                else: raise AssertionError(f'[err:{line_no}] this error is supposed to be unreachable! {times}')
                if break_outer_for_and_continue: break
            if break_outer_for_and_continue: continue

            '''
                identify & tokenize comments
                ----------------------------
            '''
            if letter == '#':
                py_line.append(CommentToken(txt_line[letter_no + 1:], line_no = line_no, letter_no = letter_no))
                skip_to_next_line = True
                break

        py_lines.append(py_line)
        if skip_to_next_line: continue

    return py_lines


def _conditioned_colon_check(line_no: int, py_line: list[Token]) -> bool | int:
    para_l: int = 0
    para_r: int = 0
    for token_no, tkn in enumerate(py_line):
        if isinstance(tkn, LParamToken): para_l += 1
        elif isinstance(tkn, RParamToken):
            if (para_l - para_r) <= 0: raise AssertionError(f'[err:{line_no}] more ")" then "("!')
            para_r += 1
        elif isinstance(tkn, ColonToken) and (para_l > 0) and (para_l - para_r == 0): return token_no
    return False


def token_line_to_yaml(py_lines: list[list[Token]]):
    inside_fc: list[dict] = []  # fc - func/class
    struct: list[dict[str, Any]] = []

    deco_stack: list[str] = []
    py_line_no: int = -1
    while True:  # for py_line in py_lines:
        '''
        increment line of token (manually)
        ==================================
        '''
        if (py_line_no := py_line_no + 1) >= len(py_lines): break
        else: py_line = py_lines[py_line_no]
        line_no: int = py_line[0].line_no

        '''
        for functions/classes that are not inline: finding their block defining indent
        ==============================================================================
        '''
        if len(inside_fc) > 0:
            if inside_fc[-1]['sub_struct']['base_indent'] == 'x':
                inside_fc[-1]['sub_struct']['base_indent'] = py_line[0].length
                if (len(py_line) > 1) and isinstance(py_line[1], DocStringToken):
                    inside_fc[-1]['sub_struct']['notes'].append(py_line[1].content)

        '''
        treating block-leave out of "def"/"class"
        =========================================
        '''
        if (len(py_line) > 1) and (not isinstance(py_line[1], CommentToken)):
            repeat: bool = True
            while repeat:
                repeat = False
                if len(inside_fc) > 0:
                    if inside_fc[-1]['sub_struct']['base_indent'] > py_line[0].length:
                        inside_fc.pop()
                        repeat = True

        '''
        treating top-level doc-strings
        ==============================
        '''
        if len(inside_fc) == 0:
            tkn_nos = has_token_after(py_line, DocStringToken, -1)
            ignore: bool = False
            if isinstance(py_line[-1], CommentToken) and ('<tomarkdown:IGNORE>' in py_line[-1].content): ignore = True
            for tkn_no in tkn_nos:
                struct.append(dict(kind = 'docstring',
                                   note = py_line[tkn_no].content,
                                   ignore = ignore))

        '''
        treating block-entering into "def"/"class", i.e. treating functions/classes
        ===========================================================================
        '''
        num_func: int = len(has_token_after(py_line, DefToken, -1))
        num_clas: int = len(has_token_after(py_line, ClassToken, -1))
        if num_func + num_clas > 1: raise AssertionError(f'[err:{line_no}] many class/def declarations on one line!')
        if num_func + num_clas == 1:
            is_func: bool = (num_func == 1)
            if is_func: token_name_no = has_token_after(py_line, DefToken, -1)[0] + 1
            else: token_name_no = has_token_after(py_line, ClassToken, -1)[0] + 1
            name: str = py_line[token_name_no].word

            forward_break: bool = False
            new_line: list[Token] = list(py_line)
            while (colon_pos := _conditioned_colon_check(line_no, new_line)) is False:
                if (py_line_no := py_line_no + 1) >= len(py_lines): forward_break = True; break
                py_line = py_lines[py_line_no]
                if isinstance(py_line[-1], CommentToken): new_line.extend(py_line[:-1])
                else: new_line.extend(py_line)
            if forward_break: break
            py_line = new_line
            is_inline: bool = (len(py_line) - colon_pos) != 1
            if isinstance(py_line[-1], CommentToken): is_inline = (len(py_line) - colon_pos) != 2

            ignore: bool = False
            if isinstance(py_line[-1], CommentToken) and ('<tomarkdown:IGNORE>' in py_line[-1].content): ignore = True
            sub_struct: dict[str, Any] = dict(name = name,
                                              kind = 'function' if is_func else 'class',
                                              notes = [],
                                              base_indent = 'x',
                                              ignore = ignore,
                                              deco_stack = deco_stack,
                                              declaration = token_line_to_str(py_line, skip_indent = True),
                                              functions = [],
                                              classes = [],
                                              child_of = None)
            if len(inside_fc) > 0:
                if is_func: inside_fc[-1]['sub_struct']['functions'].append(sub_struct)
                else: inside_fc[-1]['sub_struct']['classes'].append(sub_struct)
                sub_struct['ignore'] = sub_struct['ignore'] or inside_fc[-1]['sub_struct']['ignore']
                sub_struct['child_of'] = inside_fc[-1]['sub_struct']
            else: struct.append(sub_struct)
            if not is_inline:
                inside_fc.append(dict(name = None, sub_struct = dict()))
                inside_fc[-1]['name'] = sub_struct['name']
                inside_fc[-1]['sub_struct'] = sub_struct
            continue

        '''
        treating decorators
        ===================
        '''
        if len(has_token_after(py_line, DecoratorToken, -1)) > 0:
            if len(has_token_after(py_line, DecoratorToken, -1)) > 1:
                raise AssertionError(f'[err:{line_no}] multiple decorator in a line!')
            deco_stack.append(token_line_to_str(py_line, skip_indent = True))
        else: deco_stack = []

    return struct


def _mod_name(name: str) -> str:
    return '\_'.join(name.split('_'))


def prime_note_normalization(content: str):
    prime_note: str = ''
    for row in content.split('\n'):
        indent = len(row) - len(row.lstrip(' '))
        actual_indent = indent
        if indent >= 4: indent //= 2
        small_tab = 2*' '
        prime_note += small_tab*(indent//2) + row[actual_indent:] + '\n'
    return prime_note


def _to_md(name: str,
           sub_struct: dict,
           parent_struct: dict | None = None,
           *,
           out: dict[str, str]) -> None:
    if sub_struct['ignore']: return None

    if parent_struct is None: parent_struct = dict(kind = None, name = '', child_of = None)

    add_in: str = '  '
    if sub_struct['kind'] == 'class': add_in = '▸ '
    elif not (parent_struct['kind'] is None): add_in = '▹ '

    prime_note: str = ''
    if len(sub_struct['notes']) > 0: prime_note = prime_note_normalization(sub_struct['notes'][0])

    class_class_short: str = _mod_name(sub_struct['name'])
    if (parent_struct['kind'] == 'class') and (sub_struct['kind'] == 'class'):
        class_class_short = f'[...].{_mod_name(sub_struct["name"])}'
    elif parent_struct['kind'] == 'class':
        class_class_short = f'{_mod_name(parent_struct["name"])}.{_mod_name(sub_struct["name"])}'

    content: str = f'''
{add_in}{class_class_short}
-----'''

    _name = '.'.join(name.split('.')[:-1])
    class_class_short_toplvl: str = ''
    if (parent_struct['kind'] == 'class') and (sub_struct['kind'] == 'class'):
        if parent_struct['child_of'] is None: class_class_short_toplvl += _mod_name(parent_struct["name"])
        else: class_class_short_toplvl += f'[...].{_mod_name(parent_struct["name"])}'
        content += f'\n\n**member of:** [{class_class_short_toplvl}]({_name}.md)\n'
    elif (parent_struct['kind'] == 'function') and (sub_struct['kind'] == 'class'):
        class_class_short_toplvl = _mod_name(parent_struct["name"])
        if isinstance(parent_struct['child_of'], dict) and (parent_struct['child_of']['kind'] == 'class'):
            class_class_short_toplvl = f'{parent_struct["child_of"]["name"]}.{_mod_name(parent_struct["name"])}'
        content += f'\n\n**from within:** [{class_class_short_toplvl}]({_name}.md)\n'
    elif (parent_struct['kind'] == 'function') and (sub_struct['kind'] == 'function'):
        class_class_short_toplvl = _mod_name(parent_struct["name"])
        if isinstance(parent_struct['child_of'], dict) and (parent_struct['child_of']['kind'] == 'class'):
            class_class_short_toplvl = f'{parent_struct["child_of"]["name"]}.{_mod_name(parent_struct["name"])}'
        content += f'\n\n**from within:** {class_class_short_toplvl}\n'
    del class_class_short_toplvl

    content += f'''
**declaration**

```python'''

    for deco in sub_struct['deco_stack']: content += f'\n{deco}'

    content += f'''
{str(sub_struct['declaration'])}
```

{prime_note}
'''
    vis_cls: int = 0  # vis_cls - number of visible classes
    for cls in sub_struct['classes']:
        if not cls['ignore']: vis_cls += 1
    if vis_cls > 0:
        content += f'''
**member classes:**
'''
        for cls in sub_struct['classes']:
            if not cls['ignore']:
                content += f'\n  - ▸ [{class_class_short}.{_mod_name(cls["name"])}]({name}.{sub_struct["name"]}.md)'
        content += '\n\n'

    vis_func: int = 0
    for func in sub_struct['functions']:
        if not func['ignore']: vis_func += 1
    if vis_func > 0:
        content += f'''
??? abstract "member functions"
'''
        for func in sub_struct['functions']:
            if not func['ignore']: content += f'\n    ▹ {class_class_short}.{_mod_name(func["name"])}\n'

    content += '\n-----'

    if not (name in out): out[name] = ''
    out[name] += content

    for func in sub_struct['functions']:
        if not func['ignore']: _to_md(name, func, sub_struct, out = out)
    for clas in sub_struct['classes']:
        if not clas['ignore']: _to_md(f"{name}.{sub_struct['name']}", clas, sub_struct, out = out)


def yaml_to_md(name_of_md_file: str, struct: dict, out: dict[str, str] | None = None):
    if out is None: out: dict[str, str] = dict()
    if not (name_of_md_file in out): out[name_of_md_file] = ''

    for entry in struct:
        if (entry['kind'] == 'docstring') and (not entry['ignore']):
            out[name_of_md_file] += f'''
{prime_note_normalization(entry['note'])}

-----
'''
        elif (entry['kind'] in ('class', 'function')) and (not entry['ignore']):
            _to_md(name_of_md_file, entry, out = out)

    return out
