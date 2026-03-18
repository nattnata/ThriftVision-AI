import streamlit as st
import google.generativeai as genai
import PIL.Image
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY") or "AIzaSyB9GnYArefm6OnZx_A9AarfL5PeRaQJoG0"
genai.configure(api_key=API_KEY)

generation_config = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

model = genai.GenerativeModel(
    model_name='gemini-2.5-flash',
    generation_config=generation_config,
    system_instruction="""
    Kamu adalah 'ThriftVision: AI Wardrobe Scanner', asisten fashion Gen-Z yang ahli dalam mix-and-match pakaian thrift dan sustainable fashion.
    
    Tugas utama kamu:
    1. Memberikan saran padu padan (outfit ideas) berdasarkan pakaian yang dimiliki pengguna.
    2. Jika pengguna mengunggah foto, analisis warna, bahan, dan potongan pakaiannya untuk diberikan saran gaya (misal: 'Old Money', 'Streetwear', atau 'Coquette').
    3. Selalu berikan tips ramah lingkungan (misal: cara merawat baju bekas agar awet).
    
    Aturan Persona:
    - Gunakan bahasa gaul yang sopan (pake istilah 'slang' dikit boleh, kayak: 'vibe-nya dapet banget', 'auto-flexing', atau 'clean look').
    - Gunakan banyak emoji fashion (👕, 👟, ✨, 🎀, 🧥, 👜, 🥾, 👠, ˚🛍️, 👗, 👢, 🧣, 🧢, 👖, 🎧, 👔, 📸, 👗, 👚, 🛒, 🧶, 🧤, 👘, 👙, 👞, 👡, 🥾, 👛, 🎒, 💼, 👒, 🧢, 👑, 🕶️, 👓, 💍, ⌚, 🧵, ✂️, 💄, 💎, 🔥).
    - Jika ditanya di luar fashion, jawab: 'Duh, aku hanya bisa membahas seputar fashion! Yuk bahas outfit aja biar makin kece!'
    """
)

st.set_page_config(page_title="ThriftVision", page_icon="🛒")

with st.sidebar:
    st.title("📸 Wardrobe Scan")
    uploaded_files = st.file_uploader("Upload foto-foto bajumu!", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    
    if uploaded_files:
        for uploaded_file in uploaded_files:
            st.image(uploaded_file, caption="Item terdeteksi", use_container_width=True)
    
    st.divider()
    st.write("### Tips Hari Ini:")
    st.info("Mencuci baju dengan air dingin bisa menghemat energi dan menjaga serat kain tetap awet!")

    st.divider()
    if st.button("🗑️ Mulai Chat Baru", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.title("🧺 ThriftVision")
st.caption("Solusi Mix-and-Match Thrift kamu agar tetap keren & ramah lingkungan!")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tanya tips style atau cara padu padan..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            content_to_send = [prompt]
            
            if uploaded_files:
                for uploaded_file in uploaded_files:
                    img = PIL.Image.open(uploaded_file)
                    content_to_send.append(img)
            
            response = model.generate_content(content_to_send)
            
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
             st.error(f"Waduh, ada kendala teknis: {e}")