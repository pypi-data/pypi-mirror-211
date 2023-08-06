import typer, os
from .runner import Runner

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
    current_dir = os.path.dirname(os.path.abspath(__file__))
    runner.start(
        f"{current_dir}/workspace/plugin_test.yaml",
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
