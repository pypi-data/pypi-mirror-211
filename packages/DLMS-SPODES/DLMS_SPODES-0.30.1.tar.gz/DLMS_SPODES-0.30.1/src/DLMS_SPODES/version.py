from __future__ import annotations
from struct import pack


class AppVersion:
    __major: int
    __minor: int
    __patch: int | None
    __additional: str
    __match_args__ = ('major', 'minor', 'patch')

    def __init__(self, major: int, minor: int, patch: int = None, additional: str = ''):
        self.__major = major
        self.__minor = minor
        self.__patch = patch
        self.__additional = additional

    @classmethod
    def from_str(cls, value: str):
        match value.split(sep='.', maxsplit=2):
            case (major, minor, patch):
                match major.isdigit(), minor.isdigit(), patch.isdigit():
                    case True, True, True:                        return cls(int(major), int(minor), int(patch))
                    case True, True, False:
                        patch_seq = bytearray(patch, 'utf-8')
                        patch_seq.insert(0, ord('0'))  # if not founded integer when patch default value is 0
                        digit_pos = 0
                        while patch_seq[:digit_pos + 1].isdigit() and digit_pos < len(patch_seq):
                            digit_pos += 1
                        return cls(int(major), int(minor), int(patch_seq[:digit_pos]), patch_seq[digit_pos:].decode())
                    case _:                                      return cls(0, 0, 0)
            case (major, minor):
                match major.isdigit(), minor.isdigit():
                    case True, True:                        return cls(int(major), int(minor))
                    case _:                                      return cls(0, 0)
            case _:                                              return cls(0, 0, 0)

    @property
    def major(self) -> int:
        return self.__major

    @property
    def minor(self) -> int:
        return self.__minor

    @property
    def patch(self) -> int | None:
        return self.__patch

    @property
    def additional(self) -> str:
        return self.__additional

    def __eq__(self, other: AppVersion):
        return hash(self) == hash(other) and self.__additional == other.additional

    def __gt__(self, other: AppVersion):
        if self.__major > other.__major:
            return True
        elif self.__major < other.__major:
            return False
        elif self.__minor > other.__minor:
            return True
        elif self.__minor < other.__minor:
            return False
        if self.__patch is None:
            return False
        elif self.__patch > other.__patch:
            return True
        else:
            return False

    def __ge__(self, other: AppVersion):
        if self.__major > other.__major:
            return True
        elif self.__major < other.__major:
            return False
        elif self.__minor > other.__minor:
            return True
        elif self.__minor < other.__minor:
            return False
        if self.__patch is None:
            return True
        elif self.__patch > other.__patch:
            return True
        elif self.__patch < other.__patch:
            return False
        else:
            return True

    def __str__(self):
        return F'{self.__major}.{self.__minor}{F".{self.__patch}" if self.__patch is not None else ""}{F" <{self.__additional}>" if len(self.__additional) != 0 else ""}'

    def __repr__(self):
        return F"{self.__class__.__name__}({self.__major}, {self.__minor}{F', {self.__patch}' if self.__patch is not None else ''}{', additional='+repr(self.additional) if self.additional else ''})"

    def __hash__(self):
        """ to int6 every 2 byte for major, minor, patch """
        if self.__patch is not None:
            return hash((self.__major, self.__minor, self.__patch))
        else:
            return hash((self.__major, self.__minor))

    def select_nearest(self, variants: list[AppVersion | str]) -> AppVersion | None:
        """ select left nearest from list. If version is absence return None """
        app_versions: list[AppVersion | None] = [self]
        for version in variants:
            match version:
                case AppVersion(): app_versions.append(version)
                case str():        app_versions.append(self.from_str(version))
                case _:            pass
        app_versions.sort()
        app_versions.append(None)
        return app_versions[app_versions.index(self)-1]
