import tkinter as tk
import random

class PongGame(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Pong Game")
        self.geometry("1920x1080")  # Set window size to 1920x1080
        self.fullScreenState = False  # Fullscreen flag

        # Initial ball speed
        self.initial_ball_speed_x = 10  # Increased ball speed for larger screen
        self.initial_ball_speed_y = 10  # Increased ball speed for larger screen
        self.ball_speed_x = self.initial_ball_speed_x
        self.ball_speed_y = self.initial_ball_speed_y
        # Increment ball speed after each paddle hit to increase gameplay difficulty
        self.speed_increment = 0.5  

        self.paddle_speed = 20  # Adjusted paddle speed for larger screen
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
        self.canvas = tk.Canvas(self, width=1920, height=1080, bg="black")  # Set canvas size to match window size
        self.canvas.pack(fill=tk.BOTH, expand=True)  # Fill the entire window

        # Create paddles
        self.paddle_user = self.canvas.create_rectangle(30, 420, 60, 660, fill="white")  # Adjusted paddle position
        self.paddle_random = self.canvas.create_rectangle(1860, 420, 1890, 660, fill="white")  # Adjusted paddle position

        # Create the ball
        self.ball = self.canvas.create_oval(930, 540, 990, 600, fill="white")  # Adjusted ball position

        # Create scoreboards
        self.score_user = tk.Label(self, text="User: 0", fg="white", bg="black", font=("Arial", 24))
        self.score_user.place(x=20, y=20)

        self.score_random = tk.Label(self, text="Random: 0", fg="white", bg="black", font=("Arial", 24))
        self.score_random.place(x=1700, y=20)

    def update_game(self):
        # Move the user-controlled paddle
        if self.is_up_pressed and self.canvas.coords(self.paddle_user)[1] > 0:
            self.canvas.move(self.paddle_user, 0, -self.paddle_speed)
        if self.is_down_pressed and self.canvas.coords(self.paddle_user)[3] < 1080:
            self.canvas.move(self.paddle_user, 0, self.paddle_speed)

        # Move the AI-controlled paddle
        self.move_ai_paddle()

        # Move the ball
        self.canvas.move(self.ball, self.ball_speed_x, self.ball_speed_y)

        # Check for collisions with walls
        ball_coords = self.canvas.coords(self.ball)
        if ball_coords[1] <= 0 or ball_coords[3] >= 1080:
            self.ball_speed_y = -self.ball_speed_y

        # Check for collisions with paddles
        if self.check_collision(self.paddle_user):
            self.ball_speed_x = abs(self.ball_speed_x) + self.speed_increment
        if self.check_collision(self.paddle_random):
            self.ball_speed_x = -abs(self.ball_speed_x) - self.speed_increment

        # Check for scoring
        if ball_coords[2] >= 1920:
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
        if paddle_center_y < ball_center_y and paddle_coords[3] < 1080:
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
        self.canvas.coords(self.ball, 930, 540, 990, 600)
        # Reset the ball speed to initial values 
        self.ball_speed_x = self.initial_ball_speed_x if self.ball_speed_x > 0 else -self.initial_ball_speed_x
        self.ball_speed_y = self.initial_ball_speed_y

if __name__ == "__main__":
    game = PongGame()
    game.mainloop()
