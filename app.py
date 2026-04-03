import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import json

st.set_page_config(page_title="Team Time Dashboard – March 2026", layout="wide")

# ── Color Palette ──────────────────────────────────────────
DEV_COLOR = "#4f46e5"
MTG_COLOR = "#f59e0b"
GREEN = "#10b981"
RED = "#ef4444"

CLIENT_COLORS = {
    "KFH": "#0ea5e9", "DET": "#8b5cf6", "ENEO": "#f97316", "UAQ": "#ec4899",
    "RTA": "#84cc16", "Fotopia": "#94a3b8", "Demos": "#6366f1", "Digitizeme": "#10b981",
}
GRP_COLORS = {
    "Fotognize": "#8b5cf6", "Capture": "#f59e0b", "Fotofind": "#3b82f6",
    "Fototracker": "#0ea5e9", "CTC Application": "#ec4899", "DET Project": "#8b5cf6",
    "Internal": "#94a3b8", "Demos": "#10b981", "Fotoverifai": "#f43f5e", "Other": "#cbd5e1",
}
WT_COLORS = {"Bug Fix": "#ef4444", "Feature": "#10b981", "Support": "#3b82f6", "Unknown": "#94a3b8", "Meeting": "#f59e0b"}

# ── User Data ──────────────────────────────────────────────
USERS = {
    "Omar Mohamed": {"dev": 123.02, "mtg": 11.4, "total": 134.42, "full": True, "c": {"Fotopia": 92.69, "ENEO": 29.93, "KFH": 11.8}, "p": {"Foto Gnize V2": 108.27, "Foto GnizeV1": 26.16}, "w": {"Unknown": 121.16, "Meeting": 11.4, "Bug Fix": 1.86}},
    "Deema": {"dev": 115.73, "mtg": 18.37, "total": 134.1, "full": True, "c": {"Fotopia": 102.32, "KFH": 31.78}, "p": {"FotoCapture V6.6": 68.3, "KFH – FotoGnize": 31.78, "FotoCapture": 30.98, "FotoCapture V6.7": 3.04}, "w": {"Unknown": 104.99, "Meeting": 18.37, "Bug Fix": 10.07, "Feature": 0.67}},
    "Engy Ahmed": {"dev": 75.83, "mtg": 55.58, "total": 131.42, "full": True, "c": {"KFH": 46.42, "Fotopia": 39.5, "Digitizeme": 39.5, "ENEO": 6}, "p": {"Foto Gnize V2": 91.92, "Fotofind AI": 39.5}, "w": {"Meeting": 55.58, "Unknown": 73.33, "Bug Fix": 2.5}},
    "Yousef Eid": {"dev": 126, "mtg": 0, "total": 126, "full": True, "c": {"Fotopia": 126}, "p": {"Foto Gnize V2": 84, "Foto GnizeV1": 42}, "w": {"Unknown": 105, "Feature": 21}},
    "Sameh Amnoun": {"dev": 53.25, "mtg": 59, "total": 112.25, "full": True, "c": {"Fotopia": 103.5, "ENEO": 4, "Digitizeme": 3.75, "UAQ": 0.5, "RTA": 0.5}, "p": {"FotoCapture": 68.17, "Fotofind": 33.75, "Fotopia": 4.58, "Foto Gnize V2": 2.5, "Miscellaneous": 1.25, "Fotoverifai": 1, "FotoGnize": 1}, "w": {"Meeting": 59, "Unknown": 43.25, "Bug Fix": 10}},
    "Daniel Lewis": {"dev": 87.67, "mtg": 23.83, "total": 111.5, "full": True, "c": {"Fotopia": 87.25, "ENEO": 14, "UAQ": 10.25}, "p": {"FotoCapture V6.7": 40.58, "FotoCapture": 39.67, "FotoCapture V6.6": 17.42, "FotoCapture V6.5": 11.5, "Miscellaneous": 1.83, "Fotocapture Testing": 0.5}, "w": {"Bug Fix": 30.08, "Unknown": 34.17, "Meeting": 23.83, "Feature": 23.42}},
    "Omar Alaa": {"dev": 103.56, "mtg": 7.1, "total": 110.66, "full": False, "c": {"DET": 66.59, "Fotopia": 39.26, "UAQ": 4.8}, "p": {"Fototracker": 66.59, "FotoCapture": 38.11, "Fotofind": 5.95}, "w": {"Unknown": 65.58, "Feature": 36.57, "Meeting": 7.1, "Bug Fix": 1.4}},
    "Prajwal S.": {"dev": 104, "mtg": 6, "total": 110, "full": False, "c": {"Fotopia": 110}, "p": {"FotoScan": 110}, "w": {"Unknown": 80, "Bug Fix": 6, "Feature": 18, "Meeting": 6}},
    "Aesha H.": {"dev": 98.42, "mtg": 0, "total": 98.42, "full": True, "c": {"Fotopia": 98.42}, "p": {"Fotocapture Testing": 52.58, "Miscellaneous": 27.92, "Fotofind": 17.92}, "w": {"Unknown": 98.42}},
    "Nour Helal": {"dev": 80.25, "mtg": 13.5, "total": 93.75, "full": True, "c": {"Fotopia": 93.75}, "p": {"Foto Gnize V2": 93.75}, "w": {"Meeting": 13.5, "Unknown": 46, "Bug Fix": 17, "Feature": 17.25}},
    "Mohammed Y.": {"dev": 68.04, "mtg": 6.99, "total": 75.03, "full": False, "c": {"Fotopia": 75.03}, "p": {"Fotopia": 75.03}, "w": {"Unknown": 22.89, "Feature": 10.63, "Bug Fix": 34.52, "Meeting": 6.99}},
    "Nancy A.": {"dev": 73.76, "mtg": 0, "total": 73.76, "full": False, "c": {"Fotopia": 73.76}, "p": {"Fotopia": 73.76}, "w": {"Unknown": 72.13, "Bug Fix": 1.64}},
    "Ali Murtaza": {"dev": 32.33, "mtg": 24.17, "total": 56.5, "full": False, "c": {"Fotopia": 23.33, "Internal": 20.17, "DET": 13}, "p": {"Fotofind": 23, "Demo Support": 20.17, "DET": 13, "Global Pharma": 0.33}, "w": {"Unknown": 20.33, "Bug Fix": 12, "Meeting": 24.17}},
    "Jumana Yasser": {"dev": 52.73, "mtg": 0, "total": 52.73, "full": False, "c": {"Fotopia": 52.73}, "p": {"R&D": 52.73}, "w": {"Unknown": 52.73}},
    "AbdulRahman S.": {"dev": 33.84, "mtg": 7.8, "total": 41.64, "full": False, "c": {"Fotopia": 41.64}, "p": {"Fotopia": 41.64}, "w": {"Unknown": 33.84, "Meeting": 7.8}},
    "Ibrahim A.": {"dev": 37.53, "mtg": 1.55, "total": 39.08, "full": False, "c": {"Fotopia": 39.08}, "p": {"Fotofind": 36.75, "FotoCapture V6.6": 2.01, "FotoCapture": 0.32}, "w": {"Unknown": 25.53, "Meeting": 1.55, "Feature": 12}},
    "Ahmed Abouzaid": {"dev": 12.84, "mtg": 12.47, "total": 25.31, "full": False, "c": {"Fotopia": 25.31}, "p": {"Foto Gnize V2": 25.31}, "w": {"Meeting": 12.47, "Unknown": 12.84}},
    "Jihad M.": {"dev": 20.5, "mtg": 1.75, "total": 22.25, "full": False, "c": {"Fotopia": 21.25, "Digitizeme": 1}, "p": {"Fotofind": 22.25}, "w": {"Meeting": 1.75, "Bug Fix": 10.5, "Unknown": 10}},
    "Nagwa": {"dev": 6.98, "mtg": 4.32, "total": 11.3, "full": False, "c": {"Fotopia": 11.3}, "p": {"Foto Gnize V2": 11.15, "FotoGnize": 0.15}, "w": {"Meeting": 4.32, "Unknown": 6.98}},
    "Ahmed Alaa": {"dev": 5, "mtg": 0, "total": 5, "full": False, "c": {"Fotopia": 5}, "p": {"Fotoverifai": 5}, "w": {"Unknown": 5}},
    "Thejaswini N.": {"dev": 2.93, "mtg": 0, "total": 2.93, "full": False, "c": {"KFH": 2.93}, "p": {"KFH – CTC Application": 2.93}, "w": {"Unknown": 2.8, "Feature": 0.13}},
    "Ijaz Ahmed": {"dev": 0, "mtg": 0, "total": 0, "full": True, "c": {}, "p": {}, "w": {}},
    "Muzamil S.": {"dev": 0, "mtg": 0, "total": 0, "full": True, "c": {}, "p": {}, "w": {}},
    "Farah Eid": {"dev": 0, "mtg": 0, "total": 0, "full": True, "c": {}, "p": {}, "w": {}},
}

CAP_BASE = {
    "Yousef Eid": 119.5, "Nour Helal": 119.5, "Engy Ahmed": 119.5, "Deema": 119.5,
    "Daniel Lewis": 119.5, "Omar Mohamed": 119.5, "Sameh Amnoun": 119.5,
    "Aesha H.": 119.5, "Ijaz Ahmed": 119.5, "Muzamil S.": 119.5, "Farah Eid": 119.5,
}

# ── Client Stats ───────────────────────────────────────────
CLIENT_STATS = {
    "Fotopia": {"dev": 1077.4, "mtg": 203.9, "total": 1281.29},
    "ENEO": {"dev": 45.68, "mtg": 8.25, "total": 53.93},
    "DET": {"dev": 76.38, "mtg": 3.21, "total": 79.59},
    "KFH": {"dev": 67.35, "mtg": 25.57, "total": 92.92},
    "Digitizeme": {"dev": 32.33, "mtg": 11.92, "total": 44.25},
    "UAQ": {"dev": 15.05, "mtg": 0.5, "total": 15.55},
    "RTA": {"dev": 0, "mtg": 0.5, "total": 0.5},
}

# ── Product Stats ──────────────────────────────────────────
PRODUCT_STATS = {
    "Foto Gnize V2": {"dev": 325.78, "mtg": 91.11, "total": 416.89, "group": "Fotognize"},
    "Fotopia": {"dev": 178.14, "mtg": 16.88, "total": 195.02, "group": "Internal"},
    "FotoCapture": {"dev": 114.22, "mtg": 63.02, "total": 177.24, "group": "Capture"},
    "Fotofind": {"dev": 112.22, "mtg": 27.4, "total": 139.62, "group": "Fotofind"},
    "FotoScan": {"dev": 104, "mtg": 6, "total": 110, "group": "Other"},
    "FotoCapture V6.6": {"dev": 83.83, "mtg": 3.9, "total": 87.73, "group": "Capture"},
    "Foto GnizeV1": {"dev": 68.16, "mtg": 0, "total": 68.16, "group": "Fotognize"},
    "Fototracker": {"dev": 63.38, "mtg": 3.21, "total": 66.59, "group": "Fototracker"},
    "Fotocapture Testing": {"dev": 52.58, "mtg": 0.5, "total": 53.08, "group": "Capture"},
    "R&D": {"dev": 52.73, "mtg": 0, "total": 52.73, "group": "Internal"},
    "FotoCapture V6.7": {"dev": 42.13, "mtg": 1.5, "total": 43.63, "group": "Capture"},
    "Fotofind AI": {"dev": 30.83, "mtg": 8.67, "total": 39.5, "group": "Fotofind"},
    "KFH - CTC Application": {"dev": 2.93, "mtg": 0, "total": 2.93, "group": "CTC Application"},
    "KFH - FotoGnize": {"dev": 24.13, "mtg": 7.65, "total": 31.78, "group": "Fotognize"},
    "Miscellaneous": {"dev": 29.17, "mtg": 1.83, "total": 31, "group": "Internal"},
    "Demo Support": {"dev": 0, "mtg": 20.17, "total": 20.17, "group": "Demos"},
    "DET": {"dev": 13, "mtg": 0, "total": 13, "group": "Other"},
    "FotoCapture V6.5": {"dev": 10.75, "mtg": 0.75, "total": 11.5, "group": "Capture"},
    "Fotoverifai": {"dev": 5.75, "mtg": 0.25, "total": 6, "group": "Fotoverifai"},
    "FotoGnize": {"dev": 0.15, "mtg": 1, "total": 1.15, "group": "Fotognize"},
}

# ── Work Type Stats ────────────────────────────────────────
WORK_TYPE_STATS = {
    "Bug Fix": {"hrs": 137.57, "count": 75},
    "Feature": {"hrs": 139.68, "count": 57},
    "Support": {"hrs": 0, "count": 0},
    "Unknown": {"hrs": 1036.96, "count": 460},
    "Meeting": {"hrs": 253.84, "count": 232},
}

# ── Daily Data ─────────────────────────────────────────────
DAILY_DATA = [
    {"d": "Mar 1", "dev": 49.93, "mtg": 13.65}, {"d": "Mar 2", "dev": 66.73, "mtg": 13.28},
    {"d": "Mar 3", "dev": 60.86, "mtg": 13.21}, {"d": "Mar 4", "dev": 65.15, "mtg": 6.35},
    {"d": "Mar 5", "dev": 71.35, "mtg": 5.16}, {"d": "Mar 6", "dev": 35.74, "mtg": 0},
    {"d": "Mar 7", "dev": 31.65, "mtg": 0}, {"d": "Mar 8", "dev": 48.51, "mtg": 7.44},
    {"d": "Mar 9", "dev": 76.95, "mtg": 8.89}, {"d": "Mar 10", "dev": 77.08, "mtg": 13.25},
    {"d": "Mar 11", "dev": 56.93, "mtg": 11.26}, {"d": "Mar 12", "dev": 53.35, "mtg": 15.65},
    {"d": "Mar 13", "dev": 27.4, "mtg": 2.28}, {"d": "Mar 14", "dev": 19.55, "mtg": 3},
    {"d": "Mar 15", "dev": 68.38, "mtg": 26.21}, {"d": "Mar 16", "dev": 74.17, "mtg": 7.66},
    {"d": "Mar 17", "dev": 60.47, "mtg": 8.08}, {"d": "Mar 18", "dev": 43.96, "mtg": 7.59},
    {"d": "Mar 19", "dev": 17.18, "mtg": 0}, {"d": "Mar 20", "dev": 0.13, "mtg": 0},
    {"d": "Mar 21", "dev": 4.76, "mtg": 0}, {"d": "Mar 22", "dev": 6.96, "mtg": 0},
    {"d": "Mar 23", "dev": 8.71, "mtg": 0}, {"d": "Mar 24", "dev": 36.63, "mtg": 12.42},
    {"d": "Mar 25", "dev": 48.73, "mtg": 22.49}, {"d": "Mar 26", "dev": 54.29, "mtg": 19.12},
    {"d": "Mar 27", "dev": 29.24, "mtg": 3.4}, {"d": "Mar 28", "dev": 21.69, "mtg": 1.81},
    {"d": "Mar 29", "dev": 27.05, "mtg": 12.58}, {"d": "Mar 30", "dev": 43.61, "mtg": 12.88},
    {"d": "Mar 31", "dev": 27.07, "mtg": 6.18},
]

# ── Attribution / DevOps Data ──────────────────────────────
ATTRIBUTION = {
    "Omar Alaa": {"dn": "Omar Alaa", "total": 84, "qaFlow": 8, "inferred": 76, "byType": {"Bug": 9, "Feature": 4, "Task": 71}, "cx": {"Low": 71, "Medium": 4, "High": 9}, "bySV": {"Foto Capture": 10, "Iteration 1": 64, "Sprint11": 9, "Foto Find": 1}, "cycleTime": None, "prs": {"authored": 16, "reviewed": 0, "approved": 0, "merged": 16, "reopened": 0}, "dataSource": "live"},
    "Daniel Lewis": {"dn": "Daniel Lewis", "total": 25, "qaFlow": 19, "inferred": 6, "byType": {"Bug": 21, "Feature": 0, "Task": 4}, "cx": {"Low": 4, "Medium": 0, "High": 21}, "bySV": {"Foto Capture": 25}, "cycleTime": None, "prs": {"authored": 8, "reviewed": 0, "approved": 0, "merged": 8, "reopened": 0}, "dataSource": "live"},
    "Sameh Amnoun": {"dn": "Sameh Amnoun", "total": 16, "qaFlow": 15, "inferred": 1, "byType": {"Bug": 10, "Feature": 4, "Task": 2}, "cx": {"Low": 2, "Medium": 4, "High": 10}, "bySV": {"Foto Capture": 14, "Sprint11": 1, "Foto Find": 1}, "cycleTime": None, "prs": {"authored": 0, "reviewed": 55, "approved": 55, "merged": 0, "reopened": 0}, "dataSource": "live"},
    "Muzamil S.": {"dn": "Muzamil S.", "total": 13, "qaFlow": 4, "inferred": 9, "byType": {"Bug": 4, "Feature": 1, "Task": 8}, "cx": {"Low": 8, "Medium": 1, "High": 4}, "bySV": {"Foto Find": 13}, "cycleTime": None, "prs": {"authored": 16, "reviewed": 16, "approved": 16, "merged": 16, "reopened": 0}, "dataSource": "live"},
    "Deema": {"dn": "Deema", "total": 9, "qaFlow": 9, "inferred": 0, "byType": {"Bug": 5, "Feature": 4, "Task": 0}, "cx": {"Low": 0, "Medium": 4, "High": 5}, "bySV": {"Foto Capture": 9}, "cycleTime": None, "prs": {"authored": 9, "reviewed": 0, "approved": 0, "merged": 9, "reopened": 0}, "dataSource": "live"},
    "Thejaswini N.": {"dn": "Thejaswini N.", "total": 7, "qaFlow": 0, "inferred": 7, "byType": {"Bug": 1, "Feature": 3, "Task": 3}, "cx": {"Low": 3, "Medium": 3, "High": 1}, "bySV": {"KFH": 7}, "cycleTime": None, "prs": {"authored": 5, "reviewed": 0, "approved": 0, "merged": 5, "reopened": 0}, "dataSource": "live"},
    "Ibrahim A.": {"dn": "Ibrahim A.", "total": 3, "qaFlow": 3, "inferred": 0, "byType": {"Bug": 1, "Feature": 2, "Task": 0}, "cx": {"Low": 0, "Medium": 2, "High": 1}, "bySV": {"Foto Capture": 2, "Foto Find": 1}, "cycleTime": None, "prs": {"authored": 20, "reviewed": 0, "approved": 0, "merged": 20, "reopened": 0}, "dataSource": "live"},
    "Omar Mohamed": {"dn": "Omar Mohamed", "total": 2, "qaFlow": 0, "inferred": 2, "byType": {"Bug": 0, "Feature": 0, "Task": 2}, "cx": {"Low": 2, "Medium": 0, "High": 0}, "bySV": {"Version 1.6": 2}, "cycleTime": None, "prs": {"authored": 4, "reviewed": 0, "approved": 0, "merged": 4, "reopened": 0}, "dataSource": "live"},
    "Jihad M.": {"dn": "Jihad M.", "total": 1, "qaFlow": 0, "inferred": 1, "byType": {"Bug": 0, "Feature": 0, "Task": 1}, "cx": {"Low": 1, "Medium": 0, "High": 0}, "bySV": {"Foto Find": 1}, "cycleTime": None, "prs": {"authored": 3, "reviewed": 0, "approved": 0, "merged": 3, "reopened": 0}, "dataSource": "live"},
    "Engy Ahmed": {"dn": "Engy Ahmed", "total": 1, "qaFlow": 0, "inferred": 1, "byType": {"Bug": 0, "Feature": 0, "Task": 1}, "cx": {"Low": 1, "Medium": 0, "High": 0}, "bySV": {"Version 1.6": 1}, "cycleTime": None, "prs": {"authored": 1, "reviewed": 1, "approved": 1, "merged": 1, "reopened": 0}, "dataSource": "live"},
    "Yousef Eid": {"dn": "Yousef Eid", "total": 0, "qaFlow": 0, "inferred": 0, "byType": {"Bug": 0, "Feature": 0, "Task": 0}, "cx": {"Low": 0, "Medium": 0, "High": 0}, "bySV": {}, "cycleTime": None, "prs": {"authored": 4, "reviewed": 3, "approved": 3, "merged": 4, "reopened": 0}, "dataSource": "live-only"},
    "Nour Helal": {"dn": "Nour Helal", "total": 0, "qaFlow": 0, "inferred": 0, "byType": {"Bug": 0, "Feature": 0, "Task": 0}, "cx": {"Low": 0, "Medium": 0, "High": 0}, "bySV": {}, "cycleTime": None, "prs": {"authored": 3, "reviewed": 4, "approved": 4, "merged": 3, "reopened": 0}, "dataSource": "live-only"},
    "Prajwal S.": {"dn": "Prajwal S.", "total": 0, "qaFlow": 0, "inferred": 0, "byType": {"Bug": 0, "Feature": 0, "Task": 0}, "cx": {"Low": 0, "Medium": 0, "High": 0}, "bySV": {}, "cycleTime": None, "prs": {"authored": 2, "reviewed": 0, "approved": 0, "merged": 2, "reopened": 0}, "dataSource": "live-only"},
    "Mohamed M.": {"dn": "Mohamed M.", "total": 0, "qaFlow": 0, "inferred": 0, "byType": {"Bug": 0, "Feature": 0, "Task": 0}, "cx": {"Low": 0, "Medium": 0, "High": 0}, "bySV": {}, "cycleTime": None, "prs": {"authored": 0, "reviewed": 3, "approved": 3, "merged": 0, "reopened": 0}, "dataSource": "live-only"},
    "Aesha H.": {"dn": "Aesha H.", "total": 0, "qaFlow": 0, "inferred": 0, "byType": {"Bug": 0, "Feature": 0, "Task": 0}, "cx": {"Low": 0, "Medium": 0, "High": 0}, "bySV": {}, "cycleTime": None, "prs": {"authored": 0, "reviewed": 0, "approved": 0, "merged": 0, "reopened": 0}, "dataSource": "no-data"},
    "Ijaz Ahmed": {"dn": "Ijaz Ahmed", "total": 0, "qaFlow": 0, "inferred": 0, "byType": {"Bug": 0, "Feature": 0, "Task": 0}, "cx": {"Low": 0, "Medium": 0, "High": 0}, "bySV": {}, "cycleTime": None, "prs": {"authored": 0, "reviewed": 0, "approved": 0, "merged": 0, "reopened": 0}, "dataSource": "no-data"},
    "Farah Eid": {"dn": "Farah Eid", "total": 0, "qaFlow": 0, "inferred": 0, "byType": {"Bug": 0, "Feature": 0, "Task": 0}, "cx": {"Low": 0, "Medium": 0, "High": 0}, "bySV": {}, "cycleTime": None, "prs": {"authored": 0, "reviewed": 0, "approved": 0, "merged": 0, "reopened": 0}, "dataSource": "no-data"},
}

# ── Vacation Days ──────────────────────────────────────────
VACATION_DAYS = {
    "Yousef Eid": {"ramadan": 0, "regular": 0}, "Nour Helal": {"ramadan": 0, "regular": 0},
    "Engy Ahmed": {"ramadan": 0, "regular": 0}, "Deema": {"ramadan": 0, "regular": 0},
    "Daniel Lewis": {"ramadan": 0, "regular": 0}, "Omar Mohamed": {"ramadan": 0, "regular": 0},
    "Sameh Amnoun": {"ramadan": 0, "regular": 0}, "Aesha H.": {"ramadan": 0, "regular": 0},
    "Ijaz Ahmed": {"ramadan": 0, "regular": 0}, "Muzamil S.": {"ramadan": 0, "regular": 0},
    "Farah Eid": {"ramadan": 0, "regular": 0},
}


# ── Helper Functions ───────────────────────────────────────
def get_cap(name, vac=None):
    base = CAP_BASE.get(name)
    if base is None:
        return None
    v = (vac or {}).get(name, {"ramadan": 0, "regular": 0})
    return max(0, base - v["ramadan"] * 5.5 - v["regular"] * 7)


def filter_users(users, role="All", selected_members=None):
    filtered = {}
    for name, v in users.items():
        if selected_members and name not in selected_members:
            continue
        if role == "FT" and not v["full"]:
            continue
        if role == "PT" and v["full"]:
            continue
        if role == "QA" and not any(q in name.lower() for q in ["aesha", "ijaz", "farah"]):
            continue
        if role == "Dev" and (not v["full"] or any(q in name.lower() for q in ["aesha", "ijaz", "farah"])):
            continue
        filtered[name] = v
    return filtered


def dv_weighted(cx):
    return cx.get("High", 0) * 3 + cx.get("Medium", 0) * 2 + cx.get("Low", 0)


def dv_avg_complexity(cx):
    t = cx.get("High", 0) + cx.get("Medium", 0) + cx.get("Low", 0)
    if not t:
        return None
    s = dv_weighted(cx) / t
    return "High" if s >= 2.3 else ("Medium" if s >= 1.4 else "Low")


def dv_role(d):
    rev = d["prs"].get("reviewed", 0) + d["prs"].get("approved", 0)
    auth = d["prs"].get("authored", 0)
    tick = d.get("total", 0)
    dlv = tick * 2 + auth
    if d.get("dataSource") == "live-only":
        return "ADO Only"
    if rev > dlv * 1.5 and rev >= 8:
        return "Review-heavy"
    if dlv > rev * 1.2 and (tick >= 8 or auth >= 8):
        return "Delivery-heavy"
    return "Balanced"


# ══════════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════════
st.markdown("""
<div style="display:flex;align-items:center;justify-content:space-between;padding:8px 0;margin-bottom:10px">
    <div>
        <h1 style="margin:0;font-size:1.5rem">Team Time Dashboard</h1>
        <p style="margin:0;font-size:0.8rem;color:#718096">Nourhan Hosny's Workspace &middot; 24 members &middot; 827 entries &middot; 161 tickets &middot; 91 PRs &middot; Updated 01/04/2026</p>
    </div>
    <span style="background:#eef2ff;color:#4f46e5;font-size:0.8rem;font-weight:700;padding:4px 14px;border-radius:20px">March 2026</span>
</div>
""", unsafe_allow_html=True)

# ── Sidebar Filters ────────────────────────────────────────
with st.sidebar:
    st.header("Filters")
    role_filter = st.selectbox("Role", ["All", "FT (Full-time)", "PT (Part-time)", "Dev", "QA"])
    role_key = role_filter.split(" ")[0]
    all_names = sorted(USERS.keys())
    selected_members = st.multiselect("Team Members", all_names, default=[])

    st.divider()
    st.subheader("Vacation Days (Full-timers)")
    st.caption("Ramadan day = 5.5h deducted, Regular day = 7h deducted")
    vac = {}
    for name in sorted(CAP_BASE.keys()):
        with st.expander(name, expanded=False):
            r = st.number_input(f"Ramadan days off", 0, 14, 0, key=f"vr_{name}")
            g = st.number_input(f"Regular days off", 0, 6, 0, key=f"vg_{name}")
            vac[name] = {"ramadan": r, "regular": g}

users = filter_users(USERS, role_key, selected_members if selected_members else None)
ft_names = [n for n in users if users[n]["full"]]

# ══════════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════════
tab_ov, tab_pr, tab_cl, tab_wt, tab_ut, tab_dv = st.tabs(
    ["Overview", "Products", "Clients", "Work Types", "Utilization", "DevOps Delivery"]
)

# ══════════════════════════════════════════════════════════
# TAB: OVERVIEW
# ══════════════════════════════════════════════════════════
with tab_ov:
    tot_dev = sum(v["dev"] for v in users.values())
    tot_mtg = sum(v["mtg"] for v in users.values())
    tot_hrs = sum(v["total"] for v in users.values())
    dev_eff = tot_dev / tot_hrs * 100 if tot_hrs > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Hours", f"{tot_hrs:,.0f}")
    c2.metric("Dev Hours", f"{tot_dev:,.0f}")
    c3.metric("Meeting Hours", f"{tot_mtg:,.0f}")
    c4.metric("Dev Efficiency", f"{dev_eff:.0f}%")

    # Team bar chart + donut
    col_bar, col_donut = st.columns([2, 1])
    with col_bar:
        st.subheader("Hours by Team Member")
        sort_by = st.radio("Sort by", ["total", "dev", "mtg"], horizontal=True, key="team_sort")
        sorted_users = sorted(users.items(), key=lambda x: x[1][sort_by], reverse=True)
        names = [x[0] for x in sorted_users]
        dev_vals = [x[1]["dev"] for x in sorted_users]
        mtg_vals = [x[1]["mtg"] for x in sorted_users]
        exp_vals = [get_cap(n, vac) for n in names]

        fig = go.Figure()
        fig.add_trace(go.Bar(name="Development", x=names, y=dev_vals, marker_color=DEV_COLOR))
        fig.add_trace(go.Bar(name="Meetings", x=names, y=mtg_vals, marker_color=MTG_COLOR))
        fig.add_trace(go.Scatter(
            name="Expected", x=[n for n, e in zip(names, exp_vals) if e is not None],
            y=[e for e in exp_vals if e is not None],
            mode="lines+markers", line=dict(color=RED, width=2, dash="dash"),
            marker=dict(size=5, color=RED),
        ))
        fig.update_layout(barmode="stack", height=400, margin=dict(t=10, b=60),
                          legend=dict(orientation="h", yanchor="bottom", y=1.02))
        fig.update_xaxes(tickangle=-35)
        fig.update_yaxes(title_text="Hours")
        st.plotly_chart(fig, use_container_width=True)

    with col_donut:
        st.subheader("Dev vs Meeting")
        fig_d = go.Figure(go.Pie(
            labels=["Development", "Meetings"], values=[round(tot_dev), round(tot_mtg)],
            hole=0.6, marker_colors=[DEV_COLOR, MTG_COLOR],
            textinfo="label+percent", textfont_size=11,
        ))
        fig_d.update_layout(height=350, margin=dict(t=10, b=10), showlegend=False)
        st.plotly_chart(fig_d, use_container_width=True)
        st.caption(f"{tot_dev:,.0f}h dev · {tot_mtg:,.0f}h meetings")

    # Daily activity
    st.subheader("Daily Activity")
    st.caption("Dev vs meeting per day · shaded = Eid holiday (Mar 19-23)")
    df_daily = pd.DataFrame(DAILY_DATA)
    fig_daily = go.Figure()
    fig_daily.add_trace(go.Bar(name="Development", x=df_daily["d"], y=df_daily["dev"], marker_color=DEV_COLOR))
    fig_daily.add_trace(go.Bar(name="Meetings", x=df_daily["d"], y=df_daily["mtg"], marker_color=MTG_COLOR))
    fig_daily.add_shape(type="rect", x0="Mar 19", x1="Mar 23", y0=0, y1=1, yref="paper", fillcolor="rgba(0,0,0,0.06)", line_width=0)
    fig_daily.add_annotation(x="Mar 21", y=1.05, yref="paper", text="Eid Holiday", showarrow=False, font=dict(size=10, color="#718096"))
    fig_daily.update_layout(barmode="stack", height=250, margin=dict(t=30, b=30),
                            legend=dict(orientation="h", yanchor="bottom", y=1.02))
    fig_daily.update_yaxes(title_text="Hours")
    st.plotly_chart(fig_daily, use_container_width=True)

    # Above/Below expected + PR Reviewers
    col_pr, col_ab = st.columns(2)
    with col_pr:
        st.subheader("PR Reviewers")
        pr_data = []
        for k, d in ATTRIBUTION.items():
            rev = d["prs"].get("reviewed", 0)
            auth = d["prs"].get("authored", 0)
            if rev > 0 or auth > 0:
                role_label = "Lead Reviewer" if rev >= 20 else ("Active Reviewer" if rev >= 5 else ("Author" if auth >= 10 else "-"))
                pr_data.append({"Reviewer": d["dn"], "PRs Reviewed": rev, "PRs Authored": auth, "Role": role_label})
        if pr_data:
            df_pr = pd.DataFrame(pr_data).sort_values("PRs Reviewed", ascending=False)
            st.dataframe(df_pr, hide_index=True, use_container_width=True)

    with col_ab:
        st.subheader("Above / Below Expected Hours")
        st.caption("Full-timers only")
        ab_data = []
        for n in ft_names:
            cap = get_cap(n, vac) or 119.5
            delta = users[n]["total"] - cap
            ab_data.append({"name": n, "delta": round(delta, 1)})
        ab_data.sort(key=lambda x: x["delta"], reverse=True)
        fig_ab = go.Figure(go.Bar(
            x=[d["name"] for d in ab_data], y=[d["delta"] for d in ab_data],
            marker_color=[GREEN if d["delta"] >= 0 else RED for d in ab_data],
        ))
        fig_ab.update_layout(height=280, margin=dict(t=10, b=60))
        fig_ab.update_yaxes(title_text="Hours vs Expected")
        fig_ab.update_xaxes(tickangle=-30)
        st.plotly_chart(fig_ab, use_container_width=True)

    # Member table
    st.subheader("All Team Members")
    rows = []
    for name, v in sorted(users.items(), key=lambda x: x[1]["dev"], reverse=True):
        cap = get_cap(name, vac)
        eff = v["dev"] / v["total"] * 100 if v["total"] > 0 else 0
        delta = v["total"] - cap if cap is not None else None
        tix = ATTRIBUTION.get(name, {}).get("total", 0)
        pr_rev = ATTRIBUTION.get(name, {}).get("prs", {}).get("reviewed", 0)
        top_prods = sorted(v["p"].items(), key=lambda x: x[1], reverse=True)[:2]
        rows.append({
            "Name": name,
            "Dev Hrs": round(v["dev"], 1),
            "Mtg Hrs": round(v["mtg"], 1),
            "Total Hrs": round(v["total"], 1),
            "Expected": f"{cap:.1f}h" if cap else "-",
            "+/-": f"{delta:+.1f}h" if delta is not None else "-",
            "Dev %": f"{eff:.0f}%",
            "Tickets": tix if tix > 0 else "-",
            "PR Rev": pr_rev if pr_rev > 0 else "-",
            "Type": "Full" if v["full"] else "Part",
            "Top Products": ", ".join(p[0] for p in top_prods),
        })
    st.dataframe(pd.DataFrame(rows), hide_index=True, use_container_width=True, height=500)

# ══════════════════════════════════════════════════════════
# TAB: PRODUCTS
# ══════════════════════════════════════════════════════════
with tab_pr:
    # Group aggregation
    grp_map = {}
    for pname, pv in PRODUCT_STATS.items():
        g = pv["group"]
        if g not in grp_map:
            grp_map[g] = {"dev": 0, "mtg": 0, "total": 0}
        grp_map[g]["dev"] += pv["dev"]
        grp_map[g]["mtg"] += pv["mtg"]
        grp_map[g]["total"] += pv["total"]

    grp_order = ["Fotognize", "Capture", "Fotofind", "Fototracker", "Internal", "CTC Application", "Fotoverifai", "Demos", "Other"]
    grps = [g for g in grp_order if g in grp_map and grp_map[g]["total"] > 0.5]

    col_grp, col_mix = st.columns(2)
    with col_grp:
        st.subheader("Hours by Product Family")
        fig_pg = go.Figure()
        fig_pg.add_trace(go.Bar(name="Development", x=grps, y=[grp_map[g]["dev"] for g in grps], marker_color=DEV_COLOR))
        fig_pg.add_trace(go.Bar(name="Meetings", x=grps, y=[grp_map[g]["mtg"] for g in grps], marker_color=MTG_COLOR))
        fig_pg.update_layout(barmode="stack", height=350, margin=dict(t=10, b=30),
                              legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig_pg, use_container_width=True)

    with col_mix:
        st.subheader("Product Mix")
        fig_pm = go.Figure(go.Pie(
            labels=grps, values=[grp_map[g]["total"] for g in grps],
            hole=0.6, marker_colors=[GRP_COLORS.get(g, "#cbd5e1") for g in grps],
            textinfo="label+percent", textfont_size=10,
        ))
        fig_pm.update_layout(height=350, margin=dict(t=10, b=10), showlegend=False)
        st.plotly_chart(fig_pm, use_container_width=True)

    # Product table
    st.subheader("All Products")
    prod_rows = []
    for pname, pv in sorted(PRODUCT_STATS.items(), key=lambda x: x[1]["dev"], reverse=True):
        if pv["total"] <= 0:
            continue
        eff = pv["dev"] / pv["total"] * 100 if pv["total"] > 0 else 0
        prod_rows.append({
            "Product": pname, "Family": pv["group"],
            "Dev Hrs": round(pv["dev"], 1), "Mtg Hrs": round(pv["mtg"], 1),
            "Total Hrs": round(pv["total"], 1), "Dev %": f"{eff:.0f}%",
        })
    st.dataframe(pd.DataFrame(prod_rows), hide_index=True, use_container_width=True)

# ══════════════════════════════════════════════════════════
# TAB: CLIENTS
# ══════════════════════════════════════════════════════════
with tab_cl:
    # Client KPI cards
    client_order = ["Fotopia", "DET", "ENEO", "KFH", "UAQ", "Demos", "Digitizeme", "RTA"]
    valid_clients = [c for c in client_order if c in CLIENT_STATS]
    cols = st.columns(4)
    for i, cname in enumerate(valid_clients[:4]):
        cv = CLIENT_STATS[cname]
        eff = cv["dev"] / cv["total"] * 100 if cv["total"] > 0 else 0
        cols[i].metric(cname, f"{cv['total']:.1f}h", f"{eff:.0f}% dev")
    if len(valid_clients) > 4:
        cols2 = st.columns(4)
        for i, cname in enumerate(valid_clients[4:]):
            cv = CLIENT_STATS[cname]
            eff = cv["dev"] / cv["total"] * 100 if cv["total"] > 0 else 0
            cols2[i].metric(cname, f"{cv['total']:.1f}h", f"{eff:.0f}% dev")

    col_cb, col_cd = st.columns(2)
    with col_cb:
        st.subheader("Hours by Client")
        fig_cl = go.Figure()
        fig_cl.add_trace(go.Bar(name="Development", x=valid_clients,
                                y=[CLIENT_STATS[c]["dev"] for c in valid_clients],
                                marker_color=[CLIENT_COLORS.get(c, "#94a3b8") for c in valid_clients]))
        fig_cl.add_trace(go.Bar(name="Meetings", x=valid_clients,
                                y=[CLIENT_STATS[c]["mtg"] for c in valid_clients],
                                marker_color=[CLIENT_COLORS.get(c, "#94a3b8") + "66" for c in valid_clients]))
        fig_cl.update_layout(barmode="stack", height=320, margin=dict(t=10, b=30),
                              legend=dict(orientation="h", yanchor="bottom", y=1.02))
        st.plotly_chart(fig_cl, use_container_width=True)

    with col_cd:
        st.subheader("Client Mix")
        fig_cd = go.Figure(go.Pie(
            labels=valid_clients, values=[CLIENT_STATS[c]["total"] for c in valid_clients],
            hole=0.6, marker_colors=[CLIENT_COLORS.get(c, "#94a3b8") for c in valid_clients],
            textinfo="label+percent", textfont_size=10,
        ))
        fig_cd.update_layout(height=320, margin=dict(t=10, b=10), showlegend=False)
        st.plotly_chart(fig_cd, use_container_width=True)

    st.subheader("Classification Notes")
    st.markdown("""
- **DET** - All Fototracker project hours classified as DET this month. Additional DET entries detected via keyword matching.
- **ENEO / UAQ** - Detected via keyword matching in descriptions. Medium confidence; recommend adding client tags in Clockify.
- **KFH** - Includes KFH project entries plus entries where "KFH" appears in descriptions.
- **Fotopia (Internal)** - All work where no client keyword was found.
- **Digitizeme** - SaaS multi-tenant platform. 5 entries, 2.75h.
- **RTA** - 1 entry (0.5h meeting). Very low confidence; verify manually.
""")

# ══════════════════════════════════════════════════════════
# TAB: WORK TYPES
# ══════════════════════════════════════════════════════════
with tab_wt:
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Feature Work", "318h", "106 entries")
    c2.metric("Bug Fixes", "181h", "103 entries")
    c3.metric("Support", "144h", "102 entries")
    c4.metric("Unclassified", "618h", "253 entries")

    col_wt1, col_wt2 = st.columns(2)
    with col_wt1:
        st.subheader("Work Type Breakdown")
        wt_order = ["Feature", "Bug Fix", "Support", "Unknown", "Meeting"]
        fig_wt = go.Figure(go.Pie(
            labels=wt_order, values=[WORK_TYPE_STATS[w]["hrs"] for w in wt_order],
            hole=0.6, marker_colors=[WT_COLORS[w] for w in wt_order],
            textinfo="label+percent", textfont_size=10,
        ))
        fig_wt.update_layout(height=350, margin=dict(t=10, b=10))
        st.plotly_chart(fig_wt, use_container_width=True)

    with col_wt2:
        st.subheader("Work Type by Team Member")
        members_sorted = sorted(users.items(), key=lambda x: x[1]["total"], reverse=True)
        wt_dev_order = ["Bug Fix", "Feature", "Support", "Unknown"]
        fig_wtm = go.Figure()
        for wt in wt_dev_order:
            fig_wtm.add_trace(go.Bar(
                name=wt, x=[m[0] for m in members_sorted],
                y=[m[1]["w"].get(wt, 0) for m in members_sorted],
                marker_color=WT_COLORS[wt],
            ))
        fig_wtm.update_layout(barmode="stack", height=350, margin=dict(t=10, b=60),
                               legend=dict(orientation="h", yanchor="bottom", y=1.02))
        fig_wtm.update_xaxes(tickangle=-35)
        st.plotly_chart(fig_wtm, use_container_width=True)

    st.subheader("Classification Confidence Report")
    st.warning("253 entries (51%) could not be classified due to missing or unclear descriptions.")
    st.info("ENEO / UAQ client detection classified via keyword search (medium confidence). Recommend adding explicit client tags.")

    rules_data = [
        {"Work Type": "Bug Fix", "Keywords": "bug, fix, issue, defect, error, crash", "Entries": 75, "Hours": "137.57h", "Confidence": "High"},
        {"Work Type": "Feature", "Keywords": "develop, implement, build, creat, feature, integrat, refactor, design, architect", "Entries": 57, "Hours": "139.68h", "Confidence": "Medium"},
        {"Work Type": "Support", "Keywords": "support, cr, change request, troubleshoot", "Entries": 0, "Hours": "0h", "Confidence": "Medium"},
        {"Work Type": "Unknown", "Keywords": "no keyword found or no description", "Entries": 460, "Hours": "1,036.96h", "Confidence": "Low"},
        {"Work Type": "Meeting", "Keywords": "meeting, standup, sync, scrum, demo, review...", "Entries": 232, "Hours": "253.84h", "Confidence": "High"},
    ]
    st.dataframe(pd.DataFrame(rules_data), hide_index=True, use_container_width=True)

# ══════════════════════════════════════════════════════════
# TAB: UTILIZATION
# ══════════════════════════════════════════════════════════
with tab_ut:
    all_ft = [n for n in CAP_BASE if n in USERS]
    ft_valid = [n for n in all_ft if n in users]
    avg_log = sum(users[n]["total"] for n in ft_valid) / len(ft_valid) if ft_valid else 0
    avg_u = sum(users[n]["total"] / (get_cap(n, vac) or 119.5) * 100 for n in ft_valid) / len(ft_valid) if ft_valid else 0
    above = [n for n in ft_valid if users[n]["total"] >= (get_cap(n, vac) or 119.5)]
    below = [n for n in ft_valid if users[n]["total"] < (get_cap(n, vac) or 119.5)]

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Expected Capacity", "119.5h")
    c2.metric("Avg Utilization", f"{avg_u:.0f}%")
    c3.metric("Avg Hours Logged", f"{avg_log:.1f}h")
    c4.metric("Above Expected", str(len(above)))
    c5.metric("Below Expected", str(len(below)))
    c6.metric("Ramadan Adj.", "5.5h")

    # Util chart
    st.subheader("Full-Timer Utilization vs Expected")
    fts_sorted = sorted(ft_valid, key=lambda n: users[n]["total"] / (get_cap(n, vac) or 119.5), reverse=True)
    fig_util = go.Figure()
    bar_colors = []
    for n in fts_sorted:
        cap = get_cap(n, vac) or 119.5
        tot = users[n]["total"]
        bar_colors.append(GREEN if tot >= cap else (DEV_COLOR if tot >= cap * 0.8 else "#94a3b8"))
    fig_util.add_trace(go.Bar(name="Logged", x=fts_sorted, y=[users[n]["total"] for n in fts_sorted], marker_color=bar_colors))
    fig_util.add_trace(go.Scatter(
        name="Expected", x=fts_sorted, y=[get_cap(n, vac) or 119.5 for n in fts_sorted],
        mode="lines+markers", line=dict(color=RED, width=2, dash="dash"), marker=dict(size=6, color=RED),
    ))
    fig_util.update_layout(height=300, margin=dict(t=10, b=60), legend=dict(orientation="h", yanchor="bottom", y=1.02))
    fig_util.update_yaxes(title_text="Hours")
    st.plotly_chart(fig_util, use_container_width=True)

    # Full-timer detail table
    st.subheader("Full-Timer Detail")
    ft_rows = []
    for n in all_ft:
        v = USERS.get(n, {"dev": 0, "mtg": 0, "total": 0})
        cap = get_cap(n, vac) or 119.5
        pct = v["total"] / cap * 100 if cap > 0 else 0
        delta = v["total"] - cap
        vr = vac.get(n, {}).get("ramadan", 0)
        vreg = vac.get(n, {}).get("regular", 0)
        ft_rows.append({
            "Name": n,
            "Ramadan Days Off": vr,
            "Regular Days Off": vreg,
            "Expected": f"{cap:.1f}h",
            "Logged": f"{v['total']:.1f}h",
            "+/- Expected": f"{delta:+.1f}h",
            "Dev": f"{v['dev']:.1f}h",
            "Meetings": f"{v['mtg']:.1f}h",
            "Utilization": f"{pct:.0f}%",
        })
    st.dataframe(pd.DataFrame(ft_rows), hide_index=True, use_container_width=True)

    # Part-timer table
    st.subheader("Part-Timer Hours")
    pt_rows = []
    for name, v in sorted(users.items(), key=lambda x: x[1]["total"], reverse=True):
        if v["full"]:
            continue
        eff = v["dev"] / v["total"] * 100 if v["total"] > 0 else 0
        top_prods = sorted(v["p"].items(), key=lambda x: x[1], reverse=True)[:3]
        pt_rows.append({
            "Name": name, "Logged": f"{v['total']:.1f}h", "Dev": f"{v['dev']:.1f}h",
            "Meetings": f"{v['mtg']:.1f}h", "Dev %": f"{eff:.0f}%",
            "Top Products": ", ".join(p[0] for p in top_prods),
        })
    if pt_rows:
        st.dataframe(pd.DataFrame(pt_rows), hide_index=True, use_container_width=True)

# ══════════════════════════════════════════════════════════
# TAB: DEVOPS DELIVERY
# ══════════════════════════════════════════════════════════
with tab_dv:
    st.success(
        "**Live data - Azure DevOps org: Fotopiatech** | Attribution model: March 2026 | "
        "**172 closed tickets | 85 merged PRs** | "
        "Attribution rule: Credit goes to the last non-QA assignee in the ticket's assignment chain."
    )

    members_attr = list(ATTRIBUTION.items())
    tot_tix = sum(d["total"] for _, d in members_attr)
    qa_flow_t = sum(d["qaFlow"] for _, d in members_attr)
    inf_t = sum(d["inferred"] for _, d in members_attr)
    qa_conf_pct = round(qa_flow_t / tot_tix * 100) if tot_tix > 0 else 0
    tot_auth = sum(d["prs"]["authored"] for _, d in members_attr)
    tot_rev = sum(d["prs"]["reviewed"] for _, d in members_attr)

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Attributed Tickets", str(tot_tix))
    c2.metric("Via QA Flow", str(qa_flow_t))
    c3.metric("Inferred", str(inf_t))
    c4.metric("QA Confidence", f"{qa_conf_pct}%")
    c5.metric("PRs Authored", str(tot_auth))
    c6.metric("Avg Cycle Time", "-")

    # Role cards
    classified = [(n, d, dv_role(d)) for n, d in members_attr]
    dlv_list = [(n, d) for n, d, r in classified if r == "Delivery-heavy"]
    rvw_list = [(n, d) for n, d, r in classified if r == "Review-heavy"]
    bln_list = [(n, d) for n, d, r in classified if r == "Balanced"]
    ado_list = [(n, d) for n, d, r in classified if r == "ADO Only"]

    rc1, rc2, rc3 = st.columns(3)
    with rc1:
        st.markdown(f"**Delivery-heavy ({len(dlv_list)})**")
        for n, d in dlv_list:
            st.markdown(f"- {d['dn']} ({d['total']} tickets, {d['qaFlow']} QA-confirmed)")
        if not dlv_list:
            st.caption("None this month")
    with rc2:
        st.markdown(f"**Review-heavy ({len(rvw_list)})**")
        for n, d in rvw_list:
            st.markdown(f"- {d['dn']} ({d['prs']['reviewed']} reviews)")
        if not rvw_list:
            st.caption("None this month")
    with rc3:
        st.markdown(f"**Balanced ({len(bln_list)})**")
        for n, d in bln_list:
            st.markdown(f"- {d['dn']} ({d['total']} tickets)")
        if not bln_list:
            st.caption("None this month")

    if ado_list:
        st.markdown(f"**ADO-only ({len(ado_list)})** - Active in Azure DevOps, no Clockify time entry")
        for n, d in ado_list:
            st.markdown(f"- {d['dn']}")

    # Resource Delivery Table
    st.subheader("Resource Delivery Overview")
    dv_rows = []
    for name, d in sorted(members_attr, key=lambda x: x[1]["total"], reverse=True):
        tot = d["total"] or 1
        qc = round(d["qaFlow"] / d["total"] * 100) if d["total"] > 0 else 0
        ws = dv_weighted(d["cx"])
        avg_c = dv_avg_complexity(d["cx"]) or "-"
        role = dv_role(d)
        ct = f"{d['cycleTime']:.1f}d" if d["cycleTime"] else "-"
        sv_text = " | ".join(f"{s}: {c}" for s, c in d["bySV"].items())
        dv_rows.append({
            "Name": d["dn"], "Attributed": d["total"], "QA Flow%": f"{qc}%",
            "Bug": d["byType"]["Bug"], "Feature": d["byType"]["Feature"], "Task": d["byType"]["Task"],
            "PR Auth": d["prs"]["authored"], "PR Rev": d["prs"]["reviewed"],
            "PR Mrg": d["prs"]["merged"], "Wt. Score": ws, "Avg Cmplx": avg_c,
            "Cycle Time": ct, "Sprint Mix": sv_text, "Role": role,
        })
    st.dataframe(pd.DataFrame(dv_rows), hide_index=True, use_container_width=True, height=500)

    # Charts row
    col_wm, col_prc = st.columns(2)
    with col_wm:
        st.subheader("Work Type Mix per Resource")
        chart_order = sorted(members_attr, key=lambda x: x[1]["total"], reverse=True)
        c_labels = [d["dn"].split(" ")[0] for _, d in chart_order]
        fig_mix = go.Figure()
        fig_mix.add_trace(go.Bar(name="Bug Fix", x=c_labels, y=[d["byType"]["Bug"] for _, d in chart_order], marker_color="#ef4444"))
        fig_mix.add_trace(go.Bar(name="Feature", x=c_labels, y=[d["byType"]["Feature"] for _, d in chart_order], marker_color="#10b981"))
        fig_mix.add_trace(go.Bar(name="Task", x=c_labels, y=[d["byType"]["Task"] for _, d in chart_order], marker_color="#3b82f6"))
        fig_mix.update_layout(barmode="stack", height=350, margin=dict(t=10, b=60),
                               legend=dict(orientation="h", yanchor="bottom", y=1.02))
        fig_mix.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_mix, use_container_width=True)

    with col_prc:
        st.subheader("PR Activity")
        fig_pra = go.Figure()
        fig_pra.add_trace(go.Bar(name="Authored", x=c_labels, y=[d["prs"]["authored"] for _, d in chart_order], marker_color=DEV_COLOR))
        fig_pra.add_trace(go.Bar(name="Reviewed", x=c_labels, y=[d["prs"]["reviewed"] for _, d in chart_order], marker_color="#8b5cf6"))
        fig_pra.add_trace(go.Bar(name="Merged", x=c_labels, y=[d["prs"]["merged"] for _, d in chart_order], marker_color=GREEN))
        fig_pra.update_layout(height=350, margin=dict(t=10, b=60),
                               legend=dict(orientation="h", yanchor="bottom", y=1.02))
        fig_pra.update_xaxes(tickangle=-45)
        st.plotly_chart(fig_pra, use_container_width=True)

    # Quality Signals
    st.subheader("Quality Signals")
    flags = []
    for name, d in members_attr:
        dn = d["dn"]
        if d["total"] > 0 and d["qaFlow"] == 0:
            flags.append({"Name": dn, "Severity": "Low", "Signal": f"{d['total']} tickets - no QA handoff detected",
                          "Recommendation": "All attribution inferred. May not follow standard QA gate."})
        if d.get("dataSource") == "live-only":
            flags.append({"Name": dn, "Severity": "Low", "Signal": "ADO contributor - not in Clockify",
                          "Recommendation": "Verify time tracking."})
    flags.append({"Name": "Note", "Severity": "Low", "Signal": "Reopen rates shown as 0 unless revision history was fetched",
                  "Recommendation": "Accurate reopen counts require per-ticket revision-history queries."})
    st.dataframe(pd.DataFrame(flags), hide_index=True, use_container_width=True)

    # Sprint/Version Breakdown
    st.subheader("Sprint / Version Breakdown")
    all_sv = sorted(set(sv for _, d in members_attr for sv in d["bySV"]))
    sp_rows = []
    for name, d in sorted(members_attr, key=lambda x: x[1]["total"], reverse=True):
        row = {"Developer": d["dn"], "Total": d["total"]}
        for sv in all_sv:
            row[sv] = d["bySV"].get(sv, 0)
        sp_rows.append(row)
    if sp_rows:
        st.dataframe(pd.DataFrame(sp_rows), hide_index=True, use_container_width=True)

    # Attribution Model
    with st.expander("Attribution Model - No Silent Assumptions"):
        st.markdown("""
**Step 1 - QA-flow handoff (high confidence):** For each closed ticket, assignment history is fetched from Azure DevOps.
If the ticket was ever assigned to **Aesha Hassen** or **Ijaz Ahmed** (testers) or **Sameh Amnoun** (code reviewer),
the person assigned directly *before* that transition is credited as the delivering developer.

**Step 2 - Most-recent assignee (inferred, lower confidence):** If no QA handoff is found,
the most recent non-QA, non-reviewer assignee is credited.

**Exclusions:** Aesha, Ijaz, and Sameh are excluded from attribution - they are the gate, not the recipients.

**Role classification:** Delivery-heavy = ticket count x 2 + PRs authored > 1.2x review score and >= 8 tickets or PRs.
Review-heavy = >= 8 review/approve actions and review score > 1.5x delivery score. Balanced = neither threshold.

**Quality signal thresholds:** Reopen rate >= 15% = High, 8-14% = Medium. Cycle time > 1.6x team average flagged.
0% QA confidence flagged. ADO-only contributors flagged for time-tracking follow-up.
""")
