from __future__ import annotations

from io import BytesIO

import pandas as pd

from .utils import to_dataframe


def export_csv_bytes(leads: list[dict]) -> bytes:
    return to_dataframe(leads).to_csv(index=False).encode("utf-8")


def export_excel_bytes(leads: list[dict]) -> bytes:
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        frame = to_dataframe(leads)
        frame.to_excel(writer, index=False, sheet_name="Leads")
        summary = frame.groupby("status", dropna=False).size().reset_index(name="count")
        summary.to_excel(writer, index=False, sheet_name="Summary")
    return output.getvalue()
