import typer
from pathlib import Path
import os
import shutil
import sys
import requests

# Add the cli directory to the Python path
spai_cli_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(spai_cli_dir))

from cli.commands import hello
from cli import (
    load_and_validate_config,
    deploy_and_run_cloud,
    run_local,
)

app = typer.Typer()
app.add_typer(hello.app, name="hello")


@app.command()
def init():
    # ask for project name
    project = typer.prompt("Project name")
    # copy template
    template = Path(__file__).parent / "cli" / "project-template"
    shutil.copytree(template, Path(project))
    # change name to project in spai.config.yaml
    config = Path(project) / "spai.config.yml"
    os.system(f"sed -i 's/project-template/{project}/g' {config}")
    return typer.echo(f"Project {project} created")


@app.command()
def run(
    dir: Path = typer.Option(Path("."), "-d"),
    cloud: bool = typer.Option(False, "-c", "--cloud"),
    rebuild: bool = typer.Option(False, "-r", "--rebuild"),  # force rebuild image
):
    # make sure dir is absolute
    dir = Path(dir).resolve()
    # load and validate config
    config = load_and_validate_config(dir, typer, cloud)
    # print(config)
    # run project
    if cloud:
        return deploy_and_run_cloud(dir, config, typer, rebuild)
    return run_local(dir, config, typer)


# API_URL = "http://localhost:8000"
# API_URL = "http://148.113.137.45:8002"
API_URL = "https://spai.api.dev.earthpulse.ai"


@app.command()
def list(
    project: str = typer.Option(None, "-p", "--project"),
):
    project = "asd"
    response = requests.get(f"{API_URL}/projects/{project}")
    if response.status_code == 200:
        services = response.json()
        if len(services) == 0:
            return typer.echo(f"No services running in project '{project}'.")
        return typer.echo(f"Services in project '{project}': {services}")
    return typer.echo(response.json()["detail"])


@app.command()
def stop(
    project: str = typer.Option(None, "-p", "--project"),
):
    # list services
    project = "asd"
    response = requests.get(f"{API_URL}/projects/{project}")
    services = response.json()
    if len(services) == 0:
        return typer.echo(f"No services running in project '{project}'.")
    # delete services
    for service in services:
        service_type, name = service.split(".")
        typer.echo(f"Stopping service '{name}'...")
        response = requests.get(f"{API_URL}/stop/{service_type}/{name}")
        if response.status_code == 200:
            typer.echo(f"Stopped.")
        else:
            typer.echo("Something went wrong.")
            typer.echo(response.json()["detail"])
    return typer.echo(f"Stopped all scripts in project '{project}'.")


@app.command()
def logs(
    script: str,
):
    response = requests.get(f"{API_URL}/logs/script/{script}")
    if response.status_code == 200:
        typer.echo(response.json())
    else:
        typer.echo(response.json()["detail"])


if __name__ == "__main__":
    app()
