#!/bin/bash
set -e

echo "🚀 Starting Firebase Emulator Suite..."
echo "📍 This will run Cloud Functions locally with the same runtime as production!"

# 仮想環境が存在するかチェック
if [ ! -d "backend/functions/venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv backend/functions/venv
fi

# 仮想環境をアクティベート
echo "🔧 Activating virtual environment..."
source backend/functions/venv/bin/activate

# 依存関係をインストール
echo "📥 Installing dependencies..."
pip install -r backend/functions/requirements.txt

echo "🌐 Starting Firebase Emulator..."
echo "📚 Available endpoints will be shown in the emulator UI"
echo "🔗 Emulator UI: http://localhost:4000"
echo "📡 Functions will be available at the URLs shown in the emulator output"

# Firebase Emulatorを起動
firebase emulators:start
