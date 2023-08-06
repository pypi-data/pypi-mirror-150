import math
from math import sqrt, pow

from lib.ga.geometry.point import Point
from lib.ga.scene.obstacle import Obstacle

EPSILON = 0.000001


def segments_intersection(segment_1, segment_2):
    return segments_intersection_p(segment_1[0].x, segment_1[0].y, segment_1[1].x, segment_1[1].y,
                                   segment_2[0].x, segment_2[0].y, segment_2[1].x, segment_2[1].y)


def segments_intersection_p(p0_x, p0_y, p1_x, p1_y, p2_x, p2_y, p3_x, p3_y):
    s1_x = p1_x - p0_x

    # print("s1_y = " + str(p1_y) + " - " + str(p0_y))

    s1_y = p1_y - p0_y
    s2_x = p3_x - p2_x

    # print("s2_y = " + str(p3_y) + " - " + str(p2_y))

    s2_y = p3_y - p2_y

    # print("divisore: " + str(-s2_x) + " * " + str(s1_y) + " + " + str(s1_x) + " * " + str(s2_y))

    # s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / (-s2_x * s1_y + s1_x * s2_y)
    # t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / (-s2_x * s1_y + s1_x * s2_y)

    divisore_1 = -s2_x * s1_y + s1_x * s2_y

    if divisore_1 == 0:
        divisore_1 = EPSILON

    divisore_2 = -s2_x * s1_y + s1_x * s2_y

    if divisore_2 == 0:
        divisore_2 = EPSILON

    s = (-s1_y * (p0_x - p2_x) + s1_x * (p0_y - p2_y)) / divisore_1
    t = ( s2_x * (p0_y - p2_y) - s2_y * (p0_x - p2_x)) / divisore_2

    if s >= 0 and s <= 1 and t >= 0 and t <= 1:
        # Collision detected
        intersection_x = p0_x + (t * s1_x)
        intersection_y = p0_y + (t * s1_y)
        return Point(intersection_x, intersection_y)
    else:
        return None


def distance(point_1, point_2):
    return sqrt(pow((point_2.x - point_1.x), 2) + pow((point_2.y - point_1.y), 2))


def point_to_string(point):
    return "Point(" + str(point.x) + ", " + str(point.y) + ")"


def segment_to_string(segment):
    return "Segment(" + point_to_string(segment[0]) + ", " + point_to_string(segment[1]) + ")"

def detect_nearest_obstacle(obstacles, sensor_ray, p0) :
    min_dst = None
    nearest_obstacle = None

    for obj in obstacles:
        if issubclass(type(obj), Obstacle):
            obstacle = obj

            # check collision between obstacle edges and sensor ray
            # print(obstacle.edges)
            # raise
            for edge in obstacle.edges:
                # print("obstacle_edge:", geom_utils.segment_to_string(obstacle_edge))
                intersection_point = segments_intersection(sensor_ray, edge)

                if intersection_point is not None:
                    # print("intersection_point:", geom_utils.point_to_string(intersection_point))
                    dst = distance(p0, intersection_point)

                    if min_dst is None or dst < min_dst:
                        min_dst = dst
                        nearest_obstacle = obstacle
                        # print("new distance_from_nearest_obstacle:", distance_from_nearest_obstacle)
    return min_dst, nearest_obstacle


def radar_tuple(p0: Point, angle: float, distance: float):
    p1 = Point(
        p0.x + math.cos(angle) * distance,
        p0.y + math.sin(angle) * distance)
    return p0, p1


