#This module controls the motion of the Stepper Motor 
#Dominik Donocik October 2013


import spdriver
import math

#initialise instance of drive
driver= spdriver.Driver()


#driver.step_motor(0, 0, 200,1)

#driver.step_motor(1, 0, 400,1)

#driver.step_motor(0, 1, 400,1)

#driver.step_motor(1, 1, 200,1)

#print(driver.number_steps_right)
#print(driver.number_steps_left)

#print(driver.number_steps(0))
#print(driver.number_steps(1))


class Motion:
	def __init__(self):
		#all measurements in mm
		#this applies to small spider plotter large one stepspermm is 150
		##########################
		self.step_resolution=200
		self.pulley_pitch_diameter=20.7
		self.steps_per_mm=self.step_resolution/(math.pi*self.pulley_pitch_diameter)
		
		#steps_per_mm=150
		
		self.building_width=1000

		#define printable area

		self.canvas_width=500
		self.canvas_height=1000
		self.motor_ofset_y=500
		self.motor_ofset_x=(self.building_width-self.canvas_width)/2


		#input starting position
		self.starting_belt_length_right=100
		self.starting_belt_length_left=100

		self.columns_i=100
		self.rows_j=200

		self.pixel_width=self.canvas_width/self.columns_i
		self.pixel_height=self.canvas_height/self.rows_j
		####################


		self.current_i=0
		self.current_j=0
	

	def ij_to_xy (self, i, j):
		#convert i j (pixel coordinates) to x,y (mm coordinates relative to top left corner of building)
		return(self.motor_ofset_x+(i*self.pixel_width)+(self.pixel_width/2),self.motor_ofset_y+(j*self.pixel_height)+(self.pixel_height/2))


	def xy_to_ab(self, x, y):
		#return belt lengths in mm
		return(math.sqrt(x**2+y**2), math.sqrt((self.building_width-x)**2+y**2))

	def ab_to_AB(self, a, b):
		return(a*self.steps_per_mm, b*self.steps_per_mm)


	def ij_to_AB (self, i, j):
		#pixel coordinates to belt steps !!! not mm!!!
		x , y = self.ij_to_xy(i,j)
		a , b = self.xy_to_ab(x, y)
		A , B = self.ab_to_AB(a,b)

		#note adding round function which is neccesary to derive steps but is no longer true i,j position
		return(round(A), round(B))
		
		#return (self.ab_to_AB(self.xy_to_ab(self.ij_to_xy(i, j))))
	
		
	def AB_to_ab(self, A, B):
		#note: going in reverse from AB to ij will cause problems due to rounding, always use i, j as base and only AB once for calibration
		#note to avoid rounding error we need to move to closest i, j
		return(A/self.steps_per_mm, B/self.steps_per_mm)


	def ab_to_xy (self, a, b):
		#belt lengths in mm to x,y coordinates 
		#difficult to work out, in progress
		#x=
		#y=
		
		pass

	def xy_to_ij (self, x, y):
		#convert x, y (mm coordinates) to i, j (pixel coordinates)
		#also difficult to work out
		pass

	def move_delta(self, delta_A, delta_B):
		#simplest move difference method (can optimise this with threads)

		if delta_A>=0:
			direction=0
		else:
			direction=1
			pass

		steps=int(abs(delta_A))
		
		driver.step_motor(0, direction, steps,1)

		if delta_B>=0:
			direction=0
		else:
			direction=1

		steps=int(abs(delta_B))
		driver.step_motor(1, direction, steps,1)

	def move_to_ij(self, i, j):
		#move relative to top left corner of canvas in pixel count (i,j)
		
		print(i,j)
		current_A, current_B = self.ij_to_AB(self.current_i, self.current_j)
		A, B = self.ij_to_AB(i, j)
		print(current_A, current_B)
		print(A,B)
		delta_A=current_A-A
		delta_B=current_B-B
		print(delta_A, delta_B)
		self.move_delta(delta_A, delta_B)

		self.current_ij= (i, j)
		

	def move_to_xy (self, x, y):
		#dangerous method, wrong values could damage motors!!!
		#method to move relative to top left corner of BUILDING in mm
		#can only move to closest possible x and y
		pass


	

motion=Motion()
#print(motion.ij_to_xy(0,0))
#print(motion.ij_to_AB(0,0))
motion.move_to_ij(1,1)

for m in range(10):
	motion.move_to_ij(0,m)
#for m in range(20):
	#motion.move_to_ij(m,20)
#for m in range(20):
	#motion.move_to_ij(20,20-m)
#for m in range(20):
	#motion.move_to_ij(20-m,0)

