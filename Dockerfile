FROM ghcr.io/microaijp/microaifasterwhisper_base:latest AS base

# コンテナ上のベースディレクトリ
WORKDIR /app

# ライブラリインストール
COPY requirements.txt .
RUN pip3 install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./app/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8101"]