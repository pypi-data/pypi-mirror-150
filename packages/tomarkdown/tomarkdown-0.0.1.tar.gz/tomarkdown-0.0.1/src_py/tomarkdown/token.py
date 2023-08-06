from typing import Union


class Token(object):
    line_no: int = None
    letter_no: int = None

    # fields of inheriting Token
    length: int = None
    content: str = None
    q_sym: str = None
    val: float | int = None
    word: str = None

    def __init__(self, line_no: int, letter_no: int):
        self.line_no = line_no
        self.letter_no = letter_no

    def __repr__(self) -> str: return f'{self.__class__.__name__}({self.line_no}, {self.letter_no})'

    def __len__(self) -> int: raise AssertionError('need to be overloaded!')


class IndentationToken(Token):
    def __init__(self, length: int, line_no: int):
        super().__init__(line_no = line_no, letter_no = -1)
        self.length = length

    def __repr__(self) -> str: return f'IndentationToken({self.length}, {self.line_no})'

    def __len__(self) -> int: return self.length


class StringToken(Token):
    def __init__(self, content: str, q_sym: str, line_no: int, letter_no: int):
        super().__init__(line_no = line_no, letter_no = letter_no)
        self.content = content
        self.q_sym = q_sym

    def __repr__(self) -> str:
        _content: str = '[...]'
        if len(self.content) <= 3: _content = repr(self.content)
        return f'StringToken({_content}, {repr(self.q_sym)}, {self.line_no}, {self.letter_no})'

    def __len__(self) -> int: return len(self.content) + 2  # 2 due to pair of ' or "


class DocStringToken(Token):
    def __init__(self, content: str, q_sym: str, line_no: int, letter_no: int):
        super().__init__(line_no = line_no, letter_no = letter_no)
        self.content = content
        self.q_sym = q_sym

    def __repr__(self) -> str:
        _content: str = '[...]'
        if len(self.content) <= 3: _content = repr(self.content)
        return f'DocStringToken({_content}, {repr(self.q_sym)}, {self.line_no}, {self.letter_no})'

    def __len__(self) -> int: return len(self.content) + 6  # 6 due to pair of triplets ''' or """


class CommentToken(Token):
    def __init__(self, content: str, line_no: int, letter_no: int):
        super().__init__(line_no = line_no, letter_no = letter_no)
        self.content = content

    def __repr__(self) -> str:
        _content: str = '[...]'
        if len(self.content) <= 3: _content = repr(self.content)
        return f'CommentToken({_content}, {self.line_no}, {self.letter_no})'

    def __len__(self) -> int: return len(self.content) + 1  # 1 due to leading '#'


class NumToken(Token):
    def __init__(self, val: str, line_no: int, letter_no: int):
        super().__init__(line_no = line_no, letter_no = letter_no)
        try: self.val = int(val)
        except: self.val = float(val)

    def __repr__(self) -> str: return f'NumToken({self.val}, {self.line_no}, {self.letter_no})'

    def __len__(self) -> int: return len(str(self.val))


class PreIdentToken(Token):  # Ident means identifier
    def __init__(self, word: str, line_no: int, letter_no: int):
        super().__init__(line_no = line_no, letter_no = letter_no)
        self.word = word

    def __repr__(self) -> str: return f'{self.__class__.__name__}({self.word}, {self.line_no}, {self.letter_no})'

    def __len__(self) -> int: return len(self.word)


class IdentToken(PreIdentToken): pass


class KeywordToken(PreIdentToken):  # Ident means identifier
    def __init__(self, line_no: int, letter_no: int):
        super().__init__(word = self.word, line_no = line_no, letter_no = letter_no)

    def __repr__(self) -> str: return f'{self.__class__.__name__}({self.line_no}, {self.letter_no})'


class DefToken(KeywordToken): word = 'def'
class ClassToken(KeywordToken): word = 'class'
class DecoratorToken(PreIdentToken): pass
class PassToken(KeywordToken): word = 'pass'


class EllipsisToken(KeywordToken): word = '...'


class FunctionalSymbolToken(KeywordToken): pass


class SeperatorToken(FunctionalSymbolToken): word = ','


class OperatorToken(KeywordToken): pass  # (both) sided; no whitespace
class OperatorTokenL(KeywordToken): pass  # R - Left sided; whitespace left
class OperatorTokenR(KeywordToken): pass  # R - Right sided; whitespace right
class OperatorTokenB(KeywordToken): pass  # B - Both sided; whitespace left and right
class OperatorTokenPM(KeywordToken): pass  # PM - Plus Minus


class AttribToken(OperatorToken): word = '.'


class ColonToken(OperatorTokenR): word = ':'
class AssignToken(OperatorTokenB): word = '='
class ArrowToken(OperatorTokenB): word = '->'


class LParamToken(OperatorTokenL): word = '('
class RParamToken(OperatorTokenR): word = ')'
class LBracToken(OperatorTokenL): word = '['
class RBracToken(OperatorTokenR): word = ']'
class LCurBToken(OperatorTokenL): word = '{'
class RCurBToken(OperatorTokenR): word = '}'


class AddAssignToken(OperatorTokenB): word = '+='
class SubAssignToken(OperatorTokenB): word = '-='
class MulAssignToken(OperatorTokenB): word = '*='
class TrueDivAssignToken(OperatorTokenB): word = '/='
class FloorDivAssignToken(OperatorTokenB): word = '//='
class MatMulAssignToken(OperatorTokenB): word = '@='
class ModuloAssignToken(OperatorTokenB): word = '%='
class EqToken(OperatorTokenB): word = '=='
class NeqToken(OperatorTokenB): word = '!='
class GeToken(OperatorTokenB): word = '>='
class LeToken(OperatorTokenB): word = '<='
class WalrusToken(OperatorTokenB): word = ':='
class AddToken(OperatorTokenPM): word = '+'
class SubToken(OperatorTokenPM): word = '-'
class MulToken(OperatorToken): word = '*'
class TrueDivToken(OperatorToken): word = '/'
class FloorDivToken(OperatorToken): word = '//'
class MatMulToken(OperatorToken): word = '@'
class ModuloToken(OperatorTokenB): word = '%'
class InvertToken(OperatorTokenL): word = '~'


class PowAssignToken(OperatorTokenB): word = '**='
class RShiftAssignToken(OperatorTokenB): word = '>>='
class LShiftAssignToken(OperatorTokenB): word = '<<='
class AndAssignToken(OperatorTokenB): word = '&='
class OrAssignToken(OperatorTokenB): word = '|='
class XOrAssignToken(OperatorTokenB): word = '^='
class PowToken(OperatorToken): word = '**'
class RShiftToken(OperatorTokenB): word = '>>'
class LShiftToken(OperatorTokenB): word = '<<'
class AndToken(OperatorTokenB): word = '&'
class OrToken(OperatorTokenB): word = '|'
class XOrToken(OperatorToken): word = '^'


def has_token_after(py_line: list[Token], TokenClass: type[Token], start: int = -1) -> list[int]:
    start += 1
    out: list[int] = []
    for idx, tkn in enumerate(py_line[start:]):
        if isinstance(tkn, TokenClass): out.append(start + idx)
    return out


def token_line_to_str(py_line: list[Token], skip_indent: bool = False) -> str:
    out: str = ''

    last_tkn: Token | None = None
    for idx, tkn in enumerate(py_line):
        if idx == 0:
            if not skip_indent: out += ' '*tkn.length
            continue

        if isinstance(tkn, StringToken):
            out += f'{tkn.q_sym}{tkn.content:s}{tkn.q_sym} '
        elif isinstance(tkn, DocStringToken):
            out += f'{tkn.q_sym*3}{tkn.content:s}{tkn.q_sym*3} '
        elif isinstance(tkn, CommentToken): out += f' #{tkn.content:s} '
        elif isinstance(tkn, NumToken): out += f'{tkn.val} '
        elif isinstance(tkn, SeperatorToken): out = out.rstrip() + f'{tkn.word} '
        elif isinstance(tkn, OperatorToken): out = out.rstrip() + f'{tkn.word}'
        elif isinstance(tkn, OperatorTokenL):
            if (not (last_tkn is None)) and isinstance(last_tkn, IdentToken): out = out.rstrip() + f'{tkn.word}'
            else: out += f'{tkn.word}'
        elif isinstance(tkn, OperatorTokenR): out = out.rstrip() + f'{tkn.word} '
        elif isinstance(tkn, OperatorTokenB): out += f'{tkn.word} '
        elif isinstance(tkn, OperatorTokenPM):
            if (idx == 0) or (not isinstance(py_line[idx - 1], (IdentToken, NumToken))):
                out += f'{tkn.word}'
            else: out += f'{tkn.word} '
        elif isinstance(tkn, DecoratorToken): out += f'@{tkn.word} '
        elif isinstance(tkn, KeywordToken): out += f'{tkn.word} '
        elif isinstance(tkn, IdentToken): out += f'{tkn.word} '
        elif isinstance(tkn, EllipsisToken): out += '... '

        last_tkn = tkn

    return out
