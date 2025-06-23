# History management (for step/back functionality)

import copy

def save_state(open_set, visited, current_node, parents, open_dict, found, final_path, history):
    history.append((
        copy.deepcopy(open_set),
        copy.deepcopy(visited),
        copy.deepcopy(current_node),
        copy.deepcopy(parents),
        copy.deepcopy(open_dict),
        found,
        copy.deepcopy(final_path),
    ))

def load_previous_state(history):
    if len(history) > 1:
        history.pop()
    return copy.deepcopy(history[-1])

def save_state_bidirectional(queue_start, queue_goal, visited_start, visited_goal, expanded_node, parents_start, parents_goal, found, final_path, history):
    history.append((
        copy.deepcopy(queue_start),
        copy.deepcopy(queue_goal),
        copy.deepcopy(visited_start),
        copy.deepcopy(visited_goal),
        copy.deepcopy(expanded_node),
        copy.deepcopy(parents_start),
        copy.deepcopy(parents_goal),
        found,
        copy.deepcopy(final_path)
    ))

def load_previous_state_bidirectional(history):
    if len(history) > 1:
        history.pop()
    return copy.deepcopy(history[-1])
