"""Spacial helper functions for CommonRoad.

Author: Matthias Rowold <matthias.rowold@tum.de
"""


from commonroad.scenario.scenario import Scenario, Lanelet
from commonroad.scenario.lanelet import LaneletType, LaneletNetwork
import numpy as np
import math
import networkx as nx
import os
import sys

module_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(module_path)

from commonroad_helper_functions.utils.cubicspline import CubicSpline2D


def get_left_lanelet(scenario: Scenario, ego_obstacle_id: int, time_step: int):
    """Get Left Lanelet

    Find the ID of the lanelet to the left of the ego vehicle

    :param scenario: commonroad scenario
    :param ego_obstacle_id: obstacle ID of the considered obstacle (ego vehicle) of which to find the left lane
    :param time_step: scenario time step
    :return: ID of the left lanelet if it is valid (must exist and have the same direction)
    """
    ego_vehicle = scenario.obstacle_by_id(ego_obstacle_id)

    # current lanelet of the ego vehicle
    if time_step > 0:
        ego_lanelet_id = scenario.lanelet_network.find_lanelet_by_position(
            [ego_vehicle.prediction.trajectory.state_list[time_step - 1].position]
        )[0][0]
    else:
        # initial state
        ego_lanelet_id = scenario.lanelet_network.find_lanelet_by_position(
            [ego_vehicle.initial_state.position]
        )[0][0]

    ego_lanelet = scenario.lanelet_network.find_lanelet_by_id(ego_lanelet_id)

    if ego_lanelet.adj_left is not None and ego_lanelet.adj_left_same_direction is True:
        left_lanelet_id = ego_lanelet.adj_left
        return left_lanelet_id
    else:
        return None


def get_right_lanelet(scenario: Scenario, ego_obstacle_id: int, time_step: int):
    """Get Right Lanelet

    Find the ID of the lanelet to the right of the ego vehicle

    :param scenario: commonroad scenario
    :param ego_obstacle_id: obstacle ID of the considered obstacle (ego vehicle) of which to find the right lane
    :param time_step: scenario time step
    :return: ID of the right lanelet if it is valid (must exist and have the same direction)
    """
    ego_vehicle = scenario.obstacle_by_id(ego_obstacle_id)

    # current lanelet of the ego vehicle
    if time_step > 0:
        ego_lanelet_id = scenario.lanelet_network.find_lanelet_by_position(
            [ego_vehicle.prediction.trajectory.state_list[time_step - 1].position]
        )[0][0]
    else:
        # initial state
        ego_lanelet_id = scenario.lanelet_network.find_lanelet_by_position(
            [ego_vehicle.initial_state.position]
        )[0][0]

    ego_lanelet = scenario.lanelet_network.find_lanelet_by_id(ego_lanelet_id)

    if (
        ego_lanelet.adj_right is not None
        and ego_lanelet.adj_right_same_direction is True
    ):
        right_lanelet_id = ego_lanelet.adj_right
        return right_lanelet_id
    else:
        return None


def get_leader_on_lanelet(
    scenario: Scenario, ego_obstacle_id: int, leader_lanelet_id: int, time_step: int
):
    """Get Leader on Lanelet

    Find the ID of the next leading obstacle on a specified lanelet

    :param scenario: commonroad scenario
    :param ego_obstacle_id: obstacle id of the considered obstacle (ego vehicle) of which to find the leader
    :param leader_lanelet_id: lanelet ID of the lanelet to search for a leader
    :param time_step: scenario time step
    :return: ID of the leading obstacle, distance to leader, approaching rate to leader
    """
    ego_vehicle = scenario.obstacle_by_id(ego_obstacle_id)

    leader_lanelet = scenario.lanelet_network.find_lanelet_by_id(leader_lanelet_id)

    # get all merged lanelets by extending the leader lanelet with all possible successors
    lanelets_merged = Lanelet.all_lanelets_by_merging_successors_from_lanelet(
        lanelet=leader_lanelet, network=scenario.lanelet_network
    )
    if len(lanelets_merged[0]) == 0:
        lanelet_merged_list = [leader_lanelet]
    else:
        lanelet_merged_list = lanelets_merged[0]

    distance = 1000
    leader_id = None

    # TODO: Do  not go through all possible merged lanelets but rather only the merged lanelet that corresponds
    #  to the global path of the agent
    for lanelet_merged in lanelet_merged_list:
        # approximate center lane with a cubic spline
        lanelet_spline = lanelet2spline(lanelet=lanelet_merged)

        ego_arclength = lanelet_spline.get_min_arc_length(
            ego_vehicle.prediction.trajectory.state_list[time_step - 1].position
        )[0]

        # dynamic obstacles on the same merged lanelet
        obstacle_ids_in_lanelet = lanelet_merged.dynamic_obstacle_by_time_step(
            time_step
        )

        # remove ego vehicle
        obstacle_ids_candidates = [
            obs_id for obs_id in obstacle_ids_in_lanelet if (obs_id != ego_obstacle_id)
        ]

        if len(obstacle_ids_candidates) == 0:
            # return None if no other obstacles on the same lane
            return None, None, None

        # list of distances along the lanelet spline
        if time_step > 0:
            # TODO: include lengths of the vehicles
            dist = [
                lanelet_spline.get_min_arc_length(
                    scenario.obstacle_by_id(obs_id)
                    .prediction.trajectory.state_list[time_step - 1]
                    .position
                )[0]
                - ego_arclength
                for obs_id in obstacle_ids_candidates
            ]
        else:
            # TODO: include lengths of the vehicles
            dist = [
                lanelet_spline.get_min_arc_length(
                    scenario.obstacle_by_id(obs_id).initial_state.position
                )[0]
                - ego_arclength
                for obs_id in obstacle_ids_candidates
            ]

        # get the index of the smallest distance >0 (< 0 would be the first follower)
        dist_positive = [d for d in dist if d > 0]
        dist_positive_idx = [idx for idx, d in enumerate(dist) if d > 0]

        if len(dist_positive) > 0:
            idx = np.argmin(dist_positive)
            dist_temp = dist_positive[idx]

            if dist_temp < distance:
                # new smallest distance
                distance = dist_temp
                # leader_id
                leader_id = obstacle_ids_candidates[dist_positive_idx[idx]]

    if leader_id is not None:
        # calculate the approaching rate
        if time_step > 0:
            approaching_rate = (
                ego_vehicle.prediction.trajectory.state_list[time_step - 1].velocity
                - scenario.obstacle_by_id(leader_id)
                .prediction.trajectory.state_list[time_step - 1]
                .velocity
            )
        else:
            approaching_rate = (
                ego_vehicle.initial_state.velocity
                - scenario.obstacle_by_id(leader_id).initial_state.velocity
            )

        # return the leader id and the distance and approaching rate
        return leader_id, distance, approaching_rate
    else:
        # no leader in the current lanelet
        return None, None, None


def get_follower_on_lanelet(
    scenario: Scenario, ego_obstacle_id: int, follower_lanelet_id: int, time_step: int
):
    """Get Follower on Lanelet

    Find the ID of the next following obstacle on a specified lanelet

    :param scenario: commonroad scenario
    :param ego_obstacle_id: obstacle ID of the considered obstacle (ego vehicle) of which to find the follower
    :param follower_lanelet_id: lanelet ID of the lanelet to search for a follower
    :param time_step: scenario time step
    :return: ID of the following obstacle, distance to follower, approaching rate to follower
    """
    ego_vehicle = scenario.obstacle_by_id(ego_obstacle_id)

    follower_lanelet = scenario.lanelet_network.find_lanelet_by_id(follower_lanelet_id)

    # get all possible predecessors by connecting the ego lanelet with all possible predecessors
    lanelets_merged = all_lanelets_by_merging_predecessors_from_lanelet(
        lanelet=follower_lanelet, network=scenario.lanelet_network
    )
    if len(lanelets_merged[0]) == 0:
        lanelet_merged_list = [follower_lanelet]
    else:
        lanelet_merged_list = lanelets_merged[0]

    distance = -1000
    follower_id = None

    for lanelet_merged in lanelet_merged_list:
        # approximate center lane with a cubic spline
        lanelet_spline = lanelet2spline(lanelet=lanelet_merged)

        ego_arclength = lanelet_spline.get_min_arc_length(
            ego_vehicle.prediction.trajectory.state_list[time_step - 1].position
        )[0]

        # dynamic obstacles on the same merged lanelet
        obstacle_ids_in_lanelet = lanelet_merged.dynamic_obstacle_by_time_step(
            time_step
        )

        # remove ego vehicle
        obstacle_ids_candidates = [
            obs_id for obs_id in obstacle_ids_in_lanelet if (obs_id != ego_obstacle_id)
        ]

        if len(obstacle_ids_candidates) == 0:
            # return None if no other obstacles on the same lane
            return None, None, None

        # list of distances along the lanelet spline
        if time_step > 0:
            # TODO: include lengths of the vehicles
            dist = [
                lanelet_spline.get_min_arc_length(
                    scenario.obstacle_by_id(obs_id)
                    .prediction.trajectory.state_list[time_step - 1]
                    .position
                )[0]
                - ego_arclength
                for obs_id in obstacle_ids_candidates
            ]
        else:
            # TODO: include lengths of the vehicles
            dist = [
                lanelet_spline.get_min_arc_length(
                    scenario.obstacle_by_id(obs_id).initial_state.position
                )[0]
                - ego_arclength
                for obs_id in obstacle_ids_candidates
            ]

        # get the index of the smallest distance < 0 (> 0 would be the first leader)
        dist_negative = [d for d in dist if d < 0]
        dist_negative_idx = [idx for idx, d in enumerate(dist) if d < 0]

        if len(dist_negative) > 0:
            idx = np.argmax(dist_negative)
            dist_temp = dist_negative[idx]

            if dist_temp > distance:
                # new smallest distance
                distance = dist_temp
                # follower_id
                follower_id = obstacle_ids_candidates[dist_negative_idx[idx]]

    if follower_id is not None:
        # calculate the approaching rate
        if time_step > 0:
            approaching_rate = (
                scenario.obstacle_by_id(follower_id)
                .prediction.trajectory.state_list[time_step - 1]
                .velocity
                - ego_vehicle.prediction.trajectory.state_list[time_step - 1].velocity
            )
        else:
            approaching_rate = (
                scenario.obstacle_by_id(follower_id).initial_state.velocity
                - ego_vehicle.initial_state.velocity
            )

        # return the follower id and the distance and approaching rate
        return follower_id, distance, approaching_rate
    else:
        # no follower in the current lanelet
        return None, None, None


def all_lanelets_by_merging_predecessors_from_lanelet(
    lanelet: 'Lanelet',
    network: 'LaneletNetwork',
    max_length: float = 150.0,
    lanelet_type: LaneletType = None,
):
    """
    Computes all preceding lanelets ending up in a provided lanelet and merges them to a single lanelet for each route.

    :param lanelet: The lanelet to start from
    :param network: The network which contains all lanelets
    :param max_length: maxmimal length of merged lanelets can be provided
    :param lanelet_type: allowed type of lanelets which should be merged
    :return: List of merged lanelets, Lists of lanelet ids of which each merged lanelet consists
    """
    assert isinstance(
        lanelet, Lanelet
    ), '<Lanelet>: provided lanelet is not a valid Lanelet!'
    assert isinstance(
        network, LaneletNetwork
    ), '<Lanelet>: provided lanelet network is not a valid lanelet network!'
    assert (
        network.find_lanelet_by_id(lanelet.lanelet_id) is not None
    ), '<Lanelet>: lanelet not contained in network!'

    if lanelet.predecessor is None or len(lanelet.predecessor) == 0:
        return [], []

    # Create Graph from network
    Net = nx.DiGraph()
    lanelets = network._lanelets.values()
    leafs = list()
    for elements in lanelets:
        Net.add_node(elements)
        if elements.predecessor and lanelet.lanelet_id not in elements.predecessor:
            for predecessors in elements.predecessor:
                predecessor = network.find_lanelet_by_id(predecessors)
                if lanelet_type is None or lanelet_type in predecessor.lanelet_type:
                    Net.add_edge(elements, predecessor)
        # Find leave Nodes
        else:
            leafs.append(elements)

    merge_jobs = list()

    # Get start node for search
    start = network.find_lanelet_by_id(lanelet.lanelet_id)

    # Calculate all paths (i.e. id sequences) to leaf nodes
    for leaf in leafs:
        path = nx.all_simple_paths(Net, start, leaf)
        path = list(path)
        if len(path) < 2 and len(path) > 0:
            merge_jobs.append(path)
        else:
            for i in range(len(path)):
                merge_jobs.append([path[i]])

    # Create merged lanelets from paths
    merged_lanelets = list()
    merge_jobs_final = []
    for i in range(len(merge_jobs)):
        for j in merge_jobs[i]:
            pred = j[0]
            tmp_length = 0.0
            merge_jobs_tmp = [pred.lanelet_id]
            for k in range(1, len(j)):
                j[k].successor.append(pred.lanelet_id)
                merge_jobs_tmp.append(j[k].lanelet_id)

                if k > 0:
                    # do not consider length of inital lanelet for conservativeness
                    tmp_length += j[k].distance[-1]

                pred = Lanelet.merge_lanelets(pred, j[k])
                if tmp_length >= max_length:
                    break

            merge_jobs_final.append(merge_jobs_tmp)
        merged_lanelets.append(pred)

    return merged_lanelets, merge_jobs_final


def lanelet2spline(lanelet: Lanelet):
    """Lanelet to Spline

    Approximate the center line of a lanelet with a cubic spline

    :param lanelet: commonroad lanelet
    :return: cubic spline
    """
    center_points = lanelet.center_vertices
    lanelet_spline = CubicSpline2D(center_points[:, 0], center_points[:, 1])

    return lanelet_spline


def get_closest_lanelet_to_position(
    scenario: Scenario,
    position: np.ndarray,
    use_lanelet_ids: list = None,
    not_use_lanelets: list = [],
):
    """Closest lanelet to position
    :param scenario: commonroad scenario
    :param position: position 2x1 array
    :param use_lanelet_ids:
    :param not_use_lanelets:
    :return: ID of the closest lanelet to the positioin
    """
    lanelet_list = scenario.lanelet_network.lanelets
    min_dist = math.inf
    lanelet_id = None
    for lanelet in lanelet_list:
        if lanelet.lanelet_id in not_use_lanelets:
            continue
        if use_lanelet_ids is None or lanelet.lanelet_id in use_lanelet_ids:
            for center_point in lanelet.center_vertices:
                curr_dist = get_distance_2D(position, center_point)
                if curr_dist < min_dist:
                    min_dist = curr_dist
                    lanelet_id = lanelet.lanelet_id

    return lanelet_id


def get_distance_2D(p1, p2):
    return math.sqrt(((p1[0] - p2[0]) ** 2) + ((p1[1] - p2[1]) ** 2))


def point_in_rectangle(r1, r2, p):
    bottom_left = [min(r1[0], r2[0]), min(r1[1], r2[1])]
    top_right = [max(r1[0], r2[0]), max(r1[1], r2[1])]

    if (
        p[0] > bottom_left[0]
        and p[0] < top_right[0]
        and p[1] > bottom_left[1]
        and p[1] < top_right[1]
    ):
        return True
    else:
        return False


# EOF
