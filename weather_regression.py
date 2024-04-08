import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import r2_score
from sklearn.metrics import mean_squared_error
import numpy as np

df = pd.read_excel('universities_with_weather_data.xlsx').dropna()
# rename col to make names clearer
df = df.rename(columns={'sfcWind': 'wind speed', 'tas': 'surface temperature', 
                        'snowLying' : 'snow lying', 'hurs' : 'humidity'})

# define predictors and response variable
# run without hurs becausw it causes multicollinearity
X = df[['latitude', 'longitude', 'rainfall', 'sun', 'wind speed', 'surface temperature',
        'snow lying', 'groundfrost']]
y = df['Positivity measure (%)']

# split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# reset indices to ensure alignment
X_train = X_train.reset_index(drop=True)
y_train = y_train.reset_index(drop=True)
X_test = X_test.reset_index(drop=True)
y_test = y_test.reset_index(drop=True)

# standardise the features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# convert the scaled arrays back to dfs and add the feature names
X_train_scaled_df = pd.DataFrame(X_train_scaled, columns=X.columns)
X_test_scaled_df = pd.DataFrame(X_test_scaled, columns=X.columns)

# add a constant to the predictors
X_train_vif = sm.add_constant(X_train_scaled_df)
X_test_vif = sm.add_constant(X_test_scaled_df)

# calculate VIF
vif_data = pd.DataFrame()
vif_data['feature'] = X_train_vif.columns
vif_data['VIF'] = [variance_inflation_factor(X_train_vif.values, i) for i in range(X_train_vif.shape[1])]

# check for multicollinearity
if vif_data.loc[vif_data['feature'] != 'const', 'VIF'].max() <= 10:
    print("\nMulticollinearity check passed. Proceeding with regression model.")

    # create and fit the OLS model on the training set
    model = sm.OLS(y_train, X_train_vif).fit()

    y_pred = model.predict(X_test_vif)
    mae = mean_absolute_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"\nR^2 on Test Set: {r2}")
    print(f"Mean Absolute Error on Test Set: {mae}")
    print(f"RMSE on Test Set: {rmse}")

    # print summary of the regression
    print("\nOLS Regression Model Summary:")
    print(model.summary())
else:
    print('Data too collinear.')