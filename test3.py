import streamlit as st
import streamlit.components.v1 as components

# Sanidi ukurasa
st.set_page_config(page_title="Kikao cha Wanaume", layout="wide", initial_sidebar_state="collapsed")

st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { visibility: hidden !important; }
        iframe { width: 100%; border: none; min-height: 100vh; }
    </style>
""", unsafe_allow_html=True)

SUPABASE_URL = "https://xickklzlmwaobzobwyws.supabase.co"
SUPABASE_KEY = "sb_publishable_94BpD9gpOpYyWryIhzBjog_kxQRAG4W"

# Wahusika wote wanne
wahusika = ["Meshack", "Mwakitinya", "Fadhira", "Michael"]

html_code = f"""
<!DOCTYPE html>
<html lang="sw">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8fafc; margin: 0; padding-bottom: 50px; }}
        .glass-card {{ background: #ffffff; border: 1px solid #e2e8f0; border-radius: 2rem; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); }}
        .deadline-card {{ background: linear-gradient(135deg, #fbbf24 0%, #f59e0b 100%); }}
        .custom-scroll::-webkit-scrollbar {{ width: 5px; }}
        .custom-scroll::-webkit-scrollbar-thumb {{ background: #10b981; border-radius: 10px; }}
    </style>
</head>
<body>

    <div class="bg-white border-b px-6 py-8 text-center mb-8">
        <h1 class="text-2xl md:text-4xl font-extrabold text-slate-900 uppercase">
            Ingiza Majina kwa ajili ya <br>
            <span class="text-emerald-600 italic">Kikao cha Wanaume</span>
        </h1>
    </div>

    <div class="max-w-[92%] mx-auto mb-10">
        <div class="deadline-card rounded-[2.5rem] p-8 md:p-10 flex flex-col md:flex-row items-center justify-between text-white border-4 border-white shadow-xl">
            <div class="text-center md:text-left mb-6 md:mb-0">
                <p class="text-amber-900 font-bold text-xs uppercase tracking-widest mb-1">Muda wa Mwisho (Deadline)</p>
                <h2 class="text-2xl md:text-3xl font-black text-amber-950 uppercase">Leo saa 3:00 Usiku</h2>
            </div>
            <div id="countdown" class="text-5xl md:text-7xl font-black text-slate-900 tabular-nums">00:00:00</div>
        </div>
    </div>

    <div class="max-w-[95%] mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-8 px-4">
        
        <div class="glass-card p-6 md:p-8 flex flex-col">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-3xl font-black text-slate-800">Meshack</h3>
                <span id="badge-Meshack" class="px-4 py-1 rounded-full text-[10px] font-black uppercase bg-slate-100 text-slate-400 tracking-widest">Inasubiri</span>
            </div>
            <div id="progress-Meshack" class="mb-6"></div>
            <div id="form-Meshack" class="space-y-4 mb-8">
                <input type="text" id="in-n-Meshack" placeholder="Jina la Mwanachama" class="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl outline-none focus:border-emerald-500 font-bold text-slate-700 transition-all">
                <input type="tel" id="in-p-Meshack" placeholder="Namba ya Simu" class="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl outline-none focus:border-emerald-500 font-bold text-slate-700 transition-all">
                <button onclick="sendData('Meshack')" id="btn-Meshack" class="w-full bg-emerald-500 text-white p-4 rounded-2xl font-black shadow-lg hover:bg-emerald-600 uppercase tracking-widest text-sm transition-all">Hifadhi</button>
            </div>
            <div class="mt-auto pt-4 border-t border-slate-100">
                <p class="text-[10px] font-bold text-slate-400 uppercase mb-4 tracking-widest text-center">Miamala ya Hivi Karibuni</p>
                <div id="list-Meshack" class="custom-scroll space-y-2 overflow-y-auto max-h-[200px]"></div>
            </div>
        </div>

        <div class="glass-card p-6 md:p-8 flex flex-col">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-3xl font-black text-slate-800">Mwakitinya</h3>
                <span id="badge-Mwakitinya" class="px-4 py-1 rounded-full text-[10px] font-black uppercase bg-slate-100 text-slate-400 tracking-widest">Inasubiri</span>
            </div>
            <div id="progress-Mwakitinya" class="mb-6"></div>
            <div id="form-Mwakitinya" class="space-y-4 mb-8">
                <input type="text" id="in-n-Mwakitinya" placeholder="Jina la Mwanachama" class="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl outline-none focus:border-emerald-500 font-bold text-slate-700 transition-all">
                <input type="tel" id="in-p-Mwakitinya" placeholder="Namba ya Simu" class="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl outline-none focus:border-emerald-500 font-bold text-slate-700 transition-all">
                <button onclick="sendData('Mwakitinya')" id="btn-Mwakitinya" class="w-full bg-emerald-500 text-white p-4 rounded-2xl font-black shadow-lg hover:bg-emerald-600 uppercase tracking-widest text-sm transition-all">Hifadhi</button>
            </div>
            <div class="mt-auto pt-4 border-t border-slate-100">
                <p class="text-[10px] font-bold text-slate-400 uppercase mb-4 tracking-widest text-center">Miamala ya Hivi Karibuni</p>
                <div id="list-Mwakitinya" class="custom-scroll space-y-2 overflow-y-auto max-h-[200px]"></div>
            </div>
        </div>

        <div class="glass-card p-6 md:p-8 flex flex-col">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-3xl font-black text-slate-800">Fadhira</h3>
                <span id="badge-Fadhira" class="px-4 py-1 rounded-full text-[10px] font-black uppercase bg-slate-100 text-slate-400 tracking-widest">Inasubiri</span>
            </div>
            <div id="progress-Fadhira" class="mb-6"></div>
            <div id="form-Fadhira" class="space-y-4 mb-8">
                <input type="text" id="in-n-Fadhira" placeholder="Jina la Mwanachama" class="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl outline-none focus:border-emerald-500 font-bold text-slate-700 transition-all">
                <input type="tel" id="in-p-Fadhira" placeholder="Namba ya Simu" class="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl outline-none focus:border-emerald-500 font-bold text-slate-700 transition-all">
                <button onclick="sendData('Fadhira')" id="btn-Fadhira" class="w-full bg-emerald-500 text-white p-4 rounded-2xl font-black shadow-lg hover:bg-emerald-600 uppercase tracking-widest text-sm transition-all">Hifadhi</button>
            </div>
            <div class="mt-auto pt-4 border-t border-slate-100">
                <p class="text-[10px] font-bold text-slate-400 uppercase mb-4 tracking-widest text-center">Miamala ya Hivi Karibuni</p>
                <div id="list-Fadhira" class="custom-scroll space-y-2 overflow-y-auto max-h-[200px]"></div>
            </div>
        </div>

        <div class="glass-card p-6 md:p-8 flex flex-col">
            <div class="flex justify-between items-center mb-6">
                <h3 class="text-3xl font-black text-slate-800">Michael</h3>
                <span id="badge-Michael" class="px-4 py-1 rounded-full text-[10px] font-black uppercase bg-slate-100 text-slate-400 tracking-widest">Inasubiri</span>
            </div>
            <div id="progress-Michael" class="mb-6"></div>
            <div id="form-Michael" class="space-y-4 mb-8">
                <input type="text" id="in-n-Michael" placeholder="Jina la Mwanachama" class="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl outline-none focus:border-emerald-500 font-bold text-slate-700 transition-all">
                <input type="tel" id="in-p-Michael" placeholder="Namba ya Simu" class="w-full p-4 bg-slate-50 border-2 border-transparent rounded-2xl outline-none focus:border-emerald-500 font-bold text-slate-700 transition-all">
                <button onclick="sendData('Michael')" id="btn-Michael" class="w-full bg-emerald-500 text-white p-4 rounded-2xl font-black shadow-lg hover:bg-emerald-600 uppercase tracking-widest text-sm transition-all">Hifadhi</button>
            </div>
            <div class="mt-auto pt-4 border-t border-slate-100">
                <p class="text-[10px] font-bold text-slate-400 uppercase mb-4 tracking-widest text-center">Miamala ya Hivi Karibuni</p>
                <div id="list-Michael" class="custom-scroll space-y-2 overflow-y-auto max-h-[200px]"></div>
            </div>
        </div>

    </div>

    <script>
        const _s = supabase.createClient("{SUPABASE_URL}", "{SUPABASE_KEY}");
        const users = ["Meshack", "Mwakitinya", "Fadhira", "Michael"];

        function startTimer() {{
            const update = () => {{
                const now = new Date();
                const dl = new Date(); dl.setHours(21, 0, 0, 0);
                let diff = dl - now;
                if(diff <= 0) {{ document.getElementById('countdown').innerText = "00:00:00"; return; }}
                const h = String(Math.floor(diff/3600000)).padStart(2,'0');
                const m = String(Math.floor((diff%3600000)/60000)).padStart(2,'0');
                const s = String(Math.floor((diff%60000)/1000)).padStart(2,'0');
                document.getElementById('countdown').innerText = `${{h}}:${{m}}:${{s}}`;
            }};
            setInterval(update, 1000); update();
        }}

        async function refreshUI() {{
            for (const u of users) {{
                const {{ data, count }} = await _s.from('orodha_majina').select('*', {{ count: 'exact' }}).eq('mhusika', u).order('created_at', {{ ascending: false }});
                const c = count || 0;
                const p = Math.min((c/20)*100, 100);
                
                document.getElementById(`progress-${{u}}`).innerHTML = `
                    <div class="flex justify-between items-end mb-2">
                        <span class="text-5xl font-black text-slate-900">${{c}}<span class="text-xl text-slate-300">/20</span></span>
                        <span class="text-sm font-black ${{p === 100 ? 'text-emerald-600' : 'text-amber-600'}}">${{Math.round(p)}}%</span>
                    </div>
                    <div class="w-full h-4 bg-slate-100 rounded-full overflow-hidden p-1 shadow-inner">
                        <div class="h-full rounded-full transition-all duration-1000 ${{p === 100 ? 'bg-emerald-500' : 'bg-amber-400'}}" style="width: ${{p}}%"></div>
                    </div>
                `;

                const badge = document.getElementById(`badge-${{u}}`);
                if(p === 100) {{
                    badge.innerText = "KAMILIFU";
                    badge.className = "px-4 py-1 rounded-full text-[10px] font-black bg-emerald-100 text-emerald-600 tracking-widest";
                }} else {{
                    badge.innerText = "INASUBIRI";
                    badge.className = "px-4 py-1 rounded-full text-[10px] font-black bg-amber-100 text-amber-600 tracking-widest";
                }}

                document.getElementById(`list-${{u}}`).innerHTML = data.map((item, idx) => `
                    <div class="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-white shadow-sm mb-1">
                        <div><p class="font-black text-slate-800 text-sm">${{item.jina_la_mtu}}</p><p class="text-[10px] text-slate-400 font-bold uppercase">${{item.namba_ya_simu}}</p></div>
                        <span class="text-[10px] font-black text-slate-300 uppercase">${{c-idx}}</span>
                    </div>
                `).join('') || '<p class="text-xs text-slate-300 italic text-center py-4">Bado tupu...</p>';
            }}
        }}

        async function sendData(user) {{
            const nI = document.getElementById(`in-n-${{user}}`);
            const pI = document.getElementById(`in-p-${{user}}`);
            const btn = document.getElementById(`btn-${{user}}`);
            if(!nI.value || !pI.value) return alert("Jaza Jina na Simu!");
            btn.disabled = true; btn.innerText = "HIFADHI...";
            const {{ error }} = await _s.from('orodha_majina').insert([{{ mhusika: user, jina_la_mtu: nI.value.trim(), namba_ya_simu: pI.value.trim() }}]);
            if(!error) {{ nI.value = ''; pI.value = ''; await refreshUI(); }}
            btn.disabled = false; btn.innerText = "HIFADHI";
        }}

        startTimer(); refreshUI();
        setInterval(refreshUI, 10000);
    </script>
</body>
</html>
"""

components.html(html_code, height=1800, scrolling=True)
