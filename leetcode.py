import pandas as pd


def top_three_salaries(
    employee: pd.DataFrame, department: pd.DataFrame
) -> pd.DataFrame:

    def rank_salary(df):
        df["salary_rank"] = df["salary"].rank(method="dense", ascending=False)
        return df[df["salary_rank"] <= 3]

    df = (
        employee.merge(department, left_on="departmentId", right_on="id", how="left")
        .groupby("departmentId")
        .apply(rank_salary)
    )

    df = (
        df[["name_y", "name_x", "salary"]]
        .rename(
            columns={"name_y": "Department", "name_x": "Employee", "salary": "Salary"}
        )
        .sort_values(["Department", "Salary"], ascending=[True, False])
    )

    return df
