import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd

pd.set_option('display.max_rows', None)  # Show all rows
pd.set_option('display.max_columns', None)  # Show all columns

df = pd.read_csv('tiki_test.csv')
# print(df.head(5))
# print(df.info())
df['Sign-up Time'] = pd.to_datetime(df['Sign-up Time'])
df['Activation Time'] = pd.to_datetime(df['Activation Time'])
df['1st Listing'] = pd.to_datetime(df['1st Listing'])
df['1st Salable'] = pd.to_datetime(df['1st Salable'])
df['1st Transaction'] = pd.to_datetime(df['1st Transaction'])

# Data Aggregation
columns = ['Main Category', 'Sign-up to Activation', 'Sign-up to Transaction', 'Sign-up to Listing',
           'Sign-up to Salable', 'Activation to Listing',
           'Listing to Salable', 'Salable to Transaction']
df2 = df[columns]
grouped_data = df2.groupby('Main Category').mean()
grouped_data = grouped_data.reset_index()
# print(grouped_data)

# Compare duration of Segment by Category


class Bars:
    def __init__(self, data, m, n):
        self.data = data
        self.m = m
        self.n = n
        self.fig, self.axs = plt.subplots(m, n, sharey='all', sharex='all', figsize=(n * 3, m * 5))

    def bar_chart(self, i, j, column1, column2, title_size=6, tick_size=4):
        # Select the subplot
        ax = self.axs[i, j] if self.m > 1 and self.n > 1 else (self.axs[i] if self.m > 1 else self.axs[j])
        bars = ax.bar(self.data[column1], self.data[column2], color='lightblue')
        title = f"Avg of {column2} duration by {column1} (Days)"
        ax.set_title(title, fontsize=title_size)
        ax.tick_params(axis='both', labelsize=tick_size)
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.1f}",
                    ha='center', va='bottom', fontsize=5, color='red')
        return ax


dt = Bars(grouped_data, 4, 1)
dt.bar_chart(0, 0, 'Main Category', 'Sign-up to Activation')
dt.bar_chart(1, 0, 'Main Category', 'Activation to Listing')
dt.bar_chart(2, 0, 'Main Category', 'Listing to Salable')
dt.bar_chart(3, 0, 'Main Category', 'Salable to Transaction')
plt.subplots_adjust(top=0.939, bottom=0.006, left=0.1, right=0.868, hspace=0.286, wspace=0.14)
plt.show()


segments = grouped_data['Main Category']
bottom_values = {
    'Sign-up to Activation': 0,
    'Activation to Listing': grouped_data['Sign-up to Activation'],
    'Listing to Salable': grouped_data['Sign-up to Activation'] + grouped_data['Activation to Listing'],
    'Salable to Transaction':
    grouped_data['Sign-up to Activation'] + grouped_data['Activation to Listing'] + grouped_data['Listing to Salable']
}
colors = sns.color_palette('Set3', 4)
plt.bar(segments, grouped_data['Sign-up to Activation'], color=colors[0],
        bottom=bottom_values['Sign-up to Activation'],
        label='Sign-up to Activation')
plt.bar(segments, grouped_data['Activation to Listing'], color=colors[1],
        bottom=bottom_values['Activation to Listing'],
        label='Activation to Listing')
plt.bar(segments, grouped_data['Listing to Salable'], color=colors[2],
        bottom=bottom_values['Listing to Salable'],
        label='Listing to Salable')
plt.bar(segments, grouped_data['Salable to Transaction'], color=colors[3],
        bottom=bottom_values['Salable to Transaction'],
        label='Salable to Transaction')
plt.legend(loc='upper left', bbox_to_anchor=(1, 1))

plt.show()

# Distribution of Account
count_df = df.groupby('Sign-up Time').size().reset_index(name='Count')
count_df['Month'] = count_df['Sign-up Time'].dt.month
# print(count_df)
count_df['Sign-up Time'] = pd.to_datetime(count_df['Sign-up Time'])
total_signup = count_df['Count'].sum()
mean = count_df['Count'].mean()
median = count_df['Count'].median()
pct_90 = count_df['Count'].quantile(0.90)

sns.boxplot(x='Month', y='Count', data=count_df, palette='Set2')
plt.text(7.5, 42,
         f' total= {total_signup} \n mean={mean:.2f} \n median={median:.2f} \n pct_90={pct_90}',
         fontsize=7, color='black', bbox=dict(edgecolor='black', alpha=0.2))
plt.title('Distribution Number of Account ')
plt.xlabel('Month')
plt.show()

# Num of Account over Time
sns.lineplot(x='Sign-up Time', y='Count', data=count_df, color='blue')
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
plt.gcf().autofmt_xdate()
plt.title('Num of Account over Time')
plt.show()

# Analysis Sign-up to Transaction duration by Category
kwg = dict(bins=50, histtype='bar', alpha=0.5, edgecolor='black', density=False)
fig, axs = plt.subplots(5, 1, figsize=[5, 10])

x0 = df.loc[df['Main Category'] == 'BBFF', 'Sign-up to Transaction']
axs[0].hist(x0, **kwg, label='Sign-up to Activation')
axs[0].set_title('Distribution of Sign-up to Transaction(days) of BBFF', fontsize=5)
axs[0].tick_params(axis='both', labelsize=5)

x1 = df.loc[df['Main Category'] == 'Book', 'Sign-up to Transaction']
axs[1].hist(x1, **kwg, label='Sign-up to Transaction')
axs[1].set_title('Distribution of Sign-up to Transaction(days) of Book', fontsize=5)
axs[1].tick_params(axis='both', labelsize=5)


x2 = df.loc[df['Main Category'] == 'Digital Service', 'Sign-up to Transaction']
axs[2].hist(x2, **kwg, label='Sign-up to Transaction')
axs[2].set_title('Distribution of Sign-up to Transaction(days) of Service', fontsize=5)
axs[2].set_ylabel('Count', fontsize=7)
axs[2].tick_params(axis='both', labelsize=5)


x3 = df.loc[df['Main Category'] == 'Electronic', 'Sign-up to Transaction']
axs[3].hist(x3, **kwg, label='Sign-up to Transaction')
axs[3].set_title('Distribution of Sign-up to Transaction(days) of Electronic', fontsize=5)
axs[3].tick_params(axis='both', labelsize=5)

x4 = df.loc[df['Main Category'] == 'LifeStyle', 'Sign-up to Transaction']
axs[4].hist(x4, **kwg, label='Sign-up to Transaction')
axs[4].set_title('Distribution of Sign-up to Transaction(days) of LifeStyle', fontsize=5)
axs[4].set_xlabel('Days', fontsize=7)
axs[4].tick_params(axis='both', labelsize=5)

plt.tight_layout()
plt.show()
