# cython: language_level=3

import collections
import contextlib
import os
from typing import Dict, Optional, Union

cimport epicscorelibs
cimport epicscorelibs.Com
from libc.stdlib cimport free, malloc


cdef extern from "<ellLib.h>" nogil:
    cdef struct ELLNODE:
        ELLNODE *next
        ELLNODE *previous

    cdef struct ELLLIST:
        ELLNODE node   # Pointers to the first and last nodes on list
        int     count  # Number of nodes on the list


ctypedef struct MAC_ENTRY:
    # prev and next pointers
    ELLNODE     node
    # entry name
    char        *name
    # entry type
    char        *type
    # raw (unexpanded) value
    char        *rawval
    # expanded macro value
    char        *value
    # length of value
    size_t      length
    # error expanding value?
    int         error
    # ever been visited?
    int         visited
    # special (internal) entry?
    int         special
    # scoping level
    int         level


cdef extern from "<macLib.h>" nogil:
    ctypedef struct MAC_HANDLE:
        long        magic     # magic number (used for authentication)
        int         dirty     # values need expanding from raw values?
        int         level     # scoping level
        int         debug     # debugging level
        ELLLIST     list      # macro name / value list
        int         flags     # operating mode flags

    char *macEnvExpand(const char *str)
    MAC_HANDLE *macCreateHandle(MAC_HANDLE **handle, const char *pairs[])
    long macDeleteHandle(MAC_HANDLE *handle)
    long macExpandString(MAC_HANDLE *handle, const char *src, char *dest, long capacity)
    long macInstallMacros(MAC_HANDLE *handle, char *pairs[])
    long macParseDefns(MAC_HANDLE *handle, const char *defns, char **pairs[])
    void macPopScope(MAC_HANDLE *handle)
    void macPushScope(MAC_HANDLE *handle)
    void macSuppressWarning(MAC_HANDLE *handle, int)


cdef class _MacroContext:
    """
    A context for using EPICS macLib handle from Python.

    When other macro expansion tools just aren't enough, go with the one true
    macro expander - the one provided by EPICS - macLib.

    Parameters
    ----------
    use_environment : bool, optional
        Include environment variables when expanding macros.

    show_warnings : bool, optional
        Show warnings (see ``macSuppressWarning``).

    string_encoding : str, optional
        The default string encoding to use.  Defaults to latin-1, as these
        tools were written before utf-8 was really a thing.
    """

    cdef MAC_HANDLE *handle
    _show_warnings: bool
    cdef public str string_encoding
    cdef int use_environment

    def __init__(
        self,
        use_environment=True,
        show_warnings=False,
        string_encoding: str = "latin-1",
        macro_string: Optional[str] = None,
        macros: Optional[Dict[str, str]] = None,
    ):
        cdef const char **env_pairs = ["", "environ", NULL, NULL]

        if macCreateHandle(&self.handle, env_pairs if use_environment else NULL):
            raise RuntimeError("Failed to initialize the handle")

        self.show_warnings = show_warnings
        self.string_encoding = string_encoding
        self.use_environment = bool(use_environment)

        if macros:
            self.define(**macros)

        if macro_string:
            self.define_from_string(macro_string)

    @property
    def show_warnings(self):
        return self._show_warnings

    @show_warnings.setter
    def show_warnings(self, value: bool):
        self._show_warnings = bool(value)
        suppress = not self._show_warnings
        macSuppressWarning(self.handle, suppress)

    def __cinit__(self):
        self.handle = NULL

    def __dealloc__(self):
        if self.handle is not NULL:
            macDeleteHandle(self.handle)
            self.handle = NULL

    @contextlib.contextmanager
    def scoped(self, **macros):
        """A context manager to define macros (as kwargs) in a given scope."""
        macPushScope(self.handle)
        self.define(**macros)
        yield
        macPopScope(self.handle)

    def definitions_to_dict(self, defn: Union[str, bytes], string_encoding: str = "") -> Dict[str, str]:
        """Convert a definition string of the form ``A=value_a,B=value_a`` to a dictionary."""
        cdef char **pairs = NULL
        cdef int count

        string_encoding = string_encoding or self.string_encoding

        if not isinstance(defn, bytes):
            defn = defn.encode(string_encoding)

        count = macParseDefns(self.handle, defn, &pairs)
        if pairs == NULL or count <= 0:
            return {}

        result = {}
        for idx in range(count):
            variable = (pairs[2 * idx] or b'').decode(string_encoding)
            value = (pairs[2 * idx + 1] or b'').decode(string_encoding)
            result[variable] = value

        free(pairs)
        return result

    def define_from_string(self, macro_string):
        """Define macros with the standard VAR=VALUE syntax."""
        definitions = self.definitions_to_dict(macro_string)
        self.define(**definitions)
        return definitions

    def define(self, **macros):
        """Use kwargs to define macros."""
        for key, value in macros.items():
            self.add_macro(
                str(key).encode(self.string_encoding),
                str(value).encode(self.string_encoding)
            )

    cdef int add_macro(self, key: bytes, value: bytes):
        cdef char** pairs = [key, value, NULL];
        return macInstallMacros(self.handle, pairs)

    def get_macro_details(self) -> Dict[str, str]:
        """
        Get a dictionary of full macro details.

        This represents the internal state of the MAC_ENTRY nodes.

        Included keys: name, rawval, value, type.
        """
        encoding = self.string_encoding
        result = {}
        cdef MAC_ENTRY* entry = <MAC_ENTRY*>self.handle.list.node.next
        while entry != NULL:
            if entry.name:
                name = (entry.name or b"").decode(encoding)
                result[name] = {
                    "name": name,
                    "rawval": (entry.rawval or b"").decode(encoding),
                    "value": (entry.value or b"").decode(encoding),
                    "type": (entry.type or b"").decode(encoding),
                }
            entry = <MAC_ENTRY*>entry.node.next
        return result

    def get_macros(self) -> Dict[str, str]:
        """Get macros as a dictionary."""
        return dict(
            (macro["name"], macro["value"])
            for macro in self.get_macro_details().values()
        )

    def __len__(self):
        cdef MAC_ENTRY* entry = <MAC_ENTRY*>self.handle.list.node.next
        cdef int count = 0
        while entry != NULL:
            if entry.name:
                count += 1
            entry = <MAC_ENTRY*>entry.node.next
        return count

    def __iter__(self):
        cdef MAC_ENTRY* entry = <MAC_ENTRY*>self.handle.list.node.next
        if self.use_environment:
            yield from os.environ
        while entry != NULL:
            if entry.name:
                yield (entry.name or b"").decode(self.string_encoding)
            entry = <MAC_ENTRY*>entry.node.next

    def __getitem__(self, item):
        encoding = self.string_encoding
        # Start at the end for scoping
        cdef MAC_ENTRY* entry = <MAC_ENTRY*>self.handle.list.node.previous

        while entry != NULL:
            if entry.name:
                name = (entry.name or b"").decode(encoding)
                if name == item:
                    return self.expand((entry.rawval or b"").decode(encoding))
            entry = <MAC_ENTRY*>entry.node.previous

        if self.use_environment and item in os.environ:
            return os.environ[item]

        raise KeyError(item)

    def __setitem__(self, item, value):
        self.define(**{item: value})

    def expand_with_length(
        self, value: str, max_length: int = 1024, *, empty_on_failure: bool = False
    ) -> str:
        """
        Expand a string, specifying the maximum length of the buffer.

        Trivia: 1024 is "MY_BUFFER_SIZE" in epics-base, believe it or not...
        """
        assert max_length > 0
        cdef char* buf = <char *>malloc(max_length)
        if not buf:
            raise MemoryError("Failed to allocate buffer")
        try:
            if macExpandString(self.handle, value.encode(self.string_encoding), buf, max_length) < 0:
                if empty_on_failure:
                    return ""
            return buf.decode(self.string_encoding)
        finally:
            free(buf)

    def expand(self, value: str, *, empty_on_failure: bool = False) -> str:
        """Expand a string, using the implicit buffer length of 1024 used in EPICS."""
        assert len(value) < 1024, "For large strings, use `expand_with_length`"
        cdef char buf[1024]
        #         n = macExpandString(handle, str, dest, destCapacity);
        # return < 0? return NULL...
        if macExpandString(self.handle, value.encode(self.string_encoding), buf, 1024) < 0:
            if empty_on_failure:
                return ""
        return buf.decode(self.string_encoding)

    def expand_by_line(self, contents: str, *, delimiter: str = "\n"):
        """Expand a multi-line string, line-by-line."""
        return delimiter.join(
            self.expand(line)
            for line in contents.splitlines()
        )


class MacroContext(_MacroContext, collections.abc.MutableMapping):
    ...
