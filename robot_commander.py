# This version is currently set to work with the new brand HP Robots: Otto Starter
# Robot Commander by Iván R. Artiles
import network
import urequests
import time
import machine
from ottomotor import OttoMotor  # Import the motor library
from ottobuzzer import OttoBuzzer

FIREBASE_URL = "https://yourproject.firebaseio.com/commands.json"
CHECK_INTERVAL = 5

# Variables for motor control
sliderR = 40
sliderL = 50
# Servo duty values
loDutyL = 25
hiDutyL = 125
midDutyL = 75  # int(loDutyL + (hiDutyL - loDutyL)/2)
loDutyR = 25
hiDutyR = 125
midDutyR = 75  # int(loDutyR + (hiDutyR - loDutyR)/2)
# Initialize motor object
buzzer = OttoBuzzer(25) # Built in Buzzer
motor = OttoMotor(13, 14) # Connectors 10 & 11

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)

    while not wlan.isconnected():
        print("Connecting to WiFi...")
        time.sleep(1)
    
    buzzer.playEmoji('S_connection')
    print("Connected to WiFi:", wlan.ifconfig())
    
def check_wifi_status():
    wlan = network.WLAN(network.STA_IF)
    if not wlan.isconnected():
        print("WiFi connection lost, reconnecting...")
        connect_wifi(ssid, password)

def fetch_command():
    retries = 3  # Number of retries in case of failure
    for i in range(retries):
        try:
            response = urequests.get(FIREBASE_URL)
            print(response.json())
            if response.status_code == 200:
                data = response.json()
                if data:
                    # Get the last command entry
                    last_command = list(data.values())[-1]
                    #print(last_command)
                    command = last_command.get('command')
                    return command
                else:
                    print("No commands found")
            else:
                print("Failed to fetch command:", response.status_code)
            break  # If no exception, break the loop
        except Exception as e:
            print(f"Error fetching command (attempt {i + 1}/{retries}): {e}")
            time.sleep(2)  # Wait 2 seconds before retrying
    print("Failed to fetch command after retries.")
    return None  # Return None if all retries fail

def control_led(command):
    if command == "LED ON":
        led.value(1)
        print("LED turned ON")
    elif command == "LED OFF":
        led.value(0)
        print("LED turned OFF")
    else:
        print("Unknown command:", command)

def MotorsMove(right_speed, left_speed, direction, t=None):
    right_speed = int(right_speed / 2)
    left_speed = int(left_speed / 2)

    if direction == "forward":
        motor.leftServo.duty(midDutyL + left_speed) 
        motor.rightServo.duty(midDutyR - right_speed) 
    elif direction == "backward":
        motor.leftServo.duty(midDutyL - left_speed) 
        motor.rightServo.duty(midDutyR + right_speed) 
    elif direction == "right":
        motor.leftServo.duty(midDutyL + left_speed) 
        motor.rightServo.duty(midDutyR + right_speed) 
    elif direction == "left":
        motor.leftServo.duty(midDutyL - left_speed) 
        motor.rightServo.duty(midDutyR - right_speed) 
    else:
        raise ValueError("Invalid direction")

    if t is not None:
        time.sleep(t)
        motor.Stop(1)  # Stop after time limit

def control_motors(command):
    try:
        # Split the command into parts: "MOVE DIRECTION TIME"
        parts = command.split()
        direction = parts[1]  # Get the direction (e.g., forward, backward, left, right)
        time_limit = float(parts[2])  # Convert the time (e.g., 4, 2.4) to float

        if direction == "forward":
            MotorsMove(sliderR, sliderL, "forward", time_limit)
            print(f"Moving forward for {time_limit} seconds")
        elif direction == "backward":
            MotorsMove(sliderR, sliderL, "backward", time_limit)
            print(f"Moving backward for {time_limit} seconds")
        elif direction == "left":
            MotorsMove(sliderR, sliderL, "left", time_limit)
            print(f"Turning left for {time_limit} seconds")
        elif direction == "right":
            MotorsMove(sliderR, sliderL, "right", time_limit)
            print(f"Turning right for {time_limit} seconds")
        else:
            print(f"Unknown direction: {direction}")
    except (IndexError, ValueError) as e:
        print(f"Invalid command format: {command}. Error: {e}")

def main():
    global led
    led = machine.Pin(2, machine.Pin.OUT)

    ssid = "ssid"
    password = "pass"

    connect_wifi(ssid, password)

    last_command = None  # Initialize variable to store the last command

    while True:
        command = fetch_command()
        #print(command)
        if command and command != last_command:  # Only execute if the command is different
            if "led" in command:
                control_led(command)
            elif "move" in command:
                control_motors(command)
            last_command = command  # Update the last command
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()