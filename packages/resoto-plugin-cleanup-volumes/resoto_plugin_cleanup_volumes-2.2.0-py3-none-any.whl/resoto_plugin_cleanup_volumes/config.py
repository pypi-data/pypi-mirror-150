from dataclasses import dataclass, field
from typing import ClassVar
from resotolib.utils import parse_delta


@dataclass
class CleanupVolumesConfig:
    kind: ClassVar[str] = "plugin_cleanup_volumes"
    enabled: bool = field(
        default=False,
        metadata={"description": "Enable plugin?", "restart_required": True},
    )
    min_age: str = field(
        default="14 days",
        metadata={
            "description": "Minimum age of unused volumes to cleanup",
            "type_hint": "duration",
        },
    )

    @staticmethod
    def validate(config: "CleanupVolumesConfig") -> bool:
        parse_delta(config.min_age)
        return True
