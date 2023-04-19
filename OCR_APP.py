import streamlit as st
import easyocr
import mysql.connector
import cv2
import numpy as np 
import pandas as pd
import streamlit_option_menu as st_option
from PIL import Image
import webbrowser
import io

my_pic = "24A.jpg"

st.set_page_config(page_title='OCR_APP',layout='wide', page_icon='OCR_ICON.jpeg')

page_bg_img = '''
<style>



[data-testid="stHeader"]{
    background-color: rgba(0,0,0,0);
}


</style>
'''


st.markdown(page_bg_img, unsafe_allow_html=True)

st.title(":orange[O]ptical :blue[C]harater :green[R]ecognition (:red[OCR])")



my_connection = mysql.connector.connect(
    host='localhost',
    user='root',
    password = "12345678",
    database = "OCR"
    ) 

cursor = my_connection.cursor()

# Creating a new table
# Define the table name
table_name = "OCR_CARD_IMAGE"
create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} (id INT AUTO_INCREMENT PRIMARY KEY,CardholderName VARCHAR(255),Designation VARCHAR(255),Address VARCHAR(255),Pincode VARCHAR(255),Phonenumber VARCHAR(255),email VARCHAR(255),website VARCHAR(255),CompanyName VARCHAR(255))"


# Execute the SQL query to create the table
cursor.execute(create_table_query)
my_connection.commit()
 
 
def display_navigation():   
    selected1 = st_option.option_menu(
    menu_title = "",  
    options = ["Home","About","OCR_Process","Contact"],
    icons =["house","bar-chart",'gear',"toggles","search","list-task", 'at'],
    orientation="horizontal",
    default_index=0,
    
    styles={
        
        "nav-link": {"--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}
    }
    )
    

    return selected1



def Home():
    #st.header("*:violet[Introduction]*")
    st.subheader(":orange[OCR stands for Optical Character Recognition. It is a technology that allows a computer to recognize text or characters from images or scanned documents and convert it into machine-readable text. OCR software can analyze the shapes, patterns, and arrangement of characters in an image and extract the text information for further processing, such as storing, editing, or analyzing.]")
    st.subheader("OCR has a wide range of applications, including digitization of printed documents, automated data entry, text recognition in images, text extraction from invoices, receipts, and forms, document indexing and retrieval, and more. OCR technology is widely used in industries such as finance, healthcare, logistics, legal, and administrative tasks where large amounts of text data need to be processed efficiently and accurately.")
    st.subheader(":green[OCR can be performed using various techniques, such as pattern recognition, machine learning algorithms, neural networks, and computer vision. OCR software can handle different types of fonts, languages, and document layouts, but its accuracy may vary depending on the quality of the image, the complexity of the text, and other factors. Advances in deep learning and artificial intelligence have greatly improved the accuracy and performance of OCR systems in recent years, making it a valuable tool for text recognition and data extraction tasks.]")

    
        
def About():
    
    st.subheader(":orange[This is a Streamlit application that allows users to upload an image of a business card and extract relevant information from it using easyOCR.]")

    st.subheader(":orange[The extracted information would include the company name, card holder name,designation, mobile number, email address, website URL, pincode. The extracted information would then be displayed in the application'sgraphical user interface (GUI).]")

    st.subheader("The application would also allow users to save the extracted information into a database(MySQL) along with the uploaded business card image. The database would be able to store multiple entries, each with its own business card image and extracted information.]")

    st.subheader("The final application would have a simple and intuitive user interface that guides users through the process of uploading the business card image and extracting its information. The extracted information would be displayed in a clean and organized manner, and users would be able to easily add it to the database with the click of a button.")

    st.subheader(":green[The project would require skills in image processing, OCR, GUI development, and database management. ]")

    st.subheader(":green[Overall, the result of the project would be a useful tool for businesses and individuals who need to manage business card information efficiently.]")

def Contact():
    name = "*:green[SIBI RAVICHANDRAN]* "
    mail = (f'{"ravisibi16@gmail.com"}')
    
    col1, col2 = st.columns(2)
    with col1:
        st.image(my_pic)
        if st.button('Github'):
            webbrowser.open_new_tab("https://github.com/sibiravichandran")
        if st.button('LinkedIn'):
            webbrowser.open_new_tab("https://www.linkedin.com/in/sibi-ravichandran-817ab021b/")
            
    with col2:
        st.title(name)
        st.subheader(mail)
        st.subheader(":orange[Aspiring Data Scientist with a passion for turning data into insights and using those insights to drive business decisions.I bring a wealth of knowledge and expertise to any organization looking to streamline their operations and drive growth through effective use of technology.]") 
        st.subheader("With a passion for continuous learning and professional as well as personal development, I am dedicated to staying on the cutting edge of industry trends and best practices, and am always seeking out new challenges and opportunities to expand my skillset.") 
        st.subheader("Whether it's through formal education, online courses, or simply exploring new ideas and perspectives, I am passionate about staying curious and engaged with the world around me.")
        st.subheader(":green[With a commitment to continuous growth and development, I am constantly pushing myself to reach new heights and take on new challenges and I am committed to sharing my knowledge and insights with others, and am always eager to collaborate and exchange ideas with fellow professionals in the field.. If you share my love of learning and are looking for a dynamic and enthusiastic team member to help drive innovation and success in your organization, I would love to hear from you!]")
        st.write("---")
    


def OCR():
    
    with st.sidebar:
    
        selected2 = st_option.option_menu(
        menu_title = "Business Card Data Extraction",  
        options = ['Upload','Update','View','Delete'],
        default_index=0,
        styles={
        
        "nav-link": {"--hover-color": "#6F36AD"},
        "nav-link-selected": {"background-color": "#6F36AD"}
    }
        )
    
    if selected2 == 'Upload':
    
            uploaded_file = st.file_uploader("Choose a image file",type=["jpg", "jpeg", "png"])


            # Load the OCR reader
            reader = easyocr.Reader(['en'], gpu = False)

        # Function to extract information from the business card image
            def extract_info(uploaded_file):
                # Read the text from the image using OCR
                image = Image.open(io.BytesIO(uploaded_file.read()))

                # Convert PIL Image object to numpy array
                img_array = np.array(image)

                # Pass numpy array to EasyOCR's readtext() method
                results = reader.readtext(img_array)

                if results is not None:
                    df = pd.DataFrame(columns=[])
                    for r in results:
                        df = df.append({'Data': r[1]}, ignore_index=True)
                
                

                # return results

                for res in results:
                    pts = np.array(res[0]).astype(np.int32)
                    pts = pts.reshape((-1,1,2))
                    color = (0,0,255)
                    isClosed = True
                    thickness = 2
                    cv2.polylines(img_array,[pts],isClosed,color,thickness)

                    # cv2.imshow('image', image_with_boxes)
                
                image_with_boxes = Image.fromarray(img_array)

                return df, image_with_boxes


            # Check if a file was uploaded
            if uploaded_file is not None:
                # Do something with the uploaded file
                col1, col2 = st.columns([1,1])
                col1.subheader("Uploaded File")
                col1.image(uploaded_file, caption='Uploaded business card image', use_column_width=True)
                extracted_data, image_with_boxes = extract_info(uploaded_file)
                col2.subheader("Extracted Text with Bounding Boxes")
                col2.image(image_with_boxes, caption='Extracted text with bounding boxes', use_column_width=True)

            if uploaded_file is not None:
                st.write("Below you can find the data extracted from the uploaded business card.")
                st.write("The data table displayed is editable.")
                st.write(":red[Please make sure that data is filled only from 0-7 in the extracted data table to upload it to the database which can be modified later.]")
                st.write(":red[Please fill the details in the format mentioned below to upload it to the database.]")

                #with col1:
                edited_df = st.experimental_data_editor(extracted_data, width=1000, height=400)
                #with col2:
                st.text("""Arrange as follows: \n 
                            0 CardholderName 
                            1 Designation
                            2 Address
                            3 Pincode
                            4 Phonenumber
                            5 Email
                            6 Website
                            7 CompanyName \n
                            If any one field is not available leave it blank""")

            if uploaded_file is not None:
                new_df = pd.DataFrame(columns=['CardholderName', 'Designation', 'Address', 'Pincode', 'Phonenumber', 'email', 'website','CompanyName'])  
                new_df['CardholderName'] = edited_df[edited_df.index == 0].Data.values
                new_df['Designation'] = edited_df[edited_df.index == 1].Data.values
                new_df['Address'] = edited_df[edited_df.index == 2].Data.values
                new_df['Pincode'] = edited_df[edited_df.index == 3].Data.values
                new_df['Phonenumber'] = edited_df[edited_df.index == 4].Data.values
                new_df['email'] = edited_df[edited_df.index == 5].Data.values
                new_df['website'] = edited_df[edited_df.index == 6].Data.values
                new_df['CompanyName'] = edited_df[edited_df.index == 7].Data.values
                st.dataframe(new_df)
                
                if st.button("Upload to Database"):
                    sql = "INSERT INTO ocr_card_business(CardholderName, Designation, Address,Pincode, Phonenumber,email,website,CompanyName) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s)"
                    image_data = uploaded_file.read()
                    val = (new_df['CardholderName'][0], new_df['Designation'][0], new_df['Address'][0], new_df['Pincode'][0], new_df['Phonenumber'][0], new_df['email'][0],new_df['website'][0],new_df['CompanyName'][0])
                    cursor.execute(sql, val)
                    my_connection.commit()
                    st.success("Data uploaded successfully!")
                    st.balloons()
        
    
    if selected2 =='View':
        # Fetch business card data from the database
            cursor.execute("SELECT id, CardholderName FROM ocr_card_business")
            result1 = cursor.fetchall()
            business_cards = {}
            for row in result1:
                business_cards[row[1]] = row[0]
            selected_card_name = st.selectbox("Select a business card to update", list(business_cards.keys()))

            cursor.execute("SELECT * FROM ocr_card_business WHERE CardholderName=%s", (selected_card_name,))
            result2 = cursor.fetchone()
            
            if result2 is not None:
                # Convert data to a Pandas DataFrame
                df = pd.DataFrame([result2], columns=[col[0] for col in cursor.description])

                # Close the database connection
                cursor.close()
                my_connection.close()

                # Display data in Streamlit
                st.write("Selected Business Card:")
                st.table(df)
            else:
                st.write("No data found for the selected business card.")

            # Display the current information for the selected business card
            
            st.write("ID: ", result2[0])
            
            st.write("CardholderName: ", result2[1])
            
            st.write("Designation:  ", result2[2])
            st.write("Address:  ", result2[3])
            st.write("Pincode:  ", result2[4])
            st.write("Phone Number:  ", result2[5])
            st.write("Email:    ", result2[6])
            st.write("Website:  ", result2[7])
            st.write("Company Name:  ", result2[8])
    
        
    if selected2 == 'Update':       
            # Fetch business card data from the database
            cursor.execute("SELECT id, CardholderName FROM ocr_card_business")
            result1 = cursor.fetchall()
            business_cards = {}
            for row in result1:
                business_cards[row[1]] = row[0]
            selected_card_name = st.selectbox("Select a business card to update", list(business_cards.keys()))

            cursor.execute("SELECT * FROM ocr_card_business WHERE CardholderName=%s", (selected_card_name,))
            result2 = cursor.fetchone()

            # Display the current information for the selected business card
            st.write("CardholderName:", result2[1])
            st.write("Designation:", result2[2])
            st.write("Address:", result2[3])
            st.write("Pincode:", result2[4])
            st.write("Phone Number:", result2[5])
            st.write("Email:", result2[6])
            st.write("Website:", result2[7])
            st.write("Company Name:", result2[8])


            # Get new information for the business card
            CardholderName = st.text_input("Name", result2[1])
            Designation = st.text_input("Designation", result2[2])
            Address = st.text_input("Address", result2[3])
            Pincode = st.text_input("Pincode", result2[4])
            Phone_Number = st.text_input("Phone", result2[5])
            email = st.text_input("Email", result2[6])
            website = st.text_input("Website", result2[7])
            companyName = st.text_input("Company", result2[8])

            if st.button("Update Business Card"):
                    # Update the information for the selected business card in the database
                    cursor.execute("UPDATE ocr_card_business SET CardholderName=%s, Designation=%s, Address=%s, Pincode=%s, Phonenumber=%s, email=%s, website=%s, CompanyName=%s WHERE CardholderName=%s", 
                                        (CardholderName, Designation, Address, Pincode, Phone_Number, email, website, companyName, selected_card_name))
                    my_connection.commit()
                    st.success("Business card information updated in database.")
                    st.balloons()
                    
                    #id, CardholderName, Designation, Address, Pincode, Phonenumber, email, website, CompanyName
            

    if selected2 == 'Delete':
              
            # Fetch business card data from the database
            cursor.execute("SELECT id, CardholderName FROM ocr_card_business")
            result1 = cursor.fetchall()
            business_cards = {}
            for row in result1:
                business_cards[row[1]] = row[0]
            selected_card_name = st.selectbox("Select a business card to update", list(business_cards.keys()))

            cursor.execute("SELECT * FROM ocr_card_business WHERE CardholderName=%s", (selected_card_name,))
            result2 = cursor.fetchone()
            
            if result2 is not None:
                # Convert data to a Pandas DataFrame
                df = pd.DataFrame([result2], columns=[col[0] for col in cursor.description])


                # Display data in Streamlit
                st.write("Selected Business Card:")
                st.table(df)

        
            if st.button("Delete Business Card"):
                # Delete the selected business card from the database
                cursor.execute("DELETE FROM ocr_card_business WHERE CardholderName=%s", (selected_card_name,))
                my_connection.commit()
                st.success("Business card deleted from database.")
                st.snow()
                
            # Close the database connection
            cursor.close()
            my_connection.close()









if __name__ == '__main__':
        selected1 = display_navigation()
        if selected1 == "Home":
            Home()
            
        elif selected1 == "About":
            About()
            
        elif selected1 == "Contact":
            Contact()
        
        elif selected1 == "OCR_Process":
            OCR()




