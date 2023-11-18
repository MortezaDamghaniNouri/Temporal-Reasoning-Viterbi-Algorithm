





# This function reads information from state_weights.txt
def states_weights_file_reader():
    initial_states_file = open("state_weights.txt", "rt")
    lines = []
    while True:
        line = initial_states_file.readline()
        if line == "":
            break
        lines.append(line.rstrip("\n"))
    initial_states_file.close()
    output = []
    i = 2
    while i < len(lines):
        temp_list = lines[i].split(" ")
        output.append([temp_list[0].strip("\""), int(temp_list[1])])
        i += 1

    sum_of_weights = 0
    i = 0
    while i < len(output):
        sum_of_weights += output[i][1]
        i += 1

    i = 0
    while i < len(output):
        output[i][1] = output[i][1] / sum_of_weights
        i += 1

    return output


# This function reads information from state_action_state_weights.txt
def states_action_states_weights_file_reader():
    states_action_states_file = open("state_action_state_weights.txt", "rt")
    lines = []
    while True:
        line = states_action_states_file.readline()
        if line == "":
            break
        lines.append(line.rstrip("\n"))
    states_action_states_file.close()
    line_one_elements = lines[1].split(" ")
    default_weight = int(line_one_elements[3])
    output = []
    sum_of_weights = default_weight
    i = 2
    while i < len(lines):
        temp_list = lines[i].split(" ")
        output.append([temp_list[0].strip("\""), temp_list[1].strip("\""), temp_list[2].strip("\""), int(temp_list[3])])
        sum_of_weights += int(temp_list[3])
        i += 1

    default_weight = default_weight / sum_of_weights
    # normalizing the probabilities
    probabilities = []
    i = 0
    while i < len(output):
        current_line = output[i]
        down = 0
        j = 0
        while j < len(output):
            if output[j][0] == current_line[0] and output[j][1] == current_line[1]:
                down += output[j][3]
            j += 1

        probabilities.append(current_line[3] / down)
        i += 1

    i = 0
    while i < len(output):
        output[i][3] = probabilities[i]
        i += 1

    return default_weight, output


# This function reads information from states_observation_weights.txt
def states_observation_weights_file_reader():
    states_observations_file = open("state_observation_weights.txt", "rt")
    lines = []
    while True:
        line = states_observations_file.readline()
        if line == "":
            break
        lines.append(line.rstrip("\n"))
    states_observations_file.close()
    line_one_elements = lines[1].split(" ")
    default_weight = int(line_one_elements[3])
    output = []
    sum_of_weights = default_weight
    i = 2
    while i < len(lines):
        temp_list = lines[i].split(" ")
        output.append([temp_list[0].strip("\""), temp_list[1].strip("\""), int(temp_list[2])])
        sum_of_weights += int(temp_list[2])
        i += 1

    default_weight = default_weight / sum_of_weights
    # normalizing the probabilities
    probabilities = []
    i = 0
    while i < len(output):
        current_line = output[i]
        down = 0
        j = 0
        while j < len(output):
            if output[j][0] == current_line[0]:
                down += output[j][2]
            j += 1
        probabilities.append(current_line[2] / down)
        i += 1

    i = 0
    while i < len(output):
        output[i][2] = probabilities[i]
        i += 1

    return default_weight, output


# This function reads information from observation_actions.txt
def observation_actions_file_reader():
    observations_actions_file = open("observation_actions.txt", "rt")
    lines = []
    while True:
        line = observations_actions_file.readline()
        if line == "":
            break
        lines.append(line.rstrip("\n"))
    observations_actions_file.close()
    output = []
    i = 2
    while i < len(lines):
        temp_list = lines[i].split(" ")
        new_list = []
        j = 0
        while j < len(temp_list):
            new_list.append(temp_list[j].strip("\""))
            j += 1
        output.append(new_list)
        i += 1
    return output


# main part of the code starts here
initial_states_and_probabilities = states_weights_file_reader()
states_action_states_default_weight, states_action_states_and_probabilities = states_action_states_weights_file_reader()
states_observations_default_weight, states_observations_and_probabilities = states_observation_weights_file_reader()
observations_actions_pairs = observation_actions_file_reader()


print(states_observations_and_probabilities)



# Viterbi algorithm is implemented here
states = []
first_state_probabilities = []
first_observation = observations_actions_pairs[0][0]
i = 0
while i < len(initial_states_and_probabilities):
    current_state = initial_states_and_probabilities[i][0]
    observation_exist = False
    j = 0
    while j < len(states_observations_and_probabilities):
        if states_observations_and_probabilities[j][0] == current_state and states_observations_and_probabilities[j][1] == first_observation:
            observation_exist = True
            alpha = initial_states_and_probabilities[i][1] * states_observations_and_probabilities[j][2]
            break
        j += 1

    if not observation_exist:
        alpha = initial_states_and_probabilities[i][1] * states_observations_default_weight

    first_state_probabilities.append([current_state, alpha])
    i += 1

prob_list = []
i = 0
while i < len(first_state_probabilities):
    prob_list.append(first_state_probabilities[1])
    i += 1
maximum = max(prob_list)
alpha = 0
i = 0
while i < len(first_state_probabilities):
    if first_state_probabilities[i][1] == maximum:
        alpha = maximum
        states.append(first_state_probabilities[i][0])
    i += 1







i = 0
while i < len(initial_states_and_probabilities):












    i += 1





































