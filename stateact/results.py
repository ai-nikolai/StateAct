"""The single result format used by every benchmark.

Each run writes two files under ``<results_folder>/<trial>/``:

``episodes.csv``
    One row per environment episode. The common columns are
    ``run_id, benchmark, agent, model, trial, env_idx, env_type, success,
    done, reward, steps, error, early_stop, details``.

``summary.csv``
    One row per agent/run. The common columns are
    ``run_id, benchmark, agent, model, trial, split, num_envs, score,
    success_rate, failure_rate, avg_reward, avg_steps, started_at,
    finished_at, details``.

Benchmark-specific values live in the ``details`` JSON column and are
flattened back into the row by the loaders.

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

SUMMARY_CORE = set(SUMMARY_FIELDS)
EPISODE_CORE = set(EPISODE_FIELDS)


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
                 split="", num_envs=None, run_id=None, started_at=None):
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
        self.summary_path = os.path.join(self.directory, "summary.csv")
        self.episodes_path = os.path.join(self.directory, "episodes.csv")
        self.rows = []
        self.finished = False

    def log_episode(self, env_idx, env_type="", success=False, done=True,
                    reward=0.0, steps=0, error="", early_stop="", details=None,
                    **extra):
        if extra:
            details = {**(details or {}), **extra}
        row = {
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
        self.rows.append(row)
        _append(self.episodes_path, EPISODE_FIELDS, row)
        return row

    def finish(self, score=None, success_rate=None, failure_rate=None,
               avg_reward=None, avg_steps=None, details=None, finished_at=None):
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


def _resolve(path, name):
    if os.path.isdir(path):
        candidate = os.path.join(path, name)
        if os.path.exists(candidate):
            return candidate
        raise FileNotFoundError(candidate)
    if os.path.exists(path):
        return path
    raise FileNotFoundError(path)


def _detail_value(value):
    if isinstance(value, (list, dict, tuple)):
        return json.dumps(value, sort_keys=True)
    return value


def _normalise_episode(row):
    details = _parse_details(row)
    extra = {
        key: _detail_value(value) for key, value in details.items()
        if key not in EPISODE_CORE
    }
    normalised = {
        "run_id": row.get("run_id", ""),
        "benchmark": row.get("benchmark", ""),
        "agent": row.get("agent", ""),
        "model": row.get("model", ""),
        "trial": row.get("trial", ""),
        "env_idx": _to_int(row.get("env_idx", 0)),
        "env_type": row.get("env_type", ""),
        "success": _to_int(row.get("success", 0)),
        "done": _to_int(row.get("done", 0)),
        "reward": _to_float(row.get("reward", 0.0)),
        "steps": _to_int(row.get("steps", 0)),
        "error": row.get("error", ""),
        "early_stop": row.get("early_stop", ""),
        "details": _json(extra),
    }
    normalised.update(extra)
    return normalised


def _normalise_summary(row):
    details = _parse_details(row)
    extra = {
        key: _detail_value(value) for key, value in details.items()
        if key not in SUMMARY_CORE
    }
    normalised = {
        "run_id": row.get("run_id", ""),
        "benchmark": row.get("benchmark", ""),
        "agent": row.get("agent", ""),
        "model": row.get("model", ""),
        "trial": row.get("trial", ""),
        "split": row.get("split", ""),
        "num_envs": _to_int(row.get("num_envs", 0)),
        "score": _to_float(row.get("score", 0.0)),
        "success_rate": _to_float(row.get("success_rate", 0.0)),
        "failure_rate": _to_float(row.get("failure_rate", 0.0)),
        "avg_reward": _to_float(row.get("avg_reward", 0.0)),
        "avg_steps": _to_float(row.get("avg_steps", 0.0)),
        "started_at": row.get("started_at", ""),
        "finished_at": row.get("finished_at", ""),
        "details": _json(extra),
    }
    normalised.update(extra)
    return normalised


def load_episodes(path):
    """Load ``episodes.csv`` from a run directory or file."""
    resolved = _resolve(path, "episodes.csv")
    return [_normalise_episode(row) for row in _read_csv(resolved)]


def _summary_from_episodes(episodes):
    if not episodes:
        return []
    count = len(episodes)
    success = sum(ep["success"] for ep in episodes)
    return [{
        "run_id": episodes[0].get("run_id", ""),
        "benchmark": episodes[0].get("benchmark", ""),
        "agent": episodes[0].get("agent", ""),
        "model": episodes[0].get("model", ""),
        "trial": episodes[0].get("trial", ""),
        "split": "",
        "num_envs": count,
        "score": success / count,
        "success_rate": success / count,
        "failure_rate": 1.0 - success / count,
        "avg_reward": sum(ep["reward"] for ep in episodes) / count,
        "avg_steps": sum(ep["steps"] for ep in episodes) / count,
        "started_at": "",
        "finished_at": "",
        "details": "{}",
    }]


def load_summary(path):
    """Load ``summary.csv``; derive it from episodes if necessary."""
    if os.path.isdir(path):
        summary = os.path.join(path, "summary.csv")
        if os.path.exists(summary):
            return [_normalise_summary(row) for row in _read_csv(summary)]
        return _summary_from_episodes(load_episodes(path))

    if os.path.basename(path) == "episodes.csv":
        return _summary_from_episodes(load_episodes(path))
    return [_normalise_summary(row) for row in _read_csv(path)]


def load_run(benchmark, trial, results_folder="results"):
    """Load the summary for one run."""
    return load_summary(run_dir(trial, results_folder))


def find_runs(results_folder="results"):
    """Return ``(trial, run_dir)`` tuples containing unified result files."""
    found = []
    if not os.path.isdir(results_folder):
        return found
    for trial in sorted(os.listdir(results_folder)):
        directory = os.path.join(results_folder, trial)
        if not os.path.isdir(directory):
            continue
        if (os.path.exists(os.path.join(directory, "summary.csv"))
                or os.path.exists(os.path.join(directory, "episodes.csv"))):
            found.append((trial, directory))
    return found
