from pathlib import Path
import click
from sphinx.cmd.build import main as sphinx_build
import os
from antistasi_sqf_tools.doc_creating.config_handling import find_config_file, CONFIG_FILE_NAME
from antistasi_sqf_tools.doc_creating.creator import Creator
THIS_FILE_DIR = Path(__file__).parent.absolute()

CLI_FILE_PATH_TYPUS = click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True, path_type=Path)


def add_doc_sub_group(top_group: click.Group):
    @top_group.group(name="docs")
    @click.help_option("-h", "--help")
    def docs_cli():
        ...

    @docs_cli.command(name="sphinx-build")
    @click.help_option("-h", "--help")
    @click.option("-M", "--Make", is_flag=True)
    @click.argument("builder", default="html", type=click.STRING)
    @click.argument("source_dir", default=None, type=click.STRING)
    @click.argument("build_dir", default=None, type=click.STRING)
    @click.argument("sphinx_options", nargs=-1)
    def wrapped_sphinx_build(make, builder=None, source_dir=None, build_dir=None, sphinx_options=tuple()):
        arguments = []
        if make:
            arguments.append("-M")

        builder = builder or "html"
        arguments.append(builder)

        source_dir = source_dir or os.getcwd()
        arguments.append(source_dir)

        build_dir = build_dir or os.path.join(os.getcwd(), "build")
        arguments.append(build_dir)

        arguments.extend(sphinx_options)

        sphinx_build(arguments)

    @docs_cli.command()
    @click.help_option("-h", "--help")
    @click.option("-c", "--config-file", type=CLI_FILE_PATH_TYPUS)
    @click.option("-b", "--builder", type=click.STRING)
    def build(config_file=None, builder=None):
        config_file = config_file or find_config_file(CONFIG_FILE_NAME)
        builder = builder or "html"
        creator = Creator(config_file=config_file, builder_name=builder.casefold())
        creator.build()
