import os
import requests

# API_URL = "http://localhost:8000"
# API_URL = "http://148.113.137.45:8002"
API_URL = "https://spai.api.dev.earthpulse.ai"


def call_api(dir, endpoint, data, item_type):
    print(dir)
    return requests.post(
        f"{API_URL}/{endpoint}",
        files={
            item_type: open(
                dir / f'main.{"ipynb" if item_type == "notebook" else "py"}', "rb"
            ),
            "requirements": open(dir / "requirements.txt", "rb")
            if "requirements.txt" in os.listdir(dir)
            else None,
            "env": open(dir / ".env", "rb") if ".env" in os.listdir(dir) else None,
        },
        data=data,
    )


def run_item(item, dir, typer, config, rebuild, item_type):
    item_dir = dir / item.name
    typer.echo(f"Running item '{item.name}'...")
    data = {
        "name": item.name,
        "project": config.project,
        "rebuild": rebuild,
        "command": item.command,
    }
    if item_type == "api":
        data["port"] = item.port
    else:
        data["command"] = item.command
    if item_type != "ui":
        data["storage"] = item.storage
    response = call_api(
        item_dir,
        f"run/{item_type}",
        data,
        item_type,
    )
    if response.status_code == 200:
        print(response.json())
    else:
        typer.echo("Something went wrong.")
        typer.echo(response.json()["detail"])


def run_script_or_notebook(item, dir, typer, config, rebuild, item_type):
    item_dir = dir / item.name
    if item.run_on_start:
        return run_item(item, dir, typer, config, rebuild, item_type)
    if item.run_every:
        typer.echo(f"Setting up cronjob for item '{item.name}'...")
        response = call_api(
            item_dir,
            f"schedule/{item_type}",
            {
                "name": item.name,
                "project": config.project,
                "run_every": item.run_every,
                "storage": item.storage,
                "rebuild": rebuild,
            },
            item_type,
        )
        if response.status_code == 200:
            print(response.json())
        else:
            typer.echo("Something went wrong.")
            typer.echo(response.json()["detail"])


def check_item(item, services, typer, item_type):
    name = f"{item_type}.{item.name}"
    if name in services:
        typer.echo(f"Service '{name}' already deployed.")
        typer.echo(f"Stopping ...")  # confirm
        response = requests.get(f"{API_URL}/stop/{item_type}/{item.name}")
        if response.status_code == 200:
            typer.echo(f"Stopped.")
        else:
            typer.echo("Something went wrong.")
            typer.echo(response.json()["detail"])


def deploy_and_run_cloud(dir, config, typer, rebuild):
    typer.echo(f"Deploying...")
    response = requests.get(f"{API_URL}/projects/{config.project}")
    services = response.json()
    if config.scripts:
        typer.echo(f"Deploying scripts...")
        for script in config.scripts:
            check_item(script, services, typer, "script")
            run_script_or_notebook(
                script, dir / "scripts", typer, config, rebuild, "script"
            )
    if config.notebooks:
        typer.echo(f"Deploying notebooks...")
        for notebook in config.notebooks:
            check_item(notebook, services, typer, "notebook")
            run_script_or_notebook(
                notebook, dir / "notebooks", typer, config, rebuild, "notebook"
            )
    if config.apis:
        typer.echo(f"Deploying APIs...")
        for api in config.apis:
            check_item(api, services, typer, "api")
            run_item(api, dir / "apis", typer, config, rebuild, "api")
    if config.uis:
        typer.echo(f"Deploying UIs...")
        for ui in config.uis:
            check_item(ui, services, typer, "ui")
            run_item(ui, dir / "uis", typer, config, rebuild, "ui")
    # TODO: delete running services that no longer are in config???
