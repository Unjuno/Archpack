from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .core import ArchpackError, repair, unpack


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="archpack")
    subparsers = parser.add_subparsers(dest="command", required=True)

    unpack_parser = subparsers.add_parser("unpack", help="Generate a file tree from a pack directory.")
    unpack_parser.add_argument("pack_dir", type=Path, help="Pack directory containing a tree/ directory.")
    unpack_parser.add_argument("--out", required=True, type=Path, help="Output directory.")
    unpack_parser.add_argument(
        "--skip-existing",
        action="store_true",
        help="Do not stop on existing files. Existing files are skipped and missing files are written.",
    )

    repair_parser = subparsers.add_parser("repair", help="Repair generated files from a pack directory.")
    repair_parser.add_argument("pack_dir", type=Path, help="Pack directory containing a tree/ directory.")
    repair_parser.add_argument("--out", required=True, type=Path, help="Output directory.")
    repair_parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output files. Without this, repair only restores missing files.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "unpack":
            if args.skip_existing:
                result = repair(args.pack_dir, args.out, overwrite=False)
            else:
                result = unpack(args.pack_dir, args.out)
        elif args.command == "repair":
            result = repair(args.pack_dir, args.out, overwrite=args.overwrite)
        else:
            parser.error(f"Unknown command: {args.command}")
            return 2
    except ArchpackError as exc:
        print(f"archpack: error: {exc}", file=sys.stderr)
        return 1

    for path in result.written:
        print(f"written: {path.as_posix()}")
    for path in result.skipped:
        print(f"skipped: {path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
