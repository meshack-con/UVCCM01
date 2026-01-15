import streamlit as st
import streamlit.components.v1 as components

# 1. Config ya Streamlit
st.set_page_config(page_title="Smart-Hifadhi Cloud", layout="wide")

# 2. Ficha Header na Padding za Streamlit
st.markdown("""
    <style>
        .block-container { padding: 0rem; }
        header { visibility: hidden; }
        footer { visibility: hidden; }
        iframe { border: none; }
    </style>
    """, unsafe_allow_html=True)

# 3. Credentials zako za Supabase
SUPABASE_URL = "https://bzolhpmorjkdjfaotjgg.supabase.co"
SUPABASE_KEY = "sb_publishable_DQIXCrVzqf-OPtZBnouoGA_FkroIASY"

# 4. HTML, CSS, na JS Code
html_code = f"""
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Smart-Hifadhi Pro v6.0 | Supabase</title>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{ 
            --primary: #4361ee; --success: #2ecc71; --danger: #e74c3c; 
            --warning: #f1c40f; --dark: #0f172a; --bg: #f1f5f9; --white: #ffffff;
        }}
        body {{ font-family: 'Inter', sans-serif; background: var(--bg); margin: 0; padding: 0; color: var(--dark); }}
        .header {{ background: var(--dark); color: white; padding: 60px 20px; text-align: center; }}
        
        .stats-grid {{ 
            display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); 
            gap: 20px; max-width: 1200px; margin: -40px auto 20px auto; padding: 0 20px; 
        }}
        .stat-card {{ 
            background: var(--white); padding: 25px; border-radius: 20px; 
            box-shadow: 0 10px 15px rgba(0,0,0,0.05); text-align: center; 
        }}
        .stat-card .amount {{ font-size: 1.6rem; font-weight: 800; margin-top: 8px; display: block; }}

        .container {{ max-width: 1200px; margin: 0 auto; padding: 20px; display: grid; grid-template-columns: 1fr 350px; gap: 30px; }}
        @media (max-width: 900px) {{ .container {{ grid-template-columns: 1fr; }} }}
        
        .card {{ background: var(--white); padding: 25px; border-radius: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.02); margin-bottom: 25px; }}
        input, select {{ width: 100%; padding: 14px; border: 1.5px solid #e2e8f0; border-radius: 12px; margin-top: 10px; box-sizing: border-box; }}
        .btn {{ width: 100%; padding: 16px; border: none; border-radius: 12px; background: var(--primary); color: white; font-weight: 700; cursor: pointer; transition: 0.3s; margin-top: 15px; }}
        .btn:active {{ transform: scale(0.98); }}
        
        .alert-box {{ background: #e0f2fe; border-left: 5px solid var(--primary); padding: 15px; border-radius: 12px; margin-bottom: 25px; font-size: 0.9rem; }}
        .bar-bg {{ background: #e2e8f0; height: 10px; border-radius: 50px; margin-top: 10px; overflow: hidden; }}
        .bar-fill {{ background: var(--success); height: 100%; width: 0%; transition: 1s ease-in-out; }}
    </style>
</head>
<body>

<div class="header">
    <h1 style="margin:0;">Smart-Hifadhi Pro 💎</h1>
    <p style="opacity:0.8;">Cloud Managed by Supabase</p>
</div>

<div class="stats-grid">
    <div class="stat-card"><h4>Uwekezaji (50%)</h4><span class="amount" id="dashInvest" style="color:var(--success)">0</span></div>
    <div class="stat-card"><h4>Lazima (20%)</h4><span class="amount" id="dashEss" style="color:var(--primary)">0</span></div>
    <div class="stat-card"><h4>Sio Lazima (10%)</h4><span class="amount" id="dashLife" style="color:var(--warning)">0</span></div>
    <div class="stat-card"><h4>Emergency (10%)</h4><span class="amount" id="dashEmerg" style="color:var(--danger)">0</span></div>
</div>

<div class="container">
    <main>
        <div id="status" class="alert-box">🔄 Inasawazisha na Supabase Cloud...</div>
        
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
            <div class="card">
                <h3>💰 Ingiza Mapato</h3>
                <input type="number" id="incomeVal" placeholder="Kiasi (TSH)">
                <button class="btn" onclick="handleIncome()">Hifadhi & Gawa</button>
            </div>
            <div class="card">
                <h3>💸 Tumia Fedha</h3>
                <input type="number" id="expenseVal" placeholder="Kiasi (TSH)">
                <select id="expenseType">
                    <option value="invest_acc">Kutoka 'Uwekezaji'</option>
                    <option value="essential_acc">Kutoka 'Lazima'</option>
                    <option value="life_acc">Kutoka 'Sio Lazima'</option>
                    <option value="emergency_acc">Kutoka 'Emergency'</option>
                </select>
                <button class="btn" style="background:var(--dark)" onclick="handleExpense()">Toa Pesa</button>
            </div>
        </div>

        <div class="card">
            <h3>📊 Mwenendo wa Akaunti</h3>
            <div style="max-width: 400px; margin: 0 auto;">
                <canvas id="healthChart"></canvas>
            </div>
        </div>
    </main>

    <aside>
        <div class="card">
            <h3>🎯 Lengo la Uwekezaji</h3>
            <div id="goalText" style="font-weight:700; color:var(--primary); margin-bottom:5px;">0% Imekamilika</div>
            <div class="bar-bg"><div id="goalBar" class="bar-fill"></div></div>
            <input type="number" id="goalVal" placeholder="Weka Lengo la Mwaka" style="margin-top:20px;">
            <button class="btn" style="background:var(--success)" onclick="updateGoal()">Weka Lengo</button>
        </div>

        <div class="card">
            <h3>📜 Miamala ya Karibuni</h3>
            <div id="txList" style="font-size: 0.85rem; max-height: 300px; overflow-y: auto;">
                Inatafuta miamala...
            </div>
        </div>
    </aside>
</div>

<script>
    const _client = supabase.createClient("{SUPABASE_URL}", "{SUPABASE_KEY}");
    let currentBalances = {{}};

    const f = (n) => new Intl.NumberFormat('en-TZ').format(Math.round(n || 0));

    async function init() {{
        try {{
            // 1. Fetch Balances
            const {{ data: bal, error: e1 }} = await _client.from('balances').select('*').eq('id', 1).single();
            if (e1) throw e1;
            currentBalances = bal;

            // 2. Fetch Settings (Goal)
            const {{ data: set, error: e2 }} = await _client.from('settings').select('*').eq('id', 1).single();
            if (e2) throw e2;
            
            // 3. Fetch Recent Transactions
            const {{ data: txs }} = await _client.from('transactions').select('*').order('created_at', {{ ascending: false }}).limit(5);

            render(bal, set.yearly_goal, txs);
            document.getElementById('status').innerText = "✅ Cloud imesawazishwa!";
        }} catch (err) {{
            console.error(err);
            document.getElementById('status').innerText = "❌ Hitilafu ya kuunganisha Database!";
        }}
    }}

    async function handleIncome() {{
        const amt = parseFloat(document.getElementById('incomeVal').value);
        if(!amt) return;

        const update = {{
            invest_acc: currentBalances.invest_acc + (amt * 0.50),
            essential_acc: currentBalances.essential_acc + (amt * 0.20),
            life_acc: currentBalances.life_acc + (amt * 0.10),
            emergency_acc: currentBalances.emergency_acc + (amt * 0.10),
            tithe_acc: currentBalances.tithe_acc + (amt * 0.10)
        }};

        await _client.from('balances').update(update).eq('id', 1);
        await _client.from('transactions').insert([{{ type: 'In', category: 'Mapato', amount: amt, invested_amount: amt*0.5 }}]);
        
        document.getElementById('incomeVal').value = '';
        init();
    }

    async function handleExpense() {{
        const amt = parseFloat(document.getElementById('expenseVal').value);
        const cat = document.getElementById('expenseType').value;
        if(!amt || amt > currentBalances[cat]) return alert("Salio halitoshi!");

        const update = {{}};
        update[cat] = currentBalances[cat] - amt;

        await _client.from('balances').update(update).eq('id', 1);
        await _client.from('transactions').insert([{{ type: 'Out', category: cat, amount: amt }}]);
        
        document.getElementById('expenseVal').value = '';
        init();
    }

    async function updateGoal() {{
        const g = parseFloat(document.getElementById('goalVal').value);
        await _client.from('settings').update({{ yearly_goal: g }}).eq('id', 1);
        init();
    }}

    function render(bal, goal, txs) {{
        document.getElementById('dashInvest').innerText = f(bal.invest_acc);
        document.getElementById('dashEss').innerText = f(bal.essential_acc);
        document.getElementById('dashLife').innerText = f(bal.life_acc);
        document.getElementById('dashEmerg').innerText = f(bal.emergency_acc);

        // Progress Bar
        const pc = goal > 0 ? (bal.invest_acc / goal) * 100 : 0;
        document.getElementById('goalBar').style.width = Math.min(pc, 100) + "%";
        document.getElementById('goalText').innerText = pc.toFixed(1) + "% Imekamilika";

        // Tx List
        const listHtml = txs.map(t => `
            <div style="display:flex; justify-content:space-between; padding:8px 0; border-bottom:1px solid #eee;">
                <span>${{t.category}}</span>
                <b style="color:${{t.type==='In'?'green':'red'}}">${{t.type==='In'?'+':'-'}}${{f(t.amount)}}</b>
            </div>
        `).join('');
        document.getElementById('txList').innerHTML = listHtml;

        updateChart(bal);
    }}

    let chart;
    function updateChart(bal) {{
        const ctx = document.getElementById('healthChart').getContext('2d');
        if(chart) chart.destroy();
        chart = new Chart(ctx, {{
            type: 'doughnut',
            data: {{
                labels: ['Invest', 'Essential', 'Lifestyle', 'Emergency'],
                datasets: [{{
                    data: [bal.invest_acc, bal.essential_acc, bal.life_acc, bal.emergency_acc],
                    backgroundColor: ['#2ecc71', '#4361ee', '#f1c40f', '#e74c3c'],
                    borderWidth: 0
                }}]
            }},
            options: {{ cutout: '75%', plugins: {{ legend: {{ position: 'bottom' }} }} }}
        }});
    }}

    init();
</script>
</body>
</html>
"""

# 5. Execute
components.html(html_code, height=1200, scrolling=True)
