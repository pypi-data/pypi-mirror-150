import lief
import logging
import ExecParser.parsers.abstract as abstract


class NotELFFormat(TypeError):
    pass


class ELFParser(abstract.AbstractExecutable):

    def __new__(cls, exec_file: object) -> object:
        if lief.EXE_FORMATS.ELF != lief.parse(exec_file).format:
            raise NotELFFormat(exec_file)
        if not cls._instance:
            cls._instance = object.__new__(cls)
            logging.debug("ELFParser instance created")
        return cls._instance

    def __init__(self, exec_file):
        super().__init__(exec_file)
        self.format = 'ELF'
        logging.debug("ELFParser instance initialized")

    def basic_check(self):
        pass

    def print_header(self) -> None:
        _ = self.binary.header
        print(f"{'identity':<25}", _.identity)
        print(f"{'identity_class':<25}", _.identity_class)
        print(f"{'identity_data':<25}", _.identity_data)
        print(f"{'identity_os_abi':<25}", _.identity_os_abi)
        print(f"{'identity_abi_version':<25}", _.identity_abi_version)
        print(f"{'file_type':<25}", _.file_type)
        print(f"{'machine_type':<25}", _.machine_type)
        print(f"{'object_file_version':<25}", _.object_file_version)
        print(f"{'entrypoint':<25}", _.entrypoint)
        print(f"{'program_header_offset':<25}", _.program_header_offset)
        print(f"{'identity_version':<25}", _.identity_version)
        print(f"{'section_header_offset':<25}", _.section_header_offset)
        print(f"{'processor_flag':<25}", _.processor_flag)
        if _.processor_flag != 0:
            print(f"{'hexagon_flags_list':<25}", _.hexagon_flags_list)
            print(f"{'arm_flags_list':<25}", _.arm_flags_list)
            print(f"{'ppc64_flags_list':<25}", _.ppc64_flags_list)
            print(f"{'mips_flags_list':<25}", _.mips_flags_list)
        print(f"{'header_size':<25}", _.header_size)
        print(f"{'program_header_size':<25}", _.program_header_size)
        print(f"{'section_header_size':<25}", _.section_header_size)
        print(f"{'numberof_segments':<25}", _.numberof_segments)
        print(f"{'numberof_sections':<25}", _.numberof_sections)
        print(f"{'section_header_size':<25}", _.section_header_size)
        print(f"{'section_name_table_idx':<25}", _.section_name_table_idx)

    def print_segments(self):
        print(f"{'TYPE':<15}{'FLAGS':<15}")
        for segment in self.binary.segments:
            print(f"{segment.type.name:<15}{segment.flags.name:<15}")

    def print_segment_info(self, segment_name: str) -> None:
        ans = input("There are no way to show specific segments. Show all? (y/n): ")
        if ans.lower() == 'y':
            logging.warning("There are no way to show specific segments. Showing all")
            for segment in self.binary.segments:
                print(f"{'type':<25}", segment.type.name)
                print(f"{'flags':<25}", segment.flags.name)
                print(f"{'file_offset':<25}", segment.file_offset)
                print(f"{'alignment':<25}", segment.alignment)
                print(f"{'physical_address':<25}", segment.physical_address)
                print(f"{'physical_size':<25}", segment.physical_size)
                print(f"{'virtual_address':<25}", segment.virtual_address)
                print(f"{'virtual_size':<25}", segment.virtual_size)
                print(f"{'sections:':<25}")
                for section in segment.sections:
                    print(f"{section.name:>27}")
                print('-'*30, end='\n\n')
        else:
            pass

    def print_section_info(self, section_name: str) -> None:
        try:
            section = self.binary.get_section(section_name)
        except lief.not_found as e:
            logging.error(e)
            return None
        print(dir(section))
        print(f"{'name':<25}", section.name)
        print(f"{'name_idx':<25}", section.name_idx)
        print(f"{'type':<25}", section.type.name)
        print(f"{'entropy':<25}", section.entropy)
        print(f"{'flags':<25}", section.flags)
        if section.flags != 0:
            print(f"{'flags_list':<25}", list(map(lambda x: x.name, section.flags_list)))
        print(f"{'virtual_address':<25}", section.virtual_address)
        print(f"{'offset':<25}", section.offset)
        print(f"{'file_offset':<25}", section.file_offset)
        print(f"{'size':<25}", section.size)
        print(f"{'original_size':<25}", section.original_size)
        print(f"{'link':<25}", section.link)
        print(f"{'information':<25}", section.information)
        print(f"{'alignment':<25}", section.alignment)
        print(f"{'entry_size':<25}", section.entry_size)
