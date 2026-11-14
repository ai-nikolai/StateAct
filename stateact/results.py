"""One result format for ALFWorld, WebShop and TextCraft.

All benchmarks write the same two files under ``<results_folder>/<trial>/``:

``episodes.csv``
    One row per environment episode. The common columns are
    ``run_id, benchmark, agent, model, trial, env_idx, env_type, success,
    done, reward, steps, error, early_stop, details``. Benchmark-specific
    values live in the ``details`` JSON column.

``summary.csv``
    One row per agent/run. The common columns are
    ``run_id, benchmark, agent, model, trial, split, num_envs, score,
    success_rate, failure_rate, avg_reward, avg_steps, started_at,
    finished_at, details``.

The loaders also understand the historical layouts (``alfworld_results.csv``,
WebShop ``scores.csv`` and TextCraft ``results.csv``), so old runs remain
analysisable.

Standard library only: the benchmark environments do not install pandas.
"""

import csv
import json
import os
from datetime import datetime

__all__ = [
    "SUMMARY_FIELDS",
    "EPISODE_FIELDS",
    "RunLogger",
    "run_dir",
    "summary_path",
    "episodes_path",
    "load_run",
    "load_summary",
    "load_episodes",
    "find_runs",
]

SUMMARY_FIELDS = [
    "run_id", "benchmark", "agent", "model", "trial", "split", "num_envs",
    "score", "success_rate", "failure_rate", "avg_reward", "avg_steps",
    "started_at", "finished_at", "details",
]

EPISODE_FIELDS = [
    "run_id", "benchmark", "agent", "model", "trial", "env_idx", "env_type",
    "success", "done", "reward", "steps", "error", "early_stop", "details",
]

SUMMARY_NAMES = ("summary.csv", "scores.csv", "results.csv")
EPISODE_NAMES = ("episodes.csv", "alfworld_results.csv")
EPISODE_CORE = set(EPISODE_FIELDS)
SUMMARY_CORE = set(SUMMARY_FIELDS)


def _now():
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _json(value):
    return json.dumps(value or {}, sort_keys=True, default=str)


def _parse_details(row):
    raw = row.get("details")
    if not raw:
        return {}
    try:
        details = json.loads(raw)
    except (TypeError, ValueError):
        return {}
    return details if isinstance(details, dict) else {}


def _to_int(value, default=0):
    if value is None or value == "":
        return default
    if isinstance(value, bool):
        return int(value)
    text = str(value).strip().lower()
    if text in ("true", "yes"):
        return 1
    if text in ("false", "no"):
        return 0
    try:
        return int(float(value))
    except (TypeError, ValueError):
        return default


def _to_float(value, default=0.0):
    if value is None or value == "":
        return default
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def run_dir(trial, results_folder="results"):
    """Return ``<results_folder>/<trial>`` (the same layout for every benchmark)."""
    return os.path.join(results_folder, trial)


def summary_path(trial, results_folder="results"):
    return os.path.join(run_dir(trial, results_folder), "summary.csv")


def episodes_path(trial, results_folder="results"):
    return os.path.join(run_dir(trial, results_folder), "episodes.csv")


def _append(path, fields, row):
    exists = os.path.exists(path)
    parent = os.path.dirname(path)
    if parent:
        os.makedirs(parent, exist_ok=True)
    with open(path, "a", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, extrasaction="ignore")
        if not exists:
            writer.writeheader()
        writer.writerow(row)


class RunLogger:
    """Write the unified ``episodes.csv`` / ``summary.csv`` pair."""

    def __init__(self, benchmark, agent, model, trial, results_folder="results",
                 split="", num_envs=None, run_id=None, started_at=None,
                 summary_filename="summary.csv", episodes_filename="episodes.csv"):
        self.benchmark = benchmark
        self.agent = agent
        self.model = model
        self.trial = trial
        self.split = split
        self.num_envs = num_envs
        self.started_at = started_at or _now()
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.run_id = run_id or f"{benchmark}-{trial}-{agent}-{model}-{stamp}"

        self.directory = run_dir(trial, results_folder)
        self.summary_path = os.path.join(self.directory, summary_filename)
        self.episodes_path = os.path.join(self.directory, episodes_filename)
        self.rows = []
        self.finished = False

    def _episode_row(self, env_idx, env_type="", success=False, done=True,
                     reward=0.0, steps=0, error="", early_stop="", details=None,
                     **extra):
        if extra:
            details = {**(details or {}), **extra}
        return {
            "run_id": self.run_id,
            "benchmark": self.benchmark,
            "agent": self.agent,
            "model": self.model,
            "trial": self.trial,
            "env_idx": _to_int(env_idx),
            "env_type": env_type or "",
            "success": _to_int(success),
            "done": _to_int(done),
            "reward": _to_float(reward),
            "steps": _to_int(steps),
            "error": error or "",
            "early_stop": early_stop or "",
            "details": _json(details),
        }

    def log_episode(self, env_idx, env_type="", success=False, done=True,
                    reward=0.0, steps=0, error="", early_stop="", details=None,
                    **extra):
        """Append one episode row and return it."""
        row = self._episode_row(
            env_idx=env_idx, env_type=env_type, success=success, done=done,
            reward=reward, steps=steps, error=error, early_stop=early_stop,
            details=details, **extra,
        )
        self.rows.append(row)
        _append(self.episodes_path, EPISODE_FIELDS, row)
        return row

    def finish(self, score=None, success_rate=None, failure_rate=None,
               avg_reward=None, avg_steps=None, details=None, finished_at=None):
        """Write the one-row summary for this run and return it."""
        count = len(self.rows) or (self.num_envs or 0)
        if success_rate is None:
            success_rate = (
                sum(r["success"] for r in self.rows) / count if count else 0.0
            )
        if score is None:
            score = success_rate
        if failure_rate is None:
            failure_rate = max(0.0, 1.0 - success_rate)
        if avg_reward is None:
            avg_reward = (
                sum(r["reward"] for r in self.rows) / count if count else 0.0
            )
        if avg_steps is None:
            avg_steps = (
                sum(r["steps"] for r in self.rows) / count if count else 0.0
            )

        row = {
            "run_id": self.run_id,
            "benchmark": self.benchmark,
            "agent": self.agent,
            "model": self.model,
            "trial": self.trial,
            "split": self.split or "",
            "num_envs": count,
            "score": score,
            "success_rate": success_rate,
            "failure_rate": failure_rate,
            "avg_reward": avg_reward,
            "avg_steps": avg_steps,
            "started_at": self.started_at,
            "finished_at": finished_at or _now(),
            "details": _json(details),
        }
        _append(self.summary_path, SUMMARY_FIELDS, row)
        self.finished = True
        return row


def _read_csv(path):
    with open(path, newline="") as handle:
        return list(csv.DictReader(handle))


def _resolve(path, names):
    if os.path.isdir(path):
        for name in names:
            candidate = os.path.join(path, name)
            if os.path.exists(candidate):
                return candidate
        raise FileNotFoundError(
            f"No {' / '.join(names)} in {path}"
        )
    if os.path.exists(path):
        return path
    raise FileNotFoundError(path)


def _infer_benchmark(path):
    parts = path.replace("\\", "/").split("/")
    for benchmark in ("alfworld", "webshop", "textcraft"):
        if benchmark in parts:
            return benchmark
    return ""


def _normalise_episode(row, benchmark):
    row = dict(row)
    details = _parse_details(row)
    merged = {**details, **row}

    success = _to_int(merged.get("success", 0))
    done = _to_int(merged.get("done", success))
    reward = merged.get("reward", merged.get("total_reward", 0.0))
    steps = merged.get("steps", merged.get("num_of_steps", 0))

    extra = {
        key: value for key, value in merged.items()
        if key not in EPISODE_CORE and key != "details"
    }
    normalised = {
        "run_id": merged.get("run_id", ""),
        "benchmark": merged.get("benchmark", benchmark),
        "agent": merged.get("agent", merged.get("agent_type", "")),
        "model": merged.get("model", ""),
        "trial": merged.get("trial", ""),
        "env_idx": _to_int(merged.get("env_idx", 0)),
        "env_type": merged.get("env_type", ""),
        "success": success,
        "done": done,
        "reward": _to_float(reward),
        "steps": _to_int(steps),
        "error": merged.get("error", ""),
        "early_stop": merged.get("early_stop", ""),
        "details": _json(extra),
    }
    # Flatten details for analysis convenience.
    normalised.update(extra)
    return normalised


def _normalise_summary(row, benchmark, trial=""):
    row = dict(row)
    details = _parse_details(row)
    merged = {**details, **row}

    # WebShop legacy: avg_score / success_rate / failure_rate.
    # TextCraft legacy: rate / total_count / average_depth / max_depth.
    score = merged.get("score",
                       merged.get("avg_score",
                                  merged.get("rate", 0.0)))
    success_rate = merged.get("success_rate", merged.get("rate", score))
    failure_rate = merged.get("failure_rate")
    if failure_rate in (None, ""):
        failure_rate = max(0.0, 1.0 - _to_float(success_rate))
    num_envs = merged.get("num_envs", merged.get("total_count", 0))

    extra = {
        key: value for key, value in merged.items()
        if key not in SUMMARY_CORE and key != "details"
    }
    normalised = {
        "run_id": merged.get("run_id", ""),
        "benchmark": merged.get("benchmark", benchmark),
        "agent": merged.get("agent", ""),
        "model": merged.get("model", ""),
        "trial": merged.get("trial", trial),
        "split": merged.get("split", ""),
        "num_envs": _to_int(num_envs),
        "score": _to_float(score),
        "success_rate": _to_float(success_rate),
        "failure_rate": _to_float(failure_rate),
        "avg_reward": _to_float(merged.get("avg_reward", score)),
        "avg_steps": _to_float(merged.get("avg_steps", 0.0)),
        "started_at": merged.get("started_at", ""),
        "finished_at": merged.get("finished_at", merged.get("date", "")),
        "details": _json(extra),
    }
    normalised.update(extra)
    return normalised


def load_episodes(path, benchmark=None):
    """Load episodes from a unified or legacy file/directory."""
    resolved = _resolve(path, EPISODE_NAMES)
    if benchmark is None:
        benchmark = _infer_benchmark(resolved)
    return [_normalise_episode(row, benchmark) for row in _read_csv(resolved)]


def load_summary(path, benchmark=None):
    """Load summary rows from a unified or legacy file/directory.

    For a legacy ALFWorld episode file, one summary row is derived from the
    episodes.
    """
    resolved = _resolve(path, SUMMARY_NAMES + EPISODE_NAMES)
    if benchmark is None:
        benchmark = _infer_benchmark(resolved)
    trial = os.path.basename(os.path.dirname(resolved)) if os.path.dirname(resolved) else ""

    if os.path.basename(resolved) in EPISODE_NAMES:
        episodes = load_episodes(resolved, benchmark=benchmark)
        if not episodes:
            return []
        count = len(episodes)
        success = sum(_to_int(e["success"]) for e in episodes)
        return [{
            "run_id": episodes[0].get("run_id", ""),
            "benchmark": benchmark,
            "agent": episodes[0].get("agent", ""),
            "model": episodes[0].get("model", ""),
            "trial": trial,
            "split": "",
            "num_envs": count,
            "score": success / count,
            "success_rate": success / count,
            "failure_rate": 1.0 - success / count,
            "avg_reward": sum(_to_float(e["reward"]) for e in episodes) / count,
            "avg_steps": sum(_to_float(e["steps"]) for e in episodes) / count,
            "started_at": "",
            "finished_at": "",
            "details": "{}",
        }]

    return [_normalise_summary(row, benchmark, trial) for row in _read_csv(resolved)]


def load_run(benchmark, trial, results_folder="results"):
    """Load summary rows for a benchmark/trial with legacy fallbacks."""
    directory = run_dir(trial, results_folder)
    try:
        return load_summary(directory, benchmark=benchmark)
    except FileNotFoundError:
        pass

    if benchmark == "alfworld":
        legacy = os.path.join("game_logs", f"alfworld_eval_{trial}")
        return load_summary(legacy, benchmark=benchmark)
    raise FileNotFoundError(directory)


def find_runs(results_folder="results", benchmark=None):
    """Return ``(benchmark, trial, run_dir)`` tuples found under a results root."""
    found = []
    if not os.path.isdir(results_folder):
        return found
    names = SUMMARY_NAMES + EPISODE_NAMES
    for trial in sorted(os.listdir(results_folder)):
        directory = os.path.join(results_folder, trial)
        if not os.path.isdir(directory):
            continue
        if not any(os.path.exists(os.path.join(directory, name)) for name in names):
            continue
        try:
            rows = load_summary(directory)
        except FileNotFoundError:
            continue
        inferred = rows[0]["benchmark"] if rows else ""
        if benchmark and inferred and inferred != benchmark:
            continue
        found.append((inferred or benchmark or "", trial, directory))
    return found
