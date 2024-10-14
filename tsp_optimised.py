import math
import time
import gc

# Disable garbage collection
gc.disable()

# Function for calculating the Haversine distance between two states based on their latitude and longitude
def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    # Converting latitude and longitude from degrees to radians
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])
    # Haversine formula for calculating the great-circle distance
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(6371.0 * c)  # Earth's radius in kilometers

# Function for calculating distance between two states using Haversine formula
def calculate_state_distance(state1, state2, state_coordinates):
    lat1, lon1 = state_coordinates[state1]  # Getting latitude and longitude of state1 from the dictionary
    lat2, lon2 = state_coordinates[state2]  # Getting latitude and longitude of state2 from the dictionary
    return calculate_haversine_distance(lat1, lon1, lat2, lon2)

# Function for finding nearest neighbor of a state
def find_nearest_state(state, state_coordinates, visited_states):
    min_distance = float('inf')
    nearest_state = None
    for neighbor in state_coordinates:
        if neighbor not in visited_states:
            distance = calculate_state_distance(state, neighbor, state_coordinates)
            if distance < min_distance:
                min_distance = distance
                nearest_state = neighbor
    return nearest_state

# Function for solving TSP problem using the Nearest Neighbor Algorithm
def solve_tsp_problem(state_coordinates):
    visited_states = [list(state_coordinates.keys())[0]]  # Start from the first state (arbitrary choice)
    total_distance = 0
    current_state = visited_states[0]

    while len(visited_states) < len(state_coordinates):
        nearest_state = find_nearest_state(current_state, state_coordinates, visited_states)
        total_distance += calculate_state_distance(current_state, nearest_state, state_coordinates)
        visited_states.append(nearest_state)
        current_state = nearest_state

    # Adding  distance from the last state back to the starting state
    total_distance += calculate_state_distance(current_state, visited_states[0], state_coordinates)
    return visited_states, total_distance

# Function for reading dataset
def read_state_data(filename):
    state_coordinates = {}
    with open(filename, 'r') as f:
        next(f)  # Skipping header
        for line in f:
            if line.startswith('END'):
                break
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            state_name = ' '.join(parts[:-2]).strip().lower()      # Lowercase for uniformity
            try:
                latitude = float(parts[-2].strip())
                longitude = float(parts[-1].strip())
            except ValueError:
                continue  # Skipping invalid lines
            state_coordinates[state_name] = (latitude, longitude)  # Dictionary with state names and coordinates
    return state_coordinates
# 2-opt swap to improve the tour
def two_opt(tour, state_coordinates):
    best_tour = tour[:]
    best_distance = calculate_tour_distance(best_tour, state_coordinates)
    improved = True
    
    while improved:
        improved = False
        for i in range(1, len(tour) - 1):
            for j in range(i + 1, len(tour)):
                if j - i == 1:  # Skip adjacent nodes, no point in swapping them
                    continue
                new_tour = best_tour[:]
                # Reverse the segment between i and j to create a new tour
                new_tour[i:j] = best_tour[j-1:i-1:-1]
                
                new_distance = calculate_tour_distance(new_tour, state_coordinates)
                if new_distance < best_distance:
                    best_tour = new_tour
                    best_distance = new_distance
                    improved = True
    return best_tour, best_distance

# Helper function to calculate the total distance of a tour
def calculate_tour_distance(tour, state_coordinates):
    total_distance = 0
    for i in range(len(tour) - 1):
        total_distance += calculate_state_distance(tour[i], tour[i+1], state_coordinates)
    total_distance += calculate_state_distance(tour[-1], tour[0], state_coordinates) 
    # Return to the starting point
    return total_distance

# Function for reading dataset
def read_state_data(filename):
    state_coordinates = {}
    with open(filename, 'r') as f:
        next(f)  # Skipping header
        for line in f:
            if line.startswith('END'):
                break
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            state_name = ' '.join(parts[:-2]).strip().lower()      # Lowercase for uniformity
            try:
                latitude = float(parts[-2].strip())
                longitude = float(parts[-1].strip())
            except ValueError:
                continue  # Skipping invalid lines
            state_coordinates[state_name] = (latitude, longitude)  # Dictionary with state names and coordinates
    return state_coordinates

# Reading dataset
state_coordinates = read_state_data('project_dataset.txt')

# Solving TSP problem using the Nearest Neighbor Algorithm
start_time = time.time()
initial_tour, initial_cost = solve_tsp_problem(state_coordinates)
print('Initial Tour (Nearest Neighbor):', initial_tour)
print('Initial Total Distance:', initial_cost)

# Applying 2-opt optimization to improve the tour
optimized_tour, optimized_cost = two_opt(initial_tour, state_coordinates)
end_time = time.time()

# Printing optimized tour and total distance
print('Optimized Tour (2-opt):', optimized_tour)
print('Optimized Total Distance:', optimized_cost)
print("Execution time:", end_time - start_time)
