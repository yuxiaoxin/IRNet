# Copyright (c) Microsoft Corporation.
# Licensed under the MIT license.

# -*- coding: utf-8 -*-
"""
# @Time    : 2019/5/25
# @Author  : Jiaqi&Zecheng
# @File    : utils.py
# @Software: PyCharm
"""
# collections用来自定义一些集合，deque是便于修改的元组namedtuple是可以自己命名的元组
from collections import deque, namedtuple


# we'll use infinity as a default distance to nodes.
inf = float('inf')
#namedtuple里的Edge是自定义的集合的名字，后面三个是元组的三个元素，
Edge = namedtuple('Edge', 'start, end, cost')

#创建边集，有边则距离都为1，为了使用迪杰斯特拉算法
def make_edge(start, end, cost=1):
    return Edge(start, end, cost)


class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        # edges里的边长度只能是2或3
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))

        self.edges = [make_edge(*edge) for edge in edges]
    
    #@property装饰器就是负责把一个方法变成属性，这样的属性可以很好的进行必要的检查
    #现在vertices看着是一个方法，但@property已经将其变成了属性，定义Graph对象时可以直接给它赋vertices这个属性的值
    #没有下面这样给属性vertices赋值的函数，说明vertices是一个只读的属性，不能在修改
    # @score.setter
    # def vertices(self, value):
    # 顶点集里是边的两端这样的节点对
    @property
    def vertices(self):
        return set(
            # this piece of magic turns ([1,2], [3,4]) into [1, 2, 3, 4]
            # the set above makes it's elements unique.
            sum(
                ([edge.start, edge.end] for edge in self.edges), []
            )
        )

    # both_ends是否两端都有边
    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    # 将每条边两端的结点加入节点对数组node_pairs中
    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        #[:]表示复制一个数组，而不是在初始的edges上做修改
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            # 普通元组无法修改，但通过collections定义的数组可以
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    # 通过边来寻找一个顶点的所有邻居
    @property
    def neighbours(self):
        neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            neighbours[edge.start].add((edge.end, edge.cost))

        return neighbours

    def dijkstra(self, source, dest):
        # assert expression如果expression表达式没有报错则跳过，否则报错AssertionError
        assert source in self.vertices, 'Such source node doesn\'t exist'
        assert dest in self.vertices, 'Such source node doesn\'t exis'

        # 1. Mark all nodes unvisited and store them.
        # 2. Set the distance to zero for our initial node
        # and to infinity for other nodes.
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            # 3. Select the unvisited node with the smallest distance,
            # it's current node now.
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])

            # 6. Stop, if the smallest distance
            # among the unvisited nodes is infinity.
            if distances[current_vertex] == inf:
                break

            # 4. Find unvisited neighbors for the current node
            # and calculate their distances through the current node.
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost

                # Compare the newly calculated distance to the assigned
                # and save the smaller one.
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

            # 5. Mark the current node as visited
            # and remove it from the unvisited set.
            vertices.remove(current_vertex)

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return path


if __name__ == '__main__':
    graph = Graph([
        ("a", "b", 7), ("a", "c", 9), ("a", "f", 14), ("b", "c", 10),
        ("b", "d", 15), ("c", "d", 11), ("c", "f", 2), ("d", "e", 6),
        ("e", "f", 9)])

    print(graph.dijkstra("a", "e"))
