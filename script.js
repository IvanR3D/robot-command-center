// Import necessary Firebase modules
import { initializeApp } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-app.js";
import { getDatabase, ref, push } from "https://www.gstatic.com/firebasejs/9.17.1/firebase-database.js";

// Firebase configuration
const firebaseConfig = {
    apiKey: "YOUR_API_KEY",
    authDomain: "YOUR_AUTH_DOMAIN",
    databaseURL: "YOUR_DATABASE_URL",
    projectId: "YOUR_PROJECT_ID",
    storageBucket: "YOUR_STORAGE_BUCKET",
    messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
    appId: "YOUR_APP_ID"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const database = getDatabase(app);

// Function to send command to Firebase
function sendCommand() {
    const command = document.getElementById('command').value.toLowerCase();

    if (command.trim() !== "") {
        // Write the command to the 'commands' node in Firebase
        push(ref(database, 'commands'), {
            command: command,
        })
            .then(() => {
                console.log('Command sent:', command);
                addToHistory(command, 'success'); // Update UI with success status
            })
            .catch(error => {
                console.error('Error sending command:', error);
                addToHistory(command, 'error'); // Update UI with error status
            });

        // Clear input field
        document.getElementById('command').value = '';
    } else {
        alert("Please enter a command");
    }
}

// Function to add command to the command history in the UI
function addToHistory(command, status) {
    const historyList = document.getElementById("history");
    const listItem = document.createElement("li");
    const timestamp = new Date().toLocaleTimeString();

    listItem.classList.add(status);
    listItem.textContent = `${command.toUpperCase()} - ${timestamp} - ${status}`;

    historyList.prepend(listItem);
}

// Event listener for the button
document.getElementById("sendBtn").addEventListener("click", sendCommand);