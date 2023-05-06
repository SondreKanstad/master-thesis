import json
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from matplotlib.animation import FuncAnimation
import numpy as np

f1 = open("../psudo_lidar/predictions_new.json")
boat_pos_preds = json.load(f1)
f1.close()

f2 = open("../simulated_data/ground_truth_3d.json")
boat_pos_truth = json.load(f2)
f2.close()

f3 = open("../psudo_lidar/tracked_coord_preds.json")
tracked_coordinate_predictions = json.load(f3)
f3.close()

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

        def format_func(value, tick_number):
            return f"{int(value)} m"

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
        #plt.savefig(f"../../Figures/bev-frame-{frame}-with-track", dpi=150)

        # Show the plot
        plt.show()
        
        return fig, ax
    else:
        print(f"No predictions made for frame: {frame}")


fig, ax = plt.subplots()
def create_birds_eye_view_scatter(frame):
    # Clear scene for animation
    ax.clear()

    def format_func(value, tick_number):
        return f"{int(value)} m"

    # Set the formatter function for the x and y axis tick labels
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_func))
    ax.yaxis.set_major_formatter(ticker.FuncFormatter(format_func))
    plt.xlabel('')
    plt.ylabel('')

    x_coordinates_gt = [ground_truth[0] for ground_truth in boat_pos_truth[frame]]
    y_coordinates_gt = [ground_truth[1] for ground_truth in boat_pos_truth[frame]]

    
    #max_value_gt = max(np.max(np.abs(x_coordinates_gt)), np.max(np.abs(y_coordinates_gt)))
    max_value = 100

    if boat_pos_preds[frame]:
        x_coordinates_pred = [pred[0] for pred in tracked_coordinate_predictions[frame]]
        y_coordinates_pred = [pred[1] for pred in tracked_coordinate_predictions[frame]]

        #max_value_pred = max(np.max(np.abs(x_coordinates_pred)), np.max(np.abs(y_coordinates_pred)))
        #max_value = max(max_value_gt, max_value_pred)

        # Highlight the field of view using a pie chart
        theta_fov = np.linspace(-np.pi/2 + np.deg2rad(180-127)/2, np.pi/2 - np.deg2rad(180-127)/2, 100)
        r_fov = np.tan(np.deg2rad(63.5)) * max_value
        x_fov = np.concatenate([[0], r_fov*np.cos(theta_fov), [0]])
        y_fov = np.concatenate([[0], r_fov*np.sin(theta_fov), [0]])

        ax.set_facecolor((1.0, 0.0, 0.0, 0.5))
        ax.fill(x_fov, y_fov, alpha=1, color='w')

        # Create a scatter plot with limits centered around (0,0)
        plt.xlim(-max_value -10, max_value +10)
        plt.ylim(-max_value -10, max_value +10)

        # Create a scatter plot for ego ship and ground truth
        ax.scatter(0, 0, color='black', marker=">", label='Egoship', s=250)
        ax.scatter(x_coordinates_gt, y_coordinates_gt, label='Ground Truths', s=250)
        for index, ground_truth in enumerate(boat_pos_truth[frame]):
            ax.annotate(f"#{index + 1}", xy=(ground_truth[0] - 4, ground_truth[1] - 3), fontsize=9, zorder=1)

        ax.scatter(x_coordinates_pred, y_coordinates_pred, color='orange', label='Predictions', s=250)
        for pred in tracked_coordinate_predictions[frame]:
            ax.annotate(f"#{pred[2]}", xy=(pred[0] - 4, pred[1] - 3), fontsize=9)

        ax.legend(loc='upper left', fontsize=14)

        # Set the title and axis labels
        plt.title('Predictions for frame: ' + str(frame))
        
        #plt.savefig(f"../../Figures/bev-frame-{frame}", dpi=150)

        # Show the plot
        #plt.show()
        
        #return fig, ax
    else:
        plt.title('No predictions for frame: ' + str(frame))
        plt.xlim(-max_value -10, max_value +10)
        plt.ylim(-max_value -10, max_value +10)

        # Highlight the field of view using a pie chart
        theta_fov = np.linspace(-np.pi/2 + np.deg2rad(180-127)/2, np.pi/2 - np.deg2rad(180-127)/2, 100)
        r_fov = np.tan(np.deg2rad(63.5)) * max_value
        x_fov = np.concatenate([[0], r_fov*np.cos(theta_fov), [0]])
        y_fov = np.concatenate([[0], r_fov*np.sin(theta_fov), [0]])
        ax.set_facecolor((1.0, 0.0, 0.0, 0.5))
        ax.fill(x_fov, y_fov, alpha=1, color='w')
        ax.scatter(0, 0, color='black', marker=">", label='Egoship', s=250)
        ax.scatter(x_coordinates_gt, y_coordinates_gt, label='Ground Truths', s=250)
        for index, ground_truth in enumerate(boat_pos_truth[frame]):
            ax.annotate(f"#{index + 1}", xy=(ground_truth[0] - 4, ground_truth[1] - 3), fontsize=9, zorder=1)
        ax.legend(loc='upper left', fontsize=14)
        
    
#create_birds_eye_view_for_frame(1300)

frames = 6000

anim = FuncAnimation(fig, create_birds_eye_view_scatter, frames=frames, interval=75)
anim.save(f'../../Figures/bev-{frames}-frames.gif', writer='pillow')