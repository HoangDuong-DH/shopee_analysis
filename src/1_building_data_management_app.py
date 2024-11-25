import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    st.title("Data Management App with Visualization and Summary")
    st.write("Upload a CSV file to start.")

    # File uploader
    uploaded_file = st.file_uploader("Choose a CSV file", type=['csv'])
    if uploaded_file is not None:
        try:
            # Read the CSV file
            df = pd.read_csv(uploaded_file)
            st.success("File successfully uploaded!")
        except Exception as e:
            st.error(f"Error reading CSV file: {e}")
            return

        # Display the dataframe
        st.subheader("Data Preview")
        st.dataframe(df)

        # Allow user to select an action: View, Edit, Add, Delete, Visualize, Summary
        action = st.selectbox("Select Action", ["Edit", "Add", "Delete", "Visualize", "Summary"])
        if action == "Edit":
            st.write("Edit Data")
            # For editing, we can allow the user to select a row and column to edit
            st.write("Select the row and column you want to edit.")
            row_index = st.number_input("Row index", min_value=0, max_value=len(df) - 1, value=0, step=1)
            column = st.selectbox("Column", df.columns)
            new_value = st.text_input("New value", str(df.at[row_index, column]))

            if st.button("Update"):
                df.at[row_index, column] = new_value
                st.success("Data updated.")
                st.dataframe(df)

        elif action == "Add":
            st.write("Add a new row")
            new_row = {}
            for col in df.columns:
                new_row[col] = st.text_input(f"Value for {col}", '')
            if st.button("Add Row"):
                df = df.append(new_row, ignore_index=True)
                st.success("Row added.")
                st.dataframe(df)

        elif action == "Delete":
            st.write("Delete a row")
            row_to_delete = st.number_input("Row index to delete", min_value=0, max_value=len(df) - 1, value=0, step=1)
            if st.button("Delete Row"):
                df = df.drop(df.index[row_to_delete]).reset_index(drop=True)
                st.success("Row deleted.")
                st.dataframe(df)

        elif action == "Visualize":
            st.write("Data Visualization")
            st.write("Select the type of chart and columns to visualize.")

            chart_type = st.selectbox("Chart Type", ["Bar Chart", "Line Chart", "Pie Chart", "Histogram", "Scatter Plot"])

            if chart_type == "Pie Chart":
                column = st.selectbox("Select Column for Pie Chart", df.columns)
                if st.button("Generate Chart"):
                    fig, ax = plt.subplots()
                    data = df[column].value_counts()
                    ax.pie(data, labels=data.index, autopct='%1.1f%%', startangle=90)
                    ax.axis('equal')
                    st.pyplot(fig)

            elif chart_type == "Histogram":
                column = st.selectbox("Select Numeric Column for Histogram", df.select_dtypes(include=['float', 'int']).columns)
                bins = st.slider("Number of Bins", min_value=5, max_value=50, value=10)
                if st.button("Generate Chart"):
                    fig, ax = plt.subplots()
                    ax.hist(df[column], bins=bins)
                    ax.set_xlabel(column)
                    ax.set_ylabel('Frequency')
                    st.pyplot(fig)

            elif chart_type == "Bar Chart":
                x_column = st.selectbox("Select X-axis Column", df.columns)
                y_column = st.selectbox("Select Y-axis Column", df.select_dtypes(include=['float', 'int']).columns)
                if st.button("Generate Chart"):
                    fig, ax = plt.subplots()
                    sns.barplot(data=df, x=x_column, y=y_column, ax=ax)
                    st.pyplot(fig)

            elif chart_type == "Line Chart":
                x_column = st.selectbox("Select X-axis Column", df.columns)
                y_column = st.selectbox("Select Y-axis Column", df.select_dtypes(include=['float', 'int']).columns)
                if st.button("Generate Chart"):
                    fig, ax = plt.subplots()
                    sns.lineplot(data=df, x=x_column, y=y_column, ax=ax)
                    st.pyplot(fig)

            elif chart_type == "Scatter Plot":
                x_column = st.selectbox("Select X-axis Column", df.select_dtypes(include=['float', 'int']).columns)
                y_column = st.selectbox("Select Y-axis Column", df.select_dtypes(include=['float', 'int']).columns, index=1)
                hue_column = st.selectbox("Select Hue Column (Optional)", [None] + list(df.columns), index=0)
                if st.button("Generate Chart"):
                    fig, ax = plt.subplots()
                    if hue_column and hue_column != 'None':
                        sns.scatterplot(data=df, x=x_column, y=y_column, hue=hue_column, ax=ax)
                    else:
                        sns.scatterplot(data=df, x=x_column, y=y_column, ax=ax)
                    st.pyplot(fig)


        elif action == "Summary":

            st.write("Summary of Data")

            st.write("Here you can see an overview of the data to help with analysis and decision making.")

            st.subheader("Statistical Summary")

            # Display general statistical summary

            st.write("Descriptive Statistics for Numeric Columns:")

            st.dataframe(df.describe())

            # Count unique values in each column

            st.write("Count of Unique Values in Each Column:")

            unique_counts = df.nunique().to_frame(name='Unique Count')

            st.dataframe(unique_counts)

            # Display missing values count

            st.write("Missing Values in Each Column:")

            missing_values = df.isnull().sum().to_frame(name='Missing Count')

            st.dataframe(missing_values)

            # Display correlation matrix if numeric columns are available

            numeric_df = df.select_dtypes(include=['float', 'int'])

            if len(numeric_df.columns) > 1:
                st.subheader("Correlation Matrix")

                corr = numeric_df.corr()

                fig, ax = plt.subplots()

                sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax)

                st.pyplot(fig)
        # Allow user to download the modified data
        st.subheader("Download Data")
        if st.button("Download CSV"):
            # Convert DataFrame to CSV
            csv = df.to_csv(index=False)
            # Create a download link
            st.download_button(label="Download CSV", data=csv, file_name='modified_data.csv', mime='text/csv')
    else:
        st.info("Awaiting CSV file to be uploaded.")

if __name__ == '__main__':
    main()
