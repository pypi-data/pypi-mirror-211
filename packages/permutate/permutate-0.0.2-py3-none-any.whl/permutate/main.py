import typer
from .runner import Runner
from permutate import get_root_directory

app = typer.Typer()


@app.callback()
def callback():
    """
    Permutate is an automated testing framework for LLM Plugins.
    """


@app.command()
def start_sample():
    """
    Start the sample job
    """
    runner = Runner()
    runner.start(
        f"{get_root_directory()}/tests/files/plugin_test.yaml",
        save_to_html=True,
        save_to_csv=False
    )


@app.command()
def start(file_path: str, save_to_html=True, save_to_csv=True):
    """
    Start the batch permutation job
    """
    runner = Runner()
    runner.start(file_path, save_to_html, save_to_csv)
