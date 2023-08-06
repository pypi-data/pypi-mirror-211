from __future__ import annotations

import dataclasses
import graphlib
import textwrap
import typing
from collections.abc import Sequence

import markdown_it

from ._compat.importlib.resources.abc import Traversable
from .checks import Check, collect_checks, is_allowed
from .families import Family, collect_families
from .fixtures import apply_fixtures, collect_fixtures, compute_fixtures, pyproject

__all__ = ["Result", "ResultDict", "ProcessReturn", "process", "as_simple_dict"]


def __dir__() -> list[str]:
    return __all__


md = markdown_it.MarkdownIt()


# Helper to get the type in the JSON style returns
class ResultDict(typing.TypedDict):
    family: str
    description: str
    result: bool | None
    err_msg: str


@dataclasses.dataclass(frozen=True, kw_only=True)
class Result:
    family: str
    name: str
    description: str
    result: bool | None
    err_msg: str = ""

    def err_markdown(self) -> str:
        result: str = md.render(self.err_msg).strip()
        return result.removeprefix("<p>").removesuffix("</p>").strip()


class ProcessReturn(typing.NamedTuple):
    families: dict[str, Family]
    results: list[Result]


def process(package: Traversable, *, ignore: Sequence[str] = ()) -> ProcessReturn:
    """
    Process the package and return a dictionary of results.

    Parameters
    ----------
    package: Traversable | Path
        The Path(like) package to process

    ignore: Sequence[str]
        A list of checks to ignore
    """
    # Collect the fixtures
    fixture_functions = collect_fixtures()
    fixtures = compute_fixtures(package, fixture_functions)

    # Collect the checks
    checks = collect_checks(fixtures)

    # Collect families.
    families = collect_families()

    # These are optional, so fill in missing families.
    for name in {c.family for c in checks.values()}:
        if name not in families:
            families[name] = Family()

    # Collect our own config
    config = pyproject(package).get("tool", {}).get("repo-review", {})
    skip_checks = set(ignore) | set(config.get("ignore", ()))

    tasks: dict[str, Check] = {
        n: r for n, r in checks.items() if is_allowed(skip_checks, n)
    }
    graph: dict[str, set[str]] = {
        n: getattr(t, "requires", set()) for n, t in tasks.items()
    }
    completed: dict[str, bool | None] = {}

    # Run all the checks in topological order
    ts = graphlib.TopologicalSorter(graph)
    for name in ts.static_order():
        if all(completed.get(n, False) for n in graph[name]):
            completed[name] = apply_fixtures(fixtures, tasks[name].check)
        else:
            completed[name] = None

    # Collect the results
    result_list = []
    for task_name, check in sorted(
        tasks.items(),
        key=lambda x: (families[x[1].family].get("order", 0), x[1].family, x[0]),
    ):
        result = completed[task_name]
        doc = check.__doc__ or ""
        err_msg = check.check.__doc__ or ""

        result_list.append(
            Result(
                family=check.family,
                name=task_name,
                description=doc,
                result=result,
                err_msg=textwrap.dedent(err_msg.format(cls=check)),
            )
        )

    return ProcessReturn(families, result_list)


def as_simple_dict(results: list[Result]) -> dict[str, ResultDict]:
    return {
        result.name: typing.cast(
            ResultDict,
            {k: v for k, v in dataclasses.asdict(result).items() if k != "name"},
        )
        for result in results
    }
