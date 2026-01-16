import streamlit as st
import streamlit.components.v1 as components

# Sanidi ukurasa
st.set_page_config(page_title="Kikao cha Wanaume", layout="wide", initial_sidebar_state="collapsed")

# CSS ya kuimarisha muonekano wa Streamlit
st.markdown("""
    <style>
        .block-container { padding: 0 !important; max-width: 100% !important; }
        header, footer { visibility: hidden !important; }
        iframe { width: 100%; border: none; min-height: 100vh; }
    </style>
""", unsafe_allow_html=True)

SUPABASE_URL = "https://xickklzlmwaobzobwyws.supabase.co"
SUPABASE_KEY = "sb_publishable_94BpD9gpOpYyWryIhzBjog_kxQRAG4W"

# Tumesawazisha muundo wa HTML hapa chini
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
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #ffffff; margin: 0; padding-bottom: 50px; color: #1e293b; }}
        .header-gradient {{ background: linear-gradient(to right, #ffffff, #f0fdf4, #ffffff); }}
        .deadline-box {{ background: #fbbf24; border: 4px solid #ffffff; box-shadow: 0 15px 30px -10px rgba(251, 191, 36, 0.4); }}
        .user-card {{ background: #ffffff; border: 1px solid #f1f5f9; box-shadow: 0 10px 25px -5px rgba(0,0,0,0.04); border-radius: 2.5rem; transition: all 0.3s ease; }}
        .user-card:hover {{ transform: translateY(-5px); box-shadow: 0 20px 30px -10px rgba(0,0,0,0.07); }}
        .custom-scroll::-webkit-scrollbar {{ width: 4px; }}
        .custom-scroll::-webkit-scrollbar-thumb {{ background: #10b981; border-radius: 10px; }}
        input {{ border: 2px solid #f1f5f9 !important; }}
        input:focus {{ border-color: #10b981 !important; background: #ffffff !important; }}
    </style>
</head>
<body>

    <div class="header-gradient border-b px-6 py-10 text-center mb-8">
        <h1 class="text-3xl md:text-5xl font-extrabold text-slate-900 tracking-tight leading-tight">
            INGIZA MAJINA KWA AJILI YA <br>
            <span class="text-emerald-600 italic">KIKAO CHA WANAUME</span>
        </h1>
    </div>

    <div class="max-w-[90%] mx-auto mb-12">
        <div class="deadline-box rounded-[3rem] p-8 md:p-12 text-center">
            <p class="text-amber-900 font-bold text-sm uppercase tracking-[0.3em] mb-2">Muda wa Mwisho (Deadline)</p>
            <h2 class="text-xl md:text-2xl font-bold text-amber-950 mb-4 text-white uppercase">Leo saa 3:00 Usiku</h2>
            <div id="countdown" class="text-6xl md:text-8xl font-black text-slate-900 tracking-tighter tabular-nums">00:00:00</div>
        </div>
    </div>

    <div class="max-w-[95%] mx-auto grid grid-cols-1 md:grid-cols-3 gap-8 px-4">
        
        <div class="user-card p-8 flex flex-col h-full">
            <div class="flex justify-between items-center mb-8">
                <h3 class="text-3xl font-black text-slate-800">Meshack</h3>
                <span id="badge-Meshack" class="px-4 py-1 rounded-full text-[10px] font-black uppercase tracking-widest bg-slate-100 text-slate-400">Loading...</span>
            </div>
            <div id="progress-Meshack" class="mb-8"></div>
            <div id="form-Meshack" class="space-y-4 mb-10">
                <div id="active-form-Meshack">
                    <input type="text" id="in-n-Meshack" placeholder="Jina la Mwanachama" class="w-full p-4 bg-slate-50 rounded-2xl outline-none mb-3 font-bold text-slate-700">
                    <input type="tel" id="in-p-Meshack" placeholder="Namba ya Simu" class="w-full p-4 bg-slate-50 rounded-2xl outline-none mb-4 font-bold text-slate-700">
                    <button onclick="sendData('Meshack')" id="btn-Meshack" class="w-full bg-emerald-500 text-white p-5 rounded-2xl font-black shadow-lg shadow-emerald-100 hover:bg-emerald-600 active:scale-95 transition-all uppercase tracking-widest">Hifadhi</button>
                </div>
                <div id="msg-Meshack" class="hidden p-6 bg-emerald-50 text-emerald-700 rounded-3xl text-center border-2 border-emerald-100 font-black text-sm uppercase">✅ Lengo Limetimia</div>
            </div>
            <div class="mt-auto pt-6 border-t">
                <p class="text-[10px] font-bold text-slate-400 uppercase mb-4 tracking-widest text-center">Miamala ya Hivi Karibuni</p>
                <div id="list-Meshack" class="custom-scroll space-y-2 overflow-y-auto max-h-[250px] pr-2"></div>
            </div>
        </div>

        <div class="user-card p-8 flex flex-col h-full">
            <div class="flex justify-between items-center mb-8">
                <h3 class="text-3xl font-black text-slate-800">Mwakitinya</h3>
                <span id="badge-Mwakitinya" class="px-4 py-1 rounded-full text-[10px] font-black uppercase tracking-widest bg-slate-100 text-slate-400">Loading...</span>
            </div>
            <div id="progress-Mwakitinya" class="mb-8"></div>
            <div id="form-Mwakitinya" class="space-y-4 mb-10">
                <div id="active-form-Mwakitinya">
                    <input type="text" id="in-n-Mwakitinya" placeholder="Jina la Mwanachama" class="w-full p-4 bg-slate-50 rounded-2xl outline-none mb-3 font-bold text-slate-700">
                    <input type="tel" id="in-p-Mwakitinya" placeholder="Namba ya Simu" class="w-full p-4 bg-slate-50 rounded-2xl outline-none mb-4 font-bold text-slate-700">
                    <button onclick="sendData('Mwakitinya')" id="btn-Mwakitinya" class="w-full bg-emerald-500 text-white p-5 rounded-2xl font-black shadow-lg shadow-emerald-100 hover:bg-emerald-600 active:scale-95 transition-all uppercase tracking-widest">Hifadhi</button>
                </div>
                <div id="msg-Mwakitinya" class="hidden p-6 bg-emerald-50 text-emerald-700 rounded-3xl text-center border-2 border-emerald-100 font-black text-sm uppercase">✅ Lengo Limetimia</div>
            </div>
            <div class="mt-auto pt-6 border-t">
                <p class="text-[10px] font-bold text-slate-400 uppercase mb-4 tracking-widest text-center">Miamala ya Hivi Karibuni</p>
                <div id="list-Mwakitinya" class="custom-scroll space-y-2 overflow-y-auto max-h-[250px] pr-2"></div>
            </div>
        </div>

        <div class="user-card p-8 flex flex-col h-full">
            <div class="flex justify-between items-center mb-8">
                <h3 class="text-3xl font-black text-slate-800">Fadhira</h3>
                <span id="badge-Fadhira" class="px-4 py-1 rounded-full text-[10px] font-black uppercase tracking-widest bg-slate-100 text-slate-400">Loading...</span>
            </div>
            <div id="progress-Fadhira" class="mb-8"></div>
            <div id="form-Fadhira" class="space-y-4 mb-10">
                <div id="active-form-Fadhira">
                    <input type="text" id="in-n-Fadhira" placeholder="Jina la Mwanachama" class="w-full p-4 bg-slate-50 rounded-2xl outline-none mb-3 font-bold text-slate-700">
                    <input type="tel" id="in-p-Fadhira" placeholder="Namba ya Simu" class="w-full p-4 bg-slate-50 rounded-2xl outline-none mb-4 font-bold text-slate-700">
                    <button onclick="sendData('Fadhira')" id="btn-Fadhira" class="w-full bg-emerald-500 text-white p-5 rounded-2xl font-black shadow-lg shadow-emerald-100 hover:bg-emerald-600 active:scale-95 transition-all uppercase tracking-widest">Hifadhi</button>
                </div>
                <div id="msg-Fadhira" class="hidden p-6 bg-emerald-50 text-emerald-700 rounded-3xl text-center border-2 border-emerald-100 font-black text-sm uppercase">✅ Lengo Limetimia</div>
            </div>
            <div class="mt-auto pt-6 border-t">
                <p class="text-[10px] font-bold text-slate-400 uppercase mb-4 tracking-widest text-center">Miamala ya Hivi Karibuni</p>
                <div id="list-Fadhira" class="custom-scroll space-y-2 overflow-y-auto max-h-[250px] pr-2"></div>
            </div>
        </div>

    </div>

    <script>
        const _s = supabase.createClient("{SUPABASE_URL}", "{SUPABASE_KEY}");
        const names = ["Meshack", "Mwakitinya", "Fadhira"];

        function timer() {{
            const up = () => {{
                const now = new Date();
                const dl = new Date(); dl.setHours(21,0,0,0);
                let d = dl - now;
                if(d <= 0) {{ document.getElementById('countdown').innerText = "00:00:00"; return; }}
                const h = String(Math.floor(d/3600000)).padStart(2,'0');
                const m = String(Math.floor((d%3600000)/60000)).padStart(2,'0');
                const s = String(Math.floor((d%60000)/1000)).padStart(2,'0');
                document.getElementById('countdown').innerText = `${{h}}:${{m}}:${{s}}`;
            }};
            setInterval(up, 1000); up();
        }}

        async function ui() {{
            for (const u of names) {{
                const {{ data, count }} = await _s.from('orodha_majina').select('*', {{ count: 'exact' }}).eq('mhusika', u).order('created_at', {{ ascending: false }});
                const c = count || 0;
                const p = Math.min((c/20)*100, 100);
                
                document.getElementById(`progress-${{u}}`).innerHTML = `
                    <div class="flex justify-between items-end mb-3">
                        <span class="text-6xl font-black text-slate-900">${{c}}<span class="text-xl text-slate-300">/20</span></span>
                        <span class="text-sm font-black ${{p === 100 ? 'text-emerald-600' : 'text-amber-500'}}">${{Math.round(p)}}%</span>
                    </div>
                    <div class="w-full h-5 bg-slate-100 rounded-full overflow-hidden p-1 shadow-inner">
                        <div class="h-full rounded-full transition-all duration-1000 ${{p === 100 ? 'bg-emerald-500' : 'bg-amber-400'}}" style="width: ${{p}}%"></div>
                    </div>
                `;

                const b = document.getElementById(`badge-${{u}}`);
                if(p === 100) {{
                    b.innerText = "Kamilifu";
                    b.className = "px-4 py-1 rounded-full text-[10px] font-black uppercase bg-emerald-100 text-emerald-600 tracking-widest";
                    document.getElementById(`active-form-${{u}}`).classList.add('hidden');
                    document.getElementById(`msg-${{u}}`).classList.remove('hidden');
                }} else {{
                    b.innerText = "Inaendelea";
                    b.className = "px-4 py-1 rounded-full text-[10px] font-black uppercase bg-amber-100 text-amber-600 tracking-widest";
                }}

                document.getElementById(`list-${{u}}`).innerHTML = data.map((x, i) => `
                    <div class="flex items-center justify-between p-4 bg-slate-50 rounded-2xl border border-white mb-2">
                        <div>
                            <p class="font-black text-slate-800 text-sm">${{x.jina_la_mtu}}</p>
                            <p class="text-[10px] text-slate-400 font-bold uppercase tracking-tighter">${{x.namba_ya_simu}}</p>
                        </div>
                        <span class="bg-white border text-[10px] font-black w-6 h-6 flex items-center justify-center rounded-full text-slate-300">${{c-i}}</span>
                    </div>
                `).join('') || '<p class="text-xs text-slate-300 italic text-center py-4 uppercase font-bold tracking-widest">Bado tupu</p>';
            }}
        }}

        async function sendData(u) {{
            const nI = document.getElementById(`in-n-${{u}}`);
            const pI = document.getElementById(`in-p-${{u}}`);
            const btn = document.getElementById(`btn-${{u}}`);
            if(!nI.value || !pI.value) return alert("Jaza Jina na Simu!");
            btn.disabled = true; btn.innerText = "Inatuma...";
            const {{ error }} = await _s.from('orodha_majina').insert([{{ mhusika: u, jina_la_mtu: nI.value.trim(), namba_ya_simu: pI.value.trim() }}]);
            if(!error) {{ nI.value = ''; pI.value = ''; await ui(); }} else {{ alert("Error!"); }}
            btn.disabled = false; btn.innerText = "HIFADHI";
        }}

        timer(); ui();
        setInterval(ui, 10000);
    </script>
</body>
</html>
"""

components.html(html_code, height=1600, scrolling=True)