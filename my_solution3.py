import copy
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
    number_of_triples = int(line_one_elements[0])
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
    i = 1
    while i <= number_of_triples:
        probabilities.append(-1)
        i += 1

    i = 0
    while i < len(output):
        if probabilities[i] == -1:
            current_line = output[i]
            down = 0
            j = 0
            list_of_js = []
            while j < len(output):
                if output[j][0] == current_line[0] and output[j][1] == current_line[1]:
                    down += output[j][3]
                    list_of_js.append(j)
                j += 1

            k = 0
            while k < len(list_of_js):
                s = list_of_js[k]
                probabilities[s] = output[s][3] / down
                k += 1

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


# This function generates the output file
def output_file_generator(input_states):
    output_file = open("states.txt", "wt")
    output_file.write("states\n")
    output_file.write(str(len(input_states)) + "\n")
    i = 0
    while i < len(input_states):
        output_file.write("\"" + input_states[i] + "\"" + "\n")
        i += 1
    output_file.close()


# main part of the code starts here
initial_states_and_probabilities = states_weights_file_reader()
states_action_states_default_weight, states_action_states_and_probabilities = states_action_states_weights_file_reader()
states_observations_default_weight, states_observations_and_probabilities = states_observation_weights_file_reader()
observations_actions_pairs = observation_actions_file_reader()



print("now running viterbi algorithm...")



# Viterbi algorithm is implemented here
alphas_list = []
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

i = 0
while i < len(first_state_probabilities):
    alphas_list.append([first_state_probabilities[i][0], first_state_probabilities[i][1], []])
    i += 1

previous_probabilities_list = first_state_probabilities
i = 1
while i < len(observations_actions_pairs):
    print("now inside")
    current_action = observations_actions_pairs[i - 1][1]
    current_observation = observations_actions_pairs[i][0]
    alphas_list_copy = copy.deepcopy(alphas_list)
    j = 0
    while j < len(initial_states_and_probabilities):
        current_state = initial_states_and_probabilities[j][0]
        observation_exist = False
        k = 0
        while k < len(states_observations_and_probabilities):
            if states_observations_and_probabilities[k][0] == current_state and states_observations_and_probabilities[k][1] == current_observation:
                observation_exist = True
                theta = states_observations_and_probabilities[k][2]
                break
            k += 1
        if not observation_exist:
            theta = states_observations_default_weight

        print("Before this part")
        temp_list = []
        k = 0
        while k < len(previous_probabilities_list):
            previous_state = previous_probabilities_list[k][0]
            state_action_exist = False
            h = 0
            while h < len(states_action_states_and_probabilities):
                if states_action_states_and_probabilities[h][0] == previous_state and states_action_states_and_probabilities[h][2] == current_state and states_action_states_and_probabilities[h][1] == current_action:
                    state_action_exist = True
                    action_probability = states_action_states_and_probabilities[h][3]
                    break
                h += 1
            if not state_action_exist:
                action_probability = states_action_states_default_weight

            current_alpha = previous_probabilities_list[k][1] * action_probability * theta
            temp_list.append([previous_probabilities_list[k][0], current_alpha])
            k += 1
        print("after this part")
        probs = []
        k = 0
        while k < len(temp_list):
            probs.append(temp_list[k][1])
            k += 1
        maximum = max(probs)

        if i == 1:
            k = 0
            while k < len(temp_list):
                if temp_list[k][1] == maximum:
                    alphas_list[j][1] = maximum
                    chosen_state = temp_list[k][0]
                    alphas_list[j][2].append(chosen_state)
                    break
                k += 1

        else:
            k = 0
            while k < len(temp_list):
                if temp_list[k][1] == maximum:
                    alphas_list[j][1] = maximum
                    chosen_state = temp_list[k][0]
                    alphas_list[j][2] = copy.deepcopy(alphas_list_copy[k][2])
                    alphas_list[j][2].append(chosen_state)
                    break
                k += 1
        print("This is J: " + str(j))
        j += 1

    j = 0
    while j < len(previous_probabilities_list):
        previous_probabilities_list[j][1] = alphas_list[j][1]
        j += 1

    print(i)

    i += 1

probs = []
i = 0
while i < len(alphas_list):
    probs.append(alphas_list[i][1])
    i += 1
maximum = max(probs)
i = 0
while i < len(alphas_list):
    if alphas_list[i][1] == maximum:
        alphas_list[i][2].append(alphas_list[i][0])
        output_file_generator(alphas_list[i][2])
        break
    i += 1

















