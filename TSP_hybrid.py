import math
import time
import gc
from functools import lru_cache

# Disable garbage collection to optimize performance in recursive functions
gc.disable()

# Function for calculating the Haversine distance between two states based on their latitude and longitude
def calculate_haversine_distance(lat1, lon1, lat2, lon2):
    # Converting latitude and longitude from degrees to radians
    lat1_rad, lon1_rad, lat2_rad, lon2_rad = map(math.radians, [lat1, lon1, lat2, lon2])
    # Haversine formula for calculating the great-circle distance
    lat_dis = lat2_rad - lat1_rad
    lon_dis = lon2_rad - lon1_rad
    a = math.sin(lat_dis / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(lon_dis / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(6371.0 * c)  # Earth's radius in kilometers

# Function for calculating distance between two states using Haversine formula
def calculate_state_distance(state1, state2, state_coordinates):
    lat1, lon1 = state_coordinates[state1]  # Getting latitude and longitude of state1 from the dictionary
    lat2, lon2 = state_coordinates[state2]  # Getting latitude and longitude of state2 from the dictionary
    return calculate_haversine_distance(lat1, lon1, lat2, lon2)


# Function for solving TSP within a region using Dynamic Programming (Held-Karp algorithm)
def tsp_dp(region_coordinates):
    cities = list(region_coordinates.keys())  # city names list
    n = len(cities)                           # Number of cities
    dist = [[0] * n for _ in range(n)]        # Distance matrix for cities
    # Precompute distances between all pairs of cities in this region
    for i in range(n):
        for j in range(n):
            dist[i][j] = calculate_state_distance(cities[i], cities[j], region_coordinates)
    @lru_cache(None)                          # storing results and avoid redundant calculations

    def dp(mask, pos):
        # If all cities are visited, return to the starting city
        if mask == (1 << n) - 1:
            return dist[pos][0], [cities[pos], cities[0]]
        min_dist = float('inf')
        min_path = []
        # Visiting each unvisited city to find the optimal path
        for next_pos in range(n):
            if not mask & (1 << next_pos):
                new_dist, path = dp(mask | (1 << next_pos), next_pos)
                new_dist += dist[pos][next_pos]

                if new_dist < min_dist:
                    min_dist = new_dist
                    min_path = [cities[pos]] + path
        return min_dist, min_path
    min_distance, tour = dp(1, 0)
    return min_distance, tour

# Function for dividing cities into geographic regions based on latitude
def divide_regions(state_coordinates, num_regions=10):
    latitudes = [coords[0] for coords in state_coordinates.values()]
    min_lat, max_lat = min(latitudes), max(latitudes)
    region_step = (max_lat - min_lat) / num_regions
    regions = {i: {} for i in range(num_regions)}          # Initializing regions dictionary
    for state, (lat, lon) in state_coordinates.items():
        # Determining region index based on latitude
        region_index = int((lat - min_lat) // region_step)
        region_index = min(region_index, num_regions - 1)  # Handling boundary cases
        regions[region_index][state] = (lat, lon)          # Assigning city to its region
    return regions

# Main function for solving TSP by combining regional solutions
def solve_tsp_by_regions(state_coordinates, num_regions=10):
    regions = divide_regions(state_coordinates, num_regions)  # Dividing cities into regions
    total_tour = []
    total_distance = 0
    region_centroids = {}
    region_tours = {}
    # Solving TSP within each region
    for region_id, region_states in regions.items():
        if region_states:
            distance, tour = tsp_dp(region_states)
            total_distance += distance
            region_tours[region_id] = tour
            region_centroids[region_id] = calculate_region_centroid(region_states)
    # Connecting regions by treating centroids as points using Nearest Neighbor heuristic
    if region_centroids:
        centroid_tour, connecting_distance = solve_tsp_nn(region_centroids)
        total_distance += connecting_distance
        visited_states = set()                 # Tracking cities that have been added to avoid duplicates
        for idx in centroid_tour:
            for city in region_tours[idx]:     # Going through each region in ordered centroid tour
                if city not in visited_states:
                    total_tour.append(city)
                    visited_states.add(city)
    return total_tour, total_distance

# Function for calculating the centroid (average coordinates) of a region
def calculate_region_centroid(region_states):
    if not region_states:
        return (0, 0)
    latitudes = [coords[0] for coords in region_states.values()]
    longitudes = [coords[1] for coords in region_states.values()]
    return (sum(latitudes) / len(latitudes), sum(longitudes) / len(longitudes)) # Calculating average latitude and longitude

# Function for solving TSP for region centroids using Nearest Neighbor heuristic
def solve_tsp_nn(region_centroids):
    visited_states = [list(region_centroids.keys())[0]]
    total_distance = 0
    current_state = visited_states[0]
    # Connecting centroids using the Nearest Neighbor heuristic
    while len(visited_states) < len(region_centroids):
        nearest_state = find_nearest_state(current_state, region_centroids, visited_states)
        total_distance += calculate_state_distance(current_state, nearest_state, region_centroids)
        visited_states.append(nearest_state)
        current_state = nearest_state
    total_distance += calculate_state_distance(current_state, visited_states[0], region_centroids)
    return visited_states, total_distance

# Function for finding nearest unvisited state
def find_nearest_state(state, state_coordinates, visited_states):
    min_distance = float('inf')
    nearest_state = None
    # Find the closest unvisited state
    for neighbor in state_coordinates:
        if neighbor not in visited_states:
            distance = calculate_state_distance(state, neighbor, state_coordinates)
            if distance < min_distance:
                min_distance = distance
                nearest_state = neighbor
    return nearest_state

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
state_coordinates = read_state_data('/content/project_dataset.txt')
num_regions = 10  # Adjusting based on dataset size

# Solving TSP problem using Dynamic programming and  Nearest Neighbor Algorithm
start_time = time.time()
tour, cost = solve_tsp_by_regions(state_coordinates, num_regions)
end_time = time.time()

# Printing optimal tour and total distance
print('Optimal Tour:', tour)
print('Total Distance:', cost)
print("Execution time:", end_time - start_time)
