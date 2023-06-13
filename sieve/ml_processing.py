import torch
import numpy as np
import pandas as pd
import sys
import json
from sort import *
import cv2

def process_video(url: str) -> list:
    processed = []

    tracker = Sort()
    YOLO = torch.hub.load("ultralytics/yolov5", "yolov5s", pretrained=True)
    video = cv2.VideoCapture(url)

    while True:
        ret, frame = video.read()
        if frame is not None:
   
            results = YOLO(frame)
            detections = np.array(results.xyxy[0])

            if detections.any():
                tracked = tracker.update(detections)
            else:
                tracked = tracker.update()
            
            if tracked.any():
                rows = tracked.shape[0]
                frame_number = np.full((rows, 1), tracker.frame_count)
                tracked = np.append(tracked, frame_number, 1)
                processed.append(tracked)
        else:
            break
       
    video.release()
    cv2.destroyAllWindows()
    return processed

def format(processed: list) -> str:
    data = {}

    stacked = np.concatenate(processed)
    df = pd.DataFrame(stacked, columns = ['x1','y1','x2', 'y2', 'id', 'frame_number'])
    df['index'] = df.index
    df = df.sort_values(by=['id', 'index'])
    df = df.drop('index', axis=1)

    grouped = df.groupby(by="id")
    for id in list(grouped.groups.keys()):
        id_grouped = grouped.get_group(id)
        id_grouped = id_grouped.drop('id', axis=1)
        positions = id_grouped.to_dict(orient='records')
        data[str(id)] = {'positions': positions}

    data = json.dumps(data)
    return data
