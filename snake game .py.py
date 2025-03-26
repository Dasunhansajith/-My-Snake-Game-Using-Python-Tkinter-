import tkinter as tk
import random

class SnakeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake Game")
        
        # Canvas settings
        self.width = 600
        self.height = 400
        self.cell_size = 20
        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="black")
        self.canvas.pack()
        
        # Game variables
        self.snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake body (list of coordinates)
        self.snake_direction = "Right"
        self.food_position = self.place_food()
        self.score = 0
        self.running = True
        
        # Draw initial game state
        self.draw_snake()
        self.draw_food()
        
        # Bind keys
        self.root.bind("<Up>", lambda event: self.change_direction("Up"))
        self.root.bind("<Down>", lambda event: self.change_direction("Down"))
        self.root.bind("<Left>", lambda event: self.change_direction("Left"))
        self.root.bind("<Right>", lambda event: self.change_direction("Right"))
        
        # Start the game loop
        self.game_loop()
    
    def place_food(self):
        """Place food at a random position."""
        x = random.randint(0, (self.width // self.cell_size) - 1) * self.cell_size
        y = random.randint(0, (self.height // self.cell_size) - 1) * self.cell_size
        return (x, y)
    
    def draw_snake(self):
        """Draw the snake on the canvas."""
        self.canvas.delete("snake")
        for segment in self.snake:
            x, y = segment
            self.canvas.create_rectangle(
                x, y, x + self.cell_size, y + self.cell_size, fill="green", tags="snake"
            )
    
    def draw_food(self):
        """Draw the food on the canvas."""
        self.canvas.delete("food")
        x, y = self.food_position
        self.canvas.create_oval(
            x, y, x + self.cell_size, y + self.cell_size, fill="red", tags="food"
        )
    
    def change_direction(self, direction):
        """Change the direction of the snake."""
        opposite_directions = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }
        if direction != opposite_directions.get(self.snake_direction):  # Prevent reversing
            self.snake_direction = direction
    
    def move_snake(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.snake[0]
        
        if self.snake_direction == "Up":
            new_head = (head_x, head_y - self.cell_size)
        elif self.snake_direction == "Down":
            new_head = (head_x, head_y + self.cell_size)
        elif self.snake_direction == "Left":
            new_head = (head_x - self.cell_size, head_y)
        elif self.snake_direction == "Right":
            new_head = (head_x + self.cell_size, head_y)
        
        # Check collisions
        if (
            new_head[0] < 0 or new_head[1] < 0 or
            new_head[0] >= self.width or new_head[1] >= self.height or
            new_head in self.snake
        ):
            self.running = False
            return
        
        # Move the snake
        self.snake.insert(0, new_head)
        
        # Check if the snake eats the food
        if new_head == self.food_position:
            self.food_position = self.place_food()
            self.score += 1
        else:
            self.snake.pop()  # Remove the tail
    
    def game_loop(self):
        """Main game loop."""
        if self.running:
            self.move_snake()
            self.draw_snake()
            self.draw_food()
            self.root.after(100, self.game_loop)  # Adjust speed by changing the delay
        else:
            self.show_game_over()

    def show_game_over(self):
        """Display the game over screen with Try Again and Exit options."""
        self.canvas.delete("all")
        self.canvas.create_text(
            self.width // 2, self.height // 3,
            text=f"Game Over!\nYour Score: {self.score}",
            fill="white", font=("Arial", 20), justify="center"
        )
        
        # Create buttons for Try Again and Exit
        try_again_button = tk.Button(
            self.root, text="Try Again", command=self.restart_game, bg="green", fg="white"
        )
        exit_button = tk.Button(
            self.root, text="Exit", command=self.root.quit, bg="red", fg="white"
        )
        
        self.canvas.create_window(self.width // 2 - 50, self.height // 2, window=try_again_button)
        self.canvas.create_window(self.width // 2 + 50, self.height // 2, window=exit_button)
    
    def restart_game(self):
        """Restart the game."""
        self.snake = [(100, 100), (80, 100), (60, 100)]  # Reset snake
        self.snake_direction = "Right"  # Reset direction
        self.food_position = self.place_food()  # Reset food position
        self.score = 0  # Reset score
        self.running = True  # Reset game state
        self.canvas.delete("all")  # Clear canvas
        self.draw_snake()  # Redraw initial snake
        self.draw_food()  # Redraw food
        self.game_loop()  # Restart game loop

# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeGame(root)
    root.mainloop()

