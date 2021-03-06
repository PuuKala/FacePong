# FacePong.py

from cv2 import destroyAllWindows
import time
import turtle
import FacePosition


# Paddle class
class Paddle:
    def __init__(self, x):
        self.paddle_ = turtle.Turtle()
        self.paddle_.speed(0)
        self.paddle_.shape("square")
        self.paddle_.color("white")
        self.paddle_.shapesize(stretch_wid=5, stretch_len=1)
        self.paddle_.penup()
        self.paddle_.goto(x, 0)

    def move(self, y_coord):
        self.paddle_.sety(y_coord)


def calibrate(faces, left):
    # Calibrate the controls for 1 player
    calibs = []
    for i in range(2):
        input("Starting calibration " + str(i+1) +
              ".\nMove to comfortable position after pressing enter.\nThe calibration will take the face position from 4 seconds after pressing enter to this message.\nPress enter to continue.")
        calibs.append([0, 0])
        start = time.time()
        end = 0
        while start+4 > end:
            detected_faces = faces.getFaces(True)
            if detected_faces:
                if left:
                    calibs[i] = min(detected_faces, key=key_first_index)
                else:
                    calibs[i] = max(detected_faces, key=key_first_index)
            end = time.time()

    destroyAllWindows()
    ret = []
    ret.append(500/(calibs[0][1]-calibs[1][1]))
    ret.append(-300-ret[0]*calibs[1][1])
    print(ret)
    # Returns the [a,b] from ay+b when first calib detection is y(min) and second is y(max)
    return ret


def key_first_index(list):
    # Super simple function to be used as min function key
    return list[0]
	
class LowPassFilter:
	prev_vals = []
	
	def filter_control(self, value):
		self.prev_vals.append(value)
		if len(self.prev_vals) > 10:
			self.prev_vals.pop(0)
		return sum(self.prev_vals)/len(self.prev_vals)


# Main "function" aka. the game
if __name__ == "__main__":
    faces = FacePosition.FacePositioning()

    # Calibrating controls
    calibration_1 = calibrate(faces, True)
    calibration_2 = calibrate(faces, False)

    # Defining the window
    window = turtle.Screen()
    window.title("FacialPong")
    window.bgcolor("black")
    window.setup(width=800, height=600)
    window.tracer(0)

    # Ball
    ball = turtle.Turtle()
    ball.speed(0)
    ball.shape("square")
    ball.color("white")
    ball.penup()
    ball.goto(0, 0)
    ball.dx = 2
    ball.dy = 2

    # The paddles, paddle class defined above in this file
    l_paddle = Paddle(-350)
    r_paddle = Paddle(350)
	
    lpf = LowPassFilter()

    # Game loop
    running = True
    while running:
        window.update()
		
		# Moving the paddles
        detected_faces = faces.getFaces()
        if detected_faces:
            y = min(detected_faces, key=key_first_index)[1]
            y = lpf.filter_control(y)
            l_paddle.move(calibration_1[0]*y+calibration_1[1])

            y = max(detected_faces, key=key_first_index)[1]
            y = lpf.filter_control(y)
            r_paddle.move(calibration_1[0]*y+calibration_1[1])

        # Moving the ball
        if (ball.xcor()>-341 and (ball.xcor()+ball.dx<-350)):
            ball.setx(-341)
        elif (ball.xcor()<341 and (ball.xcor()+ball.dx>350)):
            ball.setx(341)
        else:
            ball.setx(ball.xcor() + ball.dx)
        
        ball.sety(ball.ycor() + ball.dy)

        # Border checking
        if ball.ycor() > 290:
            ball.sety(290)
            ball.dy *= -1

        if ball.ycor() < -290:
            ball.sety(-290)
            ball.dy *= -1

        if ball.xcor() > 390:
            ball.goto(0, 0)
            ball.dx = -2
            ball.dy = 2

        if ball.xcor() < -390:
            ball.goto(0, 0)
            ball.dx = 2
            ball.dy = 2

        # Paddle and ball collisions
        if (ball.xcor() > 340 and ball.xcor() < 350) and (ball.ycor() < r_paddle.paddle_.ycor()+40 and ball.ycor() > r_paddle.paddle_.ycor()-50):
            ball.dx *= -1.3
            ball.dy *= 1.3

        if (ball.xcor() < -340 and ball.xcor() > -350) and (ball.ycor() < l_paddle.paddle_.ycor()+50 and ball.ycor() > l_paddle.paddle_.ycor()-50):
            ball.dx *= -1.3
            ball.dy *= 1.3
