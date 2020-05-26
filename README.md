ZMS - Join Zoom Meetings from command line
===========================================

This tiny tool allows you to join a zoom meeting from your "Terminal" by invoking a quick short command created as alias in shell. 

For a DevOps/SRE, we spend our significant time working with "Terminal", this becomes handy in case where we get a reminder for a meeting in such cases we can run this command and get Zoom client to start and drop us in meeting immediately.

I prefer to use this tool for daily sync with team and others, when I am busy dealing with stuff in my "Terminal" and see the reminder for meeting, it becomes easy for me to just run 'dailySync<TAB>' and yo, I am in meeting, convenient right? :)


### Create entry for meeting(s)
```./zms.py -m <Meeting ID> -a <Alias Name>```

Where:

    Meeting ID: Zoom Meeting ID in your invite.
    Alias Name: A short quick name you can keep for this.


### Create short alias for your command line
```./zms.py --create_alias```

This will create alias for all the meetings you have added so far.


### List entry for all meeting(s)

```./zms.py --list-entry```


### Join a meeting

There are two ways:-

1. You can directly run `./zms.py -a <Alias Name>`
2. Using alias name from your command line. for example, `$ dailysyncup`


### Remove a meeting entry
```./zms.py --remove_entry --alias_name <Alias Name>```


References:

https://marketplace.zoom.us/docs/guides/guides/client-url-schemes





