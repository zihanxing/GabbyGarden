import base64
import streamlit as st

def autoplay_audio(file_path: str):
    type = file_path.split('.')[-1]
    with open(file_path, "rb") as f:
        data = f.read()
        b64 = base64.b64encode(data).decode()
        # <audio style="display:none;" id='hidden' controls autoplay="true">
        md = f"""
            <audio id='hidden' controls autoplay="true">
            <source src="data:audio/mp3;base64,{b64}" type="audio/{type}">
            </audio>
            <script>
                function toggleButtonVisibility() {{
                    var button = document.getElementById("hidden");
                    if (button.style.display === "none") {{
                        button.style.display = "block";
                    }} else {{
                        button.style.display = "none";
                    }}
                }}
            </script>
            """
        st.markdown(
            md,
            unsafe_allow_html=True,
        )