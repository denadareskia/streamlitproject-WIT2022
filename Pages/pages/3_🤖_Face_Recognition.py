from mtcnn.mtcnn import MTCNN
import streamlit as st
import matplotlib.pyplot as plt 
from matplotlib.patches import Rectangle
from matplotlib.patches import Circle
from PIL import Image
from numpy import asarray
from scipy.spatial.distance import cosine
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
import pandas as pd
import altair as alt

st.set_page_config(
    page_title="Aplikasi Cybersecurity",
    page_icon="🔐",
    layout="centered"
)

st.markdown("<h1 style='text-align: center;'>Aplikasi Face Recognition</h1>", unsafe_allow_html=True)
st.markdown("""### Pengenalan wajah adalah metode untuk mengidentifikasi atau memverifikasi identitas seseorang menggunakan wajah mereka. 
Sistem pengenalan wajah dapat digunakan untuk mengidentifikasi orang dalam foto, video, atau secara real-time.
Biasanya digunakan untuk membuka layar kunci pada sebuah ponsel pintar atau _smartphone_ atau dapat digunakan untuk autentikasi ketika user login kedalam sebuah aplikasi.
Berikut merupakan aplikasi Face Recognition atau pengenalan wajah sederhana menggunakan foto.
""")

choice = st.selectbox("Select Option",[
    "Deteksi Wajah",
    "Verifikasi Wajah"
])

def main():
    fig = plt.figure()
    if choice == "Deteksi Wajah":
        # load the image
        uploaded_file = st.file_uploader("Choose File", type=["jpg","png"])
        if uploaded_file is not None:
            data = asarray(Image.open(uploaded_file))
            # plot the image
            plt.axis("off")
            plt.imshow(data)
            # get the context for drawing boxes
            ax = plt.gca()
            # plot each box
            # load image from file
            # create the detector, using default weights
            detector = MTCNN()
            # detect faces in the image
            faces = detector.detect_faces(data)
            for face in faces:
                # get coordinates
                x, y, width, height = face['box']
                # create the shape
                rect = Rectangle((x, y), width, height, fill=False, color='maroon')
                # draw the box
                ax.add_patch(rect)
                # draw the dots
                for _, value in face['keypoints'].items():
                    # create and draw dot
                    dot = Circle(value, radius=2, color='maroon')
                    ax.add_patch(dot)
            # show the plot
            st.pyplot(fig)
        
    elif choice == "Verifikasi Wajah":
        column1, column2 = st.columns(2)
    
        with column1:
            image1 = st.file_uploader("Choose File", type=["jpg","png"])
           
        with column2:
            image2 = st.file_uploader("Select File", type=["jpg","png"])
        # define filenames
        if (image1 is not None) & (image2  is not None):
            col1, col2 = st.columns(2)
            image1 =  Image.open(image1)
            image2 =  Image.open(image2)
            with col1:
                st.image(image1)
            with col2:
                st.image(image2)

            filenames = [image1,image2]

            faces = [extract_face(f) for f in filenames]
            # convert into an array of samples
            samples = asarray(faces, "float32")
            # prepare the face for the model, e.g. center pixels
            samples = preprocess_input(samples, version=2)
            # create a vggface model
            model = VGGFace(model= "resnet50" , include_top=False, input_shape=(224, 224, 3),
            pooling= "avg" )
            # perform prediction
            embeddings = model.predict(samples)
            thresh = 0.5

            score = cosine(embeddings[0], embeddings[1])
            if score <= thresh:
                st.success( " >Wajah cocok!")
            else:
                st.error(" >Wajah TIDAK cocok")

def extract_face(file):
    pixels = asarray(file)
    plt.axis("off")
    plt.imshow(pixels)
    # create the detector, using default weights
    detector = MTCNN()
    # detect faces in the image
    results = detector.detect_faces(pixels)
    # extract the bounding box from the first face
    x1, y1, width, height = results[0]["box"]
    x2, y2 = x1 + width, y1 + height
    # extract the face
    face = pixels[y1:y2, x1:x2]
    # resize pixels to the model size
    image = Image.fromarray(face)
    image = image.resize((224, 224))
    face_array = asarray(image)
    return face_array
        
if __name__ == "__main__":
    main()