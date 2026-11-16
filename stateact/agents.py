"""Reasoning agents: ReAct, AgentBench, StateAct, Reflexion and ADaPT.

An agent only needs one method::

    action, state = agent.run_step(observation)

The model is any callable ``llm(prompt, stop=None) -> str``. The
:class:`stateact.llms.LLM` client is the standard implementation and talks to
any OpenAI-compatible endpoint.

Benchmark-specific prompt examples are passed in as
``example_trajectories``; the agents themselves contain no ALFWorld,
WebShop or TextCraft logic.

``keep_n_context`` controls interaction-history truncation: ``-1`` keeps all,
``0`` keeps only the current observation, and ``n`` keeps the last ``n``
observation/response pairs. The original prompt and examples are always kept.
"""

import json
import re

__all__ = [
    "BaseAgent",
    "ReActAgent",
    "AgentBenchAgent",
    "StateActAgent",
    "ReflexionAgent",
    "AdaptAgent",
]

ACTION_RE = re.compile(r"(?im)^\s*action\s*:\s*(.+?)\s*$")
THOUGHT_RE = re.compile(r"(?im)^\s*(?:think|thought)\s*:\s*(.+?)\s*$")
AGENTBENCH_ACTION_RE = re.compile(r"(?im)^\s*ACTION\s*:\s*(.+?)\s*$")
AGENTBENCH_THOUGHT_RE = re.compile(r"(?im)^\s*THOUGHT\s*:\s*(.+?)\s*$")
KEY_VALUE_RE = re.compile(r"(?m)^\s*([A-Za-z][A-Za-z0-9_ -]*)\s*:\s*(.*)$")


class BaseAgent:
    """Shared prompt/history/parsing machinery for all agents."""

    default_prompt_order = ("thought", "action")
    default_stop = ["\n\n"]
    continue_message = "OK."

    def __init__(self, llm, example_trajectories="", prompt_order=None,
                 system_prompt="", format_instructions="", stop=None,
                 max_turns=3, verbose=False, keep_n_context=-1):
        self.llm = llm
        self.example_trajectories = example_trajectories or ""
        self.prompt_order = list(prompt_order or self.default_prompt_order)
        self.system_prompt = system_prompt
        self.format_instructions = format_instructions
        self.stop = self.default_stop if stop is None else stop
        self.max_turns = max_turns
        self.verbose = verbose
        self.keep_n_context = keep_n_context
        self.history = []
        self.state = {}

    # -- model / prompt -------------------------------------------------
    def _call_llm(self, prompt):
        try:
            return self.llm(prompt, stop=self.stop)
        except TypeError:
            return self.llm(prompt)

    def format_state(self, state):
        if not isinstance(state, dict):
            return str(state)
        return "\n".join(
            f"{key}: {state.get(key, 'None')}" for key in self.prompt_order
        )

    def _examples_text(self):
        examples = self.example_trajectories
        if not examples:
            return ""
        if isinstance(examples, str):
            return examples
        return "\n\n".join(self.format_state(example) for example in examples)

    def _context_start(self, history):
        """Index where the visible interaction context starts.

        ``keep_n_context=-1`` keeps everything. ``0`` keeps no previous
        interaction, ``1`` keeps the last observation/response pair, etc.
        The original prompt/examples are always added separately.
        """
        if self.keep_n_context is None or self.keep_n_context < 0:
            return 0
        if self.keep_n_context == 0:
            return len(history)
        user_indices = [
            index for index, entry in enumerate(history)
            if entry["role"] == "user"
        ]
        if len(user_indices) <= self.keep_n_context:
            return 0
        return user_indices[-self.keep_n_context]

    def _visible_history(self, current_step_start=0):
        if current_step_start:
            previous = self.history[:current_step_start]
            return (
                previous[self._context_start(previous):]
                + self.history[current_step_start:]
            )
        return self.history[self._context_start(self.history):]

    def build_prompt(self, current_step_start=0):
        parts = []
        if self.system_prompt:
            parts.append(self.system_prompt)
        examples = self._examples_text()
        if examples:
            parts.append("Examples:\n" + examples)
        if self.format_instructions:
            parts.append(self.format_instructions)

        parts.append("Interaction:")
        for entry in self._visible_history(current_step_start):
            if entry["role"] == "user":
                parts.append(f"Observation: {entry['content']}")
            else:
                parts.append(">" + entry["content"])
        parts.append(">")
        return "\n".join(parts)

    # -- parsing --------------------------------------------------------
    def parse_response(self, response):
        raise NotImplementedError

    def _parse_labelled(self, response):
        thought = THOUGHT_RE.search(response)
        action = ACTION_RE.search(response)
        state = ""
        if thought:
            state = {"thought": thought.group(1).strip()}
        return {
            "action": action.group(1).strip() if action else "",
            "state": state,
            "thought": thought.group(1).strip() if thought else "",
        }

    # -- agent loop -----------------------------------------------------
    def reset(self):
        self.history = []
        self.state = {}

    def run_step(self, observation):
        current_step_start = len(self.history)
        self.history.append({"role": "user", "content": observation})
        for _ in range(self.max_turns):
            prompt = self.build_prompt(current_step_start=current_step_start)
            response = self._call_llm(prompt)
            if self.verbose:
                print(response)
            parsed = self.parse_response(response)
            parsed_state = parsed.get("state", "")
            if isinstance(parsed_state, dict):
                self.state.update(parsed_state)
            elif parsed_state:
                self.state = parsed_state
            self.history.append({"role": "assistant", "content": response})

            action = parsed.get("action", "")
            if action:
                return action, self.state
            # ReAct-style thought turn: feed the environment's "OK." and ask
            # for the actual action on the next model call.
            self.history.append(
                {"role": "user", "content": self.continue_message}
            )
        raise RuntimeError(
            "Agent did not produce an action after "
            f"{self.max_turns} turns. Last response:\n{response}"
        )


class ReActAgent(BaseAgent):
    """ReAct baseline: ``think: ...`` then ``action: ...``."""

    default_prompt_order = ("thought", "action")
    default_stop = ["\n"]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "format_instructions",
            "Respond with a thought line, then an action line:\n"
            "think: <reasoning>\naction: <single environment action>",
        )
        super().__init__(*args, **kwargs)

    def parse_response(self, response):
        parsed = self._parse_labelled(response)
        if not parsed["action"] and not parsed["thought"]:
            # Some models return a bare action.
            stripped = response.strip()
            if stripped and "\n" not in stripped:
                parsed["action"] = stripped
        return parsed


class AgentBenchAgent(BaseAgent):
    """AgentBench baseline using ``THOUGHT:`` / ``ACTION:`` labels."""

    default_prompt_order = ("thought", "action")
    default_stop = ["\n"]

    def __init__(self, *args, **kwargs):
        kwargs.setdefault(
            "format_instructions",
            "Respond with:\nTHOUGHT: <reasoning>\nACTION: <single environment action>",
        )
        super().__init__(*args, **kwargs)

    def parse_response(self, response):
        thought = AGENTBENCH_THOUGHT_RE.search(response)
        action = AGENTBENCH_ACTION_RE.search(response)
        return {
            "action": action.group(1).strip() if action else "",
            "state": {"thought": thought.group(1).strip()} if thought else "",
            "thought": thought.group(1).strip() if thought else "",
        }


class StateActAgent(BaseAgent):
    """StateAct with either a string or JSON response format.

    Parameters
    ----------
    format:
        ``"string"`` / ``"text"`` for ``goal: ...`` lines, or ``"json"`` for
        a JSON object with the same keys.
    prompt_order:
        Keys the model should produce, e.g.
        ``["goal", "thought", "action"]``.
    """

    def __init__(self, *args, format="string", prompt_order=None, **kwargs):
        self.format = "json" if str(format).lower() == "json" else "string"
        prompt_order = list(prompt_order or ["goal", "thought", "action"])
        kwargs.setdefault("prompt_order", prompt_order)
        if self.format == "json":
            keys = ", ".join(f'"{key}"' for key in prompt_order)
            kwargs.setdefault(
                "format_instructions",
                f"Respond with a single JSON object containing the keys: {keys}.",
            )
        else:
            lines = "\n".join(f"{key}: <value>" for key in prompt_order)
            kwargs.setdefault(
                "format_instructions",
                "Respond with one line per key:\n" + lines,
            )
        super().__init__(*args, **kwargs)

    def format_state(self, state):
        if not isinstance(state, dict):
            return str(state)
        if self.format == "json":
            return json.dumps(state, indent=2, sort_keys=False)
        return "\n".join(
            f"{key}: {state.get(key, 'None')}" for key in self.prompt_order
        )

    def _parse_string(self, response):
        state = {}
        for key, value in KEY_VALUE_RE.findall(response):
            key = key.strip().lower().replace(" ", "_")
            state[key] = value.strip()
        action = state.pop("action", "")
        return {"action": action, "state": state, "thought": state.get("thought", "")}

    def parse_response(self, response):
        if self.format == "json":
            try:
                start = response.find("{")
                end = response.rfind("}")
                if start >= 0 and end > start:
                    data = json.loads(response[start:end + 1])
                    if isinstance(data, dict):
                        action = data.get("action", "")
                        state = {
                            key: value for key, value in data.items()
                            if key != "action"
                        }
                        return {
                            "action": action,
                            "state": state,
                            "thought": state.get("thought", ""),
                        }
            except (TypeError, ValueError):
                pass
        parsed = self._parse_string(response)
        if not parsed["action"]:
            # Fall back to a bare action line.
            match = ACTION_RE.search(response)
            if match:
                parsed["action"] = match.group(1).strip()
        return parsed


class ReflexionAgent:
    """Reflexion wrapper around any base agent.

    After an unsuccessful episode, :func:`reflect` asks the model for a short
    reflection; subsequent observations include those reflections.
    """

    def __init__(self, base_agent, llm=None, max_reflections=5):
        self.base_agent = base_agent
        self.llm = llm or getattr(base_agent, "llm", None)
        self.max_reflections = max_reflections
        self.reflections = []

    def reset(self, preserve_memory=False):
        self.base_agent.reset()
        if not preserve_memory:
            self.reflections = []

    def run_step(self, observation):
        if self.reflections:
            observation = (
                observation
                + "\n\nReflections from previous attempts:\n"
                + "\n".join(f"- {item}" for item in self.reflections)
            )
        return self.base_agent.run_step(observation)

    def reflect(self, observation, action, reward=0.0, done=True, info=None):
        if self.llm is None:
            return None
        prompt = (
            "You are reflecting on a failed agent episode.\n"
            f"Last observation:\n{observation}\n"
            f"Action taken: {action}\n"
            f"Reward: {reward}\n"
            "Write one short reflection about what went wrong and what to do "
            "differently next time."
        )
        reflection = self.llm(prompt)
        self.reflections.append(reflection.strip())
        self.reflections = self.reflections[-self.max_reflections:]
        return reflection

    def finish_episode(self, observation="", action="", reward=0.0, done=True,
                       info=None, success=None):
        if success is None:
            success = reward >= 1.0
        if not success:
            return self.reflect(observation, action, reward, done, info)
        return None


class AdaptAgent:
    """Lightweight ADaPT-style wrapper.

    The base agent is tried first. If it produces no action, the model is
    asked for a short decomposition and the base agent is retried with that
    plan appended to the observation.
    """

    def __init__(self, base_agent, llm=None, max_depth=2):
        self.base_agent = base_agent
        self.llm = llm or getattr(base_agent, "llm", None)
        self.max_depth = max_depth

    def reset(self):
        self.base_agent.reset()

    def run_step(self, observation):
        context = observation
        last_error = None
        for depth in range(self.max_depth + 1):
            try:
                return self.base_agent.run_step(context)
            except RuntimeError as exc:
                last_error = exc
                if self.llm is None or depth == self.max_depth:
                    break
                plan = self.llm(
                    "Break the task into a short ordered list of subtasks. "
                    f"Observation:\n{observation}"
                )
                context = (
                    f"{observation}\n\nSuggested plan (depth {depth + 1}):\n{plan}"
                )
        raise RuntimeError(f"ADaPT failed after {self.max_depth} retries: {last_error}")
