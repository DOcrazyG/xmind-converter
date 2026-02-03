"""Exception definitions"""


class XMindConverterError(Exception):
    """XMind converter base exception"""
    pass


class XMindParserError(XMindConverterError):
    """XMind parsing exception"""
    pass


class ConverterError(XMindConverterError):
    """Conversion exception"""
    pass


class FileFormatError(XMindConverterError):
    """File format exception"""
    pass


class FileNotFoundError(XMindConverterError):
    """File not found exception"""
    pass