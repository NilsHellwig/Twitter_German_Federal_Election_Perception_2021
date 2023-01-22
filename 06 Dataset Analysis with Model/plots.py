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


def plot_overall_sentiment(data, filename):
    import matplotlib.pyplot as plt

    # Setup Font
    plt = setup_font(plt)

    # Set x_labels and bar_colors
    x_labels = ['Negative', 'Neutral', 'Positive']
    bar_colors = [NEGATIVE_COLOR, NEUTRAL_COLOR, POSITIVE_COLOR]

    # Create the bar chart with the given data and colors
    plt.bar(x_labels, data, color=bar_colors, edgecolor='black', alpha=0.7)

    # Add the x and y labels
    plt.xlabel('Sentiment')
    plt.ylabel('# Tweets')

    # Save as svg, png and pdf
    for f_type in [".svg", ".png", ".pdf"]:
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

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), title="Sentiment")
    plt.xticks(rotation=0)
    plt.ylabel('Proportion')
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
    plt.figure(figsize=(15, 8))
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
    plt.text(-0.2, 0.18, 'Positive →', ha='center', va='center',
             rotation='vertical', fontsize=14, color=POSITIVE_COLOR)
    plt.text(-0.2, -0.18, '← Negative', ha='center', va='center',
             rotation='vertical', fontsize=14, color=NEGATIVE_COLOR)

    # Set y-axis limit
    plt.ylim(-0.3, 0.3)

    # Add a vertical line to mark the election month
    plt.axvline(x=9, color='grey', linestyle='--')
    plt.text(9.25, 0.2, 'Election Month', rotation=0)

    # Save as svg, png and pdf
    for f_type in [".svg", ".png", ".pdf"]:
        plt.savefig(filename+f_type, dpi=300, bbox_inches='tight')

    plt.show()

def plot_sentiment_line_graph_for_each_month_6_week(df, filename):
    import matplotlib.pyplot as plt

    # Setup Font
    plt = setup_font(plt)

    # Set figure size and font size
    plt.figure(figsize=(15, 8))
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
    plt.text(-1.25, 0.18, 'Positive →', ha='center', va='center', rotation='vertical', fontsize=14, color=POSITIVE_COLOR)
    plt.text(-1.25, -0.18, '← Negative', ha='center', va='center', rotation='vertical', fontsize=14, color=NEGATIVE_COLOR)

    # Set y-axis limit
    plt.ylim(-0.4, 0.4)

    # Add a vertical line to mark the election month
    plt.axvline(x=6, color='grey', linestyle='--')
    plt.text(6.25, 0.25, 'Election Day', rotation=0)

    # Save as svg, png and pdf
    for f_type in [".svg", ".png", ".pdf"]:
        plt.savefig(filename+f_type, dpi=300, bbox_inches='tight')

    plt.show()