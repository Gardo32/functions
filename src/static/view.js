document.addEventListener('DOMContentLoaded', function() {
    setInterval(refreshTable, 10000);  

    function refreshTable() {
        fetchResults();  
    }

    function fetchResults() {
        fetch('/api/get_results')  
            .then(response => response.json())
            .then(data => updateTable(data))
            .catch(error => console.error('Error fetching results:', error));
    }

    function updateTable(data) {
        const tableBody = document.querySelector('#votes-table tbody');
        tableBody.innerHTML = '';  
        
        data.forEach(vote => {
            const row = document.createElement('tr');
            row.innerHTML = `<td>${vote.user_id}</td><td>${vote.choice}</td>`;
            tableBody.appendChild(row);
        });
    }
});
