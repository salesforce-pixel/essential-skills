from __future__ import annotations

import os
import subprocess
import sys
import venv
from pathlib import Path


def sf_docs_runtime_root() -> Path:
    return Path.home() / ".claude" / ".fetching-salesforce-docs-runtime"


def sf_docs_venv_root() -> Path:
    return sf_docs_runtime_root() / "venv"


def sf_docs_runtime_python() -> Path:
    root = sf_docs_venv_root()
    candidates = [
        root / "bin" / "python",
        root / "bin" / "python3",
        root / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate
    return candidates[0] if os.name != "nt" else candidates[-1]


def prepare_sf_docs_runtime_env(env: dict[str, str] | None = None) -> dict[str, str]:
    runtime_root = sf_docs_runtime_root()
    target = dict(env or os.environ)
    target.setdefault("PLAYWRIGHT_BROWSERS_PATH", str(runtime_root / "ms-playwright"))
    target.setdefault("SF_DOCS_RUNTIME_ROOT", str(runtime_root))
    return target


def _running_in_runtime() -> bool:
    """True when the current interpreter is the isolated runtime venv.

    We compare ``sys.prefix`` (which points at the venv root for a venv
    interpreter) rather than resolving the executable, because the venv's
    ``python`` symlink resolves back to the base interpreter and would make a
    system interpreter look identical to the runtime one.
    """
    try:
        return Path(sys.prefix).resolve() == sf_docs_venv_root().resolve()
    except OSError:
        return False


def _log(message: str) -> None:
    print(f"[fetching-salesforce-docs] {message}", file=sys.stderr, flush=True)


def provision_sf_docs_runtime() -> bool:
    """Create the isolated venv, install deps, and fetch the chromium browser.

    Returns True on success. Safe to call repeatedly: venv creation is
    idempotent and pip/playwright skip already-satisfied work. Heavy steps log
    to stderr so a first-run install isn't silent.
    """
    runtime_root = sf_docs_runtime_root()
    venv_root = sf_docs_venv_root()
    runtime_python = sf_docs_runtime_python()
    env = prepare_sf_docs_runtime_env()

    if not runtime_python.exists():
        _log(f"Creating isolated runtime venv at {venv_root} (one-time setup)...")
        runtime_root.mkdir(parents=True, exist_ok=True)
        venv.EnvBuilder(with_pip=True).create(str(venv_root))
        runtime_python = sf_docs_runtime_python()

    # Route all provisioning subprocess output to stderr. Their stdout (pip
    # notices, chromium download progress bars) must never contaminate this
    # script's stdout, which carries the JSON result payload.
    run_kw = {"check": True, "env": env, "stdout": sys.stderr.fileno()}

    requirements = Path(__file__).resolve().parent.parent / "requirements.txt"
    _log("Installing Python dependencies (playwright, playwright-stealth)...")
    subprocess.run(
        [str(runtime_python), "-m", "pip", "install", "--quiet", "--upgrade", "pip"],
        **run_kw,
    )
    pip_args = [str(runtime_python), "-m", "pip", "install", "--quiet"]
    if requirements.exists():
        pip_args += ["-r", str(requirements)]
    else:
        pip_args += ["playwright", "playwright-stealth"]
    subprocess.run(pip_args, **run_kw)

    _log("Installing chromium browser for Playwright (one-time, may take a minute)...")
    subprocess.run(
        [str(runtime_python), "-m", "playwright", "install", "chromium"],
        **run_kw,
    )
    _log("Runtime ready.")
    return True


def maybe_reexec_in_sf_docs_runtime(script_path: str) -> bool:
    os.environ.update(prepare_sf_docs_runtime_env())

    # Already running inside the runtime venv: nothing to do.
    if os.environ.get("SF_DOCS_RUNTIME_ACTIVE") == "1" or _running_in_runtime():
        os.environ["SF_DOCS_RUNTIME_ACTIVE"] = "1"
        return False

    runtime_python = sf_docs_runtime_python()

    # Provision on first use so the skill self-heals instead of failing with a
    # bare ModuleNotFoundError. Set SF_DOCS_RUNTIME_NO_PROVISION=1 to opt out.
    if not runtime_python.exists():
        if os.environ.get("SF_DOCS_RUNTIME_NO_PROVISION") == "1":
            return False
        try:
            provision_sf_docs_runtime()
        except Exception as exc:  # noqa: BLE001 - surface, then let import fail loudly
            _log(f"Automatic runtime provisioning failed: {exc}")
            _log("Run scripts/setup_runtime.sh manually, then retry.")
            return False
        runtime_python = sf_docs_runtime_python()
        if not runtime_python.exists():
            return False

    env = prepare_sf_docs_runtime_env()
    env["SF_DOCS_RUNTIME_ACTIVE"] = "1"
    os.execve(
        str(runtime_python),
        [str(runtime_python), str(Path(script_path).resolve()), *sys.argv[1:]],
        env,
    )
    return True
