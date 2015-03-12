This ReadMe discusses some portions of Assignment-3. 
Other assumptions have been included as comments in the code where appropriate.

This class is my first time working with the Python language, and I have been
doing my best to increase my "best coding" practices as I go. You will see this
develop throughout the assignment. For example, in program 1.1 and 1.2 I solved
certain problems in more lines than required. Halfway through problem 2.1, I
researched and discovered the proper way to store modules in a library, which I
have called "lloplib", that will be accessible to this and future assignments.
For that reason, problems after 2.1 make use of "lloplib", while I have not
had time to refactor the previous problems.

Given that this is class and not a production environment, I hope that my decision
to demonstrate learning as I go as opposed to refactoring is considered a positive
as opposed to a reason for point deduction.

The following section gives an overview of certain codes in this Assignment.
This documentation is not holistic, and should be considered in conjunction with
comments provided in-line throughout the code.

Documentation for the codes in the Assignment-3 Folder:

1.1_db_streamT.py
Mostly the same as Assignment-2, this code stores the tweet data into MongoDB. 
This code was not re-run while completing Assignment-3 as the MongoDB already
existed from Assignment-2.

1.2_db_tweets.py
This code loads tweets from the S3 JSON files stored in Assignment-2, then parses
out the text, saving it into a MongoDB named db_tweets. I have decided to store
unicode as received from Twitter so that this code is flexible to tweets in a variety 
of languages.

2.1_top_30.py
This code uses the MongoDB aggregate function to find the top 30 tweets based on the
tweet content. It then pulls data about the original poster of the tweet from db_streamT


