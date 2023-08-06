import os
import requests

# API_URL = "http://localhost:8000"
API_URL = "http://148.113.137.45:8010"


def call_api(script_dir, endpoint, data):
    return requests.post(
        f"{API_URL}/{endpoint}/script",
        files={
            "script": open(script_dir / "main.py", "rb"),
            "requirements": open(script_dir / "requirements.txt", "rb")
            if "requirements.txt" in os.listdir(script_dir)
            else None,
            "env": open(script_dir / ".env", "rb")
            if ".env" in os.listdir(script_dir)
            else None,
        },
        data=data,
    )


def deploy_and_run_cloud(dir, config, typer):
    typer.echo(f"Deploying...")
    if config.scripts:
        typer.echo(f"Deploying scripts...")
        for script in config.scripts:
            # check if script is already deployed
            response = requests.get(f"{API_URL}/projects/{config.project}")
            scripts = list(response.json().keys())
            if script.name in scripts:
                typer.echo(f"Script '{script.name}' already deployed.")
                typer.echo(f"Stopping ...")  # confirm
                response = requests.get(f"{API_URL}/stop/script/{script.name}")
                if response.status_code == 200:
                    typer.echo(f"Stopped.")
                else:
                    typer.echo("Something went wrong.")
                    typer.echo(response.json()["detail"])
            # deploy script
            script_dir = dir / "scripts" / script.name
            if script.run_on_start:
                typer.echo(f"Running script '{script.name}'...")
                response = call_api(
                    script_dir, "run", {"name": script.name, "project": config.project}
                )
                if response.status_code == 200:
                    print(response.json())
                else:
                    typer.echo("Something went wrong.")
                    typer.echo(response.json()["detail"])
            if script.run_every:
                typer.echo(f"Setting up cronjob for script '{script.name}'...")
                response = call_api(
                    script_dir,
                    "schedule",
                    {"name": script.name, "run_every": script.run_every},
                )
                if response.status_code == 200:
                    print(response.json())
                else:
                    typer.echo("Something went wrong.")
                    typer.echo(response.json()["detail"])
