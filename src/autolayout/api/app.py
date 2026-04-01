from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI, HTTPException

from autolayout.core.brief_parser import parse_brief
from autolayout.core.drafting_engine import export_plan_to_dxf
from autolayout.core.layout_engine import generate_layout
from autolayout.core.revision_engine import apply_revision
from autolayout.models import ProjectState

app = FastAPI(title="AutoLayout CAD API", version="0.1.0")
PROJECTS: dict[str, ProjectState] = {}


@app.post("/projects")
def create_project(payload: dict):
    if "brief" not in payload:
        raise HTTPException(status_code=422, detail="brief is required")
    structured = parse_brief(payload["brief"])
    first_layout = generate_layout(structured)
    project_id = str(uuid4())
    PROJECTS[project_id] = ProjectState(project_id=project_id, brief=structured, versions=[first_layout])
    return {"project_id": project_id, "version": 1, "layout": asdict(first_layout)}


@app.post("/projects/{project_id}/revise")
def revise_project(project_id: str, payload: dict):
    state = PROJECTS.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    if "revision" not in payload:
        raise HTTPException(status_code=422, detail="revision is required")

    updated_brief = apply_revision(state.brief, payload["revision"])
    new_layout = generate_layout(updated_brief)
    state.brief = updated_brief
    state.versions.append(new_layout)

    return {"project_id": project_id, "version": len(state.versions), "layout": asdict(new_layout)}


@app.post("/projects/{project_id}/export")
def export_project(project_id: str):
    state = PROJECTS.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")

    latest = state.versions[-1]
    output = Path("artifacts") / project_id / f"v{len(state.versions)}.dxf"
    file_path = export_plan_to_dxf(latest, str(output))
    return {"project_id": project_id, "version": len(state.versions), "dxf_path": file_path}


@app.get("/projects/{project_id}")
def get_project(project_id: str):
    state = PROJECTS.get(project_id)
    if not state:
        raise HTTPException(status_code=404, detail="Project not found")
    return asdict(state)
