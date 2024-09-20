import pandas as pd
import csv
import math
import ast

data = pd.read_csv('json1.csv')

true_labels = [] # List to store the true labels
# Open the text file to read true labels
with open('manually_labeled_events.txt', 'r') as file:
    # Iterate through each line in the file
    for line in file:
        true_labels.extend(line.strip())

# Extract ball and player positions
ball_and_players = data.values
num_players = 10
team_size = num_players // 2

def calculate_distance_player(player_pos1, player_pos2):
    x1, y1 = player_pos1
    x2, y2 = player_pos2
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

def calculate_distance_ball(player_pos, ball_pos):
    x1, y1 = player_pos
    x2, y2 = ball_pos
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    return distance

# Split the timesteps into windows of 10 or less timesteps
def split_into_windows(data):
    window_size = 10
    windows = []
    for i in range(0, len(data), window_size):
        windows.append(data[i:i+window_size])
    return windows

# Function to check if assignments have changed between timesteps
def assignments_changed(prev_assignments, current_assignments):
    return prev_assignments != current_assignments

# Group the data by the event label
grouped_data = data.groupby('eventid')

# Split data into windows
#windows = split_into_windows(data)
window_labels = []  # List to store the window label
event_labels = [] # List to store the event label
event_true_labels = []


all_timesteps = 0
event_counter = 0
percentage_labels = []
percentage_true_labels = []

for eventid, group in grouped_data:
    attacking_team = []  # List to store attacking team for each time step within the event
    defending_team = []  # List to store defending team for each time step within the event
    event_timestep = 0 # variable to store the event's timestep number
    event_label = 0

    # Analyze the first 10 time steps within the current event
    for _, row in group.head(30).iterrows():  # Analyze the first 10 time steps within the event
        player_distances = []
        ball_pos_str = row['ball poss']  # Extract ball position string for the current time step
        ball_pos = ast.literal_eval(ball_pos_str)

        for player_id in range(num_players):
            player_pos_str = row[f'player{player_id + 1}']  # Extract player position
            player_pos = ast.literal_eval(player_pos_str)
            distance = calculate_distance_ball(player_pos, ball_pos)
            player_distances.append(distance)

        closest_player_id = player_distances.index(min(player_distances))  # Get the index of the closest player
        if closest_player_id < team_size:
            attacking_team.append("Team A")
            defending_team.append("Team B")
        else:
            attacking_team.append("Team B")
            defending_team.append("Team A")
    # Determine the defending team for this event
    team_a_count = defending_team.count("Team A")
    team_b_count = defending_team.count("Team B")

    defending_team_label = None
    if team_a_count > team_b_count:
        defending_team_label = "Team A"
    else:
        defending_team_label = "Team B"

    if defending_team_label == "Team A":
        attacking_team_label = "Team B"
    else:
        attacking_team_label = "Team A"


    # Determine the defending and the attacking players
    defending_players = []
    attacking_players = []
    for i in range(team_size):
        if defending_team_label == "Team A":
            defending_players.append(f'player{i + 1}')
        else:
            defending_players.append(f'player{i + 6}')
        if attacking_team_label == "Team A":
            attacking_players.append(f'player{i + 1}')
        else:
            attacking_players.append(f'player{i + 6}')


    print(f"Event {eventid}:")
    

    # Split group into windows
    windows_group = split_into_windows(group)


    # Iterate over windows of 10 or less timesteps
    for window_num, window_data in enumerate(windows_group):
        prev_assignments = None  # Store assignments of the previous timestep
        ball_positions = []  # List to store ball positions within the window

        # Calculate all the distances of the players between them, for every timestep of this window
        distances = []
        for _, row in window_data.iterrows():
            defending_positions = [row[defender] for defender in defending_players]
            attacking_positions = [row[attacker] for attacker in attacking_players]
            defending_distances = []


            for defender_pos in defending_positions:
                defender_pos_ast = ast.literal_eval(defender_pos)
                distances_to_defender = []
                for attacker_pos in attacking_positions:
                    attacker_pos_ast = ast.literal_eval(attacker_pos)
                    distance = calculate_distance_player(defender_pos_ast, attacker_pos_ast)
                    distances_to_defender.append(distance)
                defending_distances.append(distances_to_defender)

            distances.append(defending_distances)

            # Store ball position for this row
            ball_pos_str_win = row['ball poss']
            ball_pos_win = ast.literal_eval(ball_pos_str_win)
            ball_positions.append(ball_pos_win)

        #assigned_defenders_window = {}  # List to store assigned defenders for each attacker at each window
        windows10_label = 0
        for timestep, distances_by_timestep in enumerate(distances):
            assigned_defenders = {}  # List to store assigned defenders for each attacker at each timestep
            event_timestep += 1
            all_timesteps += 1


            # Create a list of defender probabilities for each attacker
            defender_probabilities = []
            for attacker_id, attacker in enumerate(attacking_players):
                attacker_probabilities = []
                for defender_id, defender in enumerate(defending_players):
                    distance_to_attacker = distances_by_timestep[defender_id][attacker_id]
                    total_distances_to_attackers = sum(distances_by_timestep[defender_id])
                    probability = 100 * (1 - (distance_to_attacker / total_distances_to_attackers))
                    attacker_probabilities.append((defender, probability))
                defender_probabilities.append(attacker_probabilities)


            
            # Calculate the average distance between players for the current timestep
            #average_player_distance = sum(distances_by_timestep[defender_id][attacker_id] for defender_id in range(len(defending_players)) for attacker_id in range(len(attacking_players))) / (len(defending_players) * len(attacking_players))
            # Check if the average player distance is above the threshold
            #print("average_player_distance: ", average_player_distance)




            # Iterate over attackers and find the best defender assignment
            for _ in range(len(attacking_players)):
                max_probability = -1
                max_attacker = None
                max_defender = None
                
                for attacker_id, attacker in enumerate(attacking_players):
                    if attacker not in assigned_defenders:
                        attacker_probabilities = defender_probabilities[attacker_id]
                        for defender, probability in attacker_probabilities:
                            if defender not in assigned_defenders.values() and probability > max_probability:
                                max_probability = probability
                                max_attacker = attacker
                                max_defender = defender

                if max_attacker is not None:
                    assigned_defenders[max_attacker] = max_defender




            ball_position = ball_positions[timestep] # ball position at each timestep


            # Define a threshold for probability change
            probability_threshold = 4.7  # Adjust this value as needed
            # Define a threshold for average player distance below and over which you won't check assignment changes
            min_distance_threshold = 17.0  
            max_distance_threshold = 27.0

            # Check if assignments have changed
            if prev_assignments is not None and assignments_changed(prev_assignments, assigned_defenders):
                if event_timestep > 50:

                    # Calculate the average distance between players for the current timestep
                    average_player_distance = sum(distances_by_timestep[defender_id][attacker_id] for defender_id in range(len(defending_players)) for attacker_id in range(len(attacking_players))) / (len(defending_players) * len(attacking_players))
                    # Check if the average player distance is above and below the thresholds
                    if average_player_distance > min_distance_threshold and average_player_distance < max_distance_threshold:



                        # Check if the change involves an attacker with the ball
                        ball_defender_changed = False
                        ball_holder_attacker = None  # Define it here

                        for attacker, defender in assigned_defenders.items():
                            if prev_assignments.get(attacker) != defender:
                                attacker_id = attacking_players.index(attacker)
                                #ball_distance = distances_by_timestep[defending_players.index(defender)][attacker_id]
                                ball_distance_from_attacker = calculate_distance_ball(ast.literal_eval(attacking_positions[attacker_id]), ball_position)
                                if ball_distance_from_attacker < 1.0:
                                    ball_defender_changed = True
                                    ball_holder_attacker = attacker
                                    break

                        # Check if the change remains consistent throughout the window
                        if ball_holder_attacker is not None:
                            change_remained = True
                            for win_timestep, win_distances in enumerate(distances):
                                win_assigned_defenders = {}  # Assigned defenders for this timestep in the window
                                for attacker_id, attacker in enumerate(attacking_players):
                                    attacker_probabilities = defender_probabilities[attacker_id]
                                    defender = None
                                    max_probability = -1
                                    for defender, probability in attacker_probabilities:
                                        if defender not in win_assigned_defenders.values() and probability > max_probability:
                                            max_probability = probability
                                            max_defender = defender
                                    win_assigned_defenders[attacker] = max_defender

                                #if ball_holder_attacker is None:
                                #    ball_holder_attacker = [attacker for attacker, defender in assigned_defenders.items() if defender == assigned_defenders.get(ball_holder_attacker)][0]
                                if win_assigned_defenders.get(ball_holder_attacker) != assigned_defenders.get(ball_holder_attacker):
                                    change_remained = False
                                    break

                                # Add a check for probability change threshold
                                if change_remained and win_timestep > 0:  # Skip the first timestep
                                	for attacker_id, attacker in enumerate(attacking_players):
                                		attacker_probabilities = defender_probabilities[attacker_id]
                                		for defender, probability in attacker_probabilities:
                                			prev_probability = defender_probabilities[attacker_id][defending_players.index(prev_assignments[attacker])][1]
                                			#print("probability: ", probability, "prev_probability: ", prev_probability)
                                			if defender == assigned_defenders[attacker] and abs(probability - prev_probability) > probability_threshold:
                                				change_remained = False
                                				break

                            if change_remained:
                                window_label = 1  # Change involving ball holder, switch or trap
                            else:
                                window_label = 0  # Change in defender assignment did not remain
                        else:
                            window_label = 0  # Change without ball holder
                    else:
                        window_label = 0  # Players are clumped together, no assignment change
                else:
                    window_label = 0  # Change before timestep 50, we never see pick'n roll so quickly in an event     
            else:
                window_label = 0  # No change in assignments


            if window_label==1:
                windows10_label = 1
                print("found one on event: ", eventid,"and timestep: ", event_timestep + 1 ,"all timestep: ", all_timesteps)
            if windows10_label==1:
                event_label = 1 






            # Update previous assignments for the next timestep
            prev_assignments = assigned_defenders.copy()
        # Assign the same label to the window
        window_labels.extend([windows10_label] + [None] * (len(window_data) - 1))
    event_labels.extend([event_label] + [None] * (len(group) - 1))
    event_true_labels.extend([true_labels[event_counter]] + [None] * (len(group) - 1))

    percentage_labels.extend([event_label])
    percentage_true_labels.extend([true_labels[event_counter]])
    event_counter+=1

    


print("total events: ",event_counter)

# Initialize a counter for the matching labels
int_percentage_true_labels = [int(element) for element in percentage_true_labels]
matching_count = 0
# Iterate through the labels of both lists
for label_1, label_2 in zip(percentage_labels, int_percentage_true_labels):
    if label_1 == label_2:
        matching_count += 1
# Calculate the percentage of matching labels
percentage_matching = (matching_count / len(percentage_labels)) * 100
print(f"The percentage of matching labels is: {percentage_matching}%")

# Open a text file for writing
with open('manual_vs_automatic_labels_output.txt', 'w') as file:
    # Iterate through the elements of both lists
    for i, (num1, num2) in enumerate(zip(percentage_labels, int_percentage_true_labels), start=1):
        # Write formatted lines to the file
        file.write(f"event_{i}_label: {num1} -- event_{i}_true_label: {num2}\n")
        #file.write(f"event_{i}_true_label: {num2}\n")



# Add the window labels to your DataFrame
#data['label'] = window_labels
#data['event_labels'] = event_labels
#data['event_true_labels'] = event_true_labels

# Create a new DataFrame for window labels
#window_labels_df = pd.DataFrame({'label': window_labels})

# Merge the window labels DataFrame with the original DataFrame
#data = pd.concat([window_labels_df], ignore_index=True, axis=1)

# Save the DataFrame back to the CSV file
#data.to_csv('json1_labeled.csv', index=False)
