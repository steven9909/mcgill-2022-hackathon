from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class CreateBodyParam(_message.Message):
    __slots__ = ["id", "mass", "p_x", "p_y", "v_x", "v_y"]
    ID_FIELD_NUMBER: _ClassVar[int]
    MASS_FIELD_NUMBER: _ClassVar[int]
    P_X_FIELD_NUMBER: _ClassVar[int]
    P_Y_FIELD_NUMBER: _ClassVar[int]
    V_X_FIELD_NUMBER: _ClassVar[int]
    V_Y_FIELD_NUMBER: _ClassVar[int]
    id: int
    mass: int
    p_x: float
    p_y: float
    v_x: float
    v_y: float
    def __init__(self, id: _Optional[int] = ..., mass: _Optional[int] = ..., p_x: _Optional[float] = ..., p_y: _Optional[float] = ..., v_x: _Optional[float] = ..., v_y: _Optional[float] = ...) -> None: ...

class DeleteBodyParam(_message.Message):
    __slots__ = ["id"]
    ID_FIELD_NUMBER: _ClassVar[int]
    id: int
    def __init__(self, id: _Optional[int] = ...) -> None: ...

class EmptyParam(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class Response(_message.Message):
    __slots__ = ["received"]
    RECEIVED_FIELD_NUMBER: _ClassVar[int]
    received: bool
    def __init__(self, received: bool = ...) -> None: ...

class UpdateBodyParam(_message.Message):
    __slots__ = ["id", "p_x", "p_y", "v_x", "v_y"]
    ID_FIELD_NUMBER: _ClassVar[int]
    P_X_FIELD_NUMBER: _ClassVar[int]
    P_Y_FIELD_NUMBER: _ClassVar[int]
    V_X_FIELD_NUMBER: _ClassVar[int]
    V_Y_FIELD_NUMBER: _ClassVar[int]
    id: int
    p_x: float
    p_y: float
    v_x: float
    v_y: float
    def __init__(self, id: _Optional[int] = ..., p_x: _Optional[float] = ..., p_y: _Optional[float] = ..., v_x: _Optional[float] = ..., v_y: _Optional[float] = ...) -> None: ...
