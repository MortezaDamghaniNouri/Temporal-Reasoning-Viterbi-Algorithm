






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


# main part of the code starts here
initial_states_and_probabilities = states_weights_file_reader()




















