# マイルストーンツール フロントエンド引き継ぎドキュメント

## プロジェクト概要

打刻・タスク管理・NN予測を統合したElectronデスクトップアプリ。UIはブラウザ非依存の独自UI（VS Codeモデル）。

## 技術スタック

- Electron + TypeScript + Vite
- CSSはグローバル変数によるテーマ管理
- バックエンド: Python + FastAPI（別プロセス）

## ファイル構成

```
src/front/
├── index.html          # 骨格のみ（app-container + script読み込み）
├── main.ts             # エントリポイント（全コンポーネントのimport・インスタンス化・render）
├── global.css          # グローバルレイアウト（grid定義・CSS変数・テーマ）
├── components/
│   ├── components.ts   # 共通コンポーネント（Header, Sidebar, GraphArea, Footer, MainArea）
│   ├── menu.ts         # MenuBarクラス（メニューバー項目管理）
│   └── timer.ts        # Timer機能コンポーネント（タイマー表示・start/stopボタン・API連携）
```

## アーキテクチャ

### 描画方式

- index.htmlは`<div class="app-container">`のみ保持
- 全UI要素はTypeScriptでDOM生成→app-containerにappend
- 各コンポーネントは`constructor()`でDOM要素生成、`render()`でappend実行
- 機能別コンポーネント（timer等）はMainAreaを経由してメインエリアに描画

### レイアウト

- 外枠: CSS Grid（3列×3行）
- 内部: Flexbox
- grid-template-columns: 85fr 732fr 283fr（sidebar / main / graph）
- grid-template-rows: 25fr 668fr 94fr（header / content / footer）

### テーマ管理

- CSS変数（:root）でダーク/ライト定義
- 現在ダークテーマのみ実装済み
- ライトテーマは@media (prefers-color-scheme: light)で定義開始済み

## CSS変数一覧

```css
--main-color: #3C3C3C      /* ヘッダー・サイドバー背景 */
--text-color: #ccc          /* 通常テキスト */
--bg-color: #1E1E1E         /* 全体背景 */
--main_area-bg: #1E1E1E     /* メインエリア背景 */
--border-color: #555        /* エリア間ボーダー */
--log-color: green           /* 通常ログ */
--log-error: rgb(173,9,9)    /* エラーログ */
--stat-base: rgb(17,112,175) /* 統計元データ */
--stat-avg: rgb(226,226,35)  /* 統計平均値 */
--stat-total: white          /* 統計合計値 */
```

## コンポーネント仕様

### Header（components.ts）

- 責務: メニューバー（左）と機能名（中央）を表示
- 子要素: `<ul class="menu">`（メニューバー）、`<div class="function-name">`（機能名）
- 機能名は各機能コンポーネントから動的に変更する想定（未実装）
- gridの1行目全幅を占有、高さ固定（25fr）

### Sidebar（components.ts）

- 責務: 機能切り替えボタンを縦並びで表示
- 現在はテキストのみ（アイコン未実装）
- 幅固定（85fr）、閉じるボタンなし
- 機能追加ごとにアイコンを追加する想定

### MainArea（components.ts）

- 責務: 機能別コンポーネントの受け皿
- constructor(functions: HTMLElement, actions: HTMLButtonElement)で子要素を受け取り
- `.main-area`にappend
- サイドバーの切り替えイベントで内部をremove→別コンポーネントをappendする想定

### GraphArea（components.ts）

- 責務: グラフ表示（NN実装後に有効化）
- 現在は仮テキスト表示のみ
- xボタンで閉じる機能（未実装）
- マウス操作による幅調整（未実装）

### Footer（components.ts）

- 責務: ログ出力（1行ずつ表示）
- 通常ログ: 緑、エラーログ: 赤
- xボタンで閉じる機能（未実装）
- マウス操作による高さ調整（未実装）

### MenuBar（menu.ts）

- 責務: メニュー項目の管理・ドロップダウン生成
- addItems(label, action)でメソッドチェーンにより項目追加
- build()でDOM要素を返却
- 各メニュー項目は独立したオブジェクトとして追加・入れ替え可能な構造
- 予定メニュー: File（ファイル選択）、View（テーマ切替・コンポーネント再表示）

### Timer（timer.ts）

- 責務: タイマー表示・start/stopボタン・API連携
- 子要素: `<div class="timer">`（カウント表示）、`<button id="start">`、`<button id="end">`
- バリデーション: isTrackingフラグで2重押し防止
- API: GET /timer/start（ポート8082）、POST /timer/stop（ポート8082）
- startボタン押下でsetIntervalによるカウントアップ開始
- start/stop押下後にボタンテキストを日付に変更

## main.ts コンポーネント初期化順序

```
1. Header('機能名')       → render()
2. Sidebar('機能名')      → render()
3. GraphArea('グラフ表示エリア') → render()
4. Footer('フッター')     → render()
5. Timer()               → MainArea(timer.timer, timer.start_timer) → mainArea.render()
6. timer.render()        （イベントリスナー登録・追加要素append）
```

重要: render()の呼び出し順序がgridの配置に影響する。Header→Sidebar→GraphArea→Footer→MainAreaの順でappendすることでgrid定義通りに配置される。

## バックエンドAPI（FastAPI）

### Timer

| エンドポイント | メソッド | 引数 | 呼び出し先 |
|---|---|---|---|
| /timer/start | GET | なし | timer.start_checker() |
| /timer/stop | POST | なし | timer.end_checker() |

### Goals

| エンドポイント | メソッド | 引数 | 呼び出し先 |
|---|---|---|---|
| /goals/save | POST | goal: list[str]（Form）, month | Goals(goal).save() |
| /goals/update | POST | key, status, limit, month | Goals(key,status,limit).update() |
| /goals/data | GET | month | Goals().leard_to_jsonl() |

### Swagger自動生成クライアント

- backend_api.ts: swagger-typescript-apiで生成済み
- 型安全なAPI呼び出しが可能（現在未使用・手動fetch方式）
- 導入する場合はtimer.ts等のfetch呼び出しを置き換え

## 未実装機能一覧

### フロント（優先度順）

1. メニューバー機能実装（File/View各項目のドロップダウン・アクション定義）
2. テーマカラー切り替え機能（CSS変数のクラス切り替えによる一括変更）
3. goals用コンポーネント（タスク一覧表示・選択・status/limit変更・登録フォーム）
4. goals用CSS
5. サイドバー機能切り替え（MainArea内のremove→append）
6. xボタンによるコンポーネントクローズ/再表示
7. マウス操作によるコンポーネント幅/高さ調整（mousedown/mousemove/mouseup）
8. CSV表示エリア（timer画面内・当日分表示）
9. 統計データ表示エリア（timer: 日ごと合計・平均、goals: 目標数・達成率）
10. timer画面のレイアウト調整（仕様書準拠の3分割配置）

### バックエンド

1. logs.py（メソッド名/エラー発生時間/メッセージをlogs.txtに保存）
2. CSV読み込み・JSON返却エンドポイント
3. 統計集計ロジック
4. NN機能（完成時期予測・コーディング補助）

## 設計方針

- ロジックは全てバックエンドで処理・フロントは表示に専念
- バリデーションはフロント（TS）とバックエンド（Python）の2重チェック
- 引数は最小限に抑え不正値リスクを低減
- エラーはstrで返却→logs.txtに格納（logs.py未実装）
- 機能ごとにモジュール化→main.tsで統合
- HTMLは骨格のみ・UI要素はTS側で動的生成

## 既知の問題

| 対象 | 内容 |
|---|---|
| timer.ts | stopボタン押下後もsetIntervalが停止しない（clearInterval未実装） |
| timer.ts | 画面切り替え後にカウントがリセットされない |
| menu.ts | addItemsのaction引数にmenu.buildを渡しており不正（仮実装） |
| components.ts | MainAreaのclassListに`.main-area`（ドット付き）が指定されている |
| global.css | ライトテーマの変数が3つのみ（全変数のライト版が未定義） |

## 本番画面レイアウト要件

### 全体要件
- ダーク/ライトテーマのユーザー切り替え
- ヘッダーを除く各コンポーネントをxボタンで閉じ可能
- ヘッダーを除く各コンポーネント幅をマウス操作で調整可能

### ヘッダー
- メニューバー（File/View）+ 機能名中央表示
- 幅調整不可・VS Codeメニューバー同等の表示幅

### サイドバー
- 幅固定・閉じるボタンなし
- 機能追加ごとにアイコン追加

### フッター・統計表示エリア・グラフ表示エリア
- マウスによる幅調整可能
- xボタンで閉じ可能

### timer画面メインエリア構成
- 開始時間表示
- タイマー表示（カウントアップ）+ 開始ボタン
- CSV出力エリア（当日分）
- 統計データ（NN実装後に有効化）

### goals画面メインエリア構成
- 目標表示エリア（進行中タスク全表示）
- 目標記入エリア（第一〜第四目標入力 + ステータス設定）
- 開始ボタン（登録）・更新ボタン（ステータス更新）
- 統計データ（達成率・NN実装後に有効化）
