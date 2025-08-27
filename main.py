import streamlit as st
from utils import generate_script

st.title("🎬 Video Script Generator")

with st.sidebar:
    openai_api_key = st.text_input("Please input OpenAI API Key：", type="password")
    st.markdown("[Get OpenAI API key](https://platform.openai.com/account/api-keys)")

subject = st.text_input("💡 Please enter the title of your video")
video_length = st.number_input("⏱️ Please enter the approximate duration of the video (mins)）", min_value=0.1, step=0.1)
creativity = st.slider("✨ Please enter the creativity of the video script (small numbers indicate more rigor, large numbers indicate more variety)", min_value=0.0,
                       max_value=1.0, value=0.2, step=0.1)
submit = st.button("Generate Script")

if submit and not openai_api_key:
    st.info("Please enter your OpenAI API key")
    st.stop()
if submit and not subject:
    st.info("Please enter the title of your video")
    st.stop()
if submit and not video_length >= 0.1:
    st.info("Video length must be greater than or equal to 0.1")
    st.stop()
if submit:
    with st.spinner("AI is thinking, please wait..."):
        search_result, title, script = generate_script(subject, video_length, creativity, openai_api_key)
    st.success("Video transcript generated!")
    st.subheader("🔥 Title:")
    st.write(title)
    st.subheader("📝 Video transcript:")
    st.write(script)
    with st.expander("Wikipedia search results 👀"):
        st.info(search_result)
