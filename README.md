Voice Order: SBHacks Project

When it comes to cutting costs through automation, small businesses, drive-thru services, and restaurants run into the same problem: almost all orders require an employee to customer interaction.

Enter VoiceOrder. This general-purpose AI uses Amazon Alexa and natural language processing to determine what a customer is trying to order, and sends requests based on those orders to a simple web server. This enables businesses to cut down on costs, as well as improve the automated user experience. There’s no more need for fumbling around on a kiosk figuring out where your desired item is; all that is needed is to read off your order to the voice assistant. And instead of investing thousands of dollars investing in custom order processing, businesses only need a $35 Amazon Alexa to be more profitable and satisfy their customers.

Here is a summary of the tools we used while creating VoiceOrder:

Amazon Alexa Skills Kit API:
Utilized Amazon Alexa’s speech recognition software to take in input for further processing
Leveraged AWS Lambda to run a server-side feedback loop written in Python
Made use of the Alexa Developer Console to design custom intents and utterances

Google Cloud AutoML Natural Language Processing API:
Trained a custom machine learning model regarding our demo product to analyze user messages for order intent

FireBase:
Leveraged FireBase’s API to store orders detected by the AI on a local server
Utilized React.js to display processed orders in real-time

Team Members: Connor Lien, Matthew Park, Ryan Niu, William Zhang
