# bb - Git Branch Name and Pull Request Assistant

## 概要
`bb`は、OpenAIのAPI(`gpt-4o-mini`)を利用して、Gitのブランチ名やプルリクエストの説明を自動生成するツールです。ユーザーの入力やGitの差分情報から、適切なブランチ名やプルリクエストのタイトル、変更点のリストを生成します。

## インストール

### 事前準備
OpenAI APIキーを取得し、環境変数に設定。
```bash
$ export OPENAI_API_KEY=your-api-key
```

プロジェクトの依存関係をインストール。
```bash
$ rye sync
```

ツールとしてインストール。
```bash
$ rye install .
```

## 使い方

### コマンド
以下のコマンドを使用して、ブランチ名やプルリクエストのタイトル、説明を生成できます。

#### `pr` コマンド
Gitの差分からプルリクエストの変更点を生成します。

```bash
$ bb pr -b <branch> [-d] [-n]
-b, --branch：比較対象のブランチ（デフォルトは develop）。
-d, --description：プルリクエストの説明を生成するフラグ。
-n, --name：ブランチ名を生成するフラグ。

# プルリクエストの変更点のみを生成
$ bb pr -b main

# プルリクエストの変更点とブランチ名を生成
$ bb pr -b main -n

# プルリクエストのタイトルと変更点を生成
$ bb pr -b main -d

# プルリクエストのタイトル、変更点、ブランチ名を生成
$ bb pr -b main -dn
```

#### `bn` コマンド
ユーザーのインプットからシンプルなブランチ名を生成します。

```bash
$ bb bn <description>

$ bb bn 新しい検索UIの追加
#output feature/add-new-search-ui
```
#### `co` コマンド
Gitの差分からコミットメッセージを生成します。

```bash
$ bb co
```
