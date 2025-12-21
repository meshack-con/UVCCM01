import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 1. Konfigureshon ya Ukurasa (Browser Tab)
st.set_page_config(
    page_title="Master Admin System", 
    page_icon="meshack.png", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Kazi ya kubadilisha picha kuwa Base64 ili iweze kusomeka kila mahali
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

img_raw = get_base64_image("meshack.png")
img_data = f"data:image/png;base64,{img_raw}" if img_raw else "https://via.placeholder.com/150"

# 3. PWA INJECTION - Hii inalazimisha Icon na Jina lako lionekane kwenye simu
# Inakaa nje ya iframe ili iwe na nguvu zaidi (Root Level)
manifest_json = f"""
{{
  "name": "Master Admin System",
  "short_name": "MasterAdmin",
  "start_url": ".",
  "display": "standalone",
  "background_color": "#061a06",
  "theme_color": "#15803d",
  "icons": [
    {{ "src": "{img_data}", "sizes": "192x192", "type": "image/png" }},
    {{ "src": "{img_data}", "sizes": "512x512", "type": "image/png" }}
  ]
}}
"""
manifest_b64 = base64.b64encode(manifest_json.encode()).decode()

st.markdown(f"""
    <head>
        <link rel="manifest" href="data:application/manifest+json;base64,{manifest_b64}">
        <link rel="apple-touch-icon" href="{img_data}">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-title" content="Master Admin">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="theme-color" content="#15803d">
    </head>
    <style>
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        .block-container {{padding: 0px !important;}}
        iframe {{border: none !important;}}
    </style>
""", unsafe_allow_html=True)

# 4. FULL CODE YA SYSTEM (HTML/JS/CSS)
full_custom_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Master Admin | Full System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f0f4f0; color: #1a2e1a; overflow-x: hidden; margin: 0; padding: 0; }}
        [x-cloak] {{ display: none !important; }}
        .glass {{ background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); }}
        .stat-card {{ transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1); border-left: 4px solid #eab308; }}
        .gradient-green {{ background: linear-gradient(135deg, #15803d 0%, #166534 100%); }}
        
        .spinner-container {{ position: relative; width: 106px; height: 106px; display: flex; align-items: center; justify-content: center; }}
        .loader-ring {{
            position: absolute; width: 100%; height: 100%; border: 3px solid transparent;
            border-top-color: #eab308; border-right-color: #eab308; border-radius: 50%;
            animation: spin 0.8s cubic-bezier(0.4, 0, 0.2, 1) infinite;
        }}
        @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}

        .custom-scrollbar::-webkit-scrollbar {{ height: 4px; width: 4px; }}
        .custom-scrollbar::-webkit-scrollbar-thumb {{ background: #15803d; border-radius: 10px; }}
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
    </style>
</head>
<body x-data="adminApp()" x-init="init()" x-cloak class="antialiased">

    <template x-if="!session">
        <div class="flex items-start justify-center min-h-screen bg-[#061a06] px-4 pt-12 md:pt-20 relative overflow-hidden">
            <div class="absolute w-64 h-64 md:w-96 md:h-96 bg-green-600/20 rounded-full blur-[80px] -top-20 -left-20"></div>
            <div class="absolute w-64 h-64 md:w-96 md:h-96 bg-yellow-500/10 rounded-full blur-[80px] -bottom-20 -right-20"></div>
            
            <div class="max-w-md w-full glass p-8 md:p-10 rounded-[2.5rem] shadow-2xl text-center z-10 border border-green-900/10">
                <div class="flex justify-center mb-6">
                    <div class="spinner-container">
                        <div x-show="isLoading" class="loader-ring"></div>
                        <img src="{img_data}" alt="Logo" :class="isLoading ? 'scale-90' : 'scale-100'"
                            class="w-24 h-24 rounded-full object-cover border-2 border-yellow-400/30 shadow-inner transition-all duration-300 z-10">
                    </div>
                </div>
                
                <h2 class="text-2xl md:text-3xl font-extrabold text-green-900 mb-1">Main Admin</h2>
                <p class="text-[10px] md:text-[11px] font-black text-green-700 uppercase tracking-tighter mb-8 leading-tight">
                    VYUO NA VYUO VIKUU MANAGEMENT SYSTEM
                </p>
                
                <div class="space-y-4 text-left">
                    <div>
                        <label class="text-[10px] font-black text-green-800 uppercase ml-2 mb-1 block">Username</label>
                        <input type="text" x-model="loginData.user" placeholder="Ingiza Username" 
                            class="w-full p-4 bg-green-50/50 border border-green-100 rounded-2xl outline-none focus:ring-2 focus:ring-green-500/20 transition-all font-semibold">
                    </div>
                    
                    <div class="relative">
                        <label class="text-[10px] font-black text-green-800 uppercase ml-2 mb-1 block">Password</label>
                        <input :type="showPass ? 'text' : 'password'" x-model="loginData.pass" placeholder="Ingiza Password" 
                            class="w-full p-4 bg-green-50/50 border border-green-100 rounded-2xl outline-none focus:ring-2 focus:ring-green-500/20 transition-all font-semibold">
                        <button @click="showPass = !showPass" class="absolute right-4 top-[38px] text-green-700 hover:text-yellow-600">
                            <template x-if="!showPass"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"></path><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"></path></svg></template>
                            <template x-if="showPass"><svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18"></path></svg></template>
                        </button>
                    </div>
                    
                    <button @click="login" :disabled="isLoading" 
                        class="w-full gradient-green text-yellow-400 py-4 rounded-2xl font-bold shadow-lg transition-all tracking-widest uppercase mt-4 disabled:opacity-50">
                        <span x-show="!isLoading">LOGIN TO SYSTEM</span>
                        <span x-show="isLoading">VERIFYING...</span>
                    </button>
                </div>
            </div>
        </div>
    </template>

    <template x-if="session">
        <div class="min-h-screen flex flex-col">
            <nav class="glass border-b border-green-100 h-20 px-4 md:px-12 flex justify-between items-center sticky top-0 z-50 shadow-sm">
                <div class="flex items-center space-x-3 md:space-x-4">
                    <img src="{img_data}" alt="Logo" class="w-10 h-10 rounded-full border-2 border-yellow-400">
                    <div>
                        <span class="font-black text-sm md:text-lg block leading-none text-green-900 uppercase">Master Admin</span>
                        <span class="hidden md:block text-[9px] font-bold text-yellow-600 uppercase tracking-widest">Management Dashboard</span>
                    </div>
                </div>
                <button @click="logout" class="bg-red-50 hover:bg-red-100 px-4 py-2 rounded-xl text-red-700 font-bold text-[10px] uppercase transition-all">Logout</button>
            </nav>

            <main class="max-w-7xl mx-auto w-full px-4 md:px-6 py-8">
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-10">
                    <div class="bg-white p-7 rounded-[2rem] border border-green-50 shadow-sm stat-card">
                        <p class="text-green-600/50 text-[10px] font-extrabold uppercase mb-3">Total Colleges</p>
                        <h3 class="text-4xl font-black text-green-900" x-text="allVyuo.length">0</h3>
                    </div>
                    <div class="bg-white p-7 rounded-[2rem] border border-green-50 shadow-sm stat-card !border-l-green-600">
                        <p class="text-green-600/50 text-[10px] font-extrabold uppercase mb-3">UVCCM Branches</p>
                        <h3 class="text-4xl font-black text-green-700" x-text="allVyuo.filter(v => v.ina_uvccm).length">0</h3>
                    </div>
                    <div class="bg-white p-7 rounded-[2rem] border border-green-50 shadow-sm stat-card">
                        <p class="text-green-600/50 text-[10px] font-extrabold uppercase mb-3">Senate Leaders</p>
                        <h3 class="text-4xl font-black text-green-800" x-text="allBaraza.length">0</h3>
                    </div>
                    <div class="bg-white p-7 rounded-[2rem] border border-green-50 shadow-sm stat-card !border-l-green-900">
                        <p class="text-green-600/50 text-[10px] font-extrabold uppercase mb-3">Branch Leaders</p>
                        <h3 class="text-4xl font-black text-slate-900" x-text="allMatawi.length">0</h3>
                    </div>
                </div>

                <div class="bg-green-900 p-1 rounded-[2.5rem] md:rounded-[3rem] shadow-2xl mb-10">
                    <div class="bg-green-800 rounded-[2.3rem] md:rounded-[2.8rem] p-6 md:p-8">
                        <div class="flex flex-col md:flex-row items-center gap-6 md:gap-8">
                            <div class="flex-1 w-full text-left">
                                <label class="text-[10px] font-black text-yellow-400 uppercase mb-3 block">Chujio la Mkoa</label>
                                <select x-model="selectedRegion" @change="applyFilter" 
                                    class="w-full bg-green-950 text-white p-5 rounded-2xl border border-green-700 outline-none focus:ring-2 focus:ring-yellow-400/50 text-lg font-bold appearance-none">
                                    <option value="ALL">Mikoa Yote (National)</option>
                                    <template x-for="m in uniqueMikoa" :key="m"><option :value="m" x-text="m"></option></template>
                                </select>
                            </div>
                            <div class="w-full md:w-auto text-center px-10 md:border-l border-green-700">
                                <p class="text-green-400 text-[10px] font-black uppercase mb-1">Eneo la Ripoti</p>
                                <p class="text-yellow-400 font-black text-2xl md:text-3xl uppercase" x-text="selectedRegion === 'ALL' ? 'National' : selectedRegion"></p>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="bg-white rounded-[2rem] md:rounded-[2.5rem] border border-green-100 shadow-xl overflow-hidden">
                    <div class="p-4 md:p-8 border-b border-green-50 flex flex-col md:flex-row justify-between items-center gap-6 bg-green-50/30">
                        <div class="flex p-1.5 bg-green-100/50 rounded-2xl overflow-x-auto w-full md:w-auto no-scrollbar custom-scrollbar">
                            <button @click="tab = 'vyuo'" :class="tab === 'vyuo' ? 'bg-green-700 text-yellow-400 shadow-md' : 'text-green-800'" class="px-6 py-3 rounded-xl text-xs font-black uppercase transition-all whitespace-nowrap">Vyuo</button>
                            <button @click="tab = 'baraza'" :class="tab === 'baraza' ? 'bg-green-700 text-yellow-400 shadow-md' : 'text-green-800'" class="px-6 py-3 rounded-xl text-xs font-black uppercase transition-all whitespace-nowrap">Wajumbe Baraza</button>
                            <button @click="tab = 'matawi'" :class="tab === 'matawi' ? 'bg-green-700 text-yellow-400 shadow-md' : 'text-green-800'" class="px-6 py-3 rounded-xl text-xs font-black uppercase transition-all whitespace-nowrap">Viongozi Matawi</button>
                        </div>
                        <button @click="exportCSV" class="w-full md:w-auto gradient-green text-yellow-400 px-8 py-3.5 rounded-2xl text-[11px] font-black uppercase tracking-widest">Download CSV</button>
                    </div>

                    <div class="overflow-x-auto custom-scrollbar">
                        <template x-if="tab === 'vyuo'">
                            <table class="w-full text-left min-w-[600px]">
                                <thead class="bg-green-50 text-[10px] font-black text-green-800/40 uppercase tracking-widest border-b">
                                    <tr><th class="p-6">Mkoa</th><th class="p-6">Jina la Chuo</th><th class="p-6">Hali ya UVCCM</th></tr>
                                </thead>
                                <tbody class="divide-y divide-green-50">
                                    <template x-for="v in filteredVyuo" :key="v.id">
                                        <tr class="hover:bg-yellow-50/50 transition-colors">
                                            <td class="p-6 font-bold text-green-700" x-text="v.mkoa"></td>
                                            <td class="p-6 font-black text-green-900" x-text="v.jina_la_chuo"></td>
                                            <td class="p-6"><span :class="v.ina_uvccm ? 'bg-green-100 text-green-700 border-green-200' : 'bg-yellow-50 text-yellow-700 border-yellow-200'" class="px-3 py-1.5 rounded-full text-[9px] font-black border" x-text="v.ina_uvccm ? 'IPO' : 'HAIPO'"></span></td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </template>

                        <template x-if="tab === 'baraza'">
                            <table class="w-full text-left min-w-[800px]">
                                <thead class="bg-green-50 text-[10px] font-black text-green-800/40 uppercase tracking-widest border-b">
                                    <tr><th class="p-6">Kiongozi</th><th class="p-6">Nafasi & Course</th><th class="p-6">Chuo & Mwaka</th><th class="p-6">Mkoa</th></tr>
                                </thead>
                                <tbody class="divide-y divide-green-50">
                                    <template x-for="b in filteredBaraza" :key="b.id">
                                        <tr class="hover:bg-yellow-50/50 transition-colors">
                                            <td class="p-6"><div class="font-black text-green-900" x-text="b.jina_kamili"></div><div class="text-[10px] text-green-600 font-bold" x-text="b.namba_ya_simu"></div></td>
                                            <td class="p-6"><div class="font-bold text-green-800 text-xs uppercase" x-text="b.nafasi_ya_uongozi"></div><div class="text-[10px] text-green-600/60 font-semibold" x-text="b.degree_programme"></div></td>
                                            <td class="p-6"><div class="font-black text-green-700 text-sm" x-text="b.vyuo?.jina_la_chuo"></div><div class="text-[10px] font-bold text-yellow-600 uppercase" x-text="b.mwaka_wa_masomo"></div></td>
                                            <td class="p-6 font-black text-green-400 text-[10px]" x-text="b.vyuo?.mkoa"></td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </template>

                        <template x-if="tab === 'matawi'">
                            <table class="w-full text-left min-w-[800px]">
                                <thead class="bg-green-50 text-[10px] font-black text-green-800/40 uppercase tracking-widest border-b">
                                    <tr><th class="p-6">Kiongozi Tawi</th><th class="p-6">Nafasi & Course</th><th class="p-6">Chuo & Mwaka</th><th class="p-6">Mlezi (Patron)</th></tr>
                                </thead>
                                <tbody class="divide-y divide-green-50">
                                    <template x-for="m in filteredMatawi" :key="m.id">
                                        <tr class="hover:bg-yellow-50/50 transition-colors">
                                            <td class="p-6"><div class="font-black text-green-900" x-text="m.jina_la_kiongozi"></div><div class="text-[10px] text-green-600 font-bold" x-text="m.phone_number"></div></td>
                                            <td class="p-6"><div class="font-bold text-green-800 text-xs uppercase" x-text="m.nafasi_ya_uongozi"></div><div class="text-[10px] text-green-600/60 font-semibold" x-text="m.course_name"></div></td>
                                            <td class="p-6"><div class="font-black text-green-700 text-sm" x-text="m.vyuo?.jina_la_chuo"></div><div class="text-[10px] font-bold text-green-400" x-text="m.mwaka_wa_masomo"></div></td>
                                            <td class="p-6 text-xs text-green-800 font-bold italic" x-text="m.jina_la_mlezi"></td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </template>
                    </div>
                </div>
            </main>
        </div>
    </template>

    <script>
        const {{ createClient }} = supabase;
        const client = createClient('https://xickklzlmwaobzobwyws.supabase.co', 'sb_publishable_94BpD9gpOpYyWryIhzBjog_kxQRAG4W');

        function adminApp() {{
            return {{
                session: JSON.parse(localStorage.getItem('admin_session')) || null,
                isLoading: false, tab: 'vyuo', showPass: false,
                loginData: {{ user: '', pass: '' }},
                selectedRegion: 'ALL',
                uniqueMikoa: [], allVyuo: [], allBaraza: [], allMatawi: [],
                filteredVyuo: [], filteredBaraza: [], filteredMatawi: [],

                async init() {{ if(this.session) await this.loadAll(); }},

                async login() {{
                    if(!this.loginData.user || !this.loginData.pass) return alert("Jaza Username na Password!");
                    this.isLoading = true;
                    try {{
                        const {{ data }} = await client.from('watumiaji').select('*').eq('username', this.loginData.user).eq('password', this.loginData.pass).single();
                        if(data) {{ 
                            this.session = data; localStorage.setItem('admin_session', JSON.stringify(data)); 
                            await this.loadAll(); 
                        }} else {{ alert("Mtumiaji hajapatikana!"); }}
                    }} catch (e) {{ alert("Hitilafu ya mtandao!"); }} finally {{ this.isLoading = false; }}
                }},

                logout() {{ localStorage.removeItem('admin_session'); location.reload(); }},

                async loadAll() {{
                    const [resV, resB, resM] = await Promise.all([
                        client.from('vyuo').select('*').order('mkoa'),
                        client.from('viongozi').select('*, vyuo(*)'),
                        client.from('matawi_viongozi').select('*, vyuo(*)')
                    ]);
                    this.allVyuo = resV.data || [];
                    this.uniqueMikoa = [...new Set(this.allVyuo.map(v => v.mkoa).filter(m => m))];
                    this.allBaraza = resB.data || [];
                    this.allMatawi = resM.data || [];
                    this.applyFilter();
                }},

                applyFilter() {{
                    const filterByRegion = (list, key) => this.selectedRegion === 'ALL' ? list : list.filter(item => (key === 'mkoa' ? item.mkoa : item.vyuo?.mkoa) === this.selectedRegion);
                    this.filteredVyuo = filterByRegion(this.allVyuo, 'mkoa');
                    this.filteredBaraza = filterByRegion(this.allBaraza, 'vyuo_mkoa');
                    this.filteredMatawi = filterByRegion(this.allMatawi, 'vyuo_mkoa');
                }},

                exportCSV() {{
                    let header = "Mkoa,Chuo,Hali\\n";
                    let rows = this.filteredVyuo.map(i => `"${{i.mkoa}}","${{i.jina_la_chuo}}","${{i.ina_uvccm}}"`);
                    const blob = new Blob([header + rows.join("\\n")], {{ type: 'text/csv' }});
                    const url = URL.createObjectURL(blob);
                    const a = document.createElement('a'); a.href = url; a.download = 'ripoti.csv'; a.click();
                }}
            }}
        }}
    </script>
</body>
</html>
"""

# 5. KU-RENDER KWENYE STREAMLIT
components.html(full_custom_code, height=1500, scrolling=True)
