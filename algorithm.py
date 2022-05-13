class TSP_Solver:

  def __init__(self, verbose=False):

    self.verbose = verbose
    self.preorder_result = []
    self.total_weight_two_approx = 0
    self.pc = [] # partial circuit for RandomInsertion
    self.total_weight_random_ins = 0
    self.pc1 = [] # partial circuit for CheapestInsertion
    self.total_weight_cheapest_ins = 0

  def graphConstructor(self, edgeList):

    meta_data, self.graph = edgeList[0], edgeList[1:]
    self.name, self.V = meta_data['name'], len(self.graph)
    if self.verbose:print(f"Graph: {self.name}\n")

  def __SanityCheck(self, cycle):

    cycle_ = sorted(set(cycle))
    assert len(cycle_) == len(cycle) - 1, "What you found is not a hamiltonian cycle"
    assert cycle_ == list(range(0, self.V)), "What you found does not touch all nodes"

  def __PRIM(self, G, s):

    '''
      This function performs PRIM's algorithm, using HEAP to obtain the MST.
    '''

    inf, number_of_edges = float('inf'), 0
    V = len(G)
    visited = [0 for _ in range(V)]
    MST = list(map(lambda x: list(map(lambda y:0, x)), G))

    visited[s] = True
    while (number_of_edges < V - 1):
      minimum = inf
      x = 0
      y = 0
      for i in range(V):
          if visited[i]:
              for j in range(V):
                  if ((not visited[j]) and G[i][j]):  
                      if minimum > G[i][j]:
                          minimum = G[i][j]
                          x = i
                          y = j
      
      MST[x][y], MST[y][x] = G[x][y], G[x][y]
      visited[y] = True
      number_of_edges += 1

    return MST

  def __preorder(self, G, start):

    self.preorder_result.append(start) # print v

    if len(self.preorder_result) > 1: # Apart from visiting the tree, it also computes the sum of weights
      self.total_weight_two_approx += self.graph[self.preorder_result[-1]][self.preorder_result[-2]]

    for i in range(len(G)):
      if G[start][i] and i not in self.preorder_result:
        self.__preorder(G, i)

  def Two_approx_solver(self, s=0):

    self.__preorder(self.__PRIM(self.graph, s), s) # applying preorder visiting on obtained MST
    # H' = PREORDER(T*, r) where T*=PRIM(G, r') and r=r'
    self.total_weight_two_approx += self.graph[self.preorder_result[-1]][s] # adding starting point at the
    # end to create a cycle
    self.suboptimal_hamiltonian_cycle = self.preorder_result + [s] # adding starting point at the
    # end to create a cycle -> RETURN <H', vi1> where vir is starting point

    self.__SanityCheck(self.suboptimal_hamiltonian_cycle)

    if self.verbose:print(f"The result of 2-approx algorithm: {self.total_weight_two_approx}")

    return self.total_weight_two_approx

  def RandomInsertion(self):

    # Initialization
    self.pc.append(0) 
    nodes = [i for i in range(1, self.V)] # 0 has already been selected
    minimum = float('inf')

    for i in range(len(self.graph)):
      if self.graph[0][i]:
        if self.graph[0][i] < minimum:

          minimum = self.graph[0][i]
          j = i
    self.pc.append(j)
    nodes.remove(j)

    while len(self.pc) < self.V:
      # Selection
      k = random.choice(nodes)
      nodes.remove(k)
      # Insertion
      minimum =  float('inf')

      for idx in range(len(self.pc)-1):

        i, j = self.pc[idx], self.pc[idx+1] # edge {i, j}
        wik, wkj, wij = self.graph[i][k], self.graph[k][j], self.graph[i][j]
        w = wik + wkj - wij

        if w < minimum:
          minimum = w
          idx_of_k = idx+1 # the location where k must be inserted

      self.pc.insert(idx_of_k, k)

    for el in range(len(self.pc)-1): 
      self.total_weight_random_ins += self.graph[self.pc[el]][self.pc[el+1]]

    self.pc.append(self.pc[0]) #adding starting point at the end to create a cycle
    self.total_weight_random_ins += self.graph[self.pc[-2]][self.pc[-1]] #adding starting
    # point at the end to create a cycle
    self.__SanityCheck(self.pc)

    if self.verbose:print(f"The result of RandomInsertion algorithm: {self.total_weight_random_ins}")

    return self.total_weight_random_ins

  def CheapestInsertion(self):

    # Initialization
    self.pc1.append(0) 
    nodes = [i for i in range(1, self.V)] # 0 has already been selected
    minimum = float('inf')

    for i in range(len(self.graph)):
      if self.graph[0][i]:
        if self.graph[0][i] < minimum:

          minimum = self.graph[0][i]
          j = i
    self.pc1.append(j)
    nodes.remove(j)

    while len(self.pc1) < self.V:

      minimum = float('inf')

      for k in nodes:        
        for idx in range(len(self.pc1)-1):

          i, j = self.pc1[idx], self.pc1[idx+1] # edge {i, j}
          wik, wkj, wij = self.graph[i][k], self.graph[k][j], self.graph[i][j]
          w = wik + wkj - wij

          if w < minimum:
            minimum = w
            selected_k = k
            idx_of_k = idx+1 # the location where k must be inserted

      self.pc1.insert(idx_of_k, selected_k)
      nodes.remove(selected_k)

    for el in range(len(self.pc1)-1): 
      self.total_weight_cheapest_ins += self.graph[self.pc1[el]][self.pc1[el+1]]

    self.pc1.append(self.pc1[0]) #adding starting point at the end to create a cycle
    self.total_weight_cheapest_ins += self.graph[self.pc1[-2]][self.pc1[-1]] #adding starting
    # point at the end to create a cycle
    self.__SanityCheck(self.pc1)

    if self.verbose:print(f"The result of CheapestInsertion algorithm: {self.total_weight_cheapest_ins}")

    return self.total_weight_cheapest_ins
