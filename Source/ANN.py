import pandas as pd
import streamlit as st
import io
from keras.models import Sequential
from keras.layers import Dense
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, mean_squared_error, confusion_matrix, mean_absolute_error

def Full_ANN():

    def create_model(input_dim, first_layer_params, model_layers):
        model = Sequential()
        
        # First Layer
        if first_layer_params is not None:
            units, activation, initializer = first_layer_params
            model.add(Dense(units=units, activation=activation, kernel_initializer=initializer, input_dim=input_dim, name="dense_input"))
        
        # Subsequent Layers
        for units, activation, initializer in model_layers:
            model.add(Dense(units=units, activation=activation, kernel_initializer=initializer))
        
        return model

    def artificial_neural_network():
        if "data" not in st.session_state:
            st.session_state.data = None
        if "first_layer_params" not in st.session_state:
            st.session_state.first_layer_params = None
        if "model_layers" not in st.session_state:
            st.session_state.model_layers = []
        if "model" not in st.session_state:
            st.session_state.model = None
        if "first_layer_confirmed" not in st.session_state:
            st.session_state.first_layer_confirmed = False
        if "input_dim" not in st.session_state:
            st.session_state.input_dim = None
        if "epochs" not in st.session_state:
            st.session_state.epochs = 0
        if "y_pred" not in st.session_state:
            st.session_state.y_pred = None

        st.header("Welcome to the Aakash Smart Deep Learning Model Building ToolBox.")

        with st.container(border=True):
            st.session_state.data = st.file_uploader("Upload your data file. (Please upload a CSV file.)")

            if st.session_state.data:
                data = pd.read_csv(st.session_state.data)
                st.dataframe(data)

                # Capture the output of data.info()
                buffer = io.StringIO()
                data.info(buf=buffer)
                info_str = buffer.getvalue()

                # Display the captured info as text
                st.header("Data Information")
                st.text(info_str)

                st.dataframe(data.describe())

                X_features = st.multiselect("Select the Features you want to keep for training the machine learning", data.columns)

                if X_features:
                    X = data[X_features]

                    st.write("These are the features you have selected for training your machine learning model.")
                    st.dataframe(X)

                    y_feature = st.selectbox("Select the target variable for which you want to predict", data.columns)

                    if y_feature:
                        y = data[y_feature]

                        st.write("This is the target feature for your machine learning model.")
                        st.dataframe(y)

                        category_cols = st.multiselect("Select the features that you think are categorical. After Selecting they will be one-hot coded.", X_features)

                        for col in category_cols:
                            dummies = pd.get_dummies(data[col], prefix=col, drop_first=True)
                            X.drop([col], axis=1, inplace=True)
                            X = pd.concat([X, dummies], axis=1)

                        st.write("Your Features after One-hot encoding.")
                        st.dataframe(X)

                        st.write("It's time to break data into training and testing set.")
                        test_size = st.slider("Select the test size", 0.05, 0.9)

                        if test_size:
                            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)
                            st.session_state.input_dim = X_train.shape[1]

                            st.header("First Layer Settings")

                            if not st.session_state.first_layer_confirmed:
                                units = st.number_input("Units", value=64, key="first_units")
                                activation = st.selectbox("Activation Function", ["relu", "sigmoid", "softmax", "tanh", "elu", "selu", "softplus", "softsign", "linear"], key="first_activation")
                                initializer = st.selectbox("Kernel Initializer", ["glorot_uniform", "he_normal", "lecun_normal", "he_uniform", "lecun_uniform"], key="first_initializer")
                                if st.text_input("Type 'yes' to add first layer.") == "yes":
                                    st.session_state.first_layer_params = (units, activation, initializer)
                                    st.session_state.first_layer_confirmed = True

                            if st.session_state.first_layer_confirmed:
                                st.header("Add Layers to Your Neural Network")
                                units = st.number_input("Units", value=64, key=f"units_{len(st.session_state.model_layers)}")
                                activation = st.selectbox("Activation Function", ["relu", "sigmoid", "softmax", "tanh", "elu", "selu", "softplus", "softsign", "linear"], key=f"activation_{len(st.session_state.model_layers)}")
                                initializer = st.selectbox("Kernel Initializer", ["glorot_uniform", "he_normal", "lecun_normal", "he_uniform", "lecun_uniform"], key=f"initializer_{len(st.session_state.model_layers)}")
                                if st.button("Add Layer", key=f"add_layer_{len(st.session_state.model_layers)}"):
                                    st.session_state.model_layers.append((units, activation, initializer))

                            # Model Compilation
                            if st.session_state.first_layer_confirmed:
                                st.header("Compile Your Model")
                                optimizer = st.selectbox("Select Optimizer", ["adam", "sgd", "rmsprop"])
                                loss = st.selectbox("Select Loss Function", ["binary_crossentropy", "categorical_crossentropy", "mse"])
                                
                                if st.button("Compile Model"):
                                    st.session_state.model = create_model(st.session_state.input_dim, st.session_state.first_layer_params, st.session_state.model_layers)
                                    st.session_state.model.compile(optimizer=optimizer, loss=loss)
                                    st.success("Model compiled successfully!")
                                    
                                    st.markdown("### Model Summary")
                                    buffer = io.StringIO()
                                    st.session_state.model.summary(print_fn=lambda x: buffer.write(x + "\n"))
                                    st.text(buffer.getvalue())
                                    st.markdown("### Model Configuration")
                                    st.json(st.session_state.model.get_config())

                                st.session_state.epochs = int(st.text_input("Enter the number of epochs: "))

                                if st.button("Fit Training Data to model"):
                                    st.write("Training the model ....")
                                    st.session_state.model.fit(X_train, y_train, epochs = st.session_state.epochs)
                                    st.write("Training has been completed")

                                    st.session_state.y_pred = st.session_state.model.predict(X_test)

                                option = st.selectbox("Is your problem Regression or classification?", ("Choose", "Regression", "Classification"))

                                if option == "Regression":
                                    st.write(f"Mean_Squared_error: {mean_squared_error(y_test, st.session_state.y_pred)}")
                                    st.write(f"Mean Absolute Error: {mean_absolute_error(y_test, st.session_state.y_pred)}")
                                elif option == "Classification":
                                    st.session_state.y_pred = (st.session_state.y_pred > 0.5).astype(int)  # Applying threshold for classification
                                    accuracy = accuracy_score(y_test, st.session_state.y_pred)
                                    cm = confusion_matrix(y_test, st.session_state.y_pred)
                                    st.write(f"Accuracy Score: {accuracy}")
                                    st.write("Confusion Matrix:")
                                    st.write(cm)

    artificial_neural_network()
