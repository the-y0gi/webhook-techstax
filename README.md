# GitHub Webhook Monitor - TechStax Assessment

A full-stack application that receives GitHub webhooks, stores them in MongoDB, and displays them on a real-time dashboard using 15-second polling.

## Features

- **Webhook Receiver:** Flask endpoint to capture Push, PR, and Merge events.
- **Data Persistence:** Stores formatted action data in MongoDB.
- **Real-time UI:** Clean and minimal dashboard with 15-second auto-refresh.
- **UTC Timestamps:** All events are logged in UTC format as per requirements.

## Tech Stack

- **Backend:** Flask (Python)
- **Database:** MongoDB
- **Frontend:** HTML, CSS, JavaScript (Vanilla JS for polling)

## Setup Instructions

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Configure Environment:** Create a .env file and add your MongoDB URI:
   ```env
   MONGO_URI=mongodb://localhost:27017/
   ```
3. **Run the Application:**
   ```bash
   python app.py
   ```
4. **Webhook Setup:**
   - Use ngrok to tunnel your local port 5000.
   - Add the ngrok URL (ending in /webhook) to your GitHub repository settings.
   - Select events: Pushes and Pull Requests.

## MongoDB Schema

| Field         | Type   | Description               |
| :------------ | :----- | :------------------------ |
| `request_id`  | String | Commit Hash or PR ID      |
| `author`      | String | GitHub Username           |
| `action`      | Enum   | PUSH, PULL_REQUEST, MERGE |
| `from_branch` | String | Source branch             |
| `to_branch`   | String | Destination branch        |
| `timestamp`   | String | UTC Formatted Datetime    |
