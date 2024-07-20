import numpy as np
from heapq import heappush, heappop
import time

def is_solved(state):
	# 判断是否所有的箱子都在目标位置上，也就是字符串里面没有`B`了
	return 'B' not in state

def can_move(state, shape, player_pos, move):
	new_state = list(state)
	x, y = player_pos
	_, width = shape
	move_cost = 0
	target = x + move[0], y + move[1]
	boxtarget = x + move[0] * 2, y + move[1] * 2
	curr1d = x * width + y
	target1d = target[0] * width + target[1]
	boxtarget1d = boxtarget[0] * width + boxtarget[1]
	if state[target1d] == 'W':
		return None, move_cost
	elif state[target1d] in '-G':
		new_state[curr1d] = '-' if new_state[curr1d] == 'P' else 'G'
		new_state[target1d] = 'P' if new_state[target1d] == '-' else 'L'
		move_cost = 3
	elif state[target1d] in 'BO':
		if state[boxtarget1d] in 'WBO':
			return None, move_cost
		elif state[boxtarget1d] in '-G':
			new_state[boxtarget1d] = 'B' if new_state[boxtarget1d] == '-' else 'O'
			new_state[target1d] = 'P' if new_state[target1d] == 'B' else 'L'
			new_state[curr1d] = '-' if new_state[curr1d] == 'P' else 'G'
			move_cost = 0 if new_state[boxtarget1d] == 'O' else 2
	return ''.join(new_state), move_cost

# 判断是否死锁
def is_deadlock(state, shape):
	height, width = shape
	if not state or len(state) != height * width:
		return False
	boxes, _, _ = find_boxes_and_goals(state, shape)
	for bx, by in boxes:  # corner deadlock
		box = bx * width + by
		if ((state[box - 1] == 'W' and state[box - width] == 'W') or
			(state[box + 1] == 'W' and state[box + width] == 'W') or
			(state[box + 1] == 'W' and state[box - width] == 'W') or
			(state[box - 1] == 'W' and state[box + width] == 'W')):
			return True
	double_box_positions = [
		(0, -1, -width, -width - 1),
		(0, 1, -width, -width + 1),
		(0, -1, width - 1, width),
		(0, 1, width + 1, width),
	]
	for bx, by in boxes:  # double box deadlock
		box = bx * width + by
		for pos in double_box_positions:
			pos_set = set()
			for dir in pos:
				pos_set.add(state[box + dir])
			if pos_set in ({'B', 'W'}, {'B'}, {'B', 'O'}, {'B', 'O', 'W'}):
				return True
	box = goal = 0
	for i in range(width + 1, 2 * width - 1):  # too many boxes deadlock
		if state[i] == 'B':
			box += 1
		elif state[i] in 'GL':
			goal += 1
	if box > goal:
		return True
	box = goal = 0
	for i in range(width * (height - 2) + 1, width * (height - 2) + width - 1):
		if state[i] == 'B':
			box += 1
		elif state[i] in 'GL':
			goal += 1
	if box > goal:
		return True
	box = goal = 0
	for i in range(width + 1, width * (height - 1) + 1, width):
		if state[i] == 'B':
			box += 1
		elif state[i] in 'GL':
			goal += 1
	if box > goal:
		return True
	box = goal = 0
	for i in range(2 * width - 2, width * height - 2, width):
		if state[i] == 'B':
			box += 1
		elif state[i] in 'GL':
			goal += 1
	if box > goal:
		return True
	return False

def get_state(matrix):
	# 将矩阵转换为字符串方便储存在哈希表中
	return matrix.tobytes().decode('utf-8').replace('\x00', '')

def find_boxes_and_goals(state, shape):
	_, width = shape
	boxes, goals, boxes_on_goal = [], [], []
	for pos, char in enumerate(state):
		if char == 'B':
			boxes.append((pos // width, pos % width))
		elif char in 'GL':
			goals.append((pos // width, pos % width))
		elif char == 'O':
			boxes_on_goal.append((pos // width, pos % width))
	return boxes, goals, boxes_on_goal

def heuristic(state, player_pos, shape):
	height, width = shape
	player_x, player_y = player_pos
	boxes, goals, _ = find_boxes_and_goals(state, shape)
	boxes_cost = len(boxes) * height * width
	player_cost = 0
	#这个用于启发算法将箱子移动到目标位置
	for box_x, box_y in boxes:
		boxes_cost += min(abs(box_x - goal_x) + abs(box_y - goal_y) 
						  for goal_x, goal_y in goals)
	#这个用于启发算法将玩家移动到箱子的位置
	player_cost = min(abs(box_x - player_x) + abs(box_y - player_y) 
					  for box_x, box_y in boxes) if boxes else 0
	return boxes_cost + player_cost

def Astar(game):
	start_time = time.time()
	matrix = game.map_matrix()
	where = np.where((matrix == 'P') | (matrix == 'L'))
	player_pos = where[0][0], where[1][0]
	state = get_state(matrix)
	initcost = cur_depth=0
	cur_cost = heuristic(state, player_pos, matrix.shape)

	heap = []
	heappush(heap, (initcost,cur_cost, state, player_pos, cur_depth,''))
	moves = [(1, 0), (-1, 0), (0, -1), (0, 1)]
	direction = {
		(1, 0): 'D',
		(-1, 0): 'U', 
		(0, -1): 'L',
		(0, 1): 'R',
	}
	hash = {None}
	while heap:
		total_cost, cur_cost, state, pos, depth, path = heappop(heap)
		hash.add(state)
		for move in moves:
			new_state, move_cost = can_move(state, matrix.shape, pos, move)
			deadlock = is_deadlock(new_state, matrix.shape)
			# 如果新状态已经在哈希表中或者是死锁状态，跳过
			if new_state in hash or deadlock:
				continue
			new_pos = pos[0] + move[0], pos[1] + move[1]
			new_cost = heuristic(new_state, new_pos, matrix.shape)
			# 如果新状态很大，跳过
			if new_cost == float('inf'):
				continue
			
			heappush(heap, (move_cost + total_cost-cur_cost+new_cost, new_cost, new_state, new_pos, depth + 1, path + direction[move]))
			
			if is_solved(new_state):
				print("solved")
				print("Time Consuming:", time.time() - start_time)
				time_cost = time.time() - start_time
				return path + direction[move], time_cost
	print("unsolvable")
	return None
	
	

	
	

	
    
	
	

 