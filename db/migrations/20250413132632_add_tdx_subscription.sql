-- migrate:up
CREATE TABLE tdx_subscriptions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    city VARCHAR(50) NOT NULL,
    route_id VARCHAR(50) NOT NULL,
    direction INTEGER CHECK (direction IN (0, 1)) NOT NULL, -- 0: 去程, 1: 返程
    target_stop_uid VARCHAR(50) NOT NULL,
    notify_before_minutes INTEGER NOT NULL,
    email VARCHAR(100),
    is_active BOOLEAN DEFAULT TRUE,
    schedule_name VARCHAR(255), -- 可追蹤 Celery Beat 任務
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- migrate:down
DROP TABLE IF EXISTS tdx_subscriptions;

