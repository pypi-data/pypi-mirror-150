import shutil
from argparse import ArgumentParser
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import List

import tomli
import tomli_w
from packaging.requirements import Requirement
from pip_requirements_parser import (
    RequirementsFile,
)
import subprocess
import sys


def generate(
    requirements: List[Requirement],
    existing_requirements: List[Requirement],
    min_python_version: str,
    output_file: Path,
):
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

        if existing_requirements:
            subprocess.run(
                [
                    sys.executable,
                    "-m",
                    "poetry",
                    "add",
                    "--lock",
                    *(str(req) for req in existing_requirements),
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
                *(str(req) for req in requirements),
            ],
            cwd=work_dir,
            check=True,
        )

        top_level_requirement_names = [req.name for req in requirements]
        transitive_requirement_names = [
            req.name.lower()
            for req in existing_requirements
            if req.name not in top_level_requirement_names
        ]
        with open(work_dir / "pyproject.toml", "rb") as pyproject_file:
            pyproject = tomli.load(pyproject_file)

        pyproject["tool"]["poetry"]["dependencies"] = {
            name: version
            for name, version in pyproject["tool"]["poetry"]["dependencies"].items()
            if name.lower() not in transitive_requirement_names
        }

        with open(work_dir / "pyproject.toml", "wb") as pyproject_file:
            tomli_w.dump(pyproject, pyproject_file)

        subprocess.run(
            [
                sys.executable,
                "-m",
                "poetry",
                "lock",
                "--no-update",
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


def resolve_requirements(files: List[Path]) -> List[Requirement]:
    if not files:
        for p in ("requirements.in", "setup.py"):
            path = Path(p)
            if path.exists():
                files.append(path)
                break

    requirements = []
    for file in files:
        if file.name == "setup.py":
            raise Exception("setup.py not yet supported")

        raw_requirements = RequirementsFile.from_file(
            str(file), include_nested=True
        ).requirements
        for req in raw_requirements:
            if req.is_url:
                raise Exception(f"URLs not supported: {req}")
            if not req.req:
                raise Exception(f"Unexpected kind of requirement: {req}")
            requirements.append(req.req)

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
    parser.add_argument("--min-python-version", default="3.6")

    args = parser.parse_args()
    src_files = [Path(f) for f in args.src_files]
    output_file = Path.cwd() / Path(args.output_file)
    if len(src_files) == 1:
        src_file = src_files[0]
        if src_file.name.endswith(".in"):
            output_file = Path.cwd() / (src_file.stem + ".txt")

    requirements = resolve_requirements(src_files)
    if output_file.exists():
        existing_requirements = resolve_requirements([output_file])
    else:
        existing_requirements = []
    generate(requirements, existing_requirements, args.min_python_version, output_file)


if __name__ == "__main__":
    main()
