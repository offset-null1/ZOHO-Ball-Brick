
class Brick:
    def __init__(self, size: int) -> None:
        self.size = size
        self.mat = [[' ' for j in range(0, self.size)] for i in range(0, self.size)]
        self.ball = 0
        self.pos = self.size//2
        self.old = self.pos
        self.min_row = float('inf')
        self.min_col = float('inf')
        self.max_row = 0
        self.max_col = 0 
        self.B_flag = True
        self.B_loc = 0
        
    def construct(self) -> None:
        for j in range(self.size):
            self.mat[0][j] = 'W'

            if j == self.size//2:
                self.mat[self.size-1][j] = 'o'
            else:
                self.mat[self.size-1][j] = 'G'
            self.mat[j][0] = 'W'
            self.mat[j][self.size-1] = 'W'
                   
        print('\n'.join(['  '.join([str(i) for i in row]) for row in self.mat]))
        
                
    def display(self) -> None:      
        self.mat[self.size-1][self.old] = 'G'
        self.mat[self.size-1][self.pos] = 'o'
        print('\n'.join(['  '.join([str(i) for i in row]) for row in self.mat]))
        print(f"Ball count is {self.ball}.")
           
                       
    def operation(self, row: int, col: int) -> bool: 
        op = str(self.mat[row][col])   
                
        if op == "DE":
            self.mat[row][self.min_col : self.max_col+1] = ' '* (self.min_col - self.max_col + 2)
            if self.B_loc:
                self.mat[self.size-1][self.B_loc] = 'G'
                self.B_loc = 0
            return True
        
        if op == "DS":
            self.mat[row][col-1 : col+2] = ' '*3   #left,right and above of DS brick
            self.mat[row-1][col-1 : col+2] = ' '*3
            
            if self.B_loc:
                self.mat[self.size-1][self.B_loc] = 'G'
                self.B_loc = 0
            return True
        
        if op.isdigit():
            if self.mat[row][col] == 1:
                self.mat[row][col] = ' '
            else:    
                self.mat[row][col] -= 1
            
            if self.B_loc:
                self.mat[self.size-1][self.B_loc] = 'G' 
                self.B_loc = 0  
            return True
        
        if op == "B":
            self.mat[row][col] = ' '
            
            if self.B_flag:
                # if self.pos < self.size-2 and self.pos > 1:
                    self.mat[self.size-1][self.B_loc] = 'G'
                    self.B_loc = self.pos+1
                    self.mat[self.size-1][self.B_loc] = '_'
                    self.B_flag = False
            else:
                # if self.pos < self.size-2 and self.pos > 1:
                    self.mat[self.size-1][self.B_loc] = 'G'
                    self.B_loc = self.pos-1
                    self.mat[self.size-1][self.B_loc] = '_'
                    self.B_flag = True
            return True

        
        return False
        
        
    def ST(self) -> None:
        
        if self.pos > self.min_col and self.pos < self.max_col: #ball within the boundary of bricks
            """ 1) rows will change, column will remain mid for all rows
                2) No change in ball number 
                3) No change in ball position
            """
            
            for i in range(self.max_row):
                
                col = self.pos  # column straight to ball
                row = self.max_row-i               #rows will go bottom -> up
                
                touched_brick = self.operation(row, col)
                if touched_brick: break
        
    def LD(self) -> None:
      
        i = 0
        
        while 1:
            row = self.max_row - i               #rows will go bottom -> up
            col = self.pos - i - 1
            
            if col == 1 or col == self.size - 2 or row == 1: # ball touched wall 1st time
                
                for i in range(self.max_col):
                    touched_brick = self.operation(row, self.min_col+i)
                    if touched_brick:    
                        self.old = self.pos
                        self.pos = self.min_col+i
                        
                        if self.old != self.pos:
                           if not self.B_loc or self.pos != self.B_loc : 
                                self.ball -= 1
                                return

                self.ball -= 1
                self.old = self.pos 
                self.pos = self.size//2 #reset
                return 

            touched_brick = self.operation(row, col)
            if touched_brick: break
            i+=1        
        
        
        if self.B_loc != self.pos:        
            self.ball -= 1
                
        self.old = self.pos
        self.pos = 1 if self.pos-1 < 1 else self.pos-1
        # didn't cover the empty track
           
            

    def RD(self) -> None:
        count = 0
              # boundary = abs(min_col - self.pos - 1)
        i = 0
        while 1:
            row = self.max_row + i               #rows will go bottom -> up
            col = self.pos + i + 1

            if col == 1 or col == self.size - 2 or row == 1: # ball touched wall 1st time
                
                for i in range(self.max_col):
                    touched_brick = self.operation(row, self.max_col-i)
                    if touched_brick:    
                        self.old = self.pos
                        self.pos = self.max_col-i
                        
                        if self.old != self.pos:
                           if not self.B_loc or self.pos != self.B_loc : 
                                self.ball -= 1
                                return
                    
                self.ball -= 1 #ball touched wall twice 
                self.old = self.pos 
                self.pos = self.size//2 #reset
                return 

            touched_brick = self.operation(row, col)
            if touched_brick: break
            i+=1             
                    
        if self.B_loc != self.pos:        
            self.ball -= 1
        self.old = self.pos
        self.pos = self.size-2 if self.pos+1 > self.size-2 else self.pos+1 
        # didn't cover the empty track
           
        
        
    def getInput(self) -> None:
        flag = True
        
        while flag:
            i = input("Enter the bricks's position and brick type :").split()
            i[0],i[1] = int(i[0]), int(i[1])
            
            self.mat[i[0]][i[1]] = int(i[2]) if i[2].isdigit() else i[2]
            
            self.min_row = min(i[0], self.min_row)
            self.max_row = max(i[0], self.max_row)
            self.min_col = min(i[1], self.min_col)
            self.max_col = max(i[1], self.max_col)
           
            flag = True if input("Do you want to continue(Y or N)? :").upper() == 'Y' else False
        
        self.ball = int(input("Enter ball count: "))
        
        self.construct()
        
        
        
    def play(self):
        
        while self.ball > 0:
            direction = input("Enter the direction in which the ball need to traverse :")

            if direction == "ST":   
                self.ST()
                self.display()

            if direction == "LD":
                self.LD()
                self.display()


            if direction == "RD":
                self.RD()
                self.display()
            
          
            
b = Brick(7)
b.getInput()
b.play()             
            
            
            
            
            
        