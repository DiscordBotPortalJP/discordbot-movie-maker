# discordbot movie-maker

Discord上で動画生成を補助するためのBotです。変換処理や拡張コマンドを通じて、サーバー上での動画作成フローを簡単にすることを目的としています。

## セットアップ
1. Python 依存関係をインストール
   ```bash
   pip install -r requirements.txt
   ```
2. Bot トークンなどの環境変数を設定
3. アプリケーションを起動
   ```bash
   python main.py
   ```

## 主な構成
- `main.py`: エントリーポイント
- `cogs/`: コマンド実装
- `extensions/`: 拡張機能
- `constants/`: 定数定義
- `utils/`: 共通ユーティリティ

## 補足
実運用前に、Discord 側の権限設定と利用規約への適合を必要に応じて確認してください。
