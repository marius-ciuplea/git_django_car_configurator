// Funcția pentru a obține token-ul CSRF din cookie-uri (necesar pentru cereri POST în Django)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Numele începe cu acea valoare?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrfToken = getCookie('csrftoken'); // Obține token-ul la încărcarea paginii

async function sendPrompt() {
    const inputElement = document.getElementById('chat-input');
    const prompt = inputElement.value.trim();
    const outputDiv = document.getElementById('chat-output');
    const statusDiv = document.getElementById('status-message');

    if (!prompt) return;

    // Afișează un mesaj de așteptare
    outputDiv.innerHTML = "Agentul procesează... Vă rugăm așteptați.";
    statusDiv.innerHTML = "";
    inputElement.value = ''; // Golește câmpul de intrare

    try {
        const response = await fetch('/api/chat/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                // Dacă nu folosești @csrf_exempt în view-ul tău, ai nevoie de acest header:
                // 'X-CSRFToken': csrfToken 
            },
            body: JSON.stringify({ prompt: prompt })
        });

        const data = await response.json();

        if (data.status === 'success') {
            // Răspuns de succes de la agent (configurare, salvare, etc.)
            outputDiv.innerHTML = `**Răspuns agent:** ${data.response}`;
        } else {
            // Eroare de logică (e.g., nu este autentificat, eroare DB)
            outputDiv.innerHTML = ""; // Șterge mesajul de așteptare
            statusDiv.innerHTML = `Eroare: ${data.message}`;
        }
    } catch (error) {
        // Eroare de rețea (server nefuncțional, etc.)
        outputDiv.innerHTML = ""; 
        statusDiv.innerHTML = `A apărut o eroare de rețea. Verificați serverul Django.`;
        console.error('Fetch error:', error);
    }
}