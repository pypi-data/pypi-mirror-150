"""Collision checking helpers for CommonRoad.

Author: Levent Ögretmen <levent.oegretmen@tum.de
"""

# Standard imports
import os
import sys

# Third-party imports
from commonroad.common.file_reader import CommonRoadFileReader
from matplotlib import pyplot as plt

module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(module_path)

from commonroad_helper_functions.spacial import get_distance_2D


def collision_check(scenario, time_step, plot_circles=False):
    """Checks all obstacles in the scenario for collisions at specific time step.

    :param scenario: commonroad scenario
    :param time_step: time step of commonroad scenario
    :param plot_circles: True if circles which approximate obstacles should be plotted
    :return: True if collision happened
    :return: List of collided obstacle ids
    """
    # Add radius to every obstacle
    obstacles = scenario.obstacles
    radiuses = [_get_obstacle_radius(obstacle) for obstacle in obstacles]
    obstacles_with_radius = list(map(list, zip(obstacles, radiuses)))

    # Plot circles when flag is set
    if plot_circles:
        _plot_circles(obstacles_with_radius, time_step)

    collision = False
    collided_ids = []
    # Check every combination of obstacles for collision
    for i in range(len(obstacles_with_radius)):
        for j in range(i + 1, len(obstacles_with_radius)):
            obstacle1 = obstacles_with_radius[i][0]
            obstacle2 = obstacles_with_radius[j][0]
            if (len(obstacle1.prediction.trajectory.state_list) < time_step) or (
                len(obstacle2.prediction.trajectory.state_list) < time_step
            ):
                break
            r1 = obstacles_with_radius[i][1]
            r2 = obstacles_with_radius[j][1]
            check = _check_for_collision(obstacle1, obstacle2, r1, r2, time_step)
            if check:
                collision = True
                collided_ids.append([obstacle1.obstacle_id, obstacle2.obstacle_id])
                print(
                    f'At timestep {time_step} is a collision between Obstacle {obstacle1.obstacle_id} and {obstacle2.obstacle_id}.'
                )
    return collision, collided_ids


def _get_obstacle_radius(obstacle):
    """Returns radius in m of circle which under approximates the obstacle #TODO: Add radius for pedestrians"""
    try:
        min_side = min(obstacle.obstacle_shape.length, obstacle.obstacle_shape.width)
    except AttributeError:
        print(
            f"Collision checks are not supported for obstacles of type {obstacle.obstacle_type.name}"
        )
    return min_side / 2


def _check_for_collision(obstacle1, obstacle2, r1, r2, time_step):
    """Returns True if there is a collision between two obstacles at specific time step"""
    p1 = _get_obstacle_position(obstacle1, time_step)
    p2 = _get_obstacle_position(obstacle2, time_step)
    distance = get_distance_2D(p1, p2)
    return distance < r1 + r2


def _get_obstacle_position(obstacle, time_step):
    """Returns position of obstacle for specific time step"""
    if time_step == 0 or obstacle.obstacle_role.name == 'STATIC':
        p = obstacle.initial_state.position
    else:
        p = obstacle.prediction.trajectory.state_list[time_step - 1].position
    return p


def _plot_circles(obstacles_with_radius, time_step):
    """Plots circle approximation"""
    for obstacle_with_radius in obstacles_with_radius:
        position = _get_obstacle_position(obstacle_with_radius[0], time_step)
        radius = obstacle_with_radius[1]
        circle = plt.Circle(position, radius, color='r', zorder=20, fill=False)
        ax.add_artist(circle)
    return


if __name__ == '__main__':
    from commonroad.visualization.draw_dispatch_cr import draw_object

    # scenario_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
    #                             '../../commonroad-scenarios/scenarios/hand-crafted/DEU_Muc-2_1_T-1.xml')
    scenario_path = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        '../../commonroad-scenarios/scenarios/THI-Bicycle/RUS_Bicycle-10_1_T-1.xml',
    )

    scenario, planning_problem_set = CommonRoadFileReader(scenario_path).open()

    for i in range(0, 10):
        fig = plt.figure(figsize=(15, 5))
        ax = fig.gca()
        draw_object(scenario, draw_params={'time_begin': i})
        draw_object(planning_problem_set)
        plt.gca().set_aspect('equal')
        collision, collided_ids = collision_check(
            scenario, i, plot_circles=True
        )  # Do collision check
        plt.show()
