import itertools
import random


class Minesweeper():
    """
    Minesweeper game representation
    """

    # ... (The Minesweeper class is correct, no changes needed) ...
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
        if len(self.cells) == self.count and self.count > 0:
            return self.cells.copy()
        return set()

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
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
        self.height = height
        self.width = width
        self.moves_made = set()
        self.mines = set()
        self.safes = set()
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        if cell not in self.mines:
            self.mines.add(cell)
            for sentence in self.knowledge:
                sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        if cell not in self.safes:
            self.safes.add(cell)
            for sentence in self.knowledge:
                sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.
        """
        self.moves_made.add(cell)
        self.mark_safe(cell)

        neighbors = set()
        known_mine_count = 0
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):
                if (i, j) == cell:
                    continue
                if 0 <= i < self.height and 0 <= j < self.width:
                    if (i, j) in self.mines:
                        known_mine_count += 1
                    elif (i, j) not in self.safes:
                        neighbors.add((i, j))

        new_sentence = Sentence(neighbors, count - known_mine_count)
        if new_sentence not in self.knowledge:
            self.knowledge.append(new_sentence)

        # 统一的、更健壮的推理循环
        while True:
            changes_made = False

            # 步骤 A: 标记所有可以直接推断出的安全格和地雷格
            safes_inferred = set()
            mines_inferred = set()
            for sentence in self.knowledge:
                safes_inferred.update(sentence.known_safes())
                mines_inferred.update(sentence.known_mines())

            new_safes = safes_inferred - self.safes
            if new_safes:
                changes_made = True
                for safe_cell in new_safes:
                    self.mark_safe(safe_cell)

            new_mines = mines_inferred - self.mines
            if new_mines:
                changes_made = True
                for mine_cell in new_mines:
                    self.mark_mine(mine_cell)

            # 清理所有空的句子
            self.knowledge = [s for s in self.knowledge if s.cells]

            # 步骤 B: 通过子集规则推断新的句子
            new_inferences = []
            knowledge_copy = self.knowledge[:]  # 使用副本进行迭代
            for s1, s2 in itertools.combinations(knowledge_copy, 2):
                if s1.cells.issubset(s2.cells):
                    diff_cells = s2.cells - s1.cells
                    diff_count = s2.count - s1.count
                    inferred_sentence = Sentence(diff_cells, diff_count)
                    if inferred_sentence not in self.knowledge and inferred_sentence not in new_inferences:
                        new_inferences.append(inferred_sentence)
                        changes_made = True

            self.knowledge.extend(new_inferences)

            # 如果在一整个循环中没有任何改变，则知识库稳定
            if not changes_made:
                break

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        """
        safe_moves = self.safes - self.moves_made
        if safe_moves:
            # 使用 list 转换和 pop(0) 以确保每次返回一个确定的值，便于测试
            return list(safe_moves)[0]
        return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
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