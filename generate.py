import sys
import copy
import time
start_time = time.time()
from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        for var in self.crossword.variables: 
            for value in self.domains[var].copy():
                if len(value) != var.length:
                    self.domains[var].remove(value)


    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        
        revised = False
        overlap = self.crossword.overlaps[x, y]
        if overlap:
            a, b = overlap
            domains_to_remove = set()
            for x_domain in self.domains[x]:
                overlap_possible = False
                for y_domain in self.domains[y]:
                    if x_domain != y_domain and x_domain[a] == y_domain[b]:
                        overlap_possible = True
                        break
                # no value in y.domain satifies the constraints
                if not overlap_possible:
                    domains_to_remove.add(x_domain)
            if domains_to_remove:
                self.domains[x] -= domains_to_remove
                revised = True
        return revised

        # if self.crossword.overlaps[x,y] != None:
        #     i,j = self.crossword.overlaps[x,y]
            
        #     y_j_list = []
            
        #     for value_y in self.domains[y]:
        #         y_j_list.append(value_y[j])
            
        #     for value_x in self.domains[x]:
        #         if value_x[i] not in y_j_list:
        #             self.domains[x].remove(value_x)
        #             return True
            
        # return False


                
        
    

    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        
        #add in all possible arcs in the crossword puzzle into arcs=[]
        if arcs == None:
            arcs = []
            for var1 in self.crossword.variables.copy():
                for var2 in self.crossword.variables.copy():
                    if var1 != var2:
                        arcs.append((var1,var2))
        
        while len(arcs) != 0:
            for arc in arcs:
                dequeued_arc = arcs.pop(arcs.index(arc))
                revised = self.revise(dequeued_arc[0],dequeued_arc[1])
                if revised == True:
                    if len(self.domains[dequeued_arc[0]]) == 0:
                        return False
                    else:
                        x_neighbors = self.crossword.neighbors(dequeued_arc[0])# .copy().remove(dequeued_arc[1])
                        for neighbor in x_neighbors:
                            arcs.append((neighbor,dequeued_arc[0]))
        return True
                    
                
                
        # revised =  True
                        
        # while revised == True:
        #     for arc in arcs:
        #         print('line 159: ' + str(type(arc[0])))
        #         revised = self.revise(arc[0],arc[1])    #need self.function to call on a function of a class?
        #         if revised == True:    #access each variable in the arc in the tuple
        #             if len(self.domains[arc[0]]) == 0 or len(self.domains[arc[1]]) == 0:
        #                 return False
        #             else:
        #                 x_neighbors = self.crossword.neighbors(arc[0]).copy().remove(arc[1])
        #                 for neighbor in x_neighbors:    #only var x in revise(x,y) has been modified so add back his neighbors
        #                     arcs.append((arc[0],neighbor))
        # return True

                    

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        variable_assigned_value = True
        
        for var in self.crossword.variables:    #check if all variables in the crossword
            if variable_assigned_value == False:
                return False
            if (var in assignment.keys()) and (assignment[var] in self.crossword.words):
                variable_assigned_value = True
            else:
                variable_assigned_value = False
                
        return True
            
        

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """

        for val in assignment.values():
            if list(assignment.values()).count(val) > 1:
                return False
        #check for variable length and value match
        for var in assignment.keys():
            if var.length != len(assignment[var]):
                return False
        #check for conflicts between neighboring variables
        for var in assignment.keys():
            neighbors = self.crossword.neighbors(var)
            for neighbor in neighbors:
                if neighbor in list(assignment.keys()): #some variables may not be in the assignment
                    i,j = self.crossword.overlaps[var,neighbor]
                    if assignment[var][i] != assignment[neighbor][j]:
                        return False                    
        #all checks passed, return true
        return True
                    
                    
        


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        
        list_of_values = []
        rule_out_count = []
        
        for val in self.domains[var]:
            list_of_values.append(val)
        
        var_neighbors = self.crossword.neighbors(var)
        
        for value in list_of_values:
            count = 0                           #count ruled out values from 0
            for neighbor in var_neighbors:      #access each neighbor
                (i,j) = self.crossword.overlaps[var,neighbor]   #(i,j) is the overlap between the variable and neighbor x
                neighbor_overlap_list = []                      #initiate empty list for neighbor x
                for val_neighbor in self.domains[neighbor]:     #for domain value in neighbor x
                    neighbor_overlap_list.append(val_neighbor[j])   #add the overlapped character to the overlap list

                    for val_neighbor_overlap in neighbor_overlap_list:  #for each overlapped character
                        if value[i] != val_neighbor_overlap:            #check if it matches the overlapped character of the variable
                            count += 1                                  #if it does not, add 1 to the count
            rule_out_count.append(count) 
        
        sorted_list_of_values = [x for _,x in sorted(zip(rule_out_count,list_of_values))]
        return sorted_list_of_values


    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        
        list_of_variables = []
        for var in self.crossword.variables:
            if var not in assignment:
                list_of_variables.append([var, len(self.domains[var]), len(self.crossword.neighbors(var))])

        if list_of_variables:
            list_of_variables.sort(key=lambda x: (x[1], -x[2]))
            return list_of_variables[0][0]
        return None
    
        # unassigned_variables = []
        # variable_domain_size = []
        # for var in self.crossword.variables:
        #     if var not in assignment.keys():
        #         unassigned_variables.append(var)
        #         variable_domain_size.append(len(self.domains[var]))
        
        # min_domain_size = min(variable_domain_size)
        # min_domain_indices = [i for i, j in enumerate(variable_domain_size) if j == min_domain_size]
        
        
        # min_domain_variables = []
        # min_domain_variables_degrees = []
        # for index in min_domain_indices:    
        #     min_domain_variables.append(unassigned_variables[index])
        #     min_domain_variables_degrees.append(len(self.crossword.neighbors(unassigned_variables[index])))
            
        # max_variable_degree = max(min_domain_variables_degrees)
        # chosen_variable = min_domain_variables[min_domain_variables.index(max_variable_degree)]
        # print('chosen variable:' + str(chosen_variable))
        
        # return(chosen_variable)
          

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        assignment_completed = self.assignment_complete(assignment)
        if assignment_completed == True:
            return assignment
        var = self.select_unassigned_variable(assignment)
        for value in self.order_domain_values(var, assignment):
            temp_assignment = assignment.copy()
            temp_assignment[var] = value
            # arcs = []
            # for var1 in temp_assignment.keys():
            #     for var2 in temp_assignment.keys():
            #         if var1 != var2:
                        # arcs.append((var1,var2))
            if self.consistent(temp_assignment):# and self.ac3(arcs):
                assignment[var] = value
                result = self.backtrack(assignment)
                if result != None:
                    return result
                del assignment[var]
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
print("--- %s seconds ---" % (time.time() - start_time))