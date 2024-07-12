# MQTT RabbitMQ MongoDB Integration Project with FastAPI

This project demonstrates integration of MQTT messaging using RabbitMQ, data processing and storage in MongoDB, and exposing an API for data retrieval using FastAPI.

### Project Structure

- **client/**: Contains MQTT client scripts.
  - `mqtt_client.py`: Sends MQTT messages with random status every second.
  - `requirements.txt`: Dependencies for MQTT client.

- **server/**: Contains MQTT server scripts and API endpoint.
  - `mqtt_server.py`: Listens to MQTT messages, processes and stores data in MongoDB.
  - `app.py`: Provides an API endpoint to retrieve status counts within a specified time range using FastAPI.
  - `requirements.txt`: Dependencies for MQTT server and API.

### Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd rabitmqt_project


##############################################

COMMANDS - 

cd client
pip install -r requirements.txt
python mqtt_client.py

cd ../server
pip install -r requirements.txt
python mqtt_server.py


###########################################################################

Run this command on command promot

uvicorn app:app --reload

after running successfully above command 
then call  this endpoint of the api on postman and adjust the startTime and endTime according to you
http://localhost:8000/test/get_status_count?startTime=2024-07-09T08:00:00&endTime=2024-07-09T12:00:00