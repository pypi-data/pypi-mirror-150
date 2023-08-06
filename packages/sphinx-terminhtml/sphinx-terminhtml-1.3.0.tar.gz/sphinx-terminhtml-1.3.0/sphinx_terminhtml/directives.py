import ast
from pathlib import Path
from typing import List, Sequence, Optional, Type


from docutils.nodes import Node
from docutils.parsers.rst import directives
from docutils.statemachine import StringList
from sphinx.util.docutils import SphinxDirective
from docutils import nodes
from terminhtml.main import TerminHTML

from sphinx_terminhtml.cache import TerminalCache
from sphinx_terminhtml.logger import log
from sphinx_terminhtml.options import RunTerminalOptions, CWDRelativeTo


def html(content: str) -> nodes.raw:
    return nodes.raw(text=content, format="html")


def _get_list(input: str) -> List[str]:
    if not input.startswith("["):
        if input:
            return [input]
        return []
    return ast.literal_eval(input)


def _get_optional_path(in_path: Optional[str]) -> Optional[Path]:
    if in_path is None:
        return None
    return Path(in_path)


def _validate_cwd_relative_to(argument: Optional[str]) -> Optional[CWDRelativeTo]:
    if argument is None:
        return None
    return directives.choice(argument, [val.value for val in CWDRelativeTo])  # type: ignore


cache = TerminalCache()


class TerminHTMLDirective(SphinxDirective):
    required_arguments = 0
    option_spec = {
        "setup": directives.unchanged,
        "input": _get_list,
        "prompt-matchers": _get_list,
        "allow-exceptions": directives.flag,
        "cwd": directives.unchanged,
        "cwd-relative-to": _validate_cwd_relative_to,
        "disable-cache": directives.flag,
        "echo": directives.flag,
    }
    has_content = True
    always_setup_commands: List[str] = []
    always_prompt_matchers: List[str] = []

    def run(self) -> List[Node]:
        text = self._run_commands_in_temp_dir_generate_output_html()
        return [html(text)]

    @property
    def commands(self) -> List[str]:
        return list(self.content)

    @property
    def root_source_dir(self) -> Path:
        return Path(self.env.srcdir)

    @property
    def current_file_folder(self) -> Path:
        file_str, line = self.get_source_info()
        return Path(file_str).parent

    @property
    def cwd(self) -> Optional[Path]:
        cwd = _get_optional_path(self.options.get("cwd"))
        if cwd is None:
            return None
        if cwd.is_absolute():
            return cwd
        # Resolve path based on relative to option
        cwd_relative_to = self.options.get("cwd-relative-to", CWDRelativeTo.CWD)
        if cwd_relative_to == CWDRelativeTo.CWD:
            return cwd.resolve()
        if cwd_relative_to == CWDRelativeTo.SOURCES_ROOT:
            return (self.root_source_dir / cwd).resolve()
        if cwd_relative_to == CWDRelativeTo.CURRENT_SOURCE:
            return (self.current_file_folder / cwd).resolve()
        raise ValueError(f"Unknown cwd-relative-to: {cwd_relative_to}")

    def _run_commands_in_temp_dir_generate_output_html(self) -> str:
        self.options: RunTerminalOptions

        setup_command: str = self.options.get("setup", "")
        if setup_command:
            use_setup_commands = self.always_setup_commands + [setup_command]
        else:
            use_setup_commands = self.always_setup_commands

        prompt_matchers: List[str] = self.options.get("prompt-matchers", []) or []
        if prompt_matchers:
            use_prompt_matchers = self.always_prompt_matchers + prompt_matchers
        else:
            use_prompt_matchers = self.always_prompt_matchers

        input: List[Optional[str]] = self.options.get("input", [])
        allow_exceptions: bool = "allow-exceptions" in self.options
        return self._load_cache_or_run_commands_in_temp_dir_get_output_list(
            use_setup_commands,
            input=input,
            allow_exceptions=allow_exceptions,
            prompt_matchers=use_prompt_matchers,
            cwd=self.cwd,
        )

    def _load_cache_or_run_commands_in_temp_dir_get_output_list(
        self,
        setup_commands: List[str],
        input: List[Optional[str]],
        allow_exceptions: bool,
        prompt_matchers: List[str],
        cwd: Optional[Path] = None,
    ) -> str:
        self.content: StringList
        cache_enabled: bool = self.env.config.terminhtml_cache
        disable_this_terminal_cache: bool = "disable-cache" in self.options
        if cache_enabled and not disable_this_terminal_cache:
            cached_result = cache.get(list(self.content), self.options)
            if cached_result:
                return cached_result.content
        else:
            log.info(f"TerminHTML cache disabled, running commands {self.content}")

        result = self._run_commands_in_temp_dir_generate_html(
            setup_commands, input, allow_exceptions, prompt_matchers, cwd=cwd
        )
        cache.set(self.commands, self.options, result)
        return result

    def _run_commands_in_temp_dir_generate_html(
        self,
        setup_commands: List[str],
        input: List[Optional[str]],
        allow_exceptions: bool,
        prompt_matchers: List[str],
        cwd: Optional[Path] = None,
    ) -> str:
        global_echo: bool = self.env.config.terminhtml_echo
        echo_this_terminal: bool = "echo" in self.options
        echo_now = global_echo or echo_this_terminal
        terminhtml = TerminHTML.from_commands(
            self.commands,
            setup_commands,
            input=input,
            allow_exceptions=allow_exceptions,
            prompt_matchers=prompt_matchers,
            cwd=cwd,
            echo=echo_now,
        )
        return terminhtml.to_html(full=False)


def create_terminhtml_directive_with_setup(
    setup_commands: Optional[Sequence[str]] = None,
    prompt_matchers: Optional[Sequence[str]] = None,
) -> Type[SphinxDirective]:
    use_setup_commands = list(setup_commands or [])
    use_prompt_matchers = list(prompt_matchers or [])

    class RunTerminalDirectiveWithSetup(TerminHTMLDirective):
        always_setup_commands = use_setup_commands
        always_prompt_matchers = use_prompt_matchers

    return RunTerminalDirectiveWithSetup
