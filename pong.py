#Author: Emil Bero
import tkinter as tk
import random

class PongGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pong Game")
        self.geometry("600x400")

        # Initial ball speed
        self.initial_ball_speed_x = 5
        self.initial_ball_speed_y = 5
        self.ball_speed_x = self.initial_ball_speed_x
        self.ball_speed_y = self.initial_ball_speed_y
        # Increment ball speed after each paddle hit to increase gameplay difficulty
        self.speed_increment = 0.5  

        self.paddle_speed = 10
        self.is_up_pressed = False
        self.is_down_pressed = False

        self.random = random

        self.user_score = 0
        self.random_score = 0

        self.create_widgets()

        # Bind keyboard events for paddle control
        self.bind("<KeyPress-Up>", self.key_up_pressed)
        self.bind("<KeyRelease-Up>", self.key_up_released)
        self.bind("<KeyPress-Down>", self.key_down_pressed)
        self.bind("<KeyRelease-Down>", self.key_down_released)

        # Start the game loop
        self.after(20, self.update_game)

    def create_widgets(self):
        # Create the game canvas
        self.canvas = tk.Canvas(self, width=600, height=400, bg="black")
        self.canvas.pack()

        # Create paddles
        self.paddle_user = self.canvas.create_rectangle(10, 150, 30, 250, fill="white")
        self.paddle_random = self.canvas.create_rectangle(560, 150, 580, 250, fill="white")

        # Create the ball
        self.ball = self.canvas.create_oval(290, 190, 310, 210, fill="white")

        # Create scoreboards
        self.score_user = tk.Label(self, text="User: 0", fg="white", bg="black")
        self.score_user.place(x=10, y=10)

        self.score_random = tk.Label(self, text="Random: 0", fg="white", bg="black")
        self.score_random.place(x=500, y=10)

    def update_game(self):
        # Move the user-controlled paddle
        if self.is_up_pressed and self.canvas.coords(self.paddle_user)[1] > 0:
            self.canvas.move(self.paddle_user, 0, -self.paddle_speed)
        if self.is_down_pressed and self.canvas.coords(self.paddle_user)[3] < 400:
            self.canvas.move(self.paddle_user, 0, self.paddle_speed)

        # Move the AI-controlled paddle
        self.move_ai_paddle()

        # Move the ball
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)

        # Check for collisions with walls
        ball_coords = self.canvas.coords(self.ball)
        if ball_coords[1] <= 0 or ball_coords[3] >= 400:
            self.ball_speed_y = -self.ball_speed_y

        # Check for collisions with paddles
        if self.check_collision(self.paddle_user):
            self.ball_speed_x = abs(self.ball_speed_x) + self.speed_increment
        if self.check_collision(self.paddle_random):
            self.ball_speed_x = -abs(self.ball_speed_x) - self.speed_increment

        # Check for scoring
        if ball_coords[2] >= 600:
            self.user_score += 1
            self.score_user.config(text=f"User: {self.user_score}")
            self.reset_ball()

        elif ball_coords[0] <= 0:
            self.random_score += 1
            self.score_random.config(text=f"Random: {self.random_score}")
            self.reset_ball()

        # Schedule the next update
        self.after(20, self.update_game)

    def move_ai_paddle(self):
        paddle_coords = self.canvas.coords(self.paddle_random)
        ball_coords = self.canvas.coords(self.ball)
        
        # Center of the AI paddle
        paddle_center_y = (paddle_coords[1] + paddle_coords[3]) / 2
        
        # Center of the ball
        ball_center_y = (ball_coords[1] + ball_coords[3]) / 2
        
        # Move AI paddle towards the ball
        if paddle_center_y < ball_center_y and paddle_coords[3] < 400:
            self.canvas.move(self.paddle_random, 0, self.paddle_speed // 2)
        elif paddle_center_y > ball_center_y and paddle_coords[1] > 0:
            self.canvas.move(self.paddle_random, 0, -self.paddle_speed // 2)

    def check_collision(self, paddle):
        ball_coords = self.canvas.coords(self.ball)
        paddle_coords = self.canvas.coords(paddle)
        # Check if ball collides with paddle
        return (ball_coords[2] >= paddle_coords[0] and ball_coords[0] <= paddle_coords[2] and
                ball_coords[3] >= paddle_coords[1] and ball_coords[1] <= paddle_coords[3])

    def key_up_pressed(self, event):
        self.is_up_pressed = True

    def key_up_released(self, event):
        self.is_up_pressed = False

    def key_down_pressed(self, event):
        self.is_down_pressed = True

    def key_down_released(self, event):
        self.is_down_pressed = False

    def reset_ball(self):
        # Reset the ball position
        self.canvas.coords(self.ball, 290, 190, 310, 210)
        # Reset the ball speed to initial values 
        self.ball_speed_x = self.initial_ball_speed_x if self.ball_speed_x > 0 else -self.initial_ball_speed_x
        self.ball_speed_y = self.initial_ball_speed_y

if __name__ == "__main__":
    game = PongGame()
    game.mainloop()
