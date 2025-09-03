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

     # Added for use in sets to detect duplicate sentences
    def __hash__(self):
        return hash((frozenset(self.cells), self.count))
    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the number of cells in the set is equal to the count,
        # then all cells in the set must be mines.
        if len(self.cells) == self.count and self.count > 0:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If the count of mines is 0, then all cells in the set
        # must be safe.
        if self.count == 0:
            return self.cells.copy()
        return set()

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)


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
        # 1) Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) Mark the cell as safe
        self.mark_safe(cell)

        # 3) Add a new sentence to the AI's knowledge base
        neighbors = set()
        known_mine_count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                # Ensure the cell is within the board boundaries
                if 0 <= i < self.height and 0 <= j < self.width:
                    neighbor_cell = (i, j)
                    # Exclude the cell itself
                    if neighbor_cell == cell:
                        continue
                    # Only add undetermined cells to the new sentence
                    if neighbor_cell in self.mines:
                        known_mine_count += 1
                    elif neighbor_cell not in self.safes:
                        neighbors.add(neighbor_cell)

        new_sentence = Sentence(neighbors, count - known_mine_count)

        # Adjust count based on already known mines within neighbors
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # self.knowledge.append(new_sentence)

        # 4 & 5) Infer new knowledge (safes, mines, sentences) repeatedly
        knowledge_changed = True
        while knowledge_changed:
            knowledge_changed = False

            # Use known_safes and known_mines to infer new safe spots and mines
            safes_found = set()
            mines_found = set()
            for sentence in self.knowledge:
                safes_found.update(sentence.known_safes())
                mines_found.update(sentence.known_mines())

            if safes_found:
                for safe_cell in safes_found:
                    if safe_cell not in self.safes:
                        self.mark_safe(safe_cell)
                        knowledge_changed = True

            if mines_found:
                for mine_cell in mines_found:
                    if mine_cell not in self.mines:
                        self.mark_mine(mine_cell)
                        knowledge_changed = True

            # Remove empty sentences from knowledge
            self.knowledge = [s for s in self.knowledge if s.cells]

            # Infer new sentences using the subset method
            new_inferences = []
            for s1 in self.knowledge:
                for s2 in self.knowledge:
                    if s1.cells == s2.cells:
                        continue
                    # If s2 is a subset of s1, create a new sentence
                    if s2.cells.issubset(s1.cells):
                        inferred_cells = s1.cells - s2.cells
                        inferred_count = s1.count - s2.count
                        inferred_sentence = Sentence(inferred_cells, inferred_count)

                        # Add the new sentence if it's not already in our knowledge
                        if inferred_sentence not in self.knowledge and inferred_sentence not in new_inferences:
                            new_inferences.append(inferred_sentence)
                            knowledge_changed = True

            self.knowledge.extend(new_inferences)

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            return safe_moves.pop()
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        possible_moves = []
        for i in range(self.height):
            for j in range(self.width):
                cell = (i, j)
                if cell not in self.moves_made and cell not in self.mines:
                    possible_moves.append(cell)

        if not possible_moves:
            return None

        return random.choice(possible_moves)