console.log("🔥 FACEIT INSIGHT: Компактный режим! 🔥");

const processedPlayers = new Set();

// Слушаем сообщения "по рации" от background.js
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    
    // Если пришла команда о найденном матче
    if (message.type === "FACEIT_MATCH_FOUND") {
        console.log(`[CONTENT] 📢 Получена команда! ID матча: ${message.matchId}. Запрашиваю детали...`);
        
        // Теперь мы не ищем ники, а напрямую запрашиваем инфу о матче у API Faceit
        fetch(`https://api.faceit.com/match/v2/matches/${message.matchId}`)
            .then(response => response.json())
            .then(matchData => {
                // В этом JSON лежат все игроки!
                const teams = matchData.payload.teams;
                
                let allPlayers = [];
                if (teams.faction1) allPlayers.push(...teams.faction1.roster);
                if (teams.faction2) allPlayers.push(...teams.faction2.roster);
                
                console.log("👥 Игроки, найденные через API:", allPlayers);

                // Теперь для каждого найденного игрока можно запустить твой enrichPlayer
                allPlayers.forEach(player => {
                    // Находим HTML-элемент этого игрока на странице (как раньше)
                    const playerElement = findElementByNickname(player.nickname);
                    if (playerElement) {
                        enrichPlayer(playerElement, player.nickname); // Твоя старая функция
                    }
                });
            });
    }
});

// Вспомогательная функция, чтобы найти HTML-элемент по нику
function findElementByNickname(nickname) {
    const nicknameElements = document.querySelectorAll('[class*="Nickname__Name"]');
    for (let element of nicknameElements) {
        if (element.innerText.trim() === nickname) {
            return element;
        }
    }
    return null;
}

const API_URL = "http://127.0.0.1:8000/players/statistics?nickname="; 
async function enrichPlayer(element, nickname) {
    try {
        // Убедись, что этот URL правильный!
        const response = await fetch(API_URL + nickname);
        
        if (!response.ok) {
            console.error(`❌ Ошибка от сервера для ${nickname}: ${response.status}`);
            return;
        }

        const stats = await response.json();
        console.log(`✅ Получил стату для ${nickname}:`, stats);

        // --- СОЗДАЕМ ПОЛНУЮ КАРТОЧКУ ---
        const card = document.createElement("div");
        card.style.backgroundColor = "#1a1b1f";
        card.style.borderTop = "1px solid #3c3e45";
        card.style.padding = "10px";
        card.style.marginTop = "10px";
        card.style.width = "100%";
        card.style.fontFamily = "Roboto, sans-serif";
        card.style.fontSize = "13px";
        card.style.color = "#c7c8ca";
        card.style.display = "grid";
        card.style.gridTemplateColumns = "1fr 1fr";
        card.style.gap = "8px";

        card.innerHTML = `
            <div><span style="color: #8a8c90;">Avg K/D:</span><strong style="color: white; float: right;">${(stats.avg_kd || 0).toFixed(2)}</strong></div>
            <div><span style="color: #8a8c90;">Winrate (%):</span><strong style="color: ${(stats.winrate || 0) >= 50 ? '#4CAF50' : '#F44336'}; float: right;">${stats.winrate || 0}%</strong></div>
            <div><span style="color: #8a8c90;">Avg Kills:</span><strong style="color: white; float: right;">${(stats.avg_kills || 0).toFixed(1)}</strong></div>
            <div><span style="color: #8a8c90;">Avg HS (%):</span><strong style="color: white; float: right;">${stats.hs_percent || 0}%</strong></div>
            <div style="grid-column: span 2; border-top: 1px solid #3c3e45; margin-top: 5px; padding-top: 5px;"><span style="color: #8a8c90;">Avg Multikills (per game):</span></div>
            <div><span style="color: #8a8c90;">2k:</span><strong style="color: white; float: right;">${(stats.double_kills || 0).toFixed(2)}</strong></div>
            <div><span style="color: #8a8c90;">3k:</span><strong style="color: white; float: right;">${(stats.triple_kills || 0).toFixed(2)}</strong></div>
            <div><span style="color: #8a8c90;">4k:</span><strong style="color: white; float: right;">${(stats.quadro_kills || 0).toFixed(2)}</strong></div>
            <div><span style="color: #8a8c90;">5k:</span><strong style="color: white; float: right;">${(stats.penta_kills || 0).toFixed(2)}</strong></div>
        `;
        
        // --- НОВЫЙ СПОСОБ ВСТАВКИ ---
        // 1. Находим "тело" игрока - это вся строка
        const playerBody = element.closest('[class*="ListContentPlayer__Body"]');
        

        if (playerBody) {
            // 1. Создаем "обертку" для нашей карточки
            const cardWrapper = document.createElement('div');
            cardWrapper.style.width = '100%'; // На всю ширину
            cardWrapper.appendChild(card);
            
            // 2. Вставляем эту обертку ПОСЛЕ всей строки игрока
            playerBody.parentNode.insertBefore(cardWrapper, playerBody.nextSibling);

        } else {
            // Аварийный вариант
            element.parentNode.insertBefore(card, element.nextSibling);
        }

    } catch (error) {
        console.error(`💥 Ошибка сети для ${nickname}:`, error);
    }
}


// findPlayers() и setInterval() остаются без изменений
function findPlayers() {
    const nicknameElements = document.querySelectorAll('[class*="Nickname__Name"]');
    if (nicknameElements.length === 0) return;
    nicknameElements.forEach(element => {
        const nickname = element.innerText.trim();
        if (!nickname) return;
        if (!processedPlayers.has(nickname)) {
            if (['search', 'players'].includes(nickname.toLowerCase())) return;
            processedPlayers.add(nickname);
            console.log(`🎯 [СНАЙПЕР] Нашел: ${nickname}`);
            enrichPlayer(element, nickname);
        }
    });
}
setInterval(findPlayers, 1000);
