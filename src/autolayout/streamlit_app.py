from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

import streamlit as st

from autolayout.core.brief_parser import parse_brief
from autolayout.core.drafting_engine import export_plan_to_dxf
from autolayout.core.layout_engine import generate_layout
from autolayout.core.revision_engine import apply_revision


st.set_page_config(page_title="AutoLayout CAD", layout="wide")
st.title("Automated Layout & Drafting System (AutoCAD/BIM First Pass)")

if "brief" not in st.session_state:
    st.session_state.brief = None
if "layout_versions" not in st.session_state:
    st.session_state.layout_versions = []

col1, col2 = st.columns([2, 1])
with col1:
    brief_text = st.text_area(
        "Client brief",
        value="3BHK, 1500 sq ft, open kitchen, 1 study, maximize natural light",
        height=120,
    )
with col2:
    st.markdown("### Example")
    st.caption("3BHK, 1500 sq ft, open kitchen, 1 study, maximize natural light")

if st.button("Generate First Pass", type="primary"):
    parsed = parse_brief(brief_text)
    layout = generate_layout(parsed)
    st.session_state.brief = parsed
    st.session_state.layout_versions = [layout]

if st.session_state.layout_versions:
    latest = st.session_state.layout_versions[-1]
    st.success(f"Generated Version {len(st.session_state.layout_versions)}")

    st.subheader("Structured Program")
    st.json(asdict(st.session_state.brief))

    st.subheader("Room Layout")
    st.dataframe(
        [
            {
                "name": r.name,
                "type": r.room_type,
                "x": r.x,
                "y": r.y,
                "width": r.width,
                "height": r.height,
                "area": round(r.width * r.height, 2),
            }
            for r in latest.rooms
        ],
        use_container_width=True,
    )

    rev_col, export_col = st.columns(2)
    with rev_col:
        revision = st.text_input("Revision instruction", "increase study size")
        if st.button("Apply Revision"):
            updated = apply_revision(st.session_state.brief, revision)
            new_layout = generate_layout(updated)
            st.session_state.brief = updated
            st.session_state.layout_versions.append(new_layout)
            st.rerun()

    with export_col:
        if st.button("Export DXF"):
            version = len(st.session_state.layout_versions)
            out = Path("artifacts") / f"streamlit_v{version}.dxf"
            path = export_plan_to_dxf(latest, str(out))
            st.info(f"DXF saved at: {path}")
