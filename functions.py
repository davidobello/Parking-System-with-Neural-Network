import math


def get_closest_parking_space(car, parking_spots):
    closest_spot = None
    closest_distance = math.inf
    for spot in parking_spots:
        distance = math.hypot(spot.centerx - car.rect.centerx, spot.centery - car.rect.centery)
        if distance < closest_distance:
            closest_distance = distance
            closest_spot = spot

    return closest_spot, closest_distance
