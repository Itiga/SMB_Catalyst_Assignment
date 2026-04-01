from autolayout.core.brief_parser import parse_brief
from autolayout.core.layout_engine import generate_layout
from autolayout.core.revision_engine import apply_revision


def test_parse_brief_extracts_core_fields():
    brief = parse_brief("3BHK, 1500 sq ft, open kitchen, 1 study, maximize natural light")
    assert brief.bhk == 3
    assert brief.total_area_sqft == 1500
    assert brief.open_kitchen is True
    assert brief.maximize_natural_light is True


def test_layout_generation_creates_rooms_and_openings():
    brief = parse_brief("2BHK, 1200 sq ft, open kitchen")
    layout = generate_layout(brief)
    assert len(layout.rooms) >= 6
    assert len(layout.doors) == len(layout.rooms)
    assert layout.footprint_width_ft > 0
    assert layout.footprint_height_ft > 0


def test_revision_adjusts_area_targets():
    brief = parse_brief("2BHK, 1200 sq ft, 1 study")
    updated = apply_revision(brief, "increase study size")
    study_before = [r.target_area_sqft for r in brief.rooms if r.room_type == "study"][0]
    study_after = [r.target_area_sqft for r in updated.rooms if r.room_type == "study"][0]
    assert study_after > study_before
