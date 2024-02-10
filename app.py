import folium
from openrouteservice import client
from geopy.geocoders import Nominatim

# Create a client for OpenRouteService API
client = client.Client(key='5b3ce3597851110001cf6248d2c7369d8fc84bd1bd8e599b9b146da3')  # Replace 'your_api_key' with your actual API key

# Initialize a geocoder
geolocator = Nominatim(user_agent="geoapiExercises")

# Create a Folium map centered around India
india_center = [20.5937, 78.9629]  # Center coordinates of India
m = folium.Map(location=india_center, zoom_start=5)

# Global variables to store starting and destination coordinates
start_coords = None
end_coords = None

# Function to update the route on the map
def update_route(start_coords, end_coords):
    # Request directions from OpenRouteService
    route = client.directions(coordinates=[start_coords, end_coords], profile='driving-car', format='geojson')
    # Extract the coordinates from the route
    route_coords = route['features'][0]['geometry']['coordinates']
    # Reverse the coordinates (since Folium expects [latitude, longitude])
    route_coords = [list(reversed(coord)) for coord in route_coords]
    # Clear previous route if exists
    if 'route_layer' in globals():
        m.remove_layer(route_layer)
    # Add the route as a PolyLine to the map
    route_layer = folium.PolyLine(locations=route_coords, color="blue")
    route_layer.add_to(m)

# Function to get coordinates from address
def get_coordinates(address):
    location = geolocator.geocode(address)
    if location:
        return [location.longitude, location.latitude]
    else:
        print("Address not found!")
        return None

# Get start and end addresses from the user
start_address = input("Enter the start address: ")
end_address = input("Enter the end address: ")

# Get coordinates for start and end addresses
start_coords = get_coordinates(start_address)mum
end_coords = get_coordinates(end_address)

# Check if coordinates are obtained successfully
if start_coords and end_coords:
    # Update the route on the map
    update_route(start_coords, end_coords)
    # Display the map
    m.save('route_map.html')
    print("Route displayed on map!")
else:
    print("Failed to obtain coordinates. Please check the addresses.")
