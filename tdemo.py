import time
from cli import *

# Create a global variable to keep track of the current frame
current_frame = 0


# Define a function to draw a bouncing ball
def draw_bouncing_ball(x, y):
    ball_char = 'O'
    ball_color_fg = (255, 0, 0)  # Red foreground color
    ball_color_bg = (0, 0, 0)  # Black background color

    # Draw the bouncing ball
    set_color_fg(x, y, *ball_color_fg)
    set_color_bg(x, y, *ball_color_bg)
    set_char(x, y, ball_char)


# Define a function to update the bouncing ball's position
def update_bouncing_ball(x, y, dx, dy):
    # Clear the previous position of the ball
    set_char(x, y, ' ')

    # Update the ball's position
    x += dx
    y += dy

    # Ensure the ball stays within the console boundaries
    if not is_valid_pos(x, y):
        if x < 0:
            x = 0
            dx = -dx
        elif x >= size.columns:
            x = size.columns - 1
            dx = -dx
        if y < 0:
            y = 0
            dy = -dy
        elif y >= size.lines:
            y = size.lines - 1
            dy = -dy

    # Draw the ball at the new position
    draw_bouncing_ball(x, y)

    return x, y, dx, dy


# Create a function to handle the "start" command
def start_command(command: str):
    global current_frame
    current_frame = 0
    clear()  # Clear the console
    hide_cursor()  # Hide the cursor
    draw_bouncing_ball(size.columns // 2, size.lines // 2)  # Initial ball position


# Create a function to handle the "stop" command
def stop_command(command: str):
    show_cursor()  # Show the cursor
    current_frame = 0


# Create a function to handle the "record" command
def record_command(command: str):
    global current_frame
    current_frame = 0
    hide_cursor()  # Hide the cursor
    clear()  # Clear the console
    frames = Record()  # Create a Record object

    # Bouncing ball variables
    ball_x, ball_y = size.columns // 2, size.lines // 2
    ball_dx, ball_dy = 1, 1

    # Record frames for 5 seconds
    while current_frame < 200:
        update()
        frames.update()
        ball_x, ball_y, ball_dx, ball_dy = update_bouncing_ball(ball_x, ball_y, ball_dx, ball_dy)
        current_frame += 1
        time.sleep(0.03)  # Delay to control the frame rate

    frames.write("recorded_demo.cli")  # Save recorded frames to a file
    show_cursor()  # Show the cursor


# Create a function to handle the "play" command
def play_command(command: str):
    hide_cursor()  # Hide the cursor
    play_frames = PlayRecord("recorded_demo.cli")  # Load recorded frames
    clear()  # Clear the console

    # Play recorded frames
    while current_frame < len(play_frames.frames):
        update()
        play_frames.update()
        current_frame += 1
        time.sleep(0.03)


# Initialize the CLI graphics library
init()

# Create a CmdSystem instance to manage commands
cmd_system = CmdSystem()

# Add custom commands to the command system
cmd_system.AddCommand("start", start_command, "Start the bouncing ball demo")
cmd_system.AddCommand("stop", stop_command, "Stop the bouncing ball demo")
cmd_system.AddCommand("record", record_command, "Record the bouncing ball animation")
cmd_system.AddCommand("play", play_command, "Play the recorded animation")

# Main loop for command execution
while True:
    command = input("Enter a command (start/stop/record/play/exit): ")
    if command == "exit":
        break
    clear()  # Clear the console
    cmd_system.ExecCommand(command)
    update()  # Update the console
    draw()  # Render the console
