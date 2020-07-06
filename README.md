# nfl-betting-serverless

This is an AWS serverless deployment that leverages the [Serverless Framework].
This deployment uses freely available data found on [kaggle]. Specifically I used a csv file
detailing nfl game results dating back to 1966 through the most recent Super Bowl (https://www.kaggle.com/tobycrabtree/nfl-scores-and-betting-data?select=spreadspoke_scores.csv). I also used a nfl teams json file found on github (https://gist.github.com/fny/66892a96521f1f5406a8a388cf72537e) and augmented the file slightly to include previous team names associated with each franchise. (LA Rams --> St. Louis Rams --> LA Rams)

In this service, I only care about sports betting data, so I iterated through the csv file and parsed out any games that did not have a point spread or over/under line. I used the csv file and nfl teams json file to map through the data to create meaningful data models that tracks the betting outcomes for each game, and updates the teams' betting stats and logs the games for the following buckets related to point spreds and over/under lines:

  - covered
  - did not cover
  - push
 

# How it works

This service leverages a community serverless plugin, S3 Sync, that uploads the nfl csv file and nfl_teams.json file to S3 during the deployment process. In addition, I created a custom serverless plugin appropriately titled: "Kickoff" that triggers a "data-prep" lambda that cleanses and preps the data as stated above. After the data is formatted propery as json, data-prep finishes by uploading the new data to a /clean-data path in the S3 bucket. The upload to /clean-data triggers another lambda, "upload-data" that pulls the properly formatted json files from S3 and then uploads the data to a "Teams" and "Games" table in DynamoDB. 

In addition to this deployment, I also build another serverless deployment of a RESTful API endpoint using API Gateway and Lambda to retrive team and game data. Its still a work in progress, so it only supports getting all team data (all 32 NFL teams and their sports betting records) and getting a team by id. I will be continuing to build out the games piece. You can view that serverless deployment [here](TODO: add other repo url).


# Development Process

I used the aws-python3 runtime for the data-prep and data-upload lambdas for a few reasons. First, python seemed like the natual choice for working with csv files. I did not need to install or use any 3rd party libraries. The only 3rd party library I used was boto3, which comes with the aws-python3 runtime. So, the deployment subsequent package management (or lack therof) was a lot more streamlined, and my deployment was < 10MB. Secondly, boto3 comes with a nice API for bulk upload that makes dealing with the 25 document BatchWriteItem limit painless. batch_writer handles all of that for you which is really nice!

I used TypeScript/Node.js for the REST API endpoint in my other deployment. 

# Running the deployment:

  - In order to run this you will need to install the [Serverless Framework] and have access to an AWS account
  - All you need to do is create an .env file with the following environment variables: ACCESS_KEY_ID and SECRET_ACCESS_KEY from your AWS account, BUCKET_NAME - the S3 bucket name you want to use. Needs to be globally unique. And APP_AWS_REGION - the AWS region you would like to deploy to.
  - Next, you run npm install to install the serverless dependencies and plugins
  - Lastly, you run sls deploy and the [Serverless Framework] takes care of the rest!



[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [kaggle]: <https://www.kaggle.com/>
   [Serverless Framework]: <https://www.serverless.com/>