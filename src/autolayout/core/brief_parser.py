from __future__ import annotations

import re
from collections import defaultdict

from autolayout.models import RoomRequirement, StructuredBrief


DEFAULT_ROOM_SHARE = {
    "living": 0.18,
    "dining": 0.1,
    "kitchen": 0.1,
    "bedroom": 0.16,
    "study": 0.08,
    "bathroom": 0.06,
    "utility": 0.04,
}


def parse_brief(text: str) -> StructuredBrief:
    lower = text.lower()

    bhk_match = re.search(r"(\d+)\s*bhk", lower)
    bhk = int(bhk_match.group(1)) if bhk_match else 2

    area_match = re.search(r"(\d{3,5})\s*(sq\s*ft|sqft|square\s*feet)", lower)
    total_area = float(area_match.group(1)) if area_match else 1200.0

    open_kitchen = "open kitchen" in lower
    maximize_natural_light = "natural light" in lower or "maximize light" in lower

    room_counts = defaultdict(int)
    room_counts["bedroom"] = bhk
    room_counts["living"] = 1
    room_counts["dining"] = 1
    room_counts["kitchen"] = 1
    room_counts["bathroom"] = max(2, bhk)

    study_match = re.search(r"(\d+)\s*study", lower)
    if "study" in lower:
        room_counts["study"] = int(study_match.group(1)) if study_match else 1

    if "utility" in lower:
        room_counts["utility"] = 1

    rooms = []
    for room_type, count in room_counts.items():
        share = DEFAULT_ROOM_SHARE.get(room_type, 0.08)
        area_per = max(60.0, (total_area * share) / max(1, count))
        adjacency = []
        if room_type == "kitchen":
            adjacency = ["dining", "living"] if open_kitchen else ["dining"]
        elif room_type == "study":
            adjacency = ["living"]
        elif room_type == "bedroom":
            adjacency = ["bathroom"]
        rooms.append(
            RoomRequirement(
                room_type=room_type,
                name=room_type,
                count=count,
                target_area_sqft=round(area_per, 2),
                adjacency_pref=adjacency,
            )
        )

    return StructuredBrief(
        raw_text=text,
        bhk=bhk,
        total_area_sqft=total_area,
        maximize_natural_light=maximize_natural_light,
        open_kitchen=open_kitchen,
        rooms=rooms,
        constraints={"zoning": "public/private/service"},
    )
