"""Visualization helper functions for CommonRoad.

Authors:
- Maximilian Geisslinger <maximilian.geisslinger@tum.de>
- Matthias Rowold
"""

import os
from commonroad.scenario.trajectory import Trajectory
from commonroad.scenario.scenario import Scenario
from commonroad.prediction.prediction import TrajectoryPrediction
from commonroad.geometry import shape
from commonroad.scenario.obstacle import ObstacleType, DynamicObstacle
from commonroad.visualization.draw_dispatch_cr import draw_object
import numpy as np
import matplotlib
import matplotlib.cm as cm
from matplotlib import animation
import matplotlib.pyplot as plt
from pathlib import Path


def states_to_dynamic_obstacle(states: list, shape: shape, type: ObstacleType, id: int):
    """States to Dynamic Obstacle

    Takes a list of commonroad states and creates a commonroad dynamic obstacle

    :param states: commonroad states
    :param shape: commonroad shape
    :param type: commonroad obstacle type
    :param id: unique ID for the dynamic obstacle
    :return: commonroad dynamic obstacle
    """
    dynamic_obstacle_trajectory = Trajectory(initial_time_step=0, state_list=states)
    dynamic_obstacle_prediction = TrajectoryPrediction(
        trajectory=dynamic_obstacle_trajectory, shape=shape
    )

    dynamic_obstacle = DynamicObstacle(
        obstacle_id=id,
        obstacle_type=type,
        obstacle_shape=shape,
        initial_state=states[0],
        prediction=dynamic_obstacle_prediction,
    )
    return dynamic_obstacle


def get_plot_limits_from_scenario(scenario: Scenario):
    """Plot Limits from Scenario

    Get the x and y plot limits defined by the lanelet network

    :param scenario: commonroad scenario
    :return: plot limits [xmin, xmax, ymin, ymax]
    """
    # Vertices from all lanelets into one array
    lanelet_network = scenario.lanelet_network
    vertices = np.zeros((1, 2))
    for lanelet in lanelet_network.lanelets:
        vertices = np.vstack((vertices, lanelet.left_vertices))
        vertices = np.vstack((vertices, lanelet.right_vertices))
    vertices = vertices[1:, :]
    # Minimum/maximum x and y coordinates
    min_x = min(vertices[:, 0])
    max_x = max(vertices[:, 0])
    min_y = min(vertices[:, 1])
    max_y = max(vertices[:, 1])

    plot_limits = [min_x, max_x, min_y, max_y]
    return plot_limits


def get_max_frames_from_scenario(scenario: Scenario):
    """Max Frames from Scenario

    Get the maximum number of frames (equal to longest trajectory)

    :param scenario: commonroad scenario
    :return: maximum number of frames
    """
    frames = 1
    for dynamic_obstacle in scenario.dynamic_obstacles:
        length = dynamic_obstacle.prediction.trajectory.state_list[-1].time_step + 1
        if frames < length:
            frames = length
    return frames


def animate_scenario(
    scenario: Scenario, fps: int = 30, plot_limits=None, marked_vehicles=None
):
    """Animate Scenario

    Animate a commonroad scenario

    :param scenario: commonroad scenario
    :param fps: frames per second
    :param plot_limits: bounds for the plots
    :return: animation
    """
    if plot_limits is None:
        plot_limits = get_plot_limits_from_scenario(scenario=scenario)
    else:
        plot_limits = plot_limits

    if 1 / fps < scenario.dt:
        fps_available = 1 / scenario.dt
    else:
        fps_available = fps

    trajectory_points = get_max_frames_from_scenario(scenario=scenario)
    frames = int(trajectory_points * scenario.dt * fps_available)

    def animate(j):
        plt.cla()
        draw_object(
            obj=scenario,
            plot_limits=plot_limits,
            draw_params={'time_begin': int(j / (scenario.dt * fps_available))},
        )

        if marked_vehicles is not None:
            color = iter(plt.cm.rainbow(np.linspace(0, 1, len(marked_vehicles))))
            for marked_vehicle in marked_vehicles:
                if marked_vehicle is not None:
                    # mark the ego vehicle
                    draw_object(
                        obj=scenario.obstacle_by_id(marked_vehicle),
                        plot_limits=plot_limits,
                        draw_params={
                            'time_begin': int(j / (scenario.dt * fps_available)),
                            'facecolor': next(color),
                        },
                    )

        plt.gca().set_aspect('equal')

    fig = plt.figure(figsize=(9, 9))
    anim = animation.FuncAnimation(
        fig=fig,
        func=animate,
        frames=frames,
        interval=1 / fps_available * 1000,
        repeat=True,
        repeat_delay=1000,
        blit=False,
    )
    return anim


def save_animation(anim, save_path: str, anim_name: str, dpi=100):
    """Save Animation

    Save an animation as mp4 video

    :param anim: animation
    :param save_path: path to saving directory
    :param anim_name: animation name
    :param dpi: dpi value
    """
    print('----------------\n' 'Saving animation\n' '----------------')

    fps = 1 / anim.event_source.interval * 1000
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=fps, bitrate=1800)

    # create video path if it does not exist
    Path(save_path).mkdir(parents=True, exist_ok=True)

    filename = save_path + '/' + anim_name + '.mp4'
    anim.save(filename=filename, writer=writer, dpi=dpi)


def visualize_timestep(
    scenario,
    time_step,
    traj=None,
    all_traj=None,
    fut_pos_list=None,
    visible_area=None,
    animation_area=80.0,
    save_animation=False,
):

    """This function plots a single time step of a scenario.
    Depending on which arguments are passed, the visualization is extended.

    Arguments:
        scenario {[CommonRoad scenario object]} -- [Commonroad Scenario]
        time_step {[int]} -- [time step for commonroad scenario]

    Keyword Arguments:
        traj {[Trajectory]} -- [Object with coordinates in .x and .y] (default: {None})  #TODO: define final format for trajectories
        all_traj {[List of Trajectories]} -- [List of all possible trajectories ] (default: {None})
        fut_pos_list {[list]} -- [List of x,y coordinates of predicted vehicles] (default: {None})
        visible_area {[shapely polygon object]} -- [Area that is calcluated as visible by the sensor model] (default: {None})
        animation_area {[float]} -- [Shown area of the plot around the ego position]
        save_animation {bool} -- [True if images should be saved] (default: {False})
    """

    if all_traj is not None:
        norm = matplotlib.colors.Normalize(
            vmin=min([all_traj[i].cf for i in range(len(all_traj))]),
            vmax=max([all_traj[i].cf for i in range(len(all_traj))]),
            clip=True,
        )
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.jet)

    # Subplot 1 (Scenario)
    plt.cla()
    draw_object(scenario, draw_params={'time_begin': time_step})
    plt.gca().set_aspect('equal')

    # Draw all possible trajectories with their costs as colors
    if all_traj is not None:
        for p in all_traj:
            plt.plot(
                p.x[1:],
                p.y[1:],
                '-',
                markersize=1,
                color=mapper.to_rgba(p.cf),
                alpha=0.2,
            )

    # Draw planned trajectory
    if traj is not None:
        plt.plot(traj.x[1:], traj.y[1:], "or", markersize=1, zorder=15)
        plt.scatter(traj.x[1], traj.y[1], s=10, color='red', zorder=20)
        # Align ego position to the center
        plt.xlim(traj.x[1] - animation_area, traj.x[1] + animation_area)
        plt.ylim(traj.y[1] - animation_area, traj.y[1] + animation_area)

    # Draw predictions
    if fut_pos_list is not None:
        for fut_pos in fut_pos_list:
            plt.plot(fut_pos[:, 0], fut_pos[:, 1], '.c', markersize=2, alpha=0.8)

    # Draw visible sensor area
    if visible_area is not None:
        if visible_area.geom_type == 'MultiPolygon':
            for geom in visible_area.geoms:
                plt.fill(*geom.exterior.xy, 'g', alpha=0.2, zorder=10)
        elif visible_area.geom_type == 'Polygon':
            plt.fill(*visible_area.exterior.xy, 'g', alpha=0.2, zorder=10)
        else:
            for obj in visible_area:
                if obj.geom_type == 'Polygon':
                    plt.fill(*obj.exterior.xy, 'g', alpha=0.2, zorder=10)

    plt.title('Time: {0:.1f} s'.format(time_step * scenario.dt))

    if save_animation:
        save_path = './out/' + scenario.benchmark_id + '/'
        if not os.path.exists(save_path):
            os.makedirs(save_path)
        plt.savefig(save_path + str(time_step) + '.png')

    plt.pause(0.0001)


def visualize_lanelet_network(scenario: Scenario):
    """Visualize Lanelet Network

    This function visualizes the lanelet network

    :param scenario: commonroad scenario
    """
    for lanelet in scenario.lanelet_network.lanelets:
        x_list = []
        y_list = []
        for p, _ in enumerate(lanelet.center_vertices):
            x_list.append(lanelet.center_vertices[p][0])
            y_list.append(lanelet.center_vertices[p][1])
        plt.plot(x_list, y_list, marker='o')
        plt.text(x_list[0], y_list[0], str(lanelet.lanelet_id))


# EOF
