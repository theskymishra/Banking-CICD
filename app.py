from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)
balance = 1000.00

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NovaBank | Simple Banking</title>
<style>
*{box-sizing:border-box}
body{margin:0;background:#f1f5f9;font-family:Arial,sans-serif;color:#172033}
header{background:linear-gradient(120deg,#10234d,#2563eb);padding:35px 8%;color:white}
header h1{margin:0;font-size:32px}
header p{color:#dbeafe}
main{max-width:1000px;margin:35px auto;padding:0 20px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:20px}
.card{background:white;border-radius:18px;padding:26px;box-shadow:0 10px 30px #0f172a0d}
.label{font-size:13px;color:#64748b;letter-spacing:1px}
.amount{font-size:36px;font-weight:800;color:#173778;margin:18px 0}
input{width:100%;padding:13px;border:1px solid #cbd5e1;border-radius:9px;margin:12px 0}
button{border:0;border-radius:9px;background:#2563eb;color:white;padding:13px 18px;font-weight:bold;cursor:pointer}
button:hover{background:#1d4ed8}
.message{margin-top:14px;font-size:14px;font-weight:bold}
footer{text-align:center;color:#64748b;padding:30px}
</style>
</head>
<body>
<header>
<h1>NovaBank</h1>
<p>Simple banking. Smarter everyday money management.</p>
</header>
<main>
<div class="grid">
<section class="card">
<div class="label">AVAILABLE BALANCE</div>
<div class="amount" id="balance">Loading...</div>
<p>Demo account · INR</p>
</section>
<section class="card">
<h2>Deposit Money</h2>
<p>Add funds to your demo account.</p>
<form id="depositForm">
<input id="amount" type="number" min="0.01" step="0.01"
placeholder="Enter amount (₹)" required>
<button type="submit">Deposit Funds</button>
</form>
<div id="message" class="message"></div>
</section>
</div>
</main>
<footer>NovaBank · CI/CD Practical · Python · Docker · Kubernetes</footer>
<script>
async function refreshBalance(){
 const r=await fetch('/api/balance');
 const d=await r.json();
 document.getElementById('balance').textContent='₹'+Number(d.balance).toFixed(2);
}
document.getElementById('depositForm').addEventListener('submit',async e=>{
 e.preventDefault();
 const amount=Number(document.getElementById('amount').value);
 const r=await fetch('/api/deposit',{
  method:'POST',headers:{'Content-Type':'application/json'},
  body:JSON.stringify({amount})
 });
 const d=await r.json();
 document.getElementById('message').textContent=d.message;
 if(r.ok){
  document.getElementById('amount').value='';
  await refreshBalance();
 }
});
refreshBalance();
</script>
</body>
</html>
"""

@app.get("/")
def home():
    return render_template_string(HTML)

@app.get("/api/balance")
def get_balance():
    return jsonify(balance=round(balance, 2))

@app.post("/api/deposit")
def deposit():
    global balance
    data = request.get_json(silent=True) or {}
    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        return jsonify(message="Enter a valid amount."), 400

    if amount <= 0:
        return jsonify(message="Amount must be greater than zero."), 400

    balance = round(balance + amount, 2)
    return jsonify(message="Deposit successful.", balance=balance)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
