from __future__ import annotations

from pathlib import Path

import ezdxf

from autolayout.models import LayoutPlan


def export_plan_to_dxf(plan: LayoutPlan, output_path: str) -> str:
    doc = ezdxf.new("R2010")
    msp = doc.modelspace()

    layers = ["A-WALL", "A-DOOR", "A-WIND", "A-DIMS", "A-FURN", "A-TEXT"]
    for layer in layers:
        if layer not in doc.layers:
            doc.layers.add(name=layer)

    for room in plan.rooms:
        x0, y0 = room.x, room.y
        x1, y1 = room.x + room.width, room.y + room.height
        msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)], dxfattribs={"layer": "A-WALL"})
        msp.add_text(
            f"{room.name} ({round(room.width * room.height, 1)} sqft)",
            dxfattribs={"height": 0.7, "layer": "A-TEXT"},
        ).set_placement((x0 + 0.5, y0 + room.height / 2))

    for door in plan.doors:
        msp.add_line((door["x1"], door["y1"]), (door["x2"], door["y2"]), dxfattribs={"layer": "A-DOOR"})

    for window in plan.windows:
        msp.add_line((window["x1"], window["y1"]), (window["x2"], window["y2"]), dxfattribs={"layer": "A-WIND"})

    msp.add_linear_dim(
        base=(0, -2),
        p1=(0, 0),
        p2=(plan.footprint_width_ft, 0),
        angle=0,
        dxfattribs={"layer": "A-DIMS"},
    ).render()

    msp.add_linear_dim(
        base=(-2, 0),
        p1=(0, 0),
        p2=(0, plan.footprint_height_ft),
        angle=90,
        dxfattribs={"layer": "A-DIMS"},
    ).render()

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    doc.saveas(out)
    return str(out)
