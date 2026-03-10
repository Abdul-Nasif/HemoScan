
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler, RobustScaler, LabelEncoder, OneHotEncoder
data = "anemia.csv"
df = pd.read_csv(data)
def explore_data(df):
    """
    Input: Raw DataFrame
    Output: Dictionary with data info
    """
    return {
        'shape': df.shape,
        'columns': df.columns.tolist(),
        'dtypes': df.dtypes.to_dict(),
        'missing_values': df.isnull().sum().to_dict(),
        'basic_stats': df.describe().to_dict(),
        'sample_data': df.head()
    }



#  Handling Missing Values
def handle_missing_values(df, strategy='mean', columns=None):
    """
    Input: DataFrame with missing values
    Output: DataFrame with imputed values
    """
    df_clean = df.copy()
    if columns is None:
        columns = df.columns[df.isnull().any()].tolist()
    
    for col in columns:
        if df[col].dtype in ['int64', 'float64']:
            if strategy == 'mean':
                df_clean[col].fillna(df[col].mean(), inplace=True)
            elif strategy == 'median':
                df_clean[col].fillna(df[col].median(), inplace=True)
            elif strategy == 'mode':
                df_clean[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df_clean[col].fillna(df[col].mode()[0], inplace=True)
    
    return df_clean




# Encoding Categorical Variables
def encode_categorical(df, encoding_type='onehot', columns=None):
    """
    Input: DataFrame with categorical columns
    Output: Encoded DataFrame + encoder object
    """
    from sklearn.preprocessing import LabelEncoder, OneHotEncoder
    
    df_encoded = df.copy()
    encoders = {}
    
    if columns is None:
        columns = df.select_dtypes(include=['object']).columns
    
    if encoding_type == 'label':
        for col in columns:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df[col])
            encoders[col] = le
    
    elif encoding_type == 'onehot':
        df_encoded = pd.get_dummies(df, columns=columns, prefix=columns)
    
    return df_encoded, encoders


# Feature Scaling
def scale_features(x, y, scaling_type='standard'):
    
    import pandas as pd
    from sklearn.preprocessing import StandardScaler
    import pickle

    # Load dataset
    data = pd.read_csv("anemia.csv")

    # Separate features and target
    X = data.drop("Result", axis=1)
    y = data["Result"]

    # Columns to scale
    scale_columns = ["Hemoglobin", "MCH", "MCHC", "MCV"]

    # Create scaler
    scaler = StandardScaler()

    # Scale selected columns
    X[scale_columns] = scaler.fit_transform(X[scale_columns])

    # Combine scaled features and target
    scaled_data = pd.concat([X, y], axis=1)

    # Save scaled dataset
    scaled_data.to_csv("anemia_scaled.csv", index=False)

    # Save scaler for future predictions
    with open("scaler.pkl", "wb") as f:
        pickle.dump(scaler, f)

    print("✅ Scaled dataset saved as anemia_scaled.csv")
    print("✅ Scaler saved as scaler.pkl")

    print("\nPreview of scaled data:")
    print(scaled_data.head())
    
    return X, y, scaler

# Outlier Detection & Handling
def handle_outliers(df, method='iqr', threshold=1.5):
    """
    Input: DataFrame
    Output: DataFrame with outliers handled + outlier indices
    """
    df_clean = df.copy()
    outlier_indices = []
    
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    if method == 'iqr':
        for col in numeric_cols:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - threshold * IQR
            upper_bound = Q3 + threshold * IQR
            
            # Cap outliers
            df_clean[col] = df[col].clip(lower_bound, upper_bound)
            
            # Record outlier indices
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)].index
            outlier_indices.extend(outliers)
    
    return df_clean, list(set(outlier_indices))

# Feature Engineering
def create_features(df):
    """
    Input: DataFrame
    Output: DataFrame with new engineered features
    """
    df_new = df.copy()
    
    # Example: Create interaction features
    numeric_cols = df.select_dtypes(include=['int64', 'float64']).columns
    
    for i in range(len(numeric_cols)):
        for j in range(i+1, len(numeric_cols)):
            col1, col2 = numeric_cols[i], numeric_cols[j]
            df_new[f'{col1}_x_{col2}'] = df[col1] * df[col2]
    
    # Example: Binning
    if 'age' in df.columns:
        df_new['age_group'] = pd.cut(df['age'], 
                                     bins=[0, 18, 35, 50, 65, 100],
                                     labels=['child', 'young', 'adult', 'middle', 'senior'])
    
    return df_new

# Complete Preprocessing Pipeline
def preprocessing_pipeline(df, target_column=None):
    """
    Input: Raw DataFrame
    Output: Preprocessed DataFrame + preprocessing info
    """
    import pandas as pd
    import numpy as np
    from sklearn.model_selection import train_test_split
    from sklearn.preprocessing import StandardScaler, MinMaxScaler
    
    preprocessing_info = {
        'original_shape': df.shape,
        'steps_applied': []
    }
    
    # Make a copy
    df_clean = df.copy()
    
    # Step 1: Remove duplicates
    df_clean = df_clean.drop_duplicates()
    preprocessing_info['steps_applied'].append('duplicates_removed')
    
    # Step 2: Handle missing values
    df_clean = handle_missing_values(df_clean, strategy='median')
    preprocessing_info['steps_applied'].append('missing_values_handled')
    
    # Step 3: Encode categorical variables
    categorical_cols = df_clean.select_dtypes(include=['object']).columns
    if len(categorical_cols) > 0:
        df_clean, encoders = encode_categorical(df_clean, 'onehot', categorical_cols)
        preprocessing_info['encoders'] = encoders
        preprocessing_info['steps_applied'].append('categorical_encoded')
    
    # Step 4: Handle outliers
    df_clean, outlier_idx = handle_outliers(df_clean)
    preprocessing_info['outlier_indices'] = outlier_idx
    preprocessing_info['steps_applied'].append('outliers_handled')
    
    # Step 5: Split features and target if specified
    if target_column and target_column in df_clean.columns:
        X = df_clean.drop(columns=[target_column])
        y = df_clean[target_column]
        preprocessing_info['target_column'] = target_column
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # FIXED: Identify binary and non-binary columns
        binary_cols = []
        continuous_cols = []
        
        for col in X_train.columns:
            # Check if column is binary (only 0 and 1 values)
            unique_values = X_train[col].dropna().unique()
            if set(unique_values).issubset({0, 1}) and len(unique_values) <= 2:
                binary_cols.append(col)
            else:
                continuous_cols.append(col)
        
        preprocessing_info['binary_columns'] = binary_cols
        preprocessing_info['continuous_columns'] = continuous_cols
        
        # Step 6: Scale ONLY continuous columns (NOT binary)
        if len(continuous_cols) > 0:
            scaler = StandardScaler()
            # Scale only continuous columns
            X_train_continuous_scaled = scaler.fit_transform(X_train[continuous_cols])
            X_test_continuous_scaled = scaler.transform(X_test[continuous_cols])
            
            # Convert back to DataFrames
            X_train_continuous = pd.DataFrame(
                X_train_continuous_scaled,
                columns=continuous_cols,
                index=X_train.index
            )
            X_test_continuous = pd.DataFrame(
                X_test_continuous_scaled,
                columns=continuous_cols,
                index=X_test.index
            )
            
            # Combine with binary columns (which remain UNCHANGED)
            X_train_scaled = pd.concat([
                X_train_continuous,
                X_train[binary_cols]
            ], axis=1)
            
            X_test_scaled = pd.concat([
                X_test_continuous,
                X_test[binary_cols]
            ], axis=1)
            
            # Restore original column order
            X_train_scaled = X_train_scaled[X_train.columns]
            X_test_scaled = X_test_scaled[X_test.columns]
            
            preprocessing_info['scaler'] = scaler
            preprocessing_info['steps_applied'].append('features_scaled')
        else:
            X_train_scaled = X_train
            X_test_scaled = X_test
        
        return {
            'X_train': X_train_scaled,
            'X_test': X_test_scaled,
            'y_train': y_train,
            'y_test': y_test,
            'preprocessing_info': preprocessing_info
        }
    
    # FIXED: For when there's no target column
    else:
        # Identify binary and non-binary columns
        binary_cols = []
        continuous_cols = []
        
        for col in df_clean.columns:
            if df_clean[col].dtype in ['int64', 'float64']:
                unique_values = df_clean[col].dropna().unique()
                if set(unique_values).issubset({0, 1}) and len(unique_values) <= 2:
                    binary_cols.append(col)
                else:
                    continuous_cols.append(col)
        
        # Scale ONLY continuous columns
        if len(continuous_cols) > 0:
            scaler = StandardScaler()
            df_clean[continuous_cols] = scaler.fit_transform(df_clean[continuous_cols])
            preprocessing_info['scaler'] = scaler
            preprocessing_info['steps_applied'].append('features_scaled')
        
        preprocessing_info['binary_columns'] = binary_cols
        preprocessing_info['continuous_columns'] = continuous_cols
    
    preprocessing_info['final_shape'] = df_clean.shape
    return df_clean, preprocessing_info

def validate_preprocessed_data(df, original_info):
    """
    Input: Preprocessed DataFrame, original data info
    Output: Validation report
    """
    validation_report = {
        'missing_values_check': df.isnull().sum().sum() == 0,
        'data_types_consistent': True,
        'no_infinite_values': np.isfinite(df.select_dtypes(include=[np.number])).all().all(),
        'shape_changed': original_info['shape'] != df.shape,
        'memory_usage': df.memory_usage(deep=True).sum() / 1024**2  # MB
    }
    
    return validation_report


# runnig the pipeline


def run_complete_pipeline(df, target_column=None):
    """
    Complete preprocessing pipeline - FIXED: Preserves binary columns (0/1)
    """
    print("="*50)
    print("STARTING PREPROCESSING PIPELINE")
    print("="*50)
    
    # Step 1: Explore
    print("\n1. EXPLORING DATA...")
    print(f"Original shape: {df.shape}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    
    # Step 2: Handle missing values
    print("\n2. HANDLING MISSING VALUES...")
    df_clean = handle_missing_values(df, strategy='median')
    print(f"Missing values after cleaning: {df_clean.isnull().sum().sum()}")
    
    # Step 3: Encode categorical variables
    print("\n3. ENCODING CATEGORICAL VARIABLES...")
    categorical_cols = df_clean.select_dtypes(include=['object']).columns.tolist()
    df_encoded = df_clean.copy()
    
    if categorical_cols:
        print(f"Categorical columns found: {categorical_cols}")
        # Use label encoding instead of onehot to maintain single column
        for col in categorical_cols:
            le = LabelEncoder()
            df_encoded[col] = le.fit_transform(df_encoded[col].astype(str))
            print(f"   Encoded {col}: {dict(zip(le.classes_, le.transform(le.classes_)))}")
    else:
        print("No categorical columns found")
    
    # Step 4: Handle outliers (capping, not scaling)
    print("\n4. HANDLING OUTLIERS...")
    df_no_outliers, outliers = handle_outliers(df_encoded)
    print(f"Outliers handled: {len(outliers)} rows affected")
    
    # Step 5: Prepare for modeling
    if target_column and target_column in df_no_outliers.columns:
        print(f"\n5. PREPARING FOR MODELING WITH TARGET: {target_column}")
        X = df_no_outliers.drop(columns=[target_column])
        y = df_no_outliers[target_column]
        
        # IDENTIFY BINARY COLUMNS (including gender)
        binary_cols = []
        continuous_cols = []
        
        for col in X.columns:
            # Check if column contains only 0 and 1
            unique_vals = X[col].dropna().unique()
            if set(unique_vals).issubset({0, 1}) and len(unique_vals) <= 2:
                binary_cols.append(col)
            else:
                continuous_cols.append(col)
        
        print(f"\n📊 Column Classification:")
        print(f"   Binary columns (will NOT be scaled): {binary_cols}")
        print(f"   Continuous columns (will be scaled): {continuous_cols}")
        
        # Split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, 
            stratify=y if len(y.unique()) < 10 else None
        )
        
        # Scale ONLY continuous columns
        if len(continuous_cols) > 0:
            scaler = StandardScaler()
            
            # Fit and transform on continuous columns only
            X_train_continuous = scaler.fit_transform(X_train[continuous_cols])
            X_test_continuous = scaler.transform(X_test[continuous_cols])
            
            # Convert back to DataFrames
            X_train_continuous_df = pd.DataFrame(
                X_train_continuous,
                columns=continuous_cols,
                index=X_train.index
            )
            X_test_continuous_df = pd.DataFrame(
                X_test_continuous,
                columns=continuous_cols,
                index=X_test.index
            )
            
            # Combine with binary columns (UNSCALED)
            X_train_final = pd.concat([X_train_continuous_df, X_train[binary_cols]], axis=1)
            X_test_final = pd.concat([X_test_continuous_df, X_test[binary_cols]], axis=1)
            
            # Restore original column order
            X_train_final = X_train_final[X.columns]
            X_test_final = X_test_final[X.columns]
            
            print(f"\n✅ Scaling complete:")
            print(f"   Scaled columns: {continuous_cols}")
            print(f"   Preserved binary columns: {binary_cols}")
            
        else:
            # No continuous columns to scale
            X_train_final = X_train
            X_test_final = X_test
            scaler = None
            print("\n✅ No continuous columns to scale")
        
        # VERIFICATION - Check gender column
        gender_cols = [col for col in X_train_final.columns if 'gender' in col.lower()]
        if gender_cols:
            for col in gender_cols:
                print(f"\n🔍 VERIFICATION - {col} values:")
                print(f"   Train unique values: {sorted(X_train_final[col].unique())}")
                print(f"   Test unique values: {sorted(X_test_final[col].unique())}")
                print(f"   ✓ Column preserved as binary (0/1) - NOT SCALED")
        
        print(f"\nFinal training set shape: {X_train_final.shape}")
        print(f"Final test set shape: {X_test_final.shape}")
        
        # Save preprocessed data WITHOUT scaling for reference
        df_no_outliers.to_csv('preprocessed_data_before_scaling.csv', index=False)
        print("✅ Preprocessed data (before scaling) saved to 'preprocessed_data_before_scaling.csv'")
        
        return {
            'X_train': X_train_final,      # Scaled continuous + unscaled binary
            'X_test': X_test_final,         # Scaled continuous + unscaled binary
            'y_train': y_train,
            'y_test': y_test,
            'scaler': scaler,                # Scaler for continuous columns only
            'preprocessed_data': df_no_outliers,  # Complete data before scaling
            'binary_columns': binary_cols,
            'continuous_columns': continuous_cols,
            'column_types': {
                'binary': binary_cols,
                'continuous': continuous_cols
            }
        }
    else:
        print("\n5. IDENTIFYING COLUMN TYPES...")
        
        # Identify binary and continuous columns
        binary_cols = []
        continuous_cols = []
        
        for col in df_no_outliers.select_dtypes(include=['int64', 'float64']).columns:
            unique_vals = df_no_outliers[col].dropna().unique()
            if set(unique_vals).issubset({0, 1}) and len(unique_vals) <= 2:
                binary_cols.append(col)
            else:
                continuous_cols.append(col)
        
        print(f"\n📊 Column Classification:")
        print(f"   Binary columns (will NOT be scaled): {binary_cols}")
        print(f"   Continuous columns (will be scaled): {continuous_cols}")
        
        # Scale ONLY continuous columns
        df_final = df_no_outliers.copy()
        
        if len(continuous_cols) > 0:
            scaler = StandardScaler()
            df_final[continuous_cols] = scaler.fit_transform(df_final[continuous_cols])
            print(f"\n✅ Scaled columns: {continuous_cols}")
        else:
            scaler = None
            print("\n✅ No continuous columns to scale")
        
        print(f"\nBinary columns preserved (0/1 unchanged): {binary_cols}")
        
        # VERIFICATION
        gender_cols = [col for col in binary_cols if 'gender' in col.lower()]
        if gender_cols:
            for col in gender_cols:
                print(f"\n🔍 VERIFICATION - {col} values:")
                print(f"   Unique values: {sorted(df_final[col].unique())}")
                print(f"   ✓ Column preserved as binary (0/1) - NOT SCALED")
        
        print(f"\nFinal preprocessed shape: {df_final.shape}")
        
        return {
            'preprocessed_data': df_final,
            'scaler': scaler,
            'binary_columns': binary_cols,
            'continuous_columns': continuous_cols
        }

# RUN THE PIPELINE
if __name__ == "__main__":
    # Load your data
    data = "anemia.csv"  # Update with your actual file
    df = pd.read_csv(data)
    
    # Run the pipeline with your target column
    # Replace 'Result' with your actual target column name
    result = run_complete_pipeline(df, target_column='Result')  # or 'purchased' whatever your target is
    
    # Access the results
    if 'X_train' in result:
        X_train = result['X_train']
        X_test = result['X_test']
        y_train = result['y_train']
        y_test = result['y_test']
        
        print("\n" + "="*50)
        print("✅ PIPELINE COMPLETED SUCCESSFULLY")
        print("="*50)
        print(f"\nTraining features shape: {X_train.shape}")
        print(f"Test features shape: {X_test.shape}")
        
        # Save the processed data
        X_train.to_csv('X_train_processed.csv', index=False)
        X_test.to_csv('X_test_processed.csv', index=False)
        pd.DataFrame(y_train).to_csv('y_train.csv', index=False)
        pd.DataFrame(y_test).to_csv('y_test.csv', index=False)
        
        # Save the scaler for future use
        if result['scaler']:
            import joblib
            joblib.dump(result['scaler'], 'scaler.pkl')
            print("✅ Scaler saved to 'scaler.pkl' (for continuous columns only)")
        
        print("\n📁 Files saved:")
        print("   - X_train_processed.csv")
        print("   - X_test_processed.csv")
        print("   - y_train.csv")
        print("   - y_test.csv")
        print("   - preprocessed_data_before_scaling.csv")
    else:
        df_processed = result['preprocessed_data']
        df_processed.to_csv('processed_data.csv', index=False)
        print("✅ Processed data saved to 'processed_data.csv'")