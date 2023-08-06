#!/usr/bin/env python

"""Tests for `popro` package."""

import pandas as pd
import pytest
from click.testing import CliRunner

from popro import cli, popro


class Test_get_project_engine:
    def test_via_births_2019_8(self):

        project_engine = popro.get_projection_engine(
            year=2019, age=8, year_census=2010
        )
        assert project_engine == popro.via_births

    def test_via_census_2019_9(self):

        project_engine = popro.get_projection_engine(
            year=2019, age=9, year_census=2010
        )
        assert project_engine == popro.via_census

    def test_via_census_2019_10(self):

        project_engine = popro.get_projection_engine(
            year=2019, age=10, year_census=2010
        )
        assert project_engine == popro.via_census

    def test_year_census_smaller_than_year(self):

        with pytest.raises(ValueError):
            popro.get_projection_engine(year=2009, age=10, year_census=2010)

    def test_age_smaller_than_0(self):

        with pytest.raises(ValueError):
            popro.get_projection_engine(year=2019, age=-1, year_census=2010)

    def test_age_equal_0(self):

        try:
            popro.get_projection_engine(year=2019, age=0, year_census=2010)
        except ValueError:
            raise pytest.fail("Raise {0}".format(ValueError))


class Test_dataset:

    def test_dataset_census_columns_ok(self):
        df_census = pd.DataFrame(data=[[0, 100, 1100015, 2010],
                                       [1, 200, 1100015, 2010]],
                                 columns=["age", "population", "place", "year"]
                                 )
        try:
            popro.validate_dataset_census(df_census)
        except ValueError:
            raise pytest.fail("Raise {0}".format(ValueError))


    def test_dataset_census_columns_fail(self):
        df_census = pd.DataFrame(data=[[0, 100, 1100015, 2010],
                                       [1, 200, 1100015, 2010]],
                                 columns=["age", "population", "local", "year"]
                                 )
        with pytest.raises(ValueError):
            popro.validate_dataset_census(df_census)

class Test_get_pop_place_census_age:
    def test_none_register_found(self):
        list_dict = [
            {
                "age": 0,
                "population": 100,
                "place": 1100015,
                "year": 2010,
            },
            {
                "age": 1,
                "population": 200,
                "place": 1100015,
                "year": 2010,
            },
            {
                "age": 2,
                "population": 150,
                "place": 1100015,
                "year": 2010,
            },
        ]
        df_census = pd.DataFrame(list_dict)
        with pytest.raises(ValueError):
            popro.get_pop_place_census_age(
                df_census=df_census, place=1100015, age=3
            )

    def test_one_register_found(self):

        # fmt: off
        list_df = [
            {"age": 0, "population": 100, "place": 1100015, "year": 2010},
            {"age": 1, "population": 200, "place": 1100015, "year": 2010},
            {"age": 2, "population": 150, "place": 1100015, "year": 2010}
            ]
        df_census = pd.DataFrame(list_df)
        qtd=popro.get_pop_place_census_age(df_census=df_census, place=1100015,age=2)
        assert qtd == 150

    def test_multiple_register_found(self):

        # fmt: off
        list_df = [
            {"age": 0, "population": 100, "place": 1100015, "year": 2010},
            {"age": 2, "population": 200, "place": 1100015, "year": 2010},
            {"age": 2, "population": 150, "place": 1100015, "year": 2010}
            ]
        df_census = pd.DataFrame(list_df)
        with pytest.raises(ValueError):
            popro.get_pop_place_census_age(df_census=df_census, place=1100015,age=2)

        # def test_command_line_interface():
        #     """Test the CLI."""
        #     runner = CliRunner()
        #     result = runner.invoke(cli.main)
        #     # assert result.exit_code == 0
        #     assert "popro.cli.main" in result.output
        #     help_result = runner.invoke(cli.main, ["--help"])
        #     assert help_result.exit_code == 0
        #     assert "--help  Show this message and exit." in help_result.output
