# generate-invitation-codes

🐔動機：為了讓全球試用生成試用碼，所以生成長度任意的數量的試用碼
💣地雷：一次就 gpt-4 成功，沒有地雷

這是一個 Python 套件，可以用來生成全球試用的邀請碼。您可以通過命令行界面或將其導入到其他 Python 項目中使用。

## 安裝
使用以下命令安裝：

```sh
python3 -m pip install generate-invitation-codes
```

## 命令行界面用法
在命令行中，使用以下命令生成邀請碼：

```sh
python3 -m generate_invitation_codes your_email@example.com --num 10 --length 16
```

以下是命令行參數說明：
- `your_email@example.com`：需要生成邀請碼的電子郵件地址。
- `--num`, `-n`：（可選）要生成的邀請碼數量（預設為 5）。
- `--length`, `-l`：（可選）生成的邀請碼的長度（預設為 16，必須是偶數）。

## 套件用法
在 Python 項目中，您可以將 generate-invitation-codes 套件導入並使用 `generate_invitation_codes` 函數：
```python
from generate_invitation_codes import generate_invitation_codes
codes = generate_invitation_codes('your_email@example.com', num=10, code_length=16)
```

以下是函數參數說明：
- `email`：需要生成邀請碼的電子郵件地址。
- `num`：（可選）要生成的邀請碼數量（預設為 5）。
- `code_length`：（可選）生成的邀請碼的長度（預設為 16，必須是偶數）。