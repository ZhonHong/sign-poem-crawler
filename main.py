import requests
from bs4 import BeautifulSoup

# 設置 Headers 模擬瀏覽器
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# 初始化索引
index = 1
sql_statements = []  # 用於存儲 SQL 更新語句

# 遍歷 1 到 100 的 URL
for i in range(1, 101):
    url = f"https://fate.superd.org/{i}/"
    
    # 發送請求
    response = requests.get(url, headers=headers)

    # 檢查請求是否成功
    if response.status_code == 200:
        # 解析 HTML
        soup = BeautifulSoup(response.content, "html.parser")

        # 找到第一個 <tbody>
        tbody = soup.find("tbody")
        if tbody:
            # 移除第一個 <tr>
            first_tr = tbody.find("tr")
            if first_tr:
                first_tr.decompose()
            
            # 移除包含關鍵字的 <tr>
            for tr in tbody.find_all("tr"):
                # 檢查所有 <td> 是否包含關鍵字
                if any(keyword in td.get_text() for td in tr.find_all("td") for keyword in ["相關連結", "聖", "附"]):
                    tr.decompose()
            
            # 移除所有 <span class="MsoHyperlink"> 元素
            for span in tbody.find_all("span", class_="MsoHyperlink"):
                span.decompose()

            # 提取 <tbody> 的 HTML 格式內容
            tbody_content = str(tbody).replace("'", "''")  # 處理 SQL 單引號
            print(f"Index: {index}")
            print(tbody_content)
            print("-" * 50)
            
            # 生成 SQL 更新語句
            sql_statement = f"UPDATE HCJFDG.Poem SET inner_content = '{tbody_content}' WHERE id = {index};"
            sql_statements.append(sql_statement)
        else:
            print(f"URL: {url} - 未找到 <tbody> 標籤。")
    else:
        print(f"請求失敗，狀態碼：{response.status_code}")
    index += 1  # 增加索引

# 將 SQL 語句保存到文件
with open("main_html.sql", "w", encoding="utf-8") as file:
    file.write("\n".join(sql_statements))

print("資料已保存至 main_html.sql")
