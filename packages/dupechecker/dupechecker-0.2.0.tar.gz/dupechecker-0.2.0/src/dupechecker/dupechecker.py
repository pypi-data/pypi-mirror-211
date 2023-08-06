import argparse
import filecmp
import time
from concurrent.futures import ThreadPoolExecutor
from itertools import combinations

from griddle import griddy
from pathier import Pathier
from printbuddies import Spinner
from younotyou import younotyou


def get_duplicates(paths: list[Pathier]) -> list[list[Pathier]]:
    """Return a list of lists for duplicate files in `paths`."""
    matching_sets = []
    while len(paths) > 0:
        comparee = paths.pop()
        matching_files = [file for file in paths if filecmp.cmp(comparee, file, False)]
        if matching_files:
            [paths.pop(paths.index(file)) for file in matching_files]
            matching_files.insert(0, comparee)
            matching_sets.append(matching_files)
    return matching_sets


def get_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help=""" Glob files to compare recursively. """,
    )

    parser.add_argument(
        "-i",
        "--ignores",
        type=str,
        nargs="*",
        default=[],
        help=""" Ignore files matching these patterns.
        e.g. `dupechecker -i *.wav` will compare all files in the current working directory except .wav files.""",
    )

    parser.add_argument(
        "-d",
        "--delete_dupes",
        action="store_true",
        help=""" After finding duplicates, delete all but one copy.
        For each set of duplicates, the tool will ask you to enter the number corresponding to the copy you want to keep.
        Pressing 'enter' without entering a number will skip that set without deleting anything.""",
    )

    parser.add_argument(
        "-ad",
        "--autodelete",
        action="store_true",
        help=""" Automatically decide which file to keep and which to delete from each set of duplicate files instead of asking which to keep. """,
    )

    parser.add_argument(
        "-ns",
        "--no_show",
        action="store_true",
        help=""" Don't show printout of matching files. """,
    )

    parser.add_argument(
        "paths",
        type=str,
        default=[Pathier.cwd()],
        nargs="*",
        help=""" The paths to compare files in. """,
    )

    args = parser.parse_args()
    if not args.paths == [Pathier.cwd()]:
        args.paths = [Pathier(path) for path in args.paths]
    files = []
    print("Gathering files...")
    for path in args.paths:
        files.extend(
            list(path.rglob("*.*")) if args.recursive else list(path.glob("*.*"))
        )
    args.paths = younotyou([str(file) for file in files], exclude_patterns=args.ignores)
    num_comparisons = len(list(combinations(args.paths, 2)))
    print(f"Making {num_comparisons} comparisons between {len(args.paths)} files...")

    return args


def delete_wizard(matches: list[list[Pathier]]):
    """Ask which file to keep for each set."""
    print()
    print("Enter the corresponding number of the file to keep.")
    print(
        "Press 'Enter' without giving a number to skip deleting any files for the given set."
    )
    print()
    for match in matches:
        map_ = {str(i): file for i, file in enumerate(match, 1)}
        options = "\n".join(f"({i}) {file}" for i, file in map_.items()) + "\n"
        print(options)
        keeper = input(f"Enter number of file to keep ({', '.join(map_.keys())}): ")
        if keeper:
            [map_[num].delete() for num in map_ if num != keeper]


def autodelete(matches: list[list[Pathier]]):
    """Keep one of each set in `matches` and delete the others."""
    for match in matches:
        match.pop()
        [file.delete() for file in match]


def dupechecker(args: argparse.Namespace | None = None):
    print()
    if not args:
        args = get_args()
    s = [
        ch.rjust(i + j)
        for i in range(1, 25, 3)
        for j, ch in enumerate(["/", "-", "\\"])
    ]
    s += s[::-1]
    with Spinner(s) as spinner:
        with ThreadPoolExecutor() as exc:
            thread = exc.submit(get_duplicates, args.paths)
            while not thread.done():
                spinner.display()
                time.sleep(0.025)
            matches = thread.result()
    if matches:
        print(f"Found {len(matches)} duplicate sets of files.")
        if not args.no_show:
            print(griddy(matches))
        if args.delete_dupes or args.autodelete:
            size = args.path.size()
            delete_wizard(matches) if args.delete_dupes else autodelete(matches)
            deleted_size = size - args.path.size()
            print(f"Deleted {Pathier.format_size(deleted_size)}.")
    else:
        print("No duplicates detected.")


if __name__ == "__main__":
    dupechecker(get_args())
