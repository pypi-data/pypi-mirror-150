"""Console script for popro."""
import os
import sys
from email.policy import default

import click

import popro


@click.command()
@click.option("-ic", "--input_census", "path_census", type=click.STRING)
@click.option("-ib", "--input_birth", "path_births", type=click.STRING)
@click.option(
    "-ip", "--input_population", "path_population", type=click.STRING
)
@click.option("-yc", "--year_census", "year_census", type=click.INT)
@click.option("-y", "--year", "year", type=click.INT)
@click.option("-p", "--place", "place", type=click.INT)
@click.option("-a", "--age", "age", type=click.INT)
@click.option("-o", "--output", "output_path", type=click.STRING, default="")
@click.option("-oe", "--outerr", "output_error", type=click.STRING, default="")
@click.option("-v", "--verbose", default=False)
def main(
    path_census,
    path_births,
    path_population,
    year_census,
    year,
    place,
    age,
    output_path="",
    output_error="",
    verbose=False,
):
    """Console script for popro."""
    if path_census is None:
        click.echo("For help, type: popro --help")
        return

    engine = popro.Popro(
        path_census, path_births, path_population, year_census
    )

    if output_path != "":
        engine.project_all(output_path, output_error)
    else:
        population = engine.project(year, place, age, verbose)
        print(population)


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
