import stata_setup

def load_stata(df, stata_path="C:/Program Files/Stata18", stata_version="se"):
    stata_setup.config(stata_path, stata_version)
    from sfi import Data, Macro, SFIToolkit, Frame, Datetime as dt

    """
    Loads a Pandas DataFrame into a Stata data file format.

    Args:
        df (pandas.DataFrame): The DataFrame to be loaded into Stata format.

    Returns:
        pandas.DataFrame: The original DataFrame.
    """
    colnames = df.columns
    Data.setObsTotal(len(df))
    for i in range(len(colnames)):
        dtype = df.dtypes[i].name
        # make a valid Stata variable name
        varname = SFIToolkit.makeVarName(colnames[i], retainCase=True)
        # varname = colnames[i]
        varval = df.iloc[:, i].values.tolist()  # Use .iloc to access values by position
        if dtype == "int64":
            Data.addVarInt(varname)
            Data.store(varname, None, varval)
        elif dtype == "float64":
            Data.addVarDouble(varname)
            Data.store(varname, None, varval)
        elif dtype == "bool":
            Data.addVarByte(varname)
            Data.store(varname, None, varval)
        elif dtype == "datetime64[ns]":
            Data.addVarFloat(varname)
            price_dt_py = [dt.getSIF(j, '%tdCCYY-NN-DD') for j in df.iloc[:, i]]  # Use .iloc
            Data.store(varname, None, price_dt_py)
            Data.setVarFormat(varname, '%tdCCYY-NN-DD')
        else:
            # all other types store as a string
            Data.addVarStr(varname, 1)
            s = [str(i) for i in varval]
            Data.store(varname, None, s)
    return df


if __name__ == "__main__":
    pass
