import pandas as pd

from ..tbl.table import Table


class SortCols(Table):
    """Change column depths and sort values.

    If you want to change from ["img_no", "trj_no", "frm_no"] to
    ["frm_no", "img_no", "trj_no"], set new_depths = [2,3,1].

    Args:
        reqs[0] (Table): Table for sorting.
        param["new_depths"] (list of int): Target depth number of indexes.
            If list length < total columns, remaining columns are assumed
            as depth=0.
        param["split_depth"] (int): File split depth number.

    Returns:
        Table: Sorted Table
    """

    def set_info(self, param={}):
        """Copy info from reqs[0] and change depths.
        """
        self.info.copy_req(0)
        index_cols = self.info.get_column_name("index")
        if len(index_cols) != len(param["new_depths"]):
            raise Exception(
                "The number of new depths must be equal to the number\
                    of index columns in the table.")
        for depth, name in zip(param["new_depths"], index_cols):
            self.info.reset_depth(name, depth=depth)
        self.info.sort_column()
        self.info.sort_index()
        self.info.add_param("new_depths", param["new_depths"], "list of int",
                            "Target depth of index")
        self.info.set_split_depth(param["split_depth"])

    @staticmethod
    def process(reqs, param):
        """Change column depths and sort values.

        If you want to change from ["img_no", "trj_no", "frm_no"] to
        ["frm_no", "img_no", "trj_no"], set new_depths = [2,3,1].

        Args:
            reqs[0] (pandas.DataFrame): Table for sorting.
            param["new_depths"] (list of int): Target depth number of indexes.
                If list length < total columns, remaining columns are assumed
                as depth=0.

        Returns:
            pandas.DataFrame: Sorted table
        """
        df = reqs[0].copy()
        index_cols = list(df.columns[:len(param["new_depths"])])
        cols = df.columns[len(index_cols):]
        new_cols = []
        sorted_depth = sorted(set(param["new_depths"]))  # list
        if sorted_depth[0] == 0:  # This might have bug
            sorted_depth = sorted_depth[1:] + [0]

        for i in sorted_depth:
            for j, depth in enumerate(param["new_depths"]):
                if i == depth:
                    new_cols.append(index_cols[j])
        if len(cols) > 0:
            df = df[new_cols + list(cols)]
        else:
            df = df[new_cols]
        df = df.sort_values(new_cols).reset_index(drop=True)
        return df


class AddColumn(Table):
    """Add new columns with explicit values to a table.

    .. caution::

        Do not split the input table.
        TODO: col_values should have the same length as the input table.

    Args:
        reqs[0] (Table): The input table to add columns to.
        param["col_info"] (list): Information about the new column. The list
            should contain [depth, name, type, unit, description] or list of
            it.
        param["col_values"] (list): The values of the new column. The length of
            the list should be equal to the length of the "col_info" list.
        param["split_depth"] (int): The file split depth number.

    Returns:
        Table: The table with the new column.
    """

    def set_info(self, param={}):
        """Copy info from reqs[0] and add columns.
        """
        self.info.copy_req(0)
        if self.reqs[0].info.split_depth() > 0:
            raise Exception("Do not split the input table.")

        if isinstance(param["col_info"][0], list):
            names = []
            for col in param["col_info"]:
                self.info.add_column(*col)
                names.append(col[1])
        else:
            self.info.add_column(*param["col_info"])
            names = param["col_info"][1]
        self.info.add_param("col_values", param["col_values"], "list",
                            "Values of new column")
        self.info.add_param("col_name", names, "str or list",
                            "New column name")
        self.info.set_split_depth(param["split_depth"])

    @staticmethod
    def process(reqs, param):
        """Add new columns with explicit values to a table.

        Args:
            reqs[0] (pandas.DataFrame): The input table to add columns to.
            param["col_name"] (str): The names of the columns to add.
            param["col_values"] (list): The values of the new column. The
                length of the list should be equal to the length of the
                "col_name" list.

        Returns:
            pandas.DataFrame:  The table with the new column.
        """
        df = reqs[0].copy()

        if isinstance(param["col_name"], list):
            for col_name, col_values in zip(param["col_name"],
                                            param["col_values"]):
                df[col_name] = col_values
        else:
            df[param["col_name"]] = param["col_values"]
        return df


class Obs2Depth(Table):
    """Merge tables from different observations into a top level depth.

    .. caution::

        This class only works when used in a Pipeline object. Running process
        method or creating a Data object does not work appropriately.

    Observation names for merging should be listed into obs_name argument
    of :meth:`~slitflow.manager.Pipeline.add` in Pipeline class.

    Args:
        reqs (list of Table): Tables to merge.
        param["col_name"] (str, optional): New column name for observation
            numbers. Defaults to "obs_no".
        param["col_description"] (str): New column description. Defaults to
            "Observation number".
        param["obs_name"] (str): New observation name.
        param["split_depth"] (int): File split depth number.

    Returns:
        Table: Merged Table
    """

    def set_info(self, param={}):
        """Copy info from reqs[0] and add parameters.
        """
        self.info.copy_req(0)
        if "col_name" not in param:
            param["col_name"] = "obs_no"
            param["col_description"] = "Observation number"
        self.info.add_column(
            1, param["col_name"], "int32", "num", param["col_description"])
        self.info.add_param(
            "obs_name", param["obs_name"], "str", "New observation name")
        self.info.add_param(
            "col_name", param["col_name"], "str", "New column name")

        # This parameter is saved from Pipeline.run_Obs2Depth()
        self.info.add_param(
            "merged_obs_names", param["merged_obs_names"], "list of str",
            "Merged observation names for correspondence of numbers and\
                names.")
        self.info.set_split_depth(param["split_depth"])

    @staticmethod
    def process(reqs, param):
        """Merge different Observations into the top level depth.

        Args:
            reqs (list of pandas.DataFrame): Tables from different
                observations.
            param["col_name"] (str, optional): New column name for observation
                numbers.
        Returns:
            pandas.DataFrame: Merged table
        """
        cols = list(reqs[0].columns)
        dfs = []
        for i, req in enumerate(reqs):
            df = req.copy()
            df[param["col_name"]] = i + 1
            dfs.append(df)
        df_mrg = pd.concat(dfs)
        df_mrg = df_mrg.reindex(columns=[param["col_name"]] + cols)
        return df_mrg
