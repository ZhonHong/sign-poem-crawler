import requests
from bs4 import BeautifulSoup
import time
import random
import re  # 用於正則表達式匹配

# 設置 Headers 模擬瀏覽器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 初始化索引
index = 1
sql_statements = []  # 用於存儲 SQL 插入語句

# 遍歷 1 到 100 的 URL
for i in range(1, 101):  # 遍歷頁面
    url = f"https://fate.superd.org/{i}/"

    # 重試機制
    for attempt in range(3):
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            break
        except requests.exceptions.RequestException as e:
            print(f"重試 {attempt + 1} 次失敗: {e}")
            time.sleep(2)
    else:
        print(f"URL: {url} - 請求失敗")
        continue

    # 檢查請求是否成功
    if response.status_code == 200:
        # 解析 HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # 找到 <h1 class="entry-title">
        entry_title = soup.find("h1", class_="entry-title")
        if entry_title:
            # 提取內容，匹配從 "第一籤" 到 "第一百籤" 開始到括號結束的部分
            match = re.search(r"(第[一二三四五六七八九十百]+籤.*?\))", entry_title.get_text())
            if match:
                title = match.group(1)
                print(f"Index: {index}")
                print(f"URL: {url}")
                print(title)  # 打印匹配的部分
                print("-" * 50)  # 分隔線

                # 生成 SQL 插入語句
                sql_statement = f"INSERT INTO HCJFDG.Poem (id, title) VALUES ({index}, '{title.replace('\'', '\'\'')}');"
                sql_statements.append(sql_statement)

                index += 1  # 增加索引
        else:
            print(f"URL: {url} - 未找到 entry-title 標籤。")
    else:
        print(f"請求失敗，狀態碼：{response.status_code}")

    # 隨機延遲
    time.sleep(random.uniform(1, 3))

# 將 SQL 語句保存到文件
with open("insert_poem.sql", "w", encoding="utf-8") as file:
    file.write("\n".join(sql_statements))

print("資料已保存至 insert_poem.sql")
