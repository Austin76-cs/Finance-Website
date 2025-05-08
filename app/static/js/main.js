// Format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Update account balances
function updateBalances() {
    fetch('/api/balance')
        .then(response => response.json())
        .then(accounts => {
            let totalBalance = 0;
            const accountsList = document.getElementById('accounts-list');
            
            if (accounts.length > 0) {
                accountsList.innerHTML = '';
                accounts.forEach(account => {
                    totalBalance += account.balances.current;
                    
                    const accountElement = document.createElement('div');
                    accountElement.className = 'transaction-item';
                    accountElement.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-0">${account.name}</h6>
                                <small class="text-muted">${account.type}</small>
                            </div>
                            <div class="text-end">
                                <h6 class="mb-0">${formatCurrency(account.balances.current)}</h6>
                                <small class="text-muted">Available: ${formatCurrency(account.balances.available)}</small>
                            </div>
                        </div>
                    `;
                    accountsList.appendChild(accountElement);
                });
            }
            
            // Update total balance
            document.querySelector('.balance-positive').textContent = formatCurrency(totalBalance);
        })
        .catch(error => console.error('Error fetching balances:', error));
}

// Update transactions
function updateTransactions() {
    fetch('/api/transactions')
        .then(response => response.json())
        .then(transactions => {
            const transactionsList = document.getElementById('transactions-list');
            
            if (transactions.length > 0) {
                transactionsList.innerHTML = '';
                transactions.forEach(transaction => {
                    const transactionElement = document.createElement('div');
                    transactionElement.className = 'transaction-item';
                    transactionElement.innerHTML = `
                        <div class="d-flex justify-content-between align-items-center">
                            <div>
                                <h6 class="mb-0">${transaction.name}</h6>
                                <small class="text-muted">${transaction.date}</small>
                            </div>
                            <div class="text-end">
                                <h6 class="mb-0 ${transaction.amount < 0 ? 'balance-negative' : 'balance-positive'}">
                                    ${formatCurrency(transaction.amount)}
                                </h6>
                                <small class="text-muted">${transaction.category.join(', ')}</small>
                            </div>
                        </div>
                    `;
                    transactionsList.appendChild(transactionElement);
                });
            }
        })
        .catch(error => console.error('Error fetching transactions:', error));
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    // Check if we're on the dashboard page
    if (document.getElementById('transactions-list')) {
        updateBalances();
        updateTransactions();
        
        // Refresh data every 5 minutes
        setInterval(() => {
            updateBalances();
            updateTransactions();
        }, 300000);
    }
}); 