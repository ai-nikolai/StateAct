PROMPT1 = [{
            "role" : "system",
            "content" : """
You will interact with the environment to solve the given task.

This is the list of valid commands that are available to you:
- inventory
- go to <dir> [e.g. go to table 1]
- open <obj> [e.g. open door 1]
- close <obj> [e.g. close door 1]
- put <obj> in/on <obj> [e.g. put apple 1 in/on table 1]
- take <obj> from <obj> [e.g. take apple 1 from table 1]
- cool <obj> with <obj> [e.g. cool apple 1 with fridge 1]
- heat <obj> with <obj> [e.g. heat apple 1 with fire 1]

At every step you must output either a thought or an action:

For example:
Your task is to: put a cool apple on the table
think: The task is to cool an apple and put it on the table. So, I should first look through the various places where I can find an apple and then cool it using a fridge and then put it on the table.

For example:
The cabinet 1 is closed.
think: The cabinet 1 is closed, I should open it to see if something is inside.

For example:
think: I want to remind myself of my goal. My overarching goal was to put a cool apple on the table. I now have an apple so I should proceed to cool the apple.

For example:
You open the cabinet 2. The cabinet 2 is open. In it, you see a plate 1.
go to cabinet 1

For example:
Nothing happens.
think: I tried opening the cabinet 1, but I should first be at the location before I can open it.

For example:
You are thinking. Please take an action.
open cabinet 1

For example:
cool apple 1 with fridge 1
"""
        }]


PROMPT2 = [{
            "role" : "system",
            "content" : """
You will interact with the environment to solve the given task.

This is the list of valid commands that are available to you:
- inventory
- go to <dir> [e.g. go to table 1]
- open <obj> [e.g. open door 1]
- close <obj> [e.g. close door 1]
- put <obj> in/on <obj> [e.g. put apple 1 in/on table 1]
- take <obj> from <obj> [e.g. take apple 1 from table 1]
- cool <obj> with <obj> [e.g. cool apple 1 with fridge 1]
- heat <obj> with <obj> [e.g. heat apple 1 with fire 1]

At every step you must output either a thought or an action:

For example:
Your task is to: put a cool apple on the table
think: The task is to cool an apple and put it on the table. So, I should first look through the various places where I can find an apple and then cool it using a fridge and then put it on the table.

For example:
The cabinet 1 is closed.
think: The cabinet 1 is closed, I should open it to see if something is inside.

For example:
think: I want to remind myself of my goal. My overarching goal was to put a cool apple on the table. I now have an apple so I should proceed to cool the apple.

For example:
You open the cabinet 2. The cabinet 2 is open. In it, you see a plate 1.
go to cabinet 1

For example:
Nothing happens.
think: I tried opening the cabinet 1, but I should first be at the location before I can open it. I should try and go to cabinet 1, if I haven't done so already.

For example:
You are thinking. Please take an action.
open cabinet 1

For example:
cool apple 1 with fridge 1
"""
        }]

PROMPT3 = [{
            "role" : "system",
            "content" : """
You will interact with the environment to solve the given task.

This is the list of valid commands that are available to you:
- inventory
- go to <dir> [example: go to table 1]
- open <obj> [example: open door 1]
- close <obj> [example: close door 1]
- put <obj> in/on <obj> [example: put apple 1 in/on table 1]
- take <obj> from <obj> [example: take apple 1 from table 1]
- cool <obj> with <obj> [example: cool apple 1 with fridge 1]
- heat <obj> with <obj> [example: heat apple 1 with fire 1]

At every step you must output either a thought or an action:

For example:
You are in the middle of a room. Looking quickly around you, you see a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 9, a drawer 8, a drawer 7, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a cool mug in shelf.
> think: To solve the task, I need to find and take a mug, then cool it with fridge, then put it in shelf.
You are thinking. Please take an action.
> think: First I need to find a mug. A mug is more likely to appear in countertop (1-3), coffeemachine (1), cabinet (1-9), shelf (1-3), drawer (1-9). I can check one by one, starting with countertop 1.
You are thinking. Please take an action.
> go to countertop 1
On the countertop 1, you see a knife 1, a pan 2, a pan 1, and a plate 1.
> go to countertop 2
On the countertop 2, you see a apple 2, a butterknife 2, a fork 3, a houseplant 1, a knife 2, a lettuce 3, a spatula 1, and a winebottle 1.
> go to countertop 3
On the countertop 3, you see a apple 1, a book 1, a bread 1, a butterknife 3, a glassbottle 2, a glassbottle 1, a knife 3, a lettuce 2, a lettuce 1, a papertowelroll 1, a plate 3, a spoon 1, a statue 1, and a vase 2.
> go to coffeemachine 1
On the coffeemachine 1, you see nothing.
> go to cabinet 1
The cabinet 1 is closed.
> open cabinet 1
You open the cabinet 1. The cabinet 1 is open. In it, you see nothing.
> go to cabinet 2
The cabinet 2 is closed.
> open cabinet 2
You open the cabinet 2. The cabinet 2 is open. In it, you see nothing.
> go to cabinet 3
The cabinet 3 is closed.
> open cabinet 3
You open the cabinet 3. The cabinet 3 is open. In it, you see a pot 1.
> go to cabinet 4
On the cabinet 4, you see nothing.
> go to cabinet 5
The cabinet 5 is closed.
> open cabinet 5
You open the cabinet 5. The cabinet 5 is open. In it, you see nothing.
> go to cabinet 6
The cabinet 6 is closed.
> open cabinet 6
You open the cabinet 6. The cabinet 6 is open. In it, you see a mug 3.
> think: Now I find a mug (3). Next, I need to take it.
You are thinking. Please take an action.
> take mug 3 from cabinet 6
You pick up the mug 3 from the cabinet 6.
> think: Now I take a mug (3). Next, I need to go to a fridge (1) and cool it.
You are thinking. Please take an action.
> go to fridge 1
The fridge 1 is closed.
> cool mug 3 with fridge 1
You cool the mug 3 using the fridge 1.
> think: Now I cool the mug. Next, I need to put it in/on shelf 1.
You are thinking. Please take an action.
> go to shelf 1
On the shelf 1, you see a cup 2, a cup 1, a peppershaker 1, and a saltshaker 1.
> put mug 3 in/on shelf 1
You put the mug 3 in/on the shelf 1.
"""
        }]



PROMPT4 = [{
            "role" : "system",
            "content" : """
You will interact with the environment to solve the given task.

This is the list of valid commands that are available to you:
- inventory
- go to <dir> [example: go to table 1]
- open <obj> [example: open door 1]
- close <obj> [example: close door 1]
- put <obj> in/on <obj> [example: put apple 1 in/on table 1]
- take <obj> from <obj> [example: take apple 1 from table 1]
- cool <obj> with <obj> [example: cool apple 1 with fridge 1]
- heat <obj> with <obj> [example: heat apple 1 with fire 1]

At every step you must output either a thought or an action:

For example:
Input: 
You are in the middle of a room. Looking quickly around you, you see a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 9, a drawer 8, a drawer 7, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a cool mug in shelf.
Output:
think: To solve the task, I need to find and take a mug, then cool it with fridge, then put it in shelf.
Input:
You are thinking. Please take an action.
Ouput:
think: First I need to find a mug. A mug is more likely to appear in countertop (1-3), coffeemachine (1), cabinet (1-9), shelf (1-3), drawer (1-9). I can check one by one, starting with countertop 1.
Input:
You are thinking. Please take an action.
Ouput:
go to countertop 1
Input:
On the countertop 1, you see a knife 1, a pan 2, a pan 1, and a plate 1.
Output:
go to countertop 2
Input:
On the countertop 2, you see a apple 2, a butterknife 2, a fork 3, a houseplant 1, a knife 2, a lettuce 3, a spatula 1, and a winebottle 1.
Ouput:
go to countertop 3
Input:
On the countertop 3, you see a apple 1, a book 1, a bread 1, a butterknife 3, a glassbottle 2, a glassbottle 1, a knife 3, a lettuce 2, a lettuce 1, a papertowelroll 1, a plate 3, a spoon 1, a statue 1, and a vase 2.
Output:
go to coffeemachine 1
Input:
On the coffeemachine 1, you see nothing.
Output:
go to cabinet 1
Input:
The cabinet 1 is closed.
Output:
open cabinet 1
Input:
You open the cabinet 1. The cabinet 1 is open. In it, you see nothing.
Ouput:
go to cabinet 2
Input:
The cabinet 2 is closed.
Output:
open cabinet 2
Input:
You open the cabinet 2. The cabinet 2 is open. In it, you see nothing.
Output:
go to cabinet 3
Input:
The cabinet 3 is closed.
Output:
open cabinet 3
Input:
You open the cabinet 3. The cabinet 3 is open. In it, you see a pot 1.
Output:
go to cabinet 4
Input:
On the cabinet 4, you see nothing.
Output:
go to cabinet 5
Input:
The cabinet 5 is closed.
Output:
open cabinet 5
Input:
You open the cabinet 5. The cabinet 5 is open. In it, you see nothing.
Output:
go to cabinet 6
Input:
The cabinet 6 is closed.
Ouput:
open cabinet 6
Input:
You open the cabinet 6. The cabinet 6 is open. In it, you see a mug 3.
Ouput:
think: Now I find a mug (3). Next, I need to take it.
Input:
You are thinking. Please take an action.
Output:
take mug 3 from cabinet 6
Input:
You pick up the mug 3 from the cabinet 6.
Output:
think: Now I take a mug (3). Next, I need to go to a fridge (1) and cool it.
Input:
You are thinking. Please take an action.
Output:
go to fridge 1
Input:
The fridge 1 is closed.
Output:
cool mug 3 with fridge 1
Input:
You cool the mug 3 using the fridge 1.
Output:
think: Now I cool the mug. Next, I need to put it in/on shelf 1.
Input:
You are thinking. Please take an action.
Output:
go to shelf 1
Input:
On the shelf 1, you see a cup 2, a cup 1, a peppershaker 1, and a saltshaker 1.
Ouput:
put mug 3 in/on shelf 1
Input:
You put the mug 3 in/on the shelf 1.
"""
}]

PROMPT5 = [{
            "role" : "system",
            "content" : """
You will interact with the environment to solve the given task.

This is the list of valid commands that are available to you:
- inventory
- go to <dir> [example: go to table 1]
- open <obj> [example: open door 1]
- close <obj> [example: close door 1]
- put <obj> in/on <obj> [example: put apple 1 in/on table 1]
- take <obj> from <obj> [example: take apple 1 from table 1]
- cool <obj> with <obj> [example: cool apple 1 with fridge 1]
- heat <obj> with <obj> [example: heat apple 1 with fire 1]

At every step you must output either a thought or an action:

For example:
You are in the middle of a room. Looking quickly around you, you see a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 9, a drawer 8, a drawer 7, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a cool mug in shelf.

> think("To solve the task, I need to find and take a mug, then cool it with fridge, then put it in shelf.")

You are thinking...

> think("Ok, first I need to find the mug. I will go to the locations and find where a mug might be.")

You are thinking...

> action("go to countertop 1")

On the countertop 1, you see a knife 1, a pan 2, a pan 1, and a plate 1.

> think("I am still on the task of finding a mug. I did not find it on countertop 1. So, I will continue looking.")

You are thinking ...

> action("go to countertop 2")
"""
        }]


PROMPT6 = [{
            "role" : "system",
            "content" : """
You will interact with the environment to solve the given task.

This is the list of valid commands that are available to you:
- inventory
- go to <dir> [example: go to table 1]
- open <obj> [example: open door 1]
- close <obj> [example: close door 1]
- put <obj> in/on <obj> [example: put apple 1 in/on table 1]
- take <obj> from <obj> [example: take apple 1 from table 1]
- cool <obj> with <obj> [example: cool apple 1 with fridge 1]
- heat <obj> with <obj> [example: heat apple 1 with fire 1]

At every step you must output either a thought or an action:

For example:
User: 
You are in the middle of a room. Looking quickly around you, you see a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 9, a drawer 8, a drawer 7, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a cool mug in shelf.

System:
think("To solve the task, I need to find and take a mug, then cool it with fridge, then put it in shelf.")
think("Ok, first I need to find the mug. I will go to the locations and find where a mug might be.")
action("go to countertop 1")

User:
On the countertop 1, you see a knife 1, a pan 2, a pan 1, and a plate 1.

System:
think("I am still on the task of finding a mug. I did not find it on countertop 1. So, I will continue looking.")
action("go to countertop 2")
"""
        }]



PROMPT7 = [{
            "role" : "system",
            "content" : """
You will interact with the environment to solve the given task.

This is the list of valid commands that are available to you:
<<<
- inventory
- go to <dir> [example: go to table 1]
- open <obj> [example: open door 1]
- close <obj> [example: close door 1]
- put <obj> in/on <obj> [example: put apple 1 in/on table 1]
- take <obj> from <obj> [example: take apple 1 from table 1]
- cool <obj> with <obj> [example: cool apple 1 with fridge 1]
- heat <obj> with <obj> [example: heat apple 1 with fire 1]
>>>

For example:
<<<
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 9, a drawer 8, a drawer 7, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a cool mug in shelf.

Output:
think("To solve the task, I need to find a mug, then take a mug, then cool it with fridge, then put it in shelf.")

Input:
You are thinking.

Output:
think("Ok, first I need to find the mug. I will go to the locations and find where a mug might be.")

Input:
You are thinking.

Output:
action("go to countertop 1")

Input:
On the countertop 1, you see a knife 1, a pan 2, a pan 1, and a plate 1.

Output:
think("I am still on the task of finding a mug. I did not find it on countertop 1. So, I will continue looking.")

Input:
You are thinking.

Output:
action("go to cabinet 1")

Input:
The cabinet 1 is closed.

Ouput:
think("cabinet 1 is closed so I should open it")

Input:
You are thinking.

Output:
action("open cabinet 1")

Input:
You open the cabinet 1. The cabinet 1 is open. In it, you see a mug 3.

Output:
think("I found mug 3, so now I should take it.")

Input:
You are thinking.

Output:
action("take mug 3 from cabinet 1")

Input:
You pick up the mug 3 from the cabinet 1.

Output:
think("Now I have a mug. My goal is to find a mug, then take a mug then cool a mug with a fridge and then put it on the shelf. So, the next step is to find a fridge and cool the mug.")
>>>
"""
        }]




PROMPT = [{
            "role" : "system",
            "content" : """
You will interact with the environment to solve the given task.

This is the list of valid commands that are available to you:
<<<
- inventory
- go to <dir> [example: go to table 1]
- open <obj> [example: open door 1]
- close <obj> [example: close door 1]
- put <obj> in/on <obj> [example: put apple 1 in/on table 1]
- take <obj> from <obj> [example: take apple 1 from table 1]
- cool <obj> with <obj> [example: cool apple 1 with fridge 1]
- heat <obj> with <obj> [example: heat apple 1 with fire 1]
>>>

For example:
<<<
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 9, a drawer 8, a drawer 7, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a cool mug in shelf.

Output:
goal("Find Mug: Pending","Take Mug: Pending","Cool Mug: Pending","Put Cool Mug in Shelf: Pending")
think("Looking at the goals I need to find a mug. This is my next step.")
action("go to countertop 1")

Input:
On the countertop 1, you see a knife 1, a pan 2, a pan 1, and a plate 1.

Output:
goal("Find Mug: Pending","Take Mug: Pending","Cool Mug: Pending","Put Cool Mug in Shelf: Pending")
think("Looking at the goals, I need to find a mug. Countertop 1 did not have a mug so I will go to the next place to find a mug.")
action("go to countertop 2")

Input:
On the countertop 2, you see a apple 2, a butterknife 2, a fork 3, a houseplant 1, a knife 2, a lettuce 3, a spatula 1, and a winebottle 1.

Output:
goal("Find Mug: Pending","Take Mug: Pending","Cool Mug: Pending","Put Cool Mug in Shelf: Pending")
think("Looking at the goals, I need to find a mug. Countertop 2 did not have a mug so I will go to the next place to find a mug.")
action("go to cabinet 1")

Input:
The cabinet 1 is closed.

Ouput:
goal("Find Mug: Pending","Take Mug: Pending","Cool Mug: Pending","Put Cool Mug in Shelf: Pending")
think("Looking at the goals, I need to find a mug. Cabinet 1 is closed so I should open it.")
action("open cabinet 1")


Input:
You open the cabinet 1. The cabinet 1 is open. In it, you see a mug 3.

Output:
goal("Find Mug: Success","Take Mug: Pending","Cool Mug: Pending","Put Cool Mug in Shelf: Pending")
think("I found mug 3, so now I should take it.")
action("take mug 3 from cabinet 1")

Input:
You pick up the mug 3 from the cabinet 1.

Output:
goal("Find Mug: Success","Take Mug: Success","Cool Mug: Pending","Put Cool Mug in Shelf: Pending")
think("Now I have a mug, so now I should cool the mug with a fridge.")
action("go to fridge 1")

Input:
The fridge 1 is closed.

Output:
goal("Find Mug: Success","Take Mug: Success","Cool Mug: Pending","Put Cool Mug in Shelf: Pending")
think("Looking at the goals, I need to cool the mug. I am by the fridge so I can cool the mug.")
action("cool mug 3 with fridge 1")

Input:
You cool the mug 3 using the fridge 1.

Ouput:
goal("Find Mug: Success","Take Mug: Success","Cool Mug: Success","Put Cool Mug in Shelf: Pending")
think("I have a cool mug, now I should put it on the shelf. First, I need to go to the shelf.")
action("go to shelf 1")

Input:
On the shelf 1, you see a cup 2, a cup 1, a peppershaker 1, and a saltshaker 1.

Output:
goal("Find Mug: Success","Take Mug: Success","Cool Mug: Success","Put Cool Mug in Shelf: Pending")
think("Looking at the goals, I need to put the cool mug on the shelf. I am by the shelf so I can put the mug on the shelf.")
action("put mug 3 in/on shelf 1")
>>>
"""
        }]


PROMPT = [{
            "role" : "system",
            "content" : """
You will interact with the environment to solve the given task.

This is the list of valid commands that are available to you:
<<<
- inventory
- go to <dir> [example: go to table 1]
- open <obj> [example: open door 1]
- close <obj> [example: close door 1]
- put <obj> in/on <obj> [example: put apple 1 in/on table 1]
- take <obj> from <obj> [example: take apple 1 from table 1]
- cool <obj> with <obj> [example: cool apple 1 with fridge 1]
- heat <obj> with <obj> [example: heat apple 1 with fire 1]
>>>

For example:
<<<
Input:
You are in the middle of a room. Looking quickly around you, you see a cabinet 9, a cabinet 8, a cabinet 7, a cabinet 6, a cabinet 5, a cabinet 4, a cabinet 3, a cabinet 2, a cabinet 1, a coffeemachine 1, a countertop 3, a countertop 2, a countertop 1, a drawer 9, a drawer 8, a drawer 7, a drawer 6, a drawer 5, a drawer 4, a drawer 3, a drawer 2, a drawer 1, a fridge 1, a garbagecan 1, a microwave 1, a shelf 3, a shelf 2, a shelf 1, a sinkbasin 1, a stoveburner 4, a stoveburner 3, a stoveburner 2, a stoveburner 1, and a toaster 1.
Your task is to: put a cool mug in shelf.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("go to countertop 1")

Input:
On the countertop 1, you see a knife 1, a pan 2, a pan 1, and a plate 1.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("go to countertop 2")

Input:
On the countertop 2, you see a apple 2, a butterknife 2, a fork 3, a houseplant 1, a knife 2, a lettuce 3, a spatula 1, and a winebottle 1.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("go to cabinet 1")

Input:
The cabinet 1 is closed.

Ouput:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("open cabinet 1")


Input:
You open the cabinet 1. The cabinet 1 is open. In it, you see a mug 3.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("take mug 3 from cabinet 1")

Input:
You pick up the mug 3 from the cabinet 1.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
ction("go to fridge 1")

Input:
The fridge 1 is closed.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("cool mug 3 with fridge 1")

Input:
You cool the mug 3 using the fridge 1.

Ouput:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("go to shelf 1")

Input:
On the shelf 1, you see a cup 2, a cup 1, a peppershaker 1, and a saltshaker 1.

Output:
goal("put a cool mug in shelf")
plan("Looking at the goal and the room, I need to first find a mug, then take it, then go to a fridge, then cool the mug with the fridge and then go to the microwave and put the mug in/on the shelf.")
action("put mug 3 in/on shelf 1")
>>>
"""
        }]
