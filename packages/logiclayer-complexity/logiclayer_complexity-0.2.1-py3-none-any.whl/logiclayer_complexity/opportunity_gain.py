from dataclasses import dataclass, field
from typing import Optional

import economic_complexity
import pandas as pd

from .rca import RcaParameters


@dataclass
class OpportunityGainParameters:
    rca_params: RcaParameters
    cutoff: float
    rank: bool = field(default=False)
    sort_ascending: Optional[bool] = None

    def __getattr__(self, _name: str):
        return getattr(self.rca_params, _name)

    def _calculate(self, df: pd.DataFrame):
        cutoff = self.cutoff
        rank = self.rank
        sort_ascending = self.sort_ascending

        index = self.rca_params.location
        columns = self.rca_params.activity
        measure = self.rca_params.measure

        rca, _ = self.rca_params._calculate(df)

        rca[rca >= cutoff] = 1
        rca[rca < cutoff] = 0

        # Guess ID column names
        index_id = f"{index} ID"
        index_id = index_id if index_id in df.columns else index
        columns_id = f"{columns} ID"
        columns_id = columns_id if columns_id in df.columns else columns

        eci, pci = economic_complexity.complexity(rca)
        proximity = economic_complexity.proximity(rca)
        opportunity_gain = economic_complexity.opportunity_gain(rca, proximity, pci)

        def unpivot(ds: pd.DataFrame) -> pd.DataFrame:
            name = "Opportunity Gain"
            ds = ds.unstack().reset_index(name=name)

            if sort_ascending is not None:
                ds = ds.sort_values(ascending=sort_ascending)

            if rank or sort_ascending is not None:
                ds[f"{measure} {name} Ranking"] = ds[f"{measure} {name}"].rank(ascending=False)

            # restore index labels
            if index != index_id:
                df_index = df[[index_id, index]].set_index(index_id)
                dict_index = df_index[index].to_dict()
                ds[index] = ds[index_id].map(dict_index)

            # restore columns labels
            if columns != columns_id:
                df_columns = df[[columns_id, columns]].set_index(columns_id)
                dict_columns = df_columns[columns].to_dict()
                ds[columns] = ds[columns_id].map(dict_columns)

            return ds

        return opportunity_gain, unpivot

    def calculate(self, df: pd.DataFrame, *, unpivot: bool = True) -> pd.DataFrame:
        opportunity_gain, do_unpivot = self._calculate(df)

        return do_unpivot(opportunity_gain) if unpivot else opportunity_gain
