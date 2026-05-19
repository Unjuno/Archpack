from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import shutil


class ArchpackError(Exception):
    """Base exception for Archpack errors."""


class PackError(ArchpackError):
    """Raised when the pack directory is invalid."""


class UnsafePathError(ArchpackError):
    """Raised when a path would escape the intended tree."""


class ExistingFileError(ArchpackError):
    """Raised when unpack would overwrite an existing file."""


@dataclass(frozen=True)
class CopyResult:
    written: tuple[Path, ...]
    skipped: tuple[Path, ...]


def get_tree_dir(pack_dir: Path) -> Path:
    pack_dir = Path(pack_dir)
    tree_dir = pack_dir / "tree"
    if not pack_dir.exists():
        raise PackError(f"Pack directory does not exist: {pack_dir}")
    if not pack_dir.is_dir():
        raise PackError(f"Pack path is not a directory: {pack_dir}")
    if not tree_dir.exists():
        raise PackError(f"Pack is missing tree directory: {tree_dir}")
    if not tree_dir.is_dir():
        raise PackError(f"Pack tree path is not a directory: {tree_dir}")
    return tree_dir


def iter_pack_files(pack_dir: Path) -> list[tuple[Path, Path]]:
    tree_dir = get_tree_dir(pack_dir)
    pairs: list[tuple[Path, Path]] = []
    for source in sorted(tree_dir.rglob("*")):
        if source.is_dir():
            continue
        if source.is_symlink():
            raise UnsafePathError(f"Symlinks are not allowed in pack tree: {source}")
        rel = source.relative_to(tree_dir)
        validate_relative_path(rel)
        pairs.append((source, rel))
    return pairs


def validate_relative_path(rel: Path) -> None:
    if rel.is_absolute():
        raise UnsafePathError(f"Absolute paths are not allowed: {rel}")
    parts = rel.parts
    if not parts:
        raise UnsafePathError("Empty relative path is not allowed")
    if any(part in ("", ".", "..") for part in parts):
        raise UnsafePathError(f"Unsafe relative path: {rel}")


def destination_for(out_dir: Path, rel: Path) -> Path:
    validate_relative_path(rel)
    out_dir = Path(out_dir)
    dest = out_dir / rel
    resolved_out = out_dir.resolve(strict=False)
    resolved_dest = dest.resolve(strict=False)
    if resolved_dest != resolved_out and resolved_out not in resolved_dest.parents:
        raise UnsafePathError(f"Destination escapes output directory: {dest}")
    return dest


def unpack(pack_dir: Path, out_dir: Path, *, skip_existing: bool = False) -> CopyResult:
    written: list[Path] = []
    skipped: list[Path] = []
    out_dir = Path(out_dir)
    for source, rel in iter_pack_files(pack_dir):
        dest = destination_for(out_dir, rel)
        if dest.exists():
            if skip_existing:
                skipped.append(rel)
                continue
            raise ExistingFileError(f"Refusing to overwrite existing file: {dest}")
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        written.append(rel)
    return CopyResult(tuple(written), tuple(skipped))


def repair(pack_dir: Path, out_dir: Path, *, overwrite: bool = False) -> CopyResult:
    written: list[Path] = []
    skipped: list[Path] = []
    out_dir = Path(out_dir)
    for source, rel in iter_pack_files(pack_dir):
        dest = destination_for(out_dir, rel)
        if dest.exists() and not overwrite:
            skipped.append(rel)
            continue
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        written.append(rel)
    return CopyResult(tuple(written), tuple(skipped))
