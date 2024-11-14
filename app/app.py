import streamlit as st
from pyspark.sql import Row
from spark_init import get_spark_session
from preprocess import clean_text_spark, remove_xxxx_udf, load_models

# Initialize Spark session and load models
spark = get_spark_session()
pipeline_model = load_models(spark)

# Define banking-related labels
labels = {
    0: "Credit Approval",
    1: "Fraudulent Transaction",
    2: "Account Inquiry",
    3: "Insurance Claim",
    4: "Customer Support"
}

# Sidebar for settings and information
st.sidebar.title("Settings and Help")
st.sidebar.info("Use this app to classify texts related to banking topics. Enter text in the main area and press 'Classify'.")

# Main title and header
st.title("Banking Complaints Text Classification")
st.markdown("This app classifies text related to banking topics into predefined categories. To get started, enter your text in the area below.")

# Initialize session state for input_text if it doesn't exist
if "input_text" not in st.session_state:
    st.session_state.input_text = ""

# Example button to autofill the text area
if st.button("Example"):
    st.session_state.input_text = "I have a question about a recent transaction in my account."

# Input text with placeholder and example text using session state
input_text = st.text_area(
    "Enter text related to banking topics:",
    placeholder="Write your complaint or inquiry here...",
    value=st.session_state.input_text
)

# Process and classify text
if st.button("Classify"):
    if input_text.strip():
        # Display loading spinner
        with st.spinner("Classifying text..."):
            # Create a Spark DataFrame with the input text
            df = spark.createDataFrame([Row(complaint_what_happened=input_text)])

            # Apply text cleaning
            df_cleaned = clean_text_spark(spark, df, 'complaint_what_happened')
            df_cleaned = df_cleaned.withColumn("complaint_what_happened", remove_xxxx_udf("complaint_what_happened"))

            # Transform the text using the pipeline
            result = pipeline_model.transform(df_cleaned)

            # Get the prediction and convert it to a label
            prediction = result.select("prediction").collect()[0][0]
            predicted_label = labels.get(prediction, "Label not defined")

            # Display the label with highlighted styling
            st.success(f"**Predicted Label:** {predicted_label}")
            
            # Optionally, display confidence score if available
            # confidence_score = result.select("probability").collect()[0][0][prediction] * 100
            # st.write(f"Confidence Level: {confidence_score:.2f}%")

        # User feedback options
        st.write("Was the classification correct?")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Yes, it is correct"):
                st.success("Thank you for your feedback.")
        with col2:
            if st.button("No, it is incorrect"):
                suggestion = st.text_input("What would be the correct classification?", "")
                st.warning("Thank you for your feedback and suggestion.")
    else:
        st.warning("Please enter some text.")

# Sidebar for additional information
st.sidebar.subheader("About the Categories")
for label, description in labels.items():
    st.sidebar.write(f"**{description}**: {label}")
