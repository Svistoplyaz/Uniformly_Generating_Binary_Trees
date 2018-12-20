from collections import namedtuple
import random
import bisect

TreeNode = namedtuple("TreeNode", "value left_child right_child")

# n = 0, Cn = catalan_numbers[0], n = i, Cn = catalan_numbers[i]
catalan_numbers = [1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012, 742900, 2674440, 9694845,
                   35357670, 129644790, 477638700, 1767263190, 6564120420, 24466267020, 91482563640, 343059613650,
                   1289904147324, 4861946401452]

max_n = len(catalan_numbers) - 1

# Fill list with -1 for each possible size of tree
average_max_height = [-1 for i in range(max_n + 1)]
# Set average max height for basic trees: empty and size of 1
average_max_height[0] = 0
average_max_height[1] = 0

prob_distr = [{} for i in range(max_n + 1)]
prob_distr[0] = {0: 1}
prob_distr[1] = {0: 1}

# Fill list with -1 for each possible size of tree
average_leaves = [-1 for i in range(max_n + 1)]
# Set average max height for basic trees: empty and size of 1
average_leaves[0] = 0
average_leaves[1] = 1

prob_distr_leaves = [{} for i in range(max_n + 1)]
prob_distr_leaves[0] = {0: 1}
prob_distr_leaves[1] = {1: 1}

cur_value = 0


# Generates uniformly(by shape) binary tree of size n
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
        chance.append(chance[i - 1] + catalan_numbers[i] * catalan_numbers[n - 1 - i])

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


# Computes average max height for tree of size n
def compute_average_max_height(n):
    if n > max_n:
        return None

    if average_max_height[n] != -1:
        return average_max_height[n]

    sum = 0
    coef_sum = 0
    for i in range(n):
        coef = catalan_numbers[i] * catalan_numbers[n - 1 - i]
        coef_sum += coef
        sum += coef * max(compute_average_max_height(i), compute_average_max_height(n - 1 - i))

    ans = 1 + sum / coef_sum
    average_max_height[n] = ans

    return ans


# Computes probability distribution of max height for tree of size n
def compute_prob_distr_max_height(n):
    if n > max_n:
        return None

    if prob_distr[n] != {}:
        return prob_distr[n]

    for i in range(n):
        left_distr = compute_prob_distr_max_height(i)
        right_distr = compute_prob_distr_max_height(n - 1 - i)
        coef = catalan_numbers[i] * catalan_numbers[n - 1 - i] / catalan_numbers[n]
        for left_key in left_distr.keys():
            for right_key in right_distr.keys():
                left_prob = left_distr[left_key]
                right_prob = right_distr[right_key]

                write_to_key = 1 + max(left_key, right_key)
                what_to_write = left_prob * right_prob * coef

                if write_to_key in prob_distr[n]:
                    prob_distr[n][write_to_key] += what_to_write
                else:
                    prob_distr[n][write_to_key] = what_to_write

    return prob_distr[n]


# Computes average leaves amount for tree of size n
def compute_average_leaves(n):
    if n > max_n:
        return None

    if average_leaves[n] != -1:
        return average_leaves[n]

    sum = 0
    coef_sum = 0
    for i in range(n):
        coef = catalan_numbers[i] * catalan_numbers[n - 1 - i]
        coef_sum += coef
        sum += coef * (compute_average_leaves(i) + compute_average_leaves(n - 1 - i))

    ans = sum / coef_sum
    average_leaves[n] = ans

    return ans


# Computes probability distribution of leaves amount for tree of size n
def compute_prob_distr_leaves(n):
    if n > max_n:
        return None

    if prob_distr_leaves[n] != {}:
        return prob_distr_leaves[n]

    for i in range(n):
        left_distr = compute_prob_distr_leaves(i)
        right_distr = compute_prob_distr_leaves(n - 1 - i)
        coef = catalan_numbers[i] * catalan_numbers[n - 1 - i] / catalan_numbers[n]
        for left_key in left_distr.keys():
            for right_key in right_distr.keys():
                left_prob = left_distr[left_key]
                right_prob = right_distr[right_key]

                write_to_key = left_key + right_key
                what_to_write = left_prob * right_prob * coef

                if write_to_key in prob_distr_leaves[n]:
                    prob_distr_leaves[n][write_to_key] += what_to_write
                else:
                    prob_distr_leaves[n][write_to_key] = what_to_write

    return prob_distr_leaves[n]


if __name__ == "__main__":
    tree_root = generate_binary_tree(5)

    # for i in range(max_n):
    #     print("Tree of size " + str(i) + " has average maximum height equal to " + str(compute_average_max_height(i)))

    # print(str(compute_prob_distr_max_height(4)))

    # for i in range(max_n):
    #     print("Tree of size " + str(i) + " has average leaves equal to " + str(compute_average_leaves(i)))

    print(str(compute_prob_distr_leaves(5)))

    # queue = [tree_root]
    # while len(queue) != 0:
    #     cur = queue.pop(0)
    #     print(str(cur.value))
    #     if cur.left_child is not None:
    #         print(str(cur.value) + " is parent of left child " + str(cur.left_child.value))
    #         queue.append(cur.left_child)
    #     if cur.right_child is not None:
    #         print(str(cur.value) + " is parent of right child " + str(cur.right_child.value))
    #         queue.append(cur.right_child)
