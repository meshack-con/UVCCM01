import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# Configuration
st.set_page_config(page_title="Branch Leader Portal", layout="wide", initial_sidebar_state="collapsed")

# 1. Picha ya Base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return f"data:image/png;base64,{base64.b64encode(img_file.read()).decode()}"
    return "https://via.placeholder.com/150"

img_data = get_base64_image("meshack.png")

# 2. Ficha Streamlit UI
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {padding: 0px !important;}
    iframe {border: none !important;}
    </style>
    """, unsafe_allow_html=True)

# 3. Full HTML/JS/CSS
full_custom_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Branch Leader Portal | Modern</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8faf8; color: #1a2e1a; margin:0; padding:0; }}
        [x-cloak] {{ display: none !important; }}
        .glass {{ background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(0,0,0,0.05); }}
        .gradient-green {{ background: linear-gradient(135deg, #15803d 0%, #166534 100%); }}
        .input-focus {{ transition: all 0.3s ease; border: 2px solid #f1f5f1; }}
        .input-focus:focus {{ border-color: #15803d; background: white; box-shadow: 0 0 0 4px rgba(21, 128, 61, 0.1); }}
        
        .spinner-container {{ position: relative; width: 100px; height: 100px; display: flex; align-items: center; justify-content: center; }}
        .loader-ring {{
            position: absolute; width: 100%; height: 100%; border: 3px solid transparent;
            border-top-color: #eab308; border-right-color: #eab308; border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}
        @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
    </style>
</head>
<body x-data="branchApp()" x-init="init()" x-cloak>

    <template x-if="!session">
        <div class="flex items-start justify-center min-h-screen bg-[#061a06] px-4 pt-12 md:pt-20 relative overflow-hidden">
            <div class="absolute w-96 h-96 bg-green-600/20 rounded-full blur-[100px] -top-20 -left-20"></div>
            
            <div class="max-w-md w-full glass p-8 md:p-10 rounded-[2.5rem] shadow-2xl text-center z-10">
                <div class="flex justify-center mb-6">
                    <div class="spinner-container">
                        <div x-show="loading" class="loader-ring"></div>
                        <img src="{img_data}" class="w-20 h-20 rounded-full object-cover border-2 border-yellow-400 shadow-lg">
                    </div>
                </div>
                <h2 class="text-2xl font-black text-green-900 mb-1 uppercase tracking-tighter">Branch Portal</h2>
                <p class="text-[10px] font-bold text-green-600 uppercase tracking-widest mb-8">Ingia kusimamia viongozi wa tawi</p>
                
                <div class="space-y-4 text-left">
                    <div>
                        <label class="text-[10px] font-black uppercase text-green-800 ml-2 mb-1 block">Username</label>
                        <input type="text" x-model="loginData.user" placeholder="Username" 
                            class="w-full p-4 bg-green-50/50 rounded-2xl outline-none input-focus font-semibold">
                    </div>
                    
                    <div class="relative">
                        <label class="text-[10px] font-black uppercase text-green-800 ml-2 mb-1 block">Password</label>
                        <input :type="showPass ? 'text' : 'password'" x-model="loginData.pass" placeholder="Password" 
                            class="w-full p-4 bg-green-50/50 rounded-2xl outline-none input-focus font-semibold pr-12">
                        
                        <button @click="showPass = !showPass" type="button" class="absolute right-4 top-[38px] text-green-700 hover:text-green-900 focus:outline-none">
                            <template x-if="!showPass">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M2.036 12.322a1.012 1.012 0 010-.644C3.399 8.049 7.21 5 12 5c4.79 0 8.601 3.049 9.964 6.678a1.012 1.012 0 010 .644C20.601 15.951 16.79 19 12 19c-4.79 0-8.601-3.049-9.964-6.678z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                            </template>
                            <template x-if="showPass">
                                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-5 h-5">
                                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.98 8.223A10.477 10.477 0 001.934 12C3.226 16.338 7.244 19.5 12 19.5c.993 0 1.953-.138 2.863-.395M6.228 6.228A10.45 10.45 0 0112 4.5c4.756 0 8.773 3.162 10.065 7.498a10.523 10.523 0 01-4.293 5.774M6.228 6.228L3 3m3.228 3.228l3.65 3.65m7.894 7.894L21 21m-3.228-3.228l-3.65-3.65m0 0a3 3 0 10-4.243-4.243m4.242 4.242L9.88 9.88" />
                                </svg>
                            </template>
                        </button>
                    </div>
                    
                    <button @click="login" :disabled="loading" 
                        class="w-full gradient-green text-yellow-400 py-4 rounded-2xl font-black shadow-lg hover:opacity-90 transition-all tracking-widest uppercase mt-4">
                        <span x-text="loading ? 'AUTHENTICATING...' : 'SIGN IN'"></span>
                    </button>
                </div>
            </div>
        </div>
    </template>

    <template x-if="session">
        <div class="min-h-screen pb-20">
            <nav class="glass sticky top-0 z-50 px-6 h-20 flex justify-between items-center shadow-sm border-b border-green-100">
                <div class="flex items-center space-x-3">
                    <img src="{img_data}" class="w-10 h-10 rounded-full border-2 border-yellow-400">
                    <span class="font-black text-lg tracking-tighter text-green-900">BRANCH PORTAL</span>
                </div>
                <div class="flex items-center space-x-4">
                    <div class="hidden md:block text-right">
                        <p class="text-[9px] font-black text-green-600 uppercase leading-none">Logged in as</p>
                        <p class="text-xs font-bold text-slate-800" x-text="session.username"></p>
                    </div>
                    <button @click="logout" class="bg-red-50 text-red-600 font-black text-[10px] px-4 py-2 rounded-xl hover:bg-red-100 transition-all uppercase">Logout</button>
                </div>
            </nav>

            <div class="max-w-7xl mx-auto px-4 mt-10 grid lg:grid-cols-12 gap-8">
                
                <div class="lg:col-span-5">
                    <div class="bg-white p-8 rounded-[2.5rem] shadow-xl shadow-green-900/5 border border-green-50">
                        <h3 class="text-xl font-black mb-6 text-green-900 flex items-center">
                            <span class="w-8 h-8 bg-green-100 text-green-700 rounded-lg flex items-center justify-center mr-3 text-sm">01</span>
                            Sajili Kiongozi wa Tawi
                        </h3>
                        
                        <div class="space-y-4">
                            <div class="grid grid-cols-2 gap-4">
                                <div>
                                    <label class="text-[10px] font-black uppercase text-green-700 ml-1 mb-1 block">Mkoa</label>
                                    <select x-model="formData.mkoa" @change="fetchCollegesByRegion" class="w-full p-4 bg-green-50/30 rounded-2xl outline-none input-focus text-sm font-bold">
                                        <option value="">-- Chagua --</option>
                                        <template x-for="m in uniqueMikoa" :key="m"><option :value="m" x-text="m"></option></template>
                                    </select>
                                </div>
                                <div>
                                    <label class="text-[10px] font-black uppercase text-green-700 ml-1 mb-1 block">Chuo</label>
                                    <select x-model="formData.chuo_id" class="w-full p-4 bg-green-50/30 rounded-2xl outline-none input-focus text-sm font-bold">
                                        <option value="">-- Chagua --</option>
                                        <template x-for="c in filteredVyuo" :key="c.id"><option :value="c.id" x-text="c.jina_la_chuo"></option></template>
                                    </select>
                                </div>
                            </div>

                            <input type="text" x-model="formData.leaderName" placeholder="Jina Kamili la Kiongozi" class="w-full p-4 bg-green-50/30 rounded-2xl outline-none input-focus font-semibold">
                            
                            <div class="grid grid-cols-2 gap-4">
                                <input type="tel" x-model="formData.phone" placeholder="Namba ya Simu" class="p-4 bg-green-50/30 rounded-2xl outline-none input-focus font-semibold">
                                <input type="text" x-model="formData.course" placeholder="Kozi (mf: BAED)" class="p-4 bg-green-50/30 rounded-2xl outline-none input-focus font-semibold">
                            </div>

                            <div class="grid grid-cols-2 gap-4">
                                <select x-model="formData.year" class="p-4 bg-green-50/30 rounded-2xl outline-none input-focus text-sm font-bold">
                                    <option value="">Mwaka wa Masomo</option>
                                    <option>Year 1</option><option>Year 2</option><option>Year 3</option><option>Year 4+</option>
                                </select>
                                <select x-model="formData.position" class="p-4 bg-green-50/30 rounded-2xl outline-none input-focus text-sm font-bold">
                                    <option value="">Nafasi</option>
                                    <option>MWENYEKITI</option><option>KATIBU</option><option>KATIBU HAMASA</option><option>MJUMBE</option>
                                </select>
                            </div>

                            <input type="text" x-model="formData.mlezi" placeholder="Jina la Mlezi (Patron/Matron)" class="w-full p-4 bg-yellow-50/50 rounded-2xl outline-none border-2 border-yellow-100 focus:border-yellow-400 font-semibold">

                            <button @click="saveLeader" class="w-full gradient-green text-yellow-400 py-4 rounded-2xl font-black hover:shadow-2xl transition-all shadow-lg mt-2 tracking-widest">HIFADHI TAARIFA</button>
                        </div>
                    </div>
                </div>

                <div class="lg:col-span-7">
                    <div class="bg-white rounded-[2.5rem] shadow-xl shadow-green-900/5 border border-green-50 overflow-hidden">
                        <div class="p-8 border-b border-green-50 bg-green-50/20 flex justify-between items-center">
                            <h3 class="font-black text-green-900 text-sm uppercase tracking-widest">Kumbukumbu za Matawi</h3>
                            <span class="bg-green-700 text-yellow-400 px-3 py-1 rounded-lg text-[10px] font-black" x-text="myRecords.length + ' TOTAL'"></span>
                        </div>
                        <div class="overflow-x-auto">
                            <table class="w-full text-left">
                                <thead class="bg-green-50/50 text-[10px] uppercase font-black text-green-800/40">
                                    <tr>
                                        <th class="p-6">Maelezo ya Kiongozi</th>
                                        <th class="p-6">Nafasi</th>
                                        <th class="p-6 text-right">Action</th>
                                    </tr>
                                </thead>
                                <tbody class="divide-y divide-green-50">
                                    <template x-for="rec in myRecords" :key="rec.id">
                                        <tr class="hover:bg-yellow-50/30 transition-all">
                                            <td class="p-6">
                                                <div class="font-black text-green-900" x-text="rec.jina_la_kiongozi"></div>
                                                <div class="text-[10px] font-bold text-green-600" x-text="rec.phone_number"></div>
                                                <div class="text-[10px] text-yellow-600 font-black uppercase mt-1" x-text="rec.vyuo?.jina_la_chuo"></div>
                                                <div class="text-[9px] text-slate-400 font-bold" x-text="rec.course_name + ' • ' + rec.mwaka_wa_masomo"></div>
                                            </td>
                                            <td class="p-6">
                                                <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-[9px] font-black uppercase" x-text="rec.nafasi_ya_uongozi"></span>
                                                <div class="text-[9px] text-slate-400 mt-1 italic" x-text="'Mlezi: ' + rec.jina_la_mlezi"></div>
                                            </td>
                                            <td class="p-6 text-right">
                                                <button @click="deleteRecord(rec.id)" class="bg-red-50 text-red-400 hover:text-red-600 p-2 rounded-lg transition-colors">
                                                    <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
                                                </button>
                                            </td>
                                        </tr>
                                    </template>
                                </tbody>
                            </table>
                            <template x-if="myRecords.length === 0">
                                <div class="p-20 text-center">
                                    <p class="text-slate-300 text-xs font-black uppercase tracking-[0.2em]">Hakuna Taarifa Zilizopatikana</p>
                                </div>
                            </template>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </template>

    <script>
        const {{ createClient }} = supabase;
        const client = createClient('https://xickklzlmwaobzobwyws.supabase.co', 'sb_publishable_94BpD9gpOpYyWryIhzBjog_kxQRAG4W');

        function branchApp() {{
            return {{
                session: JSON.parse(localStorage.getItem('branch_session')) || null,
                loading: false,
                showPass: false,
                loginData: {{ user: '', pass: '' }},
                uniqueMikoa: [], allVyuo: [], filteredVyuo: [], myRecords: [],
                formData: {{ mkoa: '', chuo_id: '', leaderName: '', phone: '', course: '', year: '', position: '', mlezi: '' }},

                async init() {{
                    if (this.session) {{
                        await this.fetchBaseData();
                        await this.fetchMyRecords();
                    }}
                }},

                async login() {{
                    this.loading = true;
                    try {{
                        const {{ data }} = await client.from('watumiaji').select('*').eq('username', this.loginData.user).eq('password', this.loginData.pass).single();
                        if (data) {{
                            this.session = data;
                            localStorage.setItem('branch_session', JSON.stringify(data));
                            await this.init();
                        }} else {{ alert("Login failed! Hakikisha username na password ni sahihi."); }}
                    }} catch(e) {{ alert("Error!"); }} finally {{ this.loading = false; }}
                }},

                logout() {{ localStorage.removeItem('branch_session'); location.reload(); }},

                async fetchBaseData() {{
                    const {{ data }} = await client.from('vyuo').select('*').order('mkoa');
                    if (data) {{
                        this.allVyuo = data;
                        this.uniqueMikoa = [...new Set(data.map(v => v.mkoa).filter(m => m))];
                    }}
                }},

                fetchCollegesByRegion() {{
                    this.filteredVyuo = this.allVyuo.filter(v => v.mkoa === this.formData.mkoa);
                    this.formData.chuo_id = ''; 
                }},

                async saveLeader() {{
                    if (!this.formData.chuo_id || !this.formData.leaderName || !this.formData.phone) {{
                        alert("Tafadhali jaza Jina, Simu na Chuo."); return;
                    }}
                    const {{ error }} = await client.from('matawi_viongozi').insert([{{
                        mkoa: this.formData.mkoa,
                        chuo_id: this.formData.chuo_id,
                        jina_la_kiongozi: this.formData.leaderName,
                        phone_number: this.formData.phone,
                        course_name: this.formData.course,
                        mwaka_wa_masomo: this.formData.year,
                        nafasi_ya_uongozi: this.formData.position,
                        jina_la_mlezi: this.formData.mlezi,
                        created_by: this.session.id
                    }}]);

                    if (!error) {{
                        this.formData = {{ mkoa: '', chuo_id: '', leaderName: '', phone: '', course: '', year: '', position: '', mlezi: '' }};
                        await this.fetchMyRecords();
                        alert("Imefanikiwa!");
                    }} else {{ alert("Error saving record!"); }}
                }},

                async fetchMyRecords() {{
                    const {{ data }} = await client.from('matawi_viongozi')
                        .select('*, vyuo(jina_la_chuo)')
                        .eq('created_by', this.session.id)
                        .order('created_at', {{ ascending: false }});
                    this.myRecords = data || [];
                }},

                async deleteRecord(id) {{
                    if (confirm("Futa taarifa hii?")) {{
                        await client.from('matawi_viongozi').delete().eq('id', id);
                        await this.fetchMyRecords();
                    }}
                }}
            }}
        }}
    </script>
</body>
</html>
"""

# Render
components.html(full_custom_code, height=1200, scrolling=True)