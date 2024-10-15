import math
import time

# Function to read the TSP file and extract node coordinates
def read_tsp_file(filename):
    node_coordinates = {}  # Dictionary to store place names and their coordinates
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('END'):  # Stop when reaching the end of the file
                break
            if line.strip() == '' or line.startswith('Place Name'):  # Skip header and empty lines
                continue
            parts = line.strip().split()  # Split the line into components
            place_name = '_'.join(parts[:-2])  # Combine place name
            latitude = float(parts[-2])  # Get latitude
            longitude = float(parts[-1])  # Get longitude
            node_coordinates[place_name] = (latitude, longitude)  # Store coordinates in dictionary
    return node_coordinates

# Function to calculate the Haversine distance between two nodes
def calculate_distance(node1_coordinates, node2_coordinates):
    lat1, lon1 = node1_coordinates
    lat2, lon2 = node2_coordinates
    
    # Convert degrees to radians
    lat1_rad, lon1_rad = math.radians(lat1), math.radians(lon1)
    lat2_rad, lon2_rad = math.radians(lat2), math.radians(lon2)
    
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Earth radius in kilometers
    earth_radius_km = 6371.0
    return round(earth_radius_km * c)

# Function to calculate the total distance of the route
def calculate_total_route_distance(route, node_coordinates):
    total_distance = 0
    for i in range(len(route) - 1):
        total_distance += calculate_distance(node_coordinates[route[i]], node_coordinates[route[i + 1]])
    total_distance += calculate_distance(node_coordinates[route[-1]], node_coordinates[route[0]])  # Returning to the starting point
    return total_distance

# 2-opt optimization algorithm
def two_opt_optimization(route, node_coordinates):
    improvement_found = True
    while improvement_found:
        improvement_found = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue  # Skip adjacent nodes
                new_route = route[:]
                new_route[i:j] = route[j - 1:i - 1:-1]  # Reverse the section between i and j
                current_distance = calculate_total_route_distance(route, node_coordinates)
                new_route_distance = calculate_total_route_distance(new_route, node_coordinates)
                if new_route_distance < current_distance:
                    route = new_route  # Update route if the new distance is shorter
                    improvement_found = True
        if improvement_found:
            break
    return route

if __name__ == '__main__':
    # Read TSP data from the file
    node_coordinates = read_tsp_file('project_dataset.txt')
    
    # Check if nodes were successfully loaded
    if not node_coordinates:
        print("Error: No nodes found in the file.")
    else:
        # Record the start time for performance measurement
        start_time = time.time()
        
        # Generate the initial route based on the order of nodes
        initial_route = list(node_coordinates.keys())
        
        # Perform the 2-opt optimization on the initial route
        optimized_route = two_opt_optimization(initial_route, node_coordinates)
        
        # Record the end time and calculate the execution duration
        end_time = time.time()
        execution_time = end_time - start_time
        
        # Display the results
        print('Optimized route found:', optimized_route)
        print('Total distance:', calculate_total_route_distance(optimized_route, node_coordinates))
        print('Execution time:', execution_time)
