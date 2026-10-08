import streamlit as st
from PIL import Image #Images need to be converted to PIL images to pass to gemini so we import this. Gemini can work with PIL Image object not normal image. (This package comes with "streamlit" installation)


from api_call import note_generator,audio_transcript_generator,quiz_generator 
#note_generator(),audio_transcript_generator(), quiz_generator() function called from api_call.py file


st.title("Summarize Your Notes in Bangla & Give Quiz",anchor=False)

st.markdown("Upload upto 5 images to generate note summery and quizes.")

st.divider()



with st.sidebar:
    st.header("Controls")
    images = st.file_uploader("Upload upto 5 images",
                              type=['jpg','jpeg','png','webp'],
                              accept_multiple_files=True,
                              max_upload_size=10) 
    
    if images:
        if len(images)>5:
            st.error(":x: Maximum 5 photos")
        else:
            st.subheader("Uploaded Images",anchor=False)
            for i in range(0,len(images),3):
                cols = st.columns(3)

                for j, image in enumerate(images[i:i+3]):
                    with cols[j]:
                        st.image(image)
    selected_option = st.selectbox(label="Select Quiz Difficulty",
                 options=['Easy','Medium','Hard'],
                 index=None)


    btn = st.button("Submit",type="primary")
    
    if btn and len(images)<=5:
        if images or selected_option:
            if images and selected_option:
            
                st.success("Done :white_check_mark:")
            elif images:
                st.error("Please select quiz difficulty")
            else:
                st.error("Please upload your images")
        else:
            st.error("Please upload images and select quiz difficulty")

if btn and images and selected_option and len(images)<=5:
    #Note 
    with st.container(border=True):
        st.header("Your Notes",anchor=False,divider=True)

        #Images Converting to PIL images (Image.open() imported from PILL above)
        pil_iamges=[Image.open(image) for image in images] #List comprehension

        #Loading Spinner till get the response
        with st.spinner("Generating Your Notes..."):
            #Sending the PIL images to get response text for note section        
            generated_notes = note_generator(pil_iamges)
            st.markdown(generated_notes)

        #Audio Trancript
        st.subheader("Audio Transcript",anchor=False,divider=True)
        with st.spinner("Generating Audio Transcript..."):

            #Processing of the generated note for a good speech generation
            generated_notes= generated_notes.replace("*","")
            generated_notes= generated_notes.replace("#","")
            generated_notes= generated_notes.replace("$","")
            generated_notes= generated_notes.replace("%","")
            generated_notes= generated_notes.replace("\"\"","")
            generated_notes= generated_notes.replace("\'","")
            generated_notes= generated_notes.replace("-","")

            speech = audio_transcript_generator(generated_notes)

            st.audio(speech)


    #quiz
    with st.container(border=True):
        st.header(f"Quiz (Difficulty:{selected_option})",anchor=False,divider=True)
        with st.spinner("Generating Quiz..."):
            quiz=quiz_generator(pil_iamges,selected_option)
            st.markdown(quiz,unsafe_allow_html=True)