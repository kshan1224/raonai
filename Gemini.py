#Author - MrSentinel

import streamlit as st 
import google.generativeai as genai 
import google.ai.generativelanguage as glm 
from dotenv import load_dotenv
from PIL import Image
import os 
import io 
#from streamlit_extras.buy_me_a_coffee import button

#button(username="rwar", floating=True, width=221)
load_dotenv() 

def image_to_byte_array(image: Image) -> bytes:
    imgByteArr = io.BytesIO()
    image.save(imgByteArr, format=image.format)
    imgByteArr=imgByteArr.getvalue()
    return imgByteArr

API_KEY = os.environ.get("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)


# Define the custom CSS
custom_css = """
<style>
    .stTextInput>div>div>input {
        border: 2px solid #4CAF50; /* You can change the color and size of the border here */
    }
    .big-font {
        font-size: 10px; /* Change the size as needed */
    }
</style>
"""

# Inject the custom CSS with st.markdown
st.markdown(custom_css, unsafe_allow_html=True)
#st.header("무엇이든 물어보세요.")
# Create two columns
col1, col2 = st.columns([1, 4])

# Display the image in the first column
col1.image("./ai_image.jpg", width=100)
# Display the text in the second column
col2.header("라온 챗봇에 오신걸 환영합니다.")

gemini_vision, gemini_pro  = st.tabs(["AI 로또번호생성", "대화형 챗봇(텍스트)"])
# HTML 코드 삽입
html_code = """
<ins class="kakao_ad_area" style="display:none;"
data-ad-unit="DAN-YJPgdkNkga5Qw7Ma"
data-ad-width="320"
data-ad-height="100"></ins>
<script type="text/javascript" src="//t1.daumcdn.net/kas/static/ba.min.js" async></script>
"""


def main():
    with gemini_vision:

        #image_prompt = st.text_input("Interact with the Image", placeholder="Prompt", label_visibility="visible")
        uploaded_file = st.file_uploader("나와 연관된 이미지를 올리고 로또번호생성 버튼을 눌러주세요.", accept_multiple_files=False, type=["png", "jpg", "jpeg", "img", "webp"])
        image_prompt ="Generate 6 random numbers between 1 and 45 for the Korean Lotto."
        if uploaded_file is not None:
            st.image(Image.open(uploaded_file), use_column_width=True)

            st.markdown("""
                <style>
                        img {
                            border-radius: 10px;
                        }
                </style>
                """, unsafe_allow_html=True)
            
        if st.button("로또번호생성", use_container_width=True):
            model = genai.GenerativeModel("gemini-pro-vision")

            if uploaded_file is not None:
                if image_prompt != "":
                    image = Image.open(uploaded_file)

                    response = model.generate_content(
                        glm.Content(
                            parts = [
                                glm.Part(text=image_prompt),
                                glm.Part(
                                    inline_data=glm.Blob(
                                        mime_type="image/jpeg",
                                        data=image_to_byte_array(image)
                                    )
                                )
                            ]
                        )
                    )

                    response.resolve()

                    st.write("")
                    st.write(":blue[답변]")
                    st.write("")

                    st.markdown(response.text)
                    #st.markdown(f'<div class="big-font">{response.text}</div>', unsafe_allow_html=True)

                else:
                    st.write("")
                    st.header(":red[Please Provide a prompt]")

            else:
                st.write("")
                st.header(":red[Please Provide an image]")
    with gemini_pro:

        prompt = st.text_input("아래 입력란에 궁금한 내용을 적어주세요.", placeholder="예시) AI 기술은 한국인의 일상생활에 어떤 방식으로 접목되고 있나요?", label_visibility="visible")
        model = genai.GenerativeModel("gemini-pro")

        if st.button("질문 보내기",use_container_width=True):
            response = model.generate_content(prompt)

            st.write("")
            st.header(":blue[답변]")
            st.write("")

            st.markdown(response.text)
#st.markdown(html_code, unsafe_allow_html=True)
st.components.v1.html(html_code, height=150, scrolling=True)
# iframe을 사용하여 HTML 코드를 삽입
# Read the AdSense HTML code from the file
with open("index.html", "r") as file:
    ad_code_html = file.read()


if __name__ == "__main__":
    main()



