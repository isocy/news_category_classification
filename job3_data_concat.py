import pandas as pd
import glob

csv_file_paths = glob.glob('./crawling_data/*')

df_title_category = pd.DataFrame()
for csv_file_path in csv_file_paths:
    if csv_file_path == './crawling_data\\naver_all_news.csv':
        continue
    df_segment = pd.read_csv(csv_file_path)
    if len(df_segment.columns) == 3:
        df_segment = df_segment.iloc[:, 1:]
    df_title_category = pd.concat([df_title_category, df_segment], ignore_index=True)
df_title_category.to_csv('./crawling_data/naver_all_news.csv', index=False)
