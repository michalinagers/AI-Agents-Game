In this project, I have:

- Created a game menu where user can choose which game they would like to play
- 6 different games types (Human VS Random, Human VS Smart, Human vs Mini-Max, Random VS Smart, Smart VS Mini-Max, Mini-Max VS ML)
- Games which are not being played by a human play for 500 times, which give us results and allows us to test the quality of agents and check for areas of improvement 
- Mini-Max agent consists of using Heuristic Evaluation Function, Iterative deepening and alpha-beta pruning 
- ML agent has a hyprid approach where 2 ML algorithms have been used which are Neural Networks and Random Forest. Based of a training dataset which the agent learns, the score is combined (0.6 Neural Networks + 0.3 Random Forest)
- After each game where human plays, a game tree visualisation can be seen after the game which shows each player's step (this is not appropriate for agent vs agent games as the game tree would show 500 times after each game)
- After each agent vs agent game, a pie chart can be seen with metrics of how many wins / looses / draws 
- Accuracy metrics of Random Forest can be seen once loaded during Mini-Max VS ML agent 

- main.py: Game menu and entry point
- randomAgent.py: Random Agent implementation
- smartAgent.py: Smart Agent implementation
- minimaxAgent.py: Mini-Max Agent with alpha-beta pruning, iterative deepening (max depth 4), heuristic evaluation function
- MLagent.py: ML Agent with hybrid NN+RF model
- gameTreeVisualisation.py: Game tree visualization
- piechart.py: Pie chart for performance metrics
- connect_four_dataset.pkl: Custom dataset for ML training

I have used a custom dataset for ML learning which learns from the smart and minimax agent. I have not used the dataset provided in the assessment brief as I believe that it was not suitable for my approach (NN + RF).
After starting the game, the ML model is not being trained as I have trained the agent and stored the models in a file (nn_model.5h and connect_four_dataset.pkl). I have done this as training the model takes a very long time (approx. 1 hour) as my Mini-Max agent is very in depth, and video recording it within 12 minutes would not be possible. 

To load the code, different types of Python libraries are needed. I have used:

numpy, pandas, tensorflow, scikit-learn, matplotlib, networkx, tqdm

References:

https://docs.python.org/3/library/pickle.html

https://www.geeksforgeeks.org/understanding-python-pickling-example/

https://www.datacamp.com/tutorial/random-forests-classifier-python

https://www.activestate.com/resources/quick-reads/how-to-create-a-neural-network-in-python-with-and-without-keras/

https://networkx.org/documentation/stable/tutorial.html

https://www.w3schools.com/python/ref_func_len.asp