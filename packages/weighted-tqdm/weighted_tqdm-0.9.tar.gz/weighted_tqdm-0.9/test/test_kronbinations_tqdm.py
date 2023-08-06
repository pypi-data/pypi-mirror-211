from weighted_tqdm import *
#from kronbinations import *
import time

# create a tqdm object
a = [1, 2, 3, 4]
b = ['a', 'b', 'c', 'd']
p = weighted_kronbinations_tqdm([a,b], [1,1])
indexes = np.array([[0,0],[0,1],[0,2],[0,3],[1,0],[1,1],[1,2],[1,3]], dtype=int)
p.init(indexes)
for i in range(indexes.shape[0]):
    time.sleep(0.25)
    if i % 2 == 0:
        for j in p.sub_tqdm(range(10)):
            time.sleep(0.1)
    p.increment()