from __future__ import annotations

import re

from autolayout.models import StructuredBrief


def apply_revision(brief: StructuredBrief, instruction: str) -> StructuredBrief:
    from copy import deepcopy

    updated = deepcopy(brief)
    lower = instruction.lower()

    for room in updated.rooms:
        if room.name in lower or room.room_type in lower:
            if "increase" in lower or "bigger" in lower:
                room.target_area_sqft = round(room.target_area_sqft * 1.15, 2)
            if "decrease" in lower or "smaller" in lower:
                room.target_area_sqft = round(room.target_area_sqft * 0.9, 2)

    add_study = re.search(r"add\s+(\d+)?\s*study", lower)
    if add_study:
        amount = int(add_study.group(1)) if add_study.group(1) else 1
        for room in updated.rooms:
            if room.room_type == "study":
                room.count += amount
                break

    if "open kitchen" in lower:
        updated.open_kitchen = True

    if "more natural light" in lower or "maximize natural light" in lower:
        updated.maximize_natural_light = True

    return updated
