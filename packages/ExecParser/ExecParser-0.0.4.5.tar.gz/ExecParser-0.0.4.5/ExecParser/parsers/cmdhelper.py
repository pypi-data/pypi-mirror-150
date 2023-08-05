from ExecParser import logger
from ExecParser.parsers.pe_parser import PEParser, NotPEFormat
from ExecParser.parsers.macho_parser import MachOParser, NotMacOFormat
from ExecParser.parsers.abstract import UnknownFormat


ALL_PARSERS = [PEParser, MachOParser]


class CmdHelper(object):

    def __init__(self):
        self.my_parser = None

    def process(self, args):
        self.guess_filetype(args)
        logger.info(f"Assuming your file is a {self.my_parser.format}")

        if args.header:
            self.my_parser.print_header()

        elif args.segments:
            self.my_parser.print_segments()

        elif args.segment_info:
            self.my_parser.print_segment_info(args.segment_info)

        elif args.sections:
            self.my_parser.print_sections()

        elif args.section_info:
            self.my_parser.print_section_info(args.section_info)

    def guess_filetype(self, args):
        logger.debug("Determining executable file type.")
        for iter_parser in ALL_PARSERS:
            try:
                logger.debug(f"Trying {iter_parser}")
                self.my_parser = iter_parser(args.exec_file)
            except NotPEFormat:
                logger.debug(f"{args.exec_file} is not a PE")
                continue
            except NotMacOFormat:
                logger.debug(f"{args.exec_file} is not a Mach-O")
                continue
            except UnknownFormat:
                logger.error(f"{args.exec_file} is not executable")
                return None
            break
