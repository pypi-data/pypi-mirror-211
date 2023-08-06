import typer
from atg.commands.tools.app import tools_app
import importlib.metadata

# from atg.commands.lefse.app import lefse_app
# from atg.commands.get.app import get_app
# from atg.commands.parse.app import parse_app
# from atg.commands.diversity.app import diversity_app
# from atg.commands.util import get_initialized_tg_connection

__version__ = importlib.metadata.version('atgtools')

main_app = typer.Typer(help="CLI for ATGtools", add_completion=False, rich_markup_mode="rich")

# Tools
main_app.add_typer(typer_instance=tools_app, name="tools")

# LEfSe
# main_app.add_typer(typer_instance=lefse_app, name="lefse")

# Plots
# main_app.add_typer(typer_instance=plot_app, name="plot")

# Stats
# main_app.add_typer(typer_instance=stats_app, name="stats")

# Diversity
# main_app.add_typer(typer_instance=diversity_app, name="diversity")


@main_app.command("version", help="Current version of ATGtools.")
def version():
    typer.secho(__version__,  fg=typer.colors.BRIGHT_GREEN, bold=True)
