from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal


RoomType = Literal[
    "living",
    "dining",
    "kitchen",
    "bedroom",
    "study",
    "bathroom",
    "utility",
    "circulation",
]


@dataclass
class RoomRequirement:
    room_type: RoomType
    name: str
    count: int = 1
    target_area_sqft: float = 80.0
    adjacency_pref: List[str] = field(default_factory=list)


@dataclass
class StructuredBrief:
    raw_text: str
    rooms: List[RoomRequirement]
    bhk: int = 2
    total_area_sqft: float = 1200
    maximize_natural_light: bool = False
    open_kitchen: bool = False
    constraints: Dict[str, str] = field(default_factory=dict)


@dataclass
class RoomPlacement:
    name: str
    room_type: RoomType
    x: float
    y: float
    width: float
    height: float


@dataclass
class LayoutPlan:
    footprint_width_ft: float
    footprint_height_ft: float
    rooms: List[RoomPlacement]
    doors: List[Dict[str, float]] = field(default_factory=list)
    windows: List[Dict[str, float]] = field(default_factory=list)


@dataclass
class GenerateRequest:
    brief: str


@dataclass
class ReviseRequest:
    revision: str


@dataclass
class ProjectState:
    project_id: str
    brief: StructuredBrief
    versions: List[LayoutPlan]
