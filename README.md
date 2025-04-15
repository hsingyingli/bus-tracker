# 公車追蹤系統 (Bus Tracker)

一個用於追蹤公共交通工具到站時間並提供通知的系統。

## 功能

- 查詢公車預計到站時間
- 訂閱公車到站通知（透過電子郵件）
- 用戶認證和授權
- 速率限制保護 API

## 技術 Stack

- **後端**: FastAPI
- **資料庫**: PostgreSQL
- **快取**: Redis
- **任務佇列**: Celery + Redis
- **容器化**: Docker, Docker Compose

## 安裝與設定

### 前置需求

- Docker 和 Docker Compose
- 設定 `.env` 檔案（參考下方示例）

### 環境變數

創建一個 `.env` 檔案並設定以下變數：

```
# 資料庫設定
DATABASE_URL=postgresql://username:password@localhost:5432/db
DATABASE_MAX_POOL=10
DATABASE_MIN_POOL=1
DATABASE_MAX_QUERIES=50000
DATABASE_MAX_INACTIVE_CONNECTION_LIFETIME=300

# postgresql docker 設定
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=db

# Redis 設定
REDIS_URL=redis://redis:6379/0

# 應用程式設定
ACCESS_TOKEN_EXPIRE_MINUTES=30
ACCESS_SECRET_KEY=sercrt_key
JWT_ALGORITHM=HS256

# TDX API 設定
TDX_CLIENT_ID=your_tdx_client_id
TDX_CLIENT_SECRET=your_tdx_client_secret

# 郵件設定
EMAIL_PASSWORD=google app password
EMAIL_ADDRESS=google email address

# Worker設定

BROKER_URL=redis://redis:6379/1
RESULT_BACKEND=redis://redis:6379/2
BEAT_URL=redis://redis:6379/3
```

## 啟動服務

```bash
docker-compose up -d
```

這將啟動以下服務：

- PostgreSQL 資料庫
- Redis 伺服器
- FastAPI 應用程式
- Celery 工作處理器
- Celery Beat 排程器

## API 使用說明

### 查詢公車預計到站時間

```
GET /api/bus/estimated_time_of_arrival/city/{city}/{route}
```

- `city`: 城市名稱
- `route`: 路線名稱

### 訂閱公車到站通知

```
POST /api/bus/estimated_time_of_arrival/city/{city}/{route}/subscribe
```

請求內容:

```json
{
  "target_stop_uid": "站牌UID",
  "email": "your.email@example.com",
  "notify_before_minutes": 5,
  "direction": 0
}
```

- `target_stop_uid`: 目標站牌的唯一識別碼
- `email`: 接收通知的電子郵件地址
- `notify_before_minutes`: 提前通知的分鐘數
- `direction`: 行駛方向（0 或 1）

## 開發

### 資料庫遷移

1. [安裝 dbmate](https://github.com/amacneil/dbmate?tab=readme-ov-file#installation)
2. 更改 Makefile 裡面的參數

3. 執行 migration up

```bash
# 執行遷移
make migrate_up
```

### 測試

```bash
# 執行測試 (待實現)
make test
```

## 架構

- `app/`: 主要應用程式程式碼

  - `api/`: API 端點
  - `dependencies/`: FastAPI 相依性注入
  - `repositories/`: 資料存取層
  - `schemas/`: Pydantic 模型
  - `services/`: 外部服務整合
  - `use_cases/`: 業務邏輯
  - `utils/`: 工具函數

- `config/`: 應用程式設定
- `db/`: 資料庫相關文件和遷移
- `infra/`: 基礎設施設定
- `worker/`: Celery 工作處理器和任務定義

# 可優化地方

- 每個 subscribe 都要查詢一次 Tdx API, 可以考慮 cache 起來同站牌的 request, 減少 Tdx API 的請求次數

- 目前 Table 都沒加 Index

