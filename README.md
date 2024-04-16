## SETUP AND SEQUENCE ##
- first and foremost satisfy requirements.txt as it contains list of libraries being used.
- then run file train.py which will train our model.
- after that run app.py file where you can interact with bot as soon as you are gonna run that file a 2 pop-ups will come i) fill the one which asks for user's name as input first ii ) then you can chat with bot and
even select faqs iii) as soon as u will try to exit a window will appear asking for your feedback if you will press no it implies user is not willing to give feedback iv) but if pressed yes you will be asked to rate
interaction based on stars from 1 to 5 and at last you can leave description as feedback to creators of bot.

## FAQ INTEGRATION ##
- list of pre provided faqs is given and you can select from them.
- if question asked is not in faq list it will be appended.
- if our bot can't handle question it will be passed to doubt assistant.

## NLP ##
- used NLP for understanding user's queries precisely and also used techniques like fuzzy matching.
 
## DOUBT ASSISTANT ## 
- In case bot can't handle queries it will select one of the many answers pre-provided by doubt assistant (think of it as human assistance to solve some queries).
- The answer of doubt assistance is selcted randomly ny shuffling so bot seems more responsive.
- If any of these queries are asked again it will be answered as it is saved in a dictionary which will be dumped so the assistance isn't wasted.(fallback_tracing.pkl is files name for reference)

## USER FEEDBACK ##'
- as specified user's feedback is taken into consideration not just rating based on stars but the description as well.
- it is even used to calculate our model's performance.

## DATA SHARING ##
- Data of user's whole chat is saved in file named -> username_chat_history.csv.
- As data privacy is one of the most important aspect of modern era the data is stored in csv file in encrypted form.
- another python file named-> encryption_and_decryption has a function called -> read_encrypted_csv which returns you the decrypted data by taking filepath as input.

## PERFORMANCE MONITORING ##
- Performance of each chat will be monitored and can be accessed at csv file named-> chatbot_metrics.csv .

 if there are any more queries mail me at : dangwalshubh9@gmail.com or shubhhdangwal@gmail.com.
- first and foremost date and time of entry is mentioned in csv file then 4 aspects of performance analysis is entered.
- first aspect of performance is understanding rate of model i.e. out of all the queries asked by user how many of them were answered without calling in fallback assistance.
- second aspect of performance is miss rate of faqs i.e. out of all the queries asked by user how many of them weren't already asked.
- third and fourth aspect are user rating out of 5 and percentage of user rating. (might cause error in system hence it is commented along with the reason.)
- and at last another value is added i.e. user's feedback as it can be used to boost performance.
  
