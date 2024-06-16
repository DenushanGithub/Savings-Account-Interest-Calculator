function calculateInterest() {
    const amount = parseFloat(amountInput.value);
    const interestRate = parseFloat(interestRateInput.value);
    const term = parseInt(termInput.value);
    const termUnit = termUnitSelect.value;

    if (isNaN(amount) || isNaN(interestRate) || isNaN(term)) {
        document.getElementById('result').innerText = 'Please enter valid numbers for all fields.';
        return;
    }

    let termInMonths;
    if (termUnit === 'months') {
        termInMonths = term;
    } else {
        termInMonths = term * 12;
    }

    const monthlyInterestRate = interestRate / 100 / 12;
    let balance = amount;
    const data = [];

    for (let i = 0; i < termInMonths; i++) {
        const interest = balance * monthlyInterestRate;
        balance += interest;
        data.push(balance);
    }

    // Render chart
    renderChart(data, termInMonths);
    
    // Display total interest earned
    const interestEarned = balance - amount;
    document.getElementById('result').innerText = `Interest earned: $${interestEarned.toFixed(2)}`;
}
