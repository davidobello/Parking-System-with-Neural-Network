from settings import *
from population import Population



def train():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulated Parking Sensor")
    clock = pygame.time.Clock()

    population = Population(100)

    start_time = pygame.time.get_ticks()
    speed_up = False

    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    speed_up = not speed_up

        dt = clock.tick(30) / 1000

        for obs in obstacles:
            pygame.draw.rect(screen, BLUE, obs)
        for spot in PARKING_SPOTS:
            pygame.draw.rect(screen, GREEN, spot)

        if speed_up:
            for i in range(20):
                for car in population.population:
                    car.update(dt)

                    if car.game_over:
                        population.save_one(car)

        else:
            for car in population.population:
                car.update(dt)

                if car.game_over:
                    population.save_one(car)

        for car in population.population:
            car.draw(screen)

        if pygame.time.get_ticks() - start_time > 5000:
            population.save_all()

        if len(population.population) == 0:
            population.calculate_fitness()
            print(f'current generation: {population.current_generation}\n'
                  f'best fitness: {population.best_fitness}\n'
                  f'best fitness distance: {population.best_fitness_distance}\n'
                  f'best fitness angle: {population.best_fitness_angle}\n')
            population.reproduction()

            start_time = pygame.time.get_ticks()

        pygame.display.flip()

    pygame.quit()


def test():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulated Parking Sensor")
    clock = pygame.time.Clock()

    population = Population(1, 'saved_data2.npz')

    start_time = pygame.time.get_ticks()
    speed_up = False

    running = True

    while running:
        screen.fill(WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    speed_up = not speed_up

        dt = clock.tick(30) / 1000

        for obs in obstacles:
            pygame.draw.rect(screen, BLUE, obs)
        for spot in PARKING_SPOTS:
            pygame.draw.rect(screen, GREEN, spot)

        for car in population.population:
            car.update(dt)
            car.draw(screen)

        pygame.display.flip()

    pygame.quit()

train()