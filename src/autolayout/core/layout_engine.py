from __future__ import annotations

import math
from typing import List

from autolayout.models import LayoutPlan, RoomPlacement, StructuredBrief


PUBLIC_ROOMS = {"living", "dining", "study"}
SERVICE_ROOMS = {"kitchen", "utility", "bathroom"}


def _expand_rooms(brief: StructuredBrief) -> List[tuple[str, str, float]]:
    expanded: List[tuple[str, str, float]] = []
    for req in brief.rooms:
        for idx in range(req.count):
            suffix = f"_{idx + 1}" if req.count > 1 else ""
            expanded.append((f"{req.name}{suffix}", req.room_type, req.target_area_sqft))
    return expanded


def generate_layout(brief: StructuredBrief) -> LayoutPlan:
    total_area = brief.total_area_sqft
    width = round(math.sqrt(total_area * 1.25), 2)
    height = round(total_area / width, 2)

    expanded = _expand_rooms(brief)
    public = [r for r in expanded if r[1] in PUBLIC_ROOMS]
    private = [r for r in expanded if r[1] == "bedroom"]
    service = [r for r in expanded if r[1] in SERVICE_ROOMS]

    bands = [
        (public, 0.0, height * 0.38),
        (private, height * 0.38, height * 0.74),
        (service, height * 0.74, height),
    ]

    rooms: List[RoomPlacement] = []
    for room_group, y0, y1 in bands:
        if not room_group:
            continue
        band_h = y1 - y0
        x_cursor = 0.0
        total_group_area = sum(r[2] for r in room_group)
        for name, room_type, area in room_group:
            share = area / total_group_area if total_group_area else 1 / len(room_group)
            room_w = max(7.0, width * share)
            if x_cursor + room_w > width:
                room_w = width - x_cursor
            rooms.append(
                RoomPlacement(
                    name=name,
                    room_type=room_type,
                    x=round(x_cursor, 2),
                    y=round(y0, 2),
                    width=round(room_w, 2),
                    height=round(band_h, 2),
                )
            )
            x_cursor += room_w

    doors = []
    windows = []
    for room in rooms:
        door_x = room.x + min(3.0, room.width / 2)
        doors.append({"x1": round(door_x, 2), "y1": round(room.y, 2), "x2": round(door_x + 3, 2), "y2": round(room.y, 2)})
        if brief.maximize_natural_light or room.room_type in {"living", "bedroom", "study"}:
            windows.append(
                {
                    "x1": round(room.x + room.width * 0.2, 2),
                    "y1": round(room.y + room.height, 2),
                    "x2": round(room.x + room.width * 0.6, 2),
                    "y2": round(room.y + room.height, 2),
                }
            )

    return LayoutPlan(
        footprint_width_ft=width,
        footprint_height_ft=height,
        rooms=rooms,
        doors=doors,
        windows=windows,
    )
