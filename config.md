Allows for true persistence of localstorage data after closing and reopening anki, as well as mobile support for reading (but not writing) of the localstorage data. 

It works by saving localstorage key/value pairs starting with phrases defined in the addon configuration as __persistentlocalstorage.js in the users media folder, and then calling the script on the first reviewed card to load the values back into localstorage. 

This can be used to change card field values functionally permanently through javascript in the card template. It can be used to remember the slide you were on in an embedded powerpoint, show you randomized items with replacement across review sessions, show you the number of times you have clicked a button on the card, etc. 

It is also compatible with syncing across Ankihub decks. 

For support, see here: https://github.com/connwork/ankitruepersistence

If you like this and would like to donate, all funds will be routed to feeding my child and trying not to fail my medical school exams. https://www.paypal.com/donate/?business=JQL7U4PMGHPKS&no_recurring=0&item_name=Thank+you+%21&currency_code=USD