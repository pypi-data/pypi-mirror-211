# 自用
https://pypi.org/project/FeatureInsight/0.0.1/
bash scripts/upload_pypi.sh --verbose

# 如何使用？


from FeatureInsight import struct_Investigation,univar_dis,bivar_dis


EDA: Structure
summary=struct_Investigation(df)  
summary.print()
summary.sort('Unique Count')	


EDA: statistics

univar_dis(df,df.columns,mode="pie")
univar_dis(df,df.columns)
bivar_dis(df,[["Age","Drug"],["Sex","BP"],["K","Drug"]],mode="Bar")
bivar_dis(df,[["Age","Drug"],["Sex","BP"],["K","Drug"]],mode="Line")