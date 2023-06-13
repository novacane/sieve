from flask import Flask, request, jsonify
from celery import Celery
import redis 
import uuid
import json
from uuid import UUID
from ml_processing import *

sieve = Flask(__name__)
sieve.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'


celery = Celery(sieve.name, broker=sieve.config['CELERY_BROKER_URL'])
celery.conf.update(sieve.config)

db = redis.Redis()


@sieve.route('/push', methods=['POST'])
def push():
    source_name = request.json.get('source_name')
    source_url = request.json.get('source_url')
    id = str(uuid.uuid4())
    
    fields = {
        'source_name': source_name,
        'source_url': source_url,
        'status': 'queued'
    }

    db.hmset(id, fields)
    db.rpush("list", id)
    process_video_chain.delay(id)
    response = jsonify({'unique_id': id})
    return response, 200

@sieve.route('/status/<string:id>', methods=['GET'])
def status(id: UUID):
    if id not in db:
        return jsonify({'error': f' Video with ID {id} not found.'}), 404
    
    status = decode(db.hget(id, 'status'))
    response = jsonify({'status': status})
    return response, 200

@sieve.route('/query/<string:id>', methods=['GET'])
def query(id: UUID):
    if id not in db:
        response = jsonify({'error': f'Video with ID {id} not found.'})
        return response, 404
    
    status = decode(db.hget(id, 'status'))

    if status != 'finished':
        response = jsonify({'error': f'Video with ID {id} is currently {status}.'})
        return response, 400
    
    data = json.loads(db.hget(id, 'data'))
    response = jsonify({'data': data})
    return response, 200

@sieve.route('/list', methods=['GET'])
def listOfSubmitted():
    data = db.lrange("list", 0, -1)
    data = list(map(decode, data))
    response = jsonify({'data': data})
    return response, 200

def decode(bytes: bytes) -> str:
    return bytes.decode('utf-8')

@celery.task
def process_video_chain(id: UUID):
    db.hset(id, 'status', 'processing')
    url = decode(db.hget(id, 'source_url'))
    processed = process_video(url)
    data = format(processed)
    db.hset(id, 'data', data)
    db.hset(id, 'status', 'finished')

if __name__ == '__main__':
    sieve.run(debug=True)
