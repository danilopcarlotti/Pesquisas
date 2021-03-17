from sklearn.metrics import matthews_corrcoef


def correlation(y_true, y_pred):
    return matthews_corrcoef(y_true, y_pred)


def correlation_dataframe(df, col_target, col_class="class"):
    var_class = []
    var_target = []
    for _, row in df.iterrows():
        if row[col_target] == 0:
            var_target.append(-1)
        elif row[col_target] == 1:
            var_target.append(+1)
        if row[col_target] == 0 or row[col_target] == 1:
            if row[col_class] == 0:
                var_class.append(-1)
            elif row[col_class] == 1:
                var_class.append(+1)
    return correlation(var_class, var_target)
