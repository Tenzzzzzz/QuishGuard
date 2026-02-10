import pandas as pd
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report,confusion_matrix
import os


file_path = "features_processed.csv"

if not os.path.exists(file_path):
    print(f"Could not find {file_path}")
else:
    df = pd.read_csv(file_path)

    X = df.drop(columns=['url', 'label','count_dir'])
    y = df['label']
    print(f"Features being used: {list(X.columns)}")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        shuffle=True,
        random_state=42,
        stratify=y
    )

    print("Training XGBoost model...")
    model = xgb.XGBClassifier(
        subsample=0.8,
        gamma=0.1,
        reg_alpha=50,
        reg_lambda=50,
        n_estimators=1000,
        max_depth=3,
        learning_rate=0.05,
        scale_pos_weight=1,
        min_child_weight=5,
        colsample_bytree=0.8,
        random_state=42,
        eval_metric = 'aucpr'
    )


    model.fit(X_train, y_train,eval_set=[(X_test, y_test)],verbose=True)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print("-" * 30)
    print(f" Model Accuracy: {accuracy * 100:.2f}%")
    print("\nDetailed Report:")
    print(classification_report(y_test, y_pred))
    model.save_model(r"model/url_detection_model.json")
    print("\nConfusion Matrix (Look at Top Right for False Positives):")
    print(confusion_matrix(y_test, y_pred))

