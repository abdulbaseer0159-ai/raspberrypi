import tkinter as tk
from gpiozero import LED, Servo
import sys

# --- Hardware Setup ---
# Define the GPIO pins for the 5 LEDs
led_pins = [17, 27, 22, 23, 24]
leds = [LED(pin) for pin in led_pins]

# Define the GPIO pin for the Servo (GPIO 18 is recommended for PWM)
servo = Servo(18)

# --- GUI Setup ---
class ControlPanel:
    def __init__(self, root):
        self.root = root
        self.root.title("Raspberry Pi 5 Control Panel")
        self.root.geometry("400x500")
        self.root.configure(bg="#f0f0f0")

        # Title Label
        title_label = tk.Label(root, text="Hardware Control Panel", font=("Arial", 18, "bold"), bg="#f0f0f0")
        title_label.pack(pady=10)

        # --- LED Controls ---
        led_frame = tk.LabelFrame(root, text="LED Controls", font=("Arial", 12), bg="#f0f0f0", padx=10, pady=10)
        led_frame.pack(fill="x", padx=20, pady=10)

        self.led_buttons = []
        for i, led in enumerate(leds):
            btn = tk.Button(
                led_frame, 
                text=f"LED {i+1} (GPIO {led_pins[i]})", 
                font=("Arial", 12),
                width=20,
                command=lambda idx=i: self.toggle_led(idx)
            )
            btn.pack(pady=5)
            self.led_buttons.append(btn)
            self.update_led_button_color(i)

        # --- Servo Control ---
        servo_frame = tk.LabelFrame(root, text="Servo Motor Control (GPIO 18)", font=("Arial", 12), bg="#f0f0f0", padx=10, pady=10)
        servo_frame.pack(fill="x", padx=20, pady=10)

        self.servo_label = tk.Label(servo_frame, text="Angle: 90°", font=("Arial", 14), bg="#f0f0f0")
        self.servo_label.pack(pady=5)

        self.servo_slider = tk.Scale(
            servo_frame, 
            from_=0, to=180, 
            orient="horizontal", 
            length=300,
            font=("Arial", 12),
            command=self.update_servo
        )
        self.servo_slider.set(90) # Start at middle position
        self.servo_slider.pack(pady=5)

        # --- Quit Button ---
        quit_btn = tk.Button(root, text="Exit & Clean Up", font=("Arial", 12, "bold"), bg="#ff4d4d", fg="white", command=self.safe_exit)
        quit_btn.pack(pady=20)

    def toggle_led(self, index):
        leds[index].toggle()
        self.update_led_button_color(index)

    def update_led_button_color(self, index):
        # Change button color based on LED state
        if leds[index].is_lit:
            self.led_buttons[index].config(bg="#4dff4d", activebackground="#4dff4d")
        else:
            self.led_buttons[index].config(bg="#d9d9d9", activebackground="#d9d9d9")

    def update_servo(self, value):
        angle = int(value)
        self.servo_label.config(text=f"Angle: {angle}°")
        
        # gpiozero Servo expects values between -1.0 (min) and 1.0 (max)
        # Map 0-180 degrees to -1.0 to 1.0
        servo_value = (angle / 90.0) - 1.0
        servo.value = servo_value

    def safe_exit(self):
        # Turn off all LEDs and center the servo before exiting
        for led in leds:
            led.off()
        servo.value = 0.0 # Center servo
        self.root.destroy()
        sys.exit()

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ControlPanel(root)
    # Ensure safe cleanup if the window is closed via the 'X' button
    root.protocol("WM_DELETE_WINDOW", app.safe_exit)
    root.mainloop()
