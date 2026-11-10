"""Structured result returned by every skill, so agents get uniform feedback."""
from __future__ import annotations  #helps newer syntax work on older versions of python.

from dataclasses import dataclass, field    #Writes the boilerplate for you
from typing import Any  #Typing hints


@dataclass(frozen=True) #Mark class as data class and unchangeable
class Result:
    #Did the skill work?
    ok: bool
    #Useful outputs
    data: dict[str, Any] = field(default_factory=dict)
    #Error message (if exists)
    error: str | None = None

    @classmethod
    def success(cls, **data: Any) -> "Result":
        return cls(ok=True, data=data)

    @classmethod
    def failure(cls, error: str, **data: Any) -> "Result":
        return cls(ok=False, data=data, error=error)

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "data": self.data, "error": self.error}
