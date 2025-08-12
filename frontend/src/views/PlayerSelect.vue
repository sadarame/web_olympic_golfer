<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ゴルフ オリンピック スコア記録アプリ</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #c7e5a0 0%, #90d36a 100%);
            color: #333;
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }

        .header {
            background-color: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            padding: 0.75rem 1rem;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .card {
            background-color: rgba(255, 255, 255, 0.9);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 1.5rem;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.15);
            padding: 1.5rem;
            border: 1px solid rgba(255, 255, 255, 0.3);
            margin: 1rem;
        }

        .input-field {
            @apply w-full p-3 rounded-lg border border-gray-300 focus:outline-none focus:ring-2 focus:ring-green-500 transition-colors duration-200;
        }
        
        /* プレイヤーリストアイテムのデザイン */
        .player-list-item {
            @apply flex items-center justify-between p-3 bg-white rounded-lg shadow-sm transition-all duration-200 cursor-pointer;
            margin-bottom: 0.5rem;
            border: 2px solid transparent;
        }
        .player-list-item.selected {
            @apply bg-green-100 ring-2 ring-green-500 border-green-500;
        }

        /* カスタムボタンのデザイン */
        .btn-custom {
            @apply relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border border-neutral-200 bg-transparent px-6 font-medium text-neutral-600 transition-all duration-100 [box-shadow:3px_3px_rgb(60_80_60)] active:translate-x-[2px] active:translate-y-[2px] active:[box-shadow:0px_0px_rgb(60_80_60)];
        }

        /* 「ゲームを開始」ボタンのデザイン */
        .btn-fancy-next {
            @apply w-full relative inline-flex h-12 items-center justify-center overflow-hidden rounded-md border-2 border-green-700 bg-green-500 px-6 font-bold text-white transition-all duration-100;
            box-shadow: 3px 3px rgb(20, 100, 20);
        }
        .btn-fancy-next:active {
            transform: translate(2px, 2px);
            box-shadow: 0px 0px rgb(20, 100, 20);
        }
        .btn-fancy-next:disabled {
            @apply bg-gray-400 text-gray-700 border-gray-500 cursor-not-allowed;
            box-shadow: 3px 3px rgb(100, 100, 100);
        }
    </style>
</head>
<body>
    <!-- ヘッダー部分 -->
    <header class="header fixed top-0 left-0 right-0 z-10">
        <h1 class="text-2xl font-bold text-gray-800">
            Golf Olympic ⛳️
        </h1>
    </header>

    <!-- メインコンテンツ部分 -->
    <div class="flex-grow flex justify-center items-center p-4 pt-20">
        <div class="container mx-auto max-w-sm card">
            <h1 class="text-3xl font-bold text-center text-gray-800 mb-6">
                同伴者を追加
            </h1>

            <!-- 既存プレイヤーリストセクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">登録済プレイヤーから選択</h2>
                <div id="existing-player-list" class="space-y-2 h-48 overflow-y-scroll">
                    <!-- 既存プレイヤーリストがここに追加されます -->
                </div>
            </div>

            <!-- 新規プレイヤー追加セクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">新しい同伴者を追加</h2>
                <div class="flex space-x-2">
                    <input type="text" id="new-player-name" class="input-field" placeholder="同伴者名を入力...">
                    <button id="add-player-button" class="btn-custom w-1/3">
                        追加
                    </button>
                </div>
            </div>

            <!-- ラウンド参加メンバーリストセクション -->
            <div class="space-y-4 mb-6">
                <h2 class="text-xl font-semibold text-gray-800">ラウンドに参加する同伴者</h2>
                <div id="selected-player-list" class="space-y-2">
                    <!-- 選択されたプレイヤーリストがここに追加されます -->
                </div>
            </div>
            
            <!-- 次へボタン -->
            <div class="text-center">
                <button id="next-button" class="btn-fancy-next" disabled>
                    ゲームを開始 ➡️
                </button>
            </div>
        </div>
    </div>

    <script>
        const existingPlayerList = document.getElementById('existing-player-list');
        const selectedPlayerList = document.getElementById('selected-player-list');
        const newPlayerInput = document.getElementById('new-player-name');
        const addPlayerButton = document.getElementById('add-player-button');
        const nextButton = document.getElementById('next-button');

        // ダミーデータ（Firebaseなどのバックエンドから取得するデータを想定）
        let existingPlayers = ['ログインユーザー', 'プレイヤーA', 'プレイヤーB', 'プレイヤーC', 'プレイヤーD', 'プレイヤーE', 'プレイヤーF', 'プレイヤーG', 'プレイヤーH', 'プレイヤーI', 'プレイヤーJ'];
        let selectedPlayers = new Set();
        
        // ログインユーザーをデフォルトで選択
        selectedPlayers.add('ログインユーザー');

        // 既存プレイヤーリストをレンダリングする関数
        const renderExistingPlayers = () => {
            existingPlayerList.innerHTML = '';
            existingPlayers.forEach(name => {
                const isSelected = selectedPlayers.has(name);
                const item = document.createElement('div');
                item.className = `player-list-item ${isSelected ? 'selected' : ''}`;
                item.innerHTML = `
                    <div class="flex items-center space-x-3">
                        <input type="checkbox" ${isSelected ? 'checked' : ''} class="form-checkbox h-5 w-5 text-green-600 rounded-md" ${name === 'ログインユーザー' ? 'disabled' : ''}>
                        <span class="text-gray-800 font-medium">${name}</span>
                    </div>
                `;

                // リストアイテム全体のクリックイベント
                if (name !== 'ログインユーザー') { // ログインユーザーは選択解除できない
                    item.addEventListener('click', (e) => {
                        if (e.target.tagName !== 'INPUT') {
                            const checkbox = item.querySelector('input[type="checkbox"]');
                            checkbox.checked = !checkbox.checked;
                        }
                        
                        if (item.querySelector('input[type="checkbox"]').checked) {
                            selectedPlayers.add(name);
                        } else {
                            selectedPlayers.delete(name);
                        }
                        renderSelectedPlayers();
                    });
                }
                existingPlayerList.appendChild(item);
            });
        };

        // 選択されたプレイヤーリストをレンダリングする関数
        const renderSelectedPlayers = () => {
            selectedPlayerList.innerHTML = '';
            Array.from(selectedPlayers).forEach(name => {
                const item = document.createElement('div');
                item.className = 'player-list-item';
                item.innerHTML = `
                    <span class="text-gray-800 font-medium">${name}</span>
                    <button class="remove-player-btn text-gray-400 hover:text-red-500 transition-colors duration-200 ${name === 'ログインユーザー' ? 'hidden' : ''}">
                        ×
                    </button>
                `;

                // 削除ボタンのクリックイベント
                item.querySelector('.remove-player-btn')?.addEventListener('click', () => {
                    selectedPlayers.delete(name);
                    renderExistingPlayers(); // 既存リストの表示を更新
                    renderSelectedPlayers(); // 選択リストの表示を更新
                });
                selectedPlayerList.appendChild(item);
            });
            updateNextButtonState();
        };

        // 新しいプレイヤーを追加する関数
        const addNewPlayer = (name) => {
            if (name && !existingPlayers.includes(name)) {
                existingPlayers.push(name);
                selectedPlayers.add(name);
                renderExistingPlayers();
                renderSelectedPlayers();
                newPlayerInput.value = '';
            }
        };

        // 「ゲームを開始」ボタンの状態を更新する関数
        const updateNextButtonState = () => {
            nextButton.disabled = selectedPlayers.size < 2;
            if (nextButton.disabled) {
                nextButton.textContent = '同伴者を1人以上選択してください';
            } else {
                nextButton.textContent = `ゲームを開始 ➡️`;
            }
        };

        // 新しいプレイヤーを追加するイベントリスナー
        addPlayerButton.addEventListener('click', () => {
            addNewPlayer(newPlayerInput.value);
        });

        // 「ゲームを開始」ボタンのクリックイベント
        nextButton.addEventListener('click', () => {
            if (selectedPlayers.size >= 2) {
                alert(`ゲームを開始します！\n参加メンバー: ${Array.from(selectedPlayers).join(', ')}`);
                // TODO: 実際のアプリでは、この後スコア入力画面に遷移する処理を実装
            }
        });

        // ページ読み込み時にリストをレンダリング
        renderExistingPlayers();
        renderSelectedPlayers();
    </script>
</body>
</html>
