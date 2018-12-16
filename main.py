from collections import namedtuple
import random
import bisect

TreeNode = namedtuple("TreeNode", "value left_child right_child")

# n = 0, Cn = catalan_numbers[0], n = i, Cn = catalan_numbers[i]
catalan_numbers = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012, 742900, 2674440, 9694845,
                   35357670, 129644790, 477638700, 1767263190, 6564120420, 24466267020, 91482563640, 343059613650,
                   1289904147324, 4861946401452]

max_n = len(catalan_numbers) - 1
cur_value = 0


def generate_binary_tree(n):
    global cur_value
    # print(str(cur_value) + "Current tree size" + str(n))
    if n == 0 or n > max_n:
        return None

    root = TreeNode(value=cur_value, left_child=None, right_child=None)
    cur_value += 1

    if n == 1:
        return root

    # This array will store cumulative sum of number of combinations we can get with left and right subtrees
    # The left subtree is size of i, the right subtree is size of n-1-i
    chance = [catalan_numbers[0] * catalan_numbers[n - 1]]
    for i in range(1, n):
        chance.append(chance[i - 1] + catalan_numbers[0] * catalan_numbers[n - 1 - i])

    # Maximum value from generated array
    # print("chance" + str(n - 1))
    max_number = chance[n - 1]
    # Choosing one of subtrees combinations uniformly
    chosen_chance = random.randint(1, max_number)
    # Finding the size of left subtree
    # It is equal to index returned by this lower_bound function
    index = bisect.bisect_left(chance, chosen_chance)

    # print(str(root.value) + "Left tree size" + str(index))
    # print(str(root.value) + "Right tree size" + str(n - 1 - index))
    # Generating left subtree
    root = root._replace(left_child=generate_binary_tree(index))
    # Generating right subtree
    root = root._replace(right_child=generate_binary_tree(n - 1 - index))

    return root


tree_root = generate_binary_tree(5)

queue = [tree_root]
while len(queue) != 0:
    cur = queue.pop(0)
    print(str(cur.value))
    if cur.left_child is not None:
        print(str(cur.value) + " is parent of left child " + str(cur.left_child.value))
        queue.append(cur.left_child)
    if cur.right_child is not None:
        print(str(cur.value) + " is parent of right child " + str(cur.right_child.value))
        queue.append(cur.right_child)
