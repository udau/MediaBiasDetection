from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import time
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv(override=True)

import boto3
from boto3.dynamodb.conditions import Key
import feedparser
from scraper import scrape_article
from model import predict_stance

app = Flask(__name__)
CORS(app)

NEWS_HISTORY_TABLE = os.getenv('NEWS_HISTORY_TABLE', '').strip()
NEWS_HISTORY_TTL_DAYS = int(os.getenv('NEWS_HISTORY_TTL_DAYS', '30'))

_dynamodb = None
_history_table = None


def _get_history_table():
    global _dynamodb, _history_table

    if _history_table is not None:
        return _history_table

    if not NEWS_HISTORY_TABLE:
        return None

    if _dynamodb is None:
        _dynamodb = boto3.resource(
                'dynamodb',
            region_name=os.getenv('AWS_REGION')
        )

    _history_table = _dynamodb.Table(NEWS_HISTORY_TABLE)
    return _history_table


RssFeed = {
    'NYT': 'https://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml',
    'FOX': 'https://moxie.foxnews.com/google-publisher/latest.xml',
    'BBC': 'https://feeds.bbci.co.uk/news/rss.xml',
}


@app.route('/api/news')
def api_news():
    query = request.args.get('query', '').lower()
    full_content = request.args.get('full_content', 'false').lower() == 'true'
    articles = []

    for source, feed_url in RssFeed.items():
        parsed = feedparser.parse(feed_url)
        for i, entry in enumerate(parsed.entries):
            title = entry.get('title', '')
            summary = entry.get('summary', '') or entry.get('description', '')
            if query and query not in title.lower() and query not in summary.lower():
                continue

            published_iso = None
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                try:
                    published_iso = datetime(*entry.published_parsed[:6]).isoformat()
                except Exception:
                    pass

            image_url = None
            if hasattr(entry, 'media_content') and entry.media_content:
                image_url = entry.media_content[0].get('url')
            elif hasattr(entry, 'media_thumbnail') and entry.media_thumbnail:
                image_url = entry.media_thumbnail[0].get('url')

            article = {
                'id': f'{source}-{i}',
                'title': title,
                'source': source,
                'publishedAt': published_iso,
                'summary': summary,
                'url': entry.get('link', ''),
                'imageUrl': image_url,
            }

            if full_content and source == 'FOX':
                article['content'] = scrape_article(article['url'])

            articles.append(article)

    articles.sort(key=lambda a: a['publishedAt'] or '', reverse=True)
    return jsonify(articles)


@app.route('/api/news/content')
def api_news_content():
    url = request.args.get('url')
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    content = scrape_article(url)
    if content:
        return jsonify({'content': content})
    else:
        return jsonify({'error': 'Failed to scrape content or source not supported'}), 404


@app.route('/api/history/click', methods=['POST'])
def history_click():
    table = _get_history_table()
    if table is None:
        return jsonify({'error': 'History storage not configured. Set NEWS_HISTORY_TABLE.'}), 501

    payload = request.get_json(silent=True) or {}
    client_id = (payload.get('clientId') or '').strip()
    article = payload.get('article') or {}

    if not client_id:
        return jsonify({'error': 'clientId is required'}), 400

    clicked_at = datetime.now(timezone.utc).isoformat()
    ttl_seconds = max(0, NEWS_HISTORY_TTL_DAYS) * 24 * 60 * 60
    expires_at = int(time.time()) + ttl_seconds if ttl_seconds else None

    item = {
        'clientId': client_id,
        'clickedAt': clicked_at,  # sort key (ISO time)
        'articleId': str(article.get('id') or ''),
        'title': str(article.get('title') or ''),
        'source': str(article.get('source') or ''),
        'publishedAt': str(article.get('publishedAt') or ''),
        'summary': str(article.get('summary') or ''),
        'url': str(article.get('url') or ''),
        'imageUrl': str(article.get('imageUrl') or ''),
    }

    if expires_at is not None:
        item['expiresAt'] = expires_at  # DynamoDB TTL attribute (enable TTL on table)

    table.put_item(Item=item)
    return jsonify({'ok': True, 'clickedAt': clicked_at})


@app.route('/api/history', methods=['GET'])
def history_list():
    table = _get_history_table()
    if table is None:
        return jsonify({'error': 'History storage not configured. Set NEWS_HISTORY_TABLE.'}), 501

    client_id = (request.args.get('clientId') or '').strip()
    if not client_id:
        return jsonify({'error': 'clientId is required'}), 400

    try:
        limit = int(request.args.get('limit') or '25')
    except ValueError:
        limit = 25
    limit = max(1, min(100, limit))

    resp = table.query(
        KeyConditionExpression=Key('clientId').eq(client_id),
        ScanIndexForward=False,
        Limit=limit,
    )
    items = resp.get('Items', [])
    return jsonify(items)

@app.route('/api/analyze', methods=['POST'])
def analyze_stance():
    payload = request.get_json(silent=True) or {}
    text = payload.get('text')
    if not text:
        return jsonify({'error': 'Text is required for analysis'}), 400
    
    try:
        results = predict_stance(text)
        return jsonify(results)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
