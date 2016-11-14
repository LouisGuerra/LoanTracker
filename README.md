# LoanTracker

2 scripts. The first, LoanTrackerLite.py, takes a distribution of states and evolves it through time according to the transition probabilities. I used probabilities that I found in a mortgage credit primer.

The other, LoanTracker.py, is a bit more involved. It creates a list of individual loan objects that each has their own probability matrix, and each keeps a history log of its states. I know in practice each loan would be initialized using external data, but since I had none, I created unique probability matrices by using a randomized fuzzing function on the matrix from the primer. The system evolves by calling a step function on each individual loan, and keeping count of the distribution of states after each step.

