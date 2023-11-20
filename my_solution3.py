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
    sum_of_weights = 0
    i = 2
    while i < len(lines):
        temp_list = lines[i].split(" ")
        output.append([temp_list[0].strip("\""), int(temp_list[1])])
        sum_of_weights += int(temp_list[1])
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
    output_dictionary = {}
    reverse_output_dictionary = {}
    check_list = []
    i = 1
    while i <= number_of_triples:
        check_list.append(0)
        i += 1
    i = 0
    while i < len(output):
        if check_list[i] == 0:
            current_line = output[i]
            list_of_js = []
            j = 0
            while j < len(output):
                if output[j][2] == current_line[2] and output[j][1] == current_line[1]:
                    list_of_js.append(j)
                j += 1

            reverse_output_dictionary[current_line[2] + current_line[1]] = list_of_js
            k = 0
            while k < len(list_of_js):
                s = list_of_js[k]
                check_list[s] = 1
                k += 1

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
            output_dictionary[current_line[0] + current_line[1]] = list_of_js
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

    return default_weight, output, output_dictionary, reverse_output_dictionary


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
    number_of_pairs = int(line_one_elements[0])
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
    i = 1
    while i <= number_of_pairs:
        probabilities.append(-1)
        i += 1

    output_dictionary = {}
    reverse_output_dictionary = {}
    check_list = []
    i = 0
    while i < number_of_pairs:
        check_list.append(0)
        i += 1

    i = 0
    while i < len(output):
        if check_list[i] == 0:
            current_line = output[i]
            list_of_js = []
            j = 0
            while j < len(output):
                if current_line[1] == output[j][1]:
                    list_of_js.append(j)
                j += 1

            reverse_output_dictionary[current_line[1]] = list_of_js
            k = 0
            while k < len(list_of_js):
                s = list_of_js[k]
                check_list[s] = 1
                k += 1

        i += 1

    i = 0
    while i < len(output):
        if probabilities[i] == -1:
            current_line = output[i]
            down = 0
            j = 0
            list_of_js = []
            while j < len(output):
                if output[j][0] == current_line[0]:
                    down += output[j][2]
                    list_of_js.append(j)
                j += 1

            output_dictionary[current_line[0]] = list_of_js
            k = 0
            while k < len(list_of_js):
                s = list_of_js[k]
                probabilities[s] = output[s][2] / down
                k += 1

        i += 1

    i = 0
    while i < len(output):
        output[i][2] = probabilities[i]
        i += 1

    return default_weight, output, output_dictionary, reverse_output_dictionary


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


# This function finds the maximum element in the input list and its corresponding index
def maximum_finder(input_list):
    output_maximum = input_list[0]
    output_index = 0
    i = 1
    while i < len(input_list):
        if input_list[i] > output_maximum:
            output_maximum = input_list[i]
            output_index = i
        i += 1
    return output_maximum, output_index


# main part of the code starts here
initial_states_and_probabilities = states_weights_file_reader()
states_action_states_default_weight, states_action_states_and_probabilities, states_action_dictionary, reverse_states_action_dictionary = states_action_states_weights_file_reader()
states_observations_default_weight, states_observations_and_probabilities, states_observations_dictionary, reverse_states_observations_dictionary = states_observation_weights_file_reader()
observations_actions_pairs = observation_actions_file_reader()

# Viterbi algorithm is implemented here
alphas_list = []
first_state_probabilities = []
first_observation = observations_actions_pairs[0][0]
i = 0
while i < len(initial_states_and_probabilities):
    current_state = initial_states_and_probabilities[i][0]
    observation_exist = False
    f_list = states_observations_dictionary[current_state]
    b_list = reverse_states_observations_dictionary[first_observation]
    if len(f_list) >= len(b_list):
        list_of_indexes = b_list
    else:
        list_of_indexes = f_list
    h = 0
    while h < len(list_of_indexes):
        j = list_of_indexes[h]
        if states_observations_and_probabilities[j][0] == current_state and states_observations_and_probabilities[j][1] == first_observation:
            observation_exist = True
            alpha = initial_states_and_probabilities[i][1] * states_observations_and_probabilities[j][2]
            break
        h += 1
    if not observation_exist:
        alpha = initial_states_and_probabilities[i][1] * states_observations_default_weight
    first_state_probabilities.append([current_state, alpha])
    alphas_list.append([current_state, alpha, []])
    i += 1

previous_probabilities_list = first_state_probabilities
i = 1
while i < len(observations_actions_pairs):
    current_action = observations_actions_pairs[i - 1][1]
    current_observation = observations_actions_pairs[i][0]
    alphas_list_copy = copy.deepcopy(alphas_list)
    j = 0
    while j < len(initial_states_and_probabilities):
        current_state = initial_states_and_probabilities[j][0]
        observation_exist = False
        f_list = states_observations_dictionary[current_state]
        b_list = reverse_states_observations_dictionary[current_observation]
        if len(f_list) >= len(b_list):
            list_of_observations_indexes = b_list
        else:
            list_of_observations_indexes = f_list
        t = 0
        while t < len(list_of_observations_indexes):
            k = list_of_observations_indexes[t]
            if states_observations_and_probabilities[k][0] == current_state and states_observations_and_probabilities[k][1] == current_observation:
                observation_exist = True
                theta = states_observations_and_probabilities[k][2]
                break
            t += 1

        if not observation_exist:
            theta = states_observations_default_weight

        temp_list = []
        maximum_current_alpha = -1
        maximum_element_index = -1
        k = 0
        while k < len(previous_probabilities_list):
            previous_state = previous_probabilities_list[k][0]
            state_action_exist = False
            forward_list = states_action_dictionary[previous_state + current_action]
            reverse_list = reverse_states_action_dictionary[current_state + current_action]
            if len(forward_list) >= len(reverse_list):
                list_of_indexes = reverse_list
            else:
                list_of_indexes = forward_list
            s = 0
            while s < len(list_of_indexes):
                h = list_of_indexes[s]
                if states_action_states_and_probabilities[h][0] == previous_state and states_action_states_and_probabilities[h][2] == current_state and states_action_states_and_probabilities[h][1] == current_action:
                    state_action_exist = True
                    action_probability = states_action_states_and_probabilities[h][3]
                    break
                s += 1

            if not state_action_exist:
                action_probability = states_action_states_default_weight

            current_alpha = previous_probabilities_list[k][1] * action_probability * theta
            temp_list.append([previous_probabilities_list[k][0], current_alpha])
            if current_alpha > maximum_current_alpha:
                maximum_current_alpha = current_alpha
                maximum_element_index = k

            k += 1

        if i == 1:
            alphas_list[j][1] = maximum_current_alpha
            alphas_list[j][2].append(temp_list[maximum_element_index][0])

        else:
            alphas_list[j][1] = maximum_current_alpha
            alphas_list[j][2] = copy.deepcopy(alphas_list_copy[maximum_element_index][2])
            alphas_list[j][2].append(temp_list[maximum_element_index][0])

        j += 1

    j = 0
    while j < len(previous_probabilities_list):
        previous_probabilities_list[j][1] = alphas_list[j][1]
        j += 1

    i += 1

probs = []
i = 0
while i < len(alphas_list):
    probs.append(alphas_list[i][1])
    i += 1
maximum, index_of_maximum = maximum_finder(probs)
alphas_list[index_of_maximum][2].append(alphas_list[index_of_maximum][0])
output_file_generator(alphas_list[index_of_maximum][2])


















