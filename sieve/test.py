import requests
import json
import time
from main import decode

print("Pushing first video to queue")
time.sleep(1)
url = 'http://127.0.0.1:5000/push'
payload = {
    "source_name": "test1",
    "source_url": "https://storage.googleapis.com/sieve-public-videos/celebrity-videos/dwyane_basketball.mp4"
}
response = requests.post(url, json=payload)
res = json.loads(decode(response.content))
id1 = res['unique_id']
print(res)
print("Recieved id back")


print("Wait 12 seconds, and then attempt to query the first video")
for i in range(1, 13):
    time.sleep(1)
    print(i)

url = 'http://127.0.0.1:5000/query/' + id1
response = requests.get(url)
res = json.loads(decode(response.content))
print(res)


print("Video is currently processing. Let's add the second video to the queue in the mean time")
url = 'http://127.0.0.1:5000/push'
payload = {
    "source_name": "test2",
    "source_url": "https://storage.googleapis.com/sieve-public-videos/celebrity-videos/obama_interview.mp4"
}
response = requests.post(url, json=payload)
res = json.loads(decode(response.content))
id2 = res['unique_id']
print(res)
print("Recieved id back")

time.sleep(3)
print("Lets see the ids of the all the videos have been submitted. We should be expecting {} and {}".format(id1, id2))
time.sleep(3)
url = 'http://127.0.0.1:5000/list'
response = requests.get(url)
res = json.loads(decode(response.content))
print(res)

time.sleep(4)
print("First video should be done now. Let's query again")
time.sleep(1)
url = 'http://127.0.0.1:5000/query/' + id1
response = requests.get(url)
res = json.loads(decode(response.content))
print(res)


time.sleep(5)
print("What about the second video? Let's use the status endpoint this time to see where the second video is at")

url = 'http://127.0.0.1:5000/query/' + id2
response = requests.get(url)
res = json.loads(decode(response.content))
print(res)

time.sleep(1)

print("It isn't done yet")
print("Lets check back in a minute, because its a larger video")
for i in range(1, 61):
    time.sleep(1)
    print(i)
print("querying...")
time.sleep(2)
url = 'http://127.0.0.1:5000/query/' + id2
response = requests.get(url)
res = json.loads(decode(response.content))
print(res)


