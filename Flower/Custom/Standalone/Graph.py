class Graph:
    def __init__(self) -> None:
        self.partition = []
        self.nNodes = 0
        self.edges = []

        self.partition_value = 0

    def load(self, graphFile : str, partitionFile : str):
        f = open(graphFile, "r")
        file = f.readlines()

        self.nNodes = int(file[0].split(" ")[0])
        self.edges.clear()
        for i in range(1, len(file)):
            line = file[i].rstrip("\n ")
            neighbors = line.split(" ")
            for n in neighbors:
                self.edges.append([i - 1, int(n) - 1])
        f.close()

        self.partition.clear()
        f = open(partitionFile, "r")
        file = f.readlines()
        for line in file:
            self.partition.append(int(line.rstrip("\n ")))
        f.close()

        self.partition_value = 0
        for edge in self.edges:
            if self.partition[edge[0]] != self.partition[edge[1]]:
                self.partition_value = self.partition_value + 1
        self.partition_value = int(self.partition_value / 2)

    def eval_partition(self, partitionString : str) -> int:
        partition_value = 0
        for edge in self.edges:
            if partitionString[edge[0]] != partitionString[edge[1]]:
                partition_value = partition_value + 1
        partition_value = int(partition_value / 2)
        return partition_value

    def update_partition(self, partitionString : str):
        self.partition.clear()
        for character in partitionString:
            self.partition.append(int(character))
        self.partition_value = 0
        for edge in self.edges:
            if self.partition[edge[0]] != self.partition[edge[1]]:
                self.partition_value = self.partition_value + 1
        self.partition_value = int(self.partition_value / 2)
    