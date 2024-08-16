# Telegram Notification Bot

A FastAPI-based service for sending notifications to Telegram groups with support for Slack-like webhook parameters.

## Requirements

- Python 3.12+
- Docker
- Docker Compose

## Environment Variables

Create a `.env` file in the root directory with the following content:

```
BOT_TOKEN=your_telegram_bot_token
GROUP_IDS=id1,id2,id3
WEBHOOK_URL=https://your-domain.com
WEBAPP_HOST=0.0.0.0
WEBAPP_PORT=8000
```

- `BOT_TOKEN`: Your Telegram Bot Token
- `GROUP_IDS`: Comma-separated list of Telegram group IDs
- `WEBHOOK_URL`: The URL where your bot will receive updates
- `WEBAPP_HOST`: Host to bind the web application (default: 0.0.0.0)
- `WEBAPP_PORT`: Port to run the web application (default: 8000)

## Local Development

1. Clone the repository:

   ```
   git clone https://github.com/yourusername/tg-push.git
   cd tg-push
   ```

2. Create and activate a virtual environment:

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   uvicorn app.main:app --reload
   ```

The API will be available at `http://localhost:8000`.

## Deployment with Docker

### Local Deployment

1. Build and run the Docker container:

   ```
   docker-compose up --build
   ```

2. The API will be available at `http://localhost:8000`.

### Server Deployment

1. Ensure Docker and Docker Compose are installed on your server.

2. Clone the repository on your server:

   ```
   git clone https://github.com/yourusername/tg-push.git
   cd tg-push
   ```

3. Create a `.env` file with your production environment variables.

4. Build and run the Docker container:

   ```
   docker-compose up --build -d
   ```

5. Set up a reverse proxy (e.g., Nginx) to forward requests to your container.

6. Configure SSL/TLS for secure communication.

## API Endpoints

- POST `/send_notification`
  - Body:
    ```json
    {
    	"message": "Your notification message",
    	"text": "Alternative to message for Slack compatibility",
    	"channel": "#your-channel",
    	"username": "bot-username",
    	"icon_emoji": ":emoji:",
    	"link_names": true,
    	"mrkdwn": true
    }
    ```
  - Note: `message` or `text` is required. Other fields are optional and for Slack compatibility.

## Testing

Run tests with pytest:

```
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License.
