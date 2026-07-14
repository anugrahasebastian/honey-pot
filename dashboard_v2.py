
import streamlit as st
import json
from collections import Counter
import matplotlib.pyplot as plt
st.set_page_config(page_title="AI Honeypot Dashboard", layout="wide")
st.markdown("""
<style>
.stApp {
    background: #050B18;
    color: white;
}

.metric-card {
    background: #081427;
    border: 1px solid #00d4ff;
    border-radius: 12px;
    padding: 20px;
    text-align: center;
    box-shadow: 0 0 15px rgba(0,212,255,0.3);
}

.card-title {
    color: #00d4ff;
    font-size: 14px;
    letter-spacing: 2px;
}

.card-value {
    color: #00ffff;
    font-size: 32px;
    font-weight: bold;
}
</style>
""",unsafe_allow_html=True)
from datetime import datetime
current_time = datetime.now().strftime("%d %b %Y | %H:%M:%S")
session_id = "SOC-4471-B"
st.markdown(f"""
<div style="
background:#081427;
padding:30px;
border-radius:20px;
border:2px solid #00d4ff;
box-shadow:0 0 25px rgba(0,212,255,.35);
margin-bottom:30px;
">

<div style="display:flex;justify-content:space-between;align-items:center;">

<div>

<h1 style="
color:white;
font-size:46px;
margin:0;
font-weight:800;
letter-spacing:2px;
">
🛡 AI ENHANCED HONEYPOT DASHBOARD
</h1>

<p style="
color:#00d4ff;
font-size:18px;
margin-top:10px;
letter-spacing:3px;
font-weight:bold;
">
THREAT INTELLIGENCE • ACTIVE MONITORING
</p>

<p style="
color:#8fa9c7;
font-size:15px;
margin-top:8px;
">
SESSION :
<span style="color:#00ffff;font-weight:bold;">
{session_id}
</span>
</p>

</div>

<div>

<div style="
margin-top:15px;
background:#ff2d55;
padding:8px 16px;
border-radius:25px;
font-weight:bold;
color:white;
font-size:13px;
box-shadow:0 0 12px rgba(255,45,85,.4);
text-align:center;
">
🚨 CRITICAL ALERT ACTIVE
</div>

<p style="
color:#8fa9c7;
margin-top:15px;
text-align:center;
font-size:15px;
">
{current_time}
</p>
</div>

</div>

</div>
""", unsafe_allow_html=True)

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
# Dashboard Layout
# ----------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">

    <div class="card-title">
    THREAT SCORE
    </div>

    <div class="card-value">
    {score}
    <span style="
    font-size:18px;
    color:#8fa9c7;
    ">
    /100
    </span>
    </div>

    <div style="
    color:#00ff99;
    font-size:14px;
    margin-top:15px;
    ">
    ↑ +12 Today
    </div>

    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">

    <div class="card-title">
    THREAT LEVEL
    </div>

    <div class="card-value">
    {level}
    </div>

    <div style="
    color:#ff5555;
    font-size:14px;
    margin-top:15px;
    ">
    Threshold Exceeded
    </div>

    </div>
    """, unsafe_allow_html=True)
with col3:
    st.markdown("""
    <div class="metric-card">

    <div class="card-title">
    AI CONFIDENCE
    </div>

    <div class="card-value">
    94%
    </div>

    <div style="
    color:#8fa9c7;
    font-size:14px;
    margin-top:15px;
    ">
    ThreatNet v3.1
    </div>

    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="metric-card">
        <div class="card-title">ATTACKER SKILL</div>
        <div class="card-value">ADVANCED</div>
    </div>
    """, unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
<h2 style='color:#00d4ff'>
⚡ ATTACK LIFECYCLE TIMELINE
</h2>
""", unsafe_allow_html=True)

c1,c2,c3,c4,c5,c6 = st.columns(6)

with c1:
    st.success("Recon")

with c2:
    st.success("Initial Access")

with c3:
    st.success("Credential")

with c4:
    st.warning("Payload")

with c5:
    st.info("Persistence")

with c6:
    st.info("C2")

st.markdown("""
<div style="
background:#081427;
border:1px solid #00d4ff;
border-radius:15px;
padding:20px;
margin-bottom:20px;
box-shadow:0 0 15px rgba(0,212,255,.2);
">

<h3 style="color:#00d4ff;">
🧠 ATTACKER PROFILE
</h3>

<h2 style="color:#00ffff;">
ADVANCED
</h2>

<p style="color:white;">
Malware Downloader + Privilege Escalation
</p>

<span style="
background:#14395e;
padding:8px 12px;
border-radius:6px;
color:#00ffff;
font-weight:bold;
">
APT CLASS
</span>

</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown(f"""
<div style="
background:#081427;
border:1px solid #00d4ff;
border-radius:15px;
padding:20px;
margin-bottom:20px;
box-shadow:0 0 15px rgba(0,212,255,.2);
">

<h3 style="color:#00d4ff;">
🌐 IP ANALYSIS
</h3>

<p style="font-size:18px;color:white;">
<b>Attacker IP:</b> {attacker_ip}
</p>

<p style="font-size:18px;color:white;">
<b>Country:</b> Unknown
</p>

<p style="font-size:18px;color:white;">
<b>Threat Zone:</b>
<span style="color:#ff5555;">
HIGH RISK
</span>
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"""
<div style="
background:#081427;
border:1px solid #00d4ff;
border-radius:15px;
padding:20px;
margin-bottom:20px;
box-shadow:0 0 15px rgba(0,212,255,.2);
">

<h3 style="color:#00d4ff;">
💻 DEVICE FINGERPRINT
</h3>

<p style="color:white;font-size:18px;">
<b>Client Version:</b><br>
{client_version}
</p>

<p style="color:#00ffff;">
SSH Client Detected
</p>

</div>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
<h2 style="color:#00d4ff;">
📜 COMMANDS CAPTURED
</h2>
""", unsafe_allow_html=True)

for cmd in commands:
    st.markdown(f"""
    <div style="
    background:#081427;
    border-left:5px solid #00d4ff;
    border-radius:10px;
    padding:12px;
    margin-bottom:10px;
    color:white;
    font-family:monospace;
    box-shadow:0 0 10px rgba(0,212,255,.15);
    ">
    {cmd}
    </div>
    """, unsafe_allow_html=True)
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
if score > 80:
    threat_type = "Malware Activity"
    confidence = 95
    color = "#ff3b30"

elif score > 50:
    threat_type = "Suspicious Activity"
    confidence = 85
    color = "#ffb000"

else:
    threat_type = "Low Risk Activity"
    confidence = 70
    color = "#00ff99"

st.markdown(f"""
<div style="
background:#081427;
border:1px solid #00d4ff;
border-radius:15px;
padding:20px;
margin-bottom:15px;
box-shadow:0 0 15px rgba(0,212,255,.25);
">

<h3 style="color:#00d4ff;">
🧠 Threat Type
</h3>

<p style="
font-size:24px;
font-weight:bold;
color:{color};
">
{threat_type}
</p>

<p style="
color:white;
font-size:18px;
">
AI Confidence: {confidence}%
</p>

</div>
""", unsafe_allow_html=True)
st.markdown("---")

st.markdown("""
<div style="
background:#081427;
border:1px solid #00d4ff;
border-radius:15px;
padding:15px;
margin-top:20px;
margin-bottom:10px;
box-shadow:0 0 15px rgba(0,212,255,.2);
">
<h2 style="color:#00d4ff;">
📊 THREAT DISTRIBUTION
</h2>
</div>
""", unsafe_allow_html=True)
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
st.markdown("""
<div style="
background:#081427;
border:1px solid #00d4ff;
border-radius:15px;
padding:20px;
margin-top:20px;
margin-bottom:20px;
box-shadow:0 0 15px rgba(0,212,255,.2);
">
<h2 style="color:#00d4ff;">
🤖 AI RECOMMENDATIONS
</h2>
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.success("✅ Block Suspicious IP")
    st.info("🔐 Rotate Credentials")

with col2:
    st.warning("🛡 Enable MFA")
    st.info("🔥 Update Firewall Rules")
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
