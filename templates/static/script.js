document.addEventListener("DOMContentLoaded", () => {
    let allPlayers = [];
    const playersContainer = document.getElementById("players");
    const detailsContainer = document.getElementById("details");
    const leaderboardList = document.getElementById("leaderboard-list");

    const searchInput = document.getElementById("search");
    const teamFilter = document.getElementById("teamFilter");
    const countryFilter = document.getElementById("countryFilter");
    const sortFilter = document.getElementById("sortFilter");

    async function loadPlayers() {
        try {
            const res = await fetch("/players");
            if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
            allPlayers = await res.json();
            
            populateFilters();
            filterAndSortPlayers();
            updateLeaderboard();
        } catch (error) {
            console.error("Failed to load players:", error);
            playersContainer.innerHTML = "<p>Error loading players. Please try again later.</p>";
        }
    }

    function populateFilters() {
        const teams = [...new Set(allPlayers.map(p => p.team))].sort();
        const countries = [...new Set(allPlayers.map(p => p.nationality))].sort();

        teamFilter.innerHTML = '<option value="">All Teams</option>';
        countryFilter.innerHTML = '<option value="">All Countries</option>';

        teams.forEach(team => {
            if(team) teamFilter.innerHTML += `<option value="${team}">${team}</option>`;
        });
        countries.forEach(country => {
            if(country) countryFilter.innerHTML += `<option value="${country}">${country}</option>`;
        });
    }

    function displayPlayers(players) {
        playersContainer.innerHTML = "";
        if (players.length === 0) {
            playersContainer.innerHTML = "<p>No players match the current filters.</p>";
            return;
        }
        players.forEach(p => {
            const card = document.createElement("div");
            card.className = "player-card";
            card.id = `player-card-${p.id}`;
            card.innerHTML = `
                <div class="player-name">${p.name}</div>
                <div class="player-team">${p.team || 'Unsold'}</div>
            `;
            card.onclick = () => showDetails(p);
            playersContainer.appendChild(card);
        });
    }

    function showDetails(player) {
        // Highlight selected player
        document.querySelectorAll('.player-card').forEach(card => card.classList.remove('selected'));
        document.getElementById(`player-card-${player.id}`).classList.add('selected');

        // For now, using a placeholder for images.
        // You can replace this with actual image paths if you have them.
        const imageUrl = `https://via.placeholder.com/120/ff9800/121212?text=${player.name.charAt(0)}`;

        detailsContainer.innerHTML = `
            <div class="player-details-content">
                <img src="${imageUrl}" alt="${player.name}" class="player-image">
                <h2>${player.name}</h2>
                <p><b>Team:</b> ${player.team || 'N/A'}</p>
                <p><b>Country:</b> ${player.nationality}</p>
                <p><b>Status:</b> ${player.capped_status}</p>
                <p><b>Base Price:</b> ₹${player.base_price}</p>
                <p><b>Winning Bid:</b> ₹${player.winning_bid || 0}</p>
                <div class="bid-box">
                    <input type="number" id="bidAmount" placeholder="Enter bid amount">
                    <button onclick="placeBid(${player.id})">Place Bid</button>
                </div>
            </div>
        `;
    }

    function updateLeaderboard() {
        const sortedByBid = [...allPlayers]
            .filter(p => p.winning_bid > 0)
            .sort((a, b) => b.winning_bid - a.winning_bid)
            .slice(0, 5);

        leaderboardList.innerHTML = "";
        if (sortedByBid.length === 0) {
            leaderboardList.innerHTML = "<div class='leaderboard-placeholder'>No bids placed yet.</div>";
            return;
        }
        sortedByBid.forEach(p => {
            const li = document.createElement("li");
            li.innerHTML = `
                <span class="leader-name">${p.name}</span>
                <span class="leader-bid">₹${p.winning_bid}</span>
            `;
            leaderboardList.appendChild(li);
        });
    }
    
    window.placeBid = async function(playerId) {
        const amountInput = document.getElementById("bidAmount");
        if (!amountInput.value) {
            alert("Please enter a bid amount.");
            return;
        }

        try {
            const res = await fetch("/bid", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ player_id: playerId, amount: amountInput.value })
            });

            const result = await res.json();

            if (res.ok) {
                alert("Bid placed successfully!");
                loadPlayers(); // Reload all data to reflect changes
            } else {
                alert(`Error: ${result.error}`);
            }
        } catch (error) {
            console.error("Bid failed:", error);
            alert("An error occurred while placing the bid.");
        }
    }

    function filterAndSortPlayers() {
        const search = searchInput.value.toLowerCase();
        const team = teamFilter.value;
        const country = countryFilter.value;
        const sort = sortFilter.value;

        let filtered = allPlayers.filter(p =>
            p.name.toLowerCase().includes(search) &&
            (team === "" || p.team === team) &&
            (country === "" || p.nationality === country)
        );

        switch (sort) {
            case 'highest-bid':
                filtered.sort((a, b) => (b.winning_bid || 0) - (a.winning_bid || 0));
                break;
            case 'lowest-bid':
                filtered.sort((a, b) => (a.winning_bid || 0) - (b.winning_bid || 0));
                break;
            case 'alphabetical':
                filtered.sort((a, b) => a.name.localeCompare(b.name));
                break;
        }

        displayPlayers(filtered);
    }

    [searchInput, teamFilter, countryFilter, sortFilter].forEach(el => {
        el.addEventListener("input", filterAndSortPlayers);
        el.addEventListener("change", filterAndSortPlayers);
    });

    loadPlayers();
});