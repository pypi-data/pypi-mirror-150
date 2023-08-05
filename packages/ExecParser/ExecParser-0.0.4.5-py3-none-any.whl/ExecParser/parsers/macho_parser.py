import lief
import logging
import ExecParser.parsers.abstract as abstract


class NotMacOFormat(TypeError):
    pass


class MachOParser(abstract.AbstractExecutable):

    def __new__(cls, exec_file: object) -> object:
        if lief.EXE_FORMATS.MACHO != lief.parse(exec_file).format:
            raise NotMacOFormat(exec_file)
        if not cls._instance:
            cls._instance = object.__new__(cls)
            logging.debug("MachOParser instance created")
        return cls._instance

    def __init__(self, exec_file):
        super().__init__(exec_file)
        self.format = 'MACHO'
        logging.debug("MachOParser instance initialized")

    def basic_check(self):
        pass

    def print_header(self) -> None:
        _ = self.binary.header
        print(f"{'magic':<25}", _.magic)
        print(f"{'cpu_type':<25}", _.cpu_type)
        print(f"{'cpu_subtype':<25}", _.cpu_subtype)
        print(f"{'file_type':<25}", _.file_type)
        print(f"{'nb_cmds':<25}", _.nb_cmds)
        print(f"{'sizeof_cmds':<25}", _.sizeof_cmds)
        print(f"{'flags':<25}", _.flags)
        if _.flags != 0:
            print(f"{'flags_list':<25}", _.flags_list)
        print(f"{'reserved':<25}", _.reserved)

    def print_segments(self):
        print(f"{'NAME':<15}{'FLAGS':<15}{'SIZE':<15}{'NUMBER_OF_SECTIONS':<21}{'CMD':<15}")
        for segment in self.binary.segments:
            print(f"{segment.name:<15}{segment.flags:<15}{segment.size:<15}{segment.numberof_sections:<20}",
                  segment.command)

    def print_segment_info(self, segment_name: str) -> None:
        try:
            segment = self.binary.get_segment(segment_name)
        except lief.not_found as e:
            logging.error(e)
            return None
        print(f"{'cmd':<25}", segment.command)
        print(f"{'cmdsize':<25}", segment.command_offset)
        print(f"{'segname':<25}", segment.name)
        print(f"{'vmaddr':<25}", segment.virtual_address)
        print(f"{'vmsize':<25}", segment.virtual_size)
        print(f"{'fileoff':<25}", segment.file_offset)
        print(f"{'filesize':<25}", segment.file_size)
        print(f"{'maxprot':<25}", segment.max_protection)
        print(f"{'initprot':<25}", segment.init_protection)
        print(f"{'nsects':<25}", segment.numberof_sections)
        if segment.numberof_sections != 0:
            print(f"{'sections:':<25}")
            for it in range(segment.numberof_sections):
                print(f"{segment.sections[it].name:>27}")
        print(f"{'flags':<25}", segment.flags)

    def print_section_info(self, section_name: str) -> None:
        try:
            section = self.binary.get_section(section_name)
        except lief.not_found as e:
            logging.error(e)
            return None
        print(f"{'name':<25}", section.name)
        print(f"{'size':<25}", section.size)
        print(f"{'type':<25}", section.type)
        print(f"{'alignment':<25}", section.alignment)
        print(f"{'offset':<25}", section.offset)
        print(f"{'flags':<25}", section.flags)
        if section.flags != 0:
            print(f"{'flags_list':<15}", section.flags_list)
        print(f"{'numberof_relocations':<25}", section.numberof_relocations)
        if section.numberof_relocations != 0:
            for it in range(section.numberof_relocations):
                print(f"{'relocations':<25}", section.relocations[it])
            print(f"{'relocation_offset':<25}", section.relocation_offset)
        print(f"{'entropy':<25}", section.entropy)
        print(f"{'virtual_address':<25}", section.virtual_address)
        print(f"{'reserved1':<25}", section.reserved1)
        print(f"{'reserved2':<25}", section.reserved2)
        print(f"{'reserved3':<25}", section.reserved3)

    def get_hex(self):
        pass


