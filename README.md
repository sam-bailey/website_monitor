# Website Monitor

This is a set of python snippets useful for monitoring a website, for example an e-commerce site for stock of an item you are interested in. 

## Quickstart

1. Install the requirements in `requirements.txt`.    
2. (Optional) If you would like to send sms alerts using the `send_sms` helper function, set up a Twilio account, and follow the steps in `Twilio Setup` below.    
3. Create a new py file inside `src` and import and subclass `BaseWebsiteMonitor()` from `base.py`.    
4. In the subclass define the url of the website to be monitored, and the condition you are monitoring for. 
5. Create a for loop using the `monitor` method. This will monitor your website. Inside the loop run any actions you want in response to the monitoring.   
6. For a working example, see `src/coolblue_xbox.py`.      

## Twilio Setup

You can use Twilio to send sms via python. You can do this in many ways, but if you would like the `send_sms()` helper function then you need to define 4 environment variables. You can do this by executing the following lines in the terminal.   

```
export TWILIO_ACCOUNT_SID='your_account_sid'
export TWILIO_AUTH_TOKEN='your_auth_token'
export TWILIO_FROM_MOBILE='your_twilio_phone_number'
export TWILIO_TO_MOBILE='your_recieving_phone_number'
```
