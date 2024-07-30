import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.getcwd(), '.env')
dotenv_local_path = os.path.join(os.getcwd(), '.env.local')


print(f"dotenv_path: {dotenv_path}")
print(f"dotenv_local_path: {dotenv_local_path}")

load_dotenv(dotenv_path=dotenv_local_path, override=True)
load_dotenv(dotenv_path=dotenv_path)

# .env ファイルの存在を確認
if os.path.exists(dotenv_local_path):
    print(f"存在確認: {dotenv_local_path} は存在します。")
else:
    print(f"存在確認: {dotenv_local_path} は存在しません。")

if os.path.exists(dotenv_path):
    print(f"存在確認: {dotenv_path} は存在します。")
else:
    print(f"存在確認: {dotenv_path} は存在しません。")
