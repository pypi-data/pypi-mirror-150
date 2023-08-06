"""Interpolation functions for CommonRoad.

Author: Matthias Rowold <matthias.rowold@tum.de
"""

from commonroad.scenario.trajectory import State, Trajectory
from commonroad.scenario.scenario import Scenario
from commonroad.scenario.obstacle import DynamicObstacle
from commonroad.prediction.prediction import TrajectoryPrediction
from copy import deepcopy
import numpy as np
from commonroad.geometry.shape import Rectangle


def interpolate_trajectory(
    scenario: Scenario,
    trajectory: Trajectory,
    dt_new: float,
    initial_state: State = None,
):
    """Interpolate Trajectory

    Interpolate a commonroad trajectory to a new time step size

    :param scenario: commonroad scenario
    :param trajectory: commonroad trajectory
    :param dt_new: new time step size
    :return: new commonroad trajectory with new time vector
    """
    max_time = trajectory.state_list[-1].time_step * scenario.dt
    time_vector_previous = np.arange(0.0, max_time + scenario.dt, scenario.dt)
    time_vector_new = np.arange(dt_new, max_time, dt_new)
    state_list_interp = []

    time_step = 1
    for t in time_vector_new:
        idx = np.searchsorted(a=time_vector_previous, v=t)
        time_factor = (t - time_vector_previous[idx - 1]) / (
            time_vector_previous[idx] - time_vector_previous[idx - 1]
        )
        if t < scenario.dt and initial_state is not None:
            # interpolation between initial state and first state of the trajectory
            # the initial state is not part of the trajectory in a commonroad dynamic obstacles
            state1 = initial_state
            state2 = trajectory.state_list[idx - 1]
        else:
            # interpolation between states of the trajectory
            state1 = trajectory.state_list[idx - 2]
            state2 = trajectory.state_list[idx - 1]

        state_interp = interpolate_state(
            state1=state1, state2=state2, time_factor=time_factor
        )

        # new time step
        state_interp.time_step = time_step
        time_step = time_step + 1

        state_list_interp.append(state_interp)

    trajectory_interp = Trajectory(initial_time_step=1, state_list=state_list_interp)

    return trajectory_interp


def interpolate_state(state1: State, state2: State, time_factor: float):
    """Interpolate State

    Linear interpolation between two commonroad states

    :param state1: commonroad state
    :param state2: commonroad state
    :param time_factor: weighting factor for the states between 0 and 1. 0 equals state 1, 1 equals state 2
    :return: interpolated commonroad state
    """
    state = State()
    for slot in State.__slots__:
        if hasattr(state1, slot) and hasattr(state2, slot):
            state.__setattr__(
                slot,
                state1.__getattribute__(slot)
                + (state2.__getattribute__(slot) - state1.__getattribute__(slot))
                * time_factor,
            )

    return state


def interpolate_scenario(scenario: Scenario, dt_new: float):
    """Interpolate Scenario

    Interpolate all dynamic obstacles in a scenario to a new time step size and return a new scenario

    :param scenario: commonroad scenario
    :param dt_new: new time step size
    :return: new commonroad scenario
    """
    if dt_new == scenario.dt:
        return scenario
    else:
        print('----------------------\n' 'Interpolating scenario')

        scenario_new = deepcopy(scenario)
        scenario_new.dt = dt_new

        for dynamic_obstacle in scenario.dynamic_obstacles:
            if not isinstance(dynamic_obstacle.prediction, TrajectoryPrediction):
                raise TypeError(
                    'Interpolation for other than TrajectoryPrediction is not supported yet!'
                    'You have two options: Implement the interpolation for other commonroad prediction'
                    'methods or do not change the step size.'
                )
            else:
                new_trajectory = interpolate_trajectory(
                    scenario=scenario,
                    trajectory=dynamic_obstacle.prediction.trajectory,
                    dt_new=dt_new,
                    initial_state=dynamic_obstacle.initial_state,
                )

                # initial lanelet assignment for center and shape
                center_lanelet_assignment = {
                    0: set(
                        scenario_new.lanelet_network.find_lanelet_by_position(
                            [dynamic_obstacle.initial_state.position]
                        )[0]
                    )
                }
                shape_lanelet_assignment = {
                    0: set(
                        scenario_new.lanelet_network.find_lanelet_by_shape(
                            dynamic_obstacle.occupancy_at_time(0).shape
                        )
                    )
                }

                for time_step in range(1, len(new_trajectory.state_list)):
                    # assign center position to lanelets
                    center_lanelet_assignment[time_step] = set(
                        scenario_new.lanelet_network.find_lanelet_by_position(
                            [new_trajectory.state_list[time_step - 1].position]
                        )[0]
                    )

                    # shape at time step
                    # TODO: Support for other shapes than rectangle
                    shape = Rectangle(
                        length=dynamic_obstacle.obstacle_shape.length,
                        width=dynamic_obstacle.obstacle_shape.width,
                        center=new_trajectory.state_list[time_step - 1].position,
                        orientation=new_trajectory.state_list[
                            time_step - 1
                        ].orientation,
                    )

                    # assign to lanelet
                    shape_lanelet_assignment[time_step] = set(
                        scenario_new.lanelet_network.find_lanelet_by_shape(shape)
                    )

                new_prediction = TrajectoryPrediction(
                    trajectory=new_trajectory,
                    shape=dynamic_obstacle.prediction.shape,
                    center_lanelet_assignment=center_lanelet_assignment,
                    shape_lanelet_assignment=shape_lanelet_assignment,
                )

                new_dynamic_obstacle = DynamicObstacle(
                    obstacle_id=dynamic_obstacle.obstacle_id,
                    obstacle_type=dynamic_obstacle.obstacle_type,
                    obstacle_shape=dynamic_obstacle.obstacle_shape,
                    initial_state=dynamic_obstacle.initial_state,
                    prediction=new_prediction,
                    initial_center_lanelet_ids=dynamic_obstacle.initial_center_lanelet_ids,
                    initial_shape_lanelet_ids=dynamic_obstacle.initial_shape_lanelet_ids,
                    initial_signal_state=dynamic_obstacle.initial_signal_state,
                    signal_series=[],
                )

                scenario_new.remove_obstacle(dynamic_obstacle)
                scenario_new.add_objects(new_dynamic_obstacle)

        print('... finished \n', '----------------------')
        return scenario_new


# EOF
