import os
import re
from pathlib import Path
from typing import List, Optional, Tuple

# fmt: off
#Black / isort are broken here :)
from ceader import get_logger
from ceader.domain.knowledge.extensions_to_language import \
    EXTENSION_TO_PROGRAMMING_LANGUAGE_MAPPING
from ceader.domain.knowledge.language_to_comment import (
    COMPUTER_LANGUAGE_TO_COMMENT_DATA_MAPPING, CommentData)
# fmt: on
from ceader.domain.types.enums import CeaderStatus, ComputerLanguage
from ceader.domain.utils import get_file_lines

logger = get_logger()


class HeaderProcedure:
    def __init__(self) -> None:
        pass

    def add_header(
        self,
        filepath: Path,
        header_path: Path,
        prefer_multiline_comment: bool,
        debug: bool,
    ) -> CeaderStatus:
        cl = _understand_computer_language(filepath, debug)
        if cl is None:
            return CeaderStatus.FAILURE

        cm_data = _get_comment_data(cl)

        header_lines = self._create_header_lines(
            header_path=header_path,
            comment_data=cm_data,
            prefer_multiline_comment=prefer_multiline_comment,
        )

        if len(header_lines) == 0:
            raise ValueError("Header file is empty!")

        header_lines_in_file = self._get_header_lines_inside_file(
            filepath=filepath, header_lines=header_lines
        )

        if header_lines_in_file is None:
            self._add_header_to_file(filepath, header_lines)

        else:
            return CeaderStatus.SKIPPED

        return CeaderStatus.SUCCESS

    def remove_header(
        self,
        filepath: Path,
        header_path: Path,
        prefer_multiline_comment: bool,
        debug: bool,
    ) -> CeaderStatus:
        cl = _understand_computer_language(filepath, debug)
        if cl is None:
            return CeaderStatus.FAILURE

        cm_data = _get_comment_data(cl)

        header_lines = self._create_header_lines(
            header_path=header_path,
            comment_data=cm_data,
            prefer_multiline_comment=prefer_multiline_comment,
        )

        if len(header_lines) == 0:
            raise ValueError("Header file is empty!")
        header_lines_in_file = self._get_header_lines_inside_file(
            filepath=filepath, header_lines=header_lines
        )
        if header_lines_in_file is not None:
            self._remove_header_from_file(filepath, header_lines_in_file)
        else:
            CeaderStatus.SKIPPED

        return CeaderStatus.SUCCESS

    def _print_lines(self, header_lines: List[str]) -> None:
        print("lines in total:", len(header_lines))
        for l in header_lines:
            print(l.replace("\n", ""))
        print()

    def _create_header_lines(
        self,
        header_path: Path,
        comment_data: CommentData,
        prefer_multiline_comment: bool,
    ) -> List[str]:
        """
        Reading header file + adding comments
        """

        def get_header_lines(header_path: Path) -> List[str]:
            return get_file_lines(header_path)

        def use_single_line_comment_method(
            single_line_comment: str, lines: List[str]
        ) -> List[str]:

            for i, line in enumerate(lines):
                lines[i] = single_line_comment + line
            return lines

        def use_multi_line_comment_method(
            multi_line_comment: Tuple[str, str], lines: List[str]
        ) -> List[str]:
            return (
                [multi_line_comment[0] + "\n"] + lines + [multi_line_comment[1] + "\n"]
            )

        header_lines = get_header_lines(header_path)
        if not prefer_multiline_comment:
            if comment_data.single_line_comment is not None:
                ceader_lines = use_single_line_comment_method(
                    single_line_comment=comment_data.single_line_comment,
                    lines=header_lines,
                )
            elif comment_data.multi_line_comment is not None:
                ceader_lines = use_multi_line_comment_method(
                    multi_line_comment=comment_data.multi_line_comment,
                    lines=header_lines,
                )
            else:
                raise ValueError("Something wrong with CommentData")
            return ceader_lines

        else:

            if comment_data.multi_line_comment is not None:
                ceader_lines = use_multi_line_comment_method(
                    multi_line_comment=comment_data.multi_line_comment,
                    lines=header_lines,
                )
            elif comment_data.single_line_comment is not None:
                ceader_lines = use_single_line_comment_method(
                    single_line_comment=comment_data.single_line_comment,
                    lines=header_lines,
                )
            else:
                raise ValueError("Something wrong with CommentData")
            return ceader_lines

    def _add_header_to_file(self, filepath: Path, lines_to_add: List[str]) -> None:
        """Insert given lines as a new lines at the beginning of a file"""
        # TODO

        # define name of temporary dummy file
        dummy_file = filepath.stem + ".bak"
        # open original file in read mode and dummy file in write mode

        # TODO move to fun add_to_stringIO(StringIO, lines_to_add)
        with open(filepath, "r") as read_obj, open(dummy_file, "w") as write_obj:
            # Write given line to the dummy file
            for line in lines_to_add:
                write_obj.write(line)
            # Read lines from original file one by one and append them to the dummy file
            for line in read_obj:
                write_obj.write(line)

        # remove original file
        os.remove(filepath)
        # Rename dummy file as the original file
        os.rename(dummy_file, filepath)
        read_obj.close()
        write_obj.close()

    def _remove_header_from_file(
        self, filepath: Path, lines_to_remove: Tuple[int, int]
    ) -> None:
        """Remove given lines from file"""
        # header lines
        first_line = lines_to_remove[0]
        last_line = lines_to_remove[1]
        # define name of temporary dummy file
        dummy_file = filepath.stem + ".bak"
        # open original file in read mode and dummy file in write mode
        with open(filepath, "r") as read_obj, open(dummy_file, "w") as write_obj:
            # Read lines from original file one by one and append them to the dummy file
            for i, line in enumerate(read_obj):
                if not (i >= first_line and i <= last_line):
                    write_obj.write(line)
        # remove original file
        os.remove(filepath)
        # Rename dummy file as the original file
        os.rename(dummy_file, filepath)
        read_obj.close()
        write_obj.close()

    def _get_header_lines_inside_file(
        self, filepath: Path, header_lines: List[str]
    ) -> Optional[Tuple[int, int]]:
        """
        If header is already in file - return number of lines
        If header is not in file - return None
        """

        def get_file_lines(filepath: Path) -> List[str]:
            file = open(filepath, "r")
            file_lines = file.readlines()
            file.close()

            return file_lines

        file_lines = get_file_lines(filepath)

        first_line: Optional[int] = None
        last_line: Optional[int] = None
        correct_line_counter = 0

        for i, line in enumerate(file_lines):
            if first_line is None and re.search("^\s*$", line):
                # ignoring all blank lines
                continue
            else:
                if first_line is None:
                    first_line = i
                if line.replace(" ", "") == header_lines[correct_line_counter].replace(
                    " ", ""
                ):  # TODO QUICK FIX - Make lint removes/adds spaces sometimes!
                    correct_line_counter += 1
                else:  # lines are different
                    return None

                if correct_line_counter == len(
                    header_lines
                ):  # if last line was good, return Tuple
                    last_line = i
                    return first_line, last_line
        return None


def _understand_computer_language(
    filepath: Path, debug: bool
) -> Optional[ComputerLanguage]:
    suffix = filepath.suffix
    try:
        computer_language = EXTENSION_TO_PROGRAMMING_LANGUAGE_MAPPING[suffix]
    except:
        if debug:
            logger.warning(f"{filepath.stem} has unknown suffix! {suffix}")
            return None

    return computer_language


def _get_comment_data(computer_language: ComputerLanguage) -> CommentData:
    try:
        cd = COMPUTER_LANGUAGE_TO_COMMENT_DATA_MAPPING[computer_language]
    except:
        raise ValueError(
            f"CommentData not found - add data for language: {computer_language.value}"
        )

    return cd
