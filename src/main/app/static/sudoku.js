function handleCellKeyDown(event, row_letters, col_numbers, possible_digits) {
    const cell = event.target;
    const cellId = cell.id;

    // Block all typing/deletion on clue cells
    const navKeys = ['ArrowLeft','ArrowRight','ArrowUp','ArrowDown'];
    if (cell.classList.contains('initial-clue')) {
        if (!navKeys.includes(event.key)) {
            event.preventDefault(); // block typing or deleting
            return;
        }
        // arrows are still allowed, so do NOT return here
    }

    // Handle arrow navigation
    if (navKeys.includes(event.key)) {
        event.preventDefault(); // prevent scrolling

        let rowIndex = row_letters.indexOf(cellId[0]);
        let colIndex = col_numbers.indexOf(cellId.slice(1));

        if (event.key === 'ArrowLeft' && colIndex > 0) colIndex -= 1;
        if (event.key === 'ArrowRight' && colIndex < col_numbers.length - 1) colIndex += 1;
        if (event.key === 'ArrowUp' && rowIndex > 0) rowIndex -= 1;
        if (event.key === 'ArrowDown' && rowIndex < row_letters.length - 1) rowIndex += 1;

        const nextCellId = row_letters[rowIndex] + col_numbers[colIndex];
        const nextCell = document.getElementById(nextCellId);

        if (nextCell) {
            nextCell.focus();   // ALWAYS allow focus
        }
        
        return;
    }


    // Handle deletion
    if (event.key === 'Backspace' || event.key === 'Delete') {
        cell.innerText = '';
        event.preventDefault();
        return;
    }

    // Only allow digits
    if (possible_digits.includes(event.key)) {
        cell.innerText = event.key;  // replace with single digit
        event.preventDefault();       // prevent default to stop multiple chars
        return;
    }

    // Block all other keys
    event.preventDefault();
}


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
          td.style.backgroundColor = ''
        })

        // Highlight the violating cells (if any)
        violatingCells.forEach(cellId => {
          const cell = document.getElementById(cellId)
            if (cell) {
                if (cell.classList.contains('initial-clue')) {
                cell.style.backgroundColor = 'pink'; 
                } else {
                cell.style.color = 'lightcoral';
                }
            }
          
        });
      })
    }