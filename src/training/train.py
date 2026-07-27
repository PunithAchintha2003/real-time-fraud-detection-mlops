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

from src.config import (
    MLFLOW_TRACKING_URI,
    MLFLOW_EXPERIMENT_NAME,
    MLFLOW_REGISTERED_MODEL_NAME,
    MLFLOW_MODEL_ALIAS,
    MODELS_DIR,
    MODEL_PATH,
    SCALER_PATH,
)

from src.data.preprocessing import (
    load_data,
    preprocess_data,
)


# MLFLOW CONFIGURATION

mlflow.set_tracking_uri(
    MLFLOW_TRACKING_URI
)


# MODEL EVALUATION

def evaluate_model(
    model,
    X_test,
    y_test,
    model_name
):
    """
    Evaluate a trained classification model.

    Metrics:

    - Precision
    - Recall
    - F1 Score
    - ROC-AUC
    """

    # Generate predictions
    y_pred = model.predict(
        X_test
    )

    # Generate probabilities
    y_prob = model.predict_proba(
        X_test
    )[:, 1]

    # Calculate metrics
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

    # Display results
    print("\n" + "=" * 50)

    print(
        f"{model_name.upper()} - EVALUATION RESULTS"
    )

    print("=" * 50)

    print(
        f"Precision : {precision:.4f}"
    )

    print(
        f"Recall    : {recall:.4f}"
    )

    print(
        f"F1 Score  : {f1:.4f}"
    )

    print(
        f"ROC-AUC   : {roc_auc:.4f}"
    )

    print(
        "\nClassification Report:"
    )

    print(
        classification_report(
            y_test,
            y_pred,
            zero_division=0
        )
    )

    print(
        "Confusion Matrix:"
    )

    print(
        confusion_matrix(
            y_test,
            y_pred
        )
    )

    return {
        "precision": precision,
        "recall": recall,
        "f1_score": f1,
        "roc_auc": roc_auc,
    }


# REGISTER MODEL

def register_model_version(
    run_id,
    model_name,
    metrics
):
    """
    Register the MLflow model artifact from
    the existing training run.
    """

    print("\n" + "-" * 60)

    print(
        f"Registering {model_name} in MLflow Model Registry..."
    )

    print("-" * 60)

    # Create model URI pointing to the model artifact
    model_uri = (
        f"runs:/{run_id}/{model_name}"
    )

    # Register model from existing MLflow run
    model_version = (
        mlflow.register_model(
            model_uri=model_uri,

            name=MLFLOW_REGISTERED_MODEL_NAME
        )
    )

    version = int(
        model_version.version
    )

    print(
        "Model registered successfully."
    )

    print(
        f"Registered Model : "
        f"{MLFLOW_REGISTERED_MODEL_NAME}"
    )

    print(
        f"Model Version    : "
        f"{version}"
    )

    print(
        f"F1 Score         : "
        f"{metrics['f1_score']:.4f}"
    )

    return version


# SET CHAMPION ALIAS

def set_champion_alias(
    model_version
):
    """
    Assign the 'champion' alias to the selected
    model version.
    """

    print("\n" + "-" * 60)

    print(
        "SETTING CHAMPION MODEL ALIAS"
    )

    print("-" * 60)

    client = MlflowClient(
        tracking_uri=MLFLOW_TRACKING_URI
    )

    client.set_registered_model_alias(
        name=MLFLOW_REGISTERED_MODEL_NAME,

        alias=MLFLOW_MODEL_ALIAS,

        version=model_version
    )

    print(
        f"Registered Model : "
        f"{MLFLOW_REGISTERED_MODEL_NAME}"
    )

    print(
        f"Alias            : "
        f"@{MLFLOW_MODEL_ALIAS}"
    )

    print(
        f"Version          : "
        f"{model_version}"
    )

    print(
        "\nChampion model updated successfully."
    )


# MAIN TRAINING PIPELINE

def main():

    print("=" * 60)

    print(
        "REAL-TIME FRAUD DETECTION"
    )

    print(
        "MLFLOW TRAINING & MODEL REGISTRY PIPELINE"
    )

    print("=" * 60)

    # STEP 1: CONFIGURE MLFLOW

    print(
        "\nConfiguring MLflow..."
    )

    mlflow.set_tracking_uri(
        MLFLOW_TRACKING_URI
    )

    mlflow.set_experiment(
        MLFLOW_EXPERIMENT_NAME
    )

    print(
        f"MLflow tracking URI : "
        f"{MLFLOW_TRACKING_URI}"
    )

    print(
        f"MLflow experiment   : "
        f"{MLFLOW_EXPERIMENT_NAME}"
    )

    print(
        f"Registered model    : "
        f"{MLFLOW_REGISTERED_MODEL_NAME}"
    )

    # STEP 2: LOAD DATA

    print(
        "\nLoading dataset..."
    )

    df = load_data()

    print(
        "Dataset loaded successfully."
    )

    # STEP 3: PREPROCESS DATA

    print(
        "\nPreprocessing dataset..."
    )

    (
        X_train,
        X_test,
        y_train,
        y_test,
        scaler
    ) = preprocess_data(
        df
    )

    print(
        "Data preprocessing completed successfully."
    )

    print(
        f"\nTraining features shape : "
        f"{X_train.shape}"
    )

    print(
        f"Testing features shape  : "
        f"{X_test.shape}"
    )


    # STEP 4: TRAIN LOGISTIC REGRESSION

    print("\n" + "-" * 60)

    print(
        "Training Logistic Regression model with MLflow..."
    )

    print("-" * 60)

    logistic_params = {
        "model_type": "LogisticRegression",
        "max_iter": 1000,
        "random_state": 42,
        "test_size": 0.2,
    }

    with mlflow.start_run(
        run_name="logistic-regression"
    ) as logistic_run:

        logistic_model = (
            LogisticRegression(
                max_iter=1000,
                random_state=42
            )
        )

        logistic_model.fit(
            X_train,
            y_train
        )

        print(
            "Logistic Regression training completed."
        )

        logistic_results = evaluate_model(
            logistic_model,
            X_test,
            y_test,
            "Logistic Regression"
        )

        mlflow.log_params(
            logistic_params
        )

        mlflow.log_metrics(
            logistic_results
        )

        mlflow.set_tag(
            "model_type",
            "LogisticRegression"
        )

        mlflow.set_tag(
            "training_stage",
            "model_comparison"
        )

        # Log model artifact using a fixed artifact name
        mlflow.sklearn.log_model(
            logistic_model,
            name="logistic-regression-model"
        )

        logistic_run_id = (
            logistic_run.info.run_id
        )

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

    random_forest_params = {
        "model_type": "RandomForestClassifier",
        "n_estimators": 100,
        "random_state": 42,
        "class_weight": "balanced",
        "n_jobs": -1,
        "test_size": 0.2,
    }

    with mlflow.start_run(
        run_name="random-forest"
    ) as random_forest_run:

        random_forest_model = (
            RandomForestClassifier(
                n_estimators=100,
                random_state=42,
                class_weight="balanced",
                n_jobs=-1
            )
        )

        random_forest_model.fit(
            X_train,
            y_train
        )

        print(
            "Random Forest training completed."
        )

        random_forest_results = evaluate_model(
            random_forest_model,
            X_test,
            y_test,
            "Random Forest"
        )

        mlflow.log_params(
            random_forest_params
        )

        mlflow.log_metrics(
            random_forest_results
        )

        mlflow.set_tag(
            "model_type",
            "RandomForestClassifier"
        )

        mlflow.set_tag(
            "training_stage",
            "model_comparison"
        )

        mlflow.sklearn.log_model(
            random_forest_model,
            name="random-forest-model"
        )

        random_forest_run_id = (
            random_forest_run.info.run_id
        )

        print(
            "\nRandom Forest model logged to MLflow."
        )

        print(
            f"Run ID : {random_forest_run_id}"
        )

    # STEP 6: MODEL COMPARISON

    print("\n" + "=" * 60)

    print(
        "MODEL COMPARISON"
    )

    print("=" * 60)

    print(
        f"\n{'Metric':<15}"
        f"{'Logistic Regression':<22}"
        f"{'Random Forest':<15}"
    )

    print(
        "-" * 52
    )

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

    if (
        random_forest_results["f1_score"]
        > logistic_results["f1_score"]
    ):

        best_model = (
            random_forest_model
        )

        best_results = (
            random_forest_results
        )

        best_model_name = (
            "Random Forest"
        )

        best_run_id = (
            random_forest_run_id
        )

        best_artifact_name = (
            "random-forest-model"
        )

    else:

        best_model = (
            logistic_model
        )

        best_results = (
            logistic_results
        )

        best_model_name = (
            "Logistic Regression"
        )

        best_run_id = (
            logistic_run_id
        )

        best_artifact_name = (
            "logistic-regression-model"
        )

    print("\n" + "=" * 60)

    print(
        "BEST MODEL"
    )

    print("=" * 60)

    print(
        f"Model     : {best_model_name}"
    )

    print(
        f"Precision : "
        f"{best_results['precision']:.4f}"
    )

    print(
        f"Recall    : "
        f"{best_results['recall']:.4f}"
    )

    print(
        f"F1 Score  : "
        f"{best_results['f1_score']:.4f}"
    )

    print(
        f"ROC-AUC   : "
        f"{best_results['roc_auc']:.4f}"
    )

    print(
        f"Run ID    : {best_run_id}"
    )

    # STEP 8: REGISTER BEST MODEL

    best_model_version = (
        register_model_version(
            run_id=best_run_id,

            model_name=best_artifact_name,

            metrics=best_results
        )
    )

    # STEP 9: SET CHAMPION ALIAS

    set_champion_alias(
        best_model_version
    )

    # STEP 10: CREATE MODELS DIRECTORY

    MODELS_DIR.mkdir(
        exist_ok=True
    )

    # STEP 11: SAVE BEST MODEL LOCALLY

    joblib.dump(
        best_model,
        MODEL_PATH
    )

    # STEP 12: SAVE SCALER

    joblib.dump(
        scaler,
        SCALER_PATH
    )

    # STEP 13: FINAL OUTPUT

    print("\n" + "=" * 60)

    print(
        "MODEL REGISTRY PIPELINE COMPLETED"
    )

    print("=" * 60)

    print(
        f"Registered Model : "
        f"{MLFLOW_REGISTERED_MODEL_NAME}"
    )

    print(
        f"Model Version    : "
        f"{best_model_version}"
    )

    print(
        f"Model Alias      : "
        f"@{MLFLOW_MODEL_ALIAS}"
    )

    print(
        f"Best Model       : "
        f"{best_model_name}"
    )

    print(
        f"F1 Score         : "
        f"{best_results['f1_score']:.4f}"
    )

    print(
        f"Model path       : "
        f"{MODEL_PATH}"
    )

    print(
        f"Scaler path      : "
        f"{SCALER_PATH}"
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
        "\nTraining and model registry pipeline "
        "completed successfully."
    )


if __name__ == "__main__":
    main()