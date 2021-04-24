import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        mines_set = set()
        
        if len(self.cells) == int(self.count):
            mines_set = self.cells
        
        return(mines_set)

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        safes_set = set()
        
        if self.count == 0:
            safes_set = self.cells
            
        return(safes_set)

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.discard(cell)
            self.count -= 1
        
        return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.discard(cell)

        return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        
        self.moves_made.add(cell)
        
        self.mark_safe(cell)
        
        surrounding_cells = set()
        for cell_row in range(cell[0]-1,cell[0]+2):
            for cell_col in range(cell[1]-1,cell[1]+2):
                if (cell_row >= 0 and cell_col >= 0) and (cell_row <= 7 and cell_col <=7) and ((cell_row,cell_col) != cell):
                    print("Added surrounding cells: " + str(cell_row) + str(cell_col))
                    surrounding_cells.add((cell_row,cell_col))
                    
        new_sentence = Sentence(surrounding_cells,count)
        print("New sentence is: " + str(new_sentence))
        
        for safe_cell in self.safes:
            new_sentence.mark_safe(safe_cell)
        for mine_cell in self.mines:
            new_sentence.mark_mine(mine_cell)
        print("Processed sentence is: " + str(new_sentence))
        self.knowledge.append(new_sentence)
       
        new_safe_set = set()
        new_mine_set = set()
        updated_new_safe_set = set()
        updated_new_mine_set = set()
        
        change_made = True
        count = 0
        while change_made == True:
            change_made = False
            for sentence in self.knowledge:
                if (len(sentence.known_safes()) > 0) and (not sentence.known_safes().issubset(self.safes)) and count < 9:
                    updated_new_safe_set = new_safe_set.union(sentence.known_safes())
                    print("Known Safes from Sentence: " + str(sentence.known_safes()))
                    print("Updated Safe Set" + str(updated_new_safe_set))
                    change_made = True
                    count += 1
                    
            if len(updated_new_safe_set) > 0:
                for safe_cell in updated_new_safe_set:
                    self.mark_safe(safe_cell)
                    print("Updated safes:" + str(self.safes))

                
        change_made = True
        count = 0
        while change_made == True:
            change_made = False
            for sentence in self.knowledge:
                if (len(sentence.known_mines()) > 0) and (not sentence.known_mines().issubset(self.mines)) and count < 9:
                    updated_new_mine_set = new_mine_set.union(sentence.known_mines())
                    print("Known Mines from Sentence: " + str(sentence.known_mines()))
                    print("Updated Mines Set" + str(updated_new_mine_set))
                    change_made = True
                    count += 1
                    
            if len(updated_new_mine_set) > 0:
                for mine_cell in updated_new_mine_set:
                    self.mark_mine(mine_cell)
                    print("Updated mines:" + str(self.mines))

        change_made = True
        while change_made == True:
            for selected_sentence in self.knowledge:
                for compared_sentence in self.knowledge:
    
                    if selected_sentence.cells < compared_sentence.cells:
                        a_new_sentence = Sentence(compared_sentence.cells.difference(selected_sentence.cells),
                              compared_sentence.count - selected_sentence.count)
                        change_made = True
                        
                        if a_new_sentence not in self.knowledge:
                            self.knowledge.append(a_new_sentence)
                        if selected_sentence in self.knowledge:
                            self.knowledge.remove(selected_sentence)
                        
                        for sentence in self.knowledge:
                            
                            while (self.knowledge.count(sentence) > 1):
                                   self.knowledge.remove(sentence)
                                   if sentence.cells == set():
                                       self.knowledge.remove(sentence)
                    else:
                        change_made = False
                                   
                                   
        print("KNOWLEDGE BASE")
        for sentence in self.knowledge:
            print(sentence)
        
        print("SAFE CELLS")
        for safe_cell in self.safes:
            print(safe_cell)
        
        print("MINES")
        for mine_cell in self.mines:
            print(mine_cell)

        return

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for safe_cell in self.safes:
            if safe_cell not in self.moves_made:
                return(safe_cell)
            


    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        all_moves = set()
        for i in range(self.height):
            for j in range(self.width):
                all_moves.add((i,j))
        
        unchosen_moves = all_moves - self.moves_made
        
        non_mine_unchosen_moves = unchosen_moves - self.mines
        
        if non_mine_unchosen_moves != set():
            random_move = random.sample(non_mine_unchosen_moves,1)[0]
        
        if non_mine_unchosen_moves == set():
            return(None)
            
        return(random_move)
