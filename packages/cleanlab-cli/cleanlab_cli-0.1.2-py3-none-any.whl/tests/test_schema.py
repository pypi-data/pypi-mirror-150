from click.testing import CliRunner
from cleanlab_cli.dataset.schema import (
    validate_schema_command,
    generate_schema_command,
    check_dataset_command,
)
from cleanlab_cli.util import read_file_as_df
import os
from os.path import dirname, abspath
import logging

logger = logging.getLogger(__name__)

sample_csv = os.path.join(abspath(dirname(__file__)), "resources/datasets/sample.csv")
sample_schema = os.path.join(abspath(dirname(__file__)), "resources/schemas/sample_schema.json")


def assert_success_else_error_output(test_name, result):
    if result.exit_code != 0:
        raise AssertionError(
            f"{test_name} failed with exit code {result.exit_code} and output: {result.output}"
        )


def test_generate():
    df = read_file_as_df(sample_csv)
    runner = CliRunner()
    with runner.isolated_filesystem():
        filename = "sample"

        df.to_csv(filename + ".csv")
        df.to_excel(filename + ".xlsx", index=False)
        # df.to_json(filename + ".json", orient="table", index=False)

        for ext in [".csv", ".xlsx"]:
            result = runner.invoke(
                generate_schema_command,
                [
                    "-f",
                    filename + ext,
                    "--id-column",
                    "tweet_id",
                    "--modality",
                    "text",
                    "--output",
                    "schema.json",
                ],
                input="n",
            )
            assert_success_else_error_output("Schema generation", result)


def test_validate():
    df = read_file_as_df(sample_csv)
    runner = CliRunner()
    with runner.isolated_filesystem():
        filename = "sample"

        df.to_csv(filename + ".csv")
        df.to_excel(filename + ".xlsx", index=False)
        # df.to_json(filename + ".json", orient="table", index=False)

        for ext in [".csv", ".xlsx"]:
            result = runner.invoke(
                validate_schema_command,
                ["--schema", sample_schema, "--filepath", filename + ext],
            )
            assert_success_else_error_output("Schema validation", result)


def test_check_dataset():
    df = read_file_as_df(sample_csv)
    runner = CliRunner()
    with runner.isolated_filesystem():
        filename = "sample"
        df.to_csv(filename + ".csv")
        df.to_excel(filename + ".xlsx", index=False)

        for ext in [".csv", ".xlsx"]:
            result = runner.invoke(
                check_dataset_command,
                [
                    "-f",
                    filename + ext,
                    "-s",
                    sample_schema,
                    "-o",
                    "text",
                    "--output",
                    "issues.json",
                ],
                input="n",
            )
            assert_success_else_error_output("Dataset check", result)


if __name__ == "__main__":
    test_generate()
    test_validate()
    test_check_dataset()
