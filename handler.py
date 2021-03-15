try:
    import unzip_requirements
except ImportError:
    pass
import json, requests, os
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)
SLACK_USER_ACCESS_TOKEN = os.environ['SLACK_USER_ACCESS_TOKEN']
TARGET_CHANNEL = os.environ['TARGET_CHANNEL']
ME = os.environ['ME']

def handler(event, context):
    logging.info(event)

    if 'cron' in event: # コールドスタート対策でCloudWatchからの定期的な呼び出しに対応
        return {
            'statusCode': 200,
            'body': 'cron'
        }

    if 'challenge' in event['body']: # Event Subscriptionsでエンドポイント登録時に必要
        body = json.loads(event['body'])
        logging.info(body)
        return {
            'statusCode': 200,
            'body': body['challenge']
        }

    body = json.loads(event['body'])
    if 'event' in event['body']:
        if body['event']['channel']==TARGET_CHANNEL:
            channel = body['event']['channel']
            text = body['event']['text']
            threadTs = body['event']['ts']
            if ME in text:
                postReply(channel, '了解', threadTs)
            return {
                'statusCode': 200,
                'body': text
            }

    return {
            'statusCode': 200,
            'body': 'end'
        }

def postReply(channel, text, threadTs):
    url = 'https://slack.com/api/chat.postMessage'
    headers = {
        'Authorization': 'Bearer ' + SLACK_USER_ACCESS_TOKEN
    }
    params = {
        'channel': channel,
        'as_user': True,
        'text': text,
        'thread_ts' : threadTs
    }
    res = requests.post(url, params=params, headers=headers)
    logging.info(res.json())