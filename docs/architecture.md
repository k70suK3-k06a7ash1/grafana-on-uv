# Grafana と grafana-client の関係性

## コンポーネント定義

```
G = Grafana Server (Docker Container)
C = grafana-client (Python Library)
A = REST API
```

## 関係式

```
G ⊃ A        -- Grafana は REST API を公開する
C → A        -- grafana-client は API を呼び出す
C ∘ A = G    -- クライアントは API を通じてサーバーを操作する
```

## 通信モデル

```
┌─────────────────┐         HTTP/REST         ┌─────────────────┐
│                 │  ───────────────────────▶ │                 │
│  grafana-client │        :3000              │     Grafana     │
│    (Python)     │  ◀─────────────────────── │    (Docker)     │
│                 │         JSON              │                 │
└─────────────────┘                           └─────────────────┘
       C                                             G
```

## 操作の写像

```
f: C × Request → G × Response

where:
  Request  ∈ { GET, POST, PUT, DELETE }
  Response ∈ { Dashboard, Datasource, Alert, ... }
```

## 具体例

| 操作 | クライアント (C) | API (A) | サーバー (G) |
|------|------------------|---------|--------------|
| 取得 | `grafana.search.search_dashboards()` | `GET /api/search` | Dashboard[] |
| 作成 | `grafana.dashboard.update_dashboard()` | `POST /api/dashboards/db` | Dashboard |
| 削除 | `grafana.dashboard.delete_dashboard()` | `DELETE /api/dashboards/uid/:uid` | void |

## 依存関係

```
C depends_on G  -- クライアントはサーバーが起動している必要がある
G independent   -- サーバーは単独で動作可能
```

## 冪等性

```
GET  : 冪等 (何度実行しても同じ結果)
POST : 非冪等 (実行ごとに状態が変化する可能性)
PUT  : 冪等
DELETE: 冪等
```
