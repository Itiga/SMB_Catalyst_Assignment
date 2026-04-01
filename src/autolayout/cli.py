from __future__ import annotations

import argparse

from autolayout.core.brief_parser import parse_brief
from autolayout.core.drafting_engine import export_plan_to_dxf
from autolayout.core.layout_engine import generate_layout


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate first-pass floor plan DXF from brief")
    parser.add_argument("brief", type=str, help="Unstructured client brief")
    parser.add_argument("--out", type=str, default="artifacts/plan.dxf", help="Output DXF path")
    args = parser.parse_args()

    brief = parse_brief(args.brief)
    plan = generate_layout(brief)
    path = export_plan_to_dxf(plan, args.out)
    print(path)


if __name__ == "__main__":
    main()
