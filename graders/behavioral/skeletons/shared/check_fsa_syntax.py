"""
FSA Specification Syntax Checker

Validates the syntax of your specification.fsa file.
Run this before submitting to catch any syntax errors early.

Usage:
    py check_syntax.py                     # checks specification.fsa in the same directory
    py check_syntax.py path/to/file.fsa    # checks a specific file
"""

import os
import re
import sys


# ---------------------------------------------------------------------------
# Tokenizer
# ---------------------------------------------------------------------------

_PATTERNS = [
    ("SKIP",    re.compile(r"[ \t]+")),
    ("COMMENT", re.compile(r"#[^\n]*")),   # # ... to end of line
    ("NEWLINE", re.compile(r"\n")),
    ("STRING",  re.compile(r'"[^"\n]*"')),
    ("ARROW",   re.compile(r"->")),
    ("DASH",    re.compile(r"-")),
    ("COLON",   re.compile(r":")),
    ("COMMA",   re.compile(r",")),
    ("LBRACE",  re.compile(r"\{")),
    ("RBRACE",  re.compile(r"\}")),
    ("EQUAL",   re.compile(r"=")),
    ("EPSILON", re.compile(r"eps(?:ilon)?\b|\u03b5")),
    ("KEYWORD", re.compile(r"(?:alphabet|states|initial_state|accepting_states|transitions)\b")),
    ("ID",      re.compile(r"[A-Za-z_][A-Za-z0-9_]*|\d+")),
    ("UNKNOWN", re.compile(r".")),
]

_REQUIRED_SECTIONS = {"alphabet", "states", "initial_state", "accepting_states", "transitions"}


class _Token:
    __slots__ = ("kind", "value", "line", "col")

    def __init__(self, kind, value, line, col):
        self.kind = kind
        self.value = value
        self.line = line
        self.col = col


def _tokenize(text):
    tokens = []
    pos = 0
    line = 1
    line_start = 0
    n = len(text)
    while pos < n:
        for kind, pat in _PATTERNS:
            m = pat.match(text, pos)
            if not m:
                continue
            value = m.group()
            if kind in ("SKIP", "COMMENT"):
                pass
            elif kind == "NEWLINE":
                line += 1
                line_start = pos + 1
            else:
                col = pos - line_start + 1
                tokens.append(_Token(kind, value, line, col))
            pos = m.end()
            break
    return tokens


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class _Parser:
    def __init__(self, tokens, errors):
        self.tokens = tokens
        self.pos = 0
        self.errors = errors

    # --- primitives ---

    def _peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def _consume(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def _expect(self, kind, hint):
        tok = self._peek()
        if tok and tok.kind == kind:
            return self._consume()
        if tok:
            self.errors.append(f"Line {tok.line}, col {tok.col}: {hint}")
        else:
            self.errors.append(f"Unexpected end of file — {hint}")
        return None

    def _skip_to(self, *stop_kinds):
        """Advance until one of the stop tokens (for error recovery)."""
        while self._peek() and self._peek().kind not in stop_kinds:
            self._consume()

    # --- top-level ---

    def parse_file(self):
        found = set()
        while self._peek():
            tok = self._peek()
            if tok.kind == "KEYWORD":
                found.add(tok.value)
                self._consume()
                self._expect("COLON", f"expected ':' after '{tok.value}'")
                self._parse_section(tok.value)
            elif tok.kind == "ID":
                self.errors.append(
                    f"Line {tok.line}, col {tok.col}: unknown keyword '{tok.value}' "
                    f"(valid keywords: {', '.join(sorted(_REQUIRED_SECTIONS))})"
                )
                self._consume()
                # try to skip over whatever follows so we can keep checking
                while self._peek() and self._peek().kind not in ("KEYWORD", "ID"):
                    if self._peek().kind == "LBRACE":
                        self._skip_block()
                    else:
                        self._consume()
            else:
                self.errors.append(
                    f"Line {tok.line}, col {tok.col}: unexpected '{tok.value}'"
                )
                self._consume()

        for section in sorted(_REQUIRED_SECTIONS - found):
            self.errors.append(f"Missing required section: '{section}'")

    def _parse_section(self, section):
        tok = self._peek()
        if tok is None:
            self.errors.append(f"Unexpected end of file after '{section}:'")
            return

        if section == "initial_state":
            if tok.kind in ("ID", "KEYWORD"):
                self._consume()
            else:
                self.errors.append(
                    f"Line {tok.line}, col {tok.col}: "
                    f"expected a state name after 'initial_state:'"
                )
        elif section == "transitions":
            if tok.kind != "LBRACE":
                self.errors.append(
                    f"Line {tok.line}, col {tok.col}: expected '{{' after 'transitions:'"
                )
                return
            self._consume()
            self._parse_transitions()
            self._expect("RBRACE", "expected '}' to close 'transitions' block")
        else:
            if tok.kind != "LBRACE":
                self.errors.append(
                    f"Line {tok.line}, col {tok.col}: expected '{{' after '{section}:'"
                )
                return
            self._consume()
            if section == "states":
                self._parse_state_list()
            else:
                self._parse_id_list()
            self._expect("RBRACE", f"expected '}}' to close '{section}' block")

    def _parse_id_list(self):
        """Comma-separated IDs: item (COMMA item)* COMMA? — alphabet, accepting_states."""
        tok = self._peek()
        if tok is None or tok.kind == "RBRACE":
            return
        # first item
        if tok.kind in ("ID", "EPSILON", "KEYWORD"):
            self._consume()
        else:
            self.errors.append(
                f"Line {tok.line}, col {tok.col}: expected a symbol/state name, got '{tok.value}'"
            )
            self._consume()
            return
        # subsequent items — each must be preceded by a comma
        while self._peek() and self._peek().kind != "RBRACE":
            tok = self._peek()
            if tok.kind == "COMMA":
                self._consume()
                if self._peek() and self._peek().kind == "RBRACE":
                    break  # trailing comma OK
                tok = self._peek()
                if tok is None:
                    break
                if tok.kind in ("ID", "EPSILON", "KEYWORD"):
                    self._consume()
                else:
                    self.errors.append(
                        f"Line {tok.line}, col {tok.col}: expected a symbol/state name, got '{tok.value}'"
                    )
                    self._consume()
            else:
                self.errors.append(
                    f"Line {tok.line}, col {tok.col}: expected ',' before '{tok.value}'"
                )
                self._consume()  # consume item anyway for error recovery

    def _parse_state_list(self):
        """States: stateEntry (COMMA stateEntry)* COMMA?"""
        tok = self._peek()
        if tok is None or tok.kind == "RBRACE":
            return
        self._parse_single_state_entry()
        while self._peek() and self._peek().kind != "RBRACE":
            tok = self._peek()
            if tok.kind == "COMMA":
                self._consume()
                if self._peek() and self._peek().kind == "RBRACE":
                    break  # trailing comma OK
                self._parse_single_state_entry()
            else:
                self.errors.append(
                    f"Line {tok.line}, col {tok.col}: expected ',' before '{tok.value}'"
                )
                self._parse_single_state_entry()

    def _parse_single_state_entry(self):
        tok = self._peek()
        if tok is None or tok.kind == "RBRACE":
            return
        if tok.kind not in ("ID", "KEYWORD"):
            self.errors.append(
                f"Line {tok.line}, col {tok.col}: expected a state name, got '{tok.value}'"
            )
            self._consume()
            return
        self._consume()
        if self._peek() and self._peek().kind == "EQUAL":
            self._consume()
            ann = self._peek()
            if ann and ann.kind == "STRING":
                self._consume()
            else:
                ref = ann if ann else tok
                self.errors.append(
                    f"Line {ref.line}, col {ref.col}: expected a quoted string after '='"
                )

    def _parse_transitions(self):
        """Transitions: transition (COMMA transition)* COMMA?"""
        tok = self._peek()
        if tok is None or tok.kind == "RBRACE":
            return
        self._parse_single_transition()
        while self._peek() and self._peek().kind != "RBRACE":
            tok = self._peek()
            if tok.kind == "COMMA":
                self._consume()
                if self._peek() and self._peek().kind == "RBRACE":
                    break  # trailing comma OK
                self._parse_single_transition()
            else:
                self.errors.append(
                    f"Line {tok.line}, col {tok.col}: expected ',' before '{tok.value}'"
                )
                self._parse_single_transition()

    def _parse_single_transition(self):
        """Parse one transition: ID -symbol-> ID."""
        tok = self._peek()
        if tok is None or tok.kind == "RBRACE":
            return

        if tok.kind not in ("ID", "KEYWORD"):
            self.errors.append(
                f"Line {tok.line}, col {tok.col}: "
                f"expected a state name to start a transition, got '{tok.value}'"
            )
            self._skip_to("COMMA", "RBRACE")
            return

        src = self._consume()

        dash = self._peek()
        if not dash or dash.kind != "DASH":
            got = f"'{dash.value}'" if dash else "end of file"
            self.errors.append(
                f"Line {src.line}: expected '-' after '{src.value}' "
                f"(transition format: state -symbol-> state), got {got}"
            )
            self._skip_to("COMMA", "RBRACE")
            return
        self._consume()

        sym = self._peek()
        if not sym or sym.kind not in ("ID", "EPSILON", "KEYWORD"):
            got = f"'{sym.value}'" if sym else "end of file"
            self.errors.append(
                f"Line {src.line}: expected a transition symbol after '-', got {got}"
            )
            self._skip_to("COMMA", "RBRACE")
            return
        self._consume()

        arrow = self._peek()
        if not arrow or arrow.kind != "ARROW":
            got = f"'{arrow.value}'" if arrow else "end of file"
            self.errors.append(
                f"Line {src.line}: expected '->' after transition symbol, got {got} "
                f"(transition format: state -symbol-> state)"
            )
            self._skip_to("COMMA", "RBRACE")
            return
        self._consume()

        dst = self._peek()
        if not dst or dst.kind not in ("ID", "KEYWORD"):
            got = f"'{dst.value}'" if dst else "end of file"
            self.errors.append(
                f"Line {src.line}: expected a destination state after '->', got {got}"
            )
            self._skip_to("COMMA", "RBRACE")
            return
        self._consume()

    def _skip_block(self):
        depth = 0
        while self._peek():
            tok = self._consume()
            if tok.kind == "LBRACE":
                depth += 1
            elif tok.kind == "RBRACE":
                depth -= 1
                if depth == 0:
                    break


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def check_fsa_syntax(path):
    """Return a list of error strings. Empty list means the file is valid."""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    tokens = _tokenize(content)
    errors = []
    _Parser(tokens, errors).parse_file()
    return errors


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) > 1:
        fsa_path = sys.argv[1]
    else:
        fsa_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "specification.fsa")

    if not os.path.isfile(fsa_path):
        print(f"Error: file not found: {fsa_path}")
        print("Usage: py check_syntax.py [path/to/specification.fsa]")
        sys.exit(1)

    print(f"Checking {os.path.basename(fsa_path)}...")
    print()

    errors = check_fsa_syntax(fsa_path)

    if not errors:
        print("Syntax OK -- no errors found.")
    else:
        print(f"Found {len(errors)} syntax error(s):\n")
        for err in errors:
            print(f"  {err}")
        print()
        print("Fix the errors above and run this script again.")
        sys.exit(1)


if __name__ == "__main__":
    main()
