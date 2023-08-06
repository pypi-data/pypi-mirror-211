# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Sampling class definition."""

from __future__ import annotations
from enum import Enum
from typing import (
    Iterator,
    List,
    NamedTuple,
    Optional,
    Tuple,
    TYPE_CHECKING,
    Union,
)

from temporian.core.data.dtype import DType, py_types_to_dtypes

if TYPE_CHECKING:
    from temporian.core.operators.base import Operator


class IndexLevel(NamedTuple):
    name: str
    dtype: IndexDType


class IndexDType(Enum):
    INT32 = DType.INT32.value
    INT64 = DType.INT64.value
    STRING = DType.STRING.value


IndexType = Union[IndexDType, int, str]


class Index:
    def __init__(
        self,
        levels: Union[Tuple[str, IndexType], List[Tuple[str, IndexType]]],
    ) -> None:
        # TODO: Check for correct DType.
        if isinstance(levels, Tuple):
            levels = [levels]

        self._levels = []
        for name, dtype in levels:
            # type check name
            if not isinstance(name, str):
                raise TypeError(
                    f"Index level {(name, dtype)}'s name's type must be string."
                    f" Got {type(name)}."
                )
            # type check dtype
            dtype = py_types_to_dtypes(dtype)
            if all(
                dtype.value != index_dtype.value for index_dtype in IndexDType
            ):
                raise TypeError(
                    f"Index level {(name, dtype)}'s dtype's type must be one of"
                    f" {IndexDType}. Got {type(dtype)}."
                )
            self._levels.append(IndexLevel(name, dtype))

    def __repr__(self) -> str:
        return f"Index({self._levels})"

    def __iter__(self) -> Iterator[IndexLevel]:
        return iter(self._levels)

    # TODO: Remove
    @property
    def levels(self) -> List[IndexLevel]:
        return self._levels

    # TODO: Remove property
    @property
    def names(self) -> List[str]:
        return [index_level.name for index_level in self._levels]

    # TODO: Remove property
    @property
    def dtypes(self) -> List[IndexDType]:
        return [index_level.dtype for index_level in self._levels]

    def __eq__(self, other) -> bool:
        if not isinstance(other, Index):
            return False
        return self.levels == other.levels


class Sampling(object):
    """Lists of timestamps corresponding to unique values in an Index.

    A sampling consists of a (possibly multi-level) index, and a list of
    timestamps for each of the unique pairs of values present in it.

    A sampling holds no actual data, but rather describes the structure (or
    "schema") of data during evaluation.

    A sampling's values can correspond to actual Unix timestamps, but also to
    any arbitrary number that represents a time (e.g. the number of seconds that
    passed since an experiment's start time).

    Attributes:
        creator: Operator that created this sampling. Can be None if it wasn't
            created by an operator.
        index: Names of the columns that compose this sampling's index.
        is_unix_timestamp: Whether values correspond to Unix timestamps.
    """

    def __init__(
        self,
        index_levels: Union[
            Tuple[str, AnyDType],
            List[Tuple[str, AnyDType]],
            Index,
        ],
        is_unix_timestamp: bool,
        creator: Optional[Operator] = None,
    ) -> None:
        if isinstance(index_levels, Index):
            self._index = index_levels
        else:
            self._index = Index(index_levels)
        self._creator = creator
        self._is_unix_timestamp = is_unix_timestamp

    def __repr__(self):
        return f"Sampling<index:{self.index}, id:{id(self)}>"

    @property
    def index(self) -> Index:
        return self._index

    @property
    def creator(self) -> Optional[Operator]:
        return self._creator

    @property
    def is_unix_timestamp(self) -> bool:
        return self._is_unix_timestamp

    # TODO: Remove. A sampling is constant after its creation.
    @creator.setter
    def creator(self, creator: Optional[Operator]):
        self._creator = creator
