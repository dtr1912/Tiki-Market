import pandas as pd

sales = pd.read_csv('sales.csv')
award = pd.read_csv('award.csv')
product = pd.read_csv('product_history.csv')
df_1a = pd.read_csv('1a.csv')
df_1b = pd.read_csv('1b.csv')
df_2a = pd.read_csv('2a.csv')
df_2b = pd.read_csv('2b.csv')

markdown_sales = sales.to_markdown(index=False)
markdown_award = award.to_markdown(index=False)
markdown_product = product.to_markdown(index=False)
markdown_1a = df_1a.to_markdown(index=False)
markdown_1b = df_1b.to_markdown(index=False)
markdown_2a = df_2a.to_markdown(index=False)
markdown_2b = df_2b.to_markdown(index=False)

combined_markdown = f"""
#sales
{markdown_sales}

#award
{markdown_award}

#product_history
{markdown_product}

# 1a
{markdown_1a}

# 1b
{markdown_1b}

# 2a
{markdown_2a}

# 2b
{markdown_2b}
"""

# Ghi nội dung Markdown vào tệp
with open('data.md', 'w') as f:
    f.write(combined_markdown)
