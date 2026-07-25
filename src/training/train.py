from pathlib import Path

import joblib
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

from src.data.preprocessing import load_data, preprocess_data


# Directory where trained models and preprocessing artifacts are stored
MODELS_DIR = Path("models")


def evaluate_model(model, X_test, y_test, model_name):
    """
    Evaluate a trained classification model using
    precision, recall, F1 score, and ROC-AUC.
    """

    # Generate class predictions
    y_pred = model.predict(X_test)

    # Generate probability predictions for the positive class
    y_prob = model.predict_proba(X_test)[:, 1]

    # Calculate evaluation metrics
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)
    roc_auc = roc_auc_score(y_test, y_prob)

    # Display model evaluation results
    print("\n" + "=" * 50)
    print(f"{model_name.upper()} - EVALUATION RESULTS")
    print("=" * 50)

    print(f"Precision : {precision:.4f}")
    print(f"Recall    : {recall:.4f}")
    print(f"F1 Score  : {f1:.4f}")
    print(f"ROC-AUC   : {roc_auc:.4f}")

    # Display detailed classification report
    print("\nClassification Report:")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Display confusion matrix
    print("Confusion Matrix:")
    print(confusion_matrix(y_test, y_pred))

    # Return metrics as a dictionary
    return {
        "model_name": model_name,
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc,
    }


def main():

    print("=" * 50)
    print("REAL-TIME FRAUD DETECTION")
    print("MODEL TRAINING & COMPARISON PIPELINE")
    print("=" * 50)

    # STEP 1: LOAD DATASET

    print("\nLoading dataset...")

    # Load the raw credit card fraud dataset
    df = load_data()

    print("Dataset loaded successfully.")

    # STEP 2: PREPROCESS DATA

    print("\nPreprocessing dataset...")

    # Split the dataset into training and testing data
    # and apply StandardScaler to Time and Amount features
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

    print("Data preprocessing completed successfully.")

    # Display dataset shapes
    print(f"\nTraining features shape : {X_train.shape}")
    print(f"Testing features shape  : {X_test.shape}")

    # STEP 3: CREATE LOGISTIC REGRESSION MODEL

    print("\n" + "-" * 50)
    print("Training Logistic Regression model...")
    print("-" * 50)

    # Create Logistic Regression baseline model
    logistic_model = LogisticRegression(
        max_iter=1000,
        random_state=42
    )

    # Train Logistic Regression model
    logistic_model.fit(X_train, y_train)

    print("Logistic Regression training completed.")

    # STEP 4: EVALUATE LOGISTIC REGRESSION

    logistic_results = evaluate_model(
        logistic_model,
        X_test,
        y_test,
        "Logistic Regression"
    )

    # STEP 5: CREATE RANDOM FOREST MODEL

    print("\n" + "-" * 50)
    print("Training Random Forest model...")
    print("-" * 50)

    # Create Random Forest model
    random_forest_model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        class_weight="balanced",
        n_jobs=-1
    )

    # Train Random Forest model
    random_forest_model.fit(X_train, y_train)

    print("Random Forest training completed.")

    # STEP 6: EVALUATE RANDOM FOREST

    random_forest_results = evaluate_model(
        random_forest_model,
        X_test,
        y_test,
        "Random Forest"
    )

    # STEP 7: COMPARE MODELS

    print("\n" + "=" * 50)
    print("MODEL COMPARISON")
    print("=" * 50)

    print(
        f"\n{'Metric':<15}"
        f"{'Logistic Regression':<22}"
        f"{'Random Forest':<15}"
    )

    print("-" * 52)

    print(
        f"{'Precision':<15}"
        f"{logistic_results['precision']:<22.4f}"
        f"{random_forest_results['precision']:<15.4f}"
    )

    print(
        f"{'Recall':<15}"
        f"{logistic_results['recall']:<22.4f}"
        f"{random_forest_results['recall']:<15.4f}"
    )

    print(
        f"{'F1 Score':<15}"
        f"{logistic_results['f1_score']:<22.4f}"
        f"{random_forest_results['f1_score']:<15.4f}"
    )

    print(
        f"{'ROC-AUC':<15}"
        f"{logistic_results['roc_auc']:<22.4f}"
        f"{random_forest_results['roc_auc']:<15.4f}"
    )

    # STEP 8: SELECT BEST MODEL

    # For this baseline comparison, select the model
    # with the highest F1 score.
    # F1 score is useful here because the dataset is highly
    # imbalanced and we want a balance between precision and recall.

    if random_forest_results["f1_score"] > logistic_results["f1_score"]:

        best_model = random_forest_model
        best_results = random_forest_results

    else:

        best_model = logistic_model
        best_results = logistic_results

    print("\n" + "=" * 50)
    print("BEST MODEL")
    print("=" * 50)

    print(f"Model     : {best_results['model_name']}")
    print(f"Precision : {best_results['precision']:.4f}")
    print(f"Recall    : {best_results['recall']:.4f}")
    print(f"F1 Score  : {best_results['f1_score']:.4f}")
    print(f"ROC-AUC   : {best_results['roc_auc']:.4f}")

    # STEP 9: CREATE MODELS DIRECTORY

    # Create models directory if it does not already exist
    MODELS_DIR.mkdir(exist_ok=True)

    # STEP 10: SAVE BEST MODEL

    # Define the path for the production model artifact
    model_path = MODELS_DIR / "fraud_detection_model.joblib"

    # Save the selected best model
    joblib.dump(best_model, model_path)

    # STEP 11: SAVE SCALER

    # Define the path for the scaler artifact
    scaler_path = MODELS_DIR / "scaler.joblib"

    # Save the fitted scaler
    joblib.dump(scaler, scaler_path)

    # STEP 12: FINAL OUTPUT

    print("\n" + "=" * 50)
    print("MODEL ARTIFACTS SAVED")
    print("=" * 50)

    print(f"Model path  : {model_path}")
    print(f"Scaler path : {scaler_path}")

    print("\nTraining and model comparison pipeline completed successfully.")

if __name__ == "__main__":
    main()