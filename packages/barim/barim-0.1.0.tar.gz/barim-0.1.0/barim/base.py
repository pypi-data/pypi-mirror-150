import sys
from argparse import ArgumentParser
from dataclasses import dataclass
from types import SimpleNamespace
from typing import IO, Any, Callable, List, NoReturn, Optional, Tuple, Type, Union

from barim import ansi
from barim.exceptions import CommandDuplicateError
from barim.utils import spacer


@dataclass
class Argument:
    """
    Use to declare an arguments for a provided command
    """

    name: str
    description: Optional[str]


@dataclass
class Option:
    """
    Use to declare an option for a provided command
    """

    short: str
    long: str
    description: Optional[str] = None
    default: Optional[Any] = None

    required: bool = False

    append: bool = False
    count: bool = False
    extend: bool = False
    store: bool = False

    def __post_init__(self) -> None:
        super().__init__()

        if len(self.short) != 1 or not self.short.isalpha():
            raise ValueError("Short class attribute must be 1 in length and from the alphabet")

        if len(self.long) <= 1 or not self.long.isalpha():
            raise ValueError("Long class attribute must contain character from the alphabet")

        actions = [self.append, self.count, self.extend, self.store]
        if actions.count(True) > 1:
            raise ValueError("Conflicting between actions. Set only one of them to True")


@dataclass
class _GlobalOption(Option):
    """"""

    action: Optional[str] = None

    def __post_init__(self) -> None:
        super().__post_init__()

        if self.action is not None and self.store is True:
            raise ValueError(
                "Unable to initialize _GlobalCommandOption if attributes action and store are set. Choose only one."
            )


class Command:
    """
    Class that should be inherited to allow the creation of commands.
    """

    name: str
    description: Optional[str] = None
    version: Optional[str] = None

    arguments: Optional[List[Argument]] = None
    options: Optional[List[Option]] = None

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
        arguments: Optional[List[Argument]] = None,
        options: Optional[List[Option]] = None,
        handle: Optional[Callable] = None,
    ):
        self.color = ansi.CYAN

        if not hasattr(self, "name"):
            if name is None:
                raise ValueError("Attribute 'name' not provided")
            else:
                self.name = name
        if self.arguments is None:
            self.arguments = arguments if arguments is not None else []
        if self.options is None:
            self.options = options if options is not None else []
        if self.description is None:
            self.description = description or f"Add a new description {self.color}°˖✧◝(⁰▿⁰)◜✧˖°{ansi.RESET}"
        if self.version is None:
            self.version = version or "unknown"

        if handle is not None:
            # Patching handle function to allow creation of command in an FP friendly way
            self.handle = handle  # type: ignore[assignment]  # Too dynamic for mypy

    def __eq__(self, other):
        """Allow to create sets of command objects"""
        if not isinstance(other, type(self)):
            return NotImplemented
        return self.name == other.name

    def __hash__(self) -> int:
        """Allow to create sets of command objects"""
        return hash(self.name)

    def handle(self, argv: SimpleNamespace, opts: SimpleNamespace) -> None:
        """This method must be implemented"""
        raise NotImplementedError("Method .handle() must be implemented")


class _ArgumentParser(ArgumentParser):
    """"""

    def __init__(
        self,
        name: str,
        arguments: Optional[List[Argument]] = None,
        options: Optional[List[Option]] = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
        commands: Optional[List[Command]] = None,
    ) -> None:
        self.name = name
        self.color = ansi.CYAN
        self.arguments = arguments or []
        self.options = options or []
        self.description = description or f"Add a new description {self.color}°˖✧◝(⁰▿⁰)◜✧˖°{ansi.RESET}"
        self.version = version or "unknown"
        self.commands = commands

        super().__init__(description=self.description, add_help=False)

        for argument in self.arguments:
            self.add_argument(argument.name, help=argument.description)

        # Add default options
        options = [
            _GlobalOption(short="h", long="help", description="Display help message", action="print_help"),
            _GlobalOption(short="V", long="version", description="Display version number", action="print_version"),
            _GlobalOption(short="v", long="verbose", description="Display more log message", count=True, default=0),
        ]

        for option in options:
            if not any(option.long == command_option.long for command_option in self.options):
                self.options.append(option)

        for option in self.options:
            args = [f"-{option.short}", f"--{option.long}"]
            kwargs = {"required": option.required, "action": "store_true"}

            if option.store:
                kwargs["action"] = "store"
            elif option.count:
                kwargs["action"] = "count"
            elif option.append:
                kwargs["action"] = "append"
            elif option.extend:
                kwargs["action"] = "extend"
            else:
                pass

            if option.default is not None:
                kwargs["default"] = option.default

            self.add_argument(*args, **kwargs)  # type: ignore[arg-type]  # Too dynamic for mypy

    def _format_help_arguments(self) -> Optional[str]:
        """"""
        if self.arguments is None or not self.arguments:
            return None

        res_lst = [
            f"\t{self.color}<{argument.name}>{ansi.RESET}{spacer(f'<{argument.name}>')}{argument.description}\n".expandtabs(
                4
            )
            for argument in self.arguments
        ]
        res_str = f"\n{ansi.BOLD}ARGUMENTS{ansi.RESET}\n{''.join(res_lst)}" if res_lst else ""

        return res_str

    def _format_help_commands(self) -> Optional[str]:
        """"""
        if self.commands is None or not self.commands:
            return None

        res_lst = [
            f"\t{self.color}{command.name}{ansi.RESET}{spacer(command.name)}{command.description}\n".expandtabs(4)
            for command in self.commands
        ]
        res_str = f"\n{ansi.BOLD}AVAILABLE COMMANDS{ansi.RESET}\n{''.join(res_lst)}" if res_lst else ""

        return res_str

    def _format_help_description(self) -> str:
        """"""
        return f"\n{ansi.BOLD}DESCRIPTION{ansi.RESET}\n\t{self.description}\n".expandtabs(4)

    def _format_help_global_options(self) -> Optional[str]:
        """"""
        options = [option for option in self.options if type(option) is _GlobalOption]
        if not options:
            return None

        res_lst = [
            f"\t{self.color}-{option.short}{ansi.RESET} (--{option.long}){spacer(f'-{option.short} (--{option.long})')}{option.description}\n".expandtabs(
                4
            )
            for option in options
        ]
        res_str = f"\n{ansi.BOLD}GLOBAL OPTIONS{ansi.RESET}\n{''.join(res_lst)}" if res_lst else ""

        return res_str

    def _format_help_options(self) -> Optional[str]:
        """"""
        if self.options is None or not self.options:
            return None

        res_lst = [
            f"\t{self.color}-{option.short}{ansi.RESET} (--{option.long}){spacer(f'-{option.short} (--{option.long})')}{option.description}\n".expandtabs(
                4
            )
            for option in self.options
            if type(option) == Option
        ]
        res_str = f"\n{ansi.BOLD}OPTIONS{ansi.RESET}\n{''.join(res_lst)}" if res_lst else ""

        return res_str

    def _format_help_usage(self) -> str:
        """"""
        res_str = f"\n{ansi.BOLD}USAGE{ansi.RESET}\n\t{ansi.UNDERLINE}{self.name}{ansi.RESET}".expandtabs(4)
        res_args = [f"<{argument.name}>" for argument in self.arguments]
        res_opts = [f"[-{option.short}]" for option in self.options]
        res_str += f" {''.join(res_args)} {' '.join(res_opts)}\n"
        return res_str

    def _format_help_version(self) -> str:
        """"""
        return f"{ansi.BOLD}{self.name}{ansi.RESET} version {ansi.BOLD}{ansi.GREEN}{self.version or 'unknown'}{ansi.RESET}\n"

    def error(self, message: str) -> NoReturn:
        """"""
        print(f"{ansi.BOLD}{ansi.RED}Fatal error:{ansi.RESET} {message}")
        self.print_usage()
        sys.exit(2)

    def format_help(self) -> str:
        """"""
        res_str = f"{self._format_help_version()}{self._format_help_description()}{self._format_help_usage()}"

        format_block_arguments = self._format_help_arguments()
        if format_block_arguments is not None:
            res_str = f"{res_str}{format_block_arguments}"

        format_block_global_options = self._format_help_global_options()
        if format_block_global_options is not None:
            res_str = f"{res_str}{format_block_global_options}"

        format_block_options = self._format_help_options()
        if format_block_options is not None:
            res_str = f"{res_str}{format_block_options}"

        format_block_commands = self._format_help_commands()
        if format_block_commands is not None:
            res_str = f"{res_str}{format_block_commands}"

        return res_str

    def parse(self, args: Optional[List[str]] = None) -> Tuple[SimpleNamespace, SimpleNamespace]:
        """
        Parse args and sort them by arguments or options

        :param args: List of arguments (Default at sys.argv[1:])
        :return:
        """
        if args is None:
            if len(sys.argv) > 1:
                args = sys.argv[1:]
            else:
                self.error("No arguments provided")
        else:
            args = args

        global_options: List[Any] = [option for option in self.options if type(option) is _GlobalOption]
        for option in global_options:
            if (f"--{option.long}" in args or f"-{option.short}" in args) and option.action is not None:
                func = getattr(self, option.action)
                func(exit_code=0)

        argv = self.parse_args(args)

        res_argv = {argument.name: getattr(argv, argument.name) for argument in self.arguments}
        res_opts = {option.long: getattr(argv, option.long) for option in self.options}

        return SimpleNamespace(**res_argv), SimpleNamespace(**res_opts)

    def print_help(self, file: Optional[IO[str]] = None, exit_code: Optional[int] = None) -> None:
        """"""
        print(self.format_help())
        if exit_code is not None:
            sys.exit(exit_code)

    def print_usage(self, file: Optional[IO[str]] = None) -> None:
        """"""
        self.print_help()

    def print_version(self, exit_code: Optional[int] = None) -> None:
        """"""
        print(self._format_help_version())
        if exit_code is not None:
            sys.exit(exit_code)


class Application:
    """
    Main CLI handler
    """

    def __init__(
        self,
        name: Optional[str] = None,
        description: Optional[str] = None,
        version: Optional[str] = None,
    ) -> None:
        self._parser: Optional[_ArgumentParser] = None

        self.color = ansi.CYAN
        self.name = name or "unknown"
        self.description = description or f"Add a new description {self.color}°˖✧◝(⁰▿⁰)◜✧˖°{ansi.RESET}"
        self.version = version or f"{self.color}unknown{ansi.RESET}"
        self.commands: List[Command] = []

    @property
    def parser(self) -> _ArgumentParser:
        if self._parser is None:
            self._parser = _ArgumentParser(
                name=self.name,
                description=self.description,
                version=self.version,
                arguments=[Argument(name="command", description="The command to run")],
                options=[],
                commands=self.commands,
            )
        return self._parser

    def match_command(self, name: str) -> Command:
        """
        Return the command corresponding to the provided name.
        Exit the program in case the command is not found.
        """
        for command in self.commands:
            if command.name == name:
                return command
        self.parser.error(f"Unable to find matching command '{sys.argv[1]}'")

    def register(self, command: Union[Command, Type[Command]]) -> "Application":
        """
        Register a command to make it available for application

        :param command:
        :return:
        """
        if isinstance(command, type):
            command = command()

        self.commands.append(command)

        if len(set(self.commands)) != len(self.commands):
            raise CommandDuplicateError("Found duplicated command registered.")

        return self

    def run(self, default: bool = False) -> None:
        """
        Run the cli application

        :param default: Set to True when a single registered command must be used as default
        :return:
        """
        if default:
            if len(self.commands) != 1:
                raise RuntimeError("Too many command registered. Only one command must be register.")

            argv = sys.argv[1:]
            command = self.commands[0]
        else:
            argv = sys.argv[2:]
            args, _ = self.parser.parse([sys.argv[1]] if len(sys.argv) >= 2 else [])
            command = self.match_command(args.command)

        parser = _ArgumentParser(
            name=command.name,
            description=command.description,
            version=command.version,
            arguments=command.arguments,
            options=command.options,
        )

        args, opts = parser.parse(argv)
        command.handle(args, opts)
