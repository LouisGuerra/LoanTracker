import random

#class to represent loans
class Loan:
    def __init__(self, loanid, state, pmatrix):
        self.id = loanid  #unique id number for each loan
        self.state = state  #current states

        #individual probability matrix.
        #written in this roundabout way to ensure immutability.
        self.matrix = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for index, row in enumerate(pmatrix): 
            self.matrix[index] = row

        #history of past states, we add to it anytime we take a step.
        #just in case we need to track how a loan evolves
        self.history = []  
        self.history.append(state) 

    #like in the lite version, we leave this method in case we want to incorporate 
    #time dependant matrices later on
    def updateMatrix(self, pmatrix):
        self.matrix = []
        for x in pmatrix:
            self.matrix.append(x)

    def getId(self):
        return self.id

    def getState(self):
        return self.state

    def getMatrix(self):
        return self.matrix

    def getHistory(self):
        return self.history

    def step(self):
        #for each loan, select a new state for it to move to.
        r = random.random()
        for stateindex, j in enumerate(self.matrix[self.state]):
            #weighted random selector. subtract weights from the random
            #number until we get under 0.
            r = r - j
            if (r <= 0):
                self.state = stateindex  #update state, add it to hist
                self.history.append(self.state)
                break

#class to track loans
class LoanTracker:
    def __init__(self, loans):
        self.loans = loans   #lisst of loans

        self.count = [0, 0, 0, 0] #initiliaze/populate the counter array
        for loan in loans:  
            self.count[loan.getState()] += 1

        self.history = []  #list to hold every past iteration of count
        self.history.append(self.count) 

    #recount the states
    def updateCount(self):
        self.count = [0, 0, 0, 0]
        for loan in self.loans:  #populate the counting array
            self.count[loan.getState()] += 1
    
    def getCount(self):
        return self.count

    def getMatrix(self):
        return self.matrix

    def getHistory(self):
        return self.history

        #increment time by callin step on every loan
    def step(self):
        for loan in self.loans:
            loan.step()

        #update count and add to history
        self.updateCount()
        self.history.append(self.count)

#standard normalization of a vector to keep probabilities summing to 1.
def normalize(vector):
    out = []
    total = sum(vector)
    for x in vector:
        out.append(x/total)
    return out

#fuzzes up a matrix by randomly adding or subtracting 50% from each value.
#then renormalizes each row.
def randomMatrix(pmatrix):
    out = [[0,0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i, row in enumerate(pmatrix):
        for index, p in enumerate(row):
            out[i][index] = p/2 + (p*random.random())

        out[i] = normalize(out[i])
    return out


#this function will create loans for us to test our simulation with. 
#in reality, I imagine we'd parse these from a csv file or something, but this
#will do for now
def createLoans():
    loans = []
    pmatrix = [[.95, .01, .04, 0], [.2, .75, .03, .02], [0, 0, 1, 0], [0, 0, 0, 1]]
    #we'll create 1000 in state 0
    for i in range(0, 1000):
        new = Loan(i, 0, randomMatrix(pmatrix))
        loans.append(new)
    #and 100 in state 1
    for i in range(1000, 1100):
        new = Loan(i, 1, randomMatrix(pmatrix))
        loans.append(new)

    return loans

def main():    
    loans = createLoans() 
    lt = LoanTracker(loans)  
    #run the simulation for 10 steps
    for i in range(0, 10):
        lt.step()

    #get and print history
    hist = lt.getHistory()
    for index, row in enumerate(hist):
        print("#" + str(index))
        print(row)

main()