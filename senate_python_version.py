import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 1. Configuration ya Ukurasa
st.set_page_config(page_title="Senate Management Portal", layout="wide", initial_sidebar_state="collapsed")

# 2. Picha ya Base64 (User Avatar)
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    return "https://via.placeholder.com/150"

img_data = get_base64_image("meshack.png")

# 3. Ficha Alama za Streamlit
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0px !important;}
    iframe {border: none !important;}
    </style>
    """, unsafe_allow_html=True)

# 4. Full HTML/JS/CSS Code
full_custom_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Senate Management System | Modern</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f0f4f8; color: #1e293b; margin:0; padding:0; }}
        [x-cloak] {{ display: none !important; }}
        .glass-card {{ background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(12px); border: 1px solid rgba(255,255,255,0.5); }}
        .gradient-dark {{ background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%); }}
        .input-focus {{ transition: all 0.3s ease; border: 2px solid #e2e8f0; }}
        .input-focus:focus {{ border-color: #059669; background: white; box-shadow: 0 0 0 4px rgba(5, 150, 105, 0.1); }}
        
        .loader-ring {{
            position: absolute; width: 100%; height: 100%; border: 3px solid transparent;
            border-top-color: #10b981; border-right-color: #10b981; border-radius: 50%;
            animation: spin 0.8s linear infinite; top: 0; left: 0;
        }}
        @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body x-data="app()" x-init="init()" x-cloak>

    <template x-if="!session">
        <div class="flex items-start justify-center min-h-screen bg-[#0f172a] px-4 pt-12 md:pt-20 relative overflow-hidden">
            <div class="absolute w-96 h-96 bg-emerald-600/20 rounded-full blur-[100px] -top-20 -left-20"></div>
            
            <div class="max-w-md w-full glass-card p-10 rounded-[2.5rem] shadow-2xl text-center relative z-10">
                <div class="relative w-24 h-24 mx-auto mb-6">
                    <div x-show="loading" class="loader-ring"></div>
                    <img src="{img_data}" class="w-24 h-24 rounded-full object-cover border-4 border-white shadow-lg">
                </div>
                <h2 class="text-2xl font-black text-slate-800 mb-1 uppercase tracking-tighter">Senate Portal</h2>
                <p class="text-[10px] font-bold text-emerald-600 uppercase tracking-widest mb-8">Private Dashboard Access</p>
                
                <div class="space-y-4 text-left">
                    <div>
                        <label class="text-[10px] font-black uppercase text-slate-500 ml-2 mb-1 block">Username</label>
                        <input type="text" x-model="loginData.user" class="w-full p-4 bg-slate-100/50 rounded-2xl outline-none input-focus font-semibold" placeholder="Username">
                    </div>
                    <div class="relative">
                        <label class="text-[10px] font-black uppercase text-slate-500 ml-2 mb-1 block">Password</label>
                        <input :type="showPass ? 'text' : 'password'" x-model="loginData.pass" class="w-full p-4 bg-slate-100/50 rounded-2xl outline-none input-focus font-semibold pr-12" placeholder="••••••••">
                        <button @click="showPass = !showPass" class="absolute right-4 top-[38px] text-slate-400 hover:text-emerald-600">
                             <svg x-show="!showPass" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M2.036 12.322a1.012 1.012 0 010-.644C3.399 8.049 7.21 5 12 5c4.79 0 8.601 3.049 9.964 6.678a1.012 1.012 0 010 .644C20.601 15.951 16.79 19 12 19c-4.79 0-8.601-3.049-9.964-6.678z"/></svg>
                             <svg x-show="showPass" class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l18 18"/></svg>
                        </button>
                    </div>
                    <button @click="login" :disabled="loading" class="w-full bg-emerald-600 text-white py-4 rounded-2xl font-black shadow-lg hover:bg-emerald-700 transition-all uppercase tracking-widest mt-4">
                        <span x-text="loading ? 'AUTHENTICATING...' : 'SIGN IN'"></span>
                    </button>
                </div>
            </div>
        </div>
    </template>

    <template x-if="session">
        <div class="min-h-screen pb-20">
            <nav class="glass-card sticky top-0 z-50 px-6 h-20 flex justify-between items-center shadow-sm border-b">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 bg-emerald-600 rounded-xl flex items-center justify-center text-white font-black shadow-lg">S</div>
                    <span class="font-black text-lg tracking-tighter text-slate-800">SENATE SYSTEM</span>
                </div>
                <div class="flex items-center space-x-6">
                    <div class="hidden md:flex items-center bg-slate-100 p-1 rounded-xl">
                        <button @click="tab = 'colleges'" :class="tab === 'colleges' ? 'bg-white shadow-sm text-emerald-600' : 'text-slate-500'" class="px-6 py-2 rounded-lg font-bold text-xs transition-all">Colleges</button>
                        <button @click="tab = 'leaders'" :class="tab === 'leaders' ? 'bg-white shadow-sm text-emerald-600' : 'text-slate-500'" class="px-6 py-2 rounded-lg font-bold text-xs transition-all">Leaders</button>
                    </div>
                    <button @click="logout" class="bg-red-50 text-red-500 font-black text-[10px] px-4 py-2 rounded-xl hover:bg-red-100 uppercase tracking-widest">Logout</button>
                </div>
            </nav>

            <div class="max-w-7xl mx-auto px-6 mt-10">
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-6 mb-10">
                    <div class="bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100">
                        <p class="text-slate-400 text-[9px] font-black uppercase tracking-[0.2em] mb-1">Total Colleges</p>
                        <h3 class="text-3xl font-black text-slate-800" x-text="vyuo.length">0</h3>
                    </div>
                    <div class="bg-emerald-600 p-6 rounded-[2rem] shadow-xl shadow-emerald-900/10">
                        <p class="text-emerald-100 text-[9px] font-black uppercase tracking-[0.2em] mb-1">UVCCM Branches</p>
                        <h3 class="text-3xl font-black text-white" x-text="vyuo.filter(v => v.ina_uvccm).length">0</h3>
                    </div>
                    <div class="bg-white p-6 rounded-[2rem] shadow-sm border border-slate-100">
                        <p class="text-slate-400 text-[9px] font-black uppercase tracking-[0.2em] mb-1">Active Leaders</p>
                        <h3 class="text-3xl font-black text-blue-600" x-text="viongozi.length">0</h3>
                    </div>
                </div>

                <div x-show="tab === 'colleges'" class="grid lg:grid-cols-12 gap-8" x-transition>
                    <div class="lg:col-span-4">
                        <div class="bg-white p-8 rounded-[2.5rem] shadow-xl shadow-slate-200/50 border border-slate-100">
                            <h3 class="text-xl font-black mb-6 text-slate-800">Sajili Chuo</h3>
                            <div class="space-y-4">
                                <input type="text" x-model="formChuo.mkoa" placeholder="Mkoa (Region)" class="w-full p-4 bg-slate-50 rounded-2xl outline-none input-focus font-semibold">
                                <input type="text" x-model="formChuo.jina" placeholder="Jina la Chuo" class="w-full p-4 bg-slate-50 rounded-2xl outline-none input-focus font-semibold">
                                <select x-model="formChuo.aina" class="w-full p-4 bg-slate-50 rounded-2xl outline-none input-focus font-bold text-sm">
                                    <option>Chuo Kikuu</option><option>Chuo cha Kati</option>
                                </select>
                                <label class="flex items-center space-x-3 p-4 bg-emerald-50/50 rounded-2xl cursor-pointer">
                                    <input type="checkbox" x-model="formChuo.uvccm" class="w-5 h-5 accent-emerald-600">
                                    <span class="text-sm font-bold text-emerald-800">Ina Tawi la UVCCM?</span>
                                </label>
                                <button @click="saveChuo" class="w-full bg-slate-900 text-white py-4 rounded-2xl font-black hover:bg-black transition-all shadow-lg tracking-widest uppercase">Save College</button>
                            </div>
                        </div>
                    </div>
                    <div class="lg:col-span-8">
                        <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-100 overflow-hidden">
                            <table class="w-full text-left">
                                <thead class="bg-slate-50 text-[10px] uppercase font-black text-slate-400">
                                    <tr><th class="p-6">Maelezo ya Chuo</th><th class="p-6">Aina</th><th class="p-6">UVCCM</th><th class="p-6"></th></tr>
                                </thead>
                                <tbody class="divide-y divide-slate-50">
                                    <template x-for="v in vyuo" :key="v.id">
                                        <tr class="hover:bg-slate-50/50">
                                            <td class="p-6">
                                                <div class="font-black text-slate-800" x-text="v.jina_la_chuo"></div>
                                                <div class="text-[10px] text-emerald-600 font-bold uppercase" x-text="v.mkoa"></div>
                                            </td>
                                            <td class="p-6 text-[10px] font-bold text-slate-500 uppercase" x-text="v.aina_ya_chuo"></td>
                                            <td class="p-6">
                                                <span :class="v.ina_uvccm ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-600'" class="px-3 py-1 rounded-full text-[9px] font-black" x-text="v.ina_uvccm ? 'YES' : 'NO'"></span>
                                            </td>
                                            <td class="p-6 text-right">
                                                <button @click="deleteChuo(v.id)" class="text-red-300 hover:text-red-500"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg></button>
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
                        <div class="bg-white p-8 rounded-[2.5rem] shadow-xl border border-slate-100">
                            <h3 class="text-xl font-black mb-6 text-slate-800">Sajili Kiongozi</h3>
                            <div class="space-y-4">
                                <input type="text" x-model="formKiongozi.jina" placeholder="Jina Kamili" class="w-full p-4 bg-slate-50 rounded-2xl outline-none input-focus font-semibold">
                                <input type="text" x-model="formKiongozi.nafasi" placeholder="Nafasi ya Uongozi" class="w-full p-4 bg-slate-50 rounded-2xl outline-none input-focus font-semibold">
                                <input type="text" x-model="formKiongozi.degree" placeholder="Kozi / Programme" class="w-full p-4 bg-slate-50 rounded-2xl outline-none input-focus font-semibold">
                                <input type="tel" x-model="formKiongozi.phone" placeholder="Namba ya Simu" class="w-full p-4 bg-slate-50 rounded-2xl outline-none input-focus font-semibold">
                                <select x-model="formKiongozi.chuo_id" class="w-full p-4 bg-slate-50 rounded-2xl outline-none input-focus font-bold text-sm">
                                    <option value="">-- Chagua Chuo --</option>
                                    <template x-for="v in vyuo" :key="v.id"><option :value="v.id" x-text="v.jina_la_chuo"></option></template>
                                </select>
                                <button @click="saveKiongozi" class="w-full bg-emerald-600 text-white py-4 rounded-2xl font-black hover:bg-emerald-700 shadow-lg tracking-widest uppercase">Submit Leader</button>
                            </div>
                        </div>
                    </div>
                    <div class="lg:col-span-8">
                        <div class="bg-white rounded-[2.5rem] shadow-sm border border-slate-100 overflow-hidden">
                            <table class="w-full text-left">
                                <thead class="bg-slate-50 text-[10px] uppercase font-black text-slate-400">
                                    <tr><th class="p-6">Kiongozi</th><th class="p-6">Nafasi & Chuo</th><th class="p-6"></th></tr>
                                </thead>
                                <tbody class="divide-y divide-slate-50">
                                    <template x-for="k in viongozi" :key="k.id">
                                        <tr class="hover:bg-slate-50/50">
                                            <td class="p-6">
                                                <div class="font-black text-slate-800" x-text="k.jina_kamili"></div>
                                                <div class="text-[10px] text-slate-400 font-bold uppercase" x-text="k.degree_programme"></div>
                                                <div class="text-[10px] text-emerald-600 font-bold" x-text="k.phone_number"></div>
                                            </td>
                                            <td class="p-6">
                                                <span class="bg-slate-100 text-slate-600 px-3 py-1 rounded-full text-[9px] font-black uppercase" x-text="k.nafasi_ya_uongozi"></span>
                                                <div class="text-[10px] text-slate-400 mt-1 italic font-bold" x-text="k.vyuo?.jina_la_chuo"></div>
                                            </td>
                                            <td class="p-6 text-right">
                                                <button @click="deleteKiongozi(k.id)" class="text-red-300 hover:text-red-500"><svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg></button>
                                            </td>
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

        function app() {{
            return {{
                session: JSON.parse(localStorage.getItem('sen_session')) || null,
                tab: 'colleges', loading: false, showPass: false,
                loginData: {{ user: '', pass: '' }},
                vyuo: [], viongozi: [],
                formChuo: {{ id: null, jina: '', mkoa: '', aina: 'Chuo Kikuu', uvccm: false }},
                formKiongozi: {{ id: null, jina: '', nafasi: '', degree: '', phone: '', mwaka: 'Year 1', chuo_id: '' }},

                async init() {{ if (this.session) await this.fetchData(); }},

                async login() {{
                    this.loading = true;
                    try {{
                        const {{ data }} = await client.from('watumiaji').select('*').eq('username', this.loginData.user).eq('password', this.loginData.pass).single();
                        if (data) {{
                            this.session = data;
                            localStorage.setItem('sen_session', JSON.stringify(data));
                            await this.fetchData();
                        }} else {{ alert("Login Failed!"); }}
                    }} catch(e) {{ alert("Error connecting to database"); }}
                    finally {{ this.loading = false; }}
                }},

                logout() {{ localStorage.removeItem('sen_session'); this.session = null; }},

                async fetchData() {{
                    if (!this.session) return;
                    const resV = await client.from('vyuo').select('*').eq('created_by', this.session.id).order('jina_la_chuo');
                    this.vyuo = resV.data || [];
                    const resK = await client.from('viongozi').select('*, vyuo(jina_la_chuo)').eq('created_by', this.session.id).order('created_at', {{ascending: false}});
                    this.viongozi = resK.data || [];
                }},

                async saveChuo() {{
                    if(!this.formChuo.mkoa || !this.formChuo.jina) {{ alert("Jaza Mkoa na Jina la Chuo"); return; }}
                    await client.from('vyuo').insert([{{ 
                        jina_la_chuo: this.formChuo.jina, mkoa: this.formChuo.mkoa, aina_ya_chuo: this.formChuo.aina, 
                        ina_uvccm: this.formChuo.uvccm, created_by: this.session.id 
                    }}]);
                    this.formChuo = {{ id: null, jina: '', mkoa: '', aina: 'Chuo Kikuu', uvccm: false }};
                    await this.fetchData();
                }},

                async saveKiongozi() {{
                    if(!this.formKiongozi.chuo_id || !this.formKiongozi.jina) {{ alert("Chagua Chuo na uingize jina"); return; }}
                    await client.from('viongozi').insert([{{ 
                        jina_kamili: this.formKiongozi.jina, nafasi_ya_uongozi: this.formKiongozi.nafasi, 
                        degree_programme: this.formKiongozi.degree, phone_number: this.formKiongozi.phone,
                        mwaka_wa_masomo: this.formKiongozi.mwaka, chuo_id: this.formKiongozi.chuo_id, created_by: this.session.id 
                    }}]);
                    this.formKiongozi = {{ id: null, jina: '', nafasi: '', degree: '', phone: '', mwaka: 'Year 1', chuo_id: '' }};
                    await this.fetchData();
                }},

                async deleteChuo(id) {{ if(confirm("Futa chuo hiki?")) {{ await client.from('vyuo').delete().eq('id', id); await this.fetchData(); }} }},
                async deleteKiongozi(id) {{ if(confirm("Ondoa kiongozi huyu?")) {{ await client.from('viongozi').delete().eq('id', id); await this.fetchData(); }} }}
            }}
        }}
    </script>
</body>
</html>
"""

# Render
components.html(full_custom_code, height=1200, scrolling=True)