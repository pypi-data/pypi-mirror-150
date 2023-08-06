"""This package defines types hints used by the streamunolib library."""

from typing import Callable, Protocol, runtime_checkable


@runtime_checkable
class ExposableCallable(Protocol):
    """Interface of all components that can be exposed or hidden."""

    __call__: Callable
    __exposed__: bool
