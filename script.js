
// ============================================================
// MEDIASSIST AI - COMPLETE FRONTEND SCRIPT
// ============================================================

const API_BASE_URL = "http://127.0.0.1:5000";

// ============================================================
// ELEMENTS
// ============================================================

const themeBtn = document.getElementById("themeBtn");
const sendBtn = document.getElementById("sendBtn");
const input = document.querySelector(".chat-box input");
const chatArea = document.querySelector(".chat-area");
const chatHistory = document.getElementById("chatHistory");

// ============================================================
// SECTION SWITCHER
// ============================================================

function showSection(sectionId) {
    const sections = document.querySelectorAll(".content-section");

    sections.forEach(section => {
        section.style.display = "none";
    });

    const target = document.getElementById(sectionId);

    if (target) {
        target.style.display = "block";
    }

    window.scrollTo({
        top: 0,
        behavior: "smooth"
    });
}

document.querySelectorAll(".menu-item").forEach(item => {
    item.addEventListener("click", function () {
        document.querySelectorAll(".menu-item").forEach(menuItem => {
            menuItem.classList.remove("active");
        });

        this.classList.add("active");
    });
});

// ============================================================
// DARK MODE
// ============================================================

function updateThemeIcon() {
    if (!themeBtn) return;

    if (document.body.classList.contains("dark")) {
        themeBtn.innerHTML = '<i class="fa-solid fa-moon"></i>';
    } else {
        themeBtn.innerHTML = '<i class="fa-regular fa-sun"></i>';
    }
}

if (localStorage.getItem("mediassist_theme") === "dark") {
    document.body.classList.add("dark");
}

updateThemeIcon();

if (themeBtn) {
    themeBtn.addEventListener("click", () => {
        document.body.classList.toggle("dark");

        const theme = document.body.classList.contains("dark")
            ? "dark"
            : "light";

        localStorage.setItem("mediassist_theme", theme);

        updateThemeIcon();
    });
}

// ============================================================
// ESCAPE HTML
// ============================================================

function escapeHTML(text) {
    if (text === null || text === undefined) return "";

    const div = document.createElement("div");
    div.textContent = String(text);

    return div.innerHTML;
}

// ============================================================
// CHAT SCROLLING
// ============================================================

// All scrolling happens inside the chat history.
// The whole webpage and input box remain in their positions.

function scrollChatToBottom(smooth = false) {
    if (!chatHistory) return;

    const scroll = () => {
        chatHistory.scrollTo({
            top: chatHistory.scrollHeight,
            behavior: smooth ? "smooth" : "instant"
        });
    };

    requestAnimationFrame(scroll);
}

function removeWelcomeScreen() {
    if (!chatHistory) return;

    const welcome = chatHistory.querySelector(".chat-welcome");

    if (welcome) {
        welcome.remove();
    }
}

// ============================================================
// CREATE CHAT MESSAGES
// ============================================================

function createMessage(text, sender, extraClass = "") {
    if (!chatHistory) return null;

    removeWelcomeScreen();

    const message = document.createElement("div");

    message.className = `message ${sender} ${extraClass}`.trim();

    const bubble = document.createElement("div");

    bubble.className = sender === "user"
        ? "bubble userBubble"
        : "bubble botBubble";

    if (sender === "bot") {
        const avatar = document.createElement("span");
        avatar.className = "bot-avatar";
        avatar.textContent = "🤖";
        message.appendChild(avatar);
    }

    // textContent prevents user/API text from injecting HTML.
    // CSS white-space: pre-wrap preserves line breaks.
    bubble.textContent = String(text);

    message.appendChild(bubble);
    chatHistory.appendChild(message);

    scrollChatToBottom();

    return message;
}

function addUserMessage(text) {
    return createMessage(text, "user");
}

function addBotMessage(text) {
    return createMessage(text, "bot");
}

function addLoadingMessage() {
    return createMessage(
        "Thinking...",
        "bot",
        "loading-msg"
    );
}

// ============================================================
// CHAT SUGGESTION CHIPS
// ============================================================

document.querySelectorAll(".chips button").forEach(chip => {
    chip.addEventListener("click", () => {
        if (!input || sendBtn?.disabled) return;

        input.value = chip.innerText.trim();
        sendMessage();
    });
});

function setQuery(text) {
    if (!input) return;

    input.value = text;
    input.focus();
}

// ============================================================
// SEND MESSAGE
// ============================================================

async function sendMessage() {
    if (!input || !chatHistory) return;

    if (sendBtn && sendBtn.disabled) return;

    const text = input.value.trim();

    if (!text) return;

    addUserMessage(text);

    input.value = "";

    if (sendBtn) {
        sendBtn.disabled = true;
        sendBtn.style.opacity = "0.6";
    }

    input.disabled = true;

    const loadingMessage = addLoadingMessage();

    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                message: text
            })
        });

        if (!response.ok) {
            throw new Error(
                `Server returned HTTP ${response.status}`
            );
        }

        const data = await response.json();

        console.log("MediAssist API response:", data);

        let reply = "";

        if (typeof data === "string") {
            reply = data;
        } else if (data && typeof data.reply === "string") {
            reply = data.reply;
        } else if (data && typeof data.response === "string") {
            reply = data.response;
        } else if (data && typeof data.message === "string") {
            reply = data.message;
        }

        if (!reply.trim()) {
            reply = (
                "I understand. Could you please describe " +
                "your health concern in a little more detail?"
            );
        }

        if (loadingMessage) {
            loadingMessage.remove();
        }

        addBotMessage(reply);

        // Optional precautions returned by the backend.
        if (
            data &&
            typeof data === "object" &&
            Array.isArray(data.precautions) &&
            data.precautions.length > 0
        ) {
            const precautionText =
                "💡 Precautions:\n" +
                data.precautions
                    .map((item, index) => `${index + 1}. ${item}`)
                    .join("\n");

            // Avoid duplicating precautions already inside reply.
            const alreadyIncluded = data.precautions.every(
                item => reply.includes(String(item))
            );

            if (!alreadyIncluded) {
                addBotMessage(precautionText);
            }
        }

        // Optional follow-up returned by the backend.
        if (
            data &&
            typeof data === "object" &&
            data.follow_up
        ) {
            const followUp = String(data.follow_up).trim();

            if (followUp && !reply.includes(followUp)) {
                addBotMessage(`❓ Follow-up: ${followUp}`);
            }
        }

    } catch (error) {
        console.error("MediAssist API Error:", error);

        if (loadingMessage) {
            loadingMessage.remove();
        }

        addBotMessage(
            "⚠️ Unable to connect to MediAssist server. " +
            "Please ensure the backend is running on " +
            "http://127.0.0.1:5000."
        );

    } finally {
        if (sendBtn) {
            sendBtn.disabled = false;
            sendBtn.style.opacity = "1";
        }

        input.disabled = false;
        input.focus();

        scrollChatToBottom();
    }
}

// ============================================================
// SEND BUTTON AND ENTER KEY
// ============================================================

if (sendBtn) {
    sendBtn.addEventListener("click", sendMessage);
}

if (input) {
    input.addEventListener("keydown", event => {
        if (event.key === "Enter") {
            event.preventDefault();
            sendMessage();
        }
    });
}

// ============================================================
// BMI CALCULATOR
// ============================================================

const calculateBmiBtn = document.getElementById("calculateBmi");

if (calculateBmiBtn) {
    calculateBmiBtn.addEventListener("click", function () {
        const weightInput = document.getElementById("weight");
        const feetInput = document.getElementById("heightFeet");
        const inchesInput = document.getElementById("heightInches");
        const result = document.getElementById("bmiResult");

        if (!weightInput || !feetInput || !inchesInput || !result) {
            return;
        }

        const weight = parseFloat(weightInput.value);
        const feet = parseFloat(feetInput.value);
        const inches = parseFloat(inchesInput.value) || 0;

        if (
            isNaN(weight) ||
            isNaN(feet) ||
            weight <= 0 ||
            feet <= 0 ||
            inches < 0 ||
            inches > 11
        ) {
            result.textContent =
                "⚠️ Please enter valid weight and height.";
            return;
        }

        const totalInches = (feet * 12) + inches;
        const heightMeters = totalInches * 0.0254;
        const bmi = weight / (heightMeters * heightMeters);

        result.innerHTML = `
            <strong>Your BMI: ${bmi.toFixed(1)}</strong>
            <br>
            <small>
                BMI is a screening measure, not a diagnosis.
                For people under 18, BMI should be interpreted
                using age- and sex-specific growth standards
                by a qualified healthcare professional.
            </small>
        `;
    });
}

// ============================================================
// HYDRATION TRACKER
// ============================================================

let waterIntake =
    parseFloat(localStorage.getItem("waterIntake")) || 0;

const addWaterBtn = document.getElementById("addWaterBtn");
const waterCount = document.getElementById("waterCount");

const today = new Date().toDateString();
const savedWaterDate = localStorage.getItem("waterDate");

if (savedWaterDate !== today) {
    waterIntake = 0;

    localStorage.setItem("waterIntake", "0");
    localStorage.setItem("waterDate", today);
}

function updateWaterDisplay() {
    if (!waterCount) return;

    waterCount.innerText = `${waterIntake.toFixed(2)} Liters`;
}

if (addWaterBtn && waterCount) {
    updateWaterDisplay();

    addWaterBtn.addEventListener("click", function () {
        waterIntake += 0.25;

        localStorage.setItem("waterIntake", waterIntake);

        updateWaterDisplay();
    });
}

// ============================================================
// MEDICINE REMINDERS
// ============================================================

let medicineReminders = [];

try {
    medicineReminders =
        JSON.parse(localStorage.getItem("medicineReminders")) || [];

    if (!Array.isArray(medicineReminders)) {
        medicineReminders = [];
    }
} catch (error) {
    medicineReminders = [];
}

const medNameInput = document.getElementById("medName");
const medTimeInput = document.getElementById("medTime");
const medDosageInput = document.getElementById("medDosage");
const addMedBtn = document.getElementById("addMedBtn");
const remindersList = document.getElementById("remindersList");

function saveMedicineReminders() {
    localStorage.setItem(
        "medicineReminders",
        JSON.stringify(medicineReminders)
    );
}

function renderReminders() {
    if (!remindersList) return;

    remindersList.innerHTML = "";

    if (medicineReminders.length === 0) {
        remindersList.innerHTML = `
            <p style="opacity:0.7;font-style:italic;">
                No medicine reminders set yet.
            </p>
        `;
        return;
    }

    medicineReminders.forEach((med, index) => {
        const item = document.createElement("div");

        item.className = "medicine-reminder-item";

        item.style.cssText = `
            display:flex;
            justify-content:space-between;
            align-items:center;
            gap:12px;
            background:rgba(0,0,0,0.04);
            border:1px solid #e2e8f0;
            padding:12px 16px;
            border-radius:8px;
            margin-bottom:8px;
            ${med.taken ? "opacity:0.55;" : ""}
        `;

        item.innerHTML = `
            <div>
                <strong>💊 ${escapeHTML(med.name)}</strong>
                <span style="
                    background:#0284c7;
                    color:white;
                    padding:2px 8px;
                    border-radius:12px;
                    font-size:0.8rem;
                ">
                    ⏰ ${escapeHTML(med.time)}
                </span>

                <div style="
                    font-size:0.85rem;
                    color:#64748b;
                    margin-top:4px;
                ">
                    📝 ${escapeHTML(med.dosage || "No instructions")}
                </div>
            </div>

            <div style="display:flex;gap:8px;">
                <button
                    class="toggle-med-btn"
                    type="button"
                    style="
                        background:#10b981;
                        color:white;
                        border:none;
                        padding:6px 12px;
                        border-radius:5px;
                        cursor:pointer;
                    "
                >
                    ${med.taken ? "Undo" : "Mark Taken"}
                </button>

                <button
                    class="delete-med-btn"
                    type="button"
                    style="
                        background:#ef4444;
                        color:white;
                        border:none;
                        padding:6px 12px;
                        border-radius:5px;
                        cursor:pointer;
                    "
                >
                    Delete
                </button>
            </div>
        `;

        item.querySelector(".toggle-med-btn").addEventListener(
            "click",
            () => window.toggleMedicineTaken(index)
        );

        item.querySelector(".delete-med-btn").addEventListener(
            "click",
            () => window.deleteMedicine(index)
        );

        remindersList.appendChild(item);
    });
}

if (addMedBtn) {
    addMedBtn.addEventListener("click", () => {
        if (!medNameInput || !medTimeInput) return;

        const name = medNameInput.value.trim();
        const time = medTimeInput.value;

        const dosage = medDosageInput
            ? medDosageInput.value.trim()
            : "";

        if (!name || !time) {
            alert("Please enter both Medicine Name and Time!");
            return;
        }

        medicineReminders.push({
            name,
            time,
            dosage,
            taken: false,
            lastNotifiedDate: null
        });

        saveMedicineReminders();
        renderReminders();

        medNameInput.value = "";
        medTimeInput.value = "";

        if (medDosageInput) {
            medDosageInput.value = "";
        }
    });
}

window.toggleMedicineTaken = function (index) {
    if (!medicineReminders[index]) return;

    medicineReminders[index].taken =
        !medicineReminders[index].taken;

    saveMedicineReminders();
    renderReminders();
};

window.deleteMedicine = function (index) {
    if (!medicineReminders[index]) return;

    medicineReminders.splice(index, 1);

    saveMedicineReminders();
    renderReminders();
};

function checkMedicineTime() {
    const now = new Date();

    const hours = String(now.getHours()).padStart(2, "0");
    const minutes = String(now.getMinutes()).padStart(2, "0");

    const currentTime = `${hours}:${minutes}`;
    const todayStr = now.toDateString();

    medicineReminders.forEach(med => {
        if (
            med.time === currentTime &&
            !med.taken &&
            med.lastNotifiedDate !== todayStr
        ) {
            med.lastNotifiedDate = todayStr;

            saveMedicineReminders();

            try {
                const AudioContextClass =
                    window.AudioContext ||
                    window.webkitAudioContext;

                if (AudioContextClass) {
                    const ctx = new AudioContextClass();
                    const osc = ctx.createOscillator();

                    osc.type = "sine";
                    osc.frequency.setValueAtTime(
                        800,
                        ctx.currentTime
                    );

                    osc.connect(ctx.destination);
                    osc.start();
                    osc.stop(ctx.currentTime + 0.6);
                }
            } catch (error) {
                console.warn("Audio unavailable:", error);
            }

            alert(
                `🔔 MEDICINE REMINDER!\n\n` +
                `It is time for: ${med.name}\n` +
                `Instructions: ${med.dosage || "As prescribed"}`
            );
        }
    });
}

renderReminders();
setInterval(checkMedicineTime, 10000);

// ============================================================
// LOGIN PLACEHOLDER
// ============================================================

const login = document.querySelector(".loginBtn");

if (login) {
    login.addEventListener("click", function () {
        alert("Login feature will be available soon.");
    });
}

// ============================================================
// STARTUP
// ============================================================

window.addEventListener("load", function () {
    document.body.style.opacity = "0";

    setTimeout(function () {
        document.body.style.transition = "opacity 0.5s ease";
        document.body.style.opacity = "1";
    }, 100);
});

console.log("MediAssist AI frontend loaded successfully.");
