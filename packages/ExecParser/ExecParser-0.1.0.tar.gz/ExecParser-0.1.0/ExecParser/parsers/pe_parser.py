import lief
import logging
import ExecParser.parsers.abstract as abstract


class NotPEFormat(TypeError):
    pass


class PEParser(abstract.AbstractExecutable):

    def __new__(cls, exec_file):
        if lief.EXE_FORMATS.PE != lief.parse(exec_file).format:
            raise NotPEFormat(exec_file)
        if not cls._instance:
            cls._instance = object.__new__(cls)
            logging.debug("PEParser instance created")
        return cls._instance

    def __init__(self, exec_file):
        super().__init__(exec_file)
        self.format = 'PE'
        logging.debug("PEParser instance initialized")

    def basic_check(self):
        pass

    def print_header(self):
        pass

    def print_segments(self):
        pass

    def print_segment_info(self):
        pass

    def print_sections(self):
        pass

    def get_hex(self):
        pass
