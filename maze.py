# COMP9021 24T1
# Assignment 2 *** Due Monday Week 11 @ 10.00am

# DO *NOT* WRITE YOUR NAME TO MAINTAIN ANONYMITY FOR PLAGIARISM DETECTION


# IMPORT ANY REQUIRED MODULE
# 每一行必须是0123  行数41  列数31  每一行长度相等
# 不满足上方  incorrect input

#每一行的最后一个不能新开一个新的路径，不能出现1 3
#最后一行也是 不能出现 2 3
import sys

class MazeError(Exception):
    def __init__(self, message):
        self.message = message

class Maze:
    def __init__(self, filename):
        self.filename = filename
        self.my_grid =[]
        self.checkfile()
        self.ydim = len(self.my_grid)
        self.xdim = len(self.my_grid[0])
        self.countgate()
        self.walls()
        self.pathways()
        self.cul_de_sacs()

    def checkfile(self):
        with open(self.filename,'r') as myfile:
            lines = myfile.readlines()
            for line in lines:
                line_s = line.strip()
                if line_s == '':
                    continue
                else:
                    line_result = line_s.replace(' ','')
                    self.my_grid.append(list(line_result))
            ydim = len(self.my_grid)
            xdim = len(self.my_grid[0])
            #check input is correct
            if not (2 <= ydim <= 41):
                raise MazeError('Incorrect input.')
            if not (2 <= xdim <= 31):
                raise MazeError('Incorrect input.')
            for i in range(len(self.my_grid)):
                for j in range(len(self.my_grid[0])):
                    if not(self.my_grid[i][j] in ['0','1','2','3']):
                        raise MazeError('Incorrect input.')
                    if len(self.my_grid[i]) != xdim:
                        raise MazeError('Incorrect input.')
            # further condition, check valid maze
            for i in range(len(self.my_grid)):
                for j in range(len(self.my_grid[0])):
                    if j == xdim - 1 and (self.my_grid[i][j] == '1' or self.my_grid[i][j] == '3'):
                        raise MazeError('Input does not represent a maze.')
                    if i == ydim -1 and (self.my_grid[i][j] == '2' or self.my_grid[i][j] == '3'):
                        raise MazeError('Input does not represent a maze.')

    # REPLACE PASS ABOVE WITH YOUR CODE
    
    # POSSIBLY DEFINE OTHER METHODS
        

    def analyse(self):
        #self.countgate()
        #self.walls()
        #self.pathways()
        #self.cul_de_sacs()
        self.print_result()

        # REPLACE PASS ABOVE WITH YOUR CODE

    def cul_de_sacs(self):
        self.rule = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        self.reverse_direction = {0: 2, 1: 3, 2: 0, 3: 1}
        self.numdead = 0
        self.deadend = []
        self.notdead = []
        len_onedead = []
        self.userecord_deepdead = {}
        self.real_deadend = []
        final_deadend = []
        for sublist in self.complete_path:
            inner_pointcounts = {}
            gate_num = 0
            for each_index in range(len(sublist)):
                if each_index == 0 or each_index == len(sublist) -1:
                    continue
                if sublist[each_index] in self.gate_record:
                    gate_num += 1
            # if a complete path doesn't contain the gate, all the points are dead ends
            if gate_num == 0:
                nostart_end = sublist[1:-1]
                map_complete = set(nostart_end)
                for unique_point in map_complete:
                    self.deadend.append(unique_point)
                if len(map_complete) == 1:
                    len_onedead.append(unique_point)
            # if it contain the gate, record each point appear index in the list
            for index, value in enumerate(sublist):
                if value in inner_pointcounts:
                    inner_pointcounts[value].append(index)
                else:
                    inner_pointcounts[value] = [index]
            #print('fcebucneov')
            # check step
            for keys, values in inner_pointcounts.items():
                for repeat_index in range(len(values)-1):
                    new_complete = sublist[values[repeat_index]+1: values[repeat_index+1]]
                    dead_indicator = True
                    for every in new_complete:
                        if every in self.gate_record:
                            dead_indicator = False
                            self.notdead.append(keys)
                    if dead_indicator == True:
                        help_path = sublist[values[repeat_index]: values[repeat_index+1]+1]
                        #print(help_path)
                        newnew_dic = {}
                        num_one = 0
                        for every_point in help_path:
                            if every_point not in newnew_dic:
                                newnew_dic[every_point] = 1
                            else:
                                newnew_dic[every_point] += 1
                        #print(newnew_dic)
                        #print(newnew_dic)

                        record_deepdead = {}
                        for key, value in newnew_dic.items():
                            if value == 1:
                                for eachdirection in self.full_record[key[0]][key[1]]:
                                    if eachdirection == 1:
                                        num_one += 1
                                record_deepdead[(key, value)] = num_one
                                self.userecord_deepdead[(key, value)] = num_one
                                num_one  = 0 
                        # this is the true end point
                        #print(num_one)
                        check_allone =[]
                        for val in record_deepdead.values():
                            check_allone.append(val)
                        my_set = set(check_allone)
                        if len(my_set) == 1 and 1 in my_set:
                            for each in new_complete:
                                if each not in self.deadend:
                                    self.deadend.append(each)
        self.deadarea = len(self.real_deadend)
        #print(self.deadarea)
        true_dead = []
        for keyy, valuess in inner_pointcounts.items():
            if len(valuess) == 1:
                true_dead.append(keyy)
        #print(self.deadend)
        #print(self.userecord_deepdead)
        for key1, value1 in self.userecord_deepdead.items():
            if value1 == 1:
                self.real_deadend.append(key1[0])
        #print(self.real_deadend)
        self.deadarea = len(self.real_deadend)
        copied_full_record = []
        for row in range(self.ydim - 1):
            newappend_line = []
            for col in range(self.xdim - 1):
                newappend_line.append(self.full_record[row][col].copy())
            copied_full_record.append(newappend_line)

        new_dead_indicator = False
        stop_indicator = True
        self.changed_full_record = []
        while stop_indicator:
            for every_real_deadend in self.real_deadend:
                move_direction =  copied_full_record[every_real_deadend[0]][every_real_deadend[1]]
                # the point cannot get into
                if 1 not in move_direction:
                    continue
                #get the direction the inner dead end can get into, and mark that direction as cannot get into
                direction_index = move_direction.index(1)
                copied_full_record[every_real_deadend[0]][every_real_deadend[1]][direction_index] = 0
                new_col = every_real_deadend[1] + self.rule[direction_index][1]
                new_row = every_real_deadend[0] + self.rule[direction_index][0]
                # if it movees out the map, skip
                if (new_row, new_col) in self.gate_record:
                    continue
                # the new point, and mark the direction to the inner dead end as 0, cannoy move again
                reverse_direction_index = self.reverse_direction[direction_index]
                copied_full_record[new_row][new_col][reverse_direction_index] = 0
            new_dead_indicator = False
            for point in self.deadend:
                if point in self.real_deadend:
                    continue
                if copied_full_record[point[0]][point[1]].count(1) == 1:
                    self.real_deadend.append(point)
                    # continue the searching
                    new_dead_indicator = True
                    original_directions = self.full_record[point[0]][point[1]].count(1)
                    # if previous has more than 2 direction, and now become only 1 direction available
                    # indication there happens the two or more dead areas are connected,
                    #  have to minus the dead area, because we defind deadarea = # of inner dead end initially
                    if original_directions == 3:
                        self.deadarea -= 1
                    elif original_directions == 4:
                        self.deadarea -= 2
            if not new_dead_indicator:
                break
        self.changed_full_record = copied_full_record
        self.finalcomplete = []
        debug = 0
        for each_completed_path in self.complete_path:
            debug += 1
            number_gate = 0
            change_each_completed_path = each_completed_path[1:-1]
            unique_onepath = list(set(change_each_completed_path))
            for unique_tupleone in unique_onepath:
                if unique_tupleone in self.gate_record:
                    number_gate += 1
                    unique_onepath.remove(unique_tupleone)
            if number_gate == 1:
                indicator_help = True
                for point in unique_onepath:
                    if point in self.real_deadend:
                        continue
                    if self.changed_full_record[point[0]][point[1]].count(1) != 2:
                        indicator_help = False
                        break
                if indicator_help:
                    each_completed_path = [item for index, item in enumerate(each_completed_path) if item not in each_completed_path[:index]]
                    self.finalcomplete.append(each_completed_path)
            #if debug == 9:
            #   break


        



                    



            
    def print_result(self):
        if self.gate_num == 1:
            print('The maze has a single gate.')
        elif self.gate_num == 0:
            print('The maze has no gate.')
        else:
            print(f'The maze has {self.gate_num} gates.')

        if len(self.full_path) >= 2:
            print(f'The maze has {len(self.full_path)} sets of walls that are all connected.' )
        elif len(self.full_path) == 1:
            print('The maze has walls that are all connected.')
        else:
            print('The maze has no wall.')

        if self.inaccessible_index == 0:
            print("The maze has no inaccessible inner point.")
        elif self.inaccessible_index == 1:
            print("The maze has a unique inaccessible inner point.")
        else:
            print(f"The maze has {self.inaccessible_index} inaccessible inner points.")

        if len(self.complete_path) == 1:
            print('The maze has a unique accessible area.')
        elif len(self.complete_path) == 0:
            print('The maze has no accessible area.')
        else:
            print(f'The maze has {len(self.complete_path)} accessible areas.')

        if self.deadarea == 0:
            print('The maze has no accessible cul-de-sac')
        elif self.deadarea == 1:
            print('The maze has accessible cul-de-sacs that are all connected.')
        else:
            print(f'The maze has {self.deadarea} sets of accessible cul-de-sacs that are all connected.')

        if len(self.finalcomplete) == 0:
            print('The maze has no entry-exit path with no intersection not to cul-de-sacs.')
        elif len(self.finalcomplete) == 1:
            print('The maze has a unique entry-exit path with no intersection not to cul-de-sacs.')
        else:
            print(f'The maze has {len(self.finalcomplete)} entry-exit paths with no intersections not to cul-de-sacs.')

    def countgate(self):
        self.gate_num = 0
        self.gate_record =[]
        ydim = len(self.my_grid)
        xdim = len(self.my_grid[0])
        # firsw row
        f_row = self.my_grid[0][:-1]
        for each in f_row:
            if each == '0' or each == '2':
                self.gate_num += 1
        # record gate index
        for col in range(xdim-1):
            if self.my_grid[0][col] == '0' or self.my_grid[0][col] == '2':
                self.gate_record.append((-1, col))
        #last row 
        l_row = self.my_grid[ydim-1][:-1]
        for each in l_row:
            if each == '0':
                self.gate_num += 1
        for col in range(xdim-1):
            if self.my_grid[-1][col] == '0' :
                self.gate_record.append((ydim -1, col))
        #last row 

        #first col
        #last col
        for i in range(ydim):
            for j in range(xdim):
                if (j == 0) and (i != ydim-1):
                    if (self.my_grid[i][j] == '0') or (self.my_grid[i][j] == '1'):
                        self.gate_num += 1
                        self.gate_record.append((i, -1))
                elif (j == xdim-1) and (i != ydim-1):
                    if (self.my_grid[i][j] == '0'):
                        self.gate_num += 1
                        self.gate_record.append((i, xdim-1))
        #print('dwbeuicnweoc')
        #print(self.gate_record)

    def walls(self):
        self.full_path = []
        ydim = len(self.my_grid)
        xdim = len(self.my_grid[0])
        for row in range(ydim):
            for col in range(xdim):
                indicator = True
                if self.my_grid[row][col] == '0':
                    continue
                for num in range(len(self.full_path)):
                        for each in self.full_path[num]:
                            if (row,col) == each:
                                indicator = False
                if indicator is True:
                    curr_shape = []
                    self.dfs(row, col, curr_shape)
                    self.full_path.append(curr_shape)

    def dfs(self, row, col, curr_shape):
        curr_shape.append((row, col))
        if self.my_grid[row][col] == '1':
            valid_neighbours = self.get_neighbours1(row, col)
        elif self.my_grid[row][col] == '2':
            valid_neighbours = self.get_neighbours2(row, col)
        elif self.my_grid[row][col] == '0':
            valid_neighbours = self.get_neighbours0()
        elif self.my_grid[row][col] == '3':
            valid_neighbours = self.get_neighbours3(row, col)
        for curr_neighbour in valid_neighbours:
             if curr_neighbour in curr_shape:
                continue
             else:
                self.dfs(curr_neighbour[0], curr_neighbour[1], curr_shape)

    def get_neighbours1(self, row, col):
        #leftup up rightup clcokwise
        ydim = len(self.my_grid)
        xdim = len(self.my_grid[0])
        eight_directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        valid_record = []
        direction_indicator = -1
        for each in eight_directions:
            direction_indicator += 1
            updates_row = row + each[0]
            updates_col = col + each[1]
            if 0 <= updates_row <= ydim - 1 and 0 <= updates_col <= xdim - 1:
                if direction_indicator == 1 and (self.my_grid[updates_row][updates_col] == '2' or self.my_grid[updates_row][updates_col] == '3'):

                    valid_record.append((updates_row, updates_col))
                elif  direction_indicator == 2 and (self.my_grid[updates_row][updates_col] == '2' or self.my_grid[updates_row][updates_col] == '3'):
                    valid_record.append((updates_row, updates_col))
                elif direction_indicator == 3 and (self.my_grid[updates_row][updates_col] == '2' or self.my_grid[updates_row][updates_col] == '3' or self.my_grid[updates_row][updates_col] == '1'):
                    valid_record.append((updates_row, updates_col))
                elif direction_indicator == 7 and (self.my_grid[updates_row][updates_col] == '1' or self.my_grid[updates_row][updates_col] == '3'):
                    valid_record.append((updates_row, updates_col))
        return valid_record

    def get_neighbours2(self, row, col):
        #leftup up rightup clcokwise
        ydim = len(self.my_grid)
        xdim = len(self.my_grid[0])
        eight_directions =  [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        valid_record = []
        direction_indicator = -1
        for each in eight_directions:
            direction_indicator += 1
            updates_row = row + each[0]
            updates_col = col + each[1]
            if 0 <= updates_row <= ydim - 1 and 0 <= updates_col <= xdim - 1:
                if direction_indicator == 1 and (self.my_grid[updates_row][updates_col] == '2' or self.my_grid[updates_row][updates_col] == '3'):
                    valid_record.append((updates_row, updates_col))
                elif direction_indicator == 5 and (self.my_grid[updates_row][updates_col] == '2' or self.my_grid[updates_row][updates_col] == '3' or self.my_grid[updates_row][updates_col] == '1'):
                    valid_record.append((updates_row, updates_col))
                elif direction_indicator == 6 and (self.my_grid[updates_row][updates_col] == '1' or self.my_grid[updates_row][updates_col] == '3'):
                    valid_record.append((updates_row, updates_col))
                elif direction_indicator == 7 and (self.my_grid[updates_row][updates_col] == '1' or self.my_grid[updates_row][updates_col] == '3'):
                    valid_record.append((updates_row, updates_col))
        return valid_record

    def get_neighbours3(self, row, col):
        #leftup up rightup clcokwise
        ydim = len(self.my_grid)
        xdim = len(self.my_grid[0])
        eight_directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        valid_record = []
        direction_indicator = -1
        for each in eight_directions:
            direction_indicator += 1
            updates_row = row + each[0]
            updates_col = col + each[1]
            if 0 <= updates_row <= ydim - 1 and 0 <= updates_col <= xdim - 1:
                if direction_indicator == 1 and (self.my_grid[updates_row][updates_col] == '2' or self.my_grid[updates_row][updates_col] == '3'):
                    valid_record.append((updates_row, updates_col))
                elif direction_indicator == 2 and (self.my_grid[updates_row][updates_col] == '2' or self.my_grid[updates_row][updates_col] == '3'):
                    valid_record.append((updates_row, updates_col))
                elif direction_indicator == 3 and (self.my_grid[updates_row][updates_col] == '2' or self.my_grid[updates_row][updates_col] == '3' or self.my_grid[updates_row][updates_col] == '1'):
                    valid_record.append((updates_row, updates_col))
                elif direction_indicator == 5 and (self.my_grid[updates_row][updates_col] == '1' or self.my_grid[updates_row][updates_col] == '3' or self.my_grid[updates_row][updates_col] == '2'):
                    valid_record.append((updates_row, updates_col))
                elif direction_indicator == 6 and (self.my_grid[updates_row][updates_col] == '1' or self.my_grid[updates_row][updates_col] == '3'):
                    valid_record.append((updates_row, updates_col))
                elif direction_indicator == 7 and (self.my_grid[updates_row][updates_col] == '1' or self.my_grid[updates_row][updates_col] == '3'):
                    valid_record.append((updates_row, updates_col))
        return valid_record

    def get_neighbours0(self):
        valid_record = False
        return valid_record
    
    
    
    def pathways(self):
        self.direction_map()
        self.failpoint = 0
        self.inaccessible_index = 0
        self.complete_path = []
        exit_gate = []
        debug = 0

        for every_gate in self.gate_record:
            double_check = len(self.complete_path)
            # the complete path is alrealy explored
            flag = 1
            if self.complete_path != []:
                for each in range(double_check):
                    if every_gate in self.complete_path[each]:
                        flag = 0
                        if flag == 0:
                            continue
            if flag == 0:
                continue
            curr_path = []
            curr_path.append(every_gate)
            start_point = self.get_into(every_gate)
            #print('start point')
            #print(start_point)
            #print(curr_path)
            exist_gate = self.exitpath(curr_path, start_point)
            exit_gate.append(exist_gate)
            #print('hhhhhhhh')
            #print(exit_gate)
            # one gate represents entrance index, and the path also exits through the entrance, even through there exists other exit way
            self.complete_path.append(curr_path)
            #print('这里这里')
            #print(self.complete_path)       
            for every_complete_path in self.complete_path:
                for every_index in range(1,len(every_complete_path)-1):
                    check_correct = 0
                    if every_complete_path[every_index][0] == every_complete_path[every_index+1][0] + 1 or every_complete_path[every_index][0] == every_complete_path[every_index+1][0] - 1:
                        check_correct += 1
                    if every_complete_path[every_index][1] == every_complete_path[every_index+1][1] + 1 or every_complete_path[every_index][1] == every_complete_path[every_index+1][1] - 1:
                        check_correct += 1
                    if check_correct == 2:
                        every_complete_path.insert(every_index+1, every_complete_path[every_index-1])
            
            # there are a lot steps by repetition, (go back to the previous step), and delete the gates index ,to get the accessible index in the map
            flat_data = [item for sublist in self.complete_path for item in sublist if item not in self.gate_record]
            unique_tuple_num = len(set(flat_data))
            #(unique_tuple_num)
            # total index in the map
            total_map = (self.ydim-1)*(self.xdim-1)
            self.inaccessible_index = total_map - unique_tuple_num
            

    
    def exitpath(self, curr_path, next_point):
        double_check = 0
        exit_gate = []
        if next_point in [curr_path[0]]:
            curr_path.append(next_point)
            exit_gate.append(next_point)
            return next_point
        self_point = next_point
        if self_point in self.gate_record:
            exit_gate.append(self_point)
        curr_path.append(self_point)
        next_points = self.walk_neighbour(self_point)
        if len(next_points) != 1:
            for next_possible_point in next_points:
                if next_possible_point in  curr_path:
                    double_check += 1
                    continue
                else:
                    return self.exitpath(curr_path, next_possible_point)
            if double_check == len(next_points):
                visited_point_index = curr_path.index(self_point) -1
                return self.exitpath(curr_path, curr_path[visited_point_index])
        else:
            if next_point in curr_path:
                return self.exitpath(curr_path, next_points[0])
            


        

    def direction_map(self):
        each_record = []
        full_record = []
        for row in range(self.ydim-1):
            each_record = []
            for col in range(self.xdim-1):
                # up right down left
                record_move = [0,0,0,0]
                if self.my_grid[row][col] not in ('1','3'):
                    record_move[0] = 1
                if self.my_grid[row][col + 1] not in ('2','3'):
                    record_move[1] = 1
                if self.my_grid[row + 1][col] not in ('1','3'):
                    record_move[2] = 1
                if self.my_grid[row][col] not in ('2','3'):
                    record_move[3] = 1
                each_record.append(record_move)
            full_record.append(each_record)
        self.full_record = full_record

    def walk_neighbour(self, curr_point):
        if curr_point in self.gate_record:
            curr_point = self.get_into(curr_point)
        walk_record = []
        # up right down left
        fixed_rule = [(-1, 0), (0, 1), (1, 0), (0, -1)]
        curr_row = curr_point[0]
        curr_col = curr_point[1]
        each_record = self.full_record[curr_row][curr_col]
        # up right down left
        record_index = 0
        for indicator in each_record:
            if indicator == 1:
                curr_row += fixed_rule[record_index][0]
                curr_col += fixed_rule[record_index][1]
                walk_record.append((curr_row, curr_col))
                curr_row = curr_point[0]
                curr_col = curr_point[1]
            record_index += 1
        return walk_record

    def get_into(self, initial_gate):
        row = initial_gate[0]
        col = initial_gate[1]
        if row  == -1 :
            row += 1
        if col == -1:
            col += 1
        if row == self.ydim -1:
            row -= 1
        if col == self.xdim -1:
            col -=1

        return (row, col)


        # REPLACE PASS ABOVE WITH YOUR CODE
    def accul_de_sacs(self):
        result = []
        for each_dead in sorted(self.real_deadend, key = lambda x:(x[0],  x[1])):
            result.append(f"    \\node at ({each_dead[1] + 0.5},{each_dead[0] + 0.5}) " + "{};\n")
        return result
    
    def without_intersections(self):
        record_list = []
        finalized_list = []
        record_lines = []
        result = []
        self.finalcomplete.sort(key=lambda x: (x[1], x[0]))
    
        for each_sublist in self.finalcomplete:
            record_list = []
            for each_tuu in each_sublist:
                if each_tuu in self.real_deadend:
                    continue
                else:
                    record_list.append(each_tuu)
            finalized_list.append(record_list)

        for path in finalized_list:
            turn_path = [path[0]]
            for each_index in range(len(path)):
                if each_index == 0 or each_index == len(path) - 1:
                    continue

                # find the direction vector
                diff_2_1 = (path[each_index][0] - path[each_index - 1][0], path[each_index][1] - path[each_index - 1][1])
                diff_3_2 = (path[each_index + 1][0] - path[each_index][0], path[each_index + 1][1] - path[each_index][1])
                # this is the turn
                if diff_2_1 != diff_3_2:
                    turn_path.append(path[each_index])
            # append the last step, gate, if there is no path, record directly
            turn_path.append(path[-1])
            
            for each_index in range(len(turn_path) - 1):
                previous_coordinate = (turn_path[each_index][1] + 0.5, turn_path[each_index][0] + 0.5)
                next_coordinate = (turn_path[each_index + 1][1] + 0.5, turn_path[each_index + 1][0] + 0.5)
                #from left to right, from up to down for each single draw
                record_lines.append(sorted([previous_coordinate, next_coordinate],key=lambda x: (x[0], x[1])))
        # follow the draw sorting, that is horizontal first, from left to right
        record_lines.sort(key=lambda x: (x[0][1], x[0][0]))
        for line in record_lines:
            if line[1][1] == line[0][1]:
                result.append(f"    \draw[dashed, yellow] ({line[0][0]},{line[0][1]}) -- ({line[1][0]},{line[1][1]});\n")
        # vertical second
        for line in sorted(record_lines):
            if line[1][0] == line[0][0]:
                result.append(f"    \draw[dashed, yellow] ({line[0][0]},{line[0][1]}) -- ({line[1][0]},{line[1][1]});\n")
        return result


    def check_valid(self, row_index, col_index):
        if (0 <= row_index <= self.ydim-1) and (0 <= col_index <= self.xdim-1):
            return True
        else:
            return False
    def show_pillows(self):
        result = []
        for row in range(self.ydim):
            for col in range(self.xdim):
                if self.my_grid[row][col] != '0':
                    continue
                if ((not self.check_valid(row, col) or self.my_grid[row][col-1] in ["0", "2"]) and 
                   (not self.check_valid(row, col) or self.my_grid[row - 1][col] in ["0", "1"])):
                    result.append(f"    \\fill[green] ({col},{row}) circle(0.2);\n")
        return result
    
    def show_walls(self):
        result = []
        for each_i in range(self.ydim):
            start_record = []
            end_record = []
            each_j = 0
            while each_j < self.xdim - 1:
                if self.my_grid[each_i][each_j] in ['1', '3'] and self.my_grid[each_i][each_j-1] not in ['1', '3'] and each_j != 0:
                    start_record.append(each_j)
                elif self.my_grid[each_i][each_j] in ['1', '3'] and each_j == 0:
                    start_record.append(each_j)
                if self.my_grid[each_i][each_j] in ['1', '3'] and self.my_grid[each_i][each_j+1] not in ['1', '3']:
                    end_record.append(each_j+1)
                each_j += 1
            begin = 0
            while begin != len(start_record):
                show_line = f"    \\draw ({start_record[begin]},{each_i}) -- ({end_record[begin]},{each_i});\n"
                #print(f'{start_record[begin]},{each_i}) -de- {end_record[begin]},{each_i}')
                result.append(show_line)
                begin += 1

        for each_i in range(self.xdim):
            start_record = []
            end_record = []
            each_j = 0
            while each_j < self.ydim - 1:

                if self.my_grid[each_j][each_i] in ['2', '3'] and self.my_grid[each_j-1][each_i] not in ['2', '3'] and each_j!= 0:
                    start_record.append(each_j)
                elif self.my_grid[each_j][each_i] in ['2', '3'] and each_j == 0:
                    start_record.append(each_j)
                if self.my_grid[each_j][each_i] in ['2', '3'] and self.my_grid[each_j+1][each_i] not in ['2', '3']:
                    end_record.append(each_j+1)
                each_j += 1

            begin = 0
            while begin != len(start_record):
                show_line = f"    \\draw ({each_i},{start_record[begin]}) -- ({each_i},{end_record[begin]});\n"
                #print(f'{each_i},{start_record[begin]}) -de- {each_i},{end_record[begin]}')
                result.append(show_line)
                begin += 1
        return result
           #     if self.my_grid[each_i][each_j] in ('1','3'):

    def display(self):
        display_file = self.filename.replace(self.filename[-3:], "tex")
        with open(display_file, 'w') as displayfile:
            displayfile.write("\\documentclass[10pt]{article}\n")
            displayfile.write("\\usepackage{tikz}\n")
            displayfile.write("\\usetikzlibrary{shapes.misc}\n")
            displayfile.write("\\usepackage[margin=0cm]{geometry}\n")
            displayfile.write("\\pagestyle{empty}\n")
            displayfile.write("\\tikzstyle{every node}=[cross out, draw, red]\n")
            displayfile.write("\n")
            displayfile.write("\\begin{document}\n")
            displayfile.write("\n")
            displayfile.write("\\vspace*{\\fill}\n")
            displayfile.write("\\begin{center}\n")
            displayfile.write("\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n")
            displayfile.write("% Walls\n")
            displayfile.writelines(self.show_walls())
            displayfile.write("% Pillars\n")
            displayfile.writelines(self.show_pillows())
            displayfile.write("% Inner points in accessible cul-de-sacs\n")
            displayfile.writelines(self.accul_de_sacs())
            displayfile.write("% Entry-exit paths without intersections\n")
            displayfile.writelines(self.without_intersections())
            displayfile.write("""\\end{tikzpicture}
\\end{center}
\\vspace*{\\fill}

\\end{document}\n""")







    def check_valid(self, row_index, col_index):
        if (0 <= row_index <= self.ydim-1) and (0 <= col_index <= self.xdim-1) :
            return True
        else:
            return False
    def show_pillows(self):
        result = []
        for row in range(self.ydim):
            for col in range(self.xdim):
                if self.my_grid[row][col] != '0':
                    continue
                if ((not self.check_valid(row, col) or self.my_grid[row][col-1] in ["0", "2"]) and 
                   (not self.check_valid(row, col) or self.my_grid[row - 1][col] in ["0", "1"])):
                    result.append(f"    \\fill[green] ({col},{row}) circle(0.2);\n")
        return result
    
    def show_walls(self):
        result = []
        for each_i in range(self.ydim):
            start_record = []
            end_record = []
            each_j = 0
            while each_j < self.xdim - 1:
                if self.my_grid[each_i][each_j] in ['1', '3'] and self.my_grid[each_i][each_j-1] not in ['1', '3'] and each_j != 0:
                    start_record.append(each_j)
                elif self.my_grid[each_i][each_j] in ['1', '3'] and each_j == 0:
                    start_record.append(each_j)
                if self.my_grid[each_i][each_j] in ['1', '3'] and self.my_grid[each_i][each_j+1] not in ['1', '3']:
                    end_record.append(each_j+1)
                each_j += 1
            begin = 0
            while begin != len(start_record):
                show_line = f"    \\draw ({start_record[begin]},{each_i}) -- ({end_record[begin]},{each_i});\n"
                #print(f'{start_record[begin]},{each_i}) -de- {end_record[begin]},{each_i}')
                result.append(show_line)
                begin += 1

        for each_i in range(self.xdim):
            start_record = []
            end_record = []
            each_j = 0
            while each_j < self.ydim - 1:

                if self.my_grid[each_j][each_i] in ['2', '3'] and self.my_grid[each_j-1][each_i] not in ['2', '3'] and each_j!= 0:
                    start_record.append(each_j)
                elif self.my_grid[each_j][each_i] in ['2', '3'] and each_j == 0:
                    start_record.append(each_j)
                if self.my_grid[each_j][each_i] in ['2', '3'] and self.my_grid[each_j+1][each_i] not in ['2', '3']:
                    end_record.append(each_j+1)
                each_j += 1

            begin = 0
            while begin != len(start_record):
                show_line = f"    \\draw ({each_i},{start_record[begin]}) -- ({each_i},{end_record[begin]});\n"
                #print(f'{each_i},{start_record[begin]}) -de- {each_i},{end_record[begin]}')
                result.append(show_line)
                begin += 1
        return result
           #     if self.my_grid[each_i][each_j] in ('1','3'):

    def display(self):
        display_file = self.filename.replace(self.filename[-3:], "tex")
        with open(display_file, 'w') as displayfile:
            displayfile.write("\\documentclass[10pt]{article}\n")
            displayfile.write("\\usepackage{tikz}\n")
            displayfile.write("\\usetikzlibrary{shapes.misc}\n")
            displayfile.write("\\usepackage[margin=0cm]{geometry}\n")
            displayfile.write("\\pagestyle{empty}\n")
            displayfile.write("\\tikzstyle{every node}=[cross out, draw, red]\n")
            displayfile.write("\n")
            displayfile.write("\\begin{document}\n")
            displayfile.write("\n")
            displayfile.write("\\vspace*{\\fill}\n")
            displayfile.write("\\begin{center}\n")
            displayfile.write("\\begin{tikzpicture}[x=0.5cm, y=-0.5cm, ultra thick, blue]\n")
            displayfile.write("% Walls\n")
            displayfile.writelines(self.show_walls())
            displayfile.write("% Pillars\n")
            displayfile.writelines(self.show_pillows())
            displayfile.write("% Inner points in accessible cul-de-sacs\n")
            displayfile.writelines(self.accul_de_sacs())
            displayfile.write("% Entry-exit paths without intersections\n")
            displayfile.writelines(self.without_intersections())
            displayfile.write("""\\end{tikzpicture}
\\end{center}
\\vspace*{\\fill}

\\end{document}\n""")
