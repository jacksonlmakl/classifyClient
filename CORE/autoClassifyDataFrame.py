import openai
import pandas as pd
from CORE.getSecrets import getSecret

# Static list of column classifications

# Function to get the first 25 non-null values from each column
def get_sample_values(df):
    sample_values = {}
    if type(df) != pd.DataFrame:
        try:
            df=pd.DataFrame(df)
        except:
            df=pd.DataFrame([df])
    for column in df.columns:
        sample_values[column] = df[column].dropna().head(25).tolist()
    return sample_values

# Function to classify a column using GPT-4
def classify_column(column_name, sample_values,secrets_json):
    COLUMN_CLASSIFICATIONS = """BANK_ACCOUNT
    DRIVERS_LICENSE
    MEDICARE_NUMBER
    NATIONAL_IDENTIFIER
    ORGANIZATION_IDENTIFIER
    PASSPORT
    PHONE_NUMBER
    STREET_ADDRESS
    TAX_IDENTIFIER
    EMAIL
    IBAN
    IMEI
    IP_ADDRESS
    NAME
    PAYMENT_CARD
    URL
    VIN
    CITY
    POSTAL_CODE
    AGE
    COUNTRY
    DATE_OF_BIRTH
    ETHNICITY
    GENDER
    LAT_LONG
    LATITUDE
    LONGITUDE
    MARITAL_STATUS
    OCCUPATION
    YEAR_OF_BIRTH
    OTHER""".split('\n')
    # Set up OpenAI API key
    openai.api_key = getSecret('OPENAI',secrets_json)

    # Prompt to classify the column
    prompt = f"""You are an expert at classifying data. Based on the sample values from the column '{column_name}', 
    classify this column into one of the following categories: {', '.join(COLUMN_CLASSIFICATIONS)}. 
    Sample values: {sample_values}
    """

    # Generate a response using GPT-4 with ChatCompletion
    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": """
            You are a helpful assistant that classifies columns of a dataset. 
            You job is to classify it as one of these categories and then just return a string of that category and nothing else:
            BANK_ACCOUNT
            DRIVERS_LICENSE
            MEDICARE_NUMBER
            NATIONAL_IDENTIFIER
            ORGANIZATION_IDENTIFIER
            PASSPORT
            PHONE_NUMBER
            STREET_ADDRESS
            TAX_IDENTIFIER
            EMAIL
            IBAN
            IMEI
            IP_ADDRESS
            NAME
            PAYMENT_CARD
            URL
            VIN
            CITY
            POSTAL_CODE
            AGE
            COUNTRY
            DATE_OF_BIRTH
            ETHNICITY
            GENDER
            LAT_LONG
            LATITUDE
            LONGITUDE
            MARITAL_STATUS
            OCCUPATION
            YEAR_OF_BIRTH
            OTHER
             """},
            {"role": "user", "content": prompt}
        ],
        max_tokens=100,
        temperature=0.7
    )

    # Parse the response using response.json() to get the classification
    r_dict=response.to_dict()
    # print(r_dict,"\n\n")
    classification = r_dict.get('choices',[{}])[0].get("message",{}).get("content","").strip()
    # print("\n\n\n",classification,"\n\n\n")

    return classification


# Function to classify all columns in a DataFrame
def classify_dataframe(df,secrets_json):
    column_classifications = {}
    sample_values = get_sample_values(df)

    for column, values in sample_values.items():
        # if values:  # Only classify if there are non-null values
        classification = classify_column(column, values, secrets_json)
        column_classifications[column] = classification
        # else:
        # column_classifications[column] = 'NONE'

    return column_classifications



def autoClassify(data,secrets_json):
    if type(data) == dict:
        df = pd.DataFrame(data)
    else:
        df=data
    classifications = classify_dataframe(df,secrets_json)
    return classifications
