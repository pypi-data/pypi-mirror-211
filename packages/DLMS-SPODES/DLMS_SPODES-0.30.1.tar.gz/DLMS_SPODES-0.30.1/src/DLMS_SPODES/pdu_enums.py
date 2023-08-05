from enum import IntEnum, IntFlag
from typing import TypeAlias


class DataAccessResult(IntEnum):
    SUCCESS = 0
    HARDWARE_FAULT = 1
    TEMPORARY_FAILURE = 2
    READ_WRITE_DENIED = 3
    OBJECT_UNDEFINED = 4
    OBJECT_CLASS_INCONSISTENT = 9
    OBJECT_UNAVAILABLE = 11
    TYPE_UNMATCHED = 12
    SCOPE_OF_ACCESS_VIOLATED = 13
    DATA_BLOCK_UNAVAILABLE = 14
    LONG_GET_ABORTED = 15
    NO_LONG_GET_IN_PROGRESS = 16
    LONG_SET_ABORTED = 17
    NO_LONG_SET_IN_PROGRESS = 18
    DATA_BLOCK_NUMBER_INVALID = 19
    OTHER_REASON = 250


class GetResponse(IntEnum):
    NORMAL = 1
    WITH_DATABLOCK = 2
    WITH_LIST = 3


class SetResponse(IntEnum):
    NORMAL = 1
    DATABLOCK = 2
    LAST_DATABLOCK = 3
    LAST_DATABLOCK_WITH_LIST = 4
    WITH_LIST = 5


class ActionResult(IntEnum):
    SUCCESS = 0
    HARDWARE_FAULT = 1
    TEMPORARY_FAILURE = 2
    READ_WRITE_DENIED = 3
    OBJECT_UNDEFINED = 4
    OBJECT_CLASS_INCONSISTENT = 9
    OBJECT_UNAVAILABLE = 11
    TYPE_UNMATCHED = 12
    SCOPE_OF_ACCESS_VIOLATED = 13
    DATA_BLOCK_UNAVAILABLE = 14
    LONG_ACTION_ABORTED = 15
    NO_LONG_ACTION_IN_PROGRESS = 16
    OTHER_REASON = 250


class ActionResponse(IntEnum):
    NORMAL = 1
    WITH_PBLOCK = 2
    WITH_LIST = 3
    NEXT_PBLOCK = 4


class AttributeAccess(IntEnum):
    """use with version 0 and 1 AssociationLN"""
    NO_ACCESS = 0
    READ_ONLY = 1
    WRITE_ONLY = 2
    READ_AND_WRITE = 3
    AUTHENTICATED_READ_ONLY = 4
    AUTHENTICATED_WRITE_ONLY = 5
    AUTHENTICATED_READ_AND_WRITE = 6


class MethodAccess(IntEnum):
    """use with version 0 and 1 AssociationLN"""
    NO_ACCESS = 0
    ACCESS = 1
    AUTHENTICATED_ACCESS = 2


class SecurityPolicyVer0(IntEnum):
    NOTHING = 0
    AUTHENTICATED = 1
    ENCRYPTED = 2
    AUTHENTICATED_AND_ENCRYPTED = 3


class SecurityPolicyVer1(IntFlag):
    NOTHING = 0
    UNUSED_0 = 0b1
    UNUSED_1 = 0b10
    AUTHENTICATED_REQUEST = 0b100
    ENCRYPTED_REQUEST = 0b1000
    DIGITALLY_SIGNED_REQUEST = 0b1_0000
    AUTHENTICATED_RESPONSE = 0b10_0000
    ENCRYPTED_RESPONSE = 0b100_0000
    DIGITALLY_SIGNED_RESPONSE = 0b1000_0000


SecurityPolicy: TypeAlias = SecurityPolicyVer0 | SecurityPolicyVer1
