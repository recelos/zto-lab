class KnapsackSolver:
    def __init__(self, items, capacity):
        self.items = sorted(items, key=lambda x: x[1]/x[0], reverse=True)
        self.capacity = capacity
        self.best_value = 0
        self.best_solution = []
        self.length = len(items)

    def bound(self, node_index, current_weight, current_value):
        if current_weight >= self.capacity:
            return -1
        value_bound = current_value
        total_weight = current_weight
        for i in range(node_index, self.length):
            if total_weight + self.items[i][0] <= self.capacity:
                total_weight += self.items[i][0]
                value_bound += self.items[i][1]
            else:
                value_bound += (self.capacity - total_weight) * self.items[i][1] / self.items[i][0]
                break
        return value_bound

    def branch_and_bound(self, node_index, current_weight, current_value, items_included):
        if node_index == self.length:
            if current_value >= self.best_value:
                self.best_value = current_value
                self.best_solution = items_included[:]
            return

        if self.bound(node_index, current_weight, current_value) <= self.best_value:
            return

        if current_weight + self.items[node_index][0] <= self.capacity:
            items_included.append(node_index)
            self.branch_and_bound(node_index + 1, current_weight + self.items[node_index][0],
                                  current_value + self.items[node_index][1], items_included)
            items_included.pop()

        self.branch_and_bound(node_index + 1, current_weight, current_value, items_included)
    
    def solve(self):
        self.best_value = self.calc_first_upper_bound(self.items, self.capacity)
        self.branch_and_bound(0, 0, 0, [])
        return self.best_value, [self.items[i] for i in self.best_solution]
    
    def calc_first_upper_bound(self, items, capacity):
        backpack = 0
        value = 0
        for item in items:
            backpack += item[0]
            if backpack > capacity:
                backpack -= item[0]
                left = capacity - backpack
                part_of_item = left / item[0]
                backpack += item[0]*part_of_item
                value += part_of_item * item[1]
                return value
            else:
                value += item[1]
        return value
