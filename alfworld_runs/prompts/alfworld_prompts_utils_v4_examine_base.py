examine_v4_base_0 = ["""You are in the middle of a room. Looking quickly around you, you see a bed 1, a desk 1, a drawer 3, a drawer 2, a drawer 1, a garbagecan 1, a safe 1, a shelf 5, a shelf 4, a shelf 3, a shelf 2, a shelf 1, a sidetable 2, and a sidetable 1.
Your task is to: look at bowl under the desklamp.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find bowl",
  "thought": "To solve the task, I need to find and take a bowl, then find and use a desklamp. First I need to find a bowl. A bowl is more likely to appear in drawer (1-3), desk (1), sidetable (1-2), shelf (1-5), garbagecan (1). I can check one by one, starting with drawer 1.",
  "action": "go to drawer 1"
}""",
"""On the drawer 1, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1"
  ],
  "current_inventory": "",
  "current_location": "drawer 1",
  "current_objective": "find bowl",
  "thought": "",
  "action": "go to drawer 2"
}""",
"""The drawer 2 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2"
  ],
  "current_inventory": "",
  "current_location": "drawer 2",
  "current_objective": "find bowl",
  "thought": "",
  "action": "open drawer 2"
}""",
"""You open the drawer 2. The drawer 2 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2"
  ],
  "current_inventory": "",
  "current_location": "drawer 2",
  "current_objective": "find bowl",
  "thought": "",
  "action": "go to drawer 3"
}""",
"""The drawer 3 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3"
  ],
  "current_inventory": "",
  "current_location": "drawer 3",
  "current_objective": "find bowl",
  "thought": "",
  "action": "open drawer 3"
}""",
"""You open the drawer 3. The drawer 3 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3"
  ],
  "current_inventory": "",
  "current_location": "drawer 3",
  "current_objective": "find bowl",
  "thought": "",
  "action": "go to desk 1"
}""",
"""On the desk 1, you see a alarmclock 2, a book 1, a cellphone 1, a keychain 1, a laptop 2, a laptop 1, and a pen 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "desk 1"
  ],
  "current_inventory": "",
  "current_location": "desk 1",
  "current_objective": "find bowl",
  "thought": "",
  "action": "go to sidetable 1"
}""",
"""On the sidetable 1, you see a cd 1, a pen 1, and a pencil 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "desk 1",
    "sidetable 1"
  ],
  "current_inventory": "",
  "current_location": "sidetable 1",
  "current_objective": "find bowl",
  "thought": "",
  "action": "go to shelf 1"
}""",
"""On the shelf 1, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "desk 1",
    "sidetable 1",
    "shelf 1"
  ],
  "current_inventory": "",
  "current_location": "shelf 1",
  "current_objective": "find bowl",
  "thought": "",
  "action": "go to shelf 2"
}""",
"""On the shelf 2, you see a bowl 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "desk 1",
    "sidetable 1",
    "shelf 1",
    "shelf 2"
  ],
  "current_inventory": "",
  "current_location": "shelf 2",
  "current_objective": "take bowl",
  "thought": "Now I find a bowl (1). Next, I need to take it.",
  "action": "take bowl 1 from shelf 2"
}""",
"""You pick up the bowl 1 from the shelf 2.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "desk 1",
    "sidetable 1",
    "shelf 1",
    "shelf 2"
  ],
  "current_inventory": "bowl 1",
  "current_location": "shelf 2",
  "current_objective": "find desklamp",
  "thought": "Now I take a bowl (1). Next, I need to find a desklamp. A desklamp is more likely to appear in desk (1), sidetable (1-2), shelf (1-5), bed (1), drawer (1-3). I can check one by one, starting with desk 1.",
  "action": "go to desk 1"
}""",
"""On the desk 1, you see a alarmclock 2, a book 1, a cellphone 1, a keychain 1, a laptop 2, a laptop 1, and a pen 3.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "desk 1",
    "sidetable 1",
    "shelf 1",
    "shelf 2",
    "desk 1"
  ],
  "current_inventory": "bowl 1",
  "current_location": "desk 1",
  "current_objective": "find desklamp",
  "thought": "",
  "action": "go to sidetable 1"
}""",
"""On the sidetable 1, you see a cd 1, a pen 1, and a pencil 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "desk 1",
    "sidetable 1",
    "shelf 1",
    "shelf 2",
    "desk 1",
    "sidetable 1"
  ],
  "current_inventory": "bowl 1",
  "current_location": "sidetable 1",
  "current_objective": "find desklamp",
  "thought": "",
  "action": "go to sidetable 2"
}""",
"""On the sidetable 2, you see a alarmclock 1, a desklamp 1, and a pen 2.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at bowl under the desklamp",
  "plan": "I need to first find a bowl, then find the desklamp, and then use the desklamp to look at the bowl.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "desk 1",
    "sidetable 1",
    "shelf 1",
    "shelf 2",
    "desk 1",
    "sidetable 1",
    "sidetable 2"
  ],
  "current_inventory": "bowl 1",
  "current_location": "sidetable 2",
  "current_objective": "use desklamp",
  "thought": "Now I find a desklamp (1). Next, I need to use it.",
  "action": "use desklamp 1"
}"""
]


examine_v4_base_1 = ["""You are in the middle of a room. Looking quickly around you, you see a bed 1, a drawer 10, a drawer 9, a drawer 8, a drawer 7, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a dresser 1, a garbagecan 1, a shelf 9, a shelf 8, a shelf 7, a shelf 6, a shelf 5, a shelf 4, a shelf 3, a shelf 2, and a shelf 1.
Your task is to: examine the pen with the desklamp.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find pen",
  "thought": "To solve the task, I need to find and take a pen, then find and use a desklamp. First I need to find a pen. A pen is more likely to appear in drawer (1-10), shelf (1-9), bed (1), garbagecan (1). I can check one by one, starting with drawer 1.",
  "action": "go to drawer 1"
}""",
"""The drawer 1 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [
    "drawer 1"
  ],
  "current_inventory": "",
  "current_location": "drawer 1",
  "current_objective": "find pen",
  "thought": "",
  "action": "open drawer 1"
}""",
"""You open the drawer 1. The drawer 1 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [
    "drawer 1"
  ],
  "current_inventory": "",
  "current_location": "drawer 1",
  "current_objective": "find pen",
  "thought": "",
  "action": "go to drawer 2"
}""",
"""The drawer 2 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [
    "drawer 1",
    "drawer 2"
  ],
  "current_inventory": "",
  "current_location": "drawer 2",
  "current_objective": "find pen",
  "thought": "",
  "action": "open drawer 2"
}""",
"""You open the drawer 2. The drawer 2 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [
    "drawer 1",
    "drawer 2"
  ],
  "current_inventory": "",
  "current_location": "drawer 2",
  "current_objective": "find pen",
  "thought": "",
  "action": "go to drawer 3"
}""",
"""The drawer 3 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3"
  ],
  "current_inventory": "",
  "current_location": "drawer 3",
  "current_objective": "find pen",
  "thought": "",
  "action": "open drawer 3"
}""",
"""You open the drawer 3. The drawer 3 is open. In it, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3"
  ],
  "current_inventory": "",
  "current_location": "drawer 3",
  "current_objective": "find pen",
  "thought": "",
  "action": "go to drawer 4"
}""",
"""The drawer 4 is closed.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "drawer 4"
  ],
  "current_inventory": "",
  "current_location": "drawer 4",
  "current_objective": "find pen",
  "thought": "",
  "action": "open drawer 4"
}""",
"""You open the drawer 4. The drawer 4 is open. In it, you see a cd 3, a keychain 1, and a pen 2.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "drawer 4"
  ],
  "current_inventory": "",
  "current_location": "drawer 4",
  "current_objective": "take pen",
  "thought": "Now I find a pen (2). Next, I need to take it.",
  "action": "take pen 2 from drawer 4"
}""",
"""You pick up the pen 2 from the drawer 4.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "drawer 4"
  ],
  "current_inventory": "pen 2",
  "current_location": "drawer 4",
  "current_objective": "find desklamp",
  "thought": "Now I take a pen (2). Next, I need to find a desklamp. A desklamp is more likely to appear in dresser (1), shelf (1-9), bed (1), garbagecan (1), drawer (1-10). I can check one by one, starting with dresser 1.",
  "action": "go to dresser 1"
}""",
"""On the dresser 1, you see a alarmclock 2, a alarmclock 1, a book 1, a cd 1, a creditcard 1, a desklamp 1, a keychain 2, a pen 3, and a pen 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "examine the pen with the desklamp",
  "plan": "I need to first find a pen, then find the desklamp, and then use the desklamp to examine the pen.",
  "locations_visited": [
    "drawer 1",
    "drawer 2",
    "drawer 3",
    "drawer 4",
    "dresser 1"
  ],
  "current_inventory": "pen 2",
  "current_location": "dresser 1",
  "current_objective": "use desklamp",
  "thought": "Now I find a desklamp (1). Next, I need to use it.",
  "action": "use desklamp 1"
}"""
]

examine_v4_base_2=["""You are in the middle of a room. Looking quickly around you, you see a coffeetable 1, a diningtable 1, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a dresser 1, a garbagecan 1, a sidetable 2, a sidetable 1, and a sofa 1.
Your task is to: look at statue under the desklamp.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at statue under the desklamp",
  "plan": "I need to first find a statue, then take it, then find the desklamp, and then use the desklamp to examine the statue.",
  "locations_visited": [],
  "current_inventory": "",
  "current_location": "starting location",
  "current_objective": "find statue",
  "thought": "To solve the task, I need to find and take a statue, then find and use a desklamp. First I need to find a statue. A statue is more likely to appear in dresser (1), coffeetable (1), sidetable (1-2), diningtable (1), sofa (1), garbagecan (1). I can check one by one, starting with dresser 1.",
  "action": "go to dresser 1"
}""",
"""On the dresser 1, you see a cellphone 3, a newspaper 2, a statue 1, and a television 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at statue under the desklamp",
  "plan": "I need to first find a statue, then take it, then find the desklamp, and then use the desklamp to examine the statue.",
  "locations_visited": [
    "dresser 1"
  ],
  "current_inventory": "",
  "current_location": "dresser 1",
  "current_objective": "take statue",
  "thought": "Now I find a statue (1). Next, I need to take it.",
  "action": "take statue 1 from dresser 1"
}""",
"""You pick up the statue 1 from the dresser 1.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at statue under the desklamp",
  "plan": "I need to first find a statue, then take it, then find the desklamp, and then use the desklamp to examine the statue.",
  "locations_visited": [
    "dresser 1"
  ],
  "current_inventory": "statue 1",
  "current_location": "dresser 1",
  "current_objective": "find desklamp",
  "thought": "Now I take a statue (1). Next, I need to find a desklamp. A desklamp is more likely to appear in sidetable (1-2), coffeetable (1), diningtable (1). I can check one by one, starting with sidetable 1.",
  "action": "go to sidetable 1"
}""",
"""On the sidetable 1, you see nothing.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at statue under the desklamp",
  "plan": "I need to first find a statue, then take it, then find the desklamp, and then use the desklamp to examine the statue.",
  "locations_visited": [
    "dresser 1",
    "sidetable 1"
  ],
  "current_inventory": "statue 1",
  "current_location": "sidetable 1",
  "current_objective": "find desklamp",
  "thought": "",
  "action": "go to sidetable 2"
}""",
"""On the sidetable 2, you see a desklamp 3, a newspaper 1, and a statue 2.""",
"""{
  "prompt": "I need to look at the goal, plan and history and generate a valid next action that follows the plan.",
  "goal": "look at statue under the desklamp",
  "plan": "I need to first find a statue, then take it, then find the desklamp, and then use the desklamp to examine the statue.",
  "locations_visited": [
    "dresser 1",
    "sidetable 1",
    "sidetable 2"
  ],
  "current_inventory": "statue 1",
  "current_location": "sidetable 2",
  "current_objective": "use desklamp",
  "thought": "Now I find a desklamp (3). Next, I need to use it.",
  "action": "use desklamp 3"
}"""
]