import random
class LoanTrackerLite:
    def __init__(self, initcount, pmatrix):
        self.count = initcount #bins to count how many loans are in each state (C, D, V, L)
        self.matrix = pmatrix #2D  matrix to represent the transition probalities

        self.history = []  #list to hold every past iteration of count
        self.history.append(initcount) 
    
    #we have the option to insert a new probability matrix.
    #allows for the option to incorporate time dependant probabilities
    def updateMatrix(self, pmatrix):
        self.matrix = []
        for x in pmatrix:
            self.matrix.append(x)

    def getCount(self):
        return self.count

    def getMatrix(self):
        return self.matrix

    def getHistory(self):
        return self.history

    def step(self):
        new = [0, 0, 0, 0] #new counter

        #iterate through the bins in our count matrix
        for startindex, n in enumerate(self.count):
            #iterate through every individual loan
            for x in range(0, n):

                #for each loan, select a new bin for it to end in.
                r = random.random()
                for endindex, j in enumerate(self.matrix[startindex]):
                    #weighted random selector. subtract weights from the random
                    #number until we get under 0.
                    r = r - j
                    if (r <= 0):
                        new[endindex] += 1
                        break

        #replace old bin with new bin, and add to history
        self.history.append(new)
        self.count = new




def main():
    #initial probability matrix, and initial distribution of states
    pmatrix = [[.95, .01, .04, 0], [.2, .75, .03, .02], [0, 0, 1, 0], [0, 0, 0, 1]]
    initcount = [1000, 100, 0, 0]

    ltl = LoanTrackerLite(initcount, pmatrix)

    for i in range(0, 10):
        ltl.step()

    hist = ltl.getHistory()
    for index, row in enumerate(hist):
        print("#" + str(index))
        print(row)

    
main()