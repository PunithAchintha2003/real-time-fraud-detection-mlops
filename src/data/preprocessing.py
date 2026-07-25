import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# Path to the credit card fraud dataset
DATA_PATH = "data/creditcard.csv"


def load_data():
    """Load the credit card fraud dataset."""

    # Read the CSV dataset into a pandas DataFrame
    df = pd.read_csv(DATA_PATH)

    return df


def preprocess_data(df):
    """
    Prepare the dataset for machine learning.

    This function:
    1. Separates features and target
    2. Splits the dataset into training and testing sets
    3. Scales the Time and Amount features
    4. Returns the processed data and fitted scaler
    """

    # Separate input features from the target variable
    X = df.drop("Class", axis=1)
    y = df["Class"]

    # Split the dataset into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Create a StandardScaler instance
    scaler = StandardScaler()

    # Fit the scaler only on the training data
    X_train[["Time", "Amount"]] = scaler.fit_transform(
        X_train[["Time", "Amount"]]
    )

    # Apply the already-fitted scaler to the test data
    X_test[["Time", "Amount"]] = scaler.transform(
        X_test[["Time", "Amount"]]
    )

    # Return the processed training and testing datasets
    return X_train, X_test, y_train, y_test, scaler


def main():
    """Run the data exploration and preprocessing workflow."""

    print("Loading dataset...")

    # Load the credit card fraud dataset
    df = load_data()

    print("\nDataset loaded successfully.")

    print("\nDataset Shape:")
    print(df.shape)

    print("\nFirst 5 Rows:")
    print(df.head())

    print("\nDataset Information:")
    df.info()

    print("\nMissing Values:")
    print(df.isnull().sum())

    print("\nData Types:")
    print(df.dtypes)

    print("\nClass Distribution:")
    print(df["Class"].value_counts())

    # Calculate the percentage distribution of each class
    class_percentage = (
        df["Class"].value_counts(normalize=True) * 100
    )

    print("\nClass Distribution Percentage:")
    print(class_percentage)

    # Preprocess the dataset
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

    print("\nTraining Data Shape:")
    print(X_train.shape)

    print("\nTesting Data Shape:")
    print(X_test.shape)

    print("\nTraining Target Distribution:")
    print(y_train.value_counts())

    print("\nTesting Target Distribution:")
    print(y_test.value_counts())

    print("\nFeature Scaling:")
    print("Time and Amount features scaled using StandardScaler.")

    print("\nScaled Feature Sample:")
    print(X_train[["Time", "Amount"]].head())

    print("\nScaled Training Feature Statistics:")
    print(X_train[["Time", "Amount"]].agg(["mean", "std"]))

    print("\nData preprocessing completed successfully.")

if __name__ == "__main__":
    main()