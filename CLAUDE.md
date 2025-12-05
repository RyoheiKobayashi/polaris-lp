# CLAUDE.md

このファイルは、Claude Code (claude.ai/code) がコードを扱う際のガイダンスを提供します。

## 🎯 プロジェクト概要

**Polaris ランディングページ**
- **プロジェクト種別**: 静的Webサイト（HTML/CSS）
- **目的**: Polarisアプリのマーケティング・情報提供
- **ターゲット**:
  - 自己投資したい個人（Growthモード）
  - コンテンツ販売者・講師（Supportモード）

### ページ構成
- **index.html**: メインランディングページ
  - ヒーローセクション
  - 問題提起・ソリューション
  - Growth/Supportモード紹介
  - 料金プラン（Free/Growth/Support）
  - YouTube操作ガイド
  - CTA（App Store/Google Play準備中）
- **privacy.html**: プライバシーポリシー
- **terms.html**: 利用規約
- **tokutei.html**: 特定商取引法に基づく表記

## 🏗 技術スタック

```
HTML:                  HTML5
CSS Framework:         Tailwind CSS 3.x (CDN)
ホスティング:           静的サイトホスティング（想定）
画像:                  PNG形式（growth1-3.png, support1-3.png, icon.png）
フォント:              システムフォント
アイコン:              絵文字 + SVG
```

## 📁 ファイル構成

```
08_polaris_lp/
├── index.html          # メインLP
├── privacy.html        # プライバシーポリシー
├── terms.html          # 利用規約
├── tokutei.html        # 特定商取引法
├── images/             # 画像アセット
│   ├── icon.png        # アプリアイコン（ファビコン兼用）
│   ├── growth1.png     # Polaris画面（Growthモード）
│   ├── growth2.png     # ロードマップ画面（Growthモード）
│   ├── growth3.png     # パートナー画面（Growthモード）
│   ├── support1.png    # ダッシュボード画面（Supportモード）
│   ├── support2.png    # 分析画面（Supportモード）
│   └── support3.png    # ロードマップ管理画面（Supportモード）
└── CLAUDE.md          # このファイル
```

## 🔗 外部リソース

### お問い合わせフォーム
```
URL: https://forms.gle/mCiuPh65JQmhwe5E6
配置場所:
- index.html フッター
- privacy.html（個人情報開示請求窓口、お問い合わせ窓口）
- terms.html（退会・アカウント削除のサポート窓口）
- tokutei.html（お問い合わせ窓口）
```

### YouTube操作ガイド
```
プレイリストURL: https://www.youtube.com/playlist?list=PLkM-crNhnY-cFd-BNLr_Slwu8ti16AIWu
配置場所: index.html 使い方ガイドセクション
```

### 運営会社情報
```
会社名: 株式会社レベルアップ / LEVEL UP, K.K.
メールアドレス: hello.polaris.app@gmail.com（参考情報として記載）
```

## 🎨 デザインシステム

### カラーパレット
```css
/* 背景色 */
bg-gray-900         /* メイン背景 */
bg-gray-800         /* セカンダリ背景 */

/* アクセントカラー */
bg-blue-600         /* Growthモードバッジ */
bg-purple-600       /* Supportモードバッジ */
bg-red-600          /* YouTubeボタン */

/* グラデーション */
from-blue-900 via-purple-900 to-pink-900    /* ヒーロー・CTA */
from-blue-900 to-purple-900                  /* ソリューションボックス */
from-blue-900 to-blue-800                    /* Growthプランカード */
from-purple-900 to-purple-800                /* Supportプランカード */

/* テキスト */
text-white          /* 見出し */
text-gray-200       /* サブ見出し */
text-gray-300       /* 本文 */
text-gray-400       /* 補足テキスト */
text-gray-500       /* キャプション */
text-blue-400       /* リンク */
```

### スペーシング
```css
/* パディング */
p-6 pb-0           /* カード内テキスト（画像の上） */
p-8                /* カード内コンテンツ */
py-16              /* セクション縦方向 */

/* マージン */
mb-2               /* 小見出し下 */
mb-4               /* 中見出し下 */
mb-6               /* テキストと画像の間 */
mb-8               /* セクション内要素間 */
mb-12              /* セクション見出し下 */
```

### レスポンシブ
```css
/* ブレークポイント */
md:grid-cols-3     /* デスクトップ: 3カラム */
sm:flex-row        /* タブレット: 横並び */
/* デフォルト: モバイル（縦積み） */
```

## 📝 コンテンツ管理

### 料金プラン
```
Free:     無料
Growth:   ¥500/月（おすすめ）
Support:  ¥2,980/月
```

### 機能制限
```
                Free    Growth   Support
ロードマップ    3件     30件     100件
パートナー申請  3件     30件     100件
パートナー承認  3件     30件     100件
繰り返しToDo   ×       ○        ○
```

## 🚀 デプロイ

### App Store/Google Play リンク準備
index.html 27-50行目、300-333行目にコメントアウトされたリンクテンプレートあり。
リリース時:
1. コメントアウトを解除
2. `APP_STORE_URL` と `GOOGLE_PLAY_URL` を実際のURLに置換
3. 「準備中」セクションを削除

## 💻 コミットメッセージ規約

### 作成前の確認
コミットメッセージを作成する前に必ず以下を実行：
1. コミットしていいか確認する
2. `git status` - 変更ファイルの一覧を確認
3. `git diff` - 詳細な変更内容を確認
4. 変更の影響範囲を理解する

### フォーマット
```
<type>(<scope>): <短い要約（50文字以内）>

<詳細な説明（任意）>
- 何を変更したか
- なぜ変更したか
- どのような影響があるか

<関連Issue（任意）>
```

### Type一覧
- `feat`: 新機能の追加
  - 例: `feat(lp): YouTube操作ガイドセクションを追加`
- `fix`: バグ修正
  - 例: `fix(legal): プライバシーポリシーのリンク修正`
- `refactor`: 機能に影響しないコード改善
  - 例: `refactor(ui): カードコンポーネントのスタイル統一`
- `docs`: ドキュメントのみの変更
  - 例: `docs(readme): デプロイ手順を追加`
- `style`: コードの意味に影響しない変更（空白、フォーマット等）
  - 例: `style(legal): ヘッダーのインデント修正`
- `chore`: ビルド・開発環境の変更
  - 例: `chore(assets): 画像を最適化`

### Scope一覧（主要なもの）
- `lp`: ランディングページ（index.html）関連
- `legal`: 法的ページ（privacy/terms/tokutei）関連
- `ui`: UI・デザイン関連
- `assets`: 画像・アセット関連
- `contact`: お問い合わせフォーム関連
- `content`: コンテンツ・文言関連

### 良いコミットメッセージの例
```
feat(lp): 完全なランディングページデザインとリーガルページの追加

主な変更：
- ランディングページの全面リニューアル
  - ファビコン追加（icon.png）
  - ヒーローセクション（「スマホに北極星を」）
  - 問題提起・ソリューションセクション
  - Growthモード紹介（3画面）
  - Supportモード紹介（3画面）
  - 料金プラン（Free/Growth/Support）
  - YouTube操作ガイドリンク

- リーガルページの追加
  - privacy.html: プライバシーポリシー
  - terms.html: 利用規約
  - tokutei.html: 特定商取引法に基づく表記

影響範囲：
- ランディングページが本格的なLPへ進化
- 法的要件を満たすページが揃った
```

### 悪いコミットメッセージの例
```
❌ "修正"
❌ "LP更新"
❌ "バグフィックス"
❌ "WIP"
```

### 複数の変更を含む場合
なるべく1コミット1機能にする。複数の変更がある場合は：
```
feat(ui): お問い合わせフォーム追加とレイアウト調整

変更内容:
- お問い合わせをGoogleフォームに変更・追加
  - index.html: フッターをGoogleフォームリンクに変更
  - privacy.html, terms.html, tokutei.html: メールアドレスの下にGoogleフォーム追加

- Growth/Supportモード画面のレイアウト調整
  - 説明テキストと画像の間にスペースを追加（視認性向上）

影響:
- ユーザーがフォームから気軽に問い合わせできるように改善
- 画面説明の可読性向上
```

## 🔍 メンテナンス時の注意点

### 画像更新
- images/フォルダ内の画像を差し替える際は、ファイル名を維持
- 推奨サイズ: 横幅800-1200px（レスポンシブ対応のため）
- 「※画面はイメージです」の表記を削除しない

### リンク更新
- Googleフォーム: 全4ファイル（index, privacy, terms, tokutei）を更新
- YouTube: index.htmlのみ（セクション全体の表示/非表示も検討）

### 料金プラン変更
- index.htmlの料金プランセクション（210-264行目）を更新
- 機能制限の数値も忘れずに更新

### リーガルページ更新
- 会社情報、メールアドレスの変更時は全4ファイルを確認
- 日付（施行日・改定日）の更新を忘れない
