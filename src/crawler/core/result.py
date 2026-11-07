"""Structured result returned by every skill, so agents get uniform feedback."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class Result:
    ok: bool
    data: dict[str, Any] = field(default_factory=dict)
    error: str | None = None

    @classmethod
    def success(cls, **data: Any) -> "Result":
        return cls(ok=True, data=data)

    @classmethod
    def failure(cls, error: str, **data: Any) -> "Result":
        return cls(ok=False, data=data, error=error)

    def to_dict(self) -> dict[str, Any]:
        return {"ok": self.ok, "data": self.data, "error": self.error}
