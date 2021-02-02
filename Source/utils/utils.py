import sys
import numpy as np
import random as rand
from utils import Route_delivery as RD


def edge_in_route(edge, route):

    # this function will check if route use edge i-j or not
    for i, j in [edge, (edge[1], edge[0])]:
        if route.is_visit(i) and route.is_visit(j):
            I_inx = route.where(i)
            if j in route[I_inx].string:
                return 1
            if route[I_inx][-1] == i and route[I_inx+1][0] == j:
                return 1

    return 0


def avoid_edges_penalty(n1, n2, edges2avoid):
    # This function checks if two seq can be placed
    if edges2avoid:
        if n2[0] in edges2avoid.keys():
            if n1[-1] in edges2avoid[n2[0]]:
                return 1
        if n1[-1] in edges2avoid.keys():
            if n2[0] in edges2avoid[n1[-1]]:
                return 1
    return 0


def avoid_check_edge(avoid_list, route):
    # This is a test function to check entire route and see if there is and avoid edge
    new_avoid = avoid_list + [(j, i) for i, j in avoid_list]
    pre_node = route[0]
    for node in route[1:]:
        if (pre_node, node) in new_avoid:
            print(f"Edge {(pre_node, node)} should be avoided but its here \n {route}")
            return 0
        pre_node = node
    return 1


def avoid_check(avoid_dict, route):
    # This is a test function to check entire route and see if there is and avoid edge
    new_avoid = set()
    for key, val in avoid_dict["N"].items():
        for v in val:
            new_avoid.add((key, v))
            new_avoid.add((v, key))

    pre_seq = route[0]
    for seq in route[1:]:
        if (pre_seq[-1], seq[0]) in new_avoid:
            print(f"Edge {(pre_seq, seq)} should be avoided but its here \n {route}")
            return 0
        pre_seq = seq

    return 1


def keep_check(keep_dic, route):

    for n1, n2 in keep_dic["E"]:
        if route.is_visit(n1) and route.is_visit(n2):
            if edge_in_route((n1, n2), route):
                continue
            else:
                print(f"Edge {(n1, n2)} is not in the route \n {route}")
                return 0

        elif route.is_visit(n1) and n1 != 0 and not route.is_visit(n2):
            print(f" Node {n1} is in the route but there is no {n2} in \n {route} ")
            return 0
        elif route.is_visit(n2) and n2 != 0 and not route.is_visit(n1):
            print(f" Node {n2} is in the route but there is no {n1} in \n {route} ")
            return 0
    return 1


def check_branching(col_dic, avoid, keep):

    flag_avoid = 1
    if avoid:
        # print("Start check the list of edges to avoid")
        # print(avoid)
        for r in col_dic.values():
            flag_avoid = flag_avoid * avoid_check(avoid, r)
    if not flag_avoid:
        sys.exit("Avoided edge is used!!!")

    flag_keep = 1
    if keep:
        # print("Start checking the keep edges")
        # print(keep)
        for r in col_dic.values():
            flag_keep = flag_keep * keep_check(keep, r)

    if not flag_keep:
        sys.exit("Keep edge is not used!!!")


def build_the_route(Data, Edges=[], route=[]):
    if Edges:
        PerNode = 0
        route = [0]
        while Edges:
            for e in Edges:
                if PerNode in e:
                    break
            route.append(e[1])
            PerNode = e[1]
            Edges.remove(e)

    if 0 not in route:
        route.insert(0, 0)
        route.append(0)

    seq_route = [Data.All_seq["D0"][-1]]
    if len(Data.All_seq["D0"]) > 1:
        for seq in Data.All_seq["D0"]:
            if route[1] in seq.string:
                seq_route = [seq]

    for node in route[1:-1]:
        if node in seq_route[-1].string:
            continue
        else:
            for key, seq in Data.All_seq.items():
                if isinstance(key, int): 
                    key = [key]
                if node in list(key):
                    if len(seq) > 1:
                        if node == seq[0][0]:
                            seq_route.append(seq[0])
                        else:
                            seq_route.append(seq[1])
                    else:
                        seq_route.append(seq[0])
                    break
    seq_route.append(Data.All_seq["D1"][0])
    New_Route = RD.RouteDel(seq_route)
    if 0 in New_Route.nodes_in_path:
        sys.exit("Find you")
    if route[1:-1] != New_Route.nodes_in_path:
        print("The build route function in column gen is not working correctly")
        print(New_Route.nodes_in_path)
        print(route[1:-1])
    return New_Route, route


def spin(rw):
    slot_count = len(rw)
    randno = rand.randint(0, 10000)
    rot_degree = randno % 360
    rot_unit = 360 / slot_count
    rol_no = (rot_degree - (rot_degree % (rot_unit))) / rot_unit
    rol_value = rw[int(rol_no)]
    return rol_value


def roul_wheel(dic):
    slot_count = 0
    for i in dic.keys():
        slot_count = slot_count + dic[i]

    roulette_wheel = [0] * slot_count
    for key, val in dic.items():
        j = 0
        while j < val:
            t = rand.randint(0, slot_count - 1)
            wheel_alloc = roulette_wheel[t]
            if wheel_alloc == 0:
                roulette_wheel[t] = key
                j = j + 1

    return spin(roulette_wheel)


def Optimize(Data, routes, length):
    optimized_routes = []

    for route in routes:
        if len(route.route) > 1:
            route = TSP_Solver.solve(length, route, start=route[0], end=route[-1])
            Route_object = RD.RouteDel(route, Data, length)
            optimized_routes.append(Route_object)
        else:
            optimized_routes.append(route) # this route is [0] and will be deleted in insertation

    return optimized_routes

global counter0_
