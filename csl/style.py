"""
A CSL Style
"""

class Info:
    """
    >>> info = Info()
    >>> info.title = "ABC Style"
    >>> print(info.title)
    ABC Style
    >>> info.add_category('author-date')
    >>> print(info.categories[0])
    author-date
    """
    def __init__(self, title=None, uri=None, updated=None, categories=None):
        self.title = title
        self.uri = uri
        self.updated = updated
        self.categories = categories or []

    def add_category(self, category):
        """
        adds a category to the categories list
        """
        self.categories.append(category)


class Option:
    """
    >>> option = Option('et-al-min', '4')
    >>> print(option.value)
    4
    """
    def __init__(self, name, value):
        self.name = name
        self.value = value


class Context:
    """
    >>> context = Context()
    >>> len(context.options)
    0
    >>> context.add_option('et-al-min', 5)
    >>> len(context.options)
    1
    """
    def __init__(self, options=None, sort=None, layout=None):
        self.options = options or []
        self.sort = sort or []
        self.layout = layout or []

    def add_option(self, name, value):
        """
        adds an option to the options list
        """
        self.options.append(Option(name, value))


class Template:
    """
    A collection of CSL processing instructions.
    """
    def __init__(self, name=None, content=None):
        self.name = name
        self.content = content


class Style:
    """
    >>> style = Style()
    >>> print(style.info)
    None
    """
    def __init__(self, info=None, macros=None, 
                 citation=None, bibliography=None):
        self.info = info
        self.macros = macros or []
        self.citation = citation
        self.bibliography = bibliography


