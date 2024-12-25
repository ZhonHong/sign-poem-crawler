import requests
from bs4 import BeautifulSoup
import time
import random

# 設置 Headers 模擬瀏覽器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 初始化索引
index = 1
sql_statements = []  # 用於存儲 SQL 插入語句

# 遍歷 1 到 100 的 URL
for i in range(1, 101):
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
        # 找到第一個 <tbody>
        tbody = soup.find("tbody")
        if tbody:
            # 遍歷所有 <tr>
            for tr in tbody.find_all("tr"):
                # 檢查是否包含 "籤詩翻譯"
                if "籤詩翻譯" in tr.get_text():
                    content = tr.get_text(separator="\n", strip=True)
                    print(f"Index: {index}")
                    print(content)
                    print("-" * 50)  # 分隔線

                    # 生成 SQL 插入語句
                    sql_statement = f"INSERT INTO table_name (id, content) VALUES ({index}, '{content.replace('\'', '\'\'')}');"
                    sql_statements.append(sql_statement)

                    index += 1  # 增加索引
        else:
            print(f"URL: {url} - 未找到 <tbody> 標籤。")
    else:
        print(f"請求失敗，狀態碼：{response.status_code}")

    # 隨機延遲
    time.sleep(random.uniform(1, 3))

# 將 SQL 語句保存到文件
with open("insert_data.sql", "w", encoding="utf-8") as file:
    file.write("\n".join(sql_statements))

print("資料已保存至 insert_data.sql")
