from pathlib import Path

import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

from src.config import (
    DATA_PATH,
    FEATURE_COLUMNS,
    SCALED_FEATURES,
)


# DATA LOADING

def load_data(
    data_path: Path = DATA_PATH
):
    """
    Load the credit card fraud detection dataset.

    Args:
        data_path:
            Path to the CSV dataset.

    Returns:
        pandas.DataFrame:
            Loaded dataset.
    """

    if not data_path.exists():
        raise FileNotFoundError(
            f"Dataset not found at: {data_path}"
        )

    df = pd.read_csv(
        data_path
    )

    return df


# PREPROCESS FEATURES

def preprocess_features(
    X,
    scaler,
    fit_scaler=False
):
    """
    Apply the same preprocessing used during training.

    Only Time and Amount are scaled.

    Args:
        X:
            Input feature DataFrame.

        scaler:
            StandardScaler instance.

        fit_scaler:
            If True, fit the scaler before transforming.
            Use True only for training data.

    Returns:
        pandas.DataFrame:
            Preprocessed feature DataFrame.
    """

    # Create a copy to avoid modifying the original DataFrame
    X_processed = X.copy()

    # Ensure the expected feature order
    X_processed = X_processed[
        FEATURE_COLUMNS
    ]

    # Fit scaler only during training
    if fit_scaler:

        X_processed[
            SCALED_FEATURES
        ] = scaler.fit_transform(
            X_processed[
                SCALED_FEATURES
            ]
        )

    else:

        X_processed[
            SCALED_FEATURES
        ] = scaler.transform(
            X_processed[
                SCALED_FEATURES
            ]
        )

    return X_processed


# TRAINING PREPROCESSING

def preprocess_data(df):
    """
    Prepare the dataset for machine learning.

    Workflow:

    1. Separate features and target.
    2. Split into training and testing sets.
    3. Fit scaler only on training data.
    4. Transform training data.
    5. Transform testing data using the same scaler.

    Returns:
        X_train
        X_test
        y_train
        y_test
        scaler
    """

    # STEP 1: VALIDATE TARGET COLUMN

    if "Class" not in df.columns:
        raise ValueError(
            "Dataset must contain a 'Class' target column."
        )

    # STEP 2: SEPARATE FEATURES AND TARGET

    X = df.drop(
        "Class",
        axis=1
    )

    y = df["Class"]

    # STEP 3: VALIDATE FEATURES

    missing_features = [
        feature
        for feature in FEATURE_COLUMNS
        if feature not in X.columns
    ]

    if missing_features:

        raise ValueError(
            "Missing required features: "
            + ", ".join(
                missing_features
            )
        )

    # STEP 4: SPLIT DATA

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # STEP 5: CREATE SCALER

    scaler = StandardScaler()

    # STEP 6: PREPROCESS TRAINING DATA

    X_train = preprocess_features(
        X_train,
        scaler,
        fit_scaler=True
    )

    # STEP 7: PREPROCESS TEST DATA

    X_test = preprocess_features(
        X_test,
        scaler,
        fit_scaler=False
    )

    return (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler
    )


# MAIN

def main():

    print("=" * 60)
    print("REAL-TIME FRAUD DETECTION")
    print("DATA LOADING & PREPROCESSING")
    print("=" * 60)

    # Load dataset
    print("\nLoading dataset...")

    df = load_data()

    print(
        "Dataset loaded successfully."
    )

    print(
        f"\nDataset Shape: {df.shape}"
    )

    # Display dataset information
    print("\nFirst 5 Rows:")
    print(
        df.head()
    )

    print("\nMissing Values:")
    print(
        df.isnull().sum()
    )

    print("\nClass Distribution:")
    print(
        df["Class"].value_counts()
    )

    # Preprocess dataset
    print("\nPreprocessing dataset...")

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler
    ) = preprocess_data(df)

    print(
        "Data preprocessing completed successfully."
    )

    print(
        f"\nTraining Features Shape: {X_train.shape}"
    )

    print(
        f"Testing Features Shape : {X_test.shape}"
    )

    print(
        "\nScaled Features:"
    )

    print(
        SCALED_FEATURES
    )


if __name__ == "__main__":
    main()