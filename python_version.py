import streamlit as st
import streamlit.components.v1 as components
import base64
import os

# 1. Konfigureshon ya Ukurasa
st.set_page_config(
    page_title="Master Admin System", 
    page_icon="meshack.png", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# 2. Kubadilisha picha kuwa Base64
def get_base64_image(image_path):
    if os.path.exists(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return ""

img_raw = get_base64_image("meshack.png")
img_data = f"data:image/png;base64,{img_raw}" if img_raw else "https://via.placeholder.com/150"

# 3. CSS & PWA Styles
st.markdown(f"""
    <style>
        #MainMenu {{visibility: hidden;}}
        footer {{visibility: hidden;}}
        header {{visibility: hidden;}}
        .block-container {{padding: 0px !important;}}
        iframe {{border: none !important;}}
    </style>
""", unsafe_allow_html=True)

# 4. FULL CUSTOM CODE (HTML/JS/CSS)
full_custom_code = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Master Admin | AJAX Export</title>
    <script src="https://cdn.jsdelivr.net/npm/@supabase/supabase-js@2"></script>
    <script src="https://cdn.tailwindcss.com"></script>
    <script defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: #f0f4f0; margin: 0; padding: 0; }}
        [x-cloak] {{ display: none !important; }}
        .glass {{ background: rgba(255, 255, 255, 0.9); backdrop-filter: blur(10px); }}
        .login-field {{ border: 2px solid #166534 !important; transition: all 0.2s ease; }}
        .login-field:focus {{ border-color: #eab308 !important; background: white !important; }}
        .gradient-green {{ background: linear-gradient(135deg, #15803d 0%, #166534 100%); }}
        .loader-ring {{
            position: absolute; width: 100%; height: 100%; border: 3px solid transparent;
            border-top-color: #eab308; border-right-color: #eab308; border-radius: 50%;
            animation: spin 0.8s linear infinite;
        }}
        @keyframes spin {{ from {{ transform: rotate(0deg); }} to {{ transform: rotate(360deg); }} }}
        .no-scrollbar::-webkit-scrollbar {{ display: none; }}
    </style>
</head>
<body x-data="adminApp()" x-init="init()" x-cloak>

    <template x-if="!session">
        <div class="flex items-start justify-center min-h-screen bg-[#061a06] px-4 pt-12 relative overflow-hidden">
            <div class="max-w-md w-full glass p-10 rounded-[2.5rem] shadow-2xl text-center z-10 border border-green-900/10">
                <div class="flex justify-center mb-6">
                    <div class="relative w-24 h-24 flex items-center justify-center">
                        <div x-show="isLoading" class="loader-ring"></div>
                        <img src="{img_data}" class="w-24 h-24 rounded-full object-cover border-2 border-yellow-400">
                    </div>
                </div>
                <h2 class="text-2xl font-extrabold text-green-900 mb-8 uppercase">Main Admin Login</h2>
                <div class="space-y-5 text-left">
                    <input type="text" x-model="loginData.user" placeholder="Username" class="w-full p-4 rounded-2xl login-field font-bold">
                    <input type="password" x-model="loginData.pass" placeholder="Password" class="w-full p-4 rounded-2xl login-field font-bold">
                    <button @click="login" class="w-full gradient-green text-yellow-400 py-5 rounded-2xl font-black uppercase tracking-widest text-xs">LOGIN</button>
                </div>
            </div>
        </div>
    </template>

    <template x-if="session">
        <div class="min-h-screen">
            <nav class="glass border-b border-green-100 h-20 px-6 md:px-12 flex justify-between items-center sticky top-0 z-50">
                <div class="flex items-center space-x-3">
                    <img src="{img_data}" class="w-10 h-10 rounded-full border-2 border-yellow-400">
                    <span class="font-black text-green-900 uppercase">Master Admin</span>
                </div>
                <button @click="logout" class="bg-red-50 text-red-700 px-4 py-2 rounded-xl font-bold text-[10px] uppercase">Logout</button>
            </nav>

            <main class="max-w-7xl mx-auto px-4 py-8">
                <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mb-8">
                    <div class="bg-white p-6 rounded-3xl shadow-sm border-l-4 border-yellow-500">
                        <p class="text-[9px] font-black uppercase text-slate-400">Vyuo</p>
                        <h3 class="text-3xl font-black" x-text="allVyuo.length">0</h3>
                    </div>
                    <div class="bg-white p-6 rounded-3xl shadow-sm border-l-4 border-green-600">
                        <p class="text-[9px] font-black uppercase text-slate-400">Senate (Viongozi)</p>
                        <h3 class="text-3xl font-black" x-text="allBaraza.length">0</h3>
                    </div>
                    <div class="bg-white p-6 rounded-3xl shadow-sm border-l-4 border-blue-600">
                        <p class="text-[9px] font-black uppercase text-slate-400">Viongozi Matawi</p>
                        <h3 class="text-3xl font-black" x-text="allMatawi.length">0</h3>
                    </div>
                    <div class="bg-white p-6 rounded-3xl shadow-sm border-l-4 border-purple-600">
                        <p class="text-[9px] font-black uppercase text-slate-400">Mikoa</p>
                        <h3 class="text-3xl font-black" x-text="uniqueMikoa.length">0</h3>
                    </div>
                </div>

                <div class="bg-green-900 p-6 rounded-[2.5rem] mb-8 flex flex-col md:flex-row justify-between items-center gap-4">
                    <div class="w-full md:w-1/2">
                        <label class="text-[9px] font-black text-yellow-400 uppercase mb-2 block">Chujio la Mkoa</label>
                        <select x-model="selectedRegion" @change="applyFilter" class="w-full bg-green-950 text-white p-4 rounded-xl border border-green-700 font-bold">
                            <option value="ALL">Mikoa Yote (Kitaifa)</option>
                            <template x-for="m in uniqueMikoa" :key="m"><option :value="m" x-text="m"></option></template>
                        </select>
                    </div>
                    <button @click="downloadCurrentTabCSV" class="w-full md:w-auto bg-yellow-500 hover:bg-yellow-400 text-green-950 px-8 py-4 rounded-2xl font-black text-[11px] uppercase shadow-xl transition-all active:scale-95">
                        📥 Download CSV (Tab: <span x-text="tab"></span>)
                    </button>
                </div>

                <div class="bg-white rounded-[2rem] shadow-xl overflow-hidden border">
                    <div class="p-4 border-b bg-green-50/50 flex space-x-2 overflow-x-auto no-scrollbar">
                        <button @click="tab = 'vyuo'" :class="tab === 'vyuo' ? 'bg-green-800 text-white' : ''" class="px-6 py-3 rounded-xl text-[10px] font-black uppercase whitespace-nowrap">Vyuo</button>
                        <button @click="tab = 'baraza'" :class="tab === 'baraza' ? 'bg-green-800 text-white' : ''" class="px-6 py-3 rounded-xl text-[10px] font-black uppercase whitespace-nowrap">Viongozi Senate</button>
                        <button @click="tab = 'matawi'" :class="tab === 'matawi' ? 'bg-green-800 text-white' : ''" class="px-6 py-3 rounded-xl text-[10px] font-black uppercase whitespace-nowrap">Viongozi Matawi</button>
                        <button @click="tab = 'users'" :class="tab === 'users' ? 'bg-yellow-500 text-green-900' : 'bg-slate-100 text-slate-500'" class="px-6 py-3 rounded-xl text-[10px] font-black uppercase whitespace-nowrap">Manage Users</button>
                    </div>

                    <div class="p-2">
                        <template x-if="tab === 'vyuo'">
                            <div class="overflow-x-auto">
                                <table class="w-full text-left">
                                    <thead class="bg-slate-50 text-[9px] font-black uppercase">
                                        <tr><th class="p-6">Mkoa</th><th class="p-6">Chuo</th><th class="p-6">Hali</th></tr>
                                    </thead>
                                    <tbody>
                                        <template x-for="v in filteredVyuo" :key="v.id">
                                            <tr class="border-b hover:bg-green-50/30">
                                                <td class="p-6 font-bold" x-text="v.mkoa"></td>
                                                <td class="p-6 font-black" x-text="v.jina_la_chuo"></td>
                                                <td class="p-6"><span class="px-3 py-1 bg-green-100 rounded-full text-[9px] font-black" x-text="v.ina_uvccm ? 'IPO' : 'HAKUNA'"></span></td>
                                            </tr>
                                        </template>
                                    </tbody>
                                </table>
                            </div>
                        </template>

                        <template x-if="tab === 'baraza'">
                            <div class="overflow-x-auto">
                                <table class="w-full text-left">
                                    <thead class="bg-slate-50 text-[9px] font-black uppercase">
                                        <tr><th class="p-6">Jina</th><th class="p-6">Nafasi</th><th class="p-6">Chuo</th><th class="p-6">Simu</th></tr>
                                    </thead>
                                    <tbody>
                                        <template x-for="b in filteredBaraza" :key="b.id">
                                            <tr class="border-b hover:bg-green-50/30">
                                                <td class="p-6 font-black" x-text="b.jina"></td>
                                                <td class="p-6 text-green-700 font-bold" x-text="b.nafasi"></td>
                                                <td class="p-6 font-bold" x-text="b.vyuo?.jina_la_chuo || '-'"></td>
                                                <td class="p-6" x-text="b.namba_ya_simu"></td>
                                            </tr>
                                        </template>
                                    </tbody>
                                </table>
                            </div>
                        </template>

                        <template x-if="tab === 'matawi'">
                            <div class="overflow-x-auto">
                                <table class="w-full text-left">
                                    <thead class="bg-slate-50 text-[9px] font-black uppercase">
                                        <tr><th class="p-6">Jina</th><th class="p-6">Cheo</th><th class="p-6">Chuo</th><th class="p-6">Simu</th></tr>
                                    </thead>
                                    <tbody>
                                        <template x-for="m in filteredMatawi" :key="m.id">
                                            <tr class="border-b hover:bg-green-50/30">
                                                <td class="p-6 font-black" x-text="m.jina"></td>
                                                <td class="p-6 text-blue-700 font-bold" x-text="m.cheo"></td>
                                                <td class="p-6 font-bold" x-text="m.vyuo?.jina_la_chuo || '-'"></td>
                                                <td class="p-6" x-text="m.namba_ya_simu"></td>
                                            </tr>
                                        </template>
                                    </tbody>
                                </table>
                            </div>
                        </template>

                        <template x-if="tab === 'users'">
                            <div class="p-6 space-y-6">
                                <div class="bg-slate-50 p-6 rounded-3xl border-2 border-dashed border-slate-200">
                                    <h4 class="text-xs font-black uppercase text-green-800 mb-4">Sajili Mtumiaji Mpya</h4>
                                    <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                        <input type="text" x-model="newUser.username" placeholder="Username" class="p-4 rounded-xl border font-bold">
                                        <input type="password" x-model="newUser.password" placeholder="Password" class="p-4 rounded-xl border font-bold">
                                        <button @click="addUser" class="bg-green-800 text-white rounded-xl font-black uppercase text-[10px]">Ongeza Sasa</button>
                                    </div>
                                </div>
                                <div class="overflow-x-auto">
                                    <table class="w-full text-left">
                                        <thead class="text-[9px] font-black uppercase text-slate-400">
                                            <tr><th class="p-4">Username</th><th class="p-4">Action</th></tr>
                                        </thead>
                                        <tbody>
                                            <template x-for="u in allUsers" :key="u.id">
                                                <tr class="border-b">
                                                    <td class="p-4 font-bold" x-text="u.username"></td>
                                                    <td class="p-4"><button @click="deleteUser(u.id)" class="text-red-500 font-black text-[10px] uppercase">Futa</button></td>
                                                </tr>
                                            </template>
                                        </tbody>
                                    </table>
                                </div>
                            </div>
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
                isLoading: false, tab: 'vyuo',
                loginData: {{ user: '', pass: '' }},
                newUser: {{ username: '', password: '' }},
                selectedRegion: 'ALL',
                uniqueMikoa: [], allVyuo: [], allBaraza: [], allMatawi: [], allUsers: [],
                filteredVyuo: [], filteredBaraza: [], filteredMatawi: [],

                async init() {{ 
                    if(this.session) {{ 
                        await this.loadAll();
                        await this.loadUsers();
                    }} 
                }},

                async login() {{
                    this.isLoading = true;
                    const {{ data }} = await client.from('watumiaji').select('*').eq('username', this.loginData.user).eq('password', this.loginData.pass).single();
                    if(data) {{ 
                        this.session = data; 
                        localStorage.setItem('admin_session', JSON.stringify(data)); 
                        await this.loadAll();
                        await this.loadUsers();
                    }} else {{ alert("Login Failed!"); }}
                    this.isLoading = false;
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

                async loadUsers() {{
                    const {{ data }} = await client.from('watumiaji').select('id, username');
                    this.allUsers = data || [];
                }},

                async addUser() {{
                    if(!this.newUser.username || !this.newUser.password) return alert("Jaza taarifa zote!");
                    const {{ error }} = await client.from('watumiaji').insert([
                        {{ username: this.newUser.username, password: this.newUser.password }}
                    ]);
                    if(!error) {{
                        alert("Mtumiaji ameongezwa!");
                        this.newUser = {{ username: '', password: '' }};
                        await this.loadUsers();
                    }} else {{ alert("Error: " + error.message); }}
                }},

                async deleteUser(id) {{
                    if(confirm("Je, una uhakika unataka kumfuta huyu?")) {{
                        await client.from('watumiaji').delete().eq('id', id);
                        await this.loadUsers();
                    }}
                }},

                applyFilter() {{
                    const r = this.selectedRegion;
                    this.filteredVyuo = r === 'ALL' ? this.allVyuo : this.allVyuo.filter(v => v.mkoa === r);
                    this.filteredBaraza = r === 'ALL' ? this.allBaraza : this.allBaraza.filter(b => b.vyuo?.mkoa === r);
                    this.filteredMatawi = r === 'ALL' ? this.allMatawi : this.allMatawi.filter(m => m.vyuo?.mkoa === r);
                }},

                downloadCurrentTabCSV() {{
                    let dataToExport = [];
                    let filename = `Ripoti_${{this.tab}}.csv`;
                    let headers = "";

                    if (this.tab === 'vyuo') {{
                        headers = "Mkoa,Chuo,UVCCM\\n";
                        dataToExport = this.filteredVyuo.map(v => `"${{v.mkoa}}","${{v.jina_la_chuo}}","${{v.ina_uvccm}}"`);
                    }} else if (this.tab === 'baraza') {{
                        headers = "Jina,Nafasi,Chuo,Simu\\n";
                        dataToExport = this.filteredBaraza.map(b => `"${{b.jina}}","${{b.nafasi}}","${{b.vyuo?.jina_la_chuo}}","${{b.namba_ya_simu}}"`);
                    }} else if (this.tab === 'matawi') {{
                        headers = "Jina,Cheo,Chuo,Simu\\n";
                        dataToExport = this.filteredMatawi.map(m => `"${{m.jina}}","${{m.cheo}}","${{m.vyuo?.jina_la_chuo}}","${{m.namba_ya_simu}}"`);
                    }}

                    const csvContent = headers + dataToExport.join("\\n");
                    const blob = new Blob([csvContent], {{ type: 'text/csv' }});
                    const url = URL.createObjectURL(blob);
                    const link = document.createElement("a");
                    link.href = url;
                    link.download = filename;
                    link.click();
                }}
            }}
        }}
    </script>
</body>
</html>
"""

components.html(full_custom_code, height=1300, scrolling=True)
