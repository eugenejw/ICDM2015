#script for NIARA feature ranking
#author-James Marquardt

library(rJava)
library(FSelector)
library(plyr)

#variables to store names, associated importance, and all class labels
names<-c()
importance<-c()
class<-c()

#path to transposed ngram features
fileName="/Users/the_james_marq/NIARA/DGA_data_transpose"
#path to lexical features
lexicalFileName="~/NIARA/DGA_PaperFeatures_no_mcr.csv"

#create file connector
con <- file(description=fileName, open="r")

#get the length of the file
com <- paste("wc -l ", fileName, " | awk '{ print $1 }'", sep="")
n <- system(command=com, intern=TRUE)

#flag for first row (class label)
first<-T

#loop over each line in the file
for(i in 1:n) {
  
  #read line in, split on comma to make vector
  tmp <- strsplit(scan(file=con,what="character", nlines=1, quiet=TRUE),",")
  print(i)
  
  #if it's the first line, it's the class label
  if(first) {
    class<-tmp[[1]][-1]
    first<-F
  } else {
    
    #perform significance test here if siginificant calculate weight
    c2<-chisq.test(tmp[[1]][-1],class)
    if(c2$statistic > qchisq(c2$p.value, c2$parameter)) {
    
      #calculate gain ratio for the feature if chi2 test is significant
      name<-tmp[[1]][1]
      names<-c(names,name)
      weight<-gain.ratio(class~.,data.frame(class=class,x=tmp[[1]][-1]))
      importance<-c(importance,weight$attr_importance)
      
    } else {
      print("Not significant")
    }
  }
}
#close the connection
close(con)

#do same thing for lexical features (assumes columnn 1 is "class")
lexical.features<-read.csv(lexicalFileName)

for(i in 2:ncol(lexical.features)) {
  c2<-chisq.test(lexical.features[,i],lexical.features$class)
  if(c2$statistic > qchisq(c2$p.value,c2$parameter)) {
    names<-c(names,colnames(x)[i])
    weight<-gain.ratio(class~.data.frame(class=x$class,x=x[,i]))
    importance <- c(importance,weight$attr_importance)
  } else {
    print("Not Significant")
  }
}

#put sort features by gain ratio and output to file
out.df.all<-data.frame(feature=names,gainratio=importance)
out.df.all<-arrange(out.df.all, desc(gainratio))
write.csv(out.df.all,file="~/NIARA/ranked_features_all.csv",row.names=F,quote=F)
