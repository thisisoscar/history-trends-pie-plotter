import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

def display_row():
    global index

    ax.clear()
    current_data = domain_counts_df.iloc[index]
    current_data = current_data.dropna()
    current_data = current_data.sort_values(ascending=False)
    ax.pie(current_data, labels=current_data.index)
    ax.set_title(current_data.name)
    fig.canvas.draw()


def next_row(event):
    global index 
    index = (index + 1) % len(domain_counts_df.index)
    display_row()


def prev_row(event):
    global index 
    index = (index - 1) % len(domain_counts_df.index)
    display_row()


def is_ip(string, return_ip=False):
    try:
        if type(string) != str:
            raise ValueError

        if string.startswith('http://'):
            string = string[7:]

        if '/' in string:
            string = string.split('/')[0]

        numbers = string.split('.')
        
        if ':' in string:
            numbers[-1], port = numbers[-1].split(':')
            if 0 <= int(port) <= 65536:
                pass
            else:
                raise ValueError
        
        if len(numbers) != 4:
            raise ValueError
        
        for i in numbers:
            if 0 <= int(i) <= 255:
                pass
            else:
                raise ValueError
        
        if return_ip:
            ip = '.'.join(numbers)
            if ':' in string:
                ip += ':' + port
            return ip
        else:
            return True
    
    except ValueError:
        if return_ip:
            return None
        else:
            return False


def extract_ip(string):
    full_ip = is_ip(string, return_ip=True)
    ip = full_ip.split('/')[0]
    return ip


df = pd.read_csv(input('Enter the name/directory of the tsv file (exclude .tsv): ') + '.tsv', delimiter='\t', header=None)
df.columns = ['url', 'full domain', 'top domain', 'random number', 'datetime', 'another random number', 'transition', 'page title']
df['datetime'] = pd.to_datetime(df['datetime']).dt.date

def add_extension_visits(row):
    if row.isna()[2]: # 2 = top domain
        
        if row[0].startswith('chrome-extension'):
            row['top domain'] = 'chrome-extension://' + row['full domain']
        
        elif is_ip(row['url']):
            row['top domain'] = extract_ip(row['url'])
        
        else:
            row['top domain'] = row['url']
    
    return row

df = df.apply(add_extension_visits, axis=1)

dates = df.loc[:, 'datetime'].unique()
dates[::-1].sort()

domain_counts_df = pd.DataFrame()

domain_counts = df.loc[:, 'top domain'].value_counts()
domain_counts.name = 'all time'
domain_counts = domain_counts.rename(lambda x: f'{x}\n({domain_counts[x]})')
domain_counts_df = pd.concat([domain_counts_df, domain_counts.to_frame().T])

for i in dates:
    target_date = pd.to_datetime(i).date()
    filtered_df = df[df['datetime'] == target_date]
    filtered_df = filtered_df.loc[:, ['top domain']]

    domain_counts = filtered_df['top domain'].value_counts()
    domain_counts.name = i
    domain_counts = domain_counts.rename(lambda x: f'{x}\n({domain_counts[x]})')
    domain_counts_df = pd.concat([domain_counts_df, domain_counts.to_frame().T])


index = 0

fig, ax = plt.subplots()

fig.subplots_adjust(bottom=0.2)

previous_button = Button(plt.axes([0.58, 0.05, 0.15, 0.07]), 'Day After')
previous_button.on_clicked(prev_row)

next_button = Button(plt.axes([0.75, 0.05, 0.17, 0.07]), 'Day Before')
next_button.on_clicked(next_row)

display_row()

plt.show()