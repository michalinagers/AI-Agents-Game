import matplotlib.pyplot as plt
import pandas as pd


def createPieChart(sizes, labels=None, title="Connect 4 Game Statistics"):

    if labels is None:
        labels = ['Player 1 Wins', 'Player 2 Wins', 'Draws']
    
    fig = plt.figure(figsize=(10, 10))
    colors = ('crimson', 'cyan', 'yellow')
    explode = (0.1, 0.1, 0.1)
    wedgeprops = {'linewidth': 2, 'edgecolor': "black"}
    textprops = {'fontstyle': 'italic', 'fontweight': 'bold'}
    
    plt.pie(sizes,
           labels=labels,
           autopct='%1.1f%%',
           startangle=45,
           colors=colors,
           explode=explode,
           shadow=True,
           wedgeprops=wedgeprops,
           textprops=textprops)
    
    plt.legend(title="Game Results")
    plt.title(title, loc='center', color='black', fontsize=25, fontweight='bold')
    plt.axis('equal')
    return fig
        
plt.legend(title="Game Results")
plt.title("Connect 4 Game Statistics", loc='center', color='black', fontsize=25, fontweight='bold')
plt.axis('equal')

