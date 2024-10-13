# Robot Command Center

A simple web interface to send commands to a robot remotely. This project demonstrates how to store commands in a Firebase Realtime Database, which are then read and executed by a robot using **ESP32** and **Micropython**. The project uses **HTML**, **CSS**, and **JavaScript** for the web interface and integrates with Firebase for real-time command storage.

## Features

- **Send Commands**: Users can send text commands remotely to control the robot.
- **Command History**: Displays a log of commands sent with success/error statuses.
- **Firebase Integration**: Commands are stored and retrieved in real-time from Firebase's Realtime Database.
- **Robot Execution**: A robot with an **ESP32** microcontroller and **Micropython** listens for commands from the database and executes them.

## Getting Started

Follow these instructions to set up the project on your local machine and get the robot connected.

### Prerequisites

- **Firebase** project with Realtime Database enabled.
- **ESP32** microcontroller with **Micropython** installed.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/robot-command-center.git
   ```
   
2. Navigate to the project folder:
   ```bash
   cd robot-command-center
   ```

3. Set up Firebase configuration:
   - Replace the Firebase configuration object in `script.js` with your Firebase project credentials.

4. Upload the **Micropython** code to the ESP32:
   - The provided Micropython script (`robot_commands.py`) reads commands from Firebase and controls the robot.
   - Upload this code to your ESP32 using an IDE like **Thonny** or **uPyCraft**.

5. Open the `index.html` file in your web browser to access the web interface.

### Firebase Setup

To enable real-time command storage, follow these steps to create and configure your Firebase Realtime Database:

1. **Create a Firebase Project**:
   - Go to [Firebase Console](https://console.firebase.google.com/).
   - Click **Add Project**, name it, and follow the setup instructions.

2. **Enable Realtime Database**:
   - In the Firebase Console, navigate to **Database**.
   - Click **Create Database** under Realtime Database and set the location.
   - Choose to start in **Test Mode** (or configure rules for production).

3. **Get Firebase Config**:
   - Under **Project Settings**, find your **Firebase SDK Config**.
   - Replace the placeholder values in `script.js` with this information:
   ```js
   const firebaseConfig = {
     apiKey: "YOUR_API_KEY",
     authDomain: "YOUR_AUTH_DOMAIN",
     databaseURL: "YOUR_DATABASE_URL",
     projectId: "YOUR_PROJECT_ID",
     storageBucket: "YOUR_STORAGE_BUCKET",
     messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
     appId: "YOUR_APP_ID"
   };
   ```

4. **Set Database Structure**:
   - Create a node in your Realtime Database called `commands` where the web interface will push user commands.
   - The robot (via the ESP32 and Micropython) will read from this `commands` node to execute the latest command.

### Usage

1. Open the web interface and enter a command in the input field.
2. Press **Send Command** to store the command in the Firebase database.
3. The command history will be displayed with the success or error status.
4. If your robot is connected and listening to the database, it will execute the command.

### Example Commands for Robot

- `MOVE FORWARD 5`
- `TURN RIGHT`
- `LED ON`
- `STOP`

### Robot Setup (ESP32 + Micropython)

- **ESP32** is the microcontroller that runs the robot.
- The **Micropython** script (`robot_commands.py`) listens for commands from Firebase and interprets them to control motors, LEDs, or other components of the robot.
- Commands like "MOVE FORWARD 5" or "LED ON" will be executed based on how the robot is programmed.

## Screenshots

Insert screenshots of your project here to give users a visual representation of the interface.

## Mini-Tutorial: Create a Firebase Realtime Database

Here’s a quick guide on setting up a Firebase Realtime Database:

1. **Go to Firebase Console** and click **Add Project**.
2. **Name your project**, then click **Create**.
3. **Enable Realtime Database**: 
   - Go to the **Database** section, and click **Create Database** under Realtime Database.
   - Set up the database rules. For testing, you can allow public access by using:
   ```json
   {
     "rules": {
       ".read": "true",
       ".write": "true"
     }
   }
   ```
   - Be sure to update these rules for production environments.
4. **Add your Firebase config** to your JavaScript code (as shown in the Firebase Setup section above).

## Contributing

Contributions are welcome! Feel free to fork the project and submit a pull request or open an issue for any feature requests or bugs.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
