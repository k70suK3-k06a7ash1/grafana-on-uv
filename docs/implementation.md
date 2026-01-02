# 実装詳細

## 概要

Grafana APIをモナディックパターンで操作するPythonクライアント。

## 技術スタック

| 技術 | バージョン | 用途 |
|-----|-----------|------|
| Python | 3.13+ | ランタイム |
| uv | 0.6+ | パッケージ管理 |
| grafana-client | 5.0+ | Grafana API クライアント |
| returns | 0.26+ | モナディックパターン |
| Docker | - | Grafana コンテナ |

## ディレクトリ構造

```
grafana-on-uv/
├── main.py                 # エントリーポイント
├── pyproject.toml          # プロジェクト設定
├── docker-compose.yml      # Grafana コンテナ定義
├── Makefile                # タスクランナー
├── docs/
│   ├── architecture.md     # アーキテクチャ図
│   └── implementation.md   # 実装詳細 (本文書)
└── src/grafana_on_uv/
    ├── __init__.py         # パッケージ公開API
    ├── types.py            # 型定義
    ├── client.py           # クライアントファクトリ
    ├── operations.py       # API操作
    ├── data.py             # サンプルデータ
    ├── combinators.py      # 合成関数
    └── workflows.py        # ワークフロー
```

## レイヤーアーキテクチャ

```
┌─────────────────────────────────────────────┐
│  Presentation Layer (main.py)               │
│  - IO モナドで副作用を管理                    │
│  - エントリーポイント                         │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Application Layer                          │
│  - workflows.py: ユースケース               │
│  - combinators.py: Result 変換              │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Domain Layer                               │
│  - operations.py: API 操作 (@safe)          │
│  - data.py: ドメインデータ                   │
│  - types.py: 型エイリアス                    │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  Infrastructure Layer                       │
│  - client.py: Grafana API 接続              │
└─────────────────────────────────────────────┘
```

## モナディックパターン

### 使用するモナド

| モナド | 型 | 用途 |
|-------|-----|------|
| Result | `Result[T, E]` | 成功/失敗を表現 |
| IO | `IO[T]` | 副作用をラップ |
| IOResult | `IOResult[T, E]` | 副作用 + 成功/失敗 |

### デコレータ

```python
@safe           # 例外を Result に変換
@impure_safe    # 副作用付き関数を IOResult に変換
```

### パターンマッチング

```python
match result:
    case Success(value):
        # 成功時の処理
    case Failure(error):
        # 失敗時の処理
```

### パイプライン

```python
from returns.pipeline import flow

result = flow(
    initial_value,
    function1,
    function2,
    function3,
)
```

## 各モジュール詳細

### types.py

型エイリアスを定義。

```python
type GrafanaResult[T] = Result[T, Exception]
type GrafanaIO[T] = IOResult[T, Exception]
```

### client.py

Grafana APIクライアントのファクトリ関数。

```python
def create_client(
    url: str = "http://localhost:3000",
    username: str = "admin",
    password: str = "admin",
) -> GrafanaApi
```

### operations.py

Grafana API操作を純粋関数として定義。`@safe` デコレータで例外を `Result` に変換。

| 関数 | 戻り値 | 説明 |
|------|--------|------|
| `get_health` | `Result[dict, Exception]` | ヘルスチェック |
| `list_datasources` | `Result[list, Exception]` | データソース一覧 |
| `create_datasource` | `Result[dict, Exception]` | データソース作成 |
| `list_dashboards` | `Result[list, Exception]` | ダッシュボード一覧 |
| `create_dashboard` | `Result[dict, Exception]` | ダッシュボード作成 |

### data.py

サンプルデータの定義。

- `sample_datasource()`: TestData データソース
- `sample_dashboard()`: Random Walk パネル付きダッシュボード

### combinators.py

Result を変換する合成関数。

| 関数 | 説明 |
|------|------|
| `handle_datasource_exists` | 重複エラーを Success に変換 |
| `format_result` | Result を文字列にフォーマット |
| `log` | IO モナドでログ出力 |

### workflows.py

ビジネスワークフローを定義。

| 関数 | 説明 |
|------|------|
| `health_check_workflow` | ヘルスチェック |
| `datasource_workflow` | データソース作成 (重複ハンドリング付き) |
| `dashboard_workflow` | ダッシュボード作成 |
| `full_workflow` | 全ワークフロー実行 |

### main.py

エントリーポイント。`@impure_safe` で副作用を `IOResult` にラップ。

```python
@impure_safe
def run_workflows() -> list[tuple[str, GrafanaResult]]:
    client = create_client()
    return full_workflow(client)
```

## 実行方法

```bash
# Grafana 起動
make up

# サンプル実行
make run

# ログ確認
make logs

# 停止
make down
```

## 出力例

```
=== Grafana Client (Monadic) ===

[Health Check] Success: {'commit': '...', 'database': 'ok', 'version': '...'}
[DataSources] Success: []
[Create DataSource] Success: {'datasource': {...}, 'id': 1, 'name': 'TestData'}
[Dashboards] Success: []
[Create Dashboard] Success: {'id': 1, 'slug': 'sample-dashboard', ...}

=== Done ===
```
