document.getElementById('mealPlanForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = new FormData(this);

    fetch('/get_meal_plan', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        let resultDiv = document.getElementById('mealPlanResult');
        resultDiv.innerHTML = `<h2>Recommended Meal Plan:</h2>`;
        
        if (typeof data.meal_plan === 'string') {
            resultDiv.innerHTML += `<p>${data.meal_plan}</p>`;
        } else {
            resultDiv.innerHTML += `<ul>`;
            data.meal_plan.forEach(item => {
                resultDiv.innerHTML += `<li>${item['Food Item']}: ${item['Quantity (kg)']} kg (₹${item['Total Price (₹)']})</li>`;
            });
            resultDiv.innerHTML += `</ul>`;
        }
        
        if (data.commodity_prices) {
            resultDiv.innerHTML += `<h3>Commodity Prices (Real-time):</h3>`;
            resultDiv.innerHTML += `<ul>`;
            data.commodity_prices.forEach(item => {
                resultDiv.innerHTML += `<li>${item.commodity} - ₹${item.modal_price} per kg</li>`;
            });
            resultDiv.innerHTML += `</ul>`;
        }
        const budget = document.getElementById('budget').value;
        const familySize = document.getElementById('family_size').value;
    
        if (budget <= 0) {
            alert("Budget must be greater than zero.");
            event.preventDefault();
        }
        if (familySize <= 0) {
            alert("Family size must be greater than zero.");
            event.preventDefault();
        }
    });
});



