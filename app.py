from flask import Flask, request, render_template_string, jsonify
import random

app = Flask(__name__)

# Mock database
users = {"user@example.com": {"otp": None, "verified": False}}

# HTML template
html_template = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Payment Auth Demo</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { background-color:#f8f9fa; font-family:Segoe UI, sans-serif; }
        .card { max-width: 400px; margin:auto; margin-top:50px; padding:20px; border-radius:10px; box-shadow:0 4px 12px rgba(0,0,0,0.1); }
        .output { margin-top:15px; padding:10px; background:#f1f3f5; border-radius:5px; min-height:40px; }
    </style>
</head>
<body>
<div class="card">
    <h3 class="text-center mb-4">Payment Authorization</h3>
    <input type="email" id="email" class="form-control mb-2" placeholder="Email">
    <button class="btn btn-primary w-100 mb-2" onclick="sendOtp()">Send OTP</button>
    <input type="text" id="otp" class="form-control mb-2" placeholder="Enter OTP">
    <button class="btn btn-success w-100 mb-2" onclick="verifyOtp()">Verify & Pay</button>
    <div class="output" id="output">Status messages will appear here</div>
</div>

<script>
async function sendOtp() {
    let email = document.getElementById("email").value;
    let res = await fetch("/send_otp", {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({email})
    });
    let data = await res.json();
    document.getElementById("output").innerText = data.message;
}

async function verifyOtp() {
    let email = document.getElementById("email").value;
    let otp = document.getElementById("otp").value;
    let res = await fetch("/verify_otp", {
        method:"POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({email, otp})
    });
    let data = await res.json();
    document.getElementById("output").innerText = data.message;
}
</script>
</body>
</html>
"""

# Routes
@app.route("/")
def index():
    return render_template_string(html_template)

@app.route("/send_otp", methods=["POST"])
def send_otp():
    email = request.json.get("email")
    if email not in users:
        users[email] = {"otp": None, "verified": False}
    otp = str(random.randint(100000, 999999))
    users[email]["otp"] = otp
    # In real app: send OTP via SMS/email
    print(f"DEBUG: OTP for {email} is {otp}")
    return jsonify({"message": f"OTP sent to {email} (Check console in demo)"})

@app.route("/verify_otp", methods=["POST"])
def verify_otp():
    data = request.json
    email = data.get("email")
    otp = data.get("otp")
    if email in users and users[email]["otp"] == otp:
        users[email]["verified"] = True
        return jsonify({"message": "✅ OTP verified. Payment authorized!"})
    return jsonify({"message": "❌ Invalid OTP or email"})


if __name__ == "__main__":
    app.run(debug=True)