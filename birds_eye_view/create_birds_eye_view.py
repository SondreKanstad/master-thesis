import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation, FFMpegWriter
import numpy as np

f1 = open("../psudo_lidar/predictions_new.json")
boat_pos_preds = json.load(f1)
f1.close()

f2 = open("../simulated_data/ground_truth_3d.json")
boat_pos_truth = json.load(f2)
f2.close()

# f3 = open("../psudo_lidar/tracked_coord_preds.json")
# tracked_coordinate_predictions = json.load(f3)
# f3.close()

f4 = open("../psudo_lidar/predictions_new_id.json")
tracked_coordinate_predictions = json.load(f4)
f4.close()

f5 = open("../psudo_lidar/filtered_tracking.json")
filtered_tracked_coordinate_predictions = json.load(f5)
f5.close()


def plot_fov(ax, max_value, without_zone_3):
    # Highlight the field of view using a pie chart
    # Original fov
    if without_zone_3:
        # FOV without zone 3
        theta_fov = np.linspace(-np.pi/2 + np.deg2rad(180-84.56)/2, np.pi/2 - np.deg2rad(180-84.56)/2, 100)

    else:
        theta_fov = np.linspace(-np.pi/2 + np.deg2rad(180-127)/2, np.pi/2 - np.deg2rad(180-127)/2, 100)

    
    r_fov = np.tan(np.deg2rad(63.5)) * max_value
    x_fov = np.concatenate([[0], r_fov*np.cos(theta_fov), [0]])
    y_fov = np.concatenate([[0], r_fov*np.sin(theta_fov), [0]])
    # Red
    #ax.set_facecolor((1.0, 0.0, 0.0, 0.5))
    #
    ax.set_facecolor("lightgray")
    ax.fill(x_fov, y_fov, alpha=1, color='w')

def format_func(value, tick_number):
            return f"{int(value)} m"

def create_birds_eye_view_for_frame(frame):
    if boat_pos_preds[frame]:
        x_coordinates_pred = [pred[0] for pred in tracked_coordinate_predictions[frame]]
        y_coordinates_pred = [pred[1] for pred in tracked_coordinate_predictions[frame]]

        x_coordinates_gt = [ground_truth[0] for ground_truth in boat_pos_truth[frame]]
        y_coordinates_gt = [ground_truth[1] for ground_truth in boat_pos_truth[frame]]        

        max_value_gt = max(np.max(np.abs(x_coordinates_gt)), np.max(np.abs(y_coordinates_gt)))
        max_value_pred = max(np.max(np.abs(x_coordinates_pred)), np.max(np.abs(y_coordinates_pred)))

        max_value = max(max_value_gt, max_value_pred)

        fig, ax = plt.subplots()

        # Highlight the field of view using a pie chart
        theta_fov = np.linspace(-np.pi/2 + np.deg2rad(180-127)/2, np.pi/2 - np.deg2rad(180-127)/2, 100)
        r_fov = np.tan(np.deg2rad(63.5)) * max_value
        x_fov = np.concatenate([[0], r_fov*np.cos(theta_fov), [0]])
        y_fov = np.concatenate([[0], r_fov*np.sin(theta_fov), [0]])


        ax.set_facecolor((1.0, 0.0, 0.0, 0.5))
        ax.fill(x_fov, y_fov, alpha=1, color='w')

        # Set the formatter function for the x and y axis tick labels
        ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))
        ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_func))

        # Create a scatter plot with limits centered around (0,0)
        plt.xlim(-max_value -10, max_value +10)
        plt.ylim(-max_value -10, max_value +10)

        # Create a scatter plot
        ax.scatter(0, 0, color='black', marker=">", label='Egoship', s=250)

        ax.scatter(x_coordinates_gt, y_coordinates_gt, label='Ground Truths', s=250)

        for index, ground_truth in enumerate(boat_pos_truth[frame]):
            ax.annotate(f"#{index + 1}", xy=(ground_truth[0] - 3, ground_truth[1] - 2), fontsize=9, zorder=1)

        ax.scatter(x_coordinates_pred, y_coordinates_pred, color='orange', label='Predictions', s=250, zorder=2)

        for pred in tracked_coordinate_predictions[frame]:
            ax.annotate(f"#{pred[2]}", xy=(pred[0] - 3, pred[1] - 2), fontsize=9)


        ax.legend(loc='upper left', fontsize=14)

        # Set the title and axis labels
        plt.title('Predictions for frame: ' + str(frame))
        plt.xlabel('')
        plt.ylabel('')
        plt.savefig(f"../../Figures/bev-frame-{frame}", dpi=150)

        # Show the plot
        #plt.show()
        
        return fig, ax
    else:
        print(f"No predictions made for frame: {frame}")


fig, ax = plt.subplots()
def create_birds_eye_view_scatter(frame):
    # Clear scene for animation
    ax.clear()

    # Set the formatter function for the x and y axis tick labels
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_func))
    plt.xlabel('')
    plt.ylabel('')

    x_coordinates_gt = [ground_truth[0] for ground_truth in boat_pos_truth[frame]]
    y_coordinates_gt = [ground_truth[1] for ground_truth in boat_pos_truth[frame]]

    
    #max_value_gt = max(np.max(np.abs(x_coordinates_gt)), np.max(np.abs(y_coordinates_gt)))
    
    max_value = 100
    without_zone_3 = False

    if boat_pos_preds[frame]:
        # Filtered track predictiosn
        if without_zone_3:
            x_coordinates_pred = [pred[0] for pred in filtered_tracked_coordinate_predictions[frame]]
            y_coordinates_pred = [pred[1] for pred in filtered_tracked_coordinate_predictions[frame]]
            plot_fov(ax, max_value=max_value, without_zone_3=without_zone_3)

        # Track predictions with zone 3
        else:
            x_coordinates_pred = [pred[0] for pred in tracked_coordinate_predictions[frame]]
            y_coordinates_pred = [pred[1] for pred in tracked_coordinate_predictions[frame]]
            plot_fov(ax, max_value=max_value, without_zone_3=without_zone_3)
       

        #max_value_pred = max(np.max(np.abs(x_coordinates_pred)), np.max(np.abs(y_coordinates_pred)))
        #max_value = max(max_value_gt, max_value_pred)

        # Create a scatter plot with limits centered around (0,0)
        plt.xlim(-max_value -10, max_value +10)
        plt.ylim(-max_value -10, max_value +10)

        # Create a scatter plot for ego ship and ground truth
        ax.scatter(0, 0, color='black', marker=">", label='Ego-ship', s=250)
        ax.scatter(x_coordinates_gt, y_coordinates_gt, label='Ground truths', s=250)
        for index, ground_truth in enumerate(boat_pos_truth[frame]):
            ax.annotate(f"#{index + 1}", xy=(ground_truth[0] - 4, ground_truth[1] - 3), fontsize=9, zorder=1)

        
        
        if without_zone_3:
            ax.scatter(x_coordinates_pred, y_coordinates_pred, color='darkorange',  s=250) #label='Predictions', s=250)
            for pred in filtered_tracked_coordinate_predictions[frame]:
                ax.annotate(f"#{pred[2]}", xy=(pred[0] - 4, pred[1] - 3), fontsize=9)

        else:
            ax.scatter(x_coordinates_pred, y_coordinates_pred, color='darkorange',s=250) #label='Predictions', s=250)
            for pred in tracked_coordinate_predictions[frame]:
                ax.annotate(f"#{pred[2]}", xy=(pred[0] - 4, pred[1] - 3), fontsize=9)



        ax.scatter(-1000, -1000, color='darkorange', label='Predictions', s=250)
        ax.legend(loc='upper left', fontsize=14)

        # Set the title and axis labels
        plt.title('Predictions for frame: ' + str(frame))
        
        plt.savefig(f"../../Figures/bev-frame-{frame}-with-tracks", dpi=300)
        

        # Show the plot
        #plt.show()
        
        return fig, ax
    else:
        plt.title('No predictions for frame: ' + str(frame))
        plt.xlim(-max_value -10, max_value +10)
        plt.ylim(-max_value -10, max_value +10)
        if without_zone_3:
            plot_fov(ax, max_value=max_value, without_zone_3=without_zone_3)
        else:
            plot_fov(ax, max_value=max_value, without_zone_3=without_zone_3)
        
        ax.scatter(0, 0, color='black', marker=">", label='Ego-ship', s=250)
        ax.scatter(x_coordinates_gt, y_coordinates_gt, label='Ground truths', s=250)
        for index, ground_truth in enumerate(boat_pos_truth[frame]):
            ax.annotate(f"#{index + 1}", xy=(ground_truth[0] - 4, ground_truth[1] - 3), fontsize=9, zorder=1)

        ax.scatter(-1000, -1000, color='darkorange', label='Predictions', s=250)
        ax.legend(loc='upper left', fontsize=14)
        
    
frames = 6000

# Maybe change intervall to 100, generate 10 minute video corresponding to input
#anim = FuncAnimation(fig, create_birds_eye_view_scatter, frames=frames, interval=100)
#anim.save(f'../../Figures/new-tracks-gray-bev-{frames}-frames.gif', writer='pillow')

create_birds_eye_view_scatter(1300)





# Returns paths for all tracks in input
def filter_path_of_tracks(tracked_predictions):
    path_of_tracks = {}
    for index, timeframe in enumerate(tracked_predictions):
        for prediction in timeframe:
            if prediction[2] in path_of_tracks:
                path_of_tracks[prediction[2]]['x'].append(prediction[0])
                path_of_tracks[prediction[2]]['y'].append(prediction[1])
                path_of_tracks[prediction[2]]['timeframe'].append(index)
            else:
                path_of_tracks[prediction[2]] = {'x': [prediction[0]], 'y': [prediction[1]], 'timeframe': [index]}
    return path_of_tracks



# Returns 2d list of length of timeframes and id of track
def sort_tracks_by_length(tracks):
    path_of_tracks = filter_path_of_tracks(tracks)

    longest_tracks = []
    for id, coords in path_of_tracks.items():
        longest_tracks.append([len(coords['x']), id])

    longest_tracks = sorted(longest_tracks, key=lambda l:l[0], reverse=True)
    return longest_tracks


def bev_path_of_tracks(track_coordinate_predictions, track_id, is_pred):
    fig, ax = plt.subplots()

    # Original value used for all plots
    #max_value = 100

    max_value = 60
    plt.xlim(-max_value -10, max_value +10)
    plt.ylim(-max_value -10, max_value +10)


    # Set the formatter function for the x and y axis tick labels
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_func))

    plot_fov(ax, max_value, without_zone_3=True)
    ax.scatter(0, 0, color='black', marker=">", label='Ego-ship', s=250)
    
    # Get paths of all tracks
    path_of_tracks = filter_path_of_tracks(track_coordinate_predictions)

    # Get path of specific track
    coordinates = path_of_tracks[track_id]

    #filtered_coords = filter_outliers_from_tracks(coordinates, 2000)
    #print(filtered_coords)

   

    min_timeframe = min(coordinates['timeframe'])
    max_timeframe = max(coordinates['timeframe'])


    ground_truth_paths = {}
    
    for ground_truth in boat_pos_truth[min_timeframe: max_timeframe]:
        #print(ground_truth)
        for id, boat in enumerate(ground_truth):
            if id in ground_truth_paths:
                ground_truth_paths[id]['x'].append(boat[0])
                ground_truth_paths[id]['y'].append(boat[1])
            else:
                ground_truth_paths[id] = {'x': [boat[0]], 'y': [boat[1]]}

    if is_pred:
        ax.plot(coordinates['x'], coordinates['y'], label=f"Path for track #{track_id if track_id != None else 'None'}", c='darkorange', linewidth=2)
        ax.scatter(coordinates['x'][0], coordinates['y'][0], s=100, c='darkorange')
        ax.scatter(coordinates['x'][-1], coordinates['y'][-1], marker='X', s=100, c='darkorange')

        ax.legend(loc='upper left', fontsize=11)
        plt.title(f'Path of prediction')
        #plt.show()
        plt.savefig(f"../../Figures/path-of-track-{track_id}", dpi=300)

    else:
        # ax.plot(ground_truth_paths[0]['x'], ground_truth_paths[0]['y'], linewidth=2, c='darkgreen', label=f'Path for ship #1')
        # ax.scatter(ground_truth_paths[0]['x'][0], ground_truth_paths[0]['y'][0], s=100, c='blue')
        # ax.scatter(ground_truth_paths[0]['x'][-1], ground_truth_paths[0]['y'][-1], marker='X', s=100, c='blue')

        # ax.plot(ground_truth_paths[1]['x'], ground_truth_paths[1]['y'], linewidth=2, c='blue', label=f'Path for ship #2')
        # ax.scatter(ground_truth_paths[1]['x'][0], ground_truth_paths[1]['y'][0], s=100, c='blue')
        # ax.scatter(ground_truth_paths[1]['x'][-1], ground_truth_paths[1]['y'][-1], marker='X', s=100, c='blue')

        # ax.plot(ground_truth_paths[2]['x'], ground_truth_paths[2]['y'], linewidth=2, c='blue', label=f'Path for ship #3')
        # ax.scatter(ground_truth_paths[2]['x'][0], ground_truth_paths[2]['y'][0], s=100, c='blue')
        # ax.scatter(ground_truth_paths[2]['x'][-1], ground_truth_paths[2]['y'][-1], marker='X', s=100, c='blue')

        # ax.plot(ground_truth_paths[3]['x'], ground_truth_paths[3]['y'], linewidth=2, c='blue', label=f'Path for ship #4')
        # ax.scatter(ground_truth_paths[3]['x'][0], ground_truth_paths[3]['y'][0], s=100, c='blue')
        # ax.scatter(ground_truth_paths[3]['x'][-1], ground_truth_paths[3]['y'][-1], marker='X', s=100, c='blue')
        

        # ax.plot(ground_truth_paths[4]['x'], ground_truth_paths[4]['y'], linewidth=2, c='blue', label=f'Path for ship #5')
        # ax.scatter(ground_truth_paths[4]['x'][0], ground_truth_paths[4]['y'][0], s=100, c='blue')
        # ax.scatter(ground_truth_paths[4]['x'][-1], ground_truth_paths[4]['y'][-1], marker='X', s=100, c='blue')

        ax.legend(loc='upper left', fontsize=11)
        plt.title(f'Path of ground truth')
        #plt.show()
        plt.savefig(f"../../Figures/nearest-ground-truth-path-of-track-{track_id}", dpi=300)



# Only tracking paths of filtered predictions
#bev_path_of_tracks(filtered_tracked_coordinate_predictions, 429, is_pred=True)
