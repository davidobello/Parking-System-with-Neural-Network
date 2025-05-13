from settings import *
import pygame
from NeuralNetwork import NeuralNetwork
from functions import *
import numpy as np
import random


class Car:
    def __init__(self, saved_data_path=None):
        self.width = 50
        self.height = 30
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.angle = 0
        self.color = BLACK
        self.brain = NeuralNetwork(5, 16, 6, saved_data_path)
        self.fitness = 0
        self.game_over = False
        self.can_rotate = False
        self.image = pygame.image.load('car.png.jpg')
        self.image = pygame.transform.rotate(self.image,90)
        self.image2 = self.image
        self.beep = pygame.mixer.Sound('beep.wav')

        self.surface = pygame.Surface((self.width, self.height))
        self.surface = pygame.Surface((self.width, self.height))
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (self.x, self.y)
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))
        self.image_rect = pygame.Rect(self.rect.x, self.rect.y, self.rect.width, self.rect.height)

    def draw_line(self, screen, closest_spot):
        pygame.draw.line(screen, (255, 0, 0), self.rect.center, closest_spot.center)

    def think(self, dt):
        closest_spot, closest_distance = self.get_closest_spot()

        if closest_distance < 50:
            self.can_rotate = True
        if 80 < self.angle < 90:
            self.can_rotate = False

        inputs = np.array([
            self.rect.centerx / WIDTH,
            self.rect.centery / HEIGHT,
            closest_spot.centerx / WIDTH,
            closest_spot.centery / HEIGHT,
            self.angle / 360
        ])
        output = self.brain.forward(inputs)

        if np.argmax(output) == 0:
            self.rect.y -= 2
        elif np.argmax(output) == 1:
            self.rect.y += 2
        elif np.argmax(output) == 2:
            self.rect.x -= 2
        elif np.argmax(output) == 3:
            self.rect.x += 2

        if self.can_rotate:
            if np.argmax(output) == 4:
                self.angle += 90 * dt
            elif np.argmax(output) == 5:
                self.angle -= 90 * dt

    def get_closest_spot(self):
        closest_spot, closest_distance = get_closest_parking_space(self, PARKING_SPOTS)

        return closest_spot, closest_distance

    def collision_check(self):
        self.screen_bound()
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                self.game_over = True

    def screen_bound(self):
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.game_over = True

    def rotate(self):
        rotated_rect = pygame.transform.rotate(self.surface, -self.angle)
        rotated_image = pygame.transform.rotate(self.image, -self.angle)

        rotated_rect_rect = rotated_rect.get_rect()
        rotated_image_rect = rotated_image.get_rect()

        rotated_rect_rect.center = self.rect.center
        rotated_image_rect.center = self.rect.center

        self.rect = rotated_rect_rect
        self.image2 = rotated_image

        self.image_rect = rotated_image_rect

    def get_sensor_readings(self):
        """Simulates ultrasonic sensor readings"""
        sensor_positions = []
        sensor_angles = [-45, 0, 45]  # Left, Center, Right sensors
        distances = []

        """ Final sensor values in radians """
        for s_angle in sensor_angles:
            radian_angle = np.radians(self.angle + s_angle)
            end_x = self.rect.centerx - np.cos(radian_angle) * 75  # Sensor range
            end_y = self.rect.centery - np.sin(radian_angle) * 75

            """ Check if sensor detects an obstacle """
            min_distance = 50
            for obs in obstacles:
                if obs.collidepoint(end_x, end_y):
                    self.beep.play(maxtime=500)
                    min_distance = random.randint(10, 50)  # Simulated detection

            sensor_positions.append((self.rect.center, (end_x, end_y)))
            distances.append(min_distance)

        return sensor_positions, distances

    def draw(self, screen):
        self.rotate()

        pygame.draw.rect(screen, self.color, self.rect, 2)

        screen.blit(self.image2, self.image_rect)

        # closest_spot, distance = self.get_closest_spot()

        # self.draw_line(screen, closest_spot)

        sensors, distances = self.get_sensor_readings()

        for (start, end), dist in zip(sensors, distances):
            pygame.draw.line(screen, RED, start, end, 2)

    def movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_KP8]:
            self.rect.y -= 2
        if keys[pygame.K_KP2]:
            self.rect.y += 2
        if keys[pygame.K_KP4]:
            self.rect.x -= 2
        if keys[pygame.K_KP6]:
            self.rect.x += 2
        if keys[pygame.K_LEFT]:
            self.angle += 2
        if keys[pygame.K_RIGHT]:
            self.angle -= 2

    def update(self, dt):
        self.angle = round(self.angle % 360)

        self.think(dt)
        # self.movement()
        self.collision_check()
