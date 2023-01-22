import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd


def setup_font(plt):
    font_path = 'fonts/LinLibertine_R.ttf'  # Your font path goes here
    font_manager.fontManager.addfont(font_path)
    prop = font_manager.FontProperties(fname=font_path)

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams.update({'font.size': 14})
    plt.rcParams['font.sans-serif'] = prop.get_name()
    return plt

def plot_overall_sentiment(data, filename):
    import matplotlib.pyplot as plt
    
    # Setup Font
    plt = setup_font(plt)
    
    # Set x_labels and bar_colors
    x_labels = ['Negative', 'Neutral', 'Positive']
    bar_colors = ['red', 'orange', 'green']

    # Create the bar chart with the given data and colors
    plt.bar(x_labels, data, color=bar_colors, edgecolor='black', alpha=0.7)

    # Add the x and y labels
    plt.xlabel('Sentiment')
    plt.ylabel('# Tweets')
    
    # Save as svg and png
    for f_type in [".svg", ".png"]:
        plt.savefig(filename+f_type, dpi=300, bbox_inches='tight')
        
    # Show the chart
    plt.show()
    

def plot_sentiment(df, filename):
    import matplotlib.pyplot as plt
    
    # Setup Font
    plt = setup_font(plt)
    
    # Group the data by party and sentiment, unstack to create a table
    data = df.groupby(['party'])['sentiment'].value_counts().unstack()
    # Normalize the data so that each column sums to 100
    data = data.div(data.sum(axis=1), axis=0).mul(100)
    # Round values to 1 decimal place
    data = data.applymap(lambda x: round(x, 1))

    # Get the overall sentiment values
    combined_data = df['sentiment'].value_counts()
    # Format the data as a DataFrame and normalize
    combined_data = pd.DataFrame(combined_data).T.rename(index={'sentiment': 'Combined'})/combined_data.sum()*100
    # Round the values to 1 decimal place
    combined_data = combined_data.applymap(lambda x: round(x, 1))

    # Combine the total and party-specific data
    data_total = pd.concat([combined_data, data], axis=0)
    # Reorder columns
    data_total = data_total[["negative", "neutral", "positive"]]
    
    data_total = data_total.reindex(["Combined", "SPD", "CDU/CSU", "Grüne", "FDP", "AfD", "Die Linke"])

    # Create chart
    ax = data_total.plot(kind='bar', stacked=True, color=['red', 'grey', 'green'], width=0.8)

    for c in ax.containers:
        # Add custom label to the bars
        ax.bar_label(c, label_type='center', color='white', weight='bold', fontsize=14)

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Sentiment")
    plt.xticks(rotation=0)
    plt.ylabel('Proportion')
    plt.xlabel('Party')
    
    # Save as svg and png
    for f_type in [".svg", ".png"]:
        plt.savefig(filename+f_type, dpi=300, bbox_inches='tight')
        
    plt.show()
