from pprint import pprint
import pickle
f = open('defender.pickle', 'rb')
tree = pickle.load(f)

print(len(tree.keys()))
exit()

for i, val in enumerate(tree):

	print(tree[val])
	if i > 100:
		break