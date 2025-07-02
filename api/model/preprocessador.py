from sklearn.model_selection import train_test_split
import pickle
import numpy as np

class PreProcessador:

    def __init__(self):
        """Inicializa o preprocessador"""
        pass

    def separa_teste_treino(self, dataset, percentual_teste, seed=7):
        """ Cuida de todo o pré-processamento. """
        # limpeza dos dados e eliminação de outliers

        # feature selection

        # divisão em treino e teste
        X_train, X_test, Y_train, Y_test = self.__preparar_holdout(dataset,
                                                                  percentual_teste,
                                                                  seed)
        # normalização/padronização
        
        return (X_train, X_test, Y_train, Y_test)
    
    def __preparar_holdout(self, dataset, percentual_teste, seed):
        """ Divide os dados em treino e teste usando o método holdout.
        Assume que a variável target está na última coluna.
        O parâmetro test_size é o percentual de dados de teste.
        """
        dados = dataset.values
        X = dados[:, 0:-1]
        Y = dados[:, -1]
        return train_test_split(X, Y, test_size=percentual_teste, random_state=seed)
    
    def preparar_form(self,form):
    # Transformar os dados do formulário em array para predição
        X_input = pd.DataFrame([{
            "person_age": form.person_age,
            "person_gender": form.person_gender,
            "person_education": form.person_education,
            "person_income": form.person_income,
            "person_emp_exp": form.person_emp_exp,
            "person_home_ownership": form.person_home_ownership,
            "loan_amnt": form.loan_amnt,
            "loan_intent": form.loan_intent,
            "loan_int_rate": form.loan_int_rate,
            "loan_percent_income": form.loan_percent_income,
            "cb_person_cred_hist_length": form.cb_person_cred_hist_length,
            "credit_score": form.credit_score,
            "previous_loan_defaults_on_file": form.previous_loan_defaults_on_file
}])

        return X_input
 
    def scaler(self, X_train):
        """ Normaliza os dados. """
        # normalização/padronização
        scaler = pickle.load(open('./MachineLearning/scalers/minmax_scaler_diabetes.pkl', 'rb'))
        reescaled_X_train = scaler.transform(X_train)
        return reescaled_X_train
