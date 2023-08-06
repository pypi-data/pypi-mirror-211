def univar_dis(train_df,collist):
 """plot distribution for a fea list in df.
 Detailed explanation 
 Args:  
     df: train in dataframe
     collist: ['fea1','fea2']
     flag: 
 Returns:
   nothing
     
 """      
 import klib
 from feature_engine.encoding import CountFrequencyEncoder,OrdinalEncoder
 from feature_engine.discretisation import EqualWidthDiscretiser
 from feature_engine.imputation import DropMissingData
 df=train_df
 num_list = df[collist].select_dtypes([np.number]).columns.tolist()
 cat_list= [x for x in collist if x not in num_list]
 klib.dist_plot(df[num_list]) 
 r_n=math.ceil(len(cat_list)/3)
 if r_n>0:
   fig, ax =plt.subplots(figsize = (18, 6*r_n), nrows = r_n, ncols = 3)
   ax=ax.reshape(-1)
   #plot data

   imputer = DropMissingData(variables=cat_list)
   df=imputer.fit_transform(df)
   encoder = CountFrequencyEncoder(variables=cat_list)
   df1=encoder.fit_transform(df)
   for i in range(0,len(cat_list)):
       encoder = OrdinalEncoder(variables=cat_list[i])
       df=encoder.fit_transform(df,df1[cat_list[i]])
       encoder = EqualWidthDiscretiser(bins=20,variables=cat_list[i])
       df=encoder.fit_transform(df)
       sns.countplot(x=cat_list[i], data=df,ax=ax[i])
       ax[i].axvline(x = df[cat_list[i]].quantile(.1), color = 'r', label = '10%')
       ax[i].axvline(x = df[cat_list[i]].quantile(.9), color = 'r', label = '90%')
       ax[i].legend() 
       ax[i].set_title(cat_list[i]+"("+str(train_df[cat_list[i]].nunique())+")")
   plt.show()
