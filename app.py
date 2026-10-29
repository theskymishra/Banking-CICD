
from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)
balance = 1000.00

HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Simple Banking Application</title>
<style>
body{font-family:Arial,sans-serif;background:#f1f5f9;margin:0;padding:40px 16px}
.card{max-width:460px;margin:auto;background:white;padding:28px;border-radius:14px;
box-shadow:0 5px 20px #0001}
h1{color:#164e63;text-align:center}
.balance{background:#ecfeff;padding:20px;border-radius:10px;text-align:center}
.amount{font-size:32px;font-weight:bold;color:#0e7490}
input,button{box-sizing:border-box;width:100%;padding:12px;margin-top:12px;
border-radius:7px;font-size:16px}
input{border:1px solid #cbd5e1}
button{border:0;color:white;background:#0891b2;cursor:pointer}
.withdraw{background:#475569}
#message{text-align:center;margin-top:16px}
</style>
</head>
<body>
<div class="card">
<h1>Simple Banking App</h1>
<div class="balance">
<p>Available Balance</p>
<div class="amount" id="balance">Loading...</div>
</div>
<input type="number" id="amount" min="0.01" step="0.01"
placeholder="Enter amount">
<button onclick="transact('deposit')">Deposit Money</button>
<button class="withdraw" onclick="transact('withdraw')">Withdraw Money</button>
<p id="message"></p>
</div>
<script>
async function refreshBalance(){
 const r=await fetch('/api/balance');
 const d=await r.json();
 document.getElementById('balance').textContent=
   '₹'+Number(d.balance).toFixed(2);
}
async function transact(action){
 const amount=Number(document.getElementById('amount').value);
 const message=document.getElementById('message');
 if(!Number.isFinite(amount)||amount<=0){
   message.textContent='Enter a valid positive amount.';
   message.style.color='red';return;
 }
 try{
   const r=await fetch('/api/'+action,{
     method:'POST',headers:{'Content-Type':'application/json'},
     body:JSON.stringify({amount})
   });
   const d=await r.json();
   message.textContent=d.message;
   message.style.color=r.ok?'green':'red';
   if(r.ok){await refreshBalance();
     document.getElementById('amount').value='';}
 }catch(e){message.textContent='Request failed. Try again.';}
}
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
    return jsonify({"balance": round(balance, 2)})

def get_amount():
    data = request.get_json(silent=True) or {}
    try:
        amount = float(data.get("amount", 0))
    except (TypeError, ValueError):
        return None
    if not (0 < amount < float("inf")):
        return None
    return round(amount, 2)

@app.post("/api/deposit")
def deposit():
    global balance
    amount = get_amount()
    if amount is None:
        return jsonify({"message": "Amount must be a valid positive number."}), 400
    balance = round(balance + amount, 2)
    return jsonify({
        "message": "Deposit successful.",
        "balance": balance
    })

@app.post("/api/withdraw")
def withdraw():
    global balance
    amount = get_amount()
    if amount is None:
        return jsonify({"message": "Amount must be a valid positive number."}), 400
    if amount > balance:
        return jsonify({"message": "Insufficient balance."}), 400
    balance = round(balance - amount, 2)
    return jsonify({
        "message": "Withdrawal successful.",
        "balance": balance
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
