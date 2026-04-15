"""
MODULE 5: AUTOMATION ENGINE
Detects repetitive tasks and manages saved workflows.
"""

import memory
from voice import speak

SUGGESTION_THRESHOLD = 4  # suggest automation after N repetitions

def check_and_suggest(action_name):
    """After executing an action, check if it's repetitive enough to suggest automation."""
    repetitive = memory.get_repetitive_actions(threshold=SUGGESTION_THRESHOLD)
    if action_name in repetitive:
        count = repetitive[action_name]
        # Only suggest once every 5 times to avoid being annoying
        if count % 5 == 0:
            speak(f"You've done {action_name.replace('_', ' ')} {count} times. Want me to save this as a workflow?")
            return True
    return False

def save_workflow_from_steps(name, steps):
    """Save a multi-step workflow by name."""
    memory.save_workflow(name, steps)
    return f"Workflow '{name}' saved with {len(steps)} steps."

def run_workflow(name):
    """Execute a saved workflow."""
    import brain
    steps = memory.get_workflow(name)
    if not steps:
        return f"No workflow named '{name}' found."
    results = []
    for step in steps:
        result = brain.execute_action(step)
        results.append(result)
    return f"Workflow '{name}' complete. {len(steps)} steps done."

def list_workflows():
    workflows = memory.get_all_workflows()
    if not workflows:
        return "No saved workflows yet."
    return "Saved workflows: " + ", ".join(workflows.keys())
