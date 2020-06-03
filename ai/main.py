import os
import pygame
from math import sin, radians, degrees, copysign
from pygame.math import Vector2


class Car:
	def __init__(self, x, y, car_image, angle=180.0, length=4, max_steering=30, max_acceleration=70.0):
		self.position = Vector2(x, y)
		self.velocity = Vector2(0.0, 0.0)
		self.angle = angle
		self.length = length
		self.max_acceleration = max_acceleration
		self.max_steering = max_steering
		self.max_velocity = 20
		self.brake_deceleration = 10
		self.free_deceleration = 2
		self.image = car_image
		self.orig_image = car_image
		self.rect = self.image.get_rect(center=(x, y))

		self.acceleration = 0.0
		self.steering = 0.0

		self.mask = pygame.mask.from_surface(self.image, 50)

	def update(self, dt):
		self.velocity += (self.acceleration * dt, 0)
		angular_velocity = self.steering * 0.01 * dt * self.velocity.x
		self.position += self.velocity.rotate(-self.angle) * dt
		self.rect.center = self.position  # Update the rect each frame.
		self.angle += degrees(angular_velocity) * dt
		self.angle += degrees(angular_velocity) * dt
		self.image = pygame.transform.rotate(self.orig_image, self.angle)
		self.rect = self.image.get_rect(center=self.rect.center)
		self.mask = pygame.mask.from_surface(self.image, 50)


class Game:
	def __init__(self):
		pygame.init()
		pygame.display.set_caption("Car tutorial")
		width = 1700
		height = 800
		self.screen = pygame.display.set_mode((width, height))
		self.clock = pygame.time.Clock()
		self.ticks = 60
		self.exit = False

	def run(self):
		current_dir = os.path.dirname(os.path.abspath(__file__))
		car_image = pygame.transform.scale(pygame.image.load(os.path.join(current_dir, "car.png")).convert_alpha(), (40, 20))
		tracks_img = pygame.transform.scale(pygame.image.load(os.path.join("./","tracks1.png")).convert_alpha(), (1700, 800))
		car = Car(850, 700, car_image)
		back_mask = pygame.mask.from_surface(tracks_img, 50)
		back_rect = tracks_img.get_rect()
		ppu = 10

		while not self.exit:
			dt = self.clock.get_time() / 1000

			# Event queue
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					self.exit = True

			# User input
			pressed = pygame.key.get_pressed()

			if pressed[pygame.K_UP]:
				car.acceleration += 100 * dt
			elif pressed[pygame.K_DOWN]:
				if car.velocity.x > 0:
					car.acceleration = -car.brake_deceleration * 40
				else:
					car.acceleration -= 1.5 * dt
			elif pressed[pygame.K_SPACE]:
				if abs(car.velocity.x) > dt * car.brake_deceleration:
					car.acceleration = -copysign(car.brake_deceleration, car.velocity.x)
				else:
					car.acceleration = -car.velocity.x / dt
			else:
				if abs(car.velocity.x) > dt * car.free_deceleration:
					car.acceleration = -copysign(car.free_deceleration, car.velocity.x) * 40
				else:
					if dt != 0:
						car.acceleration = -car.velocity.x / dt
			car.acceleration = max(-car.max_acceleration, min(car.acceleration, car.max_acceleration))

			if pressed[pygame.K_RIGHT]:
				car.steering -= 30 * dt
			elif pressed[pygame.K_LEFT]:
				car.steering += 30 * dt
			else:
				car.steering = 0
			car.steering = max(-car.max_steering, min(car.steering, car.max_steering))

			# Logic
			car.update(dt)

			#Calculate offset
			offset_x = car.rect[0] - back_rect[0]
			offset_y = car.rect[1] - back_rect[1]

			#Check for overlap
			overlap = back_mask.overlap(car.mask, (offset_x, offset_y))
			print(car.acceleration)

			# Drawing
			self.screen.fill((255, 255, 255))
			self.screen.blit(tracks_img,(0, 0))
			self.screen.blit(car.image, car.rect)

			for point in car.mask.outline(8):
				pygame.draw.rect(self.screen, (255, 0, 0), (point+Vector2(car.rect.topleft), (2, 2)))
			

			if overlap:
				print('salut')
			if not overlap:
				print('ok')
			pygame.display.flip()

			self.clock.tick(self.ticks)
		pygame.quit()


if __name__ == '__main__':
	game = Game()
	game.run()