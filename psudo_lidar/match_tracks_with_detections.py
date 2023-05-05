import json

def fuse_detections_with_tracks():
    f1 = open("../simulated_data/bounding_boxes_left_10cm_camera_track_id.json")
    left_camera_tracks = json.load(f1)
    f1.close()

    f2 = open("../simulated_data/bounding_boxes_right_10cm_camera_track_id.json")
    right_camera_tracks = json.load(f2)
    f2.close()

    f3 = open("../psudo_lidar/predictions.json")
    coord_preds = json.load(f3)
    f3.close()

    tracked_coord_preds = [[] for i in range(len(coord_preds))]
    
    for timeframe, predictions in enumerate(coord_preds):
            for prediction_index, prediction in enumerate(predictions):
                if prediction_index < len(right_camera_tracks[timeframe]):
                    track = right_camera_tracks[timeframe][prediction_index]
                    prediction.append(track)
                    tracked_coord_preds[timeframe].append(prediction)

    f = open("tracked_coord_preds.json", "w")
    json.dump(tracked_coord_preds, f)
    f.close()

fuse_detections_with_tracks()