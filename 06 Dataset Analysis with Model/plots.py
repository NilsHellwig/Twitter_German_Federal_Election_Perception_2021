import matplotlib.pyplot as plt
from matplotlib import font_manager
import pandas as pd

PARTY_COLORS = {'SPD': '#E3000F', 'CDU/CSU': '#000000',  'Grüne': '#1AA037',
                'Die Linke': '#800080', 'FDP': '#FFEF00', 'AfD': '#0489DB', }
PARTY_ORDER = ["SPD", "CDU/CSU", "Grüne", "FDP", "AfD", "Die Linke"]
POSITIVE_COLOR = "#006600"
NEGATIVE_COLOR = "#FF0000"
NEUTRAL_COLOR = "#999999"
MONTH_NAMES = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May',
               6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'}

FONT_PATH = 'fonts/LinLibertine_R.ttf'

def setup_font(plt):
    font_manager.fontManager.addfont(FONT_PATH)
    prop = font_manager.FontProperties(fname=FONT_PATH)

    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams.update({'font.size': 14})
    plt.rcParams['font.sans-serif'] = prop.get_name()
    return plt


def plot_overall_sentiment(data, filename, len_dataset):
    import matplotlib.pyplot as plt

    # Setup Font
    plt = setup_font(plt)

    # Set x_labels and bar_colors
    x_labels = ['Negative', 'Neutral', 'Positive']
    bar_colors = [NEGATIVE_COLOR, NEUTRAL_COLOR, POSITIVE_COLOR]

    # Create the bar chart with the given data and colors
    plt.bar(x_labels, data, color=bar_colors)

    # Add the x and y labels
    plt.xlabel('Sentiment')
    plt.ylabel('# Tweets')
    
    plt.ylim(0, 420000)
    
    # Add labels to each bar
    for i in range(len(data)):
        plt.text(x_labels[i], data[i], "{:.1%}".format(data[i] / len_dataset), ha='center', va='bottom', fontsize=14)

    # Save as svg, png and pdf
    for f_type in [".svg", ".png", ".pdf"]:
        plt.savefig(filename+f_type, dpi=300, bbox_inches='tight')

    # Show the chart
    plt.show()

def plot_overall_opposition_government_sentiment(general_count, government_count, opposition_count, filename):
    import matplotlib.pyplot as plt
    
    # Setup Font
    plt = setup_font(plt)

    # Set x_labels and bar_colors
    x_labels = ['Negative', 'Neutral', 'Positive']
    bar_colors = [NEGATIVE_COLOR, NEUTRAL_COLOR, POSITIVE_COLOR]

    # Create a figure with 1 row and 3 columns of plots
    fig, axs = plt.subplots(1, 3)
    fig.subplots_adjust(wspace=0.3)

    # Create the first bar chart for the general corpus
    axs[0].bar(x_labels, general_count, color=bar_colors)
    axs[0].set_title("Overall")

    # Create the second bar chart for government
    axs[1].bar(x_labels, government_count, color=bar_colors)
    axs[1].set_title("Government")

    # Create the third bar chart for opposition
    axs[2].bar(x_labels, opposition_count, color=bar_colors)
    axs[2].set_title("Opposition")

    fig.set_figwidth(12)
    fig.set_figheight(4)

    # Save as svg, png and pdf
    for f_type in [".svg", ".png", ".pdf"]:
        plt.savefig(filename+f_type, dpi=300, bbox_inches='tight')

    # Show the figure
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
    combined_data = pd.DataFrame(combined_data).T.rename(
        index={'sentiment': 'Combined'})/combined_data.sum()*100
    # Round the values to 1 decimal place
    combined_data = combined_data.applymap(lambda x: round(x, 1))

    # Combine the total and party-specific data
    data_total = pd.concat([combined_data, data], axis=0)
    # Reorder columns
    data_total = data_total[["Negative", "Neutral", "Positive"]]

    data_total = data_total.reindex(
        ["Combined", "SPD", "CDU/CSU", "Grüne", "FDP", "AfD", "Die Linke"])

    # Create chart
    ax = data_total.plot(kind='bar', stacked=True, color=[
                         NEGATIVE_COLOR, NEUTRAL_COLOR, POSITIVE_COLOR], width=0.8)

    for c in ax.containers:
        # Add custom label to the bars
        ax.bar_label(c, label_type='center', color='white',
                     weight='bold', fontsize=14)

    #plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Sentiment")
    legend = plt.legend()
    if legend is not None:
        legend.remove()
    
    plt.xticks(rotation=0)
    plt.ylabel('% Proportion')
    plt.xlabel('Party')

    # Save as svg, png and pdf
    for f_type in [".svg", ".png", ".pdf"]:
        plt.savefig(filename+f_type, dpi=300, bbox_inches='tight')

    plt.show()


def plot_sentiment_line_graph_for_each_month(df, filename):
    import matplotlib.pyplot as plt

    # Setup Font
    plt = setup_font(plt)

    # Set figure size and font size
    plt.figure(figsize=(15, 6))
    plt.rcParams.update({'font.size': 16})

    # Plot the sentiment value for each party and month
    for party in PARTY_ORDER:
        plt.plot(df.loc[df['party'] == party, 'month'], df.loc[df['party'] ==
                 party, 'sentiment_value'], label=party, color=PARTY_COLORS[party])

    # Set x-axis tick labels to month names
    plt.xticks(range(1, 13), [MONTH_NAMES[i] for i in range(1, 13)])

    # Add legend, axis labels and title
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xlabel('Month')
    plt.ylabel('Mean Sentiment', x=-2)

    plt.grid(alpha=0.5)

    # Add labels for the positive and negative y-axis directions
    plt.text(-0.3, -0.35, 'Positive →', ha='center', va='center',
             rotation='vertical', fontsize=14, color=POSITIVE_COLOR)
    plt.text(-0.3, -0.55, '← Negative', ha='center', va='center',
             rotation='vertical', fontsize=14, color=NEGATIVE_COLOR)

    # Set y-axis limit
    plt.ylim(-0.625, -0.275)

    # Add a vertical line to mark the election month
    plt.axvline(x=9, color='grey', linestyle='--')
    plt.text(7.25, -0.325, 'Election Month', rotation=0)

    # Save as svg, png and pdf
    for f_type in [".svg", ".png", ".pdf"]:
        plt.savefig(filename+f_type, dpi=300, bbox_inches='tight')

    plt.show()

def plot_sentiment_line_graph_for_each_month_6_week(df, filename):
    import matplotlib.pyplot as plt

    # Setup Font
    plt = setup_font(plt)

    # Set figure size and font size
    plt.figure(figsize=(15, 6))
    plt.rcParams.update({'font.size': 16})

    # Plot the sentiment value for each party and month
    for party in PARTY_ORDER:
        plt.plot(df.loc[df['party'] == party, 'first_day_week'], df.loc[df['party'] == party, 'sentiment_value'], label=party, color=PARTY_COLORS[party])

    # Set x-axis tick labels to month names
    plt.xticks(rotation=90)

    # Add legend, axis labels and title
    plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
    plt.xlabel('Week')
    plt.ylabel('Mean Sentiment')

    plt.grid(alpha=0.5)

    # Add labels for the positive and negative y-axis directions
    plt.text(-1.2, -0.1, 'Positive →', ha='center', va='center', rotation='vertical', fontsize=14, color=POSITIVE_COLOR)
    plt.text(-1.2, -0.6, '← Negative', ha='center', va='center', rotation='vertical', fontsize=14, color=NEGATIVE_COLOR)

    # Set y-axis limit
    plt.ylim(-0.75, 0.05)

    # Add a vertical line to mark the election month
    plt.axvline(x=6, color='grey', linestyle='--')
    plt.text(6.35, -0.025, 'Election Day', rotation=0)

    # Save as svg, png and pdf
    for f_type in [".svg", ".png", ".pdf"]:
        plt.savefig(filename+f_type, dpi=300, bbox_inches='tight')

    plt.show()