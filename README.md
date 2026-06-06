# News Aggregator

Search news from multiple sources (NYT, Fox, BBC) in one place.

## Setup

### Backend (Flask)

```bash
pip install -r requirements.txt
python main.py
```

Runs at http://localhost:5000

### (Optional) AWS DynamoDB click history

The app can store a per-browser “recently viewed” history of articles you click/open.

- **Storage**: DynamoDB table with partition key `clientId` and sort key `clickedAt`
- **Backend env vars**:
  - **`NEWS_HISTORY_TABLE`**: DynamoDB table name (required to enable history)
  - **`NEWS_HISTORY_TTL_DAYS`**: days to keep history (default `30`)
  - Standard AWS credentials/region via environment or AWS config (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_REGION`, etc.)

Create the table (AWS CLI):

```bash
aws dynamodb create-table ^
  --table-name NewsClickHistory ^
  --attribute-definitions AttributeName=clientId,AttributeType=S AttributeName=clickedAt,AttributeType=S ^
  --key-schema AttributeName=clientId,KeyType=HASH AttributeName=clickedAt,KeyType=RANGE ^
  --billing-mode PAY_PER_REQUEST
```

Then set the environment variable before starting Flask:

```bash
set NEWS_HISTORY_TABLE=NewsClickHistory
python main.py
```

Notes:
- The backend uses DynamoDB TTL attribute **`expiresAt`** (epoch seconds). If you want automatic expiration, enable TTL for `expiresAt` in the DynamoDB console.

### Frontend (React)

```bash
cd frontend
npm install
npm run dev
```

Runs at http://localhost:5173

## Usage

1. Start the Flask backend first (`python main.py`)
2. Start the React frontend (`cd frontend && npm run dev`)
3. Open http://localhost:5173 in your browser
4. Search for a topic or leave empty to see all articles
5. Click any article to view details and open the full story
6. Your recently viewed articles show at the top (stored in DynamoDB if configured)
