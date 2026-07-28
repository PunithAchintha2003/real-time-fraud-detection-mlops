from typing import Any, Dict, Optional, Tuple

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
    model_name,
):
    """
    Evaluate a trained classification model.

    Metrics:
        - Precision
        - Recall
        - F1 Score
        - ROC-AUC
    """

    # GENERATE PREDICTIONS

    y_pred = model.predict(
        X_test
    )

    # GENERATE FRAUD PROBABILITIES

    y_prob = model.predict_proba(
        X_test
    )[:, 1]

    # CALCULATE METRICS

    precision = precision_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    recall = recall_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    f1 = f1_score(
        y_test,
        y_pred,
        zero_division=0,
    )

    roc_auc = roc_auc_score(
        y_test,
        y_prob,
    )

    # DISPLAY RESULTS

    print(
        "\n" + "=" * 60
    )

    print(
        f"{model_name.upper()} - EVALUATION RESULTS"
    )

    print(
        "=" * 60
    )

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
            zero_division=0,
        )
    )

    print(
        "Confusion Matrix:"
    )

    print(
        confusion_matrix(
            y_test,
            y_pred,
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
    run_id: str,
    logged_model_id: str,
    metrics: Dict[str, float],
):
    """
    Register the selected MLflow Logged Model
    in the MLflow Model Registry.

    MLflow 3.x compatible approach.

    Uses the Logged Model ID directly instead of
    searching artifacts with search_logged_models().
    """

    print(
        "\n" + "=" * 60
    )

    print(
        "REGISTERING MODEL IN MLFLOW MODEL REGISTRY"
    )

    print(
        "=" * 60
    )

    print(
        f"\nRun ID              : {run_id}"
    )

    print(
        f"Logged Model ID     : {logged_model_id}"
    )

    print(
        f"Registered Model    : "
        f"{MLFLOW_REGISTERED_MODEL_NAME}"
    )

    # CREATE MODEL URI USING LOGGED MODEL ID

    model_uri = (
        f"models:/{logged_model_id}"
    )

    print(
        f"Model URI           : {model_uri}"
    )

    # REGISTER LOGGED MODEL

    print(
        "\nRegistering MLflow Logged Model..."
    )

    model_version = (
        mlflow.register_model(
            model_uri=model_uri,
            name=MLFLOW_REGISTERED_MODEL_NAME,
        )
    )

    version = int(
        model_version.version
    )

    # DISPLAY REGISTRATION RESULT

    print(
        "\nModel registered successfully."
    )

    print(
        f"Registered Model    : "
        f"{MLFLOW_REGISTERED_MODEL_NAME}"
    )

    print(
        f"Model Version       : "
        f"{version}"
    )

    print(
        f"Logged Model ID     : "
        f"{logged_model_id}"
    )

    print(
        f"F1 Score            : "
        f"{metrics['f1_score']:.4f}"
    )

    return version


# SET CHAMPION ALIAS

def set_champion_alias(
    model_version: int,
):
    """
    Assign the 'champion' alias to the selected
    model version.
    """

    print(
        "\n" + "=" * 60
    )

    print(
        "SETTING CHAMPION MODEL ALIAS"
    )

    print(
        "=" * 60
    )

    client = MlflowClient(
        tracking_uri=MLFLOW_TRACKING_URI
    )

    # SET ALIAS

    client.set_registered_model_alias(
        name=MLFLOW_REGISTERED_MODEL_NAME,
        alias=MLFLOW_MODEL_ALIAS,
        version=model_version,
    )

    # DISPLAY RESULT

    print(
        f"\nRegistered Model : "
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


# TRAIN LOGISTIC REGRESSION

def train_logistic_regression(
    X_train,
    X_test,
    y_train,
    y_test,
):
    """
    Train and log Logistic Regression model.

    Returns:
        model
        evaluation results
        run ID
        logged model ID
    """

    print(
        "\n" + "-" * 60
    )

    print(
        "TRAINING LOGISTIC REGRESSION"
    )

    print(
        "-" * 60
    )

    params = {
        "model_type": "LogisticRegression",
        "max_iter": 1000,
        "random_state": 42,
        "test_size": 0.2,
    }

    with mlflow.start_run(
        run_name="logistic-regression"
    ) as run:

        # CREATE MODEL

        model = LogisticRegression(
            max_iter=1000,
            random_state=42,
        )

        # TRAIN MODEL

        model.fit(
            X_train,
            y_train,
        )

        print(
            "Logistic Regression training completed."
        )

        # EVALUATE MODEL

        results = evaluate_model(
            model,
            X_test,
            y_test,
            "Logistic Regression",
        )

        # LOG PARAMETERS

        mlflow.log_params(
            params
        )

        # LOG METRICS

        mlflow.log_metrics(
            results
        )

        # LOG METADATA

        mlflow.set_tag(
            "model_type",
            "LogisticRegression",
        )

        mlflow.set_tag(
            "training_stage",
            "model_comparison",
        )

        mlflow.set_tag(
            "framework",
            "scikit-learn",
        )

        # LOG MODEL
        #
        # MLflow 3.x:
        # Use name instead of deprecated artifact_path.

        logged_model = (
            mlflow.sklearn.log_model(
                sk_model=model,
                name="logistic-regression-model",
            )
        )

        # GET RUN ID

        run_id = (
            run.info.run_id
        )

        # GET LOGGED MODEL ID

        logged_model_id = (
            logged_model.model_id
        )

        # DISPLAY RESULT

        print(
            "\nLogistic Regression model logged successfully."
        )

        print(
            f"Run ID            : {run_id}"
        )

        print(
            f"Logged Model ID   : {logged_model_id}"
        )

        print(
            "Logged Model Name : "
            "logistic-regression-model"
        )

    return (
        model,
        results,
        run_id,
        logged_model_id,
    )


# TRAIN RANDOM FOREST

def train_random_forest(
    X_train,
    X_test,
    y_train,
    y_test,
):
    """
    Train and log Random Forest model.

    Returns:
        model
        evaluation results
        run ID
        logged model ID
    """

    print(
        "\n" + "-" * 60
    )

    print(
        "TRAINING RANDOM FOREST"
    )

    print(
        "-" * 60
    )

    params = {
        "model_type": "RandomForestClassifier",
        "n_estimators": 100,
        "random_state": 42,
        "class_weight": "balanced",
        "n_jobs": -1,
        "test_size": 0.2,
    }

    with mlflow.start_run(
        run_name="random-forest"
    ) as run:

        # CREATE MODEL

        model = RandomForestClassifier(
            n_estimators=100,
            random_state=42,
            class_weight="balanced",
            n_jobs=-1,
        )

        # TRAIN MODEL

        model.fit(
            X_train,
            y_train,
        )

        print(
            "Random Forest training completed."
        )

        # EVALUATE MODEL

        results = evaluate_model(
            model,
            X_test,
            y_test,
            "Random Forest",
        )

        # LOG PARAMETERS

        mlflow.log_params(
            params
        )

        # LOG METRICS

        mlflow.log_metrics(
            results
        )

        # LOG METADATA

        mlflow.set_tag(
            "model_type",
            "RandomForestClassifier",
        )

        mlflow.set_tag(
            "training_stage",
            "model_comparison",
        )

        mlflow.set_tag(
            "framework",
            "scikit-learn",
        )

        # LOG MODEL
        #
        # MLflow 3.x:
        # Use name instead of deprecated artifact_path.

        logged_model = (
            mlflow.sklearn.log_model(
                sk_model=model,
                name="random-forest-model",
            )
        )

        # GET RUN ID

        run_id = (
            run.info.run_id
        )

        # GET LOGGED MODEL ID

        logged_model_id = (
            logged_model.model_id
        )

        # DISPLAY RESULT

        print(
            "\nRandom Forest model logged successfully."
        )

        print(
            f"Run ID            : {run_id}"
        )

        print(
            f"Logged Model ID   : {logged_model_id}"
        )

        print(
            "Logged Model Name : "
            "random-forest-model"
        )

    return (
        model,
        results,
        run_id,
        logged_model_id,
    )


# MAIN TRAINING PIPELINE

def main():

    print(
        "=" * 60
    )

    print(
        "REAL-TIME FRAUD DETECTION"
    )

    print(
        "MLFLOW TRAINING & MODEL REGISTRY PIPELINE"
    )

    print(
        "=" * 60
    )

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

    print(
        f"Champion alias      : "
        f"@{MLFLOW_MODEL_ALIAS}"
    )

    # STEP 2: LOAD DATA

    print(
        "\nLoading dataset..."
    )

    df = load_data()

    print(
        "Dataset loaded successfully."
    )

    print(
        f"Dataset shape: {df.shape}"
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
        scaler,
    ) = preprocess_data(
        df
    )

    print(
        "Data preprocessing completed successfully."
    )

    print(
        f"Training features shape : "
        f"{X_train.shape}"
    )

    print(
        f"Testing features shape  : "
        f"{X_test.shape}"
    )

    # STEP 4: TRAIN LOGISTIC REGRESSION

    (
        logistic_model,
        logistic_results,
        logistic_run_id,
        logistic_logged_model_id,
    ) = train_logistic_regression(
        X_train,
        X_test,
        y_train,
        y_test,
    )

    # STEP 5: TRAIN RANDOM FOREST

    (
        random_forest_model,
        random_forest_results,
        random_forest_run_id,
        random_forest_logged_model_id,
    ) = train_random_forest(
        X_train,
        X_test,
        y_train,
        y_test,
    )

    # STEP 6: MODEL COMPARISON

    print(
        "\n" + "=" * 60
    )

    print(
        "MODEL COMPARISON"
    )

    print(
        "=" * 60
    )

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

        best_logged_model_id = (
            random_forest_logged_model_id
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

        best_logged_model_id = (
            logistic_logged_model_id
        )

    # DISPLAY BEST MODEL

    print(
        "\n" + "=" * 60
    )

    print(
        "BEST MODEL SELECTED"
    )

    print(
        "=" * 60
    )

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

    print(
        f"Logged Model ID : "
        f"{best_logged_model_id}"
    )

    # STEP 8: REGISTER BEST MODEL

    best_model_version = (
        register_model_version(
            run_id=best_run_id,
            logged_model_id=best_logged_model_id,
            metrics=best_results,
        )
    )

    # STEP 9: SET CHAMPION ALIAS

    set_champion_alias(
        best_model_version
    )

    # STEP 10: CREATE LOCAL MODELS DIRECTORY

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    # STEP 11: SAVE BEST MODEL LOCALLY

    joblib.dump(
        best_model,
        MODEL_PATH,
    )

    print(
        f"\nLocal model saved to:"
        f"\n{MODEL_PATH}"
    )

    # STEP 12: SAVE SCALER

    joblib.dump(
        scaler,
        SCALER_PATH,
    )

    print(
        f"Scaler saved to:"
        f"\n{SCALER_PATH}"
    )

    # STEP 13: FINAL OUTPUT

    print(
        "\n" + "=" * 60
    )

    print(
        "MODEL REGISTRY PIPELINE COMPLETED"
    )

    print(
        "=" * 60
    )

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


# RUN TRAINING PIPELINE

if __name__ == "__main__":

    main()