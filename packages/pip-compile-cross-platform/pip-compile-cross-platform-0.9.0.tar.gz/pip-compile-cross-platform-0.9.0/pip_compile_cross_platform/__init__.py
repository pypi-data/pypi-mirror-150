import shutil
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List, Set

from pip_requirements_parser import (
    RequirementsFile,
)
import subprocess
import sys


def generate(requirements: Set[str], min_python_version: str, output_file: Path):
    with TemporaryDirectory() as work_dir_str:
        work_dir = Path(work_dir_str)

        subprocess.run(
            [
                sys.executable,
                "-m",
                "poetry",
                "init",
                f"--python=^{min_python_version}",
                "--no-interaction",
            ],
            cwd=work_dir,
            check=True,
        )

        subprocess.run(
            [
                sys.executable,
                "-m",
                "poetry",
                "add",
                "--lock",
                *requirements,
            ],
            cwd=work_dir,
            check=True,
        )

        subprocess.run(
            [
                sys.executable,
                "-m",
                "poetry",
                "export",
                "-o",
                "requirements.txt",
            ],
            cwd=work_dir,
            check=True,
        )

        shutil.copy(str(work_dir / "requirements.txt"), str(output_file))


def resolve_requirements(files: List[Path]) -> Set[str]:
    if not files:
        for p in ("requirements.in", "setup.py"):
            path = Path(p)
            if path.exists():
                files.append(path)
                break

    requirements = set()
    for file in files:
        if file.name == "setup.py":
            requirements.add(str(Path.cwd()))

        raw_requirements = RequirementsFile.from_file(
            str(file), include_nested=True
        ).requirements
        for req in raw_requirements:
            if req.req:
                requirements.add(str(req.req))
            elif req.link:
                requirements.add(str(Path.cwd().joinpath(req.link.url)))
            else:
                raise Exception(f"Unexpected kind of requirement: {req}")

    return requirements


def main():
    parser = ArgumentParser(
        description="Compiles a cross-platform requirements.txt from requirements.in "
        "specs."
    )
    parser.add_argument(
        "src_files",
        metavar="src-file",
        nargs="*",
        help="requirements.in or setup.py file",
    )
    parser.add_argument(
        "-o --output-file",
        dest="output_file",
        default="requirements.txt",
        help="Output file name. Will be derived from input file if only one provided, "
        'otherwise defaults to "requirements.txt".',
    )
    parser.add_argument("--min-python-version", default="3.6.1")

    args = parser.parse_args()
    src_files = [Path(f) for f in args.src_files]
    output_file = Path.cwd() / Path(args.output_file)
    if len(src_files) == 1:
        src_file = src_files[0]
        if src_file.name.endswith(".in"):
            output_file = Path.cwd() / (src_file.stem + ".txt")

    requirements = resolve_requirements(src_files)
    generate(requirements, args.min_python_version, output_file)


if __name__ == "__main__":
    main()
