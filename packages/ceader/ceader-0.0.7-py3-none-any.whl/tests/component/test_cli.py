# fmt: off
import sys
import tempfile
from pathlib import Path

import pytest

from ceader.__main__ import run_cli
from ceader.domain.knowledge.extensions_to_language import \
    EXTENSION_TO_PROGRAMMING_LANGUAGE_MAPPING
from ceader.domain.utils import get_file_lines
from tests import TEST_HEADER_PATH


# fmt: on
def test_cli_add_header() -> None:

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)
        assert (len(get_file_lines(Path(file_1.name)))) == 0

        sys.argv = [
            "--foo",  # to make sure that test works. We ignore first argv using MakeFile
            "--mode",
            "add_header",
            "--files",
            str(tmpdirname),
            "--header-path",
            str(TEST_HEADER_PATH.resolve()),
            "--extensions",
            ".py",
            "--debug",
        ]
        run_cli()
        assert (len(get_file_lines(Path(file_1.name)))) > 0
        file_1.close()


def test_cli_add_header_to_file() -> None:

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)
        assert (len(get_file_lines(Path(file_1.name)))) == 0

        sys.argv = [
            "--foo",  # to make sure that test works. We ignore first argv using MakeFile
            "--mode",
            "add_header",
            "--files",
            str(file_1.name),
            "--header-path",
            str(TEST_HEADER_PATH.resolve()),
            "--extensions",
            ".py",
            "--debug",
        ]
        run_cli()
        assert (len(get_file_lines(Path(file_1.name)))) > 0
        file_1.close()


def test_cli_add_header_to_file_and_folder() -> None:

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)
        file_2 = tempfile.NamedTemporaryFile(suffix=".py")
        assert (len(get_file_lines(Path(file_1.name)))) == 0

        sys.argv = [
            "--foo",  # to make sure that test works. We ignore first argv using MakeFile
            "--mode",
            "add_header",
            "--files",
            str(tmpdirname),
            str(file_2.name),
            "--header-path",
            str(TEST_HEADER_PATH.resolve()),
            "--extensions",
            ".py",
            "--debug",
        ]
        run_cli()
        assert (len(get_file_lines(Path(file_1.name)))) > 0
        file_1.close()
        file_2.close()


def test_cli_add_and_remove_header() -> None:

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)
        assert (len(get_file_lines(Path(file_1.name)))) == 0

        sys.argv = [
            "--foo",  # to make sure that test works. We ignore first argv using MakeFile
            "--mode",
            "add_header",
            "--files",
            str(tmpdirname),
            "--header-path",
            str(TEST_HEADER_PATH.resolve()),
            "--extensions",
            ".py",
            "--debug",
        ]
        run_cli()
        assert (len(get_file_lines(Path(file_1.name)))) > 0

        sys.argv = [
            "--foo",  # to make sure that test works. We ignore first argv using MakeFile
            "--mode",
            "remove_header",
            "--files",
            str(tmpdirname),
            "--header-path",
            str(TEST_HEADER_PATH.resolve()),
            "--extensions",
            ".py",
            "--debug",
        ]
        run_cli()
        assert (len(get_file_lines(Path(file_1.name)))) == 0
        file_1.close()


def test_cli_header_is_not_file() -> None:
    with pytest.raises(ValueError):
        with tempfile.TemporaryDirectory() as tmpdirname:

            sys.argv = [
                "--foo",  # to make sure that test works. We ignore first argv using MakeFile
                "--mode",
                "add_header",
                "--files",
                str(tmpdirname),
                "--header-path",
                str(tmpdirname),
                "--extensions",
                ".py",
                "--debug",
            ]
            run_cli()


def test_cli_add_and_remove_header_all_ext() -> None:
    for ext in EXTENSION_TO_PROGRAMMING_LANGUAGE_MAPPING.keys():
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_1 = tempfile.NamedTemporaryFile(suffix=ext, dir=tmpdirname)
            assert (len(get_file_lines(Path(file_1.name)))) == 0

            sys.argv = [
                "--foo",  # to make sure that test works. We ignore first argv using MakeFile
                "--mode",
                "add_header",
                "--files",
                str(tmpdirname),
                "--header-path",
                str(TEST_HEADER_PATH.resolve()),
                "--extensions",
                f"{ext}",
                "--debug",
            ]
            run_cli()
            assert (len(get_file_lines(Path(file_1.name)))) > 0

            sys.argv = [
                "--foo",  # to make sure that test works. We ignore first argv using MakeFile
                "--mode",
                "remove_header",
                "--files",
                str(tmpdirname),
                "--header-path",
                str(TEST_HEADER_PATH.resolve()),
                "--extensions",
                f"{ext}",
                "--debug",
            ]
            run_cli()
            assert (len(get_file_lines(Path(file_1.name)))) == 0
            file_1.close()


def test_cli_add_and_remove_header_to_file() -> None:
    for ext in EXTENSION_TO_PROGRAMMING_LANGUAGE_MAPPING.keys():
        with tempfile.TemporaryDirectory() as tmpdirname:
            file_1 = tempfile.NamedTemporaryFile(suffix=ext, dir=tmpdirname)
            assert (len(get_file_lines(Path(file_1.name)))) == 0

            sys.argv = [
                "--foo",  # to make sure that test works. We ignore first argv using MakeFile
                "--mode",
                "add_header",
                "--files",
                str(file_1.name),
                "--header-path",
                str(TEST_HEADER_PATH.resolve()),
                "--extensions",
                f"{ext}",
                "--debug",
            ]
            run_cli()
            assert (len(get_file_lines(Path(file_1.name)))) > 0

            sys.argv = [
                "--foo",  # to make sure that test works. We ignore first argv using MakeFile
                "--mode",
                "remove_header",
                "--files",
                str(file_1.name),
                "--header-path",
                str(TEST_HEADER_PATH.resolve()),
                "--extensions",
                f"{ext}",
                "--debug",
            ]
            run_cli()
            assert (len(get_file_lines(Path(file_1.name)))) == 0
            file_1.close()


def test_compare_lines_with_different_comments() -> None:

    with tempfile.TemporaryDirectory() as tmpdirname:
        file_1 = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)
        file_2 = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)
        assert (len(get_file_lines(Path(file_1.name)))) == 0
        assert (len(get_file_lines(Path(file_2.name)))) == 0

        sys.argv = [
            "--foo",  # to make sure that test works. We ignore first argv using MakeFile
            "--mode",
            "add_header",
            "--files",
            str(file_1.name),
            "--header-path",
            str(TEST_HEADER_PATH.resolve()),
            "--extensions",
            ".py",
            "--debug",
        ]
        run_cli()
        file_1_len = len(get_file_lines(Path(file_1.name)))
        assert (file_1_len) > 0
        file_1.close()

        sys.argv = [
            "--foo",  # to make sure that test works. We ignore first argv using MakeFile
            "--mode",
            "add_header",
            "--files",
            str(file_2.name),
            "--header-path",
            str(TEST_HEADER_PATH.resolve()),
            "--extensions",
            ".py",
            "--debug",
            "--prefer-multiline-comment",
        ]
        run_cli()
        file_2_len = len(get_file_lines(Path(file_2.name)))
        assert (file_2_len) > 0
        file_2.close()

        assert file_2_len > file_1_len


# def test_cli_get_print_python() -> None:

#     with tempfile.TemporaryDirectory() as tmpdirname:
#         file = tempfile.NamedTemporaryFile(suffix=".py", dir=tmpdirname)
#         file.write(b"print('Hello world!')")
#         file.flush()
#         file.seek(0)
#         assert(len(get_file_lines(Path(file.name)))) == 1


#         sys.argv = [
#             "--foo", # to make sure that test works. We ignore first argv using MakeFile
#             "--mode",
#             "add_header",
#             "--files-dir",
#              str(tmpdirname),
#             "--header-path",
#             str(TEST_HEADER_PATH.resolve()),
# 		    "--extensions",
#             ".py",
# 		    "--debug"
#         ]
#         run_cli()

#         for line in get_file_lines(Path(file.name)):
#             print(line.replace("\n",""))

#         print()
#         #assert(len(get_file_lines(Path(file.name)))) == 0
#         result = StringIO(initial_value=(str(os.system(f'python {Path(file.name)}'))))
#         print(result.getvalue(),"HA")
#         assert False

# python -m pytest tests/component/test_cli.py
