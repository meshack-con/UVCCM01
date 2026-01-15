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

# 3. Full HTML/JS/CSS (AJAX Enabled)
full_custom_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Branch Leader Portal | AJAX Enabled</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f8faf8; color: #1a2e1a; margin:0; padding:0; }}
        [x-cloak] {{ display: none !important; }}
        .glass {{ background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border: 1px solid rgba(0,0,0,0.05); }}
        .gradient-green {{ background: linear-gradient(135deg, #15803d 0%, #166534 100%); }}
        
        /* AJAX INPUT BORDERS */
        .login-input-border {{ 
            border: 2px solid #166534 !important;
            transition: all 0.3s ease;
        }}
        .login-input-border:focus {{ 
            border-color: #eab308 !important;
            box-shadow: 0 0 0 4px rgba(234, 179, 8, 0.2);
            background: white !important;
        }}

        .loader-ring {{
            position: absolute; width: 100%; height: 100%; border: 3px solid transparent;
            border-top-color: #eab308; border-right-color: #eab308; border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}
        @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
        
        /* Fade transition */
        .fade-enter {{ opacity: 0; transform: translateY(10px); }}
        .fade-enter-active {{ transition: opacity 0.4s, transform 0.4s; opacity: 1; transform: translateY(0); }}
    </style>
</head>
<body x-data="branchApp()" x-init="init()" x-cloak>

    <div x-show="loading" class="fixed inset-0 bg-black/10 z-[100] flex items-center justify-center" x-transition>
        <div class="bg-white p-4 rounded-2xl shadow-xl flex items-center space-x-3">
            <div class="w-5 h-5 border-2 border-green-600 border-t-transparent animate-spin rounded-full"></div>
            <span class="text-[10px] font-black uppercase tracking-widest text-green-800">Inatafuta...</span>
        </div>
    </div>

    <template x-if="!session">
        <div class="flex items-start justify-center min-h-screen bg-[#061a06] px-4 pt-10 md:pt-16 relative overflow-hidden">
            <div class="absolute w-96 h-96 bg-green-600/20 rounded-full blur-[100px] -top-20 -left-20"></div>
            
            <div class="max-w-md w-full glass p-8 md:p-10 rounded-[2.5rem] shadow-2xl text-center z-10 mt-4">
                <div class="flex justify-center mb-6">
                    <div class="relative w-20 h-20 flex items-center justify-center">
                        <div class="loader-ring"></div>
                        <img src="{img_data}" class="w-20 h-20 rounded-full object-cover border-2 border-yellow-400 shadow-lg">
                    </div>
                </div>
                <h2 class="text-2xl font-black text-green-900 mb-1 uppercase tracking-tighter">Branch Portal</h2>
                <p class="text-[10px] font-bold text-green-600 uppercase tracking-widest mb-8">Ingia kusimamia viongozi wa tawi</p>
                
                <div class="space-y-6 text-left">
                    <div>
                        <label class="text-[11px] font-black uppercase text-green-900 ml-2 mb-1 block">Username</label>
                        <input type="text" x-model="loginData.user" placeholder="Username" 
                            class="w-full p-4 bg-white rounded-2xl outline-none login-input-border font-bold text-slate-800 placeholder:text-slate-300">
                    </div>
                    
                    <div class="relative">
                        <label class="text-[11px] font-black uppercase text-green-900 ml-2 mb-1 block">Password</label>
                        <input :type="showPass ? 'text' : 'password'" x-model="loginData.pass" placeholder="Password" 
                            class="w-full p-4 bg-white rounded-2xl outline-none login-input-border font-bold text-slate-800 pr-16 placeholder:text-slate-300">
                        <button @click="showPass = !showPass" type="button" class="absolute right-4 top-[42px] text-green-800 font-black text-[10px]">
                             <span x-text="showPass ? 'HIDE' : 'SHOW'"></span>
                        </button>
                    </div>
                    
                    <button @click="login" :disabled="loading" 
                        class="w-full gradient-green text-yellow-400 py-5 rounded-2xl font-black shadow-lg hover:opacity-95 transition-all uppercase mt-2 tracking-widest text-sm">
                        <span>INGIA KWENYE MFUMO</span>
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
                    <span class="font-black text-lg tracking-tighter text-green-900 uppercase">Branch Portal</span>
                </div>
                <div class="flex items-center space-x-4">
                    <span class="text-[10px] font-black text-green-600 uppercase" x-text="session.username"></span>
                    <button @click="logout" class="bg-red-50 text-red-600 font-black text-[10px] px-4 py-2 rounded-xl uppercase">Logout</button>
                </div>
            </nav>

            <div class="max-w-7xl mx-auto px-4 mt-10 grid lg:grid-cols-12 gap-8">
                <div class="lg:col-span-5">
                    <div class="bg-white p-8 rounded-[2.5rem] shadow-xl border border-green-50">
                        <h3 class="text-xl font-black mb-6 text-green-900 uppercase">Sajili Kiongozi</h3>
                        
                        <div class="space-y-4">
                            <div class="grid grid-cols-2 gap-4">
                                <select x-model="formData.mkoa" @change="fetchCollegesByRegion" class="p-4 bg-green-50/30 rounded-2xl outline-none border-2 border-slate-100 focus:border-green-600 text-sm font-bold">
                                    <option value="">-- Mkoa --</option>
                                    <template x-for="m in uniqueMikoa" :key="m"><option :value="m" x-text="m"></option></template>
                                </select>
                                <select x-model="formData.chuo_id" class="p-4 bg-green-50/30 rounded-2xl outline-none border-2 border-slate-100 focus:border-green-600 text-sm font-bold">
                                    <option value="">-- Chuo --</option>
                                    <template x-for="c in filteredVyuo" :key="c.id"><option :value="c.id" x-text="c.jina_la_chuo"></option></template>
                                </select>
                            </div>

                            <input type="text" x-model="formData.leaderName" placeholder="Jina Kamili" class="w-full p-4 bg-green-50/30 rounded-2xl outline-none border-2 border-slate-100 focus:border-green-600 font-semibold">
                            
                            <div class="grid grid-cols-2 gap-4">
                                <input type="tel" x-model="formData.phone" placeholder="Simu" class="p-4 bg-green-50/30 rounded-2xl outline-none border-2 border-slate-100 focus:border-green-600 font-semibold">
                                <input type="text" x-model="formData.course" placeholder="Kozi" class="p-4 bg-green-50/30 rounded-2xl outline-none border-2 border-slate-100 focus:border-green-600 font-semibold">
                            </div>

                            <div class="grid grid-cols-2 gap-4">
                                <select x-model="formData.year" class="p-4 bg-green-50/30 rounded-2xl outline-none border-2 border-slate-100 focus:border-green-600 text-sm font-bold">
                                    <option value="">Mwaka</option>
                                    <option>Year 1</option><option>Year 2</option><option>Year 3</option><option>Year 4+</option>
                                </select>
                                <select x-model="formData.position" class="p-4 bg-green-50/30 rounded-2xl outline-none border-2 border-slate-100 focus:border-green-600 text-sm font-bold">
                                    <option value="">Nafasi</option>
                                    <option>MWENYEKITI</option><option>KATIBU</option><option>KATIBU HAMASA</option><option>MJUMBE</option>
                                </select>
                            </div>

                            <input type="text" x-model="formData.mlezi" placeholder="Jina la Mlezi" class="w-full p-4 bg-yellow-50/50 rounded-2xl outline-none border-2 border-yellow-200 font-semibold">

                            <button @click="saveLeader" :disabled="loading" class="w-full gradient-green text-yellow-400 py-4 rounded-2xl font-black tracking-widest uppercase shadow-lg">
                                <span x-text="loading ? 'INAHIFADHI...' : 'HIFADHI TAARIFA'"></span>
                            </button>
                        </div>
                    </div>
                </div>

                <div class="lg:col-span-7">
                    <div class="bg-white rounded-[2.5rem] shadow-xl border border-green-50 overflow-hidden">
                        <div class="p-6 border-b border-green-50 bg-green-50/30 flex justify-between items-center">
                            <h3 class="font-black text-green-900 text-xs uppercase tracking-widest">Orodha ya Viongozi</h3>
                            <button @click="fetchMyRecords" class="text-[9px] font-black text-green-600 uppercase underline">Refresh List</button>
                        </div>
                        <table class="w-full text-left">
                            <thead class="bg-slate-50 text-[10px] uppercase font-black text-slate-400">
                                <tr><th class="p-6">Kiongozi</th><th class="p-6">Nafasi</th><th class="p-6">Action</th></tr>
                            </thead>
                            <tbody>
                                <template x-for="rec in myRecords" :key="rec.id">
                                    <tr class="border-b border-green-50 hover:bg-green-50/20 transition-all">
                                        <td class="p-6">
                                            <div class="font-black text-green-900" x-text="rec.jina_la_kiongozi"></div>
                                            <div class="text-[10px] font-bold text-green-600" x-text="rec.phone_number"></div>
                                            <div class="text-[9px] text-slate-400" x-text="rec.vyuo?.jina_la_chuo"></div>
                                        </td>
                                        <td class="p-6">
                                            <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full text-[9px] font-black uppercase" x-text="rec.nafasi_ya_uongozi"></span>
                                        </td>
                                        <td class="p-6 text-right">
                                            <button @click="deleteRecord(rec.id)" class="text-red-400 hover:text-red-600 font-black text-[10px] uppercase">Futa</button>
                                        </td>
                                    </tr>
                                </template>
                            </tbody>
                        </table>
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

                // AJAX Login
                async login() {{
                    this.loading = true;
                    try {{
                        const {{ data, error }} = await client.from('watumiaji').select('*').eq('username', this.loginData.user).eq('password', this.loginData.pass).single();
                        if (data) {{
                            this.session = data;
                            localStorage.setItem('branch_session', JSON.stringify(data));
                            await this.init();
                        }} else {{ alert("Login Imegoma! Angalia taarifa zako."); }}
                    }} catch(e) {{ alert("Error connecting to server!"); }} finally {{ this.loading = false; }}
                }},

                logout() {{ localStorage.removeItem('branch_session'); location.reload(); }},

                async fetchBaseData() {{
                    const {{ data }} = await client.from('vyuo').select('*');
                    if (data) {{
                        this.allVyuo = data;
                        this.uniqueMikoa = [...new Set(data.map(v => v.mkoa).filter(m => m))];
                    }}
                }},

                fetchCollegesByRegion() {{
                    this.filteredVyuo = this.allVyuo.filter(v => v.mkoa === this.formData.mkoa);
                    this.formData.chuo_id = '';
                }},

                // AJAX Save
                async saveLeader() {{
                    if (!this.formData.chuo_id || !this.formData.leaderName) return alert("Jaza jina na chuo!");
                    this.loading = true;
                    
                    const payload = {{
                        mkoa: this.formData.mkoa,
                        chuo_id: parseInt(this.formData.chuo_id),
                        jina_la_kiongozi: this.formData.leaderName,
                        phone_number: this.formData.phone,
                        course_name: this.formData.course,
                        mwaka_wa_masomo: this.formData.year,
                        nafasi_ya_uongozi: this.formData.position,
                        jina_la_mlezi: this.formData.mlezi,
                        created_by: this.session.id
                    }};

                    const {{ error }} = await client.from('matawi_viongozi').insert([payload]);

                    if (!error) {{
                        this.formData = {{ mkoa: '', chuo_id: '', leaderName: '', phone: '', course: '', year: '', position: '', mlezi: '' }};
                        // AJAX Refresh Table
                        await this.fetchMyRecords();
                        alert("Taarifa Zimehifadhiwa!");
                    }} else {{ 
                        alert("Kuna tatizo: " + error.message); 
                    }}
                    this.loading = false;
                }},

                // AJAX Fetch
                async fetchMyRecords() {{
                    const {{ data }} = await client.from('matawi_viongozi').select('*, vyuo(jina_la_chuo)').eq('created_by', this.session.id).order('created_at', {{ ascending: false }});
                    this.myRecords = data || [];
                }},

                // AJAX Delete
                async deleteRecord(id) {{
                    if (confirm("Futa taarifa hii?")) {{
                        this.loading = true;
                        const {{ error }} = await client.from('matawi_viongozi').delete().eq('id', id);
                        if(!error) await this.fetchMyRecords();
                        this.loading = false;
                    }}
                }}
            }}
        }}
    </script>
</body>
</html>
"""

components.html(full_custom_code, height=1200, scrolling=True)
