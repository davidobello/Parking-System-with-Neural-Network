from car import Car
from settings import *
import random


class Population:
    def __init__(self, size, saved_data_path=None):
        self.size = size
        self.population = []
        self.saved_population = []
        self.saved_data_path = saved_data_path

        self.current_generation = 0
        self.best_fitness = 0
        self.best_fitness_distance = 0
        self.best_fitness_angle = 0

        for i in range(self.size):
            self.population.append(Car(self.saved_data_path))

    def save_one(self, car):
        self.saved_population.append(car)
        self.population.remove(car)

    def save_all(self):
        for car in self.population:
            self.saved_population.append(car)

        self.population = []

    def calculate_fitness(self):
        target_angle = 90.0
        max_distance = 10.0
        max_angle_dev = 90.0

        best_fitness = 0
        best_fitness_distance = 0
        best_fitness_angle = 0
        best_car = self.saved_population[-1]

        for car in self.saved_population:
            closest_spot, closest_distance = car.get_closest_spot()
            angle_deviation = abs(car.angle - target_angle)

            distance_score = 1 - min(closest_distance / max_distance, 1) ** 2
            angle_score = 1 - min(angle_deviation / max_angle_dev, 1) ** 2

            if car.game_over:
                fitness = 0
            else:
                fitness = 0.5 * distance_score + 0.5 * angle_score

            car.fitness = fitness

            if fitness > best_fitness:
                best_fitness = fitness
                best_fitness_distance = closest_distance
                best_fitness_angle = car.angle
                best_car = car

        self.best_fitness = best_fitness
        self.best_fitness_distance = best_fitness_distance
        self.best_fitness_angle = best_fitness_angle
        best_car.brain.save_data()

    def select_car(self):
        fitness_values = [car.fitness for car in self.saved_population]
        total_fitness = sum(fitness_values)
        if total_fitness == 0:
            return random.choice(self.saved_population)  # Avoid division by zero, pick randomly

        probabilities = [f / total_fitness for f in fitness_values]
        return random.choices(self.saved_population, weights=probabilities, k=1)[0]

    def tournament_selection(self):
        fitness_values = [car.fitness for car in self.saved_population]
        selected = random.sample(list(zip(self.population, fitness_values)), self.size)
        return max(selected, key=lambda x: x[1])[0]  # Return car with the highest fitness

    def reproduction(self):
        new_population = []

        for i in range(self.size):
            parent1 = self.select_car()
            parent2 = self.select_car()

            crossed_brain = parent1.brain.crossover(parent2.brain)

            new_child = Car()
            new_child.brain = crossed_brain

            new_child.brain.mutate()

            new_population.append(new_child)

        self.population = new_population.copy()
        self.saved_population = []

        self.current_generation += 1

        # print('REPRODUCTION')