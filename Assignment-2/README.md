This update to Assignment 2 addresses a number of issues pointed out in the first grading. 
It also stores the data not only to disk in a .txt file, but also to a MongoDB database that can be
leveraged in Assignment 3.

RE: No raw data partitioning and storage
- Data is now stored in full JSON form, as requested. Storage occurs both on disk, in MongoDB, and in S3.

No resiliency in the code (rate limit, exception,…)
- Resiliency has been added throughout the code to deal with exceptions. I found that tweepy's built-in
    rate limiting was sufficient for the Twitter data pull portion of this task. Regardless, no points
    were deducted for not having resiliency in the original code, thus this change was done as a learning
    exercize as opposed to regain points

No filtering of tweets’s text on usernames (@)
- Keeping usernames in the histogram was an intentional design choice, however, I have modified the analysis
    to remove usernames at the request of the instructor.


com.christopherllop.w205assignment2 is the S3 bucket where the boto package stores and accesses scraped data

scrape.py scrapes the data
    It stores the data locally, in a MongoDB, and to S3

histo.py creates a histogram
    It first attempts to use data stored in MongoDB
    If that is not successful, it attempts to fetch data from S3
    It then builds the histogram
    I have used this dual functionality to "test" that the results of parsing from Mongo match those of
        parsing from S3. This served as a sanity check of my work.

histogram.txt is the output histogram
