from pathlib import Path

import joblib
import mlflow
import mlflow.sklearn

from mlflow import MlflowClient

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

# PROJECT CONFIGURATION

# Directory where the best production model and scaler are stored
MODELS_DIR = Path("models")

# MLflow SQLite tracking database
MLFLOW_TRACKING_URI = "sqlite:///mlflow.db"

# MLflow experiment name
EXPERIMENT_NAME = "fraud-detection-model-comparison"

# MLflow registered model name
REGISTERED_MODEL_NAME = "FraudDetectionModel"

# Alias used to identify the current production candidate
MODEL_ALIAS = "champion"

# MODEL EVALUATION

def evaluate_model(model, X_test, y_test, model_name):
    """
    Evaluate a trained classification model using:

    - Precision
    - Recall
    - F1 Score
    - ROC-AUC

    Returns:
        dict: Model evaluation metrics.
    """

    # Generate class predictions
    y_pred = model.predict(X_test)

    # Generate probability predictions for the positive class
    y_prob = model.predict_proba(X_test)[:, 1]

    # Calculate evaluation metrics
    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0
    )

    roc_auc = roc_auc_score(
        y_test,
        y_prob
    )

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

    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )

    # Display confusion matrix
    print("Confusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    # Return metrics as a dictionary
    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc,
    }

# REGISTER MODEL VERSION

def register_model_version(
    model,
    run_id,
    model_name,
    metrics
):
    """
    Register a trained MLflow model and create a new model version.

    Returns:
        int: Registered model version number.
    """

    print("\n" + "-" * 60)
    print(f"Registering {model_name} in MLflow Model Registry...")
    print("-" * 60)

    # Create a temporary MLflow run context
    # using the original training run ID.
    with mlflow.start_run(
        run_id=run_id
    ):

        # Log additional model registry metadata
        mlflow.set_tag(
            "registered_model",
            REGISTERED_MODEL_NAME
        )

        mlflow.set_tag(
            "model_selection_metric",
            "f1_score"
        )

        # Log model to MLflow Model Registry
        model_info = mlflow.sklearn.log_model(
            model,
            name=model_name,
            registered_model_name=REGISTERED_MODEL_NAME
        )

    # Extract registered model version
    version = model_info.registered_model_version

    # Display registry information
    print(
        f"{model_name} registered successfully."
    )

    print(
        f"Registered Model : {REGISTERED_MODEL_NAME}"
    )

    print(
        f"Model Version    : {version}"
    )

    print(
        f"F1 Score         : {metrics['f1_score']:.4f}"
    )

    return int(version)

# SET MODEL ALIAS

def set_champion_alias(model_version):
    """
    Assign the 'champion' alias to the selected best model version.

    MLflow 3.x uses aliases instead of the older Production stage
    workflow.
    """

    print("\n" + "-" * 60)
    print("SETTING CHAMPION MODEL ALIAS")
    print("-" * 60)

    # Create MLflow client
    client = MlflowClient(
        tracking_uri=MLFLOW_TRACKING_URI
    )

    # Assign champion alias to the selected model version
    client.set_registered_model_alias(
        name=REGISTERED_MODEL_NAME,
        alias=MODEL_ALIAS,
        version=model_version
    )

    print(
        f"Registered Model : {REGISTERED_MODEL_NAME}"
    )

    print(
        f"Alias            : @{MODEL_ALIAS}"
    )

    print(
        f"Version          : {model_version}"
    )

    print(
        "\nChampion model updated successfully."
    )

# MAIN TRAINING PIPELINE

def main():

    print("=" * 60)
    print("REAL-TIME FRAUD DETECTION")
    print("MLFLOW TRAINING & MODEL REGISTRY PIPELINE")
    print("=" * 60)

    # STEP 1: CONFIGURE MLFLOW

    print("\nConfiguring MLflow...")

    # Set SQLite database as MLflow tracking backend
    mlflow.set_tracking_uri(
        MLFLOW_TRACKING_URI
    )

    # Create or select MLflow experiment
    mlflow.set_experiment(
        EXPERIMENT_NAME
    )

    print(
        f"MLflow tracking URI : {MLFLOW_TRACKING_URI}"
    )

    print(
        f"MLflow experiment   : {EXPERIMENT_NAME}"
    )

    print(
        f"Registered model    : {REGISTERED_MODEL_NAME}"
    )

    # STEP 2: LOAD DATASET

    print("\nLoading dataset...")

    # Load raw credit card fraud dataset
    df = load_data()

    print(
        "Dataset loaded successfully."
    )

    # STEP 3: PREPROCESS DATA

    print("\nPreprocessing dataset...")

    # Split dataset and apply StandardScaler
    X_train, X_test, y_train, y_test, scaler = preprocess_data(df)

    print(
        "Data preprocessing completed successfully."
    )

    # Display dataset shapes
    print(
        f"\nTraining features shape : {X_train.shape}"
    )

    print(
        f"Testing features shape  : {X_test.shape}"
    )

    # STEP 4: TRAIN LOGISTIC REGRESSION

    print("\n" + "-" * 60)
    print(
        "Training Logistic Regression model with MLflow..."
    )
    print("-" * 60)

    # Logistic Regression parameters
    logistic_params = {
        "model_type": "LogisticRegression",
        "max_iter": 1000,
        "random_state": 42,
        "test_size": 0.2,
    }

    # Train Logistic Regression inside MLflow run
    with mlflow.start_run(
        run_name="logistic-regression"
    ) as logistic_run:

        # Create model
        logistic_model = LogisticRegression(
            max_iter=1000,
            random_state=42
        )

        # Train model
        logistic_model.fit(
            X_train,
            y_train
        )

        print(
            "Logistic Regression training completed."
        )

        # Evaluate model
        logistic_results = evaluate_model(
            logistic_model,
            X_test,
            y_test,
            "Logistic Regression"
        )

        # Log parameters
        mlflow.log_params(
            logistic_params
        )

        # Log metrics
        mlflow.log_metrics(
            logistic_results
        )

        # Add model metadata tags
        mlflow.set_tag(
            "model_type",
            "LogisticRegression"
        )

        mlflow.set_tag(
            "training_stage",
            "model_comparison"
        )

        # Log model artifact
        mlflow.sklearn.log_model(
            logistic_model,
            name="logistic-regression-model"
        )

        # Store MLflow run ID
        logistic_run_id = logistic_run.info.run_id

        print(
            "\nLogistic Regression model logged to MLflow."
        )

        print(
            f"Run ID : {logistic_run_id}"
        )

    # STEP 5: TRAIN RANDOM FOREST

    print("\n" + "-" * 60)
    print(
        "Training Random Forest model with MLflow..."
    )
    print("-" * 60)

    # Random Forest parameters
    random_forest_params = {
        "model_type": "RandomForestClassifier",
        "n_estimators": 100,
        "random_state": 42,
        "class_weight": "balanced",
        "n_jobs": -1,
        "test_size": 0.2,
    }

    # Train Random Forest inside MLflow run
    with mlflow.start_run(
        run_name="random-forest"
    ) as random_forest_run:

        # Create Random Forest model
        random_forest_model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        )

        # Train model
        random_forest_model.fit(
            X_train,
            y_train
        )

        print(
            "Random Forest training completed."
        )

        # Evaluate model
        random_forest_results = evaluate_model(
            random_forest_model,
            X_test,
            y_test,
            "Random Forest"
        )

        # Log parameters
        mlflow.log_params(
            random_forest_params
        )

        # Log metrics
        mlflow.log_metrics(
            random_forest_results
        )

        # Add model metadata tags
        mlflow.set_tag(
            "model_type",
            "RandomForestClassifier"
        )

        mlflow.set_tag(
            "training_stage",
            "model_comparison"
        )

        # Log model artifact
        mlflow.sklearn.log_model(
            random_forest_model,
            name="random-forest-model"
        )

        # Store MLflow run ID
        random_forest_run_id = random_forest_run.info.run_id

        print(
            "\nRandom Forest model logged to MLflow."
        )

        print(
            f"Run ID : {random_forest_run_id}"
        )

    # STEP 6: COMPARE MODELS

    print("\n" + "=" * 60)
    print("MODEL COMPARISON")
    print("=" * 60)

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

    # STEP 7: SELECT BEST MODEL

    # Select model with highest F1 score
    if (
        random_forest_results["f1_score"]
        > logistic_results["f1_score"]
    ):

        best_model = random_forest_model
        best_results = random_forest_results
        best_model_name = "Random Forest"
        best_run_id = random_forest_run_id

    else:

        best_model = logistic_model
        best_results = logistic_results
        best_model_name = "Logistic Regression"
        best_run_id = logistic_run_id

    print("\n" + "=" * 60)
    print("BEST MODEL")
    print("=" * 60)

    print(
        f"Model     : {best_model_name}"
    )

    print(
        f"Precision : {best_results['precision']:.4f}"
    )

    print(
        f"Recall    : {best_results['recall']:.4f}"
    )

    print(
        f"F1 Score  : {best_results['f1_score']:.4f}"
    )

    print(
        f"ROC-AUC   : {best_results['roc_auc']:.4f}"
    )

    print(
        f"Run ID    : {best_run_id}"
    )

    # STEP 8: REGISTER BEST MODEL

    best_model_version = register_model_version(
        model=best_model,
        run_id=best_run_id,
        model_name="production-model",
        metrics=best_results
    )

    # STEP 9: SET CHAMPION ALIAS

    set_champion_alias(
        best_model_version
    )

    # STEP 10: CREATE MODELS DIRECTORY

    # Create models directory if it does not exist
    MODELS_DIR.mkdir(
        exist_ok=True
    )

    # STEP 11: SAVE BEST MODEL LOCALLY

    # Define production model path
    model_path = (
        MODELS_DIR
        / "fraud_detection_model.joblib"
    )

    # Save selected best model
    joblib.dump(
        best_model,
        model_path
    )

    # STEP 12: SAVE SCALER

    # Define scaler path
    scaler_path = (
        MODELS_DIR
        / "scaler.joblib"
    )

    # Save fitted scaler
    joblib.dump(
        scaler,
        scaler_path
    )

    # STEP 13: FINAL OUTPUT

    print("\n" + "=" * 60)
    print("MODEL REGISTRY PIPELINE COMPLETED")
    print("=" * 60)

    print(
        f"Registered Model : {REGISTERED_MODEL_NAME}"
    )

    print(
        f"Model Version    : {best_model_version}"
    )

    print(
        f"Model Alias      : @{MODEL_ALIAS}"
    )

    print(
        f"Best Model       : {best_model_name}"
    )

    print(
        f"F1 Score         : {best_results['f1_score']:.4f}"
    )

    print(
        f"Model path       : {model_path}"
    )

    print(
        f"Scaler path      : {scaler_path}"
    )

    print(
        "\nMLflow tracking completed successfully."
    )

    print(
        "MLflow Model Registry updated successfully."
    )

    print(
        "Champion model alias updated successfully."
    )

    print(
        "\nTraining and model registry pipeline completed successfully."
    )

if __name__ == "__main__":
    main()