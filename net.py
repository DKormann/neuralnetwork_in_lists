
#%%

def permute (n):
  if n < 1: return [[]]
  pre = permute(n-1)
  res = []
  for k in pre:
    res = res + [[1] + k] + [[0] + k]
  return res

#%%

def XOR (x):
  if x[0] == x[1]:
    return 0
  return 1

#%%

def map (f, x):
  res = []
  for k in x:
    res.append(f(k))
  return res

#%%

X = permute(2)
Y = map (XOR, X)

#%%

def Synapse(parent, strength):
  return[
    parent,
    strength
  ]

synapse_parent=0
synapse_strength=1

def Node(parents):
  synapses = []

  for parent in parents:
    synapses.append(Synapse(parent, 1))
  activation = 0
  baseline = 0
  return[
    synapses,
    activation,
    baseline
  ]

node_synapses = 0
node_activation = 1
node_baseline = 2

def execute_node(node):
  synapses = node[node_synapses]
  node[node_activation] = node[node_baseline]
  for synapse in synapses:
    strength = synapse[synapse_strength]
    parent = synapse[synapse_parent]
    execute_node(parent)
    node[node_activation] += parent[node_activation] * strength
  if node[node_activation] < 0: node[node_activation] = 0
  return node[node_activation]


input1 = Node([])
input2 = Node([])

inner1 = Node([input1, input2])
output = Node([inner1, input1, input2])

def run(inputs):
  input1[node_baseline] = inputs[0]
  input2[node_baseline] = inputs[1]
  return execute_node(output)

run([1,1])

c = 0

#%%
c += 1
def reward (node, signal):
  for synapse in node[node_synapses]:
    parent = synapse[synapse_parent]
    parentsignal = signal * synapse[synapse_strength]
    reward(parent, parentsignal)

    synapse[synapse_strength] += signal * parent[node_activation]
    node[node_baseline] += signal


def train_step(inputs, solution):
  prediction = run(inputs)
  signal = solution - prediction
  reward(output, signal * 0.1)

  if solution == 0:
    ok = prediction < 0.5
  else:
    ok = prediction >= 0.5
  
  return inner1[node_activation], prediction, ok



print(train_step([1, 1], 0))
print(train_step([1, 0], 1))
print(train_step([0, 1], 1))
print(train_step([1, 1], 0))

output[node_synapses][0][synapse_strength]
c

#%%

