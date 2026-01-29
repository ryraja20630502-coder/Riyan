// CONFIGURATION
const API_KEY = "AIzaSyBBUCOlrTy4WkM_xKgLgHYAY4vD5qSEBvk";
const btn = document.getElementById('ai-btn');
const status = document.querySelector('.status-text');
const output = document.getElementById('chat-output');
const visualizer = document.getElementById('visualizer');

// VOICE RECOGNITION SETUP
const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
const recognition = new SpeechRecognition();

btn.addEventListener('click', () => {
    recognition.start();
    status.textContent = "Listening...";
    visualizer.style.display = "flex";
});

recognition.onresult = async (event) => {
    const text = event.results[0][0].transcript;
    output.textContent = "You: " + text;
    
    // FETCH AI RESPONSE
    status.textContent = "Thinking...";
    const response = await askGemini(text);
    
    // SPEAK RESPONSE
    speak(response);
    output.textContent = response;
    status.textContent = "System Active";
    visualizer.style.display = "none";
};

async function askGemini(prompt) {
    try {
        const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=${API_KEY}`;
        const res = await fetch(url, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ contents: [{ parts: [{ text: prompt }] }] })
        });
        const data = await res.json();
        return data.candidates[0].content.parts[0].text;
    } catch (e) {
        return "I can't think right now. Is the API key correct?";
    }
}

function speak(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    window.speechSynthesis.speak(utterance);
}