British Cycling Website is not easy to scrape due to the dynamic nested tables which hold key event information as a result the code is using Selenium rather than beautiful soup.

There is a working directory function to use a local folder followed by options which can impact how the code is ran - with/without chrome being opened directly or just in the terminal. I find that when testing it’s best to have chrome open as it’s easy to debug - by default it’s hidden as the code should be able to run in the background seamlessly. There are two default functions relating to first page and first month of the year.

While it looks slightly messy, I’ve had to split the code into months as it was previously break midway through the loop. BC uses a two digit month code so that is why I turn the loop into 2 digits as a string. The URL is with selected filters for only certain events as we are not interested in non-races.

I then check that the event element (website code) is readable before continuing onto the main loop. Each event tag is a Class name called `”events—desktop__row"` so I check that’s there. BC website requires cookies box to be clicked before the website becomes dynamic so I click accept cookies.

I, then, find the event next on the page and scroll down to it. I do this so I can check if the clicking actually works properly and automate the click of the button which provides information on all the races within the event. 

This is the main loop which I run for the number of rows in the page which is 101. There are 100 events and the header counts as the first one - which causes the script to “fail” so if you need one fail for each page, don’t panic.

As a precautionary measure, I rerun the `events` and `toggle_button` functions within the loop as I mentioned that the script would break once it had looped too many times. (I’m not sure if I need to do this but it does the job). 

Using a combination of `CSS_Selector` and `Class_Name` to find the main tables metadata and scrape that. In the raw data, event day and event date are in one column so requires a small transform. To get to the nested subtable, you find them by searching for `".table__more-data--showing table”` as that’s the id for the nested subtables. You use `toggle[-1]` because of the indexing to 0 while the count starts at 1 to open the subtable to be able to scrape.

There is a reminder of the expected failure once a page and a confirmation of which one failed.

The final part is about clicking next page as some months have over 100 events. The id of the next page button is `”a.button.button—medium.button—secondary.next"`. It’s disabled if no more pages. I, then, scroll down to the button before clicking it. 

The final part of the loop is making sure that the code doesn’t continue until there are events to look into on the next page.

Once out the loop, the table is loaded for each month and then unioned together to make a table for the output. 
