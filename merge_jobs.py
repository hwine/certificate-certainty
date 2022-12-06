#!/usr/bin/env python3
"""Merge the various job files into a single file.

We expect "merge" to change over time, hence doing a custom script
rather than a `jq` hack.

Current merge:
    - take `metadata` from first file
    - append all `data` elements
"""


import json
from pathlib import Path

import typer

# globals (common prefix allows grouping in debugger)
g_local_new_data: Path = Path(
    "/tmp/report.json"  # nosec -- we're in a short running container
)


def main(files: list[Path] = typer.Argument(None)):
    data = []
    metadata = None
    element_count = 0

    for f in files:
        with open(f) as f_in:
            d = json.load(f_in)
        if not metadata:
            metadata = d["metadata"]
        data.extend(d["data"])
        element_count += len(d["data"])
    if not len(data) == element_count:
        raise AssertionError

    combined = {
        "metadata": metadata,
        "data": data,
    }
    with open(g_local_new_data, "w") as f_out:
        json.dump(combined, f_out)


if __name__ == "__main__":
    typer.run(main)
