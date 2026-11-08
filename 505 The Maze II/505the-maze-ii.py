import heapq


class Solution:
    def shortestDistance(
        self, maze: list[list[int]], start: list[int], destination: list[int]
    ) -> int:
        # (estimated total distance, actual distance travelled, cell)
        estimated_distance_remaining = (
            abs(start[0] - destination[0])
            + abs(start[1] - destination[1])
        )
        heap = [(estimated_distance_remaining, 0, tuple(start))]
        visited = set()
        dirs = [(0, 1), (0, -1), (1, 0), (-1, 0)]

        while heap:
            estimated_total_distance, distance_travelled, cell = heapq.heappop(heap)

            if cell in visited:
                continue

            visited.add(cell)

            if cell == tuple(destination):
                return distance_travelled

            # Iterate in each direction until we hit a wall.
            for dir in dirs:
                x, y = dir

                # row, col, is better as this is just misleading as the axis would be reversed if we look at the visual example of the cell
                curr_x, curr_y = cell
                roll_distance = 0


                while (
                    0 <= curr_x < len(maze)
                    and 0 <= curr_y < len(maze[0])
                    # prob should do just -1 here for both stells so we dont have to step back
                    and maze[curr_x][curr_y] != 1
                ):
                    curr_x = curr_x + x
                    curr_y = curr_y + y
                    roll_distance += 1

                # Coordinate from before the wall or boundary.
                real_x = curr_x - x
                real_y = curr_y - y
                roll_distance -= 1

                if (real_x, real_y) in visited:
                    continue

                route_to_dest = (
                    abs(real_x - destination[0])
                    + abs(real_y - destination[1])
                )

                # next distance traveled is what we would use for dijkstra, rout_to_dest is the heuristic we use that makes this a* maze
                next_distance_travelled = distance_travelled + roll_distance

                estimated_total_distance = (
                    next_distance_travelled + route_to_dest
                )

                heapq.heappush(heap, (estimated_total_distance, next_distance_travelled, (real_x, real_y)))

                # reset
                roll_distance = 0
                curr_x = cell[0]
                curr_y = cell[1]

        return -1