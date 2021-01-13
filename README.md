# FederatedLearnig_Demo
This is the code I created for showing the possibility of creating a simple linear regression model with tensorflow and used it in an android app in order to use Federated Learning. Here is both the app and server code. 

In this project I created a machine learning model and train it on device with my phone. 




### How it works:

  Your device downloads the current model, improves it by learning from data on your phone, and then summarizes the changes as a small focused update. Only this update to the model is sent to the cloud( I used Heroku and Google Cloud but other could be used), where it is immediately averaged with other user updates to improve the shared model. All the training data remains on your device, and no individual updates are stored in the cloud.
  
  
![Image of googleAI](https://1.bp.blogspot.com/-K65Ed68KGXk/WOa9jaRWC6I/AAAAAAAABsM/gglycD_anuQSp-i67fxER1FOlVTulvV2gCLcB/s1600/FederatedLearning_FinalFiles_Flow%2BChart1.png)


