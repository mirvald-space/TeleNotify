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
  - Body: `{"text": "Your notification message", "format": "plain|html|markdown"}`

## Testing

The project includes a comprehensive test suite to ensure the reliability and correctness of the notification service. The tests cover various scenarios including:

1. Sending notifications with different message formats (plain text, HTML, Markdown)
2. Auto-detection of message format
3. Handling of special characters
4. Error cases (empty messages, missing text)
5. Query parameter and JSON body interactions

To run the tests, use the following command:

```
pytest -v
```

The test suite is located in the `tests/test_api.py` file. It uses pytest and pytest-asyncio for asynchronous test support.

Key test scenarios include:

- Sending notifications via query parameters and request body
- Testing different message formats (plain, HTML, Markdown)
- Verifying correct handling of special characters
- Checking error responses for invalid inputs
- Testing auto-detection of message format

For more details on the tests, refer to the `tests/test_api.py` file.

## Development

1. Make your changes
2. Update tests if necessary
3. Ensure all tests pass
4. Create a pull request

## License

This project is licensed under the MIT License.
