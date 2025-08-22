from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import pandas as pd
import numpy as np

app = FastAPI()

# Load dataset
df = pd.read_csv("cleaned_movies.csv")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    columns = df.columns.tolist()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "columns": columns,
        "stats_result": None,
        "comparison_result": None
    })

@app.post("/get_stats", response_class=HTMLResponse)
def get_stats(request: Request, selected_column: str = Form(...)):
    columns = df.columns.tolist()
    stats = df[selected_column].describe().round(2).to_dict()
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "columns": columns,
        "stats_result": {
            "column": selected_column,
            "stats": stats
        },
        "comparison_result": None
    })

@app.post("/compare_columns", response_class=HTMLResponse)
def compare_columns(request: Request, column1: str = Form(...), column2: str = Form(...)):
    columns = df.columns.tolist()
    comp_stats = {
        "mean": (df[column1].mean(), df[column2].mean()),
        "std": (df[column1].std(), df[column2].std()),
        "min": (df[column1].min(), df[column2].min()),
        "max": (df[column1].max(), df[column2].max())
    }
    comp_stats = {k: (round(v[0], 2), round(v[1], 2)) for k, v in comp_stats.items()}
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "columns": columns,
        "stats_result": None,
        "comparison_result": {
            "col1": column1,
            "col2": column2,
            "data": comp_stats
        }
    })

@app.post("/compare_categories")
async def compare_categories(
    cat1: str = Form(...),
    cat2: str = Form(...),
    numeric_col: str = Form(...),
    top_n: int = Form(...)
):
    result = {}
    if cat1 in df.columns and cat2 in df.columns and numeric_col in df.columns:
        top_cat1 = df.groupby(cat1)[numeric_col].sum().sort_values(ascending=False).head(top_n).to_dict()
        top_cat2 = df.groupby(cat2)[numeric_col].sum().sort_values(ascending=False).head(top_n).to_dict()
        result = {
            f"Top {cat1}": top_cat1,
            f"Top {cat2}": top_cat2
        }
    return JSONResponse(content=result)

@app.post("/year_stats")
async def year_stats(year: int = Form(...)):
    if "Year" not in df.columns:
        return JSONResponse(content={"error": "No 'Year' column found."})

    filtered = df[df["Year"] == year]
    stats = {}

    if "Genres" in df.columns and not filtered["Genres"].empty:
        stats["top_genre"] = filtered["Genres"].mode().iloc[0]
    if "Original_Language" in df.columns and not filtered["Original_Language"].empty:
        stats["top_language"] = filtered["Original_Language"].mode().iloc[0]
    if "Production_Countries" in df.columns and not filtered["Production_Countries"].empty:
        stats["top_country"] = filtered["Production_Countries"].mode().iloc[0]

    return JSONResponse(content=stats)



