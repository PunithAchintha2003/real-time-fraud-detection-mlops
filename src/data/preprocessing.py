import pandas as pd
from sklearn.model_selection import train_test_split

# Path to the credit card fraud dataset

DATA_PATH = "data/creditcard.csv"

# Load the credit card fraud dataset

def load_data():
    """Load the credit card fraud dataset."""

    df = pd.read_csv(DATA_PATH)

    return df

def preprocess_data(df):
    """Prepare features and target for machine learning."""

    X = df.drop("Class", axis=1)

    y = df["Class"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    return X_train, X_test, y_train, y_test

# Main function to preprocess the credit card fraud dataset

def main():

    print("Loading dataset...")

    # Load the credit card fraud dataset and store it in a variable
    df = load_data()

    # Print the shape of the dataset
    print("\nDataset loaded successfully.")

    # Print the shape of the dataset
    print("\nDataset Shape:")
    print(df.shape)

    # Print the first 5 rows of the dataset
    print("\nFirst 5 Rows:")
    print(df.head())

    # Print the information of the dataset
    print("\nDataset Information:")
    print(df.info())

    # Print the missing values in the dataset
    print("\nMissing Values:")
    print(df.isnull().sum())

    # Print the data types of the dataset
    print("\nData Types:")
    print(df.dtypes)
    
    # Print the class distribution of the dataset
    print("\nClass Distribution:")
    print(df["Class"].value_counts())

    # Calculate the percentage of fraudulent transactions
    fraud_percentage = (
        df["Class"].value_counts(normalize=True) * 100
    )

    # Print the class distribution percentage
    print("\nClass Distribution Percentage:")
    print(fraud_percentage)

    X_train, X_test, y_train, y_test = preprocess_data(df)

    print("\nTraining Data Shape:")
    print(X_train.shape)

    print("\nTesting Data Shape:")
    print(X_test.shape)

    print("\nTraining Target Distribution:")
    print(y_train.value_counts())

    print("\nTesting Target Distribution:")
    print(y_test.value_counts())

    print("\nData preprocessing completed successfully.")

if __name__ == "__main__":
    main()