import pandas as pd


def process_coefficients(coefficients):
    # Преобразуем данные в DataFrame
    df = pd.DataFrame(coefficients)

    # Убедимся, что работаем только с существующими колонками
    necessary_columns = ['date', 'coefficient', 'warehouseID', 'warehouseName', 'boxTypeName', 'boxTypeID']
    existing_columns = [col for col in necessary_columns if col in df.columns]

    # Возвращаем DataFrame только с нужными колонками
    return df[existing_columns]
