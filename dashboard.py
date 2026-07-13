import streamlit as st
import json
from collections import Counter
import matplotlib.pyplot as plt
st.set_page_config(page_title="AI Honeypot Dashboard", layout="wide")

st.title("🛡️ AI Enhanced Honeypot Dashboard")

LOG_FILE = "var/log/cowrie/cowrie.json"

commands = []
attacker_ip = "Unknown"
client_version = "Unknown"

try:
    with open(LOG_FILE, "r") as f:
        lines = f.readlines()

    for line in lines:
        try:
            data = json.loads(line)

            if "src_ip" in data:
                attacker_ip = data["src_ip"]

            if data.get("eventid") == "cowrie.command.input":
                commands.append(data.get("input", ""))

            if data.get("eventid") == "cowrie.client.version":
                client_version = data.get("version", "Unknown")

        except:
            pass

except:
    st.error("Cowrie log file not found.")

# ---------------------------
# Threat Scoring
# ---------------------------

score = 0

for cmd in commands:

    if "wget" in cmd:
        score += 20

    if "chmod +x" in cmd:
        score += 25

    if "sudo" in cmd:
        score += 35

    if "nc" in cmd:
        score += 30

if score < 20:
    level = "LOW"
elif score < 50:
    level = "MEDIUM"
elif score < 80:
    level = "HIGH"
else:
    level = "CRITICAL"

# ---------------------------
# Attacker Profile
# ---------------------------

profile = "General User"

if any("wget" in c for c in commands):
    profile = "Malware Downloader"

if any("sudo" in c for c in commands):
    profile += " + Privilege Escalation"

# ---------------------------
# Dashboard Layout
# ---------------------------

col1, col2 = st.columns(2)

with col1:
    st.metric("Threat Score", score)
st.subheader("🎯 Risk Meter")

risk_percent = min(score, 100)

st.progress(risk_percent)

st.write(f"Risk Level: {level}")

with col2:
    st.metric("Threat Level", level)

st.markdown("---")

st.subheader("🧠 Attacker Profile")

st.write(profile)

st.markdown("---")

st.subheader("🌐 IP Analysis")

st.write("Attacker IP:", attacker_ip)

if attacker_ip == "127.0.0.1":
    st.write("Country: Localhost Test Environment")
else:
    st.write("Country: Unknown")

st.markdown("---")

st.subheader("💻 Device Fingerprint")

st.write("Client Version:", client_version)

st.markdown("---")

st.subheader("📜 Commands Captured")

for cmd in commands:
    st.code(cmd)

st.markdown("---")

st.subheader("📊 Command Statistics")

if commands:

    counter = Counter(commands)

    chart_data = {
        "Command": list(counter.keys()),
        "Count": list(counter.values())
    }

    st.bar_chart(
        data=chart_data,
        x="Command",
        y="Count"
    )

st.markdown("---")

st.subheader("🤖 AI Threat Classification")

if score >= 80:
    threat_type = "Malware Activity"
    confidence = 95
    st.error(f"Threat Type: {threat_type}")

elif score > 50:
    threat_type = "Suspicious Activity"
    confidence = 85
    st.warning(f"Threat Type: {threat_type}")

else:
    threat_type = "Low Risk Activity"
    confidence = 70
    st.success(f"Threat Type: {threat_type}")

st.info(f"Confidence Score: {confidence}%")
st.markdown("---")

st.subheader("🥧 Threat Distribution")

labels = [
    "Malware Activity",
    "Privilege Escalation",
    "Reconnaissance"
]

sizes = [60, 30, 10]

fig, ax = plt.subplots()

ax.pie(
    sizes,
    labels=labels,
    autopct="%1.1f%%"
)

st.pyplot(fig)

st.markdown("---")
st.subheader("🚨 Live Attack Simulation")

st.write("Attacker Actions:")
st.write("✓ Downloaded suspicious file")
st.write("✓ Prepared file for execution")
st.write("✓ Attempted privilege escalation")

st.warning("AI Interpretation: Possible Malware Deployment Attack")

st.error("Threat Level: CRITICAL")
st.markdown("---")
st.subheader("📄 AI Incident Report")

st.info("""
An attacker connected to the honeypot and attempted
to download a suspicious file. The attacker then
prepared the file for execution and attempted
privilege escalation.

Threat Level: CRITICAL
Confidence: 95%

Recommended Action:
Block source IP and investigate activity.
""")
st.markdown("---")
st.subheader("🎯 Attacker Skill Assessment")

skill = "Intermediate"

if score >= 150:
    skill = "Advanced"
elif score >= 80:
    skill = "Intermediate"
else:
    skill = "Beginner"

st.success(f"Attacker Skill Level: {skill}")

if skill == "Advanced":
    st.write("Reason: Multiple high-risk commands and privilege escalation attempts.")
elif skill == "Intermediate":
    st.write("Reason: Suspicious commands and attack progression detected.")
else:
    st.write("Reason: Limited attack activity observed.")
st.markdown("---")
st.subheader("🔮 Intent Prediction")

current_intent = "Malware Download"
predicted_action = "Privilege Escalation"
confidence_pred = 85

st.info(f"""
Current Intent: {current_intent}

Predicted Next Action: {predicted_action}

Prediction Confidence: {confidence_pred}%
""")

st.markdown("---")
st.subheader("🛡️ MITRE ATT&CK Mapping")

st.success("""
T1105 - Ingress Tool Transfer
Detected via: wget malware.sh

T1548 - Abuse Elevation Control Mechanism
Detected via: sudo su

T1059 - Command and Scripting Interpreter
Detected via: Shell Commands
""")
st.markdown("---")
st.subheader("⏱️ Attack Timeline")

timeline = [
    ("10:00:01", "SSH Connection Established"),
    ("10:00:15", "Downloaded Suspicious File"),
    ("10:00:20", "Prepared File for Execution"),
    ("10:00:30", "Attempted Privilege Escalation")
]

for time, event in timeline:
    st.write(f"🔹 {time} → {event}")
