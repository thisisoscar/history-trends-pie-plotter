import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def display_row():
    global index

    ax.clear()
    current_data = domain_counts_df.iloc[index]
    current_data = current_data.dropna()
    ax.pie(current_data, labels=current_data.index)
    ax.set_title(current_data.name)
    fig.canvas.draw()


def next_row(event):
    global index 
    index = (index + 1) % len(dates)
    display_row()

def prev_row(event):
    global index 
    index = (index - 1) % len(dates)
    display_row()


df = pd.read_csv(input('Enter the name/directory of the tsv file: ') + '.tsv', delimiter='\t', header=None)
df.columns = ['url', 'full domain', 'top domain', 'random number', 'datetime', 'another random number', 'transition', 'page title']
df['datetime'] = pd.to_datetime(df['datetime']).dt.date

dates = df.loc[:, 'datetime'].unique()

domain_counts_df = pd.DataFrame()

for i in dates:
    data = {}

    target_date = pd.to_datetime(i).date()
    filtered_df = df[df['datetime'] == target_date]
    filtered_df = filtered_df.loc[:, ['top domain']]

    domain_counts = filtered_df['top domain'].value_counts()

    domain_counts.name = i

    domain_counts_df = pd.concat([domain_counts_df, domain_counts.to_frame().T])

#domain_counts_df = domain_counts_df.fillna(0.0)

index = 0

fig, ax = plt.subplots()

fig.subplots_adjust(bottom=0.2)

previous_button = Button(plt.axes([0.58, 0.05, 0.15, 0.07]), 'Prev')
previous_button.on_clicked(prev_row)

next_button = Button(plt.axes([0.75, 0.05, 0.17, 0.07]), 'Next')
next_button.on_clicked(next_row)

display_row()

plt.show()