"""This package provides the decorators to annotate a transform component."""

from typing import Callable, Union, cast

from .types import ExposableCallable


def exposed(f: Union[Callable, ExposableCallable]) -> ExposableCallable:
    """Marks a function as a UI-visible transform component."""
    f.__exposed__ = True  # type: ignore
    return cast(ExposableCallable, f)


def hidden(f: Union[Callable, ExposableCallable]) -> ExposableCallable:
    """Marks a function as a non UI-visible transform component."""
    f.__exposed__ = False  # type: ignore
    return cast(ExposableCallable, f)
