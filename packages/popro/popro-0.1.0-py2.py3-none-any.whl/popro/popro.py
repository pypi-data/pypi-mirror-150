"""
Popro - Population Projection

"""
import os

import pandas as pd


def get_pop_place_census_age(df_census, place, age):

    df_census_age = df_census[
        (df_census["place"] == place) & (df_census["age"] == age)
    ]

    # raose amount registers
    if df_census_age.shape[0] == 0:
        raise ValueError(
            "Did not find records at the Census dataset for Place: {}, Age: {}".format(
                place, age
            )
        )
    if df_census_age.shape[0] > 1:
        raise ValueError(
            "Found multiple records in the Census dataset for Place: {}, Age: {}".format(
                place, age
            )
        )
    quantity = df_census_age.iloc[0]["population"]
    return quantity


def get_pop_year_place(df_population, place, year):

    df_population_age = df_population[
        (df_population["place"] == place) & (df_population["year"] == year)
    ]

    # test amount registers found
    if df_population_age.shape[0] == 0:
        raise ValueError(
            "Did not find records at the Population dataset for Place: {}, year: {}".format(
                place, year
            )
        )
    if df_population_age.shape[0] > 1:
        raise ValueError(
            "Found multiple records in the Population dataset for Place: {}, year: {}".format(
                place, year
            )
        )
    quantity = df_population_age.iloc[0]["population"]
    return quantity


def get_births_year_place(df_births, place, year):

    df_births_year = df_births[
        (df_births["place"] == place) & (df_births["year"] == year)
    ]

    # raise amount registers
    if df_births_year.shape[0] == 0:
        raise ValueError(
            "Did not find records at the Births dataset for Place: {}, year: {}".format(
                place, year
            )
        )
    if df_births_year.shape[0] > 1:
        raise ValueError(
            "Found multiple records in the Births dataset for Place: {}, year: {}".format(
                place, year
            )
        )
    quantity = df_births_year.iloc[0]["births"]
    return quantity


def via_census(datasets, year, place, age, verbose=False, **kwargs):

    year_census = kwargs.get("year_census")
    age_census = age - (year - year_census)

    pop_place_census_year = get_pop_place_census_age(
        datasets["df_census"], place, age_census
    )
    pop_place_census = get_pop_year_place(
        datasets["df_population"], place, year_census
    )
    pop_place_target_year = get_pop_year_place(
        datasets["df_population"], place, year
    )

    # debug
    if verbose:
        str_calc_label = f"pop_{place}_{year_census}_age_{age_census} * (pop_{place}_{year} / pop_{place}_{year_census})"
        str_calc_value = f"{pop_place_census_year} * ({pop_place_target_year} / {pop_place_census})"
        print(str_calc_label)
        print(str_calc_value)

    quantity = pop_place_census_year * (
        pop_place_target_year / pop_place_census
    )
    return quantity


def via_births(datasets, year, place, age, verbose=False, **kwargs):

    birth_year = year - age
    birth_place_birth_year = get_births_year_place(
        datasets["df_births"], place, year=birth_year
    )
    pop_place_birth_year = get_pop_year_place(
        datasets["df_population"], place, birth_year
    )
    pop_place_target_year = get_pop_year_place(
        datasets["df_population"], place, year
    )

    # debug
    if verbose:
        str_calc_label = f"birth_{place}_year_{birth_year} * (pop_{place}_{year} / pop_{place}_{birth_year})"
        str_calc_value = f"{birth_place_birth_year} * ({pop_place_target_year} / {pop_place_birth_year})"
        print(str_calc_label)
        print(str_calc_value)

    quantity = birth_place_birth_year * (
        pop_place_target_year / pop_place_birth_year
    )
    return quantity


def get_projection_engine(year, age, year_census):

    if year <= year_census:
        raise ValueError(":year_census: must be less than :year: ")
    if age < 0:
        raise ValueError(":age: cannot be negative")

    ano_nasc = year - age
    if ano_nasc <= year_census:
        projection_type = via_census
    else:
        projection_type = via_births
    return projection_type


def get_projection(datasets, year, place, age, year_census, verbose=False):

    do_projection = get_projection_engine(year, age, year_census)
    quantity = do_projection(
        datasets, year, place, age, verbose, year_census=year_census
    )
    return quantity


def intersection_list(list_list_place):
    def intersec(list1, list2):
        list3 = [value for value in list1 if value in list2]
        return list3

    for i in range(len(list_list_place) - 1):
        if i == 0:
            list_agg = intersec(list_list_place[i], list_list_place[i + 1])
        else:
            list_agg = intersec(list_agg, list_list_place[i + 1])

    return list_agg


def get_list_variables(df_datasets, year_census):

    # age
    list_age = df_datasets["df_census"]["age"].unique().tolist()

    # place
    list_place_census = df_datasets["df_census"]["place"].unique().tolist()
    list_place_births = df_datasets["df_births"]["place"].unique().tolist()
    list_place_population = (
        df_datasets["df_population"]["place"].unique().tolist()
    )
    list_place = intersection_list(
        [list_place_census, list_place_births, list_place_population]
    )

    # year
    list_year = list(df_datasets["df_population"]["year"].unique())
    list_year.sort()
    list_year.remove(year_census)

    # wrapup
    dict_list_variables = {
        "list_year": list_year,
        "list_place": list_place,
        "list_age": list_age,
    }
    return dict_list_variables


def projection_all(df_datasets, year_census):

    # load list variables
    dict_list_variables = get_list_variables(df_datasets, year_census)
    list_year = dict_list_variables["list_year"]
    list_place = dict_list_variables["list_place"]
    list_age = dict_list_variables["list_age"]

    # do projections for all combinations
    list_dict_projection = []
    list_dict_error = []
    for year in list_year:
        for place in list_place:
            for age in list_age:
                try:
                    quantity = get_projection(
                        df_datasets, year, place, age, year_census
                    )
                except Exception as e:
                    # save error info in list of dict
                    dict_error = {
                        "year": year,
                        "place": place,
                        "age": age,
                        "error": str(e),
                    }
                    list_dict_error.append(dict_error)
                    continue
                # save projection info in list of dict
                dict_projection = {
                    "year": year,
                    "place": place,
                    "age": age,
                    "quantity": quantity,
                }
                list_dict_projection.append(dict_projection)

    # pack projection and error data, as a dict
    dict_reports = {
        "report_projection": list_dict_projection,
        "report_error": list_dict_error,
    }
    return dict_reports


def validate_dataset_columns(dataframe, dataset_name, columns_required):
    """_summary_

    Args:
        dataframe (DataFrame): _description_
        dataset_name (str): _description_
        columns_required (set): _description_

    Raises:
        ValueError: _description_
    """

    if columns_required.issubset(set(list(dataframe.columns))):
        return True
    else:
        raise ValueError(
            f'"{dataset_name}" must have the following columns: "{columns_required}"'
        )


def validate_dataset_census(df_census):

    validate_dataset_columns(
        df_census, "df_census", set(["age", "population", "place", "year"])
    )


def validate_dataset_births(df_births):

    validate_dataset_columns(
        df_births, "df_births", set(["year", "place", "births"])
    )


class Popro:
    def __init__(self, path_census, path_births, path_population, year_census):
        self.path_census = path_census
        self.path_births = path_births
        self.path_population = path_population
        self.year_census = year_census

        self.df_census = pd.read_csv(path_census)  # age,population,place,year
        self.df_births = pd.read_csv(path_births)  # year,place,births
        self.df_population = pd.read_csv(
            path_population
        )  # year,place,population
        self.datasets = {
            "df_census": self.df_census,
            "df_births": self.df_births,
            "df_population": self.df_population,
        }
        self.report_projection = [{}]
        self.report_error = [{}]

    def project(self, year, place, age, verbose=False):
        quantity = get_projection(
            self.datasets,
            year,
            place,
            age,
            year_census=self.year_census,
            verbose=verbose,
        )
        return quantity

    def project_all(
        self, output_report_projection_path="", output_report_error_path=""
    ):
        """
        return: DataFrame
        """
        dict_reports = projection_all(self.datasets, self.year_census)
        self.report_projection = dict_reports["report_projection"]
        self.report_error = dict_reports["report_error"]

        if output_report_projection_path != "":
            save_report(self.report_projection, output_report_projection_path)
        if output_report_error_path != "":
            save_report(self.report_error, output_report_error_path)
        return self.report_projection


def save_report(list_dict, path_report):

    df_report = pd.DataFrame(list_dict)
    df_report.to_csv(path_report, index=False)
    return df_report
