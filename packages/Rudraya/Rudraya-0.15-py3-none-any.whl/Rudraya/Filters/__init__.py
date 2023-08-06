class Missing_value:
      def __init__(self,dataset,label):
          self.__dataset = dataset
          self.__label = label
            
      def get_missing_value_report(self):
          import pandas as pd
          import numpy as np          
          var1 = (self.__dataset.isnull().sum()/self.__dataset.isnull().sum().values.sum())*100
          self.__missing_value = pd.DataFrame({"Feature":var1.index.values,"missing_value(%)":var1.values})
          self.__missing_value = self.__missing_value.sort_values('missing_value(%)',ascending=True)
          return self.__missing_value
        
      def get_plot(self,figsize=(20,5),grid=True,threshold=0): 
            import matplotlib.pyplot as plt
            import pandas as pd
            import numpy as np

            self.__hypo = threshold
            self.__filter = self.__missing_value[self.__missing_value['missing_value(%)']>self.__hypo]
            A,B = int(figsize[0]),int(figsize[1])
            fig = plt.figure(figsize=(A,B))
            plt.bar(self.__filter.Feature.values,self.__filter['missing_value(%)'].values,label='Missing Value Filter')
            plt.xticks(rotation=90)
            plt.xlim(self.__filter.Feature.values[0],self.__filter.Feature.values[-1])
            if grid==True:
               plt.grid()
            
            plt.legend()
            plt.show()         
Missing_value.__dict__

class Multicollinearity_Filter:
    
      def __init__(self,X,allowable_collinearity):
          import warnings
          warnings.filterwarnings('ignore')
          import pandas as pd
          import numpy as np
          self.__X   = X
          self.__ac  = allowable_collinearity
        
      def internal_operation(self):       
            import pandas as pd
            import numpy as np
            from statsmodels.stats.outliers_influence import variance_inflation_factor

            vif_data = pd.DataFrame()
            raw_data = pd.DataFrame()
            
            for iteration in range(1,self.__X.shape[1]):
                vif_data = pd.DataFrame()
                vif_data["feature"] = self.__X.columns
                vif_data["VIF"] = [variance_inflation_factor(self.__X.values, i) for i in range(len(self.__X.columns))]
                vif_data['Iteration']=iteration

                VIF = vif_data[vif_data.VIF==vif_data.VIF.max()].VIF.values[0]

                if VIF>self.__ac:

                   Feature = vif_data[vif_data.VIF==vif_data.VIF.max()].feature.values[0]
                   print("{} is Feature is Eliminated".format(Feature))
 
                   self.__X = self.__X.drop(columns=['{}'.format(Feature)])


                else:
                     raw_data = raw_data.append(vif_data)
                     break

                raw_data = raw_data.append(vif_data) 
                final_data = raw_data[raw_data.Iteration==raw_data.Iteration.max()]
                final_data = final_data.sort_values('VIF',ascending=True)
                final_data['Rank']= np.arange(1,final_data.shape[0]+1)
                self.__data = final_data
            return final_data
        
      def quick_plot(self,figsize=(20,5),grid=True): 
            import matplotlib.pyplot as plt
            import pandas as pd
            import numpy as np
            A,B = int(figsize[0]),int(figsize[1])
            fig = plt.figure(figsize=(A,B))
            plt.bar(self.__data.feature.values,self.__data.VIF.values,label='Multicollinarity_Reduction')
            plt.xticks(rotation=90)
            plt.xlim(self.__data.feature.values[0],self.__data.feature.values[-1])
            if grid==True:
               plt.grid()
            
            plt.legend()
            plt.show()        

Multicollinearity_Filter.__doc__    

class Variance_filter:
      def __init__(self,details):
          self.__columns = details
        
      def get_variance_report(self,dataset):
          import pandas as pd
          import numpy as np
          data1 = np.array(dataset)
          datasets = pd.DataFrame(data1,columns=self.__columns)
          self.__features = datasets.var().index
          self.__variance = np.round(datasets.var().values,5)
          self.__percentage = (self.__variance /datasets.var().sum())*100
          self.__reports  = pd.DataFrame({"Feature":self.__features,"Variance":self.__variance,"Percent":self.__percentage})
          self.__reports  = self.__reports.sort_values('Variance',ascending=False)
          self.__reports ['Rank'] = np.arange(1,self.__reports.shape[0]+1)
      
          return self.__reports
        
      def get_filter_data(self,dataset,threshold):
          import pandas as pd
          import numpy as np
          self.__filter,self.__unfilter = self.__reports[self.__reports.Percent>threshold],self.__reports[self.__reports.Percent<=threshold]
          return self.__filter,self.__unfilter
    
      def quick_plot(self,figsize=(20,5),grid=True): 
            import matplotlib.pyplot as plt
            import pandas as pd
            import numpy as np
            A,B = int(figsize[0]),int(figsize[1])
            fig = plt.figure(figsize=(A,B))
            plt.bar(self.__filter.Feature.values,self.__filter.Variance.values,label='Variance Filter')
            plt.xticks(rotation=90)
            plt.xlim(self.__filter.Feature.values[0],self.__filter.Feature.values[-1])
            if grid==True:
               plt.grid()
            
            plt.legend()
            plt.show() 

Variance_filter.__doc__

class stats_correlation:
       def __init__(self):
           """
           method='pearson','spearman','Kendall'
           """
           pass
       def get_correlation(self,X,y,method='pearson',threshold=0.05):
           from scipy.stats import pearsonr,spearmanr,kendalltau
           import pandas as pd
           import numpy as np
           self.__X = X
           self.__y = y
           
           if self.__X.ndim>1:
                if method=='pearson':
                   pearson_value  = [pearsonr(self.__X.iloc[:,f],self.__y) for f in range(0,self.__X.shape[1])]
                   pearson_corr   = [pearson_value[f1][0] for f1 in range(0,len(pearson_value))] 
                   pearson_pvalue = [pearson_value[f2][1] for f2 in range(0,len(pearson_value))]
                
                   pearson_results=  pd.DataFrame({"Feature":self.__X.columns,"correlation":pearson_corr,
                                                   "pearson_pvalue":pearson_pvalue})
                    
                   positive_corr  = pearson_results[pearson_results.correlation==abs(pearson_results.correlation)].sort_values('correlation',ascending=False)
                   negative_corr  = pearson_results[pearson_results.correlation!=abs(pearson_results.correlation)].sort_values('correlation',ascending=True)
                   
                   absolute_results = pd.DataFrame({"Feature":self.__X.columns,"correlation":np.abs(pearson_corr),
                                                   "pearson_pvalue":pearson_pvalue})
                    
                   absolute_corr  = absolute_results[absolute_results.correlation==abs(absolute_results.correlation)].sort_values('correlation',ascending=False)
                   
                   positive_corr1 = positive_corr[positive_corr.pearson_pvalue<=threshold].sort_values('pearson_pvalue',ascending=True)
                   negative_corr1 = negative_corr[negative_corr.pearson_pvalue<=threshold].sort_values('pearson_pvalue',ascending=True)
                   absolute_corr1 = absolute_corr[absolute_corr.pearson_pvalue<=threshold].sort_values('pearson_pvalue',ascending=True)
                   
                   positive_corr1['Rank']=np.arange(1,positive_corr1.shape[0]+1)
                   negative_corr1['Rank']=np.arange(1,negative_corr1.shape[0]+1)
                   absolute_corr1['Rank']=np.arange(1,absolute_corr1.shape[0]+1)
                   self.__p = positive_corr1
                   self.__n = negative_corr1
                   self.__a = absolute_corr1
                   return positive_corr1,negative_corr1,absolute_corr1   

                if method=='spearman':
                    
                   spearman_value  = [spearmanr(self.__X.iloc[:,f],self.__y) for f in range(0,self.__X.shape[1])]
                   spearman_corr   = [spearman_value[f1][0] for f1 in range(0,len(spearman_value))] 
                   spearman_pvalue = [spearman_value[f2][1] for f2 in range(0,len(spearman_value))]
                
                   spearman_results=  pd.DataFrame({"Feature":self.__X.columns,"correlation":spearman_corr,
                                                   "spearman_pvalue":spearman_pvalue})
                    
                   positive_corr2  = spearman_results[spearman_results.correlation==abs(spearman_results.correlation)].sort_values('correlation',ascending=False)
                   negative_corr2  = spearman_results[spearman_results.correlation!=abs(spearman_results.correlation)].sort_values('correlation',ascending=True)
                   
                   absolute_results2 = pd.DataFrame({"Feature":self.__X.columns,"correlation":np.abs(spearman_corr),
                                                     "spearman_pvalue":spearman_pvalue})
                    
                   absolute_corr2 = absolute_results2[absolute_results2.correlation==abs(absolute_results2.correlation)].sort_values('correlation',ascending=False)
                   
                   positive_corr3 = positive_corr2[positive_corr2.spearman_pvalue<=threshold].sort_values('spearman_pvalue',ascending=True)
                   negative_corr3 = negative_corr2[negative_corr2.spearman_pvalue<=threshold].sort_values('spearman_pvalue',ascending=True)
                   absolute_corr3 = absolute_corr2[absolute_corr2.spearman_pvalue<=threshold].sort_values('spearman_pvalue',ascending=True)
                   
                   positive_corr3['Rank']=np.arange(1,positive_corr3.shape[0]+1)
                   negative_corr3['Rank']=np.arange(1,negative_corr3.shape[0]+1)
                   absolute_corr3['Rank']=np.arange(1,absolute_corr3.shape[0]+1)
                   self.__p = positive_corr3
                   self.__n = negative_corr3
                   self.__a = absolute_corr3                
                   return positive_corr3,negative_corr3,absolute_corr3
                
                if method=='Kendall':
                    
                   kendall_value   = [kendalltau(self.__X.iloc[:,f],self.__y) for f in range(0,self.__X.shape[1])]
                   kendall_corr    = [kendall_value[f1][0] for f1 in range(0,len(kendall_value))] 
                   kendall_pvalue  = [kendall_value[f2][1] for f2 in range(0,len(kendall_value))]
                
                   kendall_results =  pd.DataFrame({"Feature":self.__X.columns,"correlation":kendall_corr,
                                                   "kendall_pvalue":kendall_pvalue})
                    
                   positive_corr4  = kendall_results[kendall_results.correlation==abs(kendall_results.correlation)].sort_values('correlation',ascending=False)
                   negative_corr4  = kendall_results[kendall_results.correlation!=abs(kendall_results.correlation)].sort_values('correlation',ascending=True)
                   
                   absolute_results4 = pd.DataFrame({"Feature":self.__X.columns,"correlation":np.abs(kendall_corr),
                                                     "kendall_pvalue":kendall_pvalue})
                    
                   absolute_corr4 = absolute_results4[absolute_results4.correlation==abs(absolute_results4.correlation)].sort_values('correlation',ascending=False)
                   
                   positive_corr5 = positive_corr4[positive_corr4.kendall_pvalue<=threshold].sort_values('kendall_pvalue',ascending=True)
                   negative_corr5 = negative_corr4[negative_corr4.kendall_pvalue<=threshold].sort_values('kendall_pvalue',ascending=True)
                   absolute_corr5 = absolute_corr4[absolute_corr4.kendall_pvalue<=threshold].sort_values('kendall_pvalue',ascending=True)
                   
                   positive_corr5['Rank']=np.arange(1,positive_corr5.shape[0]+1)
                   negative_corr5['Rank']=np.arange(1,negative_corr5.shape[0]+1)
                   absolute_corr5['Rank']=np.arange(1,absolute_corr5.shape[0]+1)
                   self.__p = positive_corr5
                   self.__n = negative_corr5
                   self.__a = absolute_corr5                
                   return positive_corr5,negative_corr5,absolute_corr5                
                
           else:
                self.__X1 = np.array(self.__X).reshape(-1)
                self.__y = y
                
                if method=='pearson':
                    correlation1, pvalue1 = pearsonr(self.__X1,self.__y)
                    return correlation1, pvalue1
                
                if method=='spearman':
                    correlation2, pvalue2 = spearmanr(self.__X1,self.__y)
                    return correlation2, pvalue2
                    
                if method=='Kendall':
                    correlation3, pvalue3 = kendalltau(self.__X1,self.__y)
                    return correlation3, pvalue3
                    
       def quick_plot(self,figsize=(20,5),grid=True,method='positive'):
            """
            positive,negative,absolute
            """
            import matplotlib.pyplot as plt
            import pandas as pd
            import numpy as np
            if self.__X.ndim>1:
                A,B = int(figsize[0]),int(figsize[1])
                fig = plt.figure(figsize=(A,B))
                if method=='positive':
                   plt.bar(self.__p.Feature.values,self.__p.correlation.values,label='Positive Correlation')
                   plt.xticks(rotation=90)
                   plt.xlim(self.__p.Feature.values[0],self.__p.Feature.values[-1])
                
                if method=='negative':
                       plt.bar(self.__n.Feature.values,self.__n.correlation.values,label='Negative Correlation')
                       plt.xticks(rotation=90)
                       plt.xlim(self.__n.Feature.values[0],self.__n.Feature.values[-1])
                        
                if method=='absolute':
                       plt.bar(self.__a.Feature.values,self.__a.correlation.values,label='Absolute Correlation')
                       plt.xticks(rotation=90)
                       plt.xlim(self.__a.Feature.values[0],self.__a.Feature.values[-1])
                if grid==True:
                   plt.grid()
                
                plt.legend()
                plt.show()  

stats_correlation.__doc__   
   
class F_Regression:
      def __init__(self):
            pass
      def get_F_score(self,X,y,threshold=0.05):
          import pandas as pd
          import numpy as np
          from sklearn.feature_selection import f_regression
            
          self.__X = X
          self.__y = y
            
          if self.__X.ndim>1:
              values = [f_regression(np.array(self.__X.iloc[:,f]).reshape(-1,1),self.__y) for f in range(0,self.__X.shape[1])]
              f1_scores = [values[f][0][0]  for f in range(0,self.__X.shape[1])]
              pvalue    = [values[f1][1][0] for f1 in range(0,self.__X.shape[1])]
              feature   = self.__X.columns
              dataset   = pd.DataFrame({"Feature":feature,"F_score":f1_scores,"P_value":pvalue}).sort_values('P_value',ascending=True)
              self.__filter_dataset = dataset[dataset.P_value<=threshold]
              return self.__filter_dataset
            
          if self.__X.ndim<=1:
             self.__X1 = np.array(self.__X).reshape(-1,1)
             self.__f1_score,self.__pvalue = f_regression(self.__X1,self.__y)
             return self.__f1_score[0],self.__pvalue[0]
            
      def quick_plot(self,figsize=(20,5),grid=True): 
            import matplotlib.pyplot as plt
            import pandas as pd
            import numpy as np
            if self.__X.ndim>1:
                A,B = int(figsize[0]),int(figsize[1])
                fig = plt.figure(figsize=(A,B))
                plt.bar(self.__filter_dataset.Feature.values,self.__filter_dataset.F_score.values,label='F_Regression')
                plt.xticks(rotation=90)
                plt.xlim(self.__filter_dataset.Feature.values[0],self.__filter_dataset.Feature.values[-1])
                if grid==True:
                   plt.grid()

                plt.legend()
                plt.show() 
F_Regression.__doc__

class Analysis_variance_test:
      def __init__(self):
            pass
      def get_report(self,dataset,columns,threshold=0.05):
          import pandas as pd
          from scipy.stats import f_oneway
          import numpy as np
        
          self.__dataset = pd.DataFrame(np.array(dataset),columns=columns)
          self.__status,self.__stat1,self.__p1,self.__feature = [],[],[],[]
          for i in range(0,len(self.__dataset.columns[:-1])) : 
              self.__data1 = self.__dataset.iloc[:,i]
              self.__data2 = self.__dataset.iloc[:,-1]
                
              self.__stat,self.__p = f_oneway(self.__data1,self.__data2) 
              
              self.__stat1.append(self.__stat)
              self.__p1.append(self.__p)
              self.__feature.append(self.__dataset.columns[i]) 
            
              if self.__p < threshold:
                   self.__status.append("Different Distribution") 
              else:
                   self.__status.append("Same Distribution")
                    
          self.__result = pd.DataFrame({"feature":self.__feature,"stat":self.__stat1,"pvalue":self.__p1,"status":self.__status}).sort_values('pvalue',ascending=True)
          
          self.__result['weight(%)'] = np.array((self.__result.stat/self.__result.stat.sum())*100)
          self.__result['rank']=np.arange(0,self.__result.shape[0])
          return self.__result
   
      def apply_filter(self,threshold=0.05):
          import numpy as np
          import pandas as pd
        
          filter_    = self.__result[self.__result.pvalue<threshold] 
          excluded_  = self.__result[self.__result.pvalue>threshold] 
          return filter_, excluded_
        
      def get_plot(self,X_label='feature',y_label='weight(%)',figsize=(20,5),grid=False,threshold=1.0,labels=False,legend=False,dpi=100): 
          """ weight(%),pvalue"""
          import matplotlib.pyplot as plt
          import numpy as np
          import pandas as pd
        
          A,B = figsize[0],figsize[1]
            
          plt.figure(figsize=(A,B),dpi=dpi)
        
          filter_data   = self.__result[self.__result.pvalue<threshold]
          
          if y_label=='weight(%)':
             plt.bar(filter_data.feature,filter_data['weight(%)'],label="Threshold:\n{}(pvalue)".format(threshold))
            
          if y_label=='pvalue':
             plt.bar(filter_data.feature,filter_data.pvalue,label="Threshold:\n{}(pvalue)".format(threshold)) 
                
          if labels==True:
              plt.xlabel("{}".format(X_label),fontsize=20)
              plt.ylabel("{}".format(y_label),fontsize=20)

          plt.xticks(rotation=90,fontsize=12)
          plt.yticks(fontsize=12) 
            
          plt.xlim(filter_data.feature.values[0],filter_data.feature.values[-1])
        
          if y_label=='weight(%)':
             plt.title("Analysis of Variance Test",fontsize=20)
            
          if y_label=='pvalue': 
             plt.title("P-value Test",fontsize=20)
                
          if legend==True:
             plt.legend(fontsize=15)
          if grid==True:
              plt.grid()
              plt.show()
          else:
               plt.show()
                
Analysis_variance_test.__doc__

class Forward_Feature_Elimination:
       def __init__(self,model,X_train,X_test,y_train,y_test,iteration,X_label):
            self.__model    = model
            self.__X_train  = X_train
            self.__X_test   = X_test
            self.__y_train  = y_train
            self.__y_test   = y_test
            self.__col_name = X_label
            self.__iteration = iteration
            self.__mylist   = []
            self.__list21,self.__list22,self.__list23,self.__list24 = [],[],[],[]
            self.__list1, self.__list2, self.__list3 = [],[],[]
            
       def get_result(self):
            import pandas as pd
            import numpy as np
            import random
            
            for i in range(0,self.__X_train.shape[1]):
                self.__feature = self.__X_train.iloc[:,i].values.reshape(-1,1)
                self.__test_feature = self.__X_test.iloc[:,i].values.reshape(-1,1)
                
                self.__model.fit(self.__feature,self.__y_train)
                self.__y_pred = self.__model.predict(self.__test_feature)
                
                #acc = metrics.r2_score(self.__y_test,self.__y_pred)
                #error = metrics.mean_absolute_error(self.__y_test,self.__y_pred)
                
                true = np.array(self.__y_test).reshape(-1)
                pred = np.array(self.__y_pred).reshape(-1)
                
                acc   = 1-np.mean(np.square(true-pred))/np.mean(np.square(true-np.mean(true)))
                error = np.mean(np.abs(true-pred))
                
                self.__list1.append(acc)
                self.__list2.append(error)
                self.__list3.append(self.__col_name[i])
                                
            self.__summary = pd.DataFrame({"Feature":self.__list3,"Accuracy":self.__list1,"Error":self.__list2})
            self.__summary = self.__summary.sort_values("Error",ascending=True)
            
            self.__f0 = self.__summary[self.__summary.Error==self.__summary.Error.min()].Feature.values[0]
            print(self.__summary[self.__summary.Error==self.__summary.Error.min()])
            
            self.__mylist.append(self.__f0)
            
            self.__new2 =  [f for f in self.__col_name]

            self.__new2.remove(self.__f0)
            
            random.shuffle(self.__new2)
            
            self.__test0 = np.array(self.__new2)
            
            self.__th = np.round(self.__summary[self.__summary.Error==self.__summary.Error.min()].Accuracy.values[0],3)

            self.__list21.append(self.__summary[self.__summary.Error==self.__summary.Error.min()].Feature.values[0])
            self.__list22.append(self.__summary[self.__summary.Error==self.__summary.Error.min()].Accuracy.values[0])
            self.__list23.append(self.__summary[self.__summary.Error==self.__summary.Error.min()].Error.values[0])
            
            self.__list11,self.__list12,self.__list13=[],[],[]
            
            for iteration in range(0,int(self.__iteration)):
                for j in self.__test0:
  
                    self.__test1    = np.concatenate([self.__mylist,['{}'.format(j)]])
                    
                    self.__feature1 = self.__X_train[self.__test1]
                    
                    self.__test_feature1 = self.__X_test[self.__test1]

                    self.__model.fit(self.__feature1,self.__y_train)
                    
                    self.__y_pred1 = self.__model.predict(self.__test_feature1)
                    
                    #acc1 = metrics.r2_score(self.__y_test,self.__y_pred1)                   
                    #error1 = metrics.mean_absolute_error(self.__y_test,self.__y_pred1)
                    
                    true1 = np.array(self.__y_test).reshape(-1)
                    pred1 = np.array(self.__y_pred1).reshape(-1)
                
                    acc1   = 1-np.mean(np.square(true1-pred1))/np.mean(np.square(true1-np.mean(true1)))
                    error1 = np.mean(np.abs(true1-pred1))
                    
                    self.__list11.append(acc1)
                    self.__list12.append(error1)
                    self.__list13.append(j)
                
                self.__result1 = pd.DataFrame({"Feature":self.__list13,"Accuracy":self.__list11,"Error":self.__list12})
                #self.__result1 = self.__result1.sort_values("Error",ascending=True)
                
                self.__f1   = self.__result1[self.__result1.Error == self.__result1.Error.min()].Feature.values[0]
                self.__round_value = np.round(self.__result1[self.__result1.Error == self.__result1.Error.min()].Accuracy.values[0],10)
                
                print("Interation {} is completed".format(iteration))
                print()
                if self.__round_value >= self.__th:
                   if self.__f1 is not self.__mylist and self.__f1 is not self.__test0:
                    
                        self.__mylist.append(self.__f1)
                        
                        self.__list21.append(self.__result1[self.__result1.Error==self.__result1.Error.min()].Feature.values[0])
                        
                        self.__list22.append(self.__result1[self.__result1.Error==self.__result1.Error.min()].Accuracy.values[0])
                        self.__list23.append(self.__result1[self.__result1.Error==self.__result1.Error.min()].Error.values[0])
        
                        print(self.__result1[self.__result1.Error==self.__result1.Error.min()])
            
                        self.__new3 =  [f for f in self.__test0]
                                    
                        self.__new3.remove(self.__f1)
                        
                        random.shuffle(self.__new3)

                        self.__test0 = np.array(self.__new3)
                        
                        self.__th = np.round(self.__result1[self.__result1.Error==self.__result1.Error.min()].Accuracy.values[0],3)#no round
                        self.__list11,self.__list12,self.__list13=[],[],[]
                        
                else:
                     self.__list11,self.__list12,self.__list13=[],[],[]
                     pass

            self.__result_summary = pd.DataFrame({"Feature":self.__list21,"Accuracy":self.__list22,"Error":self.__list23})            
            return self.__result_summary
        
       def get_plot(self,figsize=(20,8)):
        
            import pandas as pd
            import numpy as np
            import matplotlib.pyplot as plt
            
            self.__row = figsize[0]
            self.__cols = figsize[1]
            
            plt.figure(figsize=(18,6))
            
            plt.subplot(1,2,1)
            plt.plot(self.__result_summary.Feature,self.__result_summary.Error,marker='o')
            plt.xlabel("Mean Absolute Error")
            plt.ylabel("Selected Features")
            plt.xticks(rotation=90)
            plt.xlim(self.__result_summary.Feature[0],self.__result_summary.Feature[self.__result_summary.shape[0]-1])
 
            plt.grid()
            plt.legend(title = "Parameters\nMin_MAE:{}".format(np.round(self.__result_summary.Error.min(),4)))

            plt.subplot(1,2,2)
            plt.plot(self.__result_summary.Feature,self.__result_summary.Accuracy,marker='o')
            plt.xlabel("R^2 Accuracy")
            plt.ylabel("Selected Features")
            plt.xticks(rotation=90)
            plt.xlim(self.__result_summary.Feature[0],self.__result_summary.Feature[self.__result_summary.shape[0]-1])
 
            plt.grid()
            plt.legend(title = "Parameters\nMax_Acc:{}".format(np.round(self.__result_summary.Accuracy.max(),4)))
            plt.show()
            
Forward_Feature_Elimination.__doc__

class backword_feature_elimination:
      def __init__(self,model,X_train,X_test,y_train,y_test,X_label,y_label):
          import pandas as pd
          import numpy as np
          import random
          from sklearn import metrics
          self.__model   = model
          self.__X_train = X_train
          self.__X_test  = X_test
          self.__y_train = y_train
          self.__y_test  = y_test
          self.__X_label = X_label
          self.__y_label = y_label

          self.__list1, self.__list2, self.__list3                 = [],[],[]
          self.__list11,self.__list12,self.__list13, self.__list14 = [],[],[],[]
            
          self.__mylist = []
          self.__count = 0
        
          self.__model.fit(self.__X_train,self.__y_train)
          self.__y_pred = self.__model.predict(self.__X_test)
        
          self.__acc = metrics.r2_score(self.__y_test,self.__y_pred)
          self.__error = metrics.mean_absolute_error(self.__y_test,self.__y_pred)
          
          print(self.__acc,self.__error)
            
          self.__test0 = self.__X_label
            
          for j in range(0,len(self.__X_label)):
                    print("Number of Features under scanning:{}".format(len(self.__test0)))
                    for i in range(0,len(self.__test0)):
                        self.__count+=1

                        new = [f for f in self.__test0]

                        #random.shuffle(new)
                        remove_feature = self.__test0[i]
                        print(remove_feature)
                        new.remove(remove_feature)

                        array1 = np.array(new)
                        #print(i,'\n',array1,'\n',X_train.columns[i])

                        self.__feature = self.__X_train[array1].values
                        self.__test_feature = self.__X_test[array1].values

                        self.__model.fit(self.__feature,self.__y_train)
                        self.__y_pred1 = self.__model.predict(self.__test_feature)

                        self.__acc1   = metrics.r2_score(self.__y_test,self.__y_pred1)
                        self.__error1 = metrics.mean_absolute_error(self.__y_test,self.__y_pred1)

                        if self.__acc1>self.__acc:
                            self.__list1.append(remove_feature)
                            self.__list2.append(self.__acc1)
                            self.__list3.append(self.__error1) 

                    self.__summary = pd.DataFrame({"Feature":self.__list1,
                                                           "Accuracy":self.__list2,
                                                           "Error":self.__list3})

                    if (self.__summary.shape[0]>0):
                        if not remove_feature in self.__list11:
                            print("-"*80)
                            print()
                            print("Iteration{} is completed".format(j+1))
                            print(self.__summary[self.__summary.Accuracy==self.__summary.Accuracy.max()],self.__count,remove_feature)
                            print()
                            drop_feature  = self.__summary[self.__summary.Accuracy==self.__summary.Accuracy.max()].Feature.values[0]
                            drop_accuracy = self.__summary[self.__summary.Accuracy==self.__summary.Accuracy.max()].Accuracy.values[0]
                            drop_error    = self.__summary[self.__summary.Accuracy==self.__summary.Accuracy.max()].Error.values[0]

                            self.__list11.append(drop_feature)
                            self.__list12.append(drop_accuracy)
                            self.__list13.append(drop_error)
                            
                            new2 = [f for f in self.__test0]
                            new2.remove(drop_feature)
                            random.shuffle(new2)
                            self.__count=0
                            self.__test0 = np.array(new2)
                            self.__list1.clear();self.__list2.clear();self.__list3.clear()
            
          #print("Iteration{} is completed".format(j+1))
              
      def get_report(self): 
          import pandas as pd

          self.__results = pd.DataFrame({"Feature":self.__list11,
                                               "Accuracy":self.__list12,
                                               "Error":self.__list13})
          return self.__results
   
      def get_default_plot(self,grid=True,figsize=(18,6)):
    
            import matplotlib.pyplot as plt
            import pandas as pd
            import numpy as np
            self.__width,self.__height = figsize[0],figsize[1]

            plt.figure(figsize=(self.__width,self.__height))
            plt.subplot(1,2,1)
            plt.plot(self.__results.Feature,self.__results.Error,marker='o')
            plt.xlabel("Mean Absolute Error")
            plt.ylabel("Selected Features")
            plt.xticks(rotation=90)
            plt.xlim(self.__results.Feature.values[0],self.__results.Feature.values[self.__results.shape[0]-1])
            if grid==True:
               plt.grid()

            plt.legend(title = "Parameters\nMax_MAE:{}".format(np.round(self.__results.Error.min(),4)))
            plt.subplot(1,2,2)
            plt.plot(self.__results.Feature,self.__results.Accuracy,marker='o')
            plt.xlabel("R^2 Accuracy")
            plt.ylabel("Selected Features")
            plt.xticks(rotation=90)
            plt.legend(title = "Parameters\nMax_Acc:{}".format(np.round(self.__results.Accuracy.max(),4)))
            plt.xlim(self.__results.Feature.values[0],self.__results.Feature.values[self.__results.shape[0]-1])
            if grid==True:
               plt.grid()
            plt.show()
backword_feature_elimination.__doc__

class HeatMap:
      def __init__(self,dataset,figsize=(20,15),method='pearson',templet=2):
          """
          method : {'pearson', 'kendall', 'spearman'} or callable
          Method of correlation:
          templet range varies between 0 to 177
          """
          self.__A,self.__B = int(figsize[0]),int(figsize[1])
          self.__data = dataset
          self.__method = method 
          self.__idx  = templet
          self.__templet = ['Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn',
                            'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r',
                            'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd',
                            'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r',
                            'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 
                            'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples',
                            'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu',
                            'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2',
                            'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r',
                            'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r',
                            'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r',
                            'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm',
                            'coolwarm_r', 'copper', 'copper_r', 'crest', 'crest_r', 'cubehelix', 'cubehelix_r', 
                            'flag', 'flag_r', 'flare', 'flare_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 
                            'gist_gray_r', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow',
                            'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gnuplot', 
                            'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'hot', 'hot_r', 'hsv', 'hsv_r',
                            'icefire', 'icefire_r', 'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'mako',
                            'mako_r', 'nipy_spectral', 'nipy_spectral_r', 'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma',
                            'plasma_r', 'prism', 'prism_r', 'rainbow', 'rainbow_r', 'rocket', 'rocket_r', 'seismic',
                            'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 'tab10_r', 'tab20',
                            'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 'turbo',
                            'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 
                            'viridis_r', 'vlag', 'vlag_r', 'winter', 'winter_r']
      def correlation_matrics(self):
          import matplotlib.pyplot as plt
          import pandas as pd
          import numpy as np
          import seaborn as sb
          if self.__data.shape[0]>1:
              corr = self.__data.corr(method=self.__method)
              fig = plt.figure(figsize=(self.__A,self.__B))
              sb.heatmap(corr, cmap=self.__templet[self.__idx], annot=True)
              plt.title("Correlation-Matrix")
              plt.show()
HeatMap.__dict__
           