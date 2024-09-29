import math
import time

def read_places_file(filename):
    places = {}
    with open(filename, 'r') as file:
        header = file.readline()  # Read and ignore the first line (headers)
        for line in file:
            if line.startswith('END'):
                break
            columns = line.split('\t')
            if len(columns) < 3:
                continue  # Skip any malformed lines
            place_name = columns[0].strip()
            # Check if latitude and longitude are valid numbers
            try:
                latitude = float(columns[1].strip())
                longitude = float(columns[2].strip())
            except ValueError:
                continue  # Skip this line if conversion fails
            places[place_name] = (latitude, longitude)
    return places

def calculate_distance(coord1, coord2):
    # Haversine formula to calculate distance between two latitude-longitude points
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth radius in kilometers
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c  # Return distance in kilometers

def calculate_total_distance(route, places):
    total_dist = 0
    for i in range(len(route) - 1):
        total_dist += calculate_distance(places[route[i]], places[route[i + 1]])
    total_dist += calculate_distance(places[route[-1]], places[route[0]])  # Return to starting point
    return total_dist

def optimize_route(route, places):
    improved = True
    while improved:
        improved = False
        for i in range(1, len(route) - 2):
            for j in range(i + 1, len(route)):
                if j - i == 1:
                    continue
                new_route = route[:]
                new_route[i:j] = reversed(route[i:j])  # Reverse the segment
                new_distance = calculate_total_distance(new_route, places)
                if new_distance < calculate_total_distance(route, places):
                    route = new_route
                    improved = True
        if improved:
            break
    return route

if __name__ == '__main__':
    places = read_places_file('project_dataset.txt')
    start_time = time.time()
    initial_route = list(places.keys())
    best_route = optimize_route(initial_route, places)
    end_time = time.time()
    execution_time = end_time - start_time
    print('Best route found:', best_route)
    print('Total distance:', calculate_total_distance(best_route, places))
    print("Execution time:", execution_time)
