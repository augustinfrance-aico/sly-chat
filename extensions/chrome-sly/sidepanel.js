// =============================================
// SLY Chrome Extension — Side Panel Chat
// Fichier JS EXTERNE (obligatoire MV3 — CSP bloque inline)
// =============================================

(function() {
  "use strict";

  // --- Config ---
  var GROQ_KEY = "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";
  var GROQ_MODEL = "llama-3.3-70b-versatile";
  var GROQ_URL = "https://api.groq.com/openai/v1/chat/completions";
  var SYSTEM_MSG = "Tu es SLY, un assistant IA du Cooper Building (50 agents specialises). Reponds en francais, concis et direct. Pas de blabla.";
  var STORAGE_KEY = "sly_chat";

  // --- State ---
  var chatHistory = [];
  var isBusy = false;

  // --- DOM refs (set after DOMContentLoaded) ---
  var chatEl, welcomeEl, typingEl, inputEl, sendBtn, clearBtn;

  // --- Time ---
  function timeStr() {
    var d = new Date();
    var h = String(d.getHours()).padStart(2, "0");
    var m = String(d.getMinutes()).padStart(2, "0");
    return h + ":" + m;
  }

  // --- Create message DOM ---
  function createBubble(text, isUser, isError) {
    var wrapper = document.createElement("div");
    wrapper.className = "msg" + (isUser ? " u" : " a") + (isError ? " err" : "");

    var bub = document.createElement("div");
    bub.className = "bub";
    bub.textContent = text;

    var ts = document.createElement("div");
    ts.className = "ts";
    ts.textContent = timeStr();

    wrapper.appendChild(bub);
    wrapper.appendChild(ts);
    return wrapper;
  }

  // --- Show message ---
  function showMessage(text, isUser, isError) {
    if (welcomeEl) welcomeEl.style.display = "none";
    chatEl.appendChild(createBubble(text, isUser, isError || false));
    setTimeout(function() { chatEl.scrollTop = chatEl.scrollHeight; }, 30);
  }

  // --- Typing indicator ---
  function showTyping(on) {
    if (!typingEl) return;
    if (on) {
      typingEl.classList.add("on");
      if (typingEl.parentNode !== chatEl) chatEl.appendChild(typingEl);
      setTimeout(function() { chatEl.scrollTop = chatEl.scrollHeight; }, 30);
    } else {
      typingEl.classList.remove("on");
    }
  }

  // --- Busy state ---
  function setBusy(b) {
    isBusy = b;
    sendBtn.disabled = b;
    showTyping(b);
  }

  // --- Groq API ---
  function callGroq(history) {
    var messages = [{ role: "system", content: SYSTEM_MSG }];
    for (var i = 0; i < history.length; i++) {
      messages.push({ role: history[i].role, content: history[i].content });
    }

    return fetch(GROQ_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + GROQ_KEY
      },
      body: JSON.stringify({
        model: GROQ_MODEL,
        messages: messages,
        temperature: 0.7,
        max_tokens: 2048
      })
    })
    .then(function(res) {
      if (!res.ok) {
        return res.text().then(function(t) {
          throw new Error("API " + res.status + ": " + t.substring(0, 200));
        });
      }
      return res.json();
    })
    .then(function(data) {
      if (data && data.choices && data.choices[0]) {
        return data.choices[0].message.content;
      }
      throw new Error("Reponse invalide");
    });
  }

  // --- Send message ---
  function handleSend() {
    var text = inputEl.value.trim();
    if (!text || isBusy) return;

    // Show user bubble
    showMessage(text, true);
    chatHistory.push({ role: "user", content: text });

    // Clear input
    inputEl.value = "";
    inputEl.style.height = "auto";

    // Busy
    setBusy(true);

    // API call
    callGroq(chatHistory)
      .then(function(reply) {
        chatHistory.push({ role: "assistant", content: reply });
        showMessage(reply, false);
        saveChat();
      })
      .catch(function(err) {
        showMessage("Erreur: " + err.message, false, true);
      })
      .then(function() {
        setBusy(false);
        inputEl.focus();
      });
  }

  // --- Clear ---
  function handleClear() {
    chatHistory = [];
    chatEl.innerHTML = "";
    if (welcomeEl) {
      welcomeEl.style.display = "";
      chatEl.appendChild(welcomeEl);
    }
    saveChat();
    inputEl.focus();
  }

  // --- Storage ---
  function saveChat() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(chatHistory.slice(-20)));
    } catch(e) {}
  }

  function loadChat() {
    try {
      var raw = localStorage.getItem(STORAGE_KEY);
      if (raw) {
        chatHistory = JSON.parse(raw);
        for (var i = 0; i < chatHistory.length; i++) {
          showMessage(chatHistory[i].content, chatHistory[i].role === "user");
        }
      }
    } catch(e) {}
  }

  // --- Auto resize textarea ---
  function autoResize() {
    inputEl.style.height = "auto";
    inputEl.style.height = Math.min(inputEl.scrollHeight, 100) + "px";
  }

  // --- Init (when DOM ready) ---
  document.addEventListener("DOMContentLoaded", function() {
    // Get DOM refs
    chatEl = document.getElementById("chat");
    welcomeEl = document.getElementById("welcomeScreen");
    typingEl = document.getElementById("typingIndicator");
    inputEl = document.getElementById("msgInput");
    sendBtn = document.getElementById("sendBtn");
    clearBtn = document.getElementById("clearBtn");

    // Bind events via addEventListener (MV3 requires this)
    sendBtn.addEventListener("click", handleSend);

    inputEl.addEventListener("keydown", function(e) {
      if (e.key === "Enter" && !e.shiftKey) {
        e.preventDefault();
        handleSend();
      }
    });

    inputEl.addEventListener("input", autoResize);

    clearBtn.addEventListener("click", handleClear);

    // Chrome extension context menu (optional)
    try {
      if (typeof chrome !== "undefined" && chrome.runtime && chrome.runtime.onMessage) {
        chrome.runtime.onMessage.addListener(function(msg) {
          if (msg && msg.type === "context-menu-selection" && msg.text) {
            inputEl.value = msg.text;
            autoResize();
            inputEl.focus();
          }
        });
      }
    } catch(e) {}

    // Load history & focus
    loadChat();
    inputEl.focus();
  });

})();
