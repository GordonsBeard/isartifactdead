# Is Artifact a Dead Game?

tldr: yes.

http://www.isartifactdead.com

---

### What
This website currently lists how many people are currently playing Artifact. It also tracks the player count of a few other card games that were around at the same time as Artifact, but that's only visible if you view-source in the browser.

### Why
Petty spite. On the Artifact Steam Forums, shortly after the launch of Artifact, a heated topic of discussion was "is Artifact dying/going to die?". 

In my view, a lot of threads were being cluttered by folks saying things such as "It doesn't even have X players! It's doomed!!". This annoyed me, and so I built a website that would track the player count and (mockingly) points out the player count. 

The thought was that the game would, indeed, not die. This would make the website silly, a contradiction almost.

Instead it is I who is the fool for caring this hard.

### When
This was built in a weekend sometime before the actual death of Artifact. 

It is no longer archived, the code long since deleted, but at one point the text would say "Yes, there are only X players. (That's less than [other_game]!)". But then the player count cratered under every other card game on steam and so it was text that was never seen. Once the player count was consistently under 300 it was switched to just saying "Oof." instead of a player count comparison.

Then once the game was actually canceled by Valve, a second time, the website was switched the state you see today. Just a static offering of condolences in the most poster-brained way possible. rip in piss ashes to asses etc etc.

Somepoint after the death of the game someone wrote a silly article about it: https://www.thegamer.com/isartifactdead-dot-com-artifact/

### Who
I did this. I really liked Artifact and I was actually p. embarrased my "epic pwnage" blew up in my face immediately.

### How
(this is for future me when I inevitably nuke the webserver its running on and I need a how-to, again)
1. clone it
2. install requirements.txt
3. create .env file with STEAM_API_KEY=api_key
4. install nginx, create a site in sites-enabled
5. install gunicorn as wsgi
6. install supervisor to keep this all running (use the isitdead_app.conf)

follow this guide dummy: https://www.linode.com/docs/guides/flask-and-gunicorn-on-ubuntu/#copy-your-flask-app-to-your-linode