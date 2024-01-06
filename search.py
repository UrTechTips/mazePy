class Node():
    def __init__(self, position, parent, action):
        self.position = position # tupple with coordinates
        self.parent = parent
        self.action = action

class Queue():
    def __init__(self):
        self.queue = []

    def add(self, node):
        self.queue.append(node)

        return self.queue
    
    def peek(self):
        node = self.queue[0]
        return node

    def empty(self):
        if len(self.queue) == 0:
            return True
        else:
            return False
        
    def remove(self):
        if len(self.queue) == 0:
            print('Empty Queue!')
        else:
            node = self.queue[0]
            self.queue.remove(node)
            return node

class BFS():
    def __init__(self, dimentions, start, finish, walls):
        self.dimentions = dimentions # List
        self.start = start # Coordinates
        self.finish = finish # Coordinates
        self.walls = walls # Walls Coordinates (LIST or SET)

    def neighbours(self, node):
        rows = self.dimentions[0]
        columns = self.dimentions[1]

        row = node.position[0] # Node's Row
        column = node.position[1] # Node's Column

        options = [
            ('Up', (row - 1, column)),
            ('Down', (row + 1, column)),
            ('Left', (row, column - 1)),
            ('Right', (row, column + 1))
        ]
        result = [] # All neighbours

        for action, (r, c) in options:
            if 0 <= r < rows and 0 <= c < columns and (r, c) not in self.walls:
                result.append((action, (r, c)))

        return result

    def solve(self):
        visited = set()
        queue = Queue()
        path = []

        start = Node(position=self.start, parent=None, action=None)
        queue.add(start)

        while True:
            print([x.position for x in queue.queue])
            if queue.empty():
                break

            node = queue.remove()
            if node.position == self.finish:
                nNode = node
                while True:
                    if nNode.parent == None:
                        break
                    else:
                        path.append(nNode.parent.action)
                        nNode = nNode.parent
            
                return path[::-1]
            
            for action, position in self.neighbours(node):
                if position not in visited:
                    childNode = Node(position = position, parent=node, action=action)
                    queue.add(childNode)

            visited.add(node.position)