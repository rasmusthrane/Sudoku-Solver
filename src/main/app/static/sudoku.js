function updateCell(cellId, value) {
    // Send updated cell value to backend
    fetch('/update_cell', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({cell: cellId, value: value})
    });
}

function getGameState() {
      fetch('/get_game_state', {
        method: 'GET'
      })
      .then(response => response.json())
      .then(data => {
        const gameState = data.game_state;
        const violatingCells = data.violating_cells;
        document.getElementById('game_state').innerText = JSON.stringify(gameState);

        // Reset digit color for all cells
        document.querySelectorAll('td').forEach(td => {
          td.style.color = ''
        })

        // Highlight the violating cells (if any)
        violatingCells.forEach(cellId => {
          const cell = document.getElementById(cellId)
          if (cell) {
            cell.style.color = 'lightcoral'
          }
          
        });
      })
    }