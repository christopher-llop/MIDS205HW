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

One overarching issue I have been wrestling with is finding the right amount of 
resiliency to write into my code. This submission reflects my best efforts. Reflecting 
on what I have done, I think I built too much resiliency (too many exception checks)
into my first two programs (1.1, 1.2). I hope that the later programs still have
enough, but I would appreciate any feedback on this points.

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

2.2_lexical_div.py
This code computes the lexical diversity for each user for whom we collected tweets. In this analysis,
we allocate retweet content to the user who retweeted it. There are many assumptions in this analysis,
spelled out at the start of the code. See "lexical_diversity_hist.txt" for the requested plot
of the results. We find that many users had a diversity of 1 (only used unique words). We hypothesize
that these are individuals who only tweeted about #Microsoft or #Mojang once in the study period, thus
they did not have time to use multiple instances of words. After this, we see a "hump" in the lower 90%,
and 80%s. Again, with the small number of tweets per user we should be suspicious of drawing too much
from this analysis without further investigation.

2.3_db_followers.py
This code takes the top 30 tweets stored during the run of program 2.1, and pulls the followers.
It then waits a week, and pulls the followers again. Finally, the program compares the followers
and identify "unfollowers". We complete most of this task in storage as opposed to memory by storing 
to MongoDB, and using the "aggregate" function (and its pipeline) to identify users who were followers 
at time 1 but not at time 2

3.1_S3_store.py
Stores db_streamT and db_tweets to S3