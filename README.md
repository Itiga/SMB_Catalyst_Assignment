# SMB_Catalyst_Assignment

## AutoLayout & Drafting System (Streamlit + DXF)

This project converts an unstructured architecture brief into a first-pass floor plan and exports editable DXF output.

### What it does
1. Parse unstructured brief text (BHK, area, open kitchen, study, natural light).
2. Generate a zoned layout (public/private/service).
3. Place basic doors and windows.
4. Iterate from natural-language revision instructions.
5. Export editable DXF for AutoCAD workflow.

## Run from GitHub code

### 1) Clone
```bash
git clone <your-github-repo-url>
cd SMB_Catalyst_Assignment
```

### 2) Create environment and install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3) Launch Streamlit UI (recommended)
```bash
PYTHONPATH=src streamlit run src/autolayout/streamlit_app.py
```

Then open the local URL shown in terminal (usually `http://localhost:8501`).

### 4) (Optional) Run API
```bash
PYTHONPATH=src uvicorn autolayout.api.app:app --reload
```

### 5) Run tests
```bash
PYTHONPATH=src pytest -q
```

## Streamlit workflow
1. Enter client brief and click **Generate First Pass**.
2. Review structured requirements + room table.
3. Add revision text (example: `increase study size`) and click **Apply Revision**.
4. Click **Export DXF** to save a file in `artifacts/`.

## Notes
- This is first-pass planning automation, not final construction drawings.
- Output is intentionally editable so architects can override and refine quickly.
