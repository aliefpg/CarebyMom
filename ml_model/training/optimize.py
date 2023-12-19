import pandas as pd
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import learning_curve

# Load dataset
df = pd.read_csv(
    "/home/tinapyp/Development/CarebyMom/ml_model/app/data/datagenerated.csv", sep=","
)

# Drop duplicated rows
df = df.drop_duplicates()

# Mapping label 'Risk' to numeric values
Risk = {"Normal": 0, "High": 1}
df["Risk"] = df["Risk"].map(Risk).astype(float)

# Split dataset
X = df.drop("Risk", axis=1)
y = df["Risk"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42
)

# Define ColumnTransformer with StandardScaler
numeric_features = X.columns
preprocessor = StandardScaler()

# Transform data
X_train_transformed = preprocessor.fit_transform(X_train)
X_test_transformed = preprocessor.transform(X_test)

# Hyperparameter Tuning with GridSearchCV
param_grid = {
    "n_estimators": [50, 100, 150, 200, 250],
    "max_depth": [8, 10, 12, 15, 20],
    "min_samples_split": [3, 5, 7, 10, 15],
    "min_samples_leaf": [2, 4, 6, 8, 10, 12],
}

rf_model = RandomForestClassifier()

grid_search = GridSearchCV(rf_model, param_grid, cv=5, scoring="accuracy", n_jobs=-1)
grid_search.fit(X_train_transformed, y_train)

best_params = grid_search.best_params_

# Print the new best hyperparameters
print("Updated Best Hyperparameters:")
print(best_params)

# Train model with updated best parameters
best_rf_model = RandomForestClassifier(**best_params)
best_rf_model.fit(X_train_transformed, y_train)

# Print training score and cross-validation score
training_score = best_rf_model.score(X_train_transformed, y_train)
validation_score = grid_search.best_score_

print(f"Training Score: {training_score:.4f}")
print(f"Cross-Validation Score: {validation_score:.4f}")

# Plot updated learning curve
train_sizes, train_scores, test_scores = learning_curve(
    best_rf_model, X_train_transformed, y_train, cv=5, scoring="accuracy", n_jobs=-1
)

train_scores_mean = train_scores.mean(axis=1)
train_scores_std = train_scores.std(axis=1)
test_scores_mean = test_scores.mean(axis=1)
test_scores_std = test_scores.std(axis=1)

# Plotting the updated learning curve
plt.figure(figsize=(10, 6))
plt.fill_between(
    train_sizes,
    train_scores_mean - train_scores_std,
    train_scores_mean + train_scores_std,
    alpha=0.1,
    color="blue",
)
plt.fill_between(
    train_sizes,
    test_scores_mean - test_scores_std,
    test_scores_mean + test_scores_std,
    alpha=0.1,
    color="orange",
)
plt.plot(train_sizes, train_scores_mean, "o-", color="blue", label="Training score")
plt.plot(
    train_sizes, test_scores_mean, "o-", color="orange", label="Cross-validation score"
)
plt.xlabel("Training examples")
plt.ylabel("Score")
plt.legend(loc="best")
plt.title("Updated Learning Curve with Hyperparameter Tuning")
plt.show()
