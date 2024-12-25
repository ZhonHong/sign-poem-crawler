import requests
from bs4 import BeautifulSoup
import time
import random

# 設置 Headers 模擬瀏覽器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0 Safari/537.36"
}

# 初始化索引
index = 1
sql_statements = []  # 用於存儲 SQL 更新語句

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

        # 找到第一個 <tbody>
        tbody = soup.find("tbody")
        if tbody:
            # 找到所有 <tr>
            all_trs = tbody.find_all("tr")
            if len(all_trs) > 1:  # 確保有至少兩個 <tr>
                second_tr = all_trs[2]  # 獲取第二個 <tr>
                # 找到該 <tr> 中的所有 <td>
                all_tds = second_tr.find_all("td")
                # 打印結果
                print(f"Index: {index}")
                for td in all_tds:
                    # 處理文字，移除超連結
                    for a in td.find_all("a"):
                        a.decompose()  # 移除超連結標籤
                    # 提取文字並處理單引號
                    body = td.get_text(separator="\n", strip=True).replace("'", "''")
                    print(body)
                    sql_statement = f"UPDATE HCJFDG.Poem SET content = '{body}' WHERE id = {index};"
                    sql_statements.append(sql_statement)
                print("-" * 50)  # 分隔線
            else:
                print(f"URL: {url} - 沒有足夠的 <tr> 元素。")
        else:
            print(f"URL: {url} - 未找到 <tbody> 標籤。")
    else:
        print(f"請求失敗，狀態碼：{response.status_code}")

    index += 1  # 增加索引

# 將 SQL 語句保存到文件
with open("content_update_poem.sql", "w", encoding="utf-8") as file:
    file.write("\n".join(sql_statements))

print("資料已保存至 update_poem.sql")
