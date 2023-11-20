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
                if output[s][0] == "" or output[s][1] == "" or output[s][2] == "":
                    if output[s][0] == "" and output[s][1] != "" and output[s][2] != "":
                        output_dictionary["9625" + output[s][1] + output[s][2]] = probabilities[s]

                    if output[s][0] != "" and output[s][1] == "" and output[s][2] != "":
                        output_dictionary[output[s][0] + "9625" + output[s][2]] = probabilities[s]

                    if output[s][0] != "" and output[s][1] != "" and output[s][2] == "":
                        output_dictionary[output[s][0] + output[s][1] + "9625"] = probabilities[s]

                    if output[s][0] == "" and output[s][1] == "" and output[s][2] != "":
                        output_dictionary["9625" + "9625" + output[s][2]] = probabilities[s]

                    if output[s][0] == "" and output[s][1] != "" and output[s][2] == "":
                        output_dictionary["9625" + output[s][1] + "9625"] = probabilities[s]

                    if output[s][0] != "" and output[s][1] == "" and output[s][2] == "":
                        output_dictionary[output[s][0] + "9625" + "9625"] = probabilities[s]

                    if output[s][0] == "" and output[s][1] == "" and output[s][2] == "":
                        output_dictionary["9625" + "9625" + "9625"] = probabilities[s]
                else:
                    output_dictionary[output[s][0] + output[s][1] + output[s][2]] = probabilities[s]

                k += 1

        i += 1

    return default_weight, output_dictionary


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

            k = 0
            while k < len(list_of_js):
                s = list_of_js[k]
                probabilities[s] = output[s][2] / down
                if output[s][0] == "" or output[s][1] == "":
                    if output[s][0] == "" and output[s][1] != "":
                        output_dictionary["9625" + output[s][1]] = probabilities[s]
                    if output[s][0] != "" and output[s][1] == "":
                        output_dictionary[output[s][0] + "9625"] = probabilities[s]
                    if output[s][0] == "" and output[s][1] == "":
                        output_dictionary["9625" + "9625"] = probabilities[s]
                else:
                    output_dictionary[output[s][0] + output[s][1]] = probabilities[s]
                k += 1
        i += 1

    return default_weight, output_dictionary


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
states_action_states_default_weight, states_action_dictionary = states_action_states_weights_file_reader()
states_observations_default_weight, states_observations_dictionary = states_observation_weights_file_reader()
observations_actions_pairs = observation_actions_file_reader()

# Viterbi algorithm is implemented here
alphas_list = []
first_state_probabilities = []
first_observation = observations_actions_pairs[0][0]
i = 0
while i < len(initial_states_and_probabilities):
    current_state = initial_states_and_probabilities[i][0]


    print("current state: " + str(current_state))
    print("first observation: " + str(first_observation))
    result = states_observations_dictionary[current_state + first_observation]
    if result != None:
        alpha = initial_states_and_probabilities[i][1] * result
    else:
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
        result = states_observations_dictionary[current_state + current_observation]
        if result != None:
            theta = result
        else:
            theta = states_observations_default_weight

        temp_list = []
        maximum_current_alpha = -1
        maximum_element_index = -1
        k = 0
        while k < len(previous_probabilities_list):
            previous_state = previous_probabilities_list[k][0]
            result = states_action_dictionary[previous_state + current_action + current_state]
            if result != None:
                action_probability = result
            else:
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


















