import math
import itertools
import time

def read_state_data(filename):
    state_coordinates = {}
    with open(filename, 'r') as f:
        next(f)  # Skip header
        for line in f:
            if line.startswith('END'):
                break
            parts = line.strip().split()
            if len(parts) < 3:
                continue
            state_name = '_'.join(parts[:-2]).strip()
            try:
                latitude = float(parts[-2].strip())
                longitude = float(parts[-1].strip())
            except ValueError:
                continue
            state_coordinates[state_name] = (latitude, longitude)
    return state_coordinates

def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    R = 6371  # Earth's radius in kilometers
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return round(R * c)

def calculate_route_distance(route, state_coordinates):
    total_distance = 0
    for i in range(len(route)):
        state1 = route[i]
        state2 = route[(i + 1) % len(route)]
        lat1, lon1 = state_coordinates[state1]
        lat2, lon2 = state_coordinates[state2]
        total_distance += calculate_haversine_distance(lat1, lon1, lat2, lon2)
    return total_distance

def solve_tsp_exhaustive(state_coordinates):
    states = list(state_coordinates.keys())
    shortest_route = None
    shortest_distance = float('inf')

    for route in itertools.permutations(states):
        distance = calculate_route_distance(route, state_coordinates)
        if distance < shortest_distance:
            shortest_distance = distance
            shortest_route = route

    return shortest_route, shortest_distance

if __name__ == "__main__":
    state_coordinates = read_state_data('project_dataset.txt')
    
    # Limit the number of cities for feasible computation
    num_cities = 10  # Adjust this number based on your computational capacity
    limited_state_coordinates = dict(list(state_coordinates.items())[:num_cities])

    start_time = time.time()
    optimal_route, optimal_distance = solve_tsp_exhaustive(limited_state_coordinates)
    end_time = time.time()

    print(f"Optimal Route for {num_cities} cities:", optimal_route)
    print("Total Distance:", optimal_distance, "km")
    print("Execution Time:", end_time - start_time, "seconds")