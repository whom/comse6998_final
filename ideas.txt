Project thoughts

Every user has an ACCOUNT. This can be stored in a simple relational database system. Something like:
User ID
Account name
Password
Account status (validated, banned, etc.)

But if people log in with Facebook, do we still need this?

Every user can make a POST. Posts can be thought of as JSON objects like the following:
Title: string
ID: number
User: string
Images/Attachments: array of URLs
Text: string
Comments: array of comment IDs
Location: array
Score: number

Every POST has one or more COMMENTS. Comments can also be thought of as JSON objects:
ID: string
User: string
Text: string
Images/Attachments: array of URLs
Post: ID of post this comment relates to
Score: string (number of upvotes/downvotes)
Location: array

Posts and comments can be stored in ElasticSearch on AWS. Images and attachments can be stored in a storage container on AWS.
When someone clicks on a post, we fetch the post from ElasticSearch. When viewing comments, we fetch comments associated with the post from ElasticSearch.

Streaming:
Posts and comments are constantly being sent from users to our servers. Servers will need to quickly update our ElasticSearch services.

Analytics:
We can retrieve all comments a user has made and use that to decide what posts to show that user.
Use something simple, like proximity (location) or just parsing the keywords of the post the user commented on.
Maybe combine it with score?
Advanced: Measure sentiment in some way from the comments to filter out those kinds of posts?

We can initially build the app using only Back-end (Django) and HTML. So no dynamic refreshes, AJAX, or jQuery. 
It will be very forum-like.
