import pandas as pd


class MultiTableCheck():

    def __init__(self, io, sheet_name, **kwargs):
        if type(sheet_name) in [str, int]:
            sheet_name = [sheet_name]

        self._checks = {}
        self._sheets = pd.read_excel(io, sheet_name=sheet_name, **kwargs)

    def check(self, json_check):
        result = "success"

        if json_check.get("sheet") not in self._sheets:
            result = "failure: " + json_check.get("sheet") + " does not exits"
        else:
            sheet = self._sheets.get(json_check.get("sheet"))

            for column in json_check.get("columns"):
                if column.get("name") not in sheet.columns:
                    result = "failure: " + column.get("name") + " does not exits"
                    break

                if column.get("eq"):
                    sheet = sheet.loc[((sheet[column.get("name")].isin(column.get("eq"))) & (~sheet[column.get("name")].isna()))]
                    if sheet.empty:
                        result = "failure: " + column.get("name") + " does not meet criteria"
                        break

                if column.get("ne"):
                    sheet = sheet.loc[((~sheet[column.get("name")].isin(column.get("ne"))) & (~sheet[column.get("name")].isna()))]
                    if sheet.empty:
                        result = "failure: " + column.get("name") + " does not meet criteria"
                        break

                if column.get("lt"):
                    sheet = sheet.loc[sheet[column.get("name")] < min(column.get("lt"))]
                    if sheet.empty:
                        result = "failure: " + column.get("name") + " does not meet criteria"
                        break

                if column.get("gt"):
                    sheet = sheet.loc[sheet[column.get("name")] > max(column.get("gt"))]
                    if sheet.empty:
                        result = "failure: " + column.get("name") + " does not meet criteria"
                        break

                if column.get("le"):
                    sheet = sheet.loc[sheet[column.get("name")] <= min(column.get("le"))]
                    if sheet.empty:
                        result = "failure: " + column.get("name") + " does not meet criteria"
                        break

                if column.get("ge"):
                    sheet = sheet.loc[sheet[column.get("name")] >= min(column.get("ge"))]
                    if sheet.empty:
                        result = "failure: " + column.get("name") + " does not meet criteria"
                        break

        if result == "success":
            sheet = sheet.iloc[0]
            self._checks[json_check["name"]] = {"sheet": json_check["sheet"], "result": result, "row": sheet}
        else:
            self._checks[json_check["name"]] = {"sheet": json_check["sheet"], "result": result, "row": pd.DataFrame()}

    def fetch(self, check, column):
        if check in self._checks:
            return self._checks[check]["row"].get(column, float("nan"))
        return float("nan")

    def score(self):
        return self._checks
