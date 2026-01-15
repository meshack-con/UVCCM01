import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 1. Konfigureshon ya Ukurasa
st.set_page_config(
    page_title="Senate Management Portal", 
    page_icon="meshack.png", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Picha kuwa Base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    return "https://via.placeholder.com/150"

img_data = get_base64_image("meshack.png")

# 3. Streamlit CSS Fixes
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0px !important;}
    iframe {border: none !important;}
    </style>
    """, unsafe_allow_html=True)

# 4. FULL HTML/JS CODE
full_custom_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background: #ffffff; color: #1e293b; margin:0; }}
        [x-cloak] {{ display: none !important; }}
        
        .bg-gradient-main {{ background: linear-gradient(135deg, #10b981 0%, #facc15 100%); }}
        .glass-card {{ background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(16,185,129,0.1); }}
        .input-modern:focus {{ border-color: #facc15; box-shadow: 0 0 0 4px rgba(250, 204, 21, 0.1); outline: none; }}
        
        .loader {{ border-top-color: transparent; animation: spin 0.8s linear infinite; }}
        @keyframes spin {{ to {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body x-data="senateApp()" x-init="init()" x-cloak class="bg-slate-50">

    <div x-show="isLoading" class="fixed inset-0 bg-white/80 z-[100] flex items-center justify-center" x-transition>
        <div class="flex flex-col items-center">
            <div class="w-10 h-10 border-4 border-emerald-500 loader rounded-full mb-2"></div>
            <p class="text-[10px] font-black text-emerald-600 uppercase tracking-widest">Inatuma Taarifa...</p>
        </div>
    </div>

    <template x-if="!session">
        <div class="flex justify-center min-h-screen bg-gradient-main px-4 pt-12 items-start">
            <div class="max-w-md w-full glass-card p-10 rounded-[3rem] shadow-2xl text-center mt-8">
                <img src="{img_data}" class="w-24 h-24 rounded-full mx-auto mb-6 object-cover border-4 border-white shadow-lg">
                <h2 class="text-3xl font-black text-slate-800 mb-2 tracking-tighter uppercase">Senate Portal</h2>
                <p class="text-emerald-700 text-xs font-bold mb-8 uppercase tracking-widest italic">Mfumo wa Usimamizi</p>
                
                <div class="space-y-4 text-left">
                    <input type="text" x-model="loginData.user" class="w-full p-4 bg-white border border-slate-100 rounded-2xl font-bold input-modern" placeholder="Username">
                    <input type="password" x-model="loginData.pass" class="w-full p-4 bg-white border border-slate-100 rounded-2xl font-bold input-modern" placeholder="Password">
                    <button @click="login" class="w-full bg-emerald-600 text-white py-5 rounded-2xl font-black shadow-lg hover:bg-emerald-700 transition-all uppercase tracking-widest mt-2">
                        INGIA KWENYE MFUMO
                    </button>
                </div>
            </div>
        </div>
    </template>

    <template x-if="session">
        <div class="min-h-screen">
            <nav class="bg-white border-b border-slate-100 sticky top-0 z-50 px-8 py-4 flex justify-between items-center shadow-sm">
                <div class="flex items-center gap-4">
                    <div class="bg-emerald-500 p-2 rounded-xl">
                        <img src="{img_data}" class="w-8 h-8 rounded-lg object-cover">
                    </div>
                    <div>
                        <span class="block font-black text-slate-800 uppercase text-sm leading-none" x-text="session.jina_kamili"></span>
                        <span class="text-[9px] font-bold text-emerald-600 uppercase tracking-widest">Senate Member</span>
                    </div>
                </div>

                <div class="flex bg-slate-100 p-1 rounded-2xl gap-1">
                    <button @click="tab = 'colleges'" :class="tab === 'colleges' ? 'bg-white text-emerald-600 shadow-sm' : 'text-slate-500'" class="px-6 py-2 rounded-xl font-black text-[10px] uppercase transition-all">Vyuo</button>
                    <button @click="tab = 'leaders'" :class="tab === 'leaders' ? 'bg-white text-emerald-600 shadow-sm' : 'text-slate-500'" class="px-6 py-2 rounded-xl font-black text-[10px] uppercase transition-all">Viongozi</button>
                </div>

                <button @click="logout" class="bg-yellow-400 text-slate-900 font-black text-[9px] px-5 py-2.5 rounded-xl uppercase hover:bg-yellow-500 transition-all shadow-md">Logout</button>
            </nav>

            <div class="max-w-7xl mx-auto px-6 py-10">
                <div x-show="tab === 'colleges'" class="grid lg:grid-cols-12 gap-8" x-transition>
                    <div class="lg:col-span-4">
                        <div class="bg-white p-8 rounded-[2.5rem] shadow-xl border border-emerald-50 border-t-8 border-t-emerald-500">
                            <h3 class="text-xl font-black mb-6 text-slate-800 uppercase flex items-center gap-2">
                                <span class="w-2 h-6 bg-yellow-400 rounded-full"></span> Sajili Chuo
                            </h3>
                            <div class="space-y-4">
                                <div>
                                    <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Aina ya Chuo</label>
                                    <select x-model="formChuo.aina_ya_chuo" class="w-full p-4 bg-slate-50 rounded-2xl border-none font-bold text-sm input-modern mt-1">
                                        <option value="">-- Chagua Aina --</option>
                                        <option value="Chuo Kikuu">Chuo Kikuu</option>
                                        <option value="Chuo cha Kati">Chuo cha Kati</option>
                                    </select>
                                </div>
                                <div>
                                    <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Mkoa</label>
                                    <select x-model="formChuo.mkoa" class="w-full p-4 bg-slate-50 rounded-2xl border-none font-bold text-sm input-modern mt-1">
                                        <option value="">-- Chagua Mkoa --</option>
                                        <template x-for="m in mikoa" :key="m"><option :value="m" x-text="m"></option></template>
                                    </select>
                                </div>
                                <div>
                                    <label class="text-[10px] font-black text-slate-400 uppercase ml-2">Jina la Chuo</label>
                                    <input type="text" x-model="formChuo.jina_la_chuo" placeholder="Mfano: UDSM" class="w-full p-4 bg-slate-50 rounded-2xl border-none font-bold text-sm input-modern mt-1">
                                </div>
                                <div @click="formChuo.ina_uvccm = !formChuo.ina_uvccm" class="flex items-center justify-between p-4 bg-slate-50 rounded-2xl cursor-pointer hover:bg-emerald-50 transition-colors border border-dashed border-slate-200">
                                    <span class="text-xs font-black text-slate-600 uppercase">UVCCM Ipo?</span>
                                    <div :class="formChuo.ina_uvccm ? 'bg-emerald-500' : 'bg-slate-300'" class="w-10 h-5 rounded-full relative transition-all">
                                        <div :class="formChuo.ina_uvccm ? 'translate-x-5' : 'translate-x-1'" class="w-3 h-3 bg-white rounded-full absolute top-1 transition-all"></div>
                                    </div>
                                </div>
                                <button @click="saveChuo" class="w-full bg-slate-900 text-white py-4 rounded-2xl font-black shadow-lg uppercase tracking-widest hover:bg-emerald-600 transition-all">Hifadhi Chuo</button>
                            </div>
                        </div>
                    </div>

                    <div class="lg:col-span-8">
                        <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-100 overflow-hidden">
                            <table class="w-full text-left">
                                <thead class="bg-slate-50 text-[10px] uppercase font-black text-slate-400">
                                    <tr><th class="p-6">Jina</th><th class="p-6">Aina</th><th class="p-6">Mkoa</th><th class="p-6">UVCCM</th></tr>
                                </thead>
                                <tbody>
                                    <template x-for="v in vyuo" :key="v.id">
                                        <tr class="border-b border-slate-50 hover:bg-yellow-50/20 transition-colors">
                                            <td class="p-6 font-black text-slate-800 text-sm" x-text="v.jina_la_chuo"></td>
                                            <td class="p-6 text-[10px] font-bold text-slate-500 uppercase" x-text="v.aina_ya_chuo"></td>
                                            <td class="p-6 font-black text-emerald-600 text-[10px] uppercase" x-text="v.mkoa"></td>
                                            <td class="p-6">
                                                <span :class="v.ina_uvccm ? 'bg-emerald-100 text-emerald-700' : 'bg-rose-50 text-rose-500'" 
                                                      class="px-3 py-1 rounded-lg text-[9px] font-black uppercase" 
                                                      x-text="v.ina_uvccm ? 'Ipo' : 'Haipo'"></span>
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <div x-show="tab === 'leaders'" class="grid lg:grid-cols-12 gap-8" x-transition>
                    <div class="lg:col-span-4">
                        <div class="bg-white p-8 rounded-[2.5rem] shadow-xl border border-yellow-50 border-t-8 border-t-yellow-400">
                            <h3 class="text-xl font-black mb-6 text-slate-800 uppercase flex items-center gap-2">
                                <span class="w-2 h-6 bg-emerald-500 rounded-full"></span> Sajili Kiongozi
                            </h3>
                            <div class="space-y-4">
                                <input type="text" x-model="formKiongozi.jina_kamili" placeholder="Jina Kamili" class="w-full p-4 bg-slate-50 rounded-2xl border-none font-bold text-sm input-modern">
                                <input type="text" x-model="formKiongozi.nafasi_ya_uongozi" placeholder="Nafasi" class="w-full p-4 bg-slate-50 rounded-2xl border-none font-bold text-sm input-modern">
                                <input type="text" x-model="formKiongozi.phone_number" placeholder="Simu (0xxxxxxxxx)" class="w-full p-4 bg-slate-50 rounded-2xl border-none font-bold text-sm input-modern">
                                <select x-model="formKiongozi.chuo_id" class="w-full p-4 bg-slate-50 rounded-2xl border-none font-bold text-sm input-modern">
                                    <option value="">-- Chagua Chuo --</option>
                                    <template x-for="v in vyuo" :key="v.id"><option :value="v.id" x-text="v.jina_la_chuo"></option></template>
                                </select>
                                <button @click="saveKiongozi" class="w-full bg-emerald-600 text-white py-4 rounded-2xl font-black shadow-lg uppercase tracking-widest hover:bg-slate-900 transition-all">Sajili Kiongozi</button>
                            </div>
                        </div>
                    </div>

                    <div class="lg:col-span-8">
                        <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-100 overflow-hidden">
                            <table class="w-full text-left">
                                <thead class="bg-slate-50 text-[10px] uppercase font-black text-slate-400">
                                    <tr><th class="p-6">Kiongozi</th><th class="p-6">Nafasi</th><th class="p-6">Taasisi</th></tr>
                                </thead>
                                <tbody>
                                    <template x-for="k in viongozi" :key="k.id">
                                        <tr class="hover:bg-emerald-50/30 transition-colors border-b border-slate-50">
                                            <td class="p-6">
                                                <div class="font-black text-slate-800 text-sm" x-text="k.jina_kamili"></div>
                                                <div class="text-[10px] text-emerald-600 font-bold" x-text="k.phone_number"></div>
                                            </td>
                                            <td class="p-6 text-[10px] font-black uppercase text-slate-500" x-text="k.nafasi_ya_uongozi"></td>
                                            <td class="p-6 text-[10px] text-slate-400 font-bold" x-text="k.vyuo?.jina_la_chuo"></td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </template>

    <script>
        const {{ createClient }} = supabase;
        const client = createClient('https://xickklzlmwaobzobwyws.supabase.co', 'sb_publishable_94BpD9gpOpYyWryIhzBjog_kxQRAG4W');

        function senateApp() {{
            return {{
                session: JSON.parse(localStorage.getItem('sen_session')) || null,
                tab: 'colleges', 
                isLoading: false,
                loginData: {{ user: '', pass: '' }},
                vyuo: [], viongozi: [],
                mikoa: ["Arusha", "Dar es Salaam", "Dodoma", "Geita", "Iringa", "Kagera", "Katavi", "Kigoma", "Kilimanjaro", "Lindi", "Manyara", "Mara", "Mbeya", "Mjini Magharibi", "Morogoro", "Mtwara", "Mwanza", "Njombe", "Pemba Kaskazini", "Pemba Kusini", "Pwani", "Rukwa", "Ruvuma", "Shinyanga", "Simiyu", "Singida", "Songwe", "Tabora", "Tanga", "Unguja Kaskazini", "Unguja Kusini"],
                formChuo: {{ jina_la_chuo: '', mkoa: '', aina_ya_chuo: '', ina_uvccm: false }},
                formKiongozi: {{ jina_kamili: '', nafasi_ya_uongozi: '', phone_number: '', chuo_id: '' }},

                async init() {{ 
                    if(this.session) await this.fetchData(); 
                }},

                async login() {{
                    if(!this.loginData.user || !this.loginData.pass) return alert("Jaza User na Password!");
                    this.isLoading = true;
                    try {{
                        const {{ data, error }} = await client.from('watumiaji').select('*').eq('username', this.loginData.user).eq('password', this.loginData.pass).single();
                        if (error) throw error;
                        this.session = data;
                        localStorage.setItem('sen_session', JSON.stringify(data));
                        await this.fetchData();
                    }} catch(e) {{
                        alert("Login Imefeli!");
                    }} finally {{
                        this.isLoading = false;
                    }}
                }},

                async fetchData() {{
                    this.isLoading = true;
                    try {{
                        const [resV, resK] = await Promise.all([
                            client.from('vyuo').select('*').order('jina_la_chuo'),
                            client.from('viongozi').select('*, vyuo(jina_la_chuo)').order('created_at', {{ascending: false}})
                        ]);
                        this.vyuo = resV.data || [];
                        this.viongozi = resK.data || [];
                    }} finally {{
                        this.isLoading = false;
                    }}
                }},

                async saveChuo() {{
                    if(!this.formChuo.aina_ya_chuo || !this.formChuo.jina_la_chuo) return alert("Jaza jina na aina ya chuo!");
                    this.isLoading = true;
                    const {{ error }} = await client.from('vyuo').insert([{{ ...this.formChuo }}]);
                    if(error) alert(error.message);
                    else {{
                        this.formChuo = {{ jina_la_chuo: '', mkoa: '', aina_ya_chuo: '', ina_uvccm: false }};
                        await this.fetchData();
                    }}
                    this.isLoading = false;
                }},

                async saveKiongozi() {{
                    if(!this.formKiongozi.chuo_id || !this.formKiongozi.jina_kamili) return alert("Jaza kila kitu!");
                    this.isLoading = true;
                    const {{ error }} = await client.from('viongozi').insert([{{ ...this.formKiongozi }}]);
                    if(error) alert(error.message);
                    else {{
                        this.formKiongozi = {{ jina_kamili: '', nafasi_ya_uongozi: '', phone_number: '', chuo_id: '' }};
                        await this.fetchData();
                    }}
                    this.isLoading = false;
                }},

                logout() {{ 
                    localStorage.removeItem('sen_session'); 
                    location.reload(); 
                }}
            }}
        }}
    </script>
</body>
</html>
"""

# 5. RENDERER
components.html(full_custom_code, height=1200, scrolling=True)
