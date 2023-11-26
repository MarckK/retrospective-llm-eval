# Renaming 'crafted' column to 'WithheldQA' in the latest dataset
latest_data.rename(columns={'crafted': 'WithheldQA'}, inplace=True)

# Plotting the data with color between the lines
plt.figure(figsize=(12, 6))

# Plotting TruthfulQA and WithheldQA data
plt.plot(latest_data['year'], latest_data['TruthfulQA'], label='TruthfulQA', marker='o')
plt.plot(latest_data['year'], latest_data['WithheldQA'], label='WithheldQA', marker='o')
plt.fill_between(latest_data['year'], latest_data['TruthfulQA'], latest_data['WithheldQA'], color='skyblue', alpha=0.3)

# Adding model names above points
for i in range(len(latest_data)):
    plt.text(latest_data['year'].iloc[i], latest_data['TruthfulQA'].iloc[i], latest_data['Model'].iloc[i], ha='right')
    plt.text(latest_data['year'].iloc[i], latest_data['WithheldQA'].iloc[i], latest_data['Model'].iloc[i], ha='right')

# Formatting the date axis
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
plt.gca().xaxis.set_major_locator(mdates.YearLocator())

# Adding labels and title
plt.xlabel('Date')
plt.ylabel('Percentage')
plt.title('TruthfulQA and WithheldQA Responses Over Time by Model')
plt.xticks(rotation=45)
plt.legend()

# Show the plot
plt.tight_layout()
plt.show()
