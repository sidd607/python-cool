def indent(string, level=1, lstrip_first=False):
    """Multiline string indent.
    
    Indent each line of the provided string by the specified level.

    Args:
        string: The string to indent, possibly containing linebreaks.
        level: The level to indent (``level * '  '``). Defaults to 1.
        lstrip_first: If this is `True`, then the first line is not indented.
            Defaults to `False`.

    Returns:
        Indented string.
    
    """
    out = '\n'.join((level * '  ') + i for i in string.splitlines())
    if lstrip_first:
        return out.lstrip()
    return out


def is_namedtuple(x):
    """Return whether ``x`` is an instance of a namedtuple."""
    return isinstance(x, tuple) and hasattr(x, '_fields')


def print_ast(tree, level=0, inline=False):
    """Recursive function to print the AST.
    
    Args:
        tree: An abstract syntax tree consisting of tuples, namedtuples and other objects.
        level: The indent level, used for the recursive calls.
        inline: Whether or not to indent the first line.
        
    Returns:
        Nothing. The AST is printed directly to stdout.
        
    """

    if is_namedtuple(tree):

        print(indent('{0.__class__.__name__}('.format(tree), level, inline))
        for key, value in tree._asdict().items():
            print(indent(key + '=', level + 1), end='')
            print_ast(value, level + 1, True)
        print(indent(')', level))

    elif isinstance(tree, (tuple, list)):

        if isinstance(tree, tuple):
            braces = '()'
        else:
            braces = '[]'

        if len(tree) == 0:
            print(braces)
        else:
            print(indent(braces[0], level, inline))
            for obj in tree:
                print_ast(obj, level + 1)
            print(indent(braces[1], level))

    else:

        print(indent(repr(tree), level, inline))
