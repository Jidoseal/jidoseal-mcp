"""
engine_path.py — make the engine importable, once, for the MCP server package.
==============================================================================
The engine's modules import one another by TOP-LEVEL name (`import okf_manifest`,
`import tier1_gate`) — see the pyproject.toml header for why that shape is load-bearing and
must not be rewritten. Other JidoSeal surfaces reach the engine the same way: insert
the engine directory on `sys.path` and import the bare module name. This module is that one
insert for this package, so no module here has to repeat the path arithmetic (and no two
copies of it can drift).

TWO WAYS THE ENGINE CAN BE PRESENT
----------------------------------
1. A SOURCE CHECKOUT — `<repo>/engine/` sits next to this package's source directory. Insert it on
   `sys.path`, exactly as before.
2. AN INSTALL — `pip install jidoseal-mcp` pulls in the `jidoseal` distribution, which ships
   the engine's scan-path modules FLAT at the top level of site-packages (`okf_manifest.py`,
   `tier1_gate.py`, …; see pyproject.toml's `py-modules`). They are therefore already
   importable by the bare names the engine uses, and there is nothing to insert.

Case 2 is why this module exists in its current form: before it, `ENGINE_DIR` was computed
relative to this file unconditionally, which resolves to a `site-packages/engine` that does not
exist — so a stranger who installed the package rather than cloning the repo got an
`ImportError` on the first scan.

The discriminator is the MARKER FILE `okf_manifest.py` inside `ENGINE_DIR`, not the directory's
existence: a bare directory named `engine` that happens to sit one level up is not an engine,
and silently inserting it would shadow a correctly installed one.

FAIL LOUD
---------
If neither case holds the engine is genuinely absent, and every scan would fail later with a
bare `ModuleNotFoundError` naming a module the customer has never heard of. Raise here instead,
naming the fix.

Imports stdlib only (`importlib.util`, `os`, `sys`) and touches nothing else — it is on the scan
path and is held to the same "imports nothing network-capable" bar as the engine modules it
fronts. `importlib.util.find_spec` is used rather than an
`import okf_manifest` in a `try:` because it ANSWERS the question ("is the engine importable?")
without EXECUTING engine code as a side effect of asking it.
"""
from __future__ import annotations

import importlib.util
import os
import sys

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE_DIR = os.path.join(REPO_ROOT, "engine")

#: Present in a checkout's `engine/`, and shipped top-level by the `jidoseal` wheel. Either way
#: its importability is exactly the question "can this process reach the certified scoring
#: logic?", which is the only thing this module is for.
ENGINE_MARKER_MODULE = "okf_manifest"


def _checkout_engine_dir() -> str:
    """The repo's `engine/` if this file is running from a checkout, else ""."""
    marker = os.path.join(ENGINE_DIR, ENGINE_MARKER_MODULE + ".py")
    return ENGINE_DIR if os.path.isfile(marker) else ""


def ensure_engine_on_path() -> str:
    """Idempotently make the engine importable by bare name; return the directory providing it.

    Checkout: insert `<repo>/engine` first on `sys.path`. Install: verify the engine is already
    importable and leave `sys.path` alone. Neither: raise ImportError naming the fix.
    """
    engine_dir = _checkout_engine_dir()
    if engine_dir:
        if engine_dir not in sys.path:
            sys.path.insert(0, engine_dir)
        return engine_dir

    spec = importlib.util.find_spec(ENGINE_MARKER_MODULE)
    if spec is not None and spec.origin:
        return os.path.dirname(spec.origin)

    raise ImportError(
        "The JidoSeal engine is not importable. This server needs the scan engine, which ships "
        "in the `jidoseal` package: install it with `pip install jidoseal`, "
        "and run this server again."
    )
