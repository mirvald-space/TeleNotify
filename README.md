# Telegram Notification Bot

A FastAPI-based service for sending notifications to Telegram groups.

## Requirements

- Python 3.12+
- Docker (optional)

## Setup

1. Clone the repo:

   ```
   git clone https://github.com/yourusername/tg-push.git
   cd tg-push
   ```

2. Create a virtual environment (optional but recommended):

   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

4. Set up environment variables:
   Create a `.env` file in the root directory with the following content:
   ```
   BOT_TOKEN=your_bot_token_here
   GROUP_IDS=id1,id2,id3
   WEBHOOK_URL=https://your-domain.com
   ```

## Running the Application

### Local

```
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`.

### Docker

```
docker-compose up --build
```

## API Endpoints

- POST `/send_notification`
  - Query Parameters:
    - `text`: The notification message (required)
    - `bot_id`: Custom bot token (optional)
    - `chat_id`: Custom chat ID or list of chat IDs (optional)
    - `format`: Message format ('plain', 'html', or 'markdown') (optional)
  - Body: JSON object with the same fields as query parameters (optional)

### Usage Examples

1. Basic notification:

   ```
   curl -X POST "http://localhost:8000/send_notification?text=Hello, World!"
   ```

2. Using custom bot and chat:

   ```
   curl -X POST "http://localhost:8000/send_notification?text=Custom notification&bot_id=your_custom_bot_token&chat_id=-1001234567890"
   ```

3. Sending HTML-formatted message:

   ```
   curl -X POST "http://localhost:8000/send_notification" \
        -H "Content-Type: application/json" \
        -d '{"text": "<b>Bold text</b> and <i>italic</i>", "format": "html"}'
   ```

4. Sending to multiple chats:
   ```
   curl -X POST "http://localhost:8000/send_notification" \
        -H "Content-Type: application/json" \
        -d '{"text": "Multi-chat message", "chat_id": [-1001234567890, -1009876543210]}'
   ```

## Advanced Usage

You can specify custom bot tokens and chat IDs for each notification. This allows you to use different bots or send to specific chats without changing the server configuration.

- If `bot_id` is not specified, the default bot from the environment variables will be used.
- If `chat_id` is not specified, the notification will be sent to all groups specified in the environment variables.
- You can provide parameters either as query parameters or in the JSON body of the request.

## Testing

The project includes a comprehensive test suite. To run the tests:

```
pytest -v
```

## Development

1. Make your changes
2. Update tests if necessary
3. Ensure all tests pass
4. Create a pull request

## License

This project is licensed under the MIT License.
