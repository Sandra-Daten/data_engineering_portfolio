# Flask + Redis: Visit Counter Web App

This project demonstrates a simple dynamic web application that displays the number of visits to a webpage. The application consists of two components:

- A **Flask** web service written in Python
- A **Redis** database that stores the visit count

Both components are deployed in separate Docker containers and connected through a custom Docker network.

## 📁 Project Structure

flask-redis-counter/
│
├── app.py # Flask web application
├── Dockerfile # Instructions for building the Flask image
├── requirements.txt # Python dependencies
├── run.sh # Script to build and run the application
├── README.md # Project documentation
└── redis-data/ # Local volume for Redis persistence


## How to Run

1. Make the script executable (first time only):

```bash
chmod +x run.sh

2. Start the application:

./run.sh

3. Open your browser and visit:

http://localhost:5001/

