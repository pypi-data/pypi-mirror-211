import os
from os.path import abspath
from pathlib import Path

import jinja2
import typer
import uvicorn

from script_master import const

cli = typer.Typer()


def set_variable(name, value, default):
    if value is not None and value != default:
        os.environ[name] = value


@cli.command()
def init(home_dir: Path = Path.cwd()):
    """Create .env file"""

    directory = Path(abspath(__file__)).parent
    with open(directory / "template-settings.env") as f:
        template = jinja2.Template(f.read())

    home_dir = Path(home_dir or Path.cwd())
    os.environ[const.HOME_DIR_VARNAME] = str(home_dir)

    filepath = str(home_dir / ".env")
    template.stream(environ=os.environ).dump(filepath)
    typer.echo(f"Created {filepath}")


@cli.command()
def run(
    homedir: str = None,
    host: str = const.DEFAULT_HOST,
    port: int = const.DEFAULT_PORT,
    debug: bool = False,
    uvicorn_config_file: str = None,
):
    set_variable(const.HOME_DIR_VARNAME, homedir, homedir)
    set_variable("SCRIPT_MASTER_DEBUG", debug, False)

    from script_master.settings import Settings

    server = uvicorn.Server(
        Settings().for_uvicorn(
            host=host, port=port, env_file=uvicorn_config_file
        )
    )
    server.run()


if __name__ == "__main__":
    typer.run(cli)
