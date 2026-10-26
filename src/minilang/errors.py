class MiniLangError(Exception):
    """Base exception for MiniLang."""


class LexerError(MiniLangError):
    pass


class ParserError(MiniLangError):
    pass


class RuntimeExecutionError(MiniLangError):
    pass
