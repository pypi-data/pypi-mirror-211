from cleo.io.io import IO
from cleo.helpers import option

from poetry.plugins.plugin import Plugin
from poetry.poetry import Poetry
from poetry.plugins.application_plugin import ApplicationPlugin


class IgnoreBuildScriptApplicationPlugin(ApplicationPlugin):
    def activate(self, application):
        build_command = application.command_loader.get("build")
        build_command.options.append(
            option(
                "ignore-build-script",
                None,
                "Ignore build script in pyproject.toml file.",
            )
        )


class IgnoreBuildScriptPlugin(Plugin):
    def activate(self, poetry: Poetry, io: IO):
        if io.input.has_parameter_option("--ignore-build-script"):
            build_script = poetry.package.build_config.pop("script", None)
            if build_script is not None:
                io.write_line(
                    f"Ignoring build script setting '{build_script}' in config"
                )
