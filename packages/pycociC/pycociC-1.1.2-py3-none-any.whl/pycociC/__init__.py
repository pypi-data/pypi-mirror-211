from __future__ import annotations

import os
import re
import sys
import threading
from functools import wraps
from pathlib import Path
from typing import AnyStr, Callable, Iterable, Any

__all__ = ('FP_RE', 'bytes_to_pretty_view', 'eat_cache')

FP_RE = re.compile(r'.*\.py([co]|.*\.nb[ci])', re.I)


def _ignore(_): pass


def _run_with_custom_recursion_level(func: Callable[[...], Any] | None = None, *,
                                     recursion_limit: int = 0x7FFF_FFFF, stack_size: int = 0x0FFF_FFFF
                                     ) -> (
        Callable[[Callable[[...], Any]], Callable[[...], None]] | Callable[[...], None]):
    """Decorator for sys.setrecursionlimit and threading.stack_size from kwargs and start func"""

    def run_max_recursion_decorator(func: Callable[[...], Any]) -> Callable[[...], None]:
        @wraps(func)
        def wrapper(*args, **kwargs) -> None:
            reset_recursion_limit = sys.getrecursionlimit()
            sys.setrecursionlimit(recursion_limit)
            threading.stack_size(stack_size)
            try:
                thread = threading.Thread(target=func, args=args, kwargs=kwargs)
                thread.start()
                thread.join()
            finally:
                sys.setrecursionlimit(reset_recursion_limit)
                threading.stack_size()

        return wrapper

    if func is not None:
        return run_max_recursion_decorator(func)
    return run_max_recursion_decorator


@_run_with_custom_recursion_level
def eat_cache(at_dirs: Iterable[AnyStr, os.PathLike[AnyStr]] = ('.',)):
    """Function removes files matching the regular expression (see FP_RE) from all "__pycache__" folders recursively."""
    print(f"Starting for {', '.join(at_dirs)}\n\n")
    removed = 0
    for top in at_dirs:
        for dirpath, _, filenames in os.walk(top, onerror=_ignore):
            del _
            dirpath = Path(dirpath)
            if dirpath.name.casefold() != '__pycache__':
                continue
            print(dirpath)
            for filename in filenames:
                if FP_RE.fullmatch(filename):
                    try:
                        target = dirpath / filename
                        fp_size = target.stat().st_size
                        os.remove(target)
                        print(f'\t{filename} ({bytes_to_pretty_view(fp_size)})')
                        removed += fp_size
                    except OSError:
                        continue
            try:
                dirpath.rmdir()
                print(dirpath)
            except OSError:
                pass
            print()
    print(f'\nRemoved {bytes_to_pretty_view(removed)}')


def bytes_to_pretty_view(bytes_size: int = 0) -> str:
    """
    Converts the number of bytes into a pretty SI prefix.

    >>> bytes_to_pretty_view(0)
    '0B'
    >>> bytes_to_pretty_view(1_000_000_24)
    '100MB 24B'
    >>> bytes_to_pretty_view(0xFF_FF_FF_FF)
    '4GB 294MB 967kB 295B'
    """
    if not bytes_size:
        return '0B'
    result = ''
    while bytes_size:
        power = 1
        for p in ('', 'k', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y'):
            if (d := bytes_size // power) < 1000:
                bytes_size %= power
                result += f'{d}{p}B '
                break
            power *= 1000
    return result[:-1]
