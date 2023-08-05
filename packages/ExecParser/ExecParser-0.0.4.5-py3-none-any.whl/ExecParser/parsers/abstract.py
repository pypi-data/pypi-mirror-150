from abc import ABCMeta, abstractmethod
import lief


class UnknownFormat(TypeError):
    pass


class AbstractExecutable(object):
    __metaclass__ = ABCMeta

    _instance = None

    def __new__(cls, exec_file):
        if lief.EXE_FORMATS.UNKNOWN == lief.parse(exec_file).format:
            raise UnknownFormat(exec_file)

    def __init__(self, exec_file):
        self.binary = lief.parse(exec_file)

    @abstractmethod
    def basic_check(self):
        pass

    @abstractmethod
    def print_header(self):
        pass

    @abstractmethod
    def print_segments(self):
        pass

    @abstractmethod
    def print_segment_info(self, segment_name):
        pass

    def print_sections(self):
        print(f"{'NAME':<15}{'OFFSET':<15}{'SIZE':<15}{'ENTROPY':<15}")
        for section in self.binary.sections:
            print(f"{section.name:<15}{section.offset:<15}{section.size:<15}{section.entropy:<15}")

    @abstractmethod
    def print_section_info(self, section_name):
        pass

    @abstractmethod
    def get_hex(self):
        pass
