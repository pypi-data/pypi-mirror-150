"""Module for plotting the custom vehicle icons to matplotlib.

Author: Simon Sagmeister <simon.sagmeister@tum.de"""
import numpy as np
import matplotlib as mpl

import matplotlib.pyplot as plt

# flake8: noqa:E501


def draw_obstacle(obstacle, time_step, axes=None):
    """Draw a obstacle on a fig, using the custom vehicle type dependent icon.

    Args:
        obstacle (obj): CommonRoad Dynamic Obstacle.
        time_step (int): time_step to draw
        axes (obj, optional): Matplotlib axis object to draw on.
                              Defaults to plt.gca().
    """
    axes = plt.gca() if axes is None else axes

    draw_func_dict = {
        "car": draw_car_icon,
        "truck": draw_truck_icon,
        "bicycle": draw_bicycle_icon,
        "bus": draw_bus_icon,
    }

    obst_type = obstacle.obstacle_type.value
    draw_func = (
        draw_func_dict[obst_type]
        if obst_type in draw_func_dict
        else draw_placeholder_icon
    )

    current_state = obstacle.state_at_time(time_step)
    if current_state is not None:
        patch_list = draw_func(
            pos_x=current_state.position[0],
            pos_y=current_state.position[1],
            orientation=current_state.orientation,
            vehicle_length=obstacle.obstacle_shape.length,
            vehicle_width=obstacle.obstacle_shape.width,
        )
        if patch_list is not None:
            for patch in patch_list:
                axes.add_patch(patch)


def transform_to_global(
    point_array, pos_x, pos_y, orientation, vehicle_length, vehicle_width
):
    """Transform absolute coordinate to car-relative coordinate.

    Args:
        point_array: Shape: (N,2)
        pos_x: -
        pos_y: -
        orientation: -
        vehicle_length: -
        vehicle_width: -

    Returns:
        np_array: transformed absolute coordinate in the form (x,y) (shape: (N,2))
    """
    # Norm the array
    point_array = np.array(point_array)
    point_array = point_array * 0.01
    # Scale it to vehicle dim
    point_array[:, 0] = point_array[:, 0] * vehicle_length
    point_array[:, 1] = point_array[:, 1] * vehicle_width
    # Preprocess current pos
    curr_pos = np.array([pos_x, pos_y])
    curr_pos = curr_pos.reshape(2, 1)
    # Rotate points
    point_array = np.transpose(point_array)
    rot_mat = np.array(
        [
            [np.cos(orientation), -np.sin(orientation)],
            [np.sin(orientation), np.cos(orientation)],
        ]
    )
    point_array = np.matmul(rot_mat, point_array)
    # Translate points
    point_array = point_array + curr_pos
    abs_coord = np.transpose(point_array)
    return abs_coord


def draw_polygon_as_patch(
    vertices,
    zorder=20,
    facecolor="#ffffff",
    edgecolor="#000000",
    line_width=0.5,
    alpha=1.0,
) -> mpl.patches.Patch:
    """Vertices are no closed polygon (first element != last element)."""
    verts = []
    codes = [mpl.path.Path.MOVETO]
    for vert in vertices:
        verts.append(vert)
        codes.append(mpl.path.Path.LINETO)
    del codes[-1]
    codes.append(mpl.path.Path.CLOSEPOLY)
    verts.append((0, 0))

    path = mpl.path.Path(verts, codes)
    patch = mpl.patches.PathPatch(
        path,
        facecolor=facecolor,
        edgecolor=edgecolor,
        lw=line_width,
        zorder=zorder,
        alpha=alpha,
    )

    return patch


def draw_truck_icon(*args, **kwargs):
    """Construct list of elements for the truck."""
    # region Define your points in the norm square (-50<=x<=50, -50<=y<=50)
    # x -> length |  y -> width
    v_trailer = np.array([[-50, -46], [20, -46], [20, 46], [-50, 46]])
    v_driver_cabin = np.array([[25, -42], [50, -42], [50, 42], [25, 42]])
    v_roof = np.array([[25, -34], [44, -34], [44, 34], [25, 34]])
    v_a_col_l = np.array([v_roof[2], v_driver_cabin[2]])
    v_a_col_r = np.array([v_roof[1], v_driver_cabin[1]])
    v_connection = np.array(
        [
            v_trailer[2],
            [v_driver_cabin[3][0], v_driver_cabin[3][1] - 3],
            [v_driver_cabin[0][0], v_driver_cabin[0][1] + 3],
            v_trailer[1],
        ]
    )
    v_mirror_l = np.array([[43, 42], [41, 42], [41, 50], [43, 50]])
    v_mirror_r = np.array([[43, -42], [41, -42], [41, -50], [43, -50]])
    # endregion

    # Transform your coords
    v_trailer = transform_to_global(v_trailer, *args, **kwargs)
    v_driver_cabin = transform_to_global(v_driver_cabin, *args, **kwargs)
    v_roof = transform_to_global(v_roof, *args, **kwargs)
    v_a_col_l = transform_to_global(v_a_col_l, *args, **kwargs)
    v_a_col_r = transform_to_global(v_a_col_r, *args, **kwargs)
    v_connection = transform_to_global(v_connection, *args, **kwargs)
    v_mirror_l = transform_to_global(v_mirror_l, *args, **kwargs)
    v_mirror_r = transform_to_global(v_mirror_r, *args, **kwargs)

    # Create mpl.patches objects.
    p_trailer = draw_polygon_as_patch(v_trailer)
    p_driver_cabin = draw_polygon_as_patch(v_driver_cabin)
    p_roof = draw_polygon_as_patch(v_roof)
    p_a_col_l = draw_polygon_as_patch(v_a_col_l)
    p_a_col_r = draw_polygon_as_patch(v_a_col_r)
    p_connection = draw_polygon_as_patch(v_connection)
    p_mirror_l = draw_polygon_as_patch(v_mirror_l)
    p_mirror_r = draw_polygon_as_patch(v_mirror_r)

    # Create a patch collection
    list_truck = [
        p_trailer,
        p_driver_cabin,
        p_roof,
        p_a_col_l,
        p_a_col_r,
        p_connection,
        p_mirror_l,
        p_mirror_r,
    ]  # Extend the list with your additional patches

    # Return this patch collection
    return list_truck


def draw_placeholder_icon(*args, **kwargs):
    """Draw and return a rectangle if no other icon is available."""
    rect = np.array([[-50, -50], [50, -50], [50, 50], [-50, 50]])

    rect = transform_to_global(rect, *args, **kwargs)

    rect_patch = draw_polygon_as_patch(rect)

    return [rect_patch]


def draw_bus_icon(*args, **kwargs):
    """Draw and return a rectangle if no other icon is available."""
    window_color = "#555555"
    # window_color = "#ffffff"
    line_width = 0.5
    bus_color = "#ffffff"

    outline = np.array([[-50, -50], [50, -50], [50, 50], [-50, 50]])
    front_window = np.array([[47, -42], [50, -46], [50, 46], [47, 42]])
    right_window = np.array([[-20, -50], [-15, -42], [40, -42], [45, -50]])
    left_window = np.array([[-20, 50], [-15, 42], [40, 42], [45, 50]])
    roof_hatch = np.array([[-40, -27], [-15, -27], [-15, 27], [-40, 27]])
    hatch_circles = [[-35, 0], [-27.5, 0], [-20, 0]]
    roof_line = np.array([[-7, -27], [-7, 27]])
    bus_list = [outline, roof_hatch, roof_line]
    window_list = [front_window, right_window, left_window]

    bus_list = [transform_to_global(part, *args, **kwargs) for part in bus_list]
    window_list = [
        transform_to_global(window, *args, **kwargs) for window in window_list
    ]
    hatch_circles = transform_to_global(hatch_circles, *args, **kwargs)

    bus_list_patches = [
        draw_polygon_as_patch(part, facecolor=bus_color, line_width=line_width)
        for part in bus_list
    ]
    window_list_patches = [
        draw_polygon_as_patch(window, facecolor=window_color, line_width=line_width)
        for window in window_list
    ]
    hatch_circle_patches = [
        mpl.patches.Circle(
            point,
            radius=kwargs["vehicle_length"] * 2.5 / 100,
            facecolor=bus_color,
            zorder=20,
            linewidth=line_width,
            edgecolor="black",
        )
        for point in hatch_circles
    ]

    return bus_list_patches + window_list_patches + hatch_circle_patches


def draw_bicycle_icon(*args, **kwargs):
    """Construct list of elements for the bicycle."""

    def elliptic_arc(center, major, minor, start_angle, end_angle):
        """Create the vertices of an elliptic arc."""
        arc = []
        angle_list = np.linspace(start_angle, end_angle, 50)
        for angle in angle_list:
            arc.append(
                [center[0] + major * np.cos(angle), center[1] + minor * np.sin(angle)]
            )

        return np.array(arc)

    # region Define your points in the norm square (-50<=x<=50, -50<=y<=50)
    # x -> length |  y -> width
    v_front_wheel = elliptic_arc((30, 0), 20, 6, 0, 2 * np.pi)
    v_rear_wheel = elliptic_arc((-30, 0), 20, 6, 0, 2 * np.pi)
    v_handlebar = np.array([[18, 50], [16, 50], [16, -50], [18, -50]])
    v_frame = np.array([[18, 3], [18, -3], [-30, -3], [-30, 3]])
    v_body = elliptic_arc((5, 0), 20, 40, np.pi / 2 + 0.2, np.pi * 3 / 2 - 0.2)
    v_arm_r = np.array(
        [
            v_body[-1],
            v_handlebar[3],
            [v_handlebar[3][0], v_handlebar[3][1] + 7.5],
            [v_body[-1][0], v_body[-1][1] + 15],
        ]
    )
    v_arm_l = np.array(
        [
            [v_body[0][0], v_body[0][1] - 15],
            [v_handlebar[0][0], v_handlebar[0][1] - 7.5],
            v_handlebar[0],
            v_body[0],
        ]
    )
    v_body = np.concatenate([v_body, v_arm_r, v_arm_l])
    v_head = elliptic_arc((3, 0), 6, 15, 0, 2 * np.pi)
    # endregion

    # Transform your coords
    v_front_wheel = transform_to_global(v_front_wheel, *args, **kwargs)
    v_rear_wheel = transform_to_global(v_rear_wheel, *args, **kwargs)
    v_handlebar = transform_to_global(v_handlebar, *args, **kwargs)
    v_frame = transform_to_global(v_frame, *args, **kwargs)
    v_body = transform_to_global(v_body, *args, **kwargs)
    v_head = transform_to_global(v_head, *args, **kwargs)

    # Create mpl.patches objects.
    p_front_wheel = draw_polygon_as_patch(v_front_wheel)
    p_rear_wheel = draw_polygon_as_patch(v_rear_wheel)
    p_handlebar = draw_polygon_as_patch(v_handlebar)
    p_frame = draw_polygon_as_patch(v_frame)
    p_body = draw_polygon_as_patch(v_body)
    p_head = draw_polygon_as_patch(v_head)

    # Create a patch collection
    list_bicycle = [p_front_wheel, p_frame, p_rear_wheel, p_handlebar, p_body, p_head]

    # Return this patch collection
    return list_bicycle


def draw_car_icon(*args, **kwargs):
    """Return the patch of a car."""
    window_color = "#555555"
    line_width = 0.5
    car_color = "#ffffff"

    front_window = np.array(
        [
            [-21.36, -38.33],
            [-23.93, -27.66],
            [-24.98, -12.88],
            [-25.28, -0.3],
            [-25.29, -0.3],
            [-25.28, -0.04],
            [-25.29, 0.22],
            [-25.28, 0.22],
            [-24.98, 12.8],
            [-23.93, 27.58],
            [-21.36, 38.24],
            [-14.65, 36.18],
            [-7.64, 33.19],
            [-8.32, 19.16],
            [-8.62, -0.04],
            [-8.32, -19.24],
            [-7.64, -33.27],
            [-14.65, -36.27],
        ]
    )

    rear_window = np.array(
        [
            [37.68, -34.02],
            [26.22, -32.15],
            [27.43, -14.56],
            [27.8, -0.41],
            [27.43, 13.74],
            [26.22, 31.32],
            [37.68, 33.19],
            [40.17, 21.22],
            [41.3, -0.34],
            [40.17, -21.91],
            [40.17, -21.91],
        ]
    )

    left_window = np.array(
        [
            [4.32, -38.7],
            [25.84, -37.76],
            [27.35, -36.27],
            [15.06, -32.71],
            [-0.1, -32.71],
            [-13.6, -37.95],
            [0.84, -38.78],
        ]
    )

    left_mirror = np.array(
        [
            [-12.62, -49.78],
            [-13.3, -50.0],
            [-15.11, -46.63],
            [-16.78, -41.24],
            [-17.23, -39.56],
            [-14.92, -39.45],
            [-14.52, -40.68],
            [-13.97, -41.47],
        ]
    )

    engine_hood = np.array(
        [
            [-21.67, -38.04],
            [-32.98, -34.96],
            [-40.1, -29.77],
            [-46.78, -18.96],
            [-49.04, 2.65],
            [-46.78, 19.35],
            [-40.33, 29.6],
            [-32.98, 35.35],
            [-21.67, 38.44],
        ]
    )

    right_window = np.array(
        [
            [4.32, 38.7],
            [25.84, 37.76],
            [27.35, 36.27],
            [15.06, 32.71],
            [-0.1, 32.71],
            [-13.6, 37.95],
            [0.84, 38.78],
        ]
    )

    right_mirror = np.array(
        [
            [-12.62, 49.78],
            [-13.3, 50.0],
            [-15.11, 46.63],
            [-16.78, 41.24],
            [-17.23, 39.56],
            [-14.92, 39.45],
            [-14.52, 40.68],
            [-13.97, 41.47],
        ]
    )

    outline = np.array(
        [
            [0.78, -45.23],
            [-38.09, -42.38],
            [-45.85, -36.08],
            [-49.16, -15.15],
            [-49.99, 1.79],
            [-50.0, 1.79],
            [-50.0, 2.0],
            [-50.0, 2.22],
            [-49.99, 2.22],
            [-49.16, 14.1],
            [-45.85, 35.03],
            [-38.09, 41.33],
            [0.78, 44.18],
            [30.15, 42.88],
            [44.88, 37.96],
            [47.6, 32.77],
            [49.58, 14.36],
            [50.0, 3.86],
            [50.0, 0.14],
            [49.58, -15.41],
            [47.6, -33.82],
            [44.88, -39.01],
            [30.15, -43.93],
        ]
    )

    windows = [-front_window, -rear_window, -left_window, -right_window]
    car = [-outline, -left_mirror, -right_mirror, -engine_hood]

    windows = [transform_to_global(window, *args, **kwargs) for window in windows]
    car = [transform_to_global(part, *args, **kwargs) for part in car]

    window_patches = [
        draw_polygon_as_patch(window, facecolor=window_color, line_width=line_width)
        for window in windows
    ]
    car_patches = [
        draw_polygon_as_patch(part, facecolor=car_color, line_width=line_width)
        for part in car
    ]

    return car_patches + window_patches


if __name__ == "__main__":
    fig = plt.figure()
    draw_car_icon(0, 0, 0, 2.5, 0)

    debug_truck = draw_truck_icon(
        pos_x=0, pos_y=5, orientation=1, vehicle_length=10, vehicle_width=4
    )
    for element in debug_truck:
        fig.gca().add_patch(element)
    debug_bicycle = draw_bicycle_icon(
        pos_x=-7, pos_y=-3, orientation=2, vehicle_length=10, vehicle_width=4
    )
    for element in debug_bicycle:
        fig.gca().add_patch(element)

    debug_car = draw_car_icon(
        pos_x=-10, pos_y=10, orientation=1, vehicle_length=5, vehicle_width=2
    )
    for element in debug_car:
        fig.gca().add_patch(element)

    debug_bus = draw_bus_icon(
        pos_x=5, pos_y=-8, orientation=-1, vehicle_length=12, vehicle_width=4
    )
    for element in debug_bus:
        fig.gca().add_patch(element)
    # fig.gca().set_xlim(-30, 30)
    # fig.gca().set_ylim(-30, 30)
    fig.gca().axis("equal")
    plt.show()
