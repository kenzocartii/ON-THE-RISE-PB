"""
ON THE RISE: PB CIRCUIT bot
===========================

Builds the circuit's Discord server, runs teams and tournaments, tracks RISER POINTS,
and keeps the circuit website up to date.

Slash commands
  Players and captains
  /signup team_name logo         Anyone: start a team (logo required). You become captain.
  /offer @player                  Captains: offer a spot. They Accept / Decline in DMs
                                 (DM only: nothing is posted in #free-agents). 5 to 8 per team, one team each.
  /revokeoffer [player] [team]  Captains/co-captains (or staff): take back an offer; no player = list open offers
  /position player: player position  Staff: change anyone's position (roster card, #transactions, website, DM)
  /roster [team] [player] [private]   Anyone: any team's roster (complete or still building), the team a
                                player is on, or every team at once
  /release, /captain role:captain         Captains: release a player / hand over the captaincy
  /captain [player] [remove] [team]   Captains (or staff, any team): appoint one co-captain who can also /offer. Shown as (CC) on the
                                roster; the Co-Captain role is not listed separately in the member list.
  /register, /unregister         Captains/co-captains: enter (or leave) the tournament that's taking entries.
                                Staff: add team:@Team to enter/remove any team (ignore_roster, late options)
                                 Shows your RISER POINTS and how many you still need for the Major.
  /leaveteam                     Players: leave your team (not while a tournament is being played)
  /disbandteam confirm:True      Captains: delete your team (not during a tournament)
  /roster [team], /points      Team card / RISER POINTS standings
  /freeagent [position]          Turn the Free Agent role on or off
  /position                      Set your position: PG, SG, SF, PF or C. Required to create a team (/signup asks
                                 for it), accept a team's offer, become a free agent, or join the pickup queue.
                                 Positions show on rosters, team cards, pickup cards, the draft menu and website.

  RISER POINTS
  - Each circuit event gives points by placement (set per tournament in /opensignups).
  - Tournament winners qualify for the Major automatically (staff can turn that off per tournament with the
    winner_qualifies option or /tournament winner_qualifies:); others need the target set with /tournament major_target:.
  - If fewer than 3 of the players who earned a team's points are still on it, the points are lost.
  - When a Major finishes, everyone's points reset to 0.

  Staff
  /setupbot part:<what>         Staff: every one-time setup lives here (safe to run again):
                                server (admin: roles, channels, rules), rules, ranked [ranked_size], tickets,
                                moderation (welcome + join log + suspensions), media, champions, teamvoices,
                                registered (the current tournament's registered-teams channel)
  (/setupbot part:server also gives the Player role to everyone already in the server)
                                 (new members get it automatically when they join)
  /tournament major_target: points_needed        RISER POINTS needed to qualify for the Major
  /opensignups name logo [kind] [points] [closes]   (the tournament logo is required)
  /tournament logo: logo          Staff: change the current tournament logo
  /setupbot part:registered            Staff: make the 📋｜<tournament-name> channel listing registered teams (opening
                                sign-ups makes it automatically; it updates on every /register and /unregister)
  /tournament closes: closes [remind]    Staff: change when entries close; DMs captains of full teams not yet registered
  /tournament winner_qualifies: winner_qualifies   Staff: does this tournament's winner get an automatic Major spot? (yes/no)
                                 Open entries for a tournament. kind = Circuit event or Major.
                                 points = placement table, e.g. "1:300, 2:210, 3:150, 4:120, 5-6:75, 7-8:45"
  /closesignups                  Close entries (needs 6+ complete teams)
  /payout place_1:… place_2:… place_5_6:…   Set the RISER POINTS for each finishing position
                                 (1st, 2nd, 3rd, 4th, 5th-6th, 7th-8th, 9th-12th, 13th-16th, 17th-24th, 25th-32nd,
                                 33rd-48th, 49th-64th). Only fill in the ones you want to change. Applies to the
                                 current tournament and is saved for future ones.
  /setpoints team points, /setpoints reset_all:True confirm:True
  /setlogo team logo, /addteam, /removeteam, and /offer and /release with a team option
  /roster, /refresh what:rosters      Registered teams / re-send the team cards in #rosters
  /endseason confirm:True        End a tournament early and send the stay-or-leave DMs
  /testtournament [teams] [style] [publish] [channels] [scorecards]
                                 Play a whole fake tournament (2 to 64 teams) with made-up team names, logos,
                                 players and box scores, posted step by step in #announcements, #transactions,
                                 #schedule, #standings, #bracket and #score-reports (all marked TEST).
                                 A summary goes in #staff-chat. Real teams and points aren't touched.
                                 It uses your /payout table; add place_1:… place_5_6:… etc. to try a
                                 different table just for that test.
                                 publish:True also puts it on the website's /test/ page.
  /cleartest                     Delete every test tournament post.

  Pickups (ranked queue)
  /setupbot part:ranked [players] [start_rr] [teams]
                                Staff: make the "10 MANS" category with 📢｜10s-announcements, ℹ️｜10s-info (filled
                                in with how it works, ranks, RR, commands, rules), 🏠・10s-general and 🎮｜10s-queue
                                (queue card with Join/Leave buttons). Big moments (double/triple rank-ups, 5+
                                win streaks, finished placements) are posted in announcements. Also makes the
                                rank roles: Iron, Bronze, Silver, Gold, Platinum, Diamond, Amethyst, Ruby, Vibrant
                                (divisions 1-3 of 100 RR; Vibrant is the top rank, one tier, no ceiling).
                                When the queue fills, two random captains take turns picking players from a
                                dropdown (A B B A ...), or with teams:Auto-balance the bot splits them by RR.
                                Then it opens two voice channels and posts the match.
                                Every player picks the position they're playing (PG, SG, SF, PF, C) from a
                                dropdown each time they join the queue; it shows on the queue, draft and match.
                                One player from each team clicks who won; both must agree (or staff decide).
                                Each win is +10 to +32 RR and each loss -10 to -32, based on how well you played:
                                the host or staff enter stats (/pickupstats CSV or /pickupstat per player; get a
                                sheet with /pickupstats). Best player in the game: +32 win / -10 loss; worst:
                                +10 / -32. Until stats are in, everyone gets ±21, adjusted when stats arrive.
                                Great game (top of the lobby, winning team): gains x2. Win streaks: 3 x1.25,
                                4 x1.5, 5 x1.75, 6 x2, 7 x2.5, 8-9 x3, 10+ x4 (stack with great games), so big
                                wins go well past +32 (up to +256) and give double or triple rank-ups.
                                New players play 3 placement games (unranked, count 4x) and get placed between
                                Silver 1 and Platinum 3.
  /rank [player], /leaderboard  Rank card / top 20 by RR
  /pickupresult, /setrr, /setrr reset_all:True confirm:True   Staff tools

  Moderation and welcome
  /setupbot part:moderation [welcome_message]   Staff: make 👋｜welcome (greets every new member with a welcome card),
                                ⛔｜suspensions (public log) and 📥｜join-log (staff only: joins/leaves with
                                account age, flags accounts under 7 days old and people rejoining while suspended)
  /suspend member reason tournaments | length [scope] [details]
                                reason is a dropdown. Hacks/exploits and Alting/account sharing: Director of
                                Enforcement or Commissioner only. Throwing games, Threats and Discord rule breaks:
                                League Staff too. Same split for /suspensions lift:True.
                                tournaments: sit out 1-10 tournaments (the one taking sign-ups or being played
                                counts first; counts down when a champion is crowned). Can't create, join or be
                                signed to a team, register or free-agent until it's served.
                                Or length: 30m, 12h, 3d, 1w, 2d12h or perm. scope: Ranked queue / League (queue,
                                teams, tournaments) / Server timeout + league. Posts in ⛔｜suspensions, DMs the
                                player, gives the Suspended role, and lifts itself when time is up.
  /suspensions lift:True member, /suspensions [member]   Lift early / list current ones or a player's history
  /remind [what] [when] [note] [ping] [again]   Staff: reminder card in #announcements for sign-ups closing,
                                the live draw, the main draw or games (games also go to each team's channel).
                                when: 8pm, tomorrow 7pm, sat 6pm, in 2h. again: post again 15m/30m/1h/1d before.
  /reminders [cancel]           See or cancel the reminders waiting to go out

  Media
  /setupbot part:media                   Staff: MEDIA category: media-info (Stream Pings + Apply buttons), stat-leaders
                                (auto-updated every 30 min), live-now, media-shows, power-rankings, highlights,
                                edits-and-gfx, media-chat, and a Media Booth voice channel. Roles Media,
                                Streamer, Stream Pings.
  /golive link [title]          Media/Streamer: post a LIVE card that pings Stream Pings
  /refresh what:leaders                  Refresh the stat leaders now
  /giverole member kind [remove]   Staff: give or take Media / Streamer

  Rules, team voice, match scheduling
  /setupbot part:rules                   Staff: wipe #rules and post the circuit rules as cards (edit RULE_CARDS to change)
  /setupbot part:teamvoices                   Staff: give older teams a voice channel (new teams get one automatically)
  /presettime time [timezone]   Staff: the first evening slot the bot uses if captains don't agree a time
                                (default 20:00 ET, then every 30 minutes to 11:30 PM, then the next evening).
                                Group stages under 16 teams and main draws run on a 3-day clock.
  /gametime match [timezone]    Captains: pick the times that work; the other captain confirms one in DMs (or
                                suggests another). 12-48 hours to agree, then the bot picks a time and staff confirm it, which
                                can still be moved earlier or later if both captains confirm (72-hour window). New matches DM captains + co-captains
                                "YOUR NEXT ON THE RISE PB: TOURNAMENT MATCH IS ..." and ping both captains.
                                Reminders 24h, 1h and at game time.
  /reschedule match time [timezone] [reason]   Staff only: move a game (or set its time), no confirmation needed
  /nextgame                     Your team's next match and time
  /matchdms                     Turn your match DMs on/off

  Champions
  /setupbot part:champions                Staff: make 🏆｜champions and the Tournament Winner role. When a tournament ends,
                                the winning roster gets Tournament Winner + "🏆 <tournament> Champions", and the bot
                                edits the champions list (one card per title, tournament logo + team logo).
                                When a Major ends the series resets: every circuit-event champion role from that
                                series is deleted and Tournament Winner is removed from everyone except the Major
                                winners, who keep it and their Major champion role.
  /champion action:add tournament team [logo]   /champion action:remove number   Staff: fix the list by hand

  Stats from screenshots
  /statsimage kind match image [image2]
                                Upload the box-score screenshot(s). The bot reads every player's line, matches the
                                names to the rosters, and shows a preview: Save (box score + website, or pickup
                                stats + RR), Fix (edit names/numbers; learned names are remembered), or Cancel.
                                Needs Tesseract OCR installed on the bot's computer + `pip install pillow`.
  /statsimage image [image2] [team1] [team2]
                                Staff: try the reader on any screenshot. Shows what it read (and flags lines that
                                don't add up) and puts it on <site>/statstest/. Nothing touches the real league.

  Draws
  /testdraw [kind] [teams] [real_teams] [group_size] [advance] [play_through] [website]
                                Staff: practice the live draw in the channel you're in (fake teams by default,
                                or your real teams' points); nothing is saved or announced. By default it then
                                plays the group/Swiss stage with random results, posts the standings pictures,
                                runs the main-draw draw, and puts a preview on <site>/testdraw/.
                                channels:True (default) posts everything in the channels a real tournament
                                uses (#bracket, #standings, #schedule, #score-reports, #announcements), marked
                                TEST and without pinging anyone. channels:False keeps it all in one channel.
                                live:True (default) plays it like a real event: each match opens in #scheduling,
                                gets a game time, and finishes at its own time (score report + Final Score card
                                in #score-reports, result in #schedule, standings updated). You play captain of
                                the #1 seed and confirm your game times in DMs (2 minutes, then the preset time).
  /setupbot part:gamerules      Staff: make #game-rules and post the game settings + how to report scores
                                (public gym = stats screenshot, league gym = stats export). Captains and
                                co-captains also get them in DMs whenever a game time is confirmed.
  /renameteam team new_name     Commissioner/admin: rename a team (its role, team text + voice channels,
                                #rosters, the registered list and the website all update)
  /streamlink link              Streamers: the link used when you click Claim Stream (asked for on your first
                                claim, then reused). Live games show on the website with the stream linked.
                                When a claimed stream goes live the bot posts in live-now with @here: Twitch
                                links are checked for real (set TWITCH_CLIENT_ID / TWITCH_CLIENT_SECRET), other
                                links get the post at game time.
  /profile [player] [build] [ovr] [activity] [position]
                                See a player's profile card, or set yours (build, OVR 1-99, activity 1-10).
                                Staff can fix anyone's with player:. The card uses their Roblox avatar (server
                                names are Roblox usernames). Every free agent gets their own card in #free-agents.
  /game_score match winner score [stats]
                                Captains/co-captains: report a game's score (winner's points first) and attach
                                the stats screenshot (public gym) or export (league gym). The other team's
                                captain or co-captain confirms or disputes it with buttons (their DMs, their
                                team channel, or #score-reports; nobody is pinged in #score-reports). After every
                                result, both team channels get the final and who they play next.
                                Admins' reports count straight away (override).
  #game-finals                  Every result posts the Final Score graphic there with a short recap of the game
                                (how close it was, each team's Player of the Game, records / eliminated / next
                                game). Made automatically the first time a result comes in.
  /disqualify team reason [cheaters] [rewind] [confirm]
                                Staff: disqualify a team for cheating. During a tournament: their unplayed games
                                are forfeits, and rewind (pick one of their wins) reinstates the team they beat
                                in their place (groups/Swiss: their wins from that round on are flipped). After a
                                tournament: their RISER POINTS are halved and any Major spot is removed.
                                2+ players caught: points go to 0. Shows a preview; add confirm:True to do it.
  /cleartest what:draw [everything]  Staff: delete the last test draw (cards + picture), or every test draw with
                                everything:True. Stops a test draw that's still running.
  draw_in:N on /startgroups, /startswiss and /startmain: the LIVE DRAW starts N minutes later (default 5) with
  an @here in #announcements and a countdown in #bracket. Seeds, the top 8 one by one, a drum roll for #1, then
  the groups pot by pot (or the matchups), each as its own message so you can scroll back and re-watch.
  Standings, schedule, match DMs and the website stay secret until the show ends.
  Every draw is seeded by RISER POINTS (ties broken by a coin flip). Starting a tournament runs a LIVE DRAW in
  #bracket: seeds revealed from last to #1, then the matchups or groups drawn one at a time (groups use pots by
  seed), then a picture of the draw is posted there and in #announcements (needs `pip install pillow`).
  Up to 68 teams. Pictures show each team's seed, RISER POINTS (RP) and point differential (PD) in this
  tournament. Group stage: one standings picture in #standings (W-L, PD, RP) is edited after every result.
  Swiss: each new round posts a picture in #schedule, teams drawn at random within each record (1-0, 0-1...).

  Invites
  /invites [member]             How many people someone brought (still here / joined / left) and who invited them
  /invites top:True            Top recruiters. Every join is logged in 📥｜join-log with who invited them, and
                                anyone who brings 3+ people who stay gets the Recruiter role.
                                The bot needs the "Manage Server" permission to see invite links.

  Announcements
  /announce [channel] [ping] [role] [image] [color]
                                Staff: write an announcement in a form, see a preview, then Post or Cancel.
                                Posts in #announcements by default, as a branded card with your name on it.

  Ranked voice
  Voice isn't needed to queue (set PICKUP_NEEDS_VC = True in the file to require the 🔊 Waiting Room again).
  When a match starts, each team gets a locked call (team + staff only), everyone is moved in,
  and the host captain shares the server code with the 🔑 button. Calls are deleted and players sent back
  to the waiting room when the match ends. The bot needs Move Members + Manage Channels.

  Tickets
  /setupbot part:tickets                  Staff: make the SUPPORT category with 🎫｜open-a-ticket (a card with a dropdown:
                                Stats, Report a cheater, Ranked/RR, Team/roster, Roles, Media, Appeal, General)
                                and a staff-only 📁｜ticket-logs. Picking a topic asks for details, then opens a
                                private channel for that player and staff. Claim / Close buttons inside; closing
                                saves a transcript to the logs and DMs it to the player.
  /ticket action:add, /ticket action:remove     Staff: add or remove someone from a ticket
  /ticket action:close [reason]         Close the ticket you're in

  Tournament
  /startswiss [wins] [losses]   Optional Swiss qualifier (default: 3 wins = qualify, 3 losses = out).
  consolation:True on /startswiss or /startgroups: teams knocked out in the qualifier play a single-elimination
                                consolation bracket (posted in #bracket when the qualifier ends). Once both
                                brackets finish, the consolation winner gets bonus points that leave them 15
                                behind last place in the main draw (main-draw teams are topped up if needed);
                                the runner-up gets half (not in a Major or LCQ).
  /opensignups kind:LCQ         Last Chance Qualifier: the next 8 teams that haven't qualified (most RISER POINTS
                                first) are invited and entered automatically, captains get a DM. Teams tied at
                                the cutoff are ALL invited to a single-elimination play-in for the last spots
                                (results with /result, then /startmain). Odd number of
                                teams (fewer invites, or a team drops with /unregister)? The next man up gets in.
                                Run it with /startmain; the top 4 qualify for the Major. Target: 600 (/tournament major_target:).
  /startgroups [group_size] [advance]
                                Optional group stage. Pick how many teams per group (3-8, default 4), then
                                how many from each group make the main draw (1 up to group size - 1, default 2).
  /startmain                    The main draw, always double elimination, posted in #bracket.
  /result match winner [score]  Referees/staff: record a result. Next matches post automatically. When the
                                  champion is crowned, RISER POINTS are awarded (or reset after a Major) and
                                  every player is DMed with Stay / Leave buttons.
  /importstats match          Referees/staff: get a stats sheet (CSV) for a game with both rosters listed
  /importstats match file       Upload the filled-in sheet: 2FG, 3FG, FT (made/att), ORB, DRB, REB, AST, STL,
                                BLK, TO, FOUL, +/-, MIN, PT. Goes straight onto the website and the score card.
  /stat match player ...        Or enter one player at a time (run again to fix it).
  /exportstats [scope]          Download player stats as a CSV (this tournament or all year).
                                The website shows box scores when you click a game, plus tournament and
                                full-year stat leaders.
  /matches                      List the matches waiting to be played
  /resetevent confirm:True      Delete the current tournament and start over
  /website                      Anyone: link to ontherisepb.com (Ranked + Leaderboard buttons). Staff: also updates it

League website (optional, free, updates itself)
  The bot publishes the draws, standings and brackets to a GitHub Pages site after every change.
  It shows team names, logos, rosters (Discord display names), RISER POINTS and results.
  1. Make a free account at github.com.
  2. New repository -> name it "pbl-league" -> Public -> tick "Add a README file" -> Create.
  3. In the repo: Settings -> Pages -> Source "Deploy from a branch" -> Branch "main", folder "/ (root)" -> Save.
  4. Your profile picture -> Settings -> Developer settings -> Personal access tokens -> Fine-grained tokens
     -> Generate new token. Repository access: "Only select repositories" -> pbl-league.
     Permissions -> Repository permissions -> Contents: "Read and write". Generate, then copy it.
     KEEP IT SECRET, same as the Discord token.
  5. Put pbl_site.html in the same folder as this file.
  6. Start the bot with all three settings (PowerShell, one line):
        $env:DISCORD_TOKEN="..."; $env:GITHUB_TOKEN="..."; $env:GITHUB_REPO="your-github-name/pbl-league"; python pbl_bot.py
  7. In Discord, type /website. Your site is https://your-github-name.github.io/pbl-league/

  Team logos are saved in a "logos" folder next to this file. Keep it with the bot.

One-time setup (about 10 minutes)
  1. Install Python 3.10+ from python.org, then run:   pip install discord.py
  2. Go to https://discord.com/developers/applications -> New Application -> name it "PB Circuit".
  3. Bot tab -> Reset Token -> copy it. KEEP IT SECRET. Don't paste it in chats or post it anywhere.
  3b. Still on the Bot tab: under "Privileged Gateway Intents" turn ON "Server Members Intent" and Save.
      (The bot needs this to give new members the Player role.)
  4. OAuth2 -> URL Generator -> tick "bot" and "applications.commands",
     then under Bot Permissions tick "Administrator". Open the link and add the bot to your server.
  5. In your server: Server Settings -> Roles -> drag the bot's role to the very TOP.
     (A bot can only manage roles below its own.)
  6. Optional, before /setupbot part:server: Server Settings -> Enable Community. This gives you a Stage channel for Finals.
  7. Run the bot with your token:
        Windows (PowerShell):  $env:DISCORD_TOKEN="paste-token-here"; python pbl_bot.py
        Mac/Linux:             DISCORD_TOKEN="paste-token-here" python3 pbl_bot.py
  8. In Discord, type /setupbot part:server. Slash commands can take a minute to appear the first time.

The bot only works while this script is running. Teams and tournaments are saved in signups.json
next to this file, so they survive if you close and restart the bot.
"""

import asyncio
import base64
import csv
import io
import json
import os
import random
import re
import urllib.parse
import secrets
from datetime import datetime, timedelta, timezone
from pathlib import Path

import aiohttp
import discord
from discord import app_commands
from discord.ext import commands

TOKEN = os.environ.get("DISCORD_TOKEN")

# ---------------------------------------------------------------- blueprint

# Top to bottom: (name, color, permissions, show separately in member list)
ROLES = [
    ("Commissioner", 0xF1C40F, discord.Permissions(administrator=True), True),
    ("Director of Enforcement", 0x8E44AD, discord.Permissions(
        manage_messages=True, kick_members=True, moderate_members=True,
        manage_roles=True, manage_nicknames=True, mention_everyone=True), True),  # above League Staff: suspensions are theirs
    ("League Staff", 0xE74C3C, discord.Permissions(
        manage_messages=True, kick_members=True, moderate_members=True,
        manage_roles=True, manage_nicknames=True, mention_everyone=True), True),
    ("Referee", 0xE67E22, discord.Permissions.none(), True),
    ("Team Captain", 0x3498DB, discord.Permissions.none(), False),  # not hoisted: captains stay listed with their team
    ("Co-Captain", 0x5DADE2, discord.Permissions.none(), False),  # not shown as its own group in the member list
    ("Player", 0x2ECC71, discord.Permissions.none(), False),
    ("Free Agent", 0x7BED9F, discord.Permissions.none(), False),
    ("Fan", 0x000000, discord.Permissions.none(), False),
]

# Channel access types:
#   "ro"    everyone reads, only staff post
#   "open"  everyone reads and posts
#   "staff" only staff and referees can see it
#   [roles] everyone reads, only these roles (plus staff) post
TEXT_CHANNELS = [
    ("WELCOME", [("welcome", "ro"), ("rules", "ro"), ("announcements", "ro"), ("get-roles", "ro")]),
    ("LEAGUE", [("standings", "ro"), ("schedule", "ro"), ("game-announcements", "ro"), ("pickems", "ro"), ("bracket", "ro"),
                ("game-finals", "ro"),
                ("rosters", "ro"), ("transactions", "ro")]),
    ("MATCHES", [("game-rules", "ro"), ("scheduling", ["Team Captain", "Co-Captain"]),
                 ("score-reports", ["Team Captain", "Co-Captain", "Referee"]),
                 ("match-disputes", ["Team Captain", "Referee"]),
                 ("highlights", "open")]),
    ("COMMUNITY", [("general", "open"), ("free-agents", ["Free Agent", "Team Captain"]),
                   ("scrims", "captains")]),
    ("STAFF", [("staff-chat", "staff"), ("mod-log", "staff")]),
]

TEAM_COLORS = [0x1ABC9C, 0x9B59B6, 0xE91E63, 0xF39C12, 0x16A085, 0x8E44AD, 0xD35400, 0x2980B9,
               0xC0392B, 0x27AE60, 0x7F8C8D, 0xFF6F61, 0x6C5CE7, 0x00B894, 0xFDCB6E, 0xE17055]

WELCOME_TEXT = """# Welcome to ON THE RISE: PB CIRCUIT
The competitive 5v5 Practical Basketball circuit on Roblox. Every tournament earns your team **RISER POINTS**.
Stack enough of them, or win a tournament outright, and you qualify for the **Major**.

**Get started**
1. Read #rules.
2. **Start a team:** `/signup` with your team name and logo. You're the captain.
3. **Build your roster:** `/offer @player` sends an offer they accept or decline in DMs. 5 to 8 players, one team each.
4. **Enter tournaments:** when entries open in #announcements, captains type `/register`.
5. **No team?** Type `/freeagent` and post in #free-agents so captains can find you.

Track every team in #rosters, the brackets in #bracket, and RISER POINTS with `/points`. See you on the rise."""

# Each card is posted as its own embed in #rules by /setupbot part:rules (edit the text here to change the rules).
RULE_CARDS = [
    ("📜 Server rules", 0xEF4444, [
        "Be respectful. No harassment, slurs, threats or targeting players, teams or staff.",
        "No cheating, exploits, scripts, macros or alt accounts. Ever.",
        "Keep chat in the right channel. No spam, self-promo or DM advertising.",
        "Follow Discord's Terms of Service and Roblox's Community Standards.",
        "Staff decisions are final. Appeal politely with an **Appeal** ticket, never in public chat.",
    ]),
    ("👥 Teams and rosters", 0x3B82F6, [
        "Anyone can create a team with `/signup` (name, position and logo required). The creator is the captain.",
        "Rosters are **5 to 8 players**, captain included. Only complete rosters can register for tournaments.",
        "**One team per player.** Playing for a team you're not rostered on is a forfeit for that team.",
        "Captains sign players with `/offer`; the player accepts or declines in DMs. Players can only play the "
        "position they're listed at unless their captain changes it.",
        "Roster changes **lock** once entries close and stay locked until your team is eliminated.",
        "Team names and logos must be appropriate. Staff can rename or change a logo at any time.",
    ]),
    ("🏆 Tournament formats", 0xE0B44A, [
        "Every tournament needs at least **6 teams**. The top teams by RISER POINTS are seeded (one per group), "
        "the rest are drawn at random. Invite-only events (LCQ, Majors) are fully random.",
        "**Swiss qualifier:** you play a team with the same record each round. **3 wins** = into the main draw, "
        "**3 losses** = eliminated. Byes count as a win.",
        "**Group stage:** teams are drawn into groups (size set by staff), everyone plays everyone in their group once. "
        "The top teams in each group advance (staff announce how many). "
        "Tiebreakers: wins, then head-to-head, then point difference.",
        "**Main draw:** always double elimination. Lose once and you drop to the losers bracket; lose twice "
        "and you're out. If the losers-bracket team wins the Grand Final, it **resets** for one deciding game.",
        "Every match is a single game unless staff announce otherwise for that round.",
    ]),
    ("📅 Scheduling and match day", 0x22C55E, [
        "When your match is posted, captains and co-captains get a DM (game times and reminders too), and both "
        "captains are pinged in #scheduling.",
        "Captains agree a game time with `/gametime` (or `/confirmtime`); the other captain confirms in DMs. "
        "You get **24 hours** in group stages under 16 teams, **12 hours** per game in the main draw, and 48 hours "
        "otherwise. Group stages under 16 teams and the main draw are played inside **3 days**.",
        "No time agreed? **The bot picks one and staff confirm it** (evenings from 8 PM ET, every 30 minutes), spread "
        "out so games don't start at the same time. It can "
        "still be moved, but **both captains must confirm** the new time.",
        "Once a game time passes, it can't be changed. No-show rules apply.",
        "Be in your team voice channel **10 minutes** before game time. The higher seed hosts the private "
        "server and shares the code with the other captain only.",
        "**No-shows:** fewer than 5 players ready **15 minutes** after the set time is a forfeit. "
        "Two forfeits in one tournament and your team is removed.",
        "Reminders are sent 24 hours and 1 hour before game time. Turn match DMs off with `/matchdms`.",
    ]),
    ("🏀 Game rules", 0xA855F7, [
        "5v5 in Practical Basketball, using the game settings in #game-rules. No changes mid-game.",
        "Only rostered, eligible players may play. Subs must come from your own roster.",
        "**Disconnects:** if a player disconnects in the first 2 minutes, the game may be restarted once. "
        "After that, play on, and they can rejoin when they can.",
        "Intentionally crashing, lagging or leaving a game to force a restart is a forfeit.",
        "Play it out. No throwing, no sitting out to make a point, no letting a team win.",
    ]),
    ("📊 Results, stats and disputes", 0x3B82F6, [
        "Within **1 hour** of the game, a captain or co-captain reports the score with `/game_score` (attach the stats "
        "screenshot for a public gym, or the export for a league gym). The other team's captain or co-captain "
        "confirms it. Disputed scores are decided by an admin.",
        "Box score stats go on the website. Wrong stats? Open a **Stats** ticket with a screenshot.",
        "Disputes go in #match-disputes or a ticket within **24 hours**, with a clip or screenshot. "
        "No evidence, no ruling. A Referee decides, staff handle appeals.",
        "Results and stats can't be changed once the next round of that bracket has been played.",
    ]),
    ("⛔ Conduct and suspensions", 0xEF4444, [
        "Breaking the rules can get you a warning, a forfeit, a team removal or a suspension.",
        "Most suspensions are counted in **tournaments**. While suspended you can't create, join or be signed "
        "to a team, register, or play. It counts down each time a tournament's champion is crowned.",
        "Suspensions can block you from the **ranked queue**, from the **league** (teams, sign-ups and "
        "tournaments), or **time you out** server-wide. Every suspension is logged in #suspensions.",
        "Cheating, alt accounts or dodging a suspension (leaving and rejoining, playing on another account) "
        "means a permanent ban from the circuit.",
        "A suspended player can't play for their team. Playing them anyway is a forfeit.",
    ]),
    ("⭐ RISER POINTS and Majors", 0xE0B44A, [
        "Every circuit event awards RISER POINTS by final placement (1st gets 300). Teams that finish in the same "
        "round get the same points. The points table is posted when entries open.",
        "Winners of tournaments marked as Major qualifiers get a spot in the next Major automatically. Everyone "
        "else qualifies by reaching the **points target** (600).",
        "The next **8 teams** below the target are invited to the **Last Chance Qualifier (LCQ)**: the top 4 go to "
        "the Major. Teams tied at the cut-off are all invited and play a single-elimination play-in.",
        "You can miss weeks and still qualify: points stay until the Major.",
        "Points belong to the players who earned them: if fewer than **3** of them stay on the team, the points "
        "are lost.",
        "After each Major, every team's RISER POINTS reset to 0.",
    ]),
]

RULES_TEXT = "\n\n".join(f"**{t}**\n" + "\n".join(f"{i}. {r}" for i, r in enumerate(rs, 1))
                         for t, _c, rs in RULE_CARDS)

# ---------------------------------------------------------------- bot

intents = discord.Intents.default()
intents.members = True  # needed to give new members the Player role (turn on "Server Members Intent")
try:  # long rate limits raise instead of freezing the bot; the bot then retries those itself when they expire
    bot = commands.Bot(command_prefix="!", intents=intents, max_ratelimit_timeout=60.0)
except TypeError:  # older discord.py without that option: it simply waits out every rate limit
    bot = commands.Bot(command_prefix="!", intents=intents)


def rate_limit_wait(ex: Exception) -> float | None:
    """Seconds until Discord lets us try again, if `ex` is a rate limit (else None)."""
    rl = getattr(discord, "RateLimited", None)
    if isinstance(rl, type) and isinstance(ex, rl):
        return float(getattr(ex, "retry_after", 60) or 60)
    if getattr(ex, "status", 0) == 429:
        ra = getattr(ex, "retry_after", None)
        if ra is None:
            try:
                ra = float(ex.response.headers.get("Retry-After", 60))
            except Exception:
                ra = 60.0
        return float(ra)
    return None


def when_free(seconds: float) -> str:
    t = datetime.now(timezone.utc) + timedelta(seconds=seconds)
    return f"<t:{int(t.timestamp())}:t> (<t:{int(t.timestamp())}:R>)"

MIN_TEAMS = 6
DATA_FILE = Path(__file__).with_name("signups.json")


def load_data() -> dict:
    try:
        return json.loads(DATA_FILE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_data(data: dict):
    DATA_FILE.write_text(json.dumps(data, indent=2), encoding="utf-8")


def guild_signups(data: dict, guild_id: int) -> dict:
    s = data.setdefault(str(guild_id), {})
    s.setdefault("open", False)
    s.setdefault("closes", None)
    if not isinstance(s.get("teams"), dict):
        s["teams"] = {}  # teams by role ID (older versions saved a list of pending sign-ups)
    s.setdefault("free_agents", [])  # Discord user IDs
    s.setdefault("offers", {})       # pending contract offers by offer ID
    s.setdefault("tourney", None)    # the tournament taking entries / being played
    s.setdefault("circuit", {"needed": None, "qualified": []})
    s.setdefault("board", [])        # message IDs of the live roster board in #rosters
    s.setdefault("event", None)      # the current tournament (Swiss stage + main draw)
    return s


# ---------------------------------------------------------------- tournament engine
#
# A season's event is saved in signups.json as s["event"]:
#   stage: "swiss" -> "swiss_done" -> "main" -> "done"   (or straight to "main" with no Swiss)
#   swiss: records, matches, qualified/eliminated lists
#   main:  every double-elimination match, with where each slot comes from

RNG = random.SystemRandom()  # fair, unpredictable shuffles


def tag(team_id) -> str:
    if team_id in TEST_NAMES:
        return f"**{TEST_NAMES[team_id]}**"
    return f"<@&{team_id}>" if team_id else "BYE"

def swiss_new(team_ids: list[int], wins: int, losses: int) -> dict:
    return {"wins": wins, "losses": losses, "round": 0, "qualified": [], "eliminated": [], "matches": [],
            "rec": {str(t): {"w": 0, "l": 0, "opp": [], "bye": False} for t in team_ids}}


def swiss_active(sw: dict) -> list[int]:
    return [int(t) for t, r in sw["rec"].items() if r["w"] < sw["wins"] and r["l"] < sw["losses"]]


def swiss_record(sw: dict, winner: int, loser: int | None):
    rw = sw["rec"][str(winner)]
    rw["w"] += 1
    if loser is not None:
        rl = sw["rec"][str(loser)]
        rl["l"] += 1
        rw["opp"].append(loser)
        rl["opp"].append(winner)
        if rl["l"] == sw["losses"]:
            sw["eliminated"].append(loser)
    if rw["w"] == sw["wins"]:
        sw["qualified"].append(winner)


def swiss_pair(sw: dict, teams: list[int]) -> list[tuple]:
    """Pair teams with the same record, never a rematch if it can be avoided."""
    rec = sw["rec"]
    RNG.shuffle(teams)
    teams.sort(key=lambda t: (-rec[str(t)]["w"], rec[str(t)]["l"]))

    def diff(a, b):
        return abs(rec[str(a)]["w"] - rec[str(b)]["w"]) + abs(rec[str(a)]["l"] - rec[str(b)]["l"])

    def solve(lst, allow_rematch, budget):
        if not lst:
            return []
        a, rest = lst[0], lst[1:]
        for b in sorted(rest, key=lambda x: diff(a, x)):
            if not allow_rematch and b in rec[str(a)]["opp"]:
                continue
            budget[0] -= 1
            if budget[0] < 0:
                return None
            sub = solve([x for x in rest if x != b], allow_rematch, budget)
            if sub is not None:
                return [(a, b)] + sub
        return None

    return solve(teams, False, [50000]) or solve(teams, True, [50000])


def swiss_next_round(ev: dict) -> list[str]:
    """Make the next Swiss round. Returns text for #schedule."""
    sw = ev["swiss"]
    rec = sw["rec"]
    active = swiss_active(sw)
    sw["round"] += 1
    lines = [f"## Swiss round {sw['round']}"]
    if sw["round"] == 1 and ev.get("seeds"):  # seeded round 1: top half plays bottom half (1 v 9, 2 v 10...)
        order = [t for t in ev["seeds"] if t in active]
        if len(order) % 2:  # the #1 seed gets the bye
            bye = order.pop(0)
            rec[str(bye)]["bye"] = True
            swiss_record(sw, bye, None)
            lines.append(f"{tag(bye)} gets a bye as the #1 seed (counts as a win)")
        half = len(order) // 2
        for a, b in zip(order[:half], order[half:]):
            mid = ev["next_id"]
            ev["next_id"] += 1
            sw["matches"].append({"id": mid, "round": 1, "a": a, "b": b, "winner": None})
            lines.append(f"**M{mid}**: #{ev['seeds'].index(a) + 1} {tag(a)} vs #{ev['seeds'].index(b) + 1} {tag(b)}")
        return lines
    if len(active) % 2:
        cands = [t for t in active if not rec[str(t)]["bye"]] or active
        worst = min((rec[str(t)]["w"], -rec[str(t)]["l"]) for t in cands)
        bye = RNG.choice([t for t in cands if (rec[str(t)]["w"], -rec[str(t)]["l"]) == worst])
        active.remove(bye)
        rec[str(bye)]["bye"] = True
        swiss_record(sw, bye, None)
        lines.append(f"{tag(bye)} gets a bye (counts as a win)")
    for a, b in swiss_pair(sw, active):
        mid = ev["next_id"]
        ev["next_id"] += 1
        sw["matches"].append({"id": mid, "round": sw["round"], "a": a, "b": b, "winner": None})
        ra, rb = rec[str(a)], rec[str(b)]
        lines.append(f"**M{mid}**: {tag(a)} ({ra['w']}-{ra['l']}) vs {tag(b)} ({rb['w']}-{rb['l']})")
    return lines


def swiss_table(sw: dict) -> list[str]:
    rows = sorted(sw["rec"].items(), key=lambda kv: (-kv[1]["w"], kv[1]["l"]))
    lines = []
    for t, r in rows:
        status = " **QUALIFIED**" if int(t) in sw["qualified"] else " out" if int(t) in sw["eliminated"] else ""
        lines.append(f"`{r['w']}-{r['l']}` {tag(int(t))}{status}")
    blocks = [f"# Swiss standings after round {sw['round']}\n"
              f"{sw['wins']} wins = into the main draw · {sw['losses']} losses = out"]
    blocks += ["\n".join(lines[i:i + 20]) for i in range(0, len(lines), 20)]
    return blocks


# ---- Group stage (round robin; staff pick the group size and how many advance)

GROUP_SIZE_MIN, GROUP_SIZE_MAX = 3, 8


def group_plan(n: int, size: int) -> tuple[int, int, int]:
    """(number of groups, smallest group, biggest group) for n teams in groups of `size`.
    When n doesn't divide evenly some groups get one team fewer."""
    count = max(1, -(-n // size))
    return count, n // count, -(-n // count)


def group_advance_problem(n: int, size: int, advance: int) -> str | None:
    count, small, _big = group_plan(n, size)
    if advance >= small:
        return (f"With {n} teams in groups of {size} you get {count} group(s), the smallest with **{small}** teams. "
                f"Pick an advance number below {small} so somebody goes out (1-{max(1, small - 1)}).")
    if count * advance < 2:
        return "At least 2 teams have to make the main draw. Use smaller groups or let more teams advance."
    return None

def parse_score(score: str | None):
    """'42-38' -> (42, 38) as (winner points, loser points). None if no usable score."""
    nums = re.findall(r"\d+", score or "")
    if len(nums) >= 2:
        x, y = int(nums[0]), int(nums[1])
        return max(x, y), min(x, y)
    return None


def round_robin(teams: list) -> list[list[tuple]]:
    """Every team plays every other once. Returns rounds of (a, b); None means a bye."""
    t = list(teams)
    if len(t) % 2:
        t.append(None)
    n, rounds = len(t), []
    for _ in range(n - 1):
        rounds.append([(t[i], t[n - 1 - i]) for i in range(n // 2)])
        t = [t[0], t[-1]] + t[1:-1]
    return rounds


def groups_new(ev: dict, team_ids: list[int], advance: int, drawn: list[list[int]] | None = None,
               size: int = 4) -> dict:
    """Groups of `size` (some one smaller when the count doesn't divide evenly) and every group match.
    `drawn` = groups already made by the seeded pot draw; otherwise random."""
    if drawn is not None:
        groups = [list(g) for g in drawn]
    else:
        RNG.shuffle(team_ids)
        count = group_plan(len(team_ids), size)[0]
        groups = [[] for _ in range(count)]
        for i, t in enumerate(team_ids):
            groups[i % count].append(t)
    gs = {"advance": advance, "size": max(len(g) for g in groups), "groups": groups, "matches": [], "qualified": [],
          "coin": {str(t): RNG.random() for t in team_ids}}  # last-resort tiebreak, fixed at the draw
    for gi, g in enumerate(groups):
        for r, pairs in enumerate(round_robin(g), 1):
            for a, b in pairs:
                if a is not None and b is not None:
                    mid = ev["next_id"]
                    ev["next_id"] += 1
                    gs["matches"].append({"id": mid, "round": r, "group": gi, "a": a, "b": b,
                                          "winner": None, "score": None, "pts": None})
    return gs


def group_letter(gi: int) -> str:
    return chr(65 + gi)


def group_table(gs: dict, gi: int):
    """Order: wins, then head-to-head among tied teams, then point difference, then the draw's coin flip."""
    teams = gs["groups"][gi]
    ms = [m for m in gs["matches"] if m["group"] == gi]
    st = {t: {"w": 0, "l": 0, "pd": 0, "played": 0} for t in teams}
    for m in ms:
        if m["winner"]:
            w = m["winner"]
            lo = m["b"] if w == m["a"] else m["a"]
            st[w]["w"] += 1
            st[lo]["l"] += 1
            st[w]["played"] += 1
            st[lo]["played"] += 1
            if m["pts"]:
                d = m["pts"][0] - m["pts"][1]
                st[w]["pd"] += d
                st[lo]["pd"] -= d

    def h2h(t):
        tied = {x for x in teams if st[x]["w"] == st[t]["w"]}
        return sum(1 for m in ms if m["winner"] == t and m["a"] in tied and m["b"] in tied)

    order = sorted(teams, key=lambda t: (-st[t]["w"], -h2h(t), -st[t]["pd"], gs["coin"][str(t)]))
    return order, st


def groups_finished(gs: dict) -> bool:
    return all(m["winner"] for m in gs["matches"])


def groups_seeds(gs: dict) -> list[int]:
    """Group winners first, then runners-up, etc. Teams from the same group avoid each other in round 1."""
    tables = [group_table(gs, gi) for gi in range(len(gs["groups"]))]
    home = {t: gi for gi, g in enumerate(gs["groups"]) for t in g}
    stats = {t: st[t] for _order, st in tables for t in st}
    tiers = []
    for pos in range(gs["advance"]):
        tier = [order[pos] for order, _st in tables if pos < len(order)]
        tier.sort(key=lambda t: (-stats[t]["w"], -stats[t]["pd"]))  # best record in each tier seeds higher
        tiers.append(tier)

    def clashes(seeds):
        size = 2
        while size < len(seeds):
            size *= 2
        order = seed_order(size)
        bad = 0
        for k in range(0, size, 2):
            a, b = order[k], order[k + 1]
            if a <= len(seeds) and b <= len(seeds) and home[seeds[a - 1]] == home[seeds[b - 1]]:
                bad += 1
        return bad

    best = None
    width = max((len(t) for t in tiers), default=1)
    for r in range(width):
        rotated = [tiers[0]] + [t[r % len(t):] + t[:r % len(t)] if t else t for t in tiers[1:]]
        seeds = [x for t in rotated for x in t]
        score = clashes(seeds)
        if best is None or score < best[0]:
            best = (score, seeds)
        if score == 0:
            break
    return best[1] if best else []


def group_blocks(gs: dict, gi: int) -> str:
    order, st = group_table(gs, gi)
    lines = [f"**Group {group_letter(gi)}**  (top {gs['advance']} advance)"]
    for pos, t in enumerate(order, 1):
        r = st[t]
        pd = f"{r['pd']:+d}" if r["pd"] else "0"
        mark = " **Q**" if t in gs["qualified"] else ""
        lines.append(f"`{pos}. {r['w']}-{r['l']}  PD {pd}` {tag(t)}{mark}")
    return "\n".join(lines)


# ---- Double-elimination main draw

def seed_order(size: int) -> list[int]:
    """Standard bracket order, e.g. 8 -> [1, 8, 4, 5, 2, 7, 3, 6], so top seeds meet last."""
    order = [1]
    while len(order) < size:
        n = len(order) * 2
        order = [x for s in order for x in (s, n + 1 - s)]
    return order


def de_build(ev: dict, seeds: list[int]) -> dict:
    """Build every match of a double-elimination bracket. Byes fill empty seeds."""
    size = 2
    while size < len(seeds):
        size *= 2
    slots = seeds + [None] * (size - len(seeds))
    order = seed_order(size)
    matches = []

    def add(label, a_src, b_src, gf=0):
        mid = ev["next_id"]
        ev["next_id"] += 1
        matches.append({"id": mid, "label": label, "a_src": a_src, "b_src": b_src, "gf": gf,
                        "a": None, "b": None, "a_ok": False, "b_ok": False,
                        "winner": None, "loser": None, "done": False, "posted": False})
        return mid

    wb = [[add("Winners R1", ["team", slots[order[k] - 1]], ["team", slots[order[k + 1] - 1]])
           for k in range(0, size, 2)]]
    while len(wb[-1]) > 1:
        prev = wb[-1]
        name = "Winners Final" if len(prev) == 2 else f"Winners R{len(wb) + 1}"
        wb.append([add(name, ["W", prev[i]], ["W", prev[i + 1]]) for i in range(0, len(prev), 2)])

    if size == 2:
        lb_final_src = ["L", wb[0][0]]
    else:
        lb = [[add("Losers R1", ["L", wb[0][i]], ["L", wb[0][i + 1]]) for i in range(0, len(wb[0]), 2)]]
        for k in range(1, len(wb)):
            drops = wb[k] if k % 2 else list(reversed(wb[k]))  # mix up drop order to avoid quick rematches
            prev = lb[-1]
            lb.append([add(f"Losers R{len(lb) + 1}", ["W", prev[i]], ["L", drops[i]]) for i in range(len(prev))])
            if len(lb[-1]) > 1:
                p = lb[-1]
                lb.append([add(f"Losers R{len(lb) + 1}", ["W", p[i]], ["W", p[i + 1]]) for i in range(0, len(p), 2)])
        for m in matches:
            if m["id"] == lb[-1][0]:
                m["label"] = "Losers Final"
        lb_final_src = ["W", lb[-1][0]]

    add("Grand Final", ["W", wb[-1][0]], lb_final_src, gf=1)
    return {"matches": matches, "champion": None}


def de_resolve(main: dict):
    """Fill in teams as earlier matches finish, and auto-advance anyone facing a bye."""
    by_id = {m["id"]: m for m in main["matches"]}
    changed = True
    while changed:
        changed = False
        for m in main["matches"]:
            if m["done"]:
                continue
            for side in ("a", "b"):
                if m[side + "_ok"]:
                    continue
                kind, val = m[side + "_src"]
                if kind == "team":
                    m[side], m[side + "_ok"] = val, True
                elif by_id[val]["done"]:
                    m[side] = by_id[val]["winner"] if kind == "W" else by_id[val]["loser"]
                    m[side + "_ok"] = True
                if m[side + "_ok"]:
                    changed = True
            if m["a_ok"] and m["b_ok"] and (m["a"] is None or m["b"] is None):
                m["winner"] = m["a"] if m["a"] is not None else m["b"]
                m["loser"], m["done"], m["posted"] = None, True, True
                changed = True
                if m["gf"] and m["winner"]:
                    main["champion"] = m["winner"]


def de_ready(main: dict) -> list[dict]:
    return [m for m in main["matches"] if not m["done"] and m["a_ok"] and m["b_ok"]]


def slot_text(m: dict, side: str) -> str:
    if m[side + "_ok"]:
        return tag(m[side])
    kind, val = m[side + "_src"]
    return f"{'Winner' if kind == 'W' else 'Loser'} of M{val}"


def de_overview(main: dict) -> list[str]:
    blocks, current, label = [], [], None
    for m in main["matches"]:
        if m["gf"] == 2:
            continue
        if m["label"] != label:
            if current:
                blocks.append("\n".join(current))
            label, current = m["label"], [f"## {m['label']}"]
        if m["done"] and m["winner"] is None:
            continue  # an empty slot facing an empty slot: nothing to show
        if m["done"] and m["loser"] is None:
            current.append(f"M{m['id']}: {tag(m['winner'])} advances (bye)")
        elif m["a_ok"] and m["a"] is None:
            current.append(f"M{m['id']}: {slot_text(m, 'b')} advances (bye)")
        elif m["b_ok"] and m["b"] is None:
            current.append(f"M{m['id']}: {slot_text(m, 'a')} advances (bye)")
        else:
            current.append(f"M{m['id']}: {slot_text(m, 'a')} vs {slot_text(m, 'b')}")
    if current:
        blocks.append("\n".join(current))
    return blocks


def up_next(main: dict) -> list[str]:
    """Matches that just became playable and haven't been announced yet."""
    lines = []
    for m in de_ready(main):
        if not m["posted"]:
            m["posted"] = True
            lines.append(f"**M{m['id']} ({m['label']})**: {tag(m['a'])} vs {tag(m['b'])}")
    return lines


async def send_blocks(channel: discord.TextChannel | None, parts: list[str], color: int = 0xEF4444):
    """Post blocks of text as branded embed cards (a '# Heading' first line becomes the card title)."""
    if channel:
        for chunk in pack(parts, limit=3800):
            await post(channel, chunk, color=color)


def role(guild: discord.Guild, name: str) -> discord.Role | None:
    return discord.utils.get(guild.roles, name=name)


def overwrites_for(guild: discord.Guild, access) -> dict:
    everyone = guild.default_role
    staff = [r for r in (role(guild, DOE), role(guild, "League Staff"), role(guild, "Referee")) if r]
    league_staff = role(guild, "League Staff")
    ow = {guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)}

    if access == "open":
        ow[everyone] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
    elif access == "ro":
        ow[everyone] = discord.PermissionOverwrite(view_channel=True, send_messages=False, add_reactions=True)
        if league_staff:
            ow[league_staff] = discord.PermissionOverwrite(send_messages=True)
        if role(guild, DOE):
            ow[role(guild, DOE)] = discord.PermissionOverwrite(send_messages=True)
    elif access == "captains":  # hidden: only captains, co-captains and staff can see and post
        ow[everyone] = discord.PermissionOverwrite(view_channel=False)
        for name in ("Team Captain", "Co-Captain", "League Staff", DOE, "Commissioner"):
            r = role(guild, name)
            if r:
                ow[r] = discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True)
    elif access == "staff":
        ow[everyone] = discord.PermissionOverwrite(view_channel=False)
        for r in staff:
            ow[r] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
    else:  # list of role names that may post
        ow[everyone] = discord.PermissionOverwrite(view_channel=True, send_messages=False)
        if league_staff:
            ow[league_staff] = discord.PermissionOverwrite(send_messages=True)
        if role(guild, DOE):
            ow[role(guild, DOE)] = discord.PermissionOverwrite(send_messages=True)
        for name in access:
            r = role(guild, name)
            if r:
                ow[r] = discord.PermissionOverwrite(send_messages=True)
    return ow


async def get_or_make_category(guild, name, overwrites=None):
    cat = discord.utils.get(guild.categories, name=name)
    if cat is None:
        cat = await guild.create_category(name, overwrites=overwrites or {})
    return cat


async def post_once(channel: discord.TextChannel, text: str):
    """Post only if the channel is empty, so /setupbot part:server can be re-run safely."""
    async for _ in channel.history(limit=1):
        return
    await post(channel, text)


@bot.event
async def on_ready():
    if not getattr(bot, "_watching", False):
        bot._watching = True
        asyncio.create_task(suspension_watch())  # lifts suspensions when their time is up
        asyncio.create_task(leaders_watch())  # keeps the media stat leaders fresh
        asyncio.create_task(match_watch())  # match DMs, 48-hour scheduling clock, game reminders
    for guild in bot.guilds:
        bot.tree.copy_global_to(guild=guild)
        await bot.tree.sync(guild=guild)
        await cache_invites(guild)  # invite tracker: remember every link's use count
        try:
            await ensure_doe_role(guild)  # Director of Enforcement: made once, above League Staff
        except Exception as e:
            print(f"[{guild.name}] {DOE} role: {e}")
        asyncio.create_task(sync_team_emojis(guild))  # team logo emojis for the media posts
        asyncio.create_task(sync_captains_channel(guild))  # tournament captains channel
        try:
            await sweep_gone_players(guild)  # players who left the server while the bot was off
        except Exception as e:
            print(f"[{guild.name}] left-server sweep: {e}")
        try:
            await ensure_game_announcements(guild)  # matchup graphics for confirmed games
            await ensure_pickems_channel(guild)  # pick'ems: vote who wins each game
        except Exception as e:
            print(f"[{guild.name}] game announcements: {e}")
        try:
            await ensure_pickup_host(guild)  # Pickup Host: @everyone in the pickup channels only
        except Exception as e:
            print(f"[{guild.name}] pickup host: {e}")
        try:
            await ensure_slur_filter(guild)  # Discord AutoMod blocks slurs; the bot adds a 30-minute timeout
        except Exception as e:
            print(f"[{guild.name}] slur filter: {e}")
        try:
            await lock_everyone_pings(guild)  # @everyone/@here: League Staff and up, Media, Streamer only
        except Exception as e:
            print(f"[{guild.name}] everyone pings: {e}")
        try:
            n = await separate_team_roles(guild)
            if n:
                print(f"[{guild.name}] Separated {n} team role(s) in the member list.")
        except Exception as e:
            print(f"[{guild.name}] team roles: {e}")
    print(f"Logged in as {bot.user}. Slash commands ready in {len(bot.guilds)} server(s).")


@bot.event
async def on_member_join(member: discord.Member):
    """Everyone who joins the server gets the Player role."""
    player_role = role(member.guild, "Player")
    if player_role and not member.bot:
        try:
            await member.add_roles(player_role, reason="New member")
        except discord.HTTPException:
            print(f"Couldn't give Player to {member}. Is the bot's role above Player?")


@app_commands.default_permissions(manage_roles=True)
async def give_player_to_all(guild: discord.Guild) -> int:
    """Everyone already in the server gets the Player role (new members get it when they join)."""
    player_role = role(guild, "Player")
    if player_role is None:
        return 0
    given = 0
    async for member in guild.fetch_members(limit=None):
        if not member.bot and player_role not in member.roles:
            try:
                await member.add_roles(player_role, reason="Everyone gets Player")
                given += 1
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.3)
    return given


async def giveplayerrole(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    player_role = role(interaction.guild, "Player")
    if player_role is None:
        return await interaction.response.send_message("Run /setupbot part:server first.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    given = 0
    async for member in interaction.guild.fetch_members(limit=None):
        if not member.bot and player_role not in member.roles:
            try:
                await member.add_roles(player_role, reason="Everyone gets Player")
                given += 1
            except discord.HTTPException:
                pass
            await asyncio.sleep(0.3)
    await interaction.followup.send(f"Gave the Player role to {given} member(s).", ephemeral=True)


@bot.event
async def on_guild_join(guild):
    bot.tree.copy_global_to(guild=guild)
    await bot.tree.sync(guild=guild)


# ---------------------------------------------------------------- /setupbot part:server

# one-time setup: run with /setupbot part:server
async def setup(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    notes = []

    # Roles
    made = {}
    for name, color, perms, hoist in ROLES:
        r = role(guild, name)
        if r is None:
            r = await guild.create_role(name=name, colour=discord.Colour(color), permissions=perms,
                                        hoist=hoist, reason="Circuit setup")
        made[name] = r

    # Put the roles in blueprint order, just under the bot's own role
    top = guild.me.top_role.position
    try:
        await guild.edit_role_positions(
            {made[name]: max(1, top - 1 - i) for i, (name, *_rest) in enumerate(ROLES)})
    except discord.HTTPException:
        notes.append("Couldn't reorder roles. Drag the bot's role to the top and run /setupbot part:server again.")
    await separate_team_roles(guild)  # teams stay their own groups above Players

    asyncio.create_task(give_player_to_all(guild))  # members who joined before the bot get Player too
    # Give the person running /setupbot part:server the Commissioner role
    try:
        await interaction.user.add_roles(made["Commissioner"], reason="Circuit setup")
    except discord.HTTPException:
        notes.append("Couldn't give you Commissioner. Move the bot's role above it and run /setupbot part:server again.")

    # Text channels
    for cat_name, channels in TEXT_CHANNELS:
        cat_ow = overwrites_for(guild, "staff") if cat_name == "STAFF" else None
        cat = await get_or_make_category(guild, cat_name, cat_ow)
        for ch_name, access in channels:
            if discord.utils.get(cat.text_channels, name=ch_name) is None:
                await guild.create_text_channel(ch_name, category=cat,
                                                overwrites=overwrites_for(guild, access))

    # Private TEAMS category (team channels are added with /addteam)
    await get_or_make_category(guild, "TEAMS", overwrites_for(guild, "staff"))

    # Voice
    everyone = guild.default_role
    player, staff_role = made["Player"], made["League Staff"]
    voice = await get_or_make_category(guild, "VOICE")
    for i in range(1, 5):
        name = f"Game Day {i}"
        if discord.utils.get(voice.voice_channels, name=name) is None:
            await guild.create_voice_channel(name, category=voice, overwrites={
                everyone: discord.PermissionOverwrite(view_channel=True, connect=False),
                player: discord.PermissionOverwrite(connect=True, speak=True),
                staff_role: discord.PermissionOverwrite(connect=True, speak=True),
            })
    finals_ow = {
        everyone: discord.PermissionOverwrite(view_channel=True, connect=True, speak=False),
        staff_role: discord.PermissionOverwrite(connect=True, speak=True),
    }
    if discord.utils.get(guild.channels, name="Finals Stage") is None:
        try:
            await guild.create_stage_channel("Finals Stage", category=voice, overwrites=finals_ow)
        except discord.HTTPException:
            await guild.create_voice_channel("Finals Stage", category=voice, overwrites=finals_ow)
            notes.append("Finals Stage was made as a voice channel (turn on Community for a Stage channel).")

    # Posts
    await post_once(discord.utils.get(guild.text_channels, name="welcome"), WELCOME_TEXT)
    rules_ch = discord.utils.get(guild.text_channels, name="rules")
    if rules_ch and not [m async for m in rules_ch.history(limit=1)]:
        await post_rules(rules_ch)
    gr_ch = discord.utils.get(guild.text_channels, name="game-rules")
    if gr_ch and not [m async for m in gr_ch.history(limit=1)]:
        await gr_ch.send(embed=game_rules_embed("📢 League game settings",
                                                "Every ON THE RISE game is played with these settings."))

    msg = ("ON THE RISE: PB CIRCUIT is built. Next: /setupbot part:server, /tournament major_target: to set the Major target, "
           "then /opensignups to open your first tournament.")
    if notes:
        msg += "\n\n" + "\n".join(f"- {n}" for n in notes)
    await interaction.followup.send(msg, ephemeral=True)


# ---------------------------------------------------------------- how the bot's posts look
#
# Every post is an embed card: circuit name + bot avatar at the top, a coloured bar, a title,
# the details, and a footer with the time. Match results get a full "Final Score" card.

BRAND = 0xEF4444
GOOD, INFO, GOLD, MUTED = 0x22C55E, 0x3B82F6, 0xE0B44A, 0x52525B


def brand_embed(text: str | None = None, title: str | None = None, color: int = BRAND,
                url: str | None = None) -> discord.Embed:
    if text and title is None:
        first, _, rest = text.strip().partition("\n")
        if first.startswith("#"):
            title, text = first.lstrip("#").strip(), rest.strip()
        elif first.startswith("**") and first.endswith("**") and len(first) < 120:
            title, text = first.strip("*").strip(), rest.strip()
    e = discord.Embed(title=(title or None) and title[:256], description=(text or None) and text[:4000],
                      colour=color, url=url, timestamp=datetime.now(timezone.utc))
    icon = bot.user.display_avatar.url if bot.user else None
    e.set_author(name=LEAGUE_NAME, icon_url=icon)
    e.set_footer(text="ON THE RISE · PB CIRCUIT", icon_url=icon)
    return e


async def post(channel, text: str | None = None, *, title: str | None = None, color: int = BRAND,
               view=None, file=None, ping: str | None = None, url: str | None = None, allowed_mentions=None):
    """Send `text` as a branded embed card. `file` (a logo) becomes the card's thumbnail."""
    if channel is None:
        return None
    e = brand_embed(text, title, color, url)
    kw = {"embed": e, "allowed_mentions": NO_PINGS}
    if file is not None:
        e.set_thumbnail(url=f"attachment://{file.filename}")
        kw["file"] = file
    if view is not None:
        kw["view"] = view
    if ping:  # a real @mention outside the card, so that one person gets notified
        kw["content"] = ping
        kw["allowed_mentions"] = discord.AllowedMentions(users=True, roles=False, everyone=False)
    return await channel.send(**kw)


def match_label(ev: dict, m: dict) -> str:
    if m.get("label"):
        return m["label"]
    if "group" in m:
        return f"Group {group_letter(m['group'])} · Round {m['round']}"
    if "round" in m:
        return f"Swiss · Round {m['round']}"
    return f"M{m['id']}"


def potg_score(line: dict) -> float:
    """How good a game was: points, assists, rebounds, steals and blocks."""
    return (line.get("pts", 0) + 1.2 * line.get("ast", 0) + 0.8 * line.get("reb", 0)
            + 1.5 * line.get("stl", 0) + 1.5 * line.get("blk", 0))


def players_of_the_game(m: dict) -> dict:
    """A Player of the Game for EACH team: {team id: (player key, line)}, from the box score ({} if none)."""
    out = {}
    for tid in (m.get("a"), m.get("b")):
        rows = {k: v for k, v in (m.get("box") or {}).items() if v.get("team") == tid}
        if rows:
            out[tid] = max(rows.items(), key=lambda kv: potg_score(kv[1]))
    return out


def potg_stats(p: dict) -> str:
    extra = "".join(f" / {p[k]} {k.upper()}" for k in ("stl", "blk") if p.get(k))
    return f"{p['pts']} PTS / {p['reb']} REB / {p['ast']} AST{extra}"


def who(key) -> str:
    return f"<@{key}>" if str(key).isdigit() else f"**{key}**"


def score_card(s: dict, ev: dict, m: dict, reporter: int | None = None) -> discord.Embed:
    tz = s.get("tourney") or {}
    tname = tz.get("name", "Tournament")
    w = m.get("winner")
    lo = m["b"] if w == m["a"] else m["a"]
    sc = m.get("score") or ""
    sw, sl = sc.split("-", 1) if "-" in sc else ("W", "L")
    lines = ["**Scoreline**",
             f"**W** · {tag(w)} · **{sw}**",
             f"**L** · {tag(lo)} · {sl}"]
    potg = players_of_the_game(m)
    if potg:
        lines += ["", "**Players of the Game**"] + [
            f"**{team_name(s, tid)}:** {who(potg[tid][0])} · {potg_stats(potg[tid][1])}" for tid in (w, lo) if tid in potg]
    else:
        lines += ["", "*Box score not entered yet. Referees: `/stat`.*"]
    if reporter:
        lines += ["", "**Reported by**", f"<@{reporter}>"]
    url = (site_url() or None) and f"{site_url()}#m{m['id']}"
    e = brand_embed("\n".join(lines), f"Final Score · {tname} · {match_label(ev, m)}", GOOD, url)
    e.set_author(name=f"{LEAGUE_NAME}: {tname}", icon_url=bot.user.display_avatar.url if bot.user else None)
    return e


def box_button(m: dict):
    if not site_url():
        return None
    v = discord.ui.View(timeout=None)
    v.add_item(discord.ui.Button(label="View Full Box Score", style=discord.ButtonStyle.link,
                                 url=f"{site_url()}#m{m['id']}"))
    return v


def match_heading(ev: dict | None, m: dict) -> str:
    """'Group A · round 2', 'Swiss round 3', 'Winners R1', 'Consolation Final'... for any match."""
    if m.get("label"):
        return m["label"]
    if "group" in m:
        return f"Group {group_letter(m['group'])} · round {m.get('round', 1)}"
    if ev and ev.get("swiss") and m in ev["swiss"]["matches"]:
        return f"Swiss round {m.get('round', 1)}"
    return "Match"


def _fit(d, text: str, max_w: int, size: int, min_size: int = 18):
    f = _font(size)
    while size > min_size and d.textlength(text, font=f) > max_w:
        size -= 2
        f = _font(size)
    return f


def final_score_picture(s: dict, ev: dict, m: dict, pname=str) -> bytes:
    """The FINAL SCORE graphic: both team logos, the score, the winner, and each team's Player of the Game."""
    from PIL import Image, ImageDraw
    W, H = 1600, 900
    tz = s.get("tourney") or {}
    tname = tz.get("name", "Tournament")
    tlogo = str(LOGO_DIR / tz["logo"]) if tz.get("logo") and (LOGO_DIR / tz["logo"]).exists() else None
    heading = stage_heading(match_heading(ev, m), m["id"])
    img, d = _canvas(W, H, tname, "Final score · " + heading.title().replace("Game M", "Game M"), tlogo)
    WHITE, GREY, DIM, ORANGE, GREEN = (245, 245, 245), (150, 150, 155), (90, 90, 96), (255, 122, 0), (74, 222, 128)
    w = m.get("winner")
    a, b = m["a"], m["b"]
    sc = parse_score(m.get("score")) or (0, 0)
    pts = {w: max(sc), (b if w == a else a): min(sc)} if w else {a: 0, b: 0}
    d.text((W / 2 - d.textlength("FINAL", font=_font(34)) / 2, 232), "FINAL", font=_font(34), fill=GREY)
    rec = lambda t: "-".join(map(str, team_record(ev, t)))
    for t, cx in ((a, 300), (b, W - 300)):
        tm = s["teams"].get(str(t), {})
        name = tm.get("name", "TBD")
        won = t == w
        lg = _logo((LOGO_DIR / tm["logo"]) if tm.get("logo") else None, 270, name)
        if not won and w:  # fade the loser's logo a little
            alpha = lg.getchannel("A").point(lambda v: int(v * .55))
            lg.putalpha(alpha)
        if won:  # orange ring around the winner
            ring = Image.new("RGBA", (294, 294), (0, 0, 0, 0))
            ImageDraw.Draw(ring).ellipse((0, 0, 293, 293), outline=ORANGE, width=7)
            img.paste(ring, (int(cx - 147), 233), ring)
        img.paste(lg, (int(cx - 135), 245), lg)
        nf = _fit(d, name.upper(), 470, 46)
        d.text((cx - d.textlength(name.upper(), font=nf) / 2, 540), name.upper(), font=nf, fill=WHITE if won else GREY)
        sub = f"{rec(t)} in {tname}" if ev else ""
        if sub:
            f2 = _font(22, bold=False)
            d.text((cx - d.textlength(sub, font=f2) / 2, 600), sub, font=f2, fill=GREY)
        if won:
            pf = _font(24)
            tw = d.textlength("WIN", font=pf)
            d.rounded_rectangle((cx - tw / 2 - 18, 640, cx + tw / 2 + 18, 678), 8, fill=ORANGE)
            d.text((cx - tw / 2, 645), "WIN", font=pf, fill=(20, 20, 20))
    la, lb = str(pts.get(a, 0)), str(pts.get(b, 0))
    big = _fit(d, max(la, lb, key=len), 270, 190, 120)  # 3-digit scores shrink so they don't hit the logos
    sy = 300 + (190 - big.size) * 0.45 if hasattr(big, "size") else 300
    d.text((W / 2 - 60 - d.textlength(la, font=big), sy), la, font=big, fill=WHITE if a == w else DIM)
    d.text((W / 2 + 60, sy), lb, font=big, fill=WHITE if b == w else DIM)
    d.rectangle((W / 2 - 22, 400, W / 2 + 22, 412), fill=ORANGE)
    # Players of the Game
    d.line((50, 712, W - 50, 712), fill=(40, 40, 44), width=2)
    potg = players_of_the_game(m)  # one per team, under that team's side
    if potg:
        for tid, x0 in ((a, 50), (b, W / 2 + 20)):
            if tid not in potg:
                continue
            key, p = potg[tid]
            label = "PLAYER OF THE GAME · " + s["teams"].get(str(tid), {}).get("name", "TBD").upper()
            d.text((x0, 732), label, font=_fit(d, label, W / 2 - 90, 22, 14), fill=ORANGE if tid == w else GREY)
            nm = pname(key)
            d.text((x0, 764), nm, font=_fit(d, nm, W / 2 - 90, 38), fill=WHITE)
            d.text((x0, 812), potg_stats(p).replace(" / ", " · "), font=_font(24, bold=False), fill=GREY)
    else:
        msg = "Box score coming soon at ontherisepb.com"
        f3 = _font(26, bold=False)
        d.text((W / 2 - d.textlength(msg, font=f3) / 2, 765), msg, font=f3, fill=GREY)
    return _png(img)


def next_match_for(ev: dict | None, tid) -> dict | None:
    """The team's next playable match ({id, a, b, label}), or None."""
    for x in open_matches(ev):
        if tid in (x["a"], x["b"]):
            return x
    return None


async def post_next_up(guild: discord.Guild, s: dict, ev: dict, m: dict):
    """After a result: both teams' channels get the final score and who they play next."""
    w = m.get("winner")
    sc = m.get("score") or ""
    for tid in (m.get("a"), m.get("b")):
        t = s["teams"].get(str(tid))
        ch = guild.get_channel(int((t or {}).get("channel") or 0)) if t else None
        if ch is None:
            continue
        other = m["b"] if tid == m["a"] else m["a"]
        head = ("✅ **Win!** " if tid == w else "**Loss.** ") + f"M{m['id']} final: **{team_name(s, w)}** won {sc} vs " \
               f"**{team_name(s, other if tid == w else tid)}**."
        nxt = next_match_for(ev, tid)
        if nxt:
            opp = nxt["b"] if nxt["a"] == tid else nxt["a"]
            body = (f"\n\n**Up next: M{nxt['id']}** vs **{team_name(s, opp)}** ({nxt['label']}).\n"
                    f"Captains: agree a time with `/gametime match:{nxt['id']}` (you'll get a DM too).")
        elif (ev.get("main") or {}).get("champion") == tid:
            body = "\n\n🏆 **Champions!** That's the tournament."
        else:
            body = "\n\nNo next game yet: it depends on other results. You'll get a DM as soon as your next match is set."
        try:
            await ch.send(embed=brand_embed(head + body, f"Final · M{m['id']}", GOOD if tid == w else MUTED),
                          allowed_mentions=NO_PINGS)
        except discord.HTTPException:
            pass


# ---------------------------------------------------------------- #game-finals: graphic + a short recap
#
# Every result posts the Final Score graphic in #game-finals with a few lines about the game: how close it was,
# each team's Player of the Game, what it means (records, qualified / eliminated) and who they play next.
# When box score stats come in later (/stat, imports), the post is redrawn with the Players of the Game.

def game_synopsis(s: dict, ev: dict, m: dict, pname=str) -> str:
    rnd = random.Random(m["id"])  # same wording every time this game is redrawn
    w = m.get("winner")
    lo = m["b"] if w == m["a"] else m["a"]
    W_, L_ = f"**{team_name(s, w)}**", f"**{team_name(s, lo)}**"
    sc = parse_score(m.get("score"))
    lines = []
    if sc:
        hi, low = max(sc), min(sc)
        gap = hi - low
        if gap >= 20:
            lead = rnd.choice([f"{W_} ran away with it, beating {L_} **{hi}-{low}**.",
                               f"No contest: {W_} blew out {L_} **{hi}-{low}**.",
                               f"{W_} were in control from start to finish and won by {gap}, **{hi}-{low}** over {L_}."])
        elif gap >= 10:
            lead = rnd.choice([f"{W_} handled {L_} **{hi}-{low}**.",
                               f"A comfortable **{hi}-{low}** win for {W_} over {L_}.",
                               f"{W_} pulled away from {L_} for a **{hi}-{low}** win."])
        elif gap >= 4:
            lead = rnd.choice([f"{W_} beat {L_} **{hi}-{low}**.",
                               f"{W_} got past {L_} **{hi}-{low}**.",
                               f"{W_} held off {L_}, **{hi}-{low}**."])
        else:
            lead = rnd.choice([f"What a finish. {W_} edged {L_} **{hi}-{low}**.",
                               f"Down to the wire: {W_} survived {L_} **{hi}-{low}**.",
                               f"{W_} won a nail-biter, **{hi}-{low}** over {L_}."])
    else:
        lead = f"{W_} beat {L_}."
    lines.append(lead)
    potg = players_of_the_game(m)
    def stat_words(p):
        bits = [f"{p['pts']} points"]
        if p.get("reb", 0) >= 5:
            bits.append(f"{p['reb']} rebounds")
        if p.get("ast", 0) >= 4:
            bits.append(f"{p['ast']} assists")
        if p.get("stl", 0) >= 3:
            bits.append(f"{p['stl']} steals")
        if p.get("blk", 0) >= 3:
            bits.append(f"{p['blk']} blocks")
        return ", ".join(bits[:-1]) + (" and " if len(bits) > 1 else "") + bits[-1]
    if w in potg:
        k, p = potg[w]
        lines.append(rnd.choice([f"**{pname(k)}** led the way with {stat_words(p)}.",
                                 f"**{pname(k)}** was the Player of the Game for {W_} with {stat_words(p)}.",
                                 f"{W_} rode **{pname(k)}**: {stat_words(p)}."]))
    if lo in potg:
        k, p = potg[lo]
        lines.append(rnd.choice([f"For {L_}, **{pname(k)}** had {stat_words(p)}.",
                                 f"**{pname(k)}** put up {stat_words(p)} for {L_} in the loss.",
                                 f"{L_}{chr(39) if team_name(s, lo).endswith('s') else chr(39) + 's'} best was **{pname(k)}** with {stat_words(p)}."]))
    # what it means
    sw = ev.get("swiss")
    if sw and m in sw["matches"]:
        rw, rl = sw["rec"][str(w)], sw["rec"][str(lo)]
        lines.append(f"{W_} move to **{rw['w']}-{rw['l']}**" + (" and **qualify for the main draw**" if w in sw["qualified"]
                                                               else "") + f"; {L_} drop to **{rl['w']}-{rl['l']}**"
                     + (" and are **out**." if lo in sw["eliminated"] else "."))
    elif "group" in m:
        a_w, a_l = team_record(ev, w)
        b_w, b_l = team_record(ev, lo)
        lines.append(f"In Group {group_letter(m['group'])}, {W_} improve to **{a_w}-{a_l}** and {L_} fall to **{b_w}-{b_l}**.")
    else:
        lab = match_heading(ev, m)
        main = ev.get("main") or {}
        if main.get("champion") == w and m in main.get("matches", []):
            lines.append(f"🏆 {W_} are the **champions** of {(s.get('tourney') or {}).get('name', 'the tournament')}!")
        elif (ev.get("consolation") or {}).get("champion") == w and m in ev["consolation"]["matches"]:
            lines.append(f"{W_} win the **consolation bracket**.")
        elif lab.startswith("Grand"):
            lines.append(f"{W_} win the first Grand Final from the losers bracket, so it **resets**: one more game decides it.")
        elif lab.startswith("Losers") or lab.startswith("Consolation"):
            lines.append(f"{L_} are **eliminated**. {W_} stay alive.")
        elif lab.startswith("Winners"):
            lines.append(f"{W_} stay in the winners bracket; {L_} drop to the losers bracket.")
        elif lab.startswith("LCQ play-in"):
            lines.append(f"{W_} move on in the LCQ play-in; {L_} are out.")
    nxt = next_match_for(ev, w)
    if nxt:
        opp = nxt["b"] if nxt["a"] == w else nxt["a"]
        lines.append(f"Up next for {W_}: **M{nxt['id']}** vs **{team_name(s, opp)}**.")
    return "\n\n".join(lines)


async def final_score_png(guild: discord.Guild, s: dict, ev: dict, m: dict) -> bytes | None:
    def pname(k):
        mem = guild.get_member(int(k)) if str(k).isdigit() else None
        return mem.display_name if mem else str(k)
    try:
        return await asyncio.to_thread(final_score_picture, s, ev, m, pname)
    except ImportError:
        return None
    except Exception as e:
        print(f"[final score picture] {e}")
        return None


async def game_finals_channel(guild: discord.Guild):
    ch = chan(guild, "game-finals")
    if ch is None:
        try:
            cat = discord.utils.get(guild.categories, name="LEAGUE")
            ch = await guild.create_text_channel("game-finals", category=cat, overwrites=overwrites_for(guild, "ro"),
                                                 topic="Every final score, with a quick recap of the game.")
        except discord.HTTPException:
            return None
    return ch


async def post_game_final(guild: discord.Guild, s: dict, ev: dict, m: dict, edit: bool = False):
    """Post (or, after stats come in, redraw) the game's graphic + recap in #game-finals."""
    def pname(k):
        mem = guild.get_member(int(k)) if str(k).isdigit() else None
        return mem.display_name if mem else str(k)
    tz = s.get("tourney") or {}
    e = brand_embed(game_synopsis(s, ev, m, pname),
                    f"FINAL · {stage_heading(match_heading(ev, m), m['id']).title()}", GOOD)
    e.set_author(name=f"{LEAGUE_NAME}: {tz.get('name', 'Tournament')}")
    _se = sched(s)["matches"].get(str(m["id"]), {})
    if _se.get("stream_link"):  # where it was streamed, so people can catch the replay
        _by = _se.get("stream_name") or (pname(_se["stream"]) if _se.get("stream") else "the stream")
        e.add_field(name="Watch the replay", value=f"[{stream_platform(_se['stream_link'])} · {_by}]({_se['stream_link']})", inline=False)
    png = await final_score_png(guild, s, ev, m)
    f = discord.File(io.BytesIO(png), filename=f"final_M{m['id']}.png") if png else None
    if f:
        e.set_image(url=f"attachment://{f.filename}")
    v = box_button(m)
    try:
        if edit and m.get("final_post"):
            ch = guild.get_channel(m["final_post"][0])
            if ch is None:
                return
            msg = await ch.fetch_message(m["final_post"][1])
            await msg.edit(embed=e, attachments=[f] if f else [])
            return
        ch = await game_finals_channel(guild)
        if ch is None:
            return
        kw = {"embed": e, "allowed_mentions": NO_PINGS}
        if f:
            kw["file"] = f
        if v:
            kw["view"] = v
        msg = await ch.send(**kw)
        m["final_post"] = [ch.id, msg.id]
    except discord.HTTPException as ex:
        print(f"[game finals] {ex}")


# ---------------------------------------------------------------- #game-analysis: a written breakdown of each game
#
# Once a game has a result AND a box score (export, CSV or /stat), the bot writes 6-9 sentences in
# #game-analysis: how it went, the shooting and the stat battles, who starred, who struggled, and what it means.
# Re-importing stats rewrites the same post.

def _fg(l):
    return l.get("fg2m", 0) + l.get("fg3m", 0), l.get("fg2a", 0) + l.get("fg3a", 0)


def _pct(m_, a_):
    return 100 * m_ / a_ if a_ else 0.0


def team_box(m: dict, tid) -> dict:
    tot = {k: 0 for k in ("pts", "fg2m", "fg2a", "fg3m", "fg3a", "ftm", "fta", "reb", "orb", "drb", "ast", "stl",
                          "blk", "to")}
    for ln in (m.get("box") or {}).values():
        if ln.get("team") == tid:
            for k in tot:
                tot[k] += ln.get(k, 0) or 0
    return tot


def stat_line(l: dict) -> str:
    fm, fa = _fg(l)
    bits = [f"{l.get('pts', 0)} points" + (f" on {fm}/{fa}" if fa else "")]
    if l.get("reb", 0) >= 5:
        bits.append(f"{l['reb']} rebounds")
    if l.get("ast", 0) >= 4:
        bits.append(f"{l['ast']} assists")
    if l.get("stl", 0) + l.get("blk", 0) >= 3:
        bits.append(f"{l.get('stl', 0)} steals and {l.get('blk', 0)} blocks")
    return ", ".join(bits[:-1]) + (" and " if len(bits) > 1 else "") + bits[-1]


def game_analysis_text(s: dict, ev: dict, m: dict, pname) -> str | None:
    box = m.get("box") or {}
    w = m.get("winner")
    if not box or not w or m.get("a") is None or m.get("b") is None:
        return None
    lo = m["b"] if w == m["a"] else m["a"]
    W, L = f"**{team_name(s, w)}**", f"**{team_name(s, lo)}**"
    sc = m.get("pts") or parse_score(m.get("score"))
    margin = int(sc[0]) - int(sc[1]) if sc else None
    tw, tl = team_box(m, w), team_box(m, lo)
    lines = {"w": [(u, l) for u, l in box.items() if l.get("team") == w],
             "l": [(u, l) for u, l in box.items() if l.get("team") == lo]}
    out = []
    head = stage_heading(match_heading(ev, m), m["id"]).title()
    # 1. the result
    if margin is None:
        out.append(f"{W} beat {L} in {head}.")
    elif margin >= 20:
        out.append(f"This one was never close: {W} ran {L} off the floor, {m['score']}, in {head}.")
    elif margin >= 10:
        out.append(f"{W} handled {L} comfortably, winning {m['score']} in {head}.")
    elif margin <= 3:
        out.append(f"{W} survived a thriller against {L}, {m['score']}, in {head}.")
    else:
        out.append(f"{W} got past {L} {m['score']} in {head}, but it was a fight.")
    # 2. shooting
    wfm, wfa = _fg(tw)
    lfm, lfa = _fg(tl)
    if wfa and lfa:
        wp, lp = _pct(wfm, wfa), _pct(lfm, lfa)
        w3, l3 = _pct(tw["fg3m"], tw["fg3a"]), _pct(tl["fg3m"], tl["fg3a"])
        if abs(wp - lp) >= 8:
            better, worse = (W, L) if wp > lp else (L, W)
            out.append(f"The shooting told the story: {better} hit {max(wp, lp):.0f}% from the field while {worse} "
                       f"managed just {min(wp, lp):.0f}%.")
        else:
            out.append(f"Both teams shot it about the same ({wp:.0f}% to {lp:.0f}%), so it came down to the details.")
        if tw["fg3a"] + tl["fg3a"] >= 10 and abs(tw["fg3m"] - tl["fg3m"]) >= 3:
            nm3, a_, b_ = (W, tw, tl) if tw["fg3m"] > tl["fg3m"] else (L, tl, tw)
            out.append(f"{nm3} won the three-point battle {a_['fg3m']}-{b_['fg3m']} "
                       f"({_pct(a_['fg3m'], a_['fg3a']):.0f}% vs {_pct(b_['fg3m'], b_['fg3a']):.0f}%).")
    # 3. the other battles
    edges = []
    if abs(tw["reb"] - tl["reb"]) >= 6:
        edges.append(f"{W if tw['reb'] > tl['reb'] else L} owned the glass {max(tw['reb'], tl['reb'])}-{min(tw['reb'], tl['reb'])}")
    if abs(tw["to"] - tl["to"]) >= 4:
        sloppy, n = (W, tw["to"]) if tw["to"] > tl["to"] else (L, tl["to"])
        edges.append(f"{sloppy} were sloppy with {n} turnovers")
    if abs(tw["ast"] - tl["ast"]) >= 6:
        edges.append(f"{W if tw['ast'] > tl['ast'] else L} moved the ball better ({max(tw['ast'], tl['ast'])} assists "
                     f"to {min(tw['ast'], tl['ast'])})")
    if edges:
        out.append((edges[0][0].upper() + edges[0][1:]) + ("; " + edges[1] if len(edges) > 1 else "") + ".")
    # 4-5. the stars
    def best(ls):
        return max(ls, key=lambda x: (x[1].get("pts", 0) + 0.7 * x[1].get("reb", 0) + x[1].get("ast", 0)
                                      + 1.5 * (x[1].get("stl", 0) + x[1].get("blk", 0)) - x[1].get("to", 0)), default=None)
    bw, bl = best(lines["w"]), best(lines["l"])
    if bw:
        out.append(f"{pname(bw[0])} was the best player on the floor for {W} with {stat_line(bw[1])}.")
    if bl and bl[1].get("pts", 0) >= 10:
        out.append(f"{pname(bl[0])} tried to keep {L} in it with {stat_line(bl[1])}, but didn't get enough help.")
    elif bl:
        out.append(f"{pname(bl[0])} led {L} with {stat_line(bl[1])}.")
    # 6. who struggled
    strugglers = []
    for side, ls in lines.items():
        for u, l in ls:
            fm, fa = _fg(l)
            if (bw and u == bw[0]) or (bl and u == bl[0]):
                continue
            if fa >= 8 and _pct(fm, fa) < 35:
                strugglers.append((_pct(fm, fa) - 2 * fa, u, l, f"went {fm}/{fa} from the field"
                                   + (f" ({l.get('fg3m', 0)}/{l.get('fg3a', 0)} from three)" if l.get("fg3a", 0) >= 4 else "")))
            elif l.get("to", 0) >= 4:
                strugglers.append((40 - 3 * l["to"], u, l, f"turned it over {l['to']} times"))
    struggler = None
    if strugglers:
        _k, u, l, what = min(strugglers, key=lambda x: x[0])
        struggler = u
        team_ = W if l.get("team") == w else L
        out.append(f"On the other end of it, {pname(u)} had a night to forget for {team_} and {what}.")
    # 7. the glue guy
    glue = [(l.get("stl", 0) + l.get("blk", 0), l.get("ast", 0), u, l) for u, l in box.items()
            if (not bw or u != bw[0]) and (not bl or u != bl[0]) and u != struggler]
    glue = [g for g in glue if g[0] >= 3 or g[1] >= 6]
    if glue:
        d_, a_, u, l = max(glue, key=lambda x: (x[0] * 2 + x[1]))
        team_ = W if l.get("team") == w else L
        out.append(f"{pname(u)} quietly did the dirty work for {team_}" + (f" with {l.get('stl', 0)} steals and "
                   f"{l.get('blk', 0)} blocks." if d_ >= 3 else f", dishing {a_} assists."))
    # 8. what it means
    rec = {r["tid"]: r for r in power_table(s, ev)}
    rw, rl = rec.get(w), rec.get(lo)
    if rw and rl:
        out.append(f"{W} move to {rw['w']}-{rw['l']}" + (" and look dangerous" if rw["l"] == 0 and rw["w"] >= 2 else "")
                   + f", while {L} fall to {rl['w']}-{rl['l']}"
                   + (" and are running out of chances." if rl["l"] >= 2 and rl["l"] > rl["w"] else "."))
    return " ".join(out[:9])


async def analysis_channel(guild: discord.Guild, s: dict):
    c = media(s)["chans"]
    ch = guild.get_channel(c.get("analysis") or 0) or discord.utils.get(guild.text_channels, name="🧠｜game-analysis") \
        or chan(guild, "game-analysis")
    if ch is None:
        try:
            cat = guild.get_channel(c.get("category") or 0) or discord.utils.get(guild.categories, name="MEDIA") \
                or discord.utils.get(guild.categories, name="LEAGUE")
            ch = await guild.create_text_channel("🧠｜game-analysis", category=cat, overwrites=overwrites_for(guild, "ro"),
                                                 topic="A breakdown of every game that has stats: who starred, who struggled.")
        except discord.HTTPException:
            return None
    return ch


async def post_game_analysis(guild: discord.Guild, s: dict, ev: dict, m: dict):
    """Write (or rewrite) the game's breakdown in #game-analysis once it has a result and a box score."""
    def pname(k):
        mem = guild.get_member(int(k)) if str(k).isdigit() else None
        return mem.display_name if mem else str(k)
    text = game_analysis_text(s, ev, m, pname)
    if not text:
        return
    e = brand_embed(text, f"🧠 Game analysis · {team_name(s, m['a'])} vs {team_name(s, m['b'])}", INFO)
    e.set_author(name=stage_heading(match_heading(ev, m), m["id"]).title())
    e.set_footer(text="Written automatically from the box score · full stats on the website")
    try:
        if m.get("analysis_post"):
            ch = guild.get_channel(m["analysis_post"][0])
            if ch:
                msg = await ch.fetch_message(m["analysis_post"][1])
                await msg.edit(embed=e)
                return
        ch = await analysis_channel(guild, s)
        if ch is None:
            return
        msg = await ch.send(embed=e, allowed_mentions=NO_PINGS)
        m["analysis_post"] = [ch.id, msg.id]
        d2 = load_data()  # keep the post id even if the caller doesn't save
        for x in all_matches(guild_signups(d2, guild.id).get("event")):
            if x["id"] == m["id"]:
                x["analysis_post"] = m["analysis_post"]
        save_data(d2)
    except discord.HTTPException as ex:
        print(f"[game analysis] {ex}")
    finally:
        save_analysis_feed(guild, s, ev, m, text)


def save_analysis_feed(guild: discord.Guild, s: dict, ev: dict, m: dict, text: str):
    """The website's Media tab keeps the latest game breakdowns (same text as #game-analysis)."""
    try:
        d2 = load_data()
        s2 = guild_signups(d2, guild.id)
        tname = (s2.get("tourney") or {}).get("name", "")
        feed = [x for x in s2.get("analysis_feed", []) if not (x["id"] == m["id"] and x.get("tournament") == tname)]
        feed.insert(0, {"id": m["id"], "tournament": tname, "a": team_name(s, m["a"]), "b": team_name(s, m["b"]),
                        "winner": team_name(s, m["winner"]), "score": m.get("score"),
                        "head": stage_heading(match_heading(ev, m), m["id"]).title(), "text": site_text(text),
                        "at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
        s2["analysis_feed"] = feed[:40]
        save_data(d2)
        schedule_publish(guild)
    except Exception as ex:
        print(f"[analysis feed] {ex}")


async def post_score_card(guild: discord.Guild, s: dict, ev: dict, m: dict, reporter: int | None):
    """Post the Final Score card in #score-reports and remember it so /stat can update it."""
    ch = chan(guild, "score-reports")
    if ch is None:
        return
    e = score_card(s, ev, m, reporter)
    kw = {"embed": e, "allowed_mentions": NO_PINGS}
    t = s["teams"].get(str(m.get("winner")), {})  # the big graphic goes in #game-finals; here, the winner's logo
    f = logo_file(t) if t else None
    if f:
        e.set_thumbnail(url=f"attachment://{f.filename}")
    if f:
        kw["file"] = f
    v = box_button(m)
    if v:
        kw["view"] = v
    msg = await ch.send(**kw)
    m["card"] = [ch.id, msg.id, reporter]


async def refresh_score_card(guild: discord.Guild, s: dict, ev: dict, m: dict):
    """After /stat, redraw the card (and the #game-finals post) so the Players of the Game show up."""
    try:
        await post_game_analysis(guild, s, ev, m)  # #game-analysis: written once the stats are in
    except Exception as ex:
        print(f"[game analysis] {ex}")
    if m.get("final_post"):
        await post_game_final(guild, s, ev, m, edit=True)
    if not m.get("card"):
        return
    ch_id, msg_id, reporter = m["card"]
    ch = guild.get_channel(ch_id)
    if ch is None:
        return
    try:
        msg = await ch.fetch_message(msg_id)
        e = score_card(s, ev, m, reporter)
        if msg.attachments:  # keep the winner's logo
            e.set_thumbnail(url=f"attachment://{msg.attachments[0].filename}")
        await msg.edit(embed=e)
    except discord.HTTPException:
        pass


# ---------------------------------------------------------------- teams
#
# Each team is saved in signups.json under s["teams"][<team role id>]:
#   name, captain (Discord ID), logo (file in the logos folder), channel (ID),
#   roster: {Discord ID: ""}  (the captain is on the roster too), points, core, board_msg

NO_PINGS = discord.AllowedMentions.none()
ROSTER_MIN, ROSTER_MAX = 5, 8
LOGO_DIR = Path(__file__).with_name("logos")
LOGO_TYPES = {"image/png": "png", "image/jpeg": "jpg", "image/webp": "webp", "image/gif": "gif"}
LOGO_MAX_BYTES = 1_000_000


POSITIONS = [("PG", "PG · Point Guard"), ("SG", "SG · Shooting Guard"), ("SF", "SF · Small Forward"),
             ("PF", "PF · Power Forward"), ("C", "C · Center")]


def pos_of(s: dict, uid) -> str | None:
    return s.setdefault("positions", {}).get(str(uid))


def pos_tag(s: dict, uid) -> str:
    p = pos_of(s, uid)
    return f" · {p}" if p else ""


def team_list(s: dict) -> list[tuple[str, dict]]:
    return sorted(s["teams"].items(), key=lambda kv: kv[1]["name"].lower())


def team_roles(guild: discord.Guild) -> list[discord.Role]:
    s = guild_signups(load_data(), guild.id)
    return [r for key, _t in team_list(s) if (r := guild.get_role(int(key)))]


def team_of(s: dict, user_id: int) -> str | None:
    """The team key a player is on, or None."""
    for key, t in s["teams"].items():
        if str(user_id) in t["roster"]:
            return key
    return None


def captain_team(s: dict, user_id: int) -> str | None:
    for key, t in s["teams"].items():
        if t["captain"] == user_id:
            return key
    return None


def signer_team(s: dict, user_id: int) -> str | None:
    """The team this person can sign players for: their own team if they're captain or co-captain."""
    key = captain_team(s, user_id)
    if key:
        return key
    for key, t in s["teams"].items():
        if t.get("co") == user_id:
            return key
    return None


async def get_cocaptain_role(guild: discord.Guild):
    r = role(guild, "Co-Captain")
    if r is None:
        try:
            r = await guild.create_role(name="Co-Captain", colour=discord.Colour(0x5DADE2), hoist=False,
                                        reason="Co-captains")
        except discord.HTTPException:
            return None
    return r




async def reply_after(interaction: discord.Interaction, text: str):
    """Answer a deferred command. If the channel it was used in got deleted (e.g. disbanding a team from
    the team's own channel), send the answer by DM instead."""
    try:
        await interaction.followup.send(text, ephemeral=True, allowed_mentions=NO_PINGS)
    except discord.HTTPException:
        try:
            await interaction.user.send(embed=brand_embed(text, None, BRAND))
        except discord.HTTPException:
            pass


@bot.tree.error
async def on_app_command_error(interaction: discord.Interaction, error: app_commands.AppCommandError):
    """One place for command errors: no scary tracebacks for things that are fine, a short note for the rest."""
    import traceback
    orig = getattr(error, "original", error)
    if isinstance(error, app_commands.CheckFailure):
        msg = "You don't have permission to use that command."
    elif isinstance(orig, discord.NotFound) and getattr(orig, "code", None) in (10003, 10008, 10062):
        # 10003/10008: the channel or message is gone (usually deleted by the command itself)
        # 10062: the interaction expired, usually because two copies of the bot are running
        print(f"[note] /{interaction.command.name if interaction.command else '?'}: {orig.text} (ignored)")
        return
    else:
        print(f"[error] /{interaction.command.name if interaction.command else '?'}:")
        traceback.print_exception(type(orig), orig, orig.__traceback__)
        msg = "Something went wrong running that command. Staff can check the bot window for details."
    try:
        if interaction.response.is_done():
            await interaction.followup.send(msg, ephemeral=True)
        else:
            await interaction.response.send_message(msg, ephemeral=True)
    except discord.HTTPException:
        pass


def is_staff(member: discord.Member) -> bool:
    return member.guild_permissions.administrator or any(
        r.name in ("Commissioner", DOE, "League Staff") for r in member.roles)


DOE = "Director of Enforcement"


def is_enforcer(member) -> bool:
    """Who can hand out and lift suspensions: the Director of Enforcement, or Commissioner and above."""
    return is_commissioner(member) or any(r.name == DOE for r in getattr(member, "roles", []))


PING_ROLES = ("Media", "Streamer")  # below League Staff, but still allowed to use @everyone / @here


def may_ping_everyone(guild: discord.Guild, r: discord.Role) -> bool:
    """League Staff and every role above it, plus Media and Streamer."""
    ls = role(guild, "League Staff")
    if r.name in PING_ROLES or r.permissions.administrator:
        return True
    return ls is not None and r.position >= ls.position


# ---------------------------------------------------------------- SLUR FILTER
# Discord's own AutoMod "slurs" word list blocks the message before anyone sees it (it also catches common
# misspellings). Discord won't let that list time people out by itself, so the bot does: 30 minutes.
SLUR_RULE = "OTR slur filter"
SLUR_TIMEOUT = timedelta(minutes=30)
_slur_rule_ids: dict[int, int] = {}


async def ensure_slur_filter(guild: discord.Guild):
    log = chan(guild, "mod-log")
    actions = [discord.AutoModRuleAction(custom_message="Slurs aren't allowed here. You've been timed out for 30 minutes.")]
    if log:
        actions.append(discord.AutoModRuleAction(channel_id=log.id))  # staff see what was said in #mod-log
    try:
        rules = await guild.fetch_automod_rules()
    except discord.Forbidden:
        print(f"[{guild.name}] slur filter: give the bot the Manage Server permission so it can set up AutoMod.")
        return
    # a server can only have one "word list" (preset) rule: use it if it's already there
    preset = next((r for r in rules if r.trigger.type == discord.AutoModRuleTriggerType.keyword_preset), None)
    if preset is None:
        rule = await guild.create_automod_rule(
            name=SLUR_RULE, event_type=discord.AutoModRuleEventType.message_send,
            trigger=discord.AutoModTrigger(presets=discord.AutoModPresets(slurs=True)),
            actions=actions, enabled=True, reason="Block slurs (the bot adds a 30-minute timeout)")
        print(f"[{guild.name}] Made the AutoMod slur filter.")
    else:
        pr = preset.trigger.presets
        if not pr.slurs or not preset.enabled:
            new = discord.AutoModPresets(slurs=True, profanity=pr.profanity, sexual_content=pr.sexual_content)
            keep = [a for a in preset.actions if a.type != discord.AutoModRuleActionType.block_message]
            if log and not any(a.type == discord.AutoModRuleActionType.send_alert_message for a in keep):
                keep.append(discord.AutoModRuleAction(channel_id=log.id))
            preset = await preset.edit(trigger=discord.AutoModTrigger(presets=new, allow_list=preset.trigger.allow_list),
                                       actions=[actions[0]] + keep, enabled=True,
                                       reason="Block slurs (the bot adds a 30-minute timeout)")
            print(f"[{guild.name}] Turned on slurs in the existing AutoMod word-list rule.")
        if pr.profanity or pr.sexual_content:
            print(f"[{guild.name}] Note: the AutoMod word-list rule also blocks "
                  + ", ".join(n for n, on in (("swearing", pr.profanity), ("sexual words", pr.sexual_content)) if on)
                  + ", so those get the 30-minute timeout too.")
        rule = preset
    _slur_rule_ids[guild.id] = rule.id


@bot.event
async def on_automod_action(execution: discord.AutoModAction):
    """AutoMod blocked a slur: time the sender out for 30 minutes, tell them, note it in #mod-log."""
    guild = execution.guild
    if guild is None or execution.action.type != discord.AutoModRuleActionType.block_message:
        return  # one action per message (AutoMod sends an event for each of the rule's actions)
    if _slur_rule_ids.get(guild.id) != execution.rule_id:
        return
    member = execution.member or guild.get_member(execution.user_id)
    if member is None:
        try:
            member = await guild.fetch_member(execution.user_id)
        except discord.HTTPException:
            return
    if member.bot:
        return
    data = load_data()
    s = guild_signups(data, guild.id)
    strikes = s.setdefault("slur_strikes", {})
    strikes[str(member.id)] = strikes.get(str(member.id), 0) + 1
    n = strikes[str(member.id)]
    save_data(data)
    where = f"<#{execution.channel_id}>" if execution.channel_id else "a channel"
    done = True
    try:
        if not member.is_timed_out():  # several blocked messages in a row only start the clock once
            await member.timeout(SLUR_TIMEOUT, reason="Used a slur (AutoMod)")
    except discord.Forbidden:
        done = False  # staff above the bot's role, or the server owner
    except discord.HTTPException as e:
        done = False
        print(f"[slur filter] {e}")
    if done:
        try:
            await member.send(embed=brand_embed(
                f"You were timed out in **{guild.name}** for **30 minutes** for using a slur. "
                "Slurs aren't allowed anywhere in the server. More of this can lead to a suspension.",
                "Timed out · 30 minutes", BRAND))
        except discord.HTTPException:
            pass
    log = chan(guild, "mod-log")
    if log:
        await post(log, f"{member.mention} used a slur in {where} (AutoMod blocked it; the message is in the "
                        f"AutoMod alert above).\n"
                        + ("**Timed out for 30 minutes.**" if done else
                           "**Couldn't time them out** (their role is above the bot's, or they own the server).")
                        + f"\nSlur strikes: **{n}**" + (" · consider a suspension (/suspend)." if n >= 3 else "."),
                   title="Slur filter", color=BRAND)


async def lock_everyone_pings(guild: discord.Guild) -> list[str]:
    """Only League Staff and up, Media and Streamer can @everyone / @here. Everyone else loses it, in the role
    settings and in any channel that had it turned on for them. Returns what changed."""
    changed = []
    top = guild.me.top_role.position
    for r in guild.roles:
        if r.managed or r.position >= top:
            continue  # bot roles, and roles above the bot (the bot can't edit those)
        want = may_ping_everyone(guild, r) and not r.is_default()
        if r.permissions.mention_everyone != want:
            if not want or r.name in PING_ROLES or r.name in ("League Staff", DOE):
                perms = discord.Permissions(r.permissions.value)
                perms.mention_everyone = want
                try:
                    await r.edit(permissions=perms, reason="@everyone pings: League Staff and up, Media, Streamer only")
                    changed.append(f"{'+' if want else '-'} {r.name}")
                    await asyncio.sleep(0.4)
                except discord.HTTPException:
                    pass
    for ch in guild.channels:  # channel settings can't turn it back on for anyone else
        for target, ow in list(ch.overwrites.items()):
            if ow.mention_everyone is not True:
                continue
            if isinstance(target, discord.Role):
                ok = (may_ping_everyone(guild, target) and not target.is_default()) or \
                    (target.name == PICKUP_HOST and in_pickup_category(guild, ch))
            else:
                ok = is_staff(target) or any(x.name in PING_ROLES for x in getattr(target, "roles", []))
            if not ok:
                ow.mention_everyone = None
                try:
                    await ch.set_permissions(target, overwrite=ow, reason="@everyone pings locked down")
                    changed.append(f"#{ch.name}: {getattr(target, 'name', target)}")
                    await asyncio.sleep(0.4)
                except discord.HTTPException:
                    pass
    if not guild.me.guild_permissions.mention_everyone and not guild.me.guild_permissions.administrator:
        print(f"[{guild.name}] The bot's own role can't @everyone: turn on 'Mention @everyone' for it.")
    if changed:
        print(f"[{guild.name}] @everyone pings: " + ", ".join(changed))
    return changed


# ---------------------------------------------------------------- Pickup Host: @everyone in the pickup category only
#
# The Pickup Host role can @everyone / @here ONLY in the pickup (10 MANS) channels, and only once an hour:
# right after a ping the bot takes the permission away from that host for an hour, then gives it back.

PICKUP_HOST = "Pickup Host"
HOST_COOLDOWN = timedelta(hours=1)


def pickup_category_id(guild: discord.Guild) -> int | None:
    return pug(guild_signups(load_data(), guild.id)).get("chans", {}).get("category")


def in_pickup_category(guild: discord.Guild, ch) -> bool:
    cid = pickup_category_id(guild)
    return bool(cid) and (getattr(ch, "id", None) == cid or getattr(ch, "category_id", None) == cid)


def pickup_text_channels(guild: discord.Guild) -> list:
    cat = guild.get_channel(pickup_category_id(guild) or 0)
    return list(cat.text_channels) if cat else []


async def ensure_pickup_host(guild: discord.Guild):
    """Make the Pickup Host role (no @everyone anywhere by itself) and allow it in the pickup channels."""
    r = role(guild, PICKUP_HOST)
    if r is None:
        try:
            r = await guild.create_role(name=PICKUP_HOST, colour=discord.Colour(0x14B8A6), hoist=False,
                                        reason="Pickup Host: @everyone in the pickup channels, once an hour")
            print(f"[{guild.name}] Made the {PICKUP_HOST} role.")
        except discord.HTTPException:
            return
    p = pug(guild_signups(load_data(), guild.id))
    ann = p.get("chans", {}).get("announcements")
    for ch in pickup_text_channels(guild):
        ow = ch.overwrites.get(r) or discord.PermissionOverwrite()
        want_send = True if ch.id == ann else ow.send_messages  # hosts can post their ping in the announcements
        if ow.mention_everyone is not True or ow.send_messages != want_send:
            ow.mention_everyone = True
            ow.send_messages = want_send
            try:
                await ch.set_permissions(r, overwrite=ow, reason="Pickup Host can @everyone here")
                await asyncio.sleep(0.4)
            except discord.HTTPException:
                pass


def host_cooldowns(s: dict) -> dict:
    return pug(s).setdefault("host_cd", {})  # user id -> when their @everyone comes back (iso)


async def set_host_block(guild: discord.Guild, member, block: bool):
    """Turn a host's own @everyone off (block) or back on in every pickup channel."""
    for ch in pickup_text_channels(guild):
        try:
            if block:
                ow = ch.overwrites.get(member) or discord.PermissionOverwrite()
                ow.mention_everyone = False
                await ch.set_permissions(member, overwrite=ow, reason="Pickup Host @everyone cooldown (1 hour)")
            else:
                ow = ch.overwrites.get(member)
                if ow is None:
                    continue
                ow.mention_everyone = None
                await ch.set_permissions(member, overwrite=None if ow.is_empty() else ow,
                                         reason="Pickup Host @everyone cooldown over")
            await asyncio.sleep(0.3)
        except discord.HTTPException:
            pass


@bot.listen("on_message")
async def pickup_host_ping(message: discord.Message):
    """A Pickup Host used @everyone/@here in the pickup channels: start their 1-hour cooldown."""
    if not message.guild or message.author.bot or not message.mention_everyone:
        return
    member = message.author
    roles = getattr(member, "roles", [])
    if not any(r.name == PICKUP_HOST for r in roles) or any(may_ping_everyone(message.guild, r) for r in roles
                                                              if not r.is_default()):
        return  # not a host, or staff/media who can ping anyway
    if not in_pickup_category(message.guild, message.channel):
        return
    guild = message.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    until = datetime.now(timezone.utc) + HOST_COOLDOWN
    host_cooldowns(s)[str(member.id)] = until.isoformat(timespec="seconds")
    save_data(data)
    await set_host_block(guild, member, True)
    try:
        await member.send(embed=brand_embed(f"Your @everyone in **{guild.name}**'s pickup channels went out. You can "
                                            f"ping again {ts(until, 'R')} ({ts(until, 't')}).",
                                            "Pickup ping sent", INFO))
    except discord.HTTPException:
        pass


async def host_cooldown_once(guild: discord.Guild):
    """Give hosts their @everyone back once their hour is up."""
    data = load_data()
    s = guild_signups(data, guild.id)
    cds = host_cooldowns(s)
    now = datetime.now(timezone.utc)
    done = [u for u, t in cds.items() if datetime.fromisoformat(t) <= now]
    if not done:
        return
    for u in done:
        cds.pop(u, None)
    save_data(data)
    for u in done:
        member = guild.get_member(int(u))
        if member:
            await set_host_block(guild, member, False)


@app_commands.describe(member="Who", remove="Set True to take the role away")
@app_commands.default_permissions(manage_roles=True)
async def pickuphost(interaction: discord.Interaction, member: discord.Member, remove: bool = False):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    await ensure_pickup_host(guild)
    r = role(guild, PICKUP_HOST)
    if r is None:
        return await interaction.followup.send("I couldn't make the Pickup Host role. Move my role to the top.",
                                               ephemeral=True)
    try:
        if remove:
            await member.remove_roles(r, reason=f"By {interaction.user}")
        else:
            await member.add_roles(r, reason=f"By {interaction.user}")
    except discord.HTTPException:
        return await interaction.followup.send("I couldn't change their roles. Move my role above Pickup Host.",
                                               ephemeral=True)
    if not pickup_text_channels(guild):
        note = " Note: there's no pickup category yet. Run `/setupbot part:ranked` first."
    else:
        note = ""
    await interaction.followup.send(
        f"{member.mention} {'is no longer' if remove else 'is now'} a Pickup Host." + ("" if remove else
        " They can @everyone / @here in the pickup channels, once an hour.") + note,
        ephemeral=True, allowed_mentions=NO_PINGS)


async def ensure_doe_role(guild: discord.Guild):
    """Servers set up before this role existed: make it, put it right above League Staff, and give it
    League Staff's access in every channel (staff channels, team channels, voice)."""
    ls = role(guild, "League Staff")
    doe = role(guild, DOE)
    if ls is None:
        return
    if doe is None:
        name, color, perms, hoist = next(r for r in ROLES if r[0] == DOE)
        doe = await guild.create_role(name=name, colour=discord.Colour(color), permissions=perms, hoist=hoist,
                                      reason="Director of Enforcement")
        print(f"[{guild.name}] Made the {DOE} role.")
    want = ls.position + 1
    if doe.position < want and want < guild.me.top_role.position:
        try:
            await doe.edit(position=want, reason="Director of Enforcement sits above League Staff")
        except discord.HTTPException:
            print(f"[{guild.name}] Couldn't move {DOE} above League Staff. Drag the bot's role higher.")
    added = 0
    for ch in guild.channels:  # same access as League Staff wherever League Staff has its own setting
        ow = ch.overwrites
        if ls in ow and doe not in ow:
            try:
                await ch.set_permissions(doe, overwrite=ow[ls], reason="Director of Enforcement access")
                added += 1
                await asyncio.sleep(0.4)
            except discord.HTTPException:
                pass
    if added:
        print(f"[{guild.name}] Gave {DOE} access to {added} channel(s).")


ADMIN_ROLE_WORDS = ("commissioner", "admin", "owner")  # role names that count as Commissioner-level


def is_commissioner(member) -> bool:
    """Only the Commissioner or an admin can sign players or enter teams for someone else: the server owner,
    anyone with the Administrator permission, or a role whose name has Commissioner, Admin or Owner in it."""
    if getattr(member, "guild_permissions", None) is None:
        return False
    if member.guild_permissions.administrator:
        return True
    g = getattr(member, "guild", None)
    if g is not None and getattr(g, "owner_id", None) == member.id:
        return True
    return any(w in r.name.lower() for r in member.roles for w in ADMIN_ROLE_WORDS)


def roster_locked(s: dict) -> bool:
    """Rosters freeze once the main draw starts, until the tournament ends."""
    ev = s["event"]
    return bool(ev and ev["stage"] == "main")


def tournament_running(s: dict) -> bool:
    ev = s["event"]
    return bool(ev and ev["stage"] != "done")


def current_busy(s: dict) -> bool:
    """The current tournament is past entries and not finished yet (entries closed, drawing or being played)."""
    tz = s.get("tourney")
    ev = s.get("event")
    if not tz or s.get("open"):
        return False
    return ev is None or ev.get("stage") != "done" or cons_running(ev)


def signup_target(s: dict) -> tuple[dict | None, bool, bool]:
    """Where /register and /unregister go: (tournament, entries open?, is it the NEXT tournament?).
    While one tournament is being played, captains sign up for the next one."""
    up = s.get("upcoming")
    if up and current_busy(s):
        return up, bool(up.get("open")), True
    return s.get("tourney"), bool(s.get("open")), False


async def promote_upcoming(guild: discord.Guild) -> bool:
    """The current tournament is over (and has been for 10 minutes, so its wrap-up posts go out first):
    the next tournament becomes the current one, with the teams that already registered."""
    data = load_data()
    s = guild_signups(data, guild.id)
    up = s.get("upcoming")
    if not up or current_busy(s):
        if up and up.get("ready_since"):
            up.pop("ready_since")
            save_data(data)
        return False
    now = datetime.now(timezone.utc)
    if not up.get("ready_since"):
        up["ready_since"] = now.isoformat(timespec="seconds")
        save_data(data)
        return False
    if now - datetime.fromisoformat(up["ready_since"]) < timedelta(minutes=10):
        return False
    archive_event(guild, s)  # last tournament's stats into the year table / website archive
    s.pop("upcoming")
    open_ = up.pop("open", True)
    s["open"], s["closes"], s["closes_at"] = open_, up.pop("closes", None), up.pop("closes_at", None)
    up.pop("ready_since", None)
    up["entrants"] = [k for k in up["entrants"] if k in s["teams"]]
    s["tourney"], s["event"] = up, None
    save_data(data)
    await update_board(guild, data)
    ann = chan(guild, "announcements")
    if ann:
        names = ", ".join(f"**{s['teams'][k]['name']}**" for k in up["entrants"]) or "none yet"
        await post(ann, f"# {up['name']} is up next!\n**{len(up['entrants'])} teams** already registered: {names}\n"
                        + ("Entries are still open: captains, `/register`." if open_ else
                           "Entries are closed. The draw is coming soon."), file=logo_file(up))
    print(f"[{guild.name}] {up['name']} is now the current tournament.")
    return True


async def log_transaction(guild: discord.Guild, text: str, team: dict | None = None):
    """Post to #transactions. Pass the team so its logo shows on the card."""
    ch = discord.utils.get(guild.text_channels, name="transactions")
    if ch:
        await post(ch, text, title="Transaction", color=INFO, file=logo_file(team) if team else None)


async def save_logo(att: discord.Attachment) -> tuple[str | None, str | None]:
    """Check and save an uploaded logo. Returns (filename, None) or (None, problem)."""
    kind = (att.content_type or "").split(";")[0].strip().lower()
    if kind not in LOGO_TYPES:
        return None, "The logo has to be an image: PNG, JPG, WEBP or GIF."
    if att.size > LOGO_MAX_BYTES:
        return None, "The logo is too big. Keep it under 1 MB (a 512x512 PNG is perfect)."
    LOGO_DIR.mkdir(exist_ok=True)
    filename = f"{secrets.token_hex(6)}.{LOGO_TYPES[kind]}"
    (LOGO_DIR / filename).write_bytes(await att.read())
    return filename, None


def logo_file(t: dict) -> discord.File | None:
    if t.get("logo") and (LOGO_DIR / t["logo"]).exists():
        return discord.File(LOGO_DIR / t["logo"], filename=t["logo"])
    return None


async def give_roles(guild: discord.Guild, user_id: int, *roles, remove: bool = False):
    try:
        member = await guild.fetch_member(user_id)
    except discord.HTTPException:
        return  # they left the server
    roles = [r for r in roles if r]
    try:
        if remove:
            await member.remove_roles(*[r for r in roles if r in member.roles])
        else:
            await member.add_roles(*roles)
    except discord.HTTPException:
        pass


async def make_team_voice(guild: discord.Guild, category, team: discord.Role, name: str):
    """The team's own voice channel: the team can join and talk, staff can join, everyone else can't see it."""
    ow = {guild.default_role: discord.PermissionOverwrite(view_channel=False, connect=False),
          guild.me: discord.PermissionOverwrite(view_channel=True, connect=True, manage_channels=True, move_members=True),
          team: discord.PermissionOverwrite(view_channel=True, connect=True, speak=True, stream=True)}
    for rn in ("Commissioner", DOE, "League Staff", "Referee"):
        r = role(guild, rn)
        if r:
            ow[r] = discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)
    try:
        return await guild.create_voice_channel(f"🔊 {name}", category=category, overwrites=ow)
    except discord.HTTPException:
        return None


def team_role_floor(guild: discord.Guild) -> int:
    """Team roles go just above Player / Free Agent / Team Captain / Co-Captain, so a player is listed under
    their team (not under Team Captain or Players). Staff roles stay above."""
    base = [r.position for r in (role(guild, n) for n in ("Player", "Free Agent", "Team Captain", "Co-Captain")) if r]
    return (max(base) + 1) if base else 1


async def place_team_role(guild: discord.Guild, team: discord.Role, hoist: bool = True):
    want = team_role_floor(guild)
    if team.position < want - 1 or team.hoist != hoist:
        try:
            top = guild.me.top_role.position
            await team.edit(hoist=hoist, position=min(want, top - 1),
                            reason="Team still playing: own group in the member list" if hoist else
                            "Team not playing right now: listed with everyone else")
        except discord.HTTPException:
            print(f"Couldn't move the {team.name} role. Put the bot's role near the top of the role list.")


ONLY_ACTIVE_TEAMS_SHOWN = True  # member list: only teams still playing get their own group (False = every team)


def active_team_ids(s: dict) -> set[int]:
    """Teams shown as their own group in the member list: entered in the tournament taking sign-ups, or still
    alive in the one being played (out of the qualifier, consolation or main draw = not shown). Between
    tournaments only the last champion is shown."""
    if not ONLY_ACTIVE_TEAMS_SHOWN:
        return {int(k) for k in s["teams"]}
    tz = s.get("tourney") or {}
    ev = s.get("event") or {}
    entrants = {int(k) for k in tz.get("entrants", []) if k in s["teams"]}
    if not ev:
        return entrants if s.get("open") else set()
    if ev.get("stage") == "done" and not cons_running(ev):
        champ = (ev.get("main") or {}).get("champion")
        return {champ} if champ else set()
    alive = set(entrants) or {int(t) for t in ev.get("seeds", [])}
    sw, gs, main = ev.get("swiss"), ev.get("groups"), ev.get("main")
    if sw:
        alive -= {int(t) for t in sw.get("eliminated", [])}
    if gs and (ev.get("stage") != "groups"):
        alive &= {int(t) for t in gs.get("qualified", []) + ev.get("byes", [])} | {int(t) for t in (main and [x for m in main["matches"]
                                                                                    for x in (m.get("a"), m.get("b")) if x] or [])}
    if main:
        losses = {}
        for m in main["matches"]:
            if m["done"] and m.get("loser") is not None:
                losses[m["loser"]] = losses.get(m["loser"], 0) + 1
        alive -= {t for t, n in losses.items() if n >= 2}
        if main.get("champion"):
            alive = {main["champion"]}
    cons = ev.get("consolation")
    if cons and cons_running(ev):
        in_cons = {x for m in cons["matches"] for x in (m.get("a"), m.get("b")) if x}
        out_cons = {m["loser"] for m in cons["matches"] if m.get("winner") and m.get("loser")}
        alive |= in_cons - out_cons
    return {t for t in alive if str(t) in s["teams"]}


_hoist_lock: dict[int, asyncio.Lock] = {}


async def sync_team_hoist(guild: discord.Guild) -> int:
    """Show only the teams still playing as their own group in the member list. Returns how many changed."""
    lock = _hoist_lock.setdefault(guild.id, asyncio.Lock())
    async with lock:
        s = guild_signups(load_data(), guild.id)
        active = active_team_ids(s)
        changed = 0
        for key in s["teams"]:
            r = guild.get_role(int(key))
            if r is None:
                continue
            want = int(key) in active
            if r.hoist != want:
                await place_team_role(guild, r, hoist=want)
                changed += 1
                await asyncio.sleep(0.5)
        return changed


async def separate_team_roles(guild: discord.Guild) -> int:
    """Make every team role its own group in the member list (for teams made before this existed)."""
    s = guild_signups(load_data(), guild.id)
    fixed = 0
    tc = role(guild, "Team Captain")
    if tc and tc.hoist:  # a hoisted Team Captain role would pull captains out of their team's group
        try:
            await tc.edit(hoist=False, reason="Captains are listed with their team")
        except discord.HTTPException:
            pass
    active = active_team_ids(s)
    for key in s["teams"]:
        r = guild.get_role(int(key))
        want = int(key) in active
        if r and (r.hoist != want or r.position < team_role_floor(guild) - 1):
            await place_team_role(guild, r, hoist=want)
            fixed += 1
    return fixed


async def create_team(guild: discord.Guild, data: dict, name: str, captain: discord.Member, logo: str) -> str:
    """Make the team role + private channel, save it, and give the captain their roles. Returns the team key."""
    s = guild_signups(data, guild.id)
    color = TEAM_COLORS[len(s["teams"]) % len(TEAM_COLORS)]
    # hoist=True: the team shows as its own group in the member list, separate from Players
    team = await guild.create_role(name=name, colour=discord.Colour(color), hoist=True, reason="New team")
    await place_team_role(guild, team)
    player_role = role(guild, "Player")
    teams_cat = await get_or_make_category(guild, "TEAMS", overwrites_for(guild, "staff"))
    ow = overwrites_for(guild, "staff")
    ow[team] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
    channel = await guild.create_text_channel(name, category=teams_cat, overwrites=ow,
                                              topic=f"Team role ID: {team.id}")
    key = str(team.id)
    voice = await make_team_voice(guild, teams_cat, team, name)
    s["teams"][key] = {"name": name, "captain": captain.id, "logo": logo, "channel": channel.id,
                       "voice": voice.id if voice else None,
                       "roster": {str(captain.id): ""}, "points": 0, "core": []}
    if captain.id in s["free_agents"]:
        s["free_agents"].remove(captain.id)
    save_data(data)

    await captain.add_roles(*[r for r in (team, role(guild, "Team Captain"), player_role) if r])
    fa = role(guild, "Free Agent")
    if fa and fa in captain.roles:
        await captain.remove_roles(fa)
    f = logo_file(s["teams"][key])
    await post(channel, f"Captain: {captain.mention}\n"
                       f"Captain, offer spots with `/offer @player`. You need {ROSTER_MIN} to {ROSTER_MAX} players "
                       "including you, and nobody can be on two teams. Once you have "
                       f"{ROSTER_MIN}, your team shows up in #rosters and on the website, and you can "
                       "`/register` for tournaments.", title=f"Welcome to {name}", file=f)
    return key


async def delete_team(guild: discord.Guild, data: dict, key: str, reason: str):
    s = guild_signups(data, guild.id)
    t = s["teams"].pop(key, None)
    if t:
        tz = s.get("tourney")
        added = []
        if tz and key in tz.get("entrants", []):
            tz["entrants"].remove(key)
            if not (s.get("event") and s["event"].get("stage") not in (None, "done")):
                added = lcq_fill(s)
        if key in circuit(s)["qualified"]:
            circuit(s)["qualified"].remove(key)
        if added:
            asyncio.create_task(lcq_announce_next_up(guild, s, added))
        for oid in [k for k, o in s["offers"].items() if o["team"] == key]:
            s["offers"].pop(oid)
    save_data(data)
    if not t:
        return
    rosters = chan(guild, "rosters")
    if rosters and t.get("board_msg"):
        try:
            await (await rosters.fetch_message(t["board_msg"])).delete()
        except discord.HTTPException:
            pass
    for uid in t["roster"]:
        await give_roles(guild, int(uid), role(guild, "Team Captain"), role(guild, "Co-Captain"), remove=True)
    for cid in (t.get("channel"), t.get("voice")):
        ch = guild.get_channel(cid or 0)
        if ch:
            try:
                await ch.delete(reason=reason)
            except discord.HTTPException:
                pass
    team = guild.get_role(int(key))
    if team:
        try:
            await team.delete(reason=reason)
        except discord.HTTPException:
            pass
    await log_transaction(guild, f"Team removed: **{t['name']}** ({reason})", t)


async def remove_member(guild: discord.Guild, data: dict, key: str, user_id: int, how: str) -> str:
    """Take a player off a team. Passes on the captaincy, disbands an empty team, and checks RISER POINTS."""
    s = guild_signups(data, guild.id)
    t = s["teams"].get(key)
    if not t or str(user_id) not in t["roster"]:
        return "They're not on that team."
    t["roster"].pop(str(user_id))
    if not t["roster"]:
        await delete_team(guild, data, key, "last player left")
        return f"<@{user_id}> left and **{t['name']}** had no players left, so the team was disbanded."
    note = ""
    if t.get("co") == user_id:
        t["co"] = None
    if t["captain"] == user_id:
        # the co-captain steps up if there is one
        t["captain"] = t["co"] if t.get("co") and str(t["co"]) in t["roster"] else int(next(iter(t["roster"])))
        if t.get("co") == t["captain"]:
            t["co"] = None
            await give_roles(guild, t["captain"], role(guild, "Co-Captain"), remove=True)
        await give_roles(guild, t["captain"], role(guild, "Team Captain"))
        note = f" <@{t['captain']}> is the new captain."
    lost = check_core(s, key)
    if lost:
        note += f"\n{lost}"
    save_data(data)
    await give_roles(guild, user_id, guild.get_role(int(key)), role(guild, "Team Captain"), role(guild, "Co-Captain"),
                     remove=True)
    text = f"<@{user_id}> {how} **{t['name']}**.{note}"
    await log_transaction(guild, text, t)
    ch = guild.get_channel(t.get("channel") or 0)
    if ch:
        await post(ch, text, title="Roster update", color=INFO)
    return text

def render_board(s: dict) -> str:
    """The summary message at the top of #rosters."""
    tz = s.get("tourney")
    c = circuit(s)
    complete = [t for _k, t in team_list(s) if is_complete(t)]
    building = len(s["teams"]) - len(complete)
    lines = [f"# {LEAGUE_NAME}: teams",
             f"**{len(s['teams'])} team(s)** shown below: {len(complete)} complete"
             + (f", {building} still building their roster (they need {ROSTER_MIN} players to /register)"
                if building else "") + "."]
    if c["needed"] is not None:
        lines.append(f"**Major:** {c['needed']} RISER POINTS to qualify. Winners of Major-qualifier events qualify automatically.")
    if tz:
        state = "taking entries" if s["open"] else "entries closed"
        lines.append(f"**Current tournament:** {tz['name']} ({'MAJOR' if tz['kind'] == 'major' else 'circuit event'}"
                     f", {state}) · {len([k for k in tz['entrants'] if k in s['teams']])} registered")
        if tz.get("spec") and tz["kind"] != "major":
            lines.append(f"RISER POINTS: {spec_text(tz['spec'])}")
    lines.append("Start a team: `/signup` with a name and logo. Captains: `/offer @player`, then `/register`.")
    fa = s["free_agents"]
    if fa:
        shown = ", ".join(f"<@{u}>" for u in fa[:50])
        lines.append(f"**Free agents ({len(fa)}):** {shown}" + (f" and {len(fa) - 50} more" if len(fa) > 50 else ""))
    else:
        lines.append("**Free agents:** none yet. Type `/freeagent` to be listed.")
    return "\n".join(lines)[:1990]


def team_embed(guild: discord.Guild, s: dict, key: str) -> tuple[discord.Embed, discord.File | None]:
    t = s["teams"][key]
    tz = s.get("tourney")
    r = guild.get_role(int(key))
    players = [f"<@{u}>{pos_tag(s, u)}{' (C)' if int(u) == t['captain'] else ' (CC)' if int(u) == t.get('co') else ''}" for u in t["roster"]]
    desc = f"**Players ({len(players)}/{ROSTER_MAX})**\n" + "\n".join(players) + f"\n\n{points_line(s, key)}"
    if not is_complete(t):
        need = ROSTER_MIN - len(t["roster"])
        desc = (f"🔨 **Still building: {len(t['roster'])}/{ROSTER_MIN} players.** Needs {need} more to enter "
                "tournaments.\n\n" + desc)
    if tz and key in tz.get("entrants", []):
        desc += f"\nRegistered for **{tz['name']}**"
    embed = discord.Embed(title=t["name"], description=desc,
                          colour=r.colour if r else discord.Colour.orange())
    icon = bot.user.display_avatar.url if bot.user else None
    embed.set_author(name=LEAGUE_NAME, icon_url=icon)
    embed.set_footer(text="ON THE RISE · PB CIRCUIT", icon_url=icon)
    f = logo_file(t)
    if f:
        embed.set_thumbnail(url=f"attachment://{t['logo']}")
    return embed, f


def pack(parts: list[str], limit: int = 1900) -> list[str]:
    """Fit the blocks into as few Discord messages as possible (2000 characters max each)."""
    chunks, current = [], ""
    for part in parts:
        if current and len(current) + len(part) + 2 > limit:
            chunks.append(current)
            current = ""
        current = f"{current}\n\n{part}" if current else part
    if current:
        chunks.append(current)
    return chunks


async def update_board(guild: discord.Guild, data: dict | None = None):
    """Keep #rosters current: a summary message, then one card (with logo) per team, including teams still
    building their roster (marked as such).
    Also refreshes the website."""
    data = data if data is not None else load_data()
    s = guild_signups(data, guild.id)
    channel = chan(guild, "rosters")
    if channel is not None:
        for old in s.get("board", []):  # messages from older versions of the bot
            try:
                await (await channel.fetch_message(old)).delete()
            except discord.HTTPException:
                pass
        s["board"] = []
        card = brand_embed(render_board(s))
        msg = None
        if s.get("board_summary"):
            try:
                msg = await channel.fetch_message(s["board_summary"])
                if not msg.embeds or msg.embeds[0].description != card.description:
                    await msg.edit(content=None, embed=card, allowed_mentions=NO_PINGS)
            except discord.HTTPException:
                msg = None
        if msg is None:
            msg = await channel.send(embed=card, allowed_mentions=NO_PINGS)
            s["board_summary"] = msg.id
        tz = s.get("tourney") or {}
        c = circuit(s)
        for key, t in team_list(s):
            sig = json.dumps([t["name"], list(t["roster"]), t["captain"], t.get("logo"), t.get("points", 0),
                              key in c["qualified"], c["needed"], key in tz.get("entrants", []), tz.get("name")])
            if t.get("board_sig") == sig and t.get("board_msg"):
                continue
            if t.get("board_msg"):
                try:
                    await (await channel.fetch_message(t["board_msg"])).delete()
                except discord.HTTPException:
                    pass
                t["board_msg"] = None
            embed, f = team_embed(guild, s, key)
            sent = await channel.send(embed=embed, allowed_mentions=NO_PINGS, **({"file": f} if f else {}))
            t["board_msg"], t["board_sig"] = sent.id, sig
        save_data(data)
    try:
        await refresh_registered(guild, data)  # the tournament's own "registered teams" channel
    except Exception as e:
        print(f"[registered channel] {e}")
    try:
        await refresh_fa_cards(guild, data)  # one profile card per free agent in #free-agents
        save_data(data)
    except Exception as e:
        print(f"[free agent board] {e}")
    asyncio.create_task(sync_team_emojis(guild))  # new team or new logo: its logo emoji
    asyncio.create_task(sync_team_hoist(guild))  # member list: only teams still playing get their own group
    asyncio.create_task(sync_captains_channel(guild))  # tournament captains channel: made, updated or deleted
    schedule_publish(guild)

def reg_channel_name(tname: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", tname.lower()).strip("-")[:80] or "tournament"
    return f"📋｜{slug}"


async def ensure_registered_channel(guild: discord.Guild, data: dict) -> discord.TextChannel | None:
    """Make the read-only channel named after the current tournament (once per tournament)."""
    s = guild_signups(data, guild.id)
    tz = s.get("tourney")
    if not tz:
        return None
    ch = guild.get_channel(tz.get("reg_channel") or 0)
    if ch:
        return ch
    cat = await get_or_make_category(guild, "LEAGUE")
    ch = await guild.create_text_channel(reg_channel_name(tz["name"]), category=cat,
                                         overwrites=overwrites_for(guild, "ro"),
                                         topic=f"Teams registered for {tz['name']}. Updated by the bot.")
    tz["reg_channel"], tz["reg_msg"], tz["reg_sig"] = ch.id, None, None
    save_data(data)
    return ch


def registered_card(guild: discord.Guild, s: dict) -> discord.Embed:
    tz = s["tourney"]
    keys = [k for k in tz.get("entrants", []) if k in s["teams"]]
    lines = []
    for i, k in enumerate(keys, 1):
        t = s["teams"][k]
        r = guild.get_role(int(k))
        players = " ".join(f"<@{u}>{pos_tag(s, u)}" for u in t["roster"] if int(u) != t["captain"])
        lines.append(f"**{i}. {r.mention if r else t['name']}** · {t.get('points', 0)} RISER POINTS\n"
                     f"Captain <@{t['captain']}>{pos_tag(s, t['captain'])}"
                     + (f" · Co-captain <@{t['co']}>" if t.get("co") else "") + (f"\n{players}" if players else ""))
    state = (f"Entries **open**" + (f" · close **{s['closes']}**" if s.get("closes") else "")
             if s.get("open") else "Entries **closed**")
    head = (f"{state}\n**{len(keys)}** team(s) registered" + (f" · {MIN_TEAMS} needed to start" if len(keys) < MIN_TEAMS
                                                              and s.get("open") else "") + "\n")
    foot = ("\n\nCaptains or co-captains: type `/register` to enter, `/unregister` to drop out." if s.get("open") else "")
    body = head + ("\n\n".join(lines) if lines else "\nNo teams yet.") + foot
    e = brand_embed(body[:4000], f"{tz['name']} · registered teams", GOLD)
    if tz.get("logo") and (LOGO_DIR / tz["logo"]).exists():
        e.set_thumbnail(url=f"attachment://{tz['logo']}")
    return e


async def refresh_registered(guild: discord.Guild, data: dict):
    """Keep the tournament channel's list of registered teams up to date (edits one message)."""
    s = guild_signups(data, guild.id)
    tz = s.get("tourney")
    if not tz:
        return
    ch = guild.get_channel(tz.get("reg_channel") or 0)
    if ch is None:
        if not s.get("open"):
            return  # only make the channel while entries are open (or with /setupbot part:registered)
        ch = await ensure_registered_channel(guild, data)
    e = registered_card(guild, s)
    sig = json.dumps([e.description, tz.get("logo")])
    if tz.get("reg_sig") == sig and tz.get("reg_msg"):
        return
    f = discord.File(LOGO_DIR / tz["logo"], filename=tz["logo"]) if tz.get("logo") and (LOGO_DIR / tz["logo"]).exists() else None
    msg = None
    if tz.get("reg_msg"):
        try:
            msg = await ch.fetch_message(tz["reg_msg"])
            await msg.edit(embed=e, attachments=[f] if f else [], allowed_mentions=NO_PINGS)
        except discord.HTTPException:
            msg = None
    if msg is None:
        msg = await ch.send(embed=e, allowed_mentions=NO_PINGS, **({"file": f} if f else {}))
        tz["reg_msg"] = msg.id
    tz["reg_sig"] = sig
    save_data(data)


# ---------------------------------------------------------------- tournament captains channel
#
# Once entries close, a private channel for the captains and co-captains of the teams IN that tournament
# (plus staff): 🧢｜<tournament>-captains. Access follows the entrants and captaincy changes, and the channel is
# deleted when the tournament ends (champion crowned and the consolation bracket done).

_capchan_lock: dict[int, asyncio.Lock] = {}


def tourney_running(s: dict) -> bool:
    tz = s.get("tourney") or {}
    ev = s.get("event")
    if not tz or s.get("open") or not tz.get("entrants"):
        return False
    return ev is None or ev.get("stage") != "done" or cons_running(ev)


def tourney_captains(s: dict) -> set[int]:
    tz = s.get("tourney") or {}
    return {u for k in tz.get("entrants", []) if k in s["teams"] for u in captains_of(s, k)}


async def sync_captains_channel(guild: discord.Guild):
    lock = _capchan_lock.setdefault(guild.id, asyncio.Lock())
    async with lock:
        data = load_data()
        s = guild_signups(data, guild.id)
        tz = s.get("tourney") or {}
        ch = guild.get_channel(int(s.get("cap_chan") or 0))
        if not tourney_running(s):
            if ch:
                try:
                    await ch.delete(reason="Tournament over: captains channel removed")
                except discord.HTTPException:
                    pass
            if s.get("cap_chan"):
                s["cap_chan"] = None
                save_data(data)
            return
        want = {uid for uid in tourney_captains(s) if guild.get_member(uid)}
        if ch is None:
            slug = re.sub(r"[^a-z0-9]+", "-", tz.get("name", "tournament").lower()).strip("-")[:60] or "tournament"
            ow = overwrites_for(guild, "staff")
            for uid in want:
                ow[guild.get_member(uid)] = discord.PermissionOverwrite(view_channel=True, send_messages=True,
                                                                        read_message_history=True)
            try:
                cat = discord.utils.get(guild.categories, name="MATCHES") or discord.utils.get(guild.categories,
                                                                                               name="LEAGUE")
                ch = await guild.create_text_channel(f"🧢｜{slug}-captains", category=cat, overwrites=ow,
                                                     topic=f"Captains and co-captains of the teams in {tz.get('name')}. "
                                                           "Deleted when the tournament ends.")
            except discord.HTTPException as e:
                print(f"[captains channel] {e}")
                return
            s["cap_chan"] = ch.id
            save_data(data)
            try:
                await ch.send(content=" ".join(f"<@{u}>" for u in sorted(want))[:1900] or None,
                              embed=brand_embed(
                                  f"Welcome, captains and co-captains of **{tz.get('name')}**. This channel is just for "
                                  "you and staff: sort out game times, ask questions, flag problems.\n\n"
                                  "• Schedule with `/gametime` or `/confirmtime`\n• Report scores with `/game_score`\n"
                                  "• Get your team in the arena with `/arenacall`\n\n"
                                  "It's deleted automatically when the tournament ends.", "🧢 Tournament captains", GOLD),
                              allowed_mentions=discord.AllowedMentions(users=True))
            except discord.HTTPException:
                pass
            return
        # keep access in step with the entrants and captaincy changes
        have = {t.id for t, o in ch.overwrites.items() if isinstance(t, discord.Member) and o.view_channel}
        for uid in want - have:
            m_ = guild.get_member(uid)
            if m_:
                try:
                    await ch.set_permissions(m_, view_channel=True, send_messages=True, read_message_history=True,
                                             reason="Captain of a team in the tournament")
                    await asyncio.sleep(0.3)
                except discord.HTTPException:
                    pass
        for uid in have - want:
            m_ = guild.get_member(uid)
            if m_ and not is_staff(m_):
                try:
                    await ch.set_permissions(m_, overwrite=None, reason="No longer a captain in the tournament")
                    await asyncio.sleep(0.3)
                except discord.HTTPException:
                    pass


# one-time setup: run with /setupbot part:registered
async def registeredchannel(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    if not s.get("tourney"):
        return await interaction.followup.send("There's no tournament. Open one with /opensignups.", ephemeral=True)
    ch = await ensure_registered_channel(interaction.guild, data)
    s["tourney"]["reg_sig"] = None
    save_data(data)
    await refresh_registered(interaction.guild, data)
    await interaction.followup.send(f"Registered teams are listed in {ch.mention} and update automatically.",
                                    ephemeral=True)


@bot.tree.command(description="Staff: open entries for a tournament and set its RISER POINTS.")
@app_commands.describe(name="Tournament name, e.g. 'Rise Open 1'",
                       logo="The tournament's logo (PNG, JPG, WEBP or GIF, under 1 MB). Required.",
                       kind="Circuit event, Major (qualified teams only) or LCQ (invite-only, top 4 to the Major)",
                       points="Points per placement, e.g. 1:300, 2:210, 3:150, 4:120, 5-6:75 (blank = default)",
                       closes="When entries close, e.g. 'Friday at 8pm' (optional)",
                       winner_qualifies="Does the winner get an automatic Major spot? (default yes)")
@app_commands.choices(kind=[
    app_commands.Choice(name="Circuit event (awards RISER POINTS)", value="event"),
    app_commands.Choice(name="Major (qualified teams only, points reset after)", value="major"),
    app_commands.Choice(name="Last Chance Qualifier: next 8 teams invited, top 4 to the Major", value="lcq"),
])
@app_commands.default_permissions(manage_roles=True)
async def opensignups(interaction: discord.Interaction, name: str, logo: discord.Attachment, kind: str = "event",
                      points: str | None = None, closes: str | None = None, winner_qualifies: bool = True):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can open a tournament.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    nxt = current_busy(s)  # one is being played: these entries are for the NEXT tournament
    if s.get("tourney") and s.get("open"):
        return await interaction.response.send_message(
            f"**{s['tourney']['name']}** is still taking entries. Close them first (/closesignups).", ephemeral=True)
    if nxt and s.get("upcoming"):
        return await interaction.response.send_message(
            f"**{s['upcoming']['name']}** is already the next tournament. It starts once the current one ends.",
            ephemeral=True)
    if nxt and kind == "lcq":
        return await interaction.response.send_message(
            "An LCQ uses the final RISER POINTS, so open it after the current tournament is done.", ephemeral=True)
    spec = {}
    if kind == "event":
        if points:
            spec, problem = parse_spec(points)
        else:  # the saved payout table from /payout, or the built-in one
            spec, problem = default_payout(s), None
        if problem:
            return await interaction.response.send_message(problem, ephemeral=True)
    if logo is None:
        return await interaction.response.send_message("Attach the tournament's logo to open sign-ups.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    logo_name, problem = await save_logo(logo)
    if problem:
        return await interaction.followup.send(problem + " Sign-ups were not opened.", ephemeral=True)
    data = load_data()  # fresh copy after the upload
    s = guild_signups(data, guild.id)
    if nxt:
        s["upcoming"] = {"name": name.strip()[:60], "kind": kind, "spec": spec, "entrants": [], "logo": logo_name,
                         "winner_qualifies": winner_qualifies if kind == "event" else False, "open": True,
                         "closes": closes, "closes_at": closes_iso(closes)}
        save_data(data)
        cur = s["tourney"]["name"]
        text = (f"# {name} is open for entries!\n**{cur}** is still being played, and you can already sign up for "
                f"the next one. It starts once {cur} is finished.\n"
                + (f"**RISER POINTS:** {spec_text(spec)}\n" if kind == "event" else
                   "**MAJOR:** only qualified teams can enter.\n")
                + f"Captains: `/register` to enter (you need {ROSTER_MIN}+ players)."
                + (f"\nEntries close **{closes}**." if closes else ""))
        ann = chan(guild, "announcements")
        if ann:
            await post(ann, text, file=logo_file(s["upcoming"]))
        schedule_publish(guild)
        return await interaction.followup.send(
            f"**{name}** is open for entries as the **next** tournament. Teams can register now; it takes over "
            f"automatically once **{cur}** ends (close its entries any time with /closesignups).", ephemeral=True)
    archive_event(guild, s)  # keep last tournament's player stats for the year table
    s["tourney"] = {"name": name.strip()[:60], "kind": kind, "spec": spec, "entrants": [], "logo": logo_name,
                    "winner_qualifies": winner_qualifies if kind == "event" else False}
    s["open"], s["closes"], s["event"] = True, closes, None
    s["closes_at"] = closes_iso(closes)
    tied_out = []
    if kind == "lcq":  # invite-only: the entrants are set now
        straight, tied, spots = lcq_invites(s)
        s["tourney"]["entrants"] = list(straight)
        s["tourney"]["lcq"] = {"invited": list(straight), "next_up": [], "playin": list(tied), "spots": spots}
        if tied:
            playin_start(s, tied, spots)  # tied at the cutoff: single-elimination play-in for the last spots
        else:
            lcq_fill(s)  # odd number of invites: the next man up gets in too
        s["open"], s["closes"] = False, None
    save_data(data)
    await update_board(guild, data)

    c = circuit(s)
    if kind == "lcq":
        inv = s["tourney"]["entrants"]
        listing = "\n".join(f"{i}. **{s['teams'][k]['name']}** · {s['teams'][k].get('points', 0)} RISER POINTS"
                            + (" · *next man up*" if k in s["tourney"]["lcq"]["next_up"] else "")
                            for i, k in enumerate(inv, 1))
        if tied:
            pi = s["event"]["playin"]
            listing += (f"\n\n**Tied at the cutoff ({s['teams'][tied[0]].get('points', 0)} RISER POINTS):** "
                        + ", ".join(f"**{s['teams'][k]['name']}**" for k in tied)
                        + f"\nThey're all invited to a **single-elimination play-in** for the last **{spots}** "
                          f"spot{'s' if spots != 1 else ''}. Play-in round 1:\n"
                        + "\n".join(f"**M{m['id']}**: {tag(m['a'])} vs {tag(m['b'])}" for m in pi["matches"]))
        line_ = lcq_line(s)[:4]
        if line_:
            listing += "\n\n**Next in line if a team drops:** " + ", ".join(
                f"{s['teams'][k]['name']} ({s['teams'][k].get('points', 0)})" for k in line_)
        target = f" under **{c['needed']} RISER POINTS**" if c["needed"] is not None else ""
        text = (f"# {name} (LAST CHANCE QUALIFIER)\nThe next **{len(inv)}** teams{target} that haven't qualified are "
                f"**invited directly**. The **top {LCQ_SPOTS}** qualify for the Major. No RISER POINTS are given.\n\n"
                f"**Invited:**\n{listing or 'No eligible teams.'}\n\nNo /register needed. Watch #bracket for the draw.")
        ann = chan(guild, "announcements")
        if ann:
            await post(ann, text, file=logo_file(s["tourney"]))
        for k in inv:  # captains and co-captains get a DM invite
            for uid in captains_of(s, k):
                await dm(uid, brand_embed(f"**{s['teams'][k]['name']}** is invited to **{name}**, the Last Chance "
                                          f"Qualifier. The top {LCQ_SPOTS} teams qualify for the Major. You're already "
                                          "entered, no /register needed. Watch #bracket for the draw.",
                                          "🎟️ You're in the LCQ", GOLD))
        if s["tourney"].get("reg_channel"):
            await refresh_registered(guild, data)
        schedule_publish(guild)
        for k in tied:  # play-in teams get their own DM
            for uid in captains_of(s, k):
                await dm(uid, brand_embed(f"**{s['teams'][k]['name']}** is tied at the LCQ cutoff, so you're invited "
                                          f"to a **single-elimination play-in** for the last {spots} spot(s) in "
                                          f"**{name}**. Your match is in #schedule; win and you're in the LCQ.",
                                          "🎟️ LCQ play-in", GOLD))
        save_data(data)
        warn = (f"\n{len(tied)} teams are tied at the cutoff: they play a single-elimination play-in for the last "
                f"{spots} spot(s) first (record results with /result). Start the LCQ once it's done.") if tied else ""
        return await interaction.followup.send(
            f"**{name}** (LCQ) is set with {len(s['tourney']['entrants'])} invited teams and announced. Start it "
            f"with /startmain (or /startgroups). The top {LCQ_SPOTS} qualify for the Major.{warn}", ephemeral=True)
    if kind == "major":
        who = "Only teams that **qualified** can enter: tournament winners"
        who += f" and teams with **{c['needed']}+ RISER POINTS**." if c["needed"] is not None else "."
        text = (f"# {name} (MAJOR) is open for entries!\n{who}\n"
                "After the Major, every team's RISER POINTS reset to 0.")
    else:
        text = (f"# {name} is open for entries!\n**RISER POINTS:** {spec_text(spec)}\n"
                + ("**The winner qualifies for the Major automatically.**" if winner_qualifies else
                   "This one does **not** give the winner an automatic Major spot. Points still count."))
        if c["needed"] is not None:
            text += f" Everyone else needs **{c['needed']} RISER POINTS**."
    text += (f"\nCaptains: type `/register` to enter (you need {ROSTER_MIN}+ players). "
             "Your points and what you still need are shown when you register.")
    if closes:
        text += f"\nEntries close **{closes}**."
    text += "\nNo team yet? `/signup` to start one, or `/freeagent` to get found."
    ann = chan(guild, "announcements")
    if ann:
        await post(ann, text, file=logo_file(s["tourney"]))
    schedule_publish(guild)
    await interaction.followup.send(
        f"**{name}** is open for entries and announced with its logo. "
        + ("" if kind == "major" else "Winner gets a Major spot." if winner_qualifies else "Winner does NOT get a Major spot.")
        + " Change it any time with /tournament winner_qualifies:.", ephemeral=True)


@app_commands.describe(winner_qualifies="Yes: the winner gets an automatic Major spot. No: points only.")
@app_commands.default_permissions(manage_roles=True)
async def majorspot(interaction: discord.Interaction, winner_qualifies: bool):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    tz = s.get("tourney")
    if not tz:
        return await interaction.response.send_message("There's no tournament open. Use /opensignups.", ephemeral=True)
    if tz.get("kind") == "major":
        return await interaction.response.send_message("This is the Major itself, so there's no Major spot to give.",
                                                       ephemeral=True)
    if tz.get("kind") == "lcq":
        return await interaction.response.send_message(f"In the LCQ the top {LCQ_SPOTS} qualify automatically.",
                                                       ephemeral=True)
    if s.get("event") and s["event"].get("stage") == "done":
        return await interaction.response.send_message("That tournament is already finished.", ephemeral=True)
    tz["winner_qualifies"] = winner_qualifies
    save_data(data)
    schedule_publish(interaction.guild)
    ann = chan(interaction.guild, "announcements")
    if ann:
        await post(ann, f"The winner of **{tz['name']}** "
                        + ("**will qualify for the Major** automatically." if winner_qualifies else
                           "will **not** get an automatic Major spot. RISER POINTS still count."),
                   title="Major spot update", color=GOLD)
    await interaction.response.send_message(
        f"Saved: the winner of **{tz['name']}** " + ("qualifies for the Major." if winner_qualifies else
                                                     "does not get a Major spot."), ephemeral=True)


@app_commands.describe(closes="When entries close, e.g. 'Friday at 1 PM EST'",
                       remind="DM the captains of full teams that haven't registered yet (default yes)")
@app_commands.default_permissions(manage_roles=True)
async def setcloses(interaction: discord.Interaction, closes: str, remind: bool = True):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    tz = s.get("tourney")
    if not tz or not s["open"]:
        return await interaction.response.send_message("No tournament is taking entries right now.", ephemeral=True)
    s["closes"] = closes.strip()[:80]
    s["closes_at"] = closes_iso(closes)
    save_data(data)
    await interaction.response.defer(ephemeral=True)
    c = circuit(s)
    waiting = [k for k, t in team_list(s) if is_complete(t) and k not in tz["entrants"]
               and (tz.get("kind") != "major" or k in c["qualified"] or (c["needed"] is not None
                                                                          and t.get("points", 0) >= c["needed"]))]
    lines = [f"Entries for **{tz['name']}** now close **{s['closes']}**.",
             f"**{len(tz['entrants'])}** team(s) entered so far."]
    ann = chan(interaction.guild, "announcements")
    if ann:
        await post(ann, "\n".join(lines), title="Entry deadline", color=GOLD)
    sent, failed = 0, []
    if remind:  # a private reminder to each captain whose full team isn't entered yet
        for k in waiting:
            t = s["teams"][k]
            for who in [t["captain"]] + ([t["co"]] if t.get("co") else []):
                try:
                    cap = interaction.guild.get_member(who) or await bot.fetch_user(who)
                    await cap.send(embed=brand_embed(
                        f"Your team **{t['name']}** isn't entered in **{tz['name']}** yet.\n"
                        f"Entries close **{s['closes']}**. Type `/register` in **{interaction.guild.name}** to enter.\n"
                        f"{points_line(s, k)}", "Don't miss the tournament", GOLD), file=logo_file(t) or discord.utils.MISSING)
                    sent += 1
                except (discord.HTTPException, AttributeError):
                    failed.append(f"{t['name']} (<@{who}>)")
    await update_board(interaction.guild, data)  # also refreshes the website
    note = f" Sent {sent} DM(s) to captains/co-captains who still need to register." if remind and waiting else ""
    if failed:
        note += " Couldn't DM (DMs closed): " + ", ".join(failed) + "."
    await interaction.followup.send(f"Entries now close **{s['closes']}**. Announced in #announcements.{note}",
                                    ephemeral=True)


@app_commands.describe(logo="The new tournament logo (PNG, JPG, WEBP or GIF, under 1 MB)")
@app_commands.default_permissions(manage_roles=True)
async def tournamentlogo(interaction: discord.Interaction, logo: discord.Attachment):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    data = load_data()
    if not guild_signups(data, interaction.guild.id).get("tourney"):
        return await interaction.response.send_message("There's no tournament open. Use /opensignups.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    logo_name, problem = await save_logo(logo)
    if problem:
        return await interaction.followup.send(problem, ephemeral=True)
    data = load_data()
    tz = guild_signups(data, interaction.guild.id)["tourney"]
    tz["logo"] = logo_name
    save_data(data)
    schedule_publish(interaction.guild)
    await interaction.followup.send(f"Updated the logo for **{tz['name']}**.", file=logo_file(tz), ephemeral=True)


@app_commands.describe(position="Your position")
@app_commands.choices(position=[app_commands.Choice(name=n, value=v) for v, n in POSITIONS])
async def position(interaction: discord.Interaction, position: str):
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    s.setdefault("positions", {})[str(interaction.user.id)] = position
    save_data(data)
    await interaction.response.send_message(f"Your position is now **{dict(POSITIONS)[position]}**.", ephemeral=True)
    await update_board(interaction.guild, data)


@app_commands.describe(player="The player", position="Their new position")
@app_commands.choices(position=[app_commands.Choice(name=n, value=v) for v, n in POSITIONS])
@app_commands.default_permissions(manage_roles=True)
async def setposition(interaction: discord.Interaction, player: discord.Member, position: str):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can change someone else's position. "
                                                       "Use /position to change your own.", ephemeral=True)
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    old = pos_of(s, player.id)
    s.setdefault("positions", {})[str(player.id)] = position
    save_data(data)
    await interaction.response.defer(ephemeral=True)
    key = team_of(s, player.id)
    t = s["teams"].get(key) if key else None
    if t:
        await log_transaction(guild, f"{player.mention} ({t['name']}) moved from **{old or 'no position'}** to "
                                     f"**{position}** by staff", t)
    await update_board(guild, data)  # roster cards + website
    try:
        await player.send(embed=brand_embed(f"League staff changed your position in **{guild.name}** to "
                                            f"**{dict(POSITIONS)[position]}**.", "Position updated", INFO))
    except discord.HTTPException:
        pass
    await interaction.followup.send(f"{player.mention} is now **{dict(POSITIONS)[position]}**"
                                    + (f" (was {old})" if old and old != position else "")
                                    + (f" on **{t['name']}**." if t else "."), ephemeral=True,
                                    allowed_mentions=NO_PINGS)


class PositionPick(discord.ui.View):
    """A dropdown to choose a position, then carry on (e.g. join the pickup queue)."""

    def __init__(self, guild_id: int, then: str):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(custom_id=f"pug:setpos:{guild_id}:{then}:0", placeholder="Pick your position",
                                        options=[discord.SelectOption(label=n, value=v) for v, n in POSITIONS]))


@bot.tree.command(description="Anyone: start a team. You become its captain.")
@app_commands.describe(team_name="Your team's name", position="The position you play",
                       logo="Your team logo (PNG, JPG, WEBP or GIF, under 1 MB)")
@app_commands.choices(position=[app_commands.Choice(name=n, value=v) for v, n in POSITIONS])
async def signup(interaction: discord.Interaction, team_name: str, position: str, logo: discord.Attachment):
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    if suspended_from(s, user.id, "league"):
        return await interaction.response.send_message(suspended_from(s, user.id, "league"), ephemeral=True)
    team_name = team_name.strip()
    problem = None
    if team_of(s, user.id):
        problem = f"You're already on **{s['teams'][team_of(s, user.id)]['name']}**. Leave it first with /leaveteam."
    elif not 2 <= len(team_name) <= 32:
        problem = "Team names need to be 2 to 32 characters."
    elif any(t["name"].lower() == team_name.lower() for t in s["teams"].values()) or role(guild, team_name):
        problem = f"The name **{team_name}** is taken. Pick another."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    s.setdefault("positions", {})[str(user.id)] = position
    save_data(data)
    await interaction.response.defer(ephemeral=True, thinking=True)
    filename, problem = await save_logo(logo)
    if problem:
        return await interaction.followup.send(problem, ephemeral=True)
    key = await create_team(guild, data, team_name, user, filename)
    await log_transaction(guild, f"New team: **{team_name}**, captain {user.mention}", s["teams"][key])
    await update_board(guild, data)
    await interaction.followup.send(
        f"**{team_name}** is created and you're the captain. Your team channel is <#{s['teams'][key]['channel']}>.\n"
        f"Next: offer spots with `/offer @player` ({ROSTER_MIN} to {ROSTER_MAX} players including you). "
        f"Once you have {ROSTER_MIN}, use `/register` to enter tournaments.", ephemeral=True)


@bot.tree.command(name="offer", description="Captains/co-captains: offer a player a spot on your team. They accept or decline in DMs.")
@app_commands.describe(player="The player to offer a spot", team="Commissioner/admin only: which team (captains leave this empty)")
async def sign(interaction: discord.Interaction, player: discord.Member, team: discord.Role | None = None):
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    if team is not None and not is_commissioner(user):
        return await interaction.response.send_message("Only the Commissioner or an admin can sign players for another team. "
                                                       "Captains just use /offer @player.", ephemeral=True)
    key = str(team.id) if team else signer_team(s, user.id)
    problem = None
    if key is None or key not in s["teams"]:
        problem = ("Only team captains and co-captains can sign players. Start a team with /signup."
                   if not team else f"{team.mention} isn't a league team.")
    elif roster_locked(s):
        problem = "Rosters are locked while the main draw is being played."
    elif player.bot:
        problem = "You can't sign a bot."
    elif team_of(s, player.id):
        problem = f"{player.mention} is already on **{s['teams'][team_of(s, player.id)]['name']}**."
    elif suspended_from(s, player.id, "league"):
        problem = f"{player.mention} is suspended from the league right now."
    elif len(s["teams"][key]["roster"]) >= ROSTER_MAX:
        problem = f"Your roster is full ({ROSTER_MAX} players). Release someone first with /release."
    elif any(o["team"] == key and o["player"] == player.id for o in s["offers"].values()):
        problem = f"{player.mention} already has an offer from you. Wait for them to accept or decline."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)

    t = s["teams"][key]
    oid = secrets.token_hex(4)
    s["offers"][oid] = {"team": key, "player": player.id, "from": user.id}
    save_data(data)
    text = (f"**{t['name']}** wants to sign you in {guild.name}!\n"
            f"Offer from {user.mention}. {points_line(s, key)}\n"
            "Accept to join the team, or decline. You can only be on one team.")
    view = OfferView(guild.id, oid, player.id)
    f = logo_file(t)
    try:
        sent = await post(player, text, title=f"Contract offer: {t['name']}", color=GOLD, view=view, file=f)
        s["offers"][oid]["msg"] = ["dm", sent.id] if sent else None
        save_data(data)
        where = "in their DMs"
    except discord.HTTPException:  # DMs closed: offers are DM-only (never posted in #free-agents)
        s["offers"].pop(oid, None)
        save_data(data)
        return await interaction.followup.send(
            f"{player.mention} has DMs turned off, so the offer wasn't sent. Offers only go by DM: ask them to allow "
            "DMs from server members (Server name → Privacy Settings → Direct Messages), then run /offer again.",
            ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.followup.send(f"Offer sent to {player.mention} {where}. You'll hear back in your team "
                                    "channel when they answer.", ephemeral=True, allowed_mentions=NO_PINGS)


@bot.tree.command(description="Captains/co-captains: take back a contract offer (or list your open offers).")
@app_commands.describe(player="The player whose offer to take back (leave empty to see your open offers)",
                       team="Staff only: which team's offer")
async def revokeoffer(interaction: discord.Interaction, player: discord.Member | None = None,
                      team: discord.Role | None = None):
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    staff = is_staff(user)
    if team is not None and not staff:
        return await interaction.response.send_message("Only staff can pick a team. Captains leave `team` empty.",
                                                       ephemeral=True)
    key = str(team.id) if team is not None else signer_team(s, user.id)
    if key is None and staff and player is not None:  # staff can just name the player
        key = next((o["team"] for o in s["offers"].values() if o["player"] == player.id), None)
    if key is None or key not in s["teams"]:
        return await interaction.response.send_message("Only captains and co-captains (or staff) can revoke offers.",
                                                       ephemeral=True)
    t = s["teams"][key]
    mine = {oid: o for oid, o in s["offers"].items() if o["team"] == key}
    if player is None:
        lines = [f"<@{o['player']}> · sent by <@{o['from']}>" for o in mine.values()]
        return await interaction.response.send_message(
            embed=brand_embed("\n".join(lines) or "No open offers.", f"{t['name']}: open offers", INFO)
            if lines else None, content=None if lines else f"**{t['name']}** has no open offers.", ephemeral=True,
            allowed_mentions=NO_PINGS)
    hits = [oid for oid, o in mine.items() if o["player"] == player.id]
    if not hits:
        return await interaction.response.send_message(f"**{t['name']}** has no open offer to {player.mention}.",
                                                       ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    for oid in hits:
        o = s["offers"].pop(oid)
        where = o.get("msg")
        try:  # grey out the offer card so it can't be accepted
            if where:
                ch = (await player.create_dm()) if where[0] == "dm" else guild.get_channel(where[0])
                msg = await ch.fetch_message(where[1])
                e = brand_embed(f"**{t['name']}** withdrew this offer.", f"Offer withdrawn: {t['name']}", MUTED)
                await msg.edit(embed=e, view=None, attachments=[])
        except (discord.HTTPException, AttributeError):
            pass
    save_data(data)
    try:
        await player.send(embed=brand_embed(f"**{t['name']}** took back their offer in {guild.name}.",
                                            "Offer withdrawn", MUTED))
    except discord.HTTPException:
        pass
    team_ch = guild.get_channel(t.get("channel") or 0)
    if team_ch:
        await post(team_ch, f"{user.mention} took back the offer to {player.mention}.", title="Offer withdrawn",
                   color=MUTED)
    await interaction.followup.send(f"Offer to {player.mention} withdrawn. They can't accept it any more.",
                                    ephemeral=True, allowed_mentions=NO_PINGS)


class OfferView(discord.ui.View):
    """Accept / Decline buttons for a contract offer. Clicks are handled in on_interaction."""

    def __init__(self, guild_id: int, offer_id: str, user_id: int):
        super().__init__(timeout=None)
        base = f"{guild_id}:{offer_id}:{user_id}"
        self.add_item(discord.ui.Button(label="Accept", style=discord.ButtonStyle.success,
                                        custom_id=f"pbl:accept:{base}"))
        self.add_item(discord.ui.Button(label="Decline", style=discord.ButtonStyle.secondary,
                                        custom_id=f"pbl:decline:{base}"))


async def answer_offer(interaction: discord.Interaction, guild: discord.Guild, action: str, oid: str, uid: int):
    data = load_data()
    s = guild_signups(data, guild.id)
    if action == "accept" and suspended_from(s, uid, "league"):
        return await interaction.response.send_message(suspended_from(s, uid, "league"), ephemeral=True)
    if action == "accept" and oid in s["offers"] and not pos_of(s, uid):
        return await interaction.response.send_message(
            f"Before you can join a team you need a position. Type **/position** in {guild.name}, "
            "then click Accept again. The offer stays open.", ephemeral=True)
    offer = s["offers"].pop(oid, None)
    if offer is None:
        save_data(data)
        return await interaction.response.edit_message(content="This offer is no longer available.", view=None,
                                                       attachments=[])
    t = s["teams"].get(offer["team"])
    team_ch = guild.get_channel(t.get("channel") or 0) if t else None

    if action == "decline":
        save_data(data)
        await interaction.response.edit_message(
            content=f"You declined the offer from **{t['name'] if t else 'that team'}**.", view=None, attachments=[])
        if team_ch:
            await post(team_ch, f"<@{uid}> declined your offer.", title="Offer declined", color=MUTED)
        return

    problem = None
    if not t:
        problem = "That team doesn't exist any more."
    elif team_of(s, uid):
        problem = f"You're already on **{s['teams'][team_of(s, uid)]['name']}**. Leave it first to join another team."
    elif roster_locked(s):
        problem = "Rosters are locked while the main draw is being played. Ask again after the tournament."
    elif len(t["roster"]) >= ROSTER_MAX:
        problem = f"**{t['name']}** already has a full roster."
    if problem:
        save_data(data)
        await interaction.response.edit_message(content=f"Couldn't join: {problem}", view=None, attachments=[])
        if team_ch and t:
            await post(team_ch, f"<@{uid}> tried to accept, but: {problem}", title="Offer couldn't go through", color=MUTED)
        return

    t["roster"][str(uid)] = ""
    for other in [k for k, o in s["offers"].items() if o["player"] == uid]:
        s["offers"].pop(other)  # they're on a team now, so other offers are void
    if uid in s["free_agents"]:
        s["free_agents"].remove(uid)
    save_data(data)
    await interaction.response.edit_message(content=f"You've joined **{t['name']}**! Welcome to the team.",
                                            view=None, attachments=[])
    await give_roles(guild, uid, guild.get_role(int(offer["team"])), role(guild, "Player"))
    await give_roles(guild, uid, role(guild, "Free Agent"), remove=True)
    await log_transaction(guild, f"**{t['name']}** signed <@{uid}>", t)
    if team_ch:
        done = " Your roster is complete, so you can `/register` for tournaments." if len(t["roster"]) == ROSTER_MIN else ""
        await post(team_ch, f"<@{uid}> accepted and joined the team! ({len(t['roster'])}/{ROSTER_MAX}){done}",
                   title="New signing", color=GOOD, file=logo_file(t))
    await update_board(guild, data)


@bot.tree.command(description="Commissioner+: put a player straight onto a team (no offer, no accept).")
@app_commands.describe(player="The player to sign", team="The team they join",
                       position="Their position (needed if they don't have one yet)",
                       move="If they're on another team: take them off it and move them (default no)",
                       ignore_lock="Sign even while rosters are locked for the main draw (default no)")
@app_commands.choices(position=[app_commands.Choice(name=label, value=code) for code, label in POSITIONS])
@app_commands.default_permissions(manage_roles=True)
async def forcesign(interaction: discord.Interaction, player: discord.Member, team: discord.Role,
                    position: str | None = None, move: bool = False, ignore_lock: bool = False):
    guild, user = interaction.guild, interaction.user
    if not is_commissioner(user):
        return await interaction.response.send_message("Only the Commissioner or an admin can force-sign players.",
                                                       ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    key = str(team.id)
    t = s["teams"].get(key)
    old = team_of(s, player.id)
    problem = None
    if t is None:
        problem = f"{team.mention} isn't a league team."
    elif player.bot:
        problem = "You can't sign a bot."
    elif old == key:
        problem = f"{player.mention} is already on **{t['name']}**."
    elif old and not move:
        problem = (f"{player.mention} is on **{s['teams'][old]['name']}**. Run it again with `move:True` to take them "
                   "off that team and sign them here.")
    elif old and s["teams"][old]["captain"] == player.id and len(s["teams"][old]["roster"]) > 1:
        problem = (f"{player.mention} is the captain of **{s['teams'][old]['name']}**. Hand the captaincy on first "
                   "(their captain runs /captain role:captain), then move them.")
    elif roster_locked(s) and not ignore_lock:
        problem = "Rosters are locked while the main draw is being played. Add `ignore_lock:True` to sign anyway."
    elif len(t["roster"]) >= ROSTER_MAX:
        problem = f"**{t['name']}** already has a full roster ({ROSTER_MAX}). Release someone first."
    elif suspended_from(s, player.id, "league"):
        problem = f"{player.mention} is suspended from the league. Lift it with /suspensions lift:True first."
    elif not position and not pos_of(s, player.id):
        problem = f"{player.mention} has no position yet. Add `position:` to the command."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    moved = ""
    if old:
        old_name = s["teams"][old]["name"]
        await remove_member(guild, data, old, player.id, "was moved by the Commissioner from")
        moved = f" (moved from **{old_name}**)"
        s = guild_signups(data, guild.id)
        t = s["teams"][key]
    if position:
        s.setdefault("positions", {})[str(player.id)] = position
    t["roster"][str(player.id)] = ""
    for other in [k for k, o in s["offers"].items() if o["player"] == player.id]:
        s["offers"].pop(other)  # on a team now: any other offers are void
    if player.id in s["free_agents"]:
        s["free_agents"].remove(player.id)
    save_data(data)
    await give_roles(guild, player.id, team, role(guild, "Player"))
    await give_roles(guild, player.id, role(guild, "Free Agent"), remove=True)
    await log_transaction(guild, f"**{t['name']}** signed {player.mention}{moved} · signed by the Commissioner", t)
    team_ch = guild.get_channel(t.get("channel") or 0)
    if team_ch:
        done = " Your roster is complete, so you can `/register` for tournaments." if len(t["roster"]) == ROSTER_MIN else ""
        await post(team_ch, f"{player.mention} has been signed to the team by the Commissioner{moved}. "
                            f"({len(t['roster'])}/{ROSTER_MAX}){done}", title="New signing", color=GOOD, file=logo_file(t))
    try:
        await post(player, f"You've been signed to **{t['name']}** in {guild.name}{moved}.\n"
                           f"Position: **{pos_of(s, player.id)}**. Leave any time with `/leaveteam`.",
                   title=f"Signed: {t['name']}", color=GOOD, file=logo_file(t))
    except discord.HTTPException:
        pass
    await update_board(guild, data)
    await interaction.followup.send(f"{player.mention} is now on **{t['name']}**{moved} "
                                    f"({len(t['roster'])}/{ROSTER_MAX}).", ephemeral=True, allowed_mentions=NO_PINGS)


@bot.tree.command(description="Captains: release a player from your team.")
@app_commands.describe(player="The player to release", team="Staff only: which team")
async def release(interaction: discord.Interaction, player: discord.Member, team: discord.Role | None = None):
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    key = str(team.id) if (team and is_staff(user)) else captain_team(s, user.id)
    problem = None
    if key is None or key not in s["teams"]:
        problem = "Only team captains (or staff) can release players."
    elif str(player.id) not in s["teams"][key]["roster"]:
        problem = f"{player.mention} isn't on that team."
    elif roster_locked(s):
        problem = "Rosters are locked while the main draw is being played."
    elif s["teams"][key]["captain"] == player.id:
        problem = "You can't release the captain. Pass it on with /captain role:captain first."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    text = await remove_member(guild, data, key, player.id, "was released from")
    await update_board(guild, data)
    await reply_after(interaction, text)


@app_commands.describe(player="The teammate who becomes captain")
async def makecaptain(interaction: discord.Interaction, player: discord.Member):
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    key = captain_team(s, interaction.user.id)
    if key is None:
        return await interaction.response.send_message("Only a team captain can do that.", ephemeral=True)
    t = s["teams"][key]
    if str(player.id) not in t["roster"] or player.id == interaction.user.id:
        return await interaction.response.send_message(f"{player.mention} isn't one of your teammates.",
                                                       ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    t["captain"] = player.id
    if t.get("co") == player.id:
        t["co"] = None
        await give_roles(guild, player.id, role(guild, "Co-Captain"), remove=True)
    save_data(data)
    await give_roles(guild, interaction.user.id, role(guild, "Team Captain"), remove=True)
    await give_roles(guild, player.id, role(guild, "Team Captain"))
    await log_transaction(guild, f"{player.mention} is now captain of **{t['name']}**", t)
    await update_board(guild, data)
    await interaction.followup.send(f"{player.mention} is now the captain.", ephemeral=True,
                                    allowed_mentions=NO_PINGS)


@app_commands.describe(player="The teammate to make co-captain", remove="Set True to take co-captain away",
                       team="Staff only: which team (captains leave this empty)")
async def cocaptain(interaction: discord.Interaction, player: discord.Member | None = None, remove: bool = False,
                    team: discord.Role | None = None):
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    staff = is_staff(interaction.user)
    if team is not None and not staff:
        return await interaction.response.send_message("Only staff can pick a team. Captains leave `team` empty.",
                                                       ephemeral=True)
    if team is not None:
        key = str(team.id)
    elif staff and player is not None and team_of(s, player.id) and not captain_team(s, interaction.user.id):
        key = team_of(s, player.id)  # staff can just name the player
    else:
        key = captain_team(s, interaction.user.id)
    if key is None or key not in s["teams"]:
        return await interaction.response.send_message(
            "Only a team captain (or staff, with `team`) can appoint a co-captain."
            if team is None else f"{team.mention} isn't a league team.", ephemeral=True, allowed_mentions=NO_PINGS)
    t = s["teams"][key]
    co_role = await get_cocaptain_role(guild)
    old = t.get("co")
    if remove:
        if not old:
            return await interaction.response.send_message("Your team doesn't have a co-captain.", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        t["co"] = None
        save_data(data)
        await give_roles(guild, old, co_role, remove=True)
        await log_transaction(guild, f"<@{old}> is no longer co-captain of **{t['name']}**", t)
        await update_board(guild, data)
        return await interaction.followup.send(f"<@{old}> is no longer co-captain.", ephemeral=True,
                                               allowed_mentions=NO_PINGS)
    if player is None:
        return await interaction.response.send_message("Pick the teammate to make co-captain.", ephemeral=True)
    if str(player.id) not in t["roster"] or player.id == t["captain"]:
        return await interaction.response.send_message(f"{player.mention} isn't one of your teammates.",
                                                       ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    t["co"] = player.id
    save_data(data)
    if old and old != player.id:
        await give_roles(guild, old, co_role, remove=True)
    await give_roles(guild, player.id, co_role)
    by = " (appointed by staff)" if interaction.user.id != t["captain"] else ""
    await log_transaction(guild, f"{player.mention} is now co-captain of **{t['name']}**{by}", t)
    await update_board(guild, data)
    try:
        await player.send(embed=brand_embed(f"You're now co-captain of **{t['name']}** in {guild.name}. You can "
                                            "sign players with `/offer @player`.", "Co-captain", INFO))
    except discord.HTTPException:
        pass
    await interaction.followup.send(f"{player.mention} is now co-captain"
                                    + (f" (replacing <@{old}>)" if old and old != player.id else "")
                                    + ". They can sign players too.", ephemeral=True, allowed_mentions=NO_PINGS)


@bot.tree.command(description="Leave your team (not while a tournament is being played).")
async def leaveteam(interaction: discord.Interaction):
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    key = team_of(s, interaction.user.id)
    if key is None:
        return await interaction.response.send_message("You're not on a team.", ephemeral=True)
    if tournament_running(s):
        return await interaction.response.send_message(
            "A tournament is being played, so teams are locked. You can leave once it's over, "
            "or ask league staff.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    text = await remove_member(guild, data, key, interaction.user.id, "left")
    await update_board(guild, data)
    await reply_after(interaction, text)


@bot.tree.command(description="Captains: delete your whole team (not while a tournament is being played).")
@app_commands.describe(confirm="Set to True to confirm. Everyone on the team is released.")
async def disbandteam(interaction: discord.Interaction, confirm: bool = False):
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    key = captain_team(s, interaction.user.id)
    if key is None:
        return await interaction.response.send_message("Only a team captain can disband a team.", ephemeral=True)
    if tournament_running(s):
        return await interaction.response.send_message("Teams can't be disbanded during a tournament.",
                                                       ephemeral=True)
    if not confirm:
        return await interaction.response.send_message(
            "This deletes your team and releases everyone on it. Run /disbandteam confirm:True to do it.",
            ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    name = s["teams"][key]["name"]
    await delete_team(guild, data, key, "disbanded by the captain")
    await update_board(guild, data)
    await reply_after(interaction, f"**{name}** has been disbanded and everyone on it is now free to join another team.")


@bot.tree.command(description="Staff: change a team's logo.")
@app_commands.describe(team="The team's role", logo="The new logo (PNG, JPG, WEBP or GIF, under 1 MB)")
@app_commands.default_permissions(manage_roles=True)
async def setlogo(interaction: discord.Interaction, team: discord.Role, logo: discord.Attachment):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can change logos.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    t = s["teams"].get(str(team.id))
    if not t:
        return await interaction.response.send_message(f"{team.mention} isn't a league team.", ephemeral=True,
                                                       allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    filename, problem = await save_logo(logo)
    if problem:
        return await interaction.followup.send(problem, ephemeral=True)
    t["logo"] = filename
    save_data(data)
    ch = guild.get_channel(t.get("channel") or 0)
    if ch:
        await post(ch, "League staff updated your team logo.", title="New logo", file=logo_file(t))
    schedule_publish(guild)
    await interaction.followup.send(f"Logo updated for **{t['name']}**. The website will update in a minute.",
                                    ephemeral=True)


@app_commands.describe(team="The team's role (leave empty for your own team)")
async def teaminfo(interaction: discord.Interaction, team: discord.Role | None = None):
    s = guild_signups(load_data(), interaction.guild.id)
    key = str(team.id) if team else team_of(s, interaction.user.id)
    if not key or key not in s["teams"]:
        return await interaction.response.send_message("Couldn't find that team.", ephemeral=True)
    embed, f = team_embed(interaction.guild, s, key)
    await interaction.response.send_message(embed=embed, ephemeral=True, **({"file": f} if f else {}))


@bot.tree.command(description="See who's on a team (even ones still building), or which team a player is on.")
@app_commands.describe(team="A team's role (leave empty to see every team)",
                       player="Show the team this player is on", private="Only you see the answer (default no)")
async def roster(interaction: discord.Interaction, team: discord.Role | None = None,
                 player: discord.Member | None = None, private: bool = False):
    guild = interaction.guild
    s = guild_signups(load_data(), guild.id)
    if player is not None and team is None:
        key = team_of(s, player.id)
        if not key:
            return await interaction.response.send_message(f"{player.mention} isn't on a team."
                                                           + (" They're a free agent." if player.id in s["free_agents"]
                                                              else ""), ephemeral=True, allowed_mentions=NO_PINGS)
    elif team is not None:
        key = str(team.id)
        if key not in s["teams"]:
            return await interaction.response.send_message(f"{team.mention} isn't a league team.", ephemeral=True,
                                                           allowed_mentions=NO_PINGS)
    else:
        key = None
    if key:  # works for every team, complete or still building
        embed, f = team_embed(guild, s, key)
        t = s["teams"][key]
        if not is_complete(t):
            embed.description += (f"\n\n*Still building: needs {ROSTER_MIN - len(t['roster'])} more player(s) "
                                  f"to be a full team.*")
        return await interaction.response.send_message(embed=embed, ephemeral=private, allowed_mentions=NO_PINGS,
                                                       **({"file": f} if f else {}))
    teams = team_list(s)
    if not teams:
        return await interaction.response.send_message("No teams yet. Start one with /signup.", ephemeral=True)
    blocks = []
    for k, t in teams:
        r = guild.get_role(int(k))
        ppl = ", ".join(f"<@{u}>{' (C)' if int(u) == t['captain'] else ' (CC)' if int(u) == t.get('co') else ''}"
                        for u in t["roster"])
        state = "" if is_complete(t) else f" · still building ({len(t['roster'])}/{ROSTER_MIN})"
        blocks.append(f"**{r.mention if r else t['name']}** · {len(t['roster'])} player(s){state}\n{ppl}")
    pages = pack(blocks, 3800)
    embeds = [brand_embed(pg, f"Rosters · {len(teams)} team(s)" if i == 0 else None, INFO)
              for i, pg in enumerate(pages[:10])]
    await interaction.response.send_message(embeds=embeds, ephemeral=private, allowed_mentions=NO_PINGS)


async def signuplist(interaction: discord.Interaction):
    s = guild_signups(load_data(), interaction.guild.id)
    tz = s.get("tourney")
    if not tz:
        return await interaction.response.send_message("No tournament has been opened yet.", ephemeral=True)
    keys = [k for k in tz["entrants"] if k in s["teams"]]
    lines = [f"{i}. **{s['teams'][k]['name']}** · {points_line(s, k)}" for i, k in enumerate(keys, 1)]
    header = (f"**{tz['name']}**: entries {'open' if s['open'] else 'closed'}, {len(keys)} team(s), "
              f"{MIN_TEAMS} needed.\n")
    await interaction.response.send_message((header + ("\n".join(lines) or "No teams yet."))[:1990],
                                            ephemeral=True, allowed_mentions=NO_PINGS)


@app_commands.default_permissions(manage_roles=True)
async def rosterboard(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can refresh the board.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    for t in s["teams"].values():
        t["board_sig"] = None  # force every card to be re-sent
    await update_board(interaction.guild, data)
    await interaction.followup.send("Team cards refreshed in #rosters.", ephemeral=True)


@bot.tree.command(description="Staff: close entries for the current tournament.")
@app_commands.default_permissions(manage_roles=True)
async def closesignups(interaction: discord.Interaction):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can close entries.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    up = s.get("upcoming")
    if up and up.get("open") and current_busy(s):  # the NEXT tournament's entries
        up["entrants"] = [k for k in up["entrants"] if k in s["teams"]]
        up["open"] = False
        save_data(data)
        ann = chan(guild, "announcements")
        if ann:
            await post(ann, f"**Entries for {up['name']} are closed: {len(up['entrants'])} teams.** It starts once "
                            f"**{s['tourney']['name']}** is finished.")
        schedule_publish(guild)
        return await interaction.response.send_message(
            f"Entries for **{up['name']}** are closed ({len(up['entrants'])} teams). It becomes the current tournament "
            "automatically when this one ends.", ephemeral=True)
    tz = s.get("tourney")
    if not tz or not s["open"]:
        return await interaction.response.send_message("No tournament is taking entries.", ephemeral=True)
    tz["entrants"] = [k for k in tz["entrants"] if k in s["teams"]]
    short = [k for k in tz["entrants"] if not is_complete(s["teams"][k])]
    ok = len(tz["entrants"]) - len(short)
    if ok < MIN_TEAMS:
        return await interaction.response.send_message(
            f"Only {ok} complete team(s) registered and a tournament needs {MIN_TEAMS}. Entries stay open.",
            ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    for k in short:
        tz["entrants"].remove(k)  # rosters that dropped below the minimum after registering
    s["open"], s["closes"] = False, None
    save_data(data)
    await update_board(guild, data)
    names = ", ".join(f"**{s['teams'][k]['name']}**" for k in tz["entrants"])
    ann = chan(guild, "announcements")
    if ann:
        await post(ann, f"**Entries for {tz['name']} are closed: {len(tz['entrants'])} teams.**\n{names}\n"
                       "The draw is coming soon.")
    dropped = (" Removed (roster under " + str(ROSTER_MIN) + "): "
               + ", ".join(s["teams"][k]["name"] for k in short) + ".") if short else ""
    await interaction.followup.send(f"Entries closed with {len(tz['entrants'])} teams.{dropped}\n"
                                    "Next: /startswiss, /startgroups, or /startmain.", ephemeral=True)


@bot.tree.command(description="Commissioner/admin: rename a team (role, team channels, rosters and website).")
@app_commands.describe(team="The team to rename", new_name="The new team name")
@app_commands.default_permissions(manage_roles=True)
async def renameteam(interaction: discord.Interaction, team: discord.Role, new_name: str):
    guild = interaction.guild
    if not is_commissioner(interaction.user):
        return await interaction.response.send_message("Only the Commissioner or an admin can rename teams.",
                                                       ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    key = str(team.id)
    t = s["teams"].get(key)
    new_name = re.sub(r"\s+", " ", new_name).strip()
    problem = None
    if t is None:
        problem = f"{team.mention} isn't a league team."
    elif not 2 <= len(new_name) <= 32:
        problem = "Team names need to be 2 to 32 characters."
    elif any(k != key and x["name"].lower() == new_name.lower() for k, x in s["teams"].items()) or \
            (role(guild, new_name) and role(guild, new_name).id != team.id):
        problem = f"There's already a team or role called **{new_name}**."
    elif t["name"] == new_name:
        problem = f"That team is already called **{new_name}**."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    old = t["name"]
    t["name"] = new_name
    save_data(data)
    notes = []
    reason = f"Renamed by {interaction.user}"
    try:
        await team.edit(name=new_name, reason=reason)
    except discord.HTTPException:
        notes.append("couldn't rename the role (move my role above it)")
    for cid, fmt in ((t.get("channel"), "{}"), (t.get("voice"), "🔊 {}")):
        ch = guild.get_channel(int(cid)) if cid else None
        if ch:
            try:
                await ch.edit(name=fmt.format(new_name), reason=reason)
            except discord.HTTPException:
                notes.append(f"couldn't rename {ch.mention}")
    team_ch = guild.get_channel(int(t["channel"])) if t.get("channel") else None
    if team_ch:
        await post(team_ch, f"Your team is now called **{new_name}** (was {old}).", title="Team renamed", color=INFO)
    await log_transaction(guild, f"**{old}** is now **{new_name}** (renamed by {interaction.user.mention})", t)
    await update_board(guild, data)  # rosters, registered channel and the website
    await interaction.followup.send(f"Renamed **{old}** to **{new_name}**."
                                    + (" Note: " + "; ".join(notes) + "." if notes else ""), ephemeral=True)


@bot.tree.command(description="Commissioner/admin: create a team for someone (they become captain).")
@app_commands.describe(name="Team name", captain="The captain", logo="Team logo (PNG, JPG, WEBP or GIF, under 1 MB)")
@app_commands.default_permissions(manage_roles=True)
async def addteam(interaction: discord.Interaction, name: str, captain: discord.Member, logo: discord.Attachment):
    guild = interaction.guild
    if not is_commissioner(interaction.user):
        return await interaction.response.send_message("Only the Commissioner or an admin can create a team for someone.",
                                                       ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    name = name.strip()
    problem = None
    if team_of(s, captain.id):
        problem = f"{captain.mention} is already on a team."
    elif any(t["name"].lower() == name.lower() for t in s["teams"].values()) or role(guild, name):
        problem = f"The name **{name}** is taken."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    filename, problem = await save_logo(logo)
    if problem:
        return await interaction.followup.send(problem, ephemeral=True)
    key = await create_team(guild, data, name, captain, filename)
    await log_transaction(guild, f"New team: **{name}**, captain {captain.mention} (added by staff)", s["teams"][key])
    await update_board(guild, data)
    await interaction.followup.send(f"Created **{name}** with {captain.mention} as captain.", ephemeral=True,
                                    allowed_mentions=NO_PINGS)


@bot.tree.command(description="Staff: delete a team's role and channel.")
@app_commands.describe(team="The team's role")
@app_commands.default_permissions(manage_roles=True)
async def removeteam(interaction: discord.Interaction, team: discord.Role):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can remove teams.", ephemeral=True)
    data = load_data()
    if str(team.id) not in guild_signups(data, interaction.guild.id)["teams"]:
        return await interaction.response.send_message(f"{team.mention} isn't a league team.", ephemeral=True,
                                                       allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    await delete_team(interaction.guild, data, str(team.id), "removed by staff")
    await update_board(interaction.guild, data)
    await reply_after(interaction, "Team removed.")


@bot.tree.command(description="Turn the Free Agent role on or off.")
@app_commands.describe(position="The position you play (needed the first time)")
@app_commands.choices(position=[app_commands.Choice(name=n, value=v) for v, n in POSITIONS])
async def freeagent(interaction: discord.Interaction, position: str | None = None):
    guild, user = interaction.guild, interaction.user
    pre = guild_signups(load_data(), guild.id)
    if suspended_from(pre, user.id, "league") and user.id not in pre["free_agents"]:
        return await interaction.response.send_message(suspended_from(pre, user.id, "league"), ephemeral=True)
    if position:
        d0 = load_data()
        guild_signups(d0, guild.id).setdefault("positions", {})[str(user.id)] = position
        save_data(d0)
    elif not pos_of(pre, user.id) and user.id not in pre["free_agents"]:
        return await interaction.response.send_message("Add your position: /freeagent position:PG (or SG, SF, PF, C).",
                                                       ephemeral=True)
    fa = role(guild, "Free Agent")
    if fa is None:
        return await interaction.response.send_message("Staff need to run /setupbot part:server first.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    if fa in user.roles or user.id in s["free_agents"]:
        if user.id in s["free_agents"]:
            s["free_agents"].remove(user.id)
        save_data(data)
        await interaction.response.defer(ephemeral=True)
        await give_roles(guild, user.id, fa, remove=True)
        msg = "Removed your Free Agent role."
    else:
        if team_of(s, user.id):
            return await interaction.response.send_message("You're already on a team.", ephemeral=True)
        s["free_agents"].append(user.id)
        save_data(data)
        await interaction.response.defer(ephemeral=True)
        await give_roles(guild, user.id, fa)
        pr = profiles(s).get(str(user.id)) or {}
        msg = ("You're now a Free Agent: your profile card is posted in #free-agents."
               + ("" if pr.get("build") and pr.get("ovr") and pr.get("activity") else
                  " Add your build, OVR and activity with `/profile build:... ovr:... activity:...` so captains "
                  "can scout you."))
    await update_board(guild, data)
    await interaction.followup.send(msg, ephemeral=True)


# ---------------------------------------------------------------- player profiles + the free agent board
#
# /profile build:... ovr:... activity:... position:...  sets your own profile (staff can fix anyone's with player:).
# /profile [player]  shows a profile card. Free agents are listed in #free-agents on a board the bot keeps
# updated: grouped by position, best OVR first, with build, OVR and activity (all self-reported).

def profiles(s: dict) -> dict:
    return s.setdefault("profiles", {})  # user id -> {build, ovr, activity, updated}


def activity_bar(n) -> str:
    n = max(0, min(10, int(n or 0)))
    return "▰" * n + "▱" * (10 - n)


def profile_line(s: dict, uid) -> str:
    pr = profiles(s).get(str(uid)) or {}
    bits = [pr.get("build") or "build not set",
            f"**{pr['ovr']} OVR**" if pr.get("ovr") else "OVR not set",
            f"Activity {pr['activity']}/10" if pr.get("activity") else "activity not set"]
    return " · ".join(bits)


_rbx_cache: dict[str, dict] = {}  # roblox username (lowercase) -> {"id", "img", "at"}


async def roblox_lookup(username: str) -> dict:
    """{'id': Roblox user id or None, 'img': avatar headshot URL or None}. Server names are Roblox usernames.
    Cached for 6 hours so the bot doesn't ask Roblox every time."""
    import time as _time
    key = (username or "").strip().lower()
    hit = _rbx_cache.get(key)
    if hit and _time.time() - hit["at"] < 6 * 3600:
        return hit
    out = {"id": None, "img": None, "at": _time.time()}
    if not re.match(r"^[A-Za-z0-9_]{3,20}$", key):
        _rbx_cache[key] = out
        return out
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=8)) as session:
            async with session.post("https://users.roblox.com/v1/usernames/users",
                                    json={"usernames": [key], "excludeBannedUsers": False}) as r:
                found = (await r.json()).get("data", []) if r.status == 200 else []
            if found:
                out["id"] = found[0]["id"]
                async with session.get("https://thumbnails.roblox.com/v1/users/avatar-headshot",
                                       params={"userIds": str(out["id"]), "size": "420x420", "format": "Png",
                                               "isCircular": "false"}) as r:
                    imgs = (await r.json()).get("data", []) if r.status == 200 else []
                if imgs and imgs[0].get("imageUrl"):
                    out["img"] = imgs[0]["imageUrl"]
    except Exception as e:
        print(f"[roblox] {username}: {e}")
        if hit:
            return hit
    _rbx_cache[key] = out
    return out


def roblox_name(member) -> str:
    """Server names are Roblox usernames. Two names, like "yaro (yachtyshifts)": the one in brackets is Roblox."""
    name = (getattr(member, "display_name", None) or str(member)).strip()
    m = re.search(r"\(([^()]+)\)\s*$", name)
    return m.group(1).strip() if m else name


async def profile_embed(guild: discord.Guild, s: dict, member: discord.abc.User) -> discord.Embed:
    """One player's profile card: their Roblox avatar as the picture and their Roblox name as the title."""
    pr = profiles(s).get(str(member.id)) or {}
    key = team_of(s, member.id)
    t = s["teams"].get(key) if key else None
    name = roblox_name(member)  # the Roblox username (from brackets if they have two names)
    rbx = await roblox_lookup(name)
    link = (f"https://www.roblox.com/users/{rbx['id']}/profile" if rbx.get("id")
            else f"https://www.roblox.com/user.aspx?username={urllib.parse.quote(name)}")
    if t:
        status = f"🏀 **{t['name']}**" + (" · Captain" if t["captain"] == member.id else " · Co-Captain"
                                          if t.get("co") == member.id else "")
    elif member.id in s["free_agents"]:
        status = "🆓 **FREE AGENT** · captains, sign them with `/offer`"
    else:
        status = "No team"
    act = pr.get("activity")
    desc = (f"{status}\n<@{member.id}>\n\n"
            f"**Position:** {pos_of(s, member.id) or 'not set'}\n"
            f"**Build:** {pr.get('build') or 'not set'}\n"
            f"**OVR:** {pr.get('ovr') or 'not set'}\n"
            f"**Activity:** " + (f"{activity_bar(act)} {act}/10" if act else "not set")
            + f"\n\n[View Roblox profile]({link})")
    if not pr:
        desc += "\n*Set it up with `/profile build:... ovr:... activity:...`*"
    shown = getattr(member, "display_name", None) or name
    e = brand_embed(desc, shown, GOLD if not t else INFO, url=link)
    if rbx.get("img"):
        e.set_thumbnail(url=rbx["img"])
    else:
        try:
            e.set_thumbnail(url=member.display_avatar.url)  # not found on Roblox: fall back to the Discord picture
        except AttributeError:
            pass
    e.set_footer(text="Build, OVR and activity are self-reported · ON THE RISE · PB CIRCUIT")
    return e


async def refresh_fa_cards(guild: discord.Guild, data: dict):
    """#free-agents: one profile card per free agent (Roblox avatar, position, build, OVR, activity).
    Cards update when the profile changes and disappear when the player joins a team or stops being a free agent."""
    s = guild_signups(data, guild.id)
    ch = chan(guild, "free-agents")
    if ch is None:
        return
    if s.get("fa_board"):  # the old all-in-one list: replaced by single cards
        try:
            await (await ch.fetch_message(s["fa_board"])).delete()
        except discord.HTTPException:
            pass
        s["fa_board"], s["fa_board_sig"] = None, None
    cards = s.setdefault("fa_cards", {})  # user id -> [message id, signature]
    want = [u for u in s["free_agents"] if not team_of(s, u)]
    for uid in [u for u in cards if int(u) not in want]:
        try:
            await (await ch.fetch_message(cards[uid][0])).delete()
        except discord.HTTPException:
            pass
        cards.pop(uid, None)
    for u in want:
        member = guild.get_member(int(u))
        if member is None:
            continue
        sig = json.dumps([roblox_name(member), pos_of(s, u), profiles(s).get(str(u))])
        have = cards.get(str(u))
        if have and have[1] == sig:
            continue
        emb = await profile_embed(guild, s, member)
        msg = None
        if have:
            try:
                msg = await ch.fetch_message(have[0])
                await msg.edit(embed=emb, allowed_mentions=NO_PINGS)
            except discord.HTTPException:
                msg = None
        if msg is None:
            msg = await ch.send(embed=emb, allowed_mentions=NO_PINGS)
        cards[str(u)] = [msg.id, sig]


@bot.tree.command(description="See a player's profile, or set yours: build, OVR and activity (1-10).")
@app_commands.describe(player="Whose profile to see (staff: whose profile to change)",
                       build="Your build, e.g. Playmaking Shot Creator", ovr="Your OVR (1-99)",
                       activity="How active you are, 1 (rarely on) to 10 (on every day)",
                       position="Your position")
@app_commands.choices(position=[app_commands.Choice(name=n, value=v) for v, n in POSITIONS])
async def profile(interaction: discord.Interaction, player: discord.Member | None = None, build: str | None = None,
                  ovr: app_commands.Range[int, 1, 99] | None = None,
                  activity: app_commands.Range[int, 1, 10] | None = None, position: str | None = None):
    guild = interaction.guild
    editing = any(v is not None for v in (build, ovr, activity, position))
    target = player or interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    if not editing:
        await interaction.response.defer()
        return await interaction.followup.send(embed=await profile_embed(guild, s, target), allowed_mentions=NO_PINGS)
    if player is not None and player.id != interaction.user.id and not is_staff(interaction.user):
        return await interaction.response.send_message("You can only change your own profile.", ephemeral=True)
    pr = profiles(s).setdefault(str(target.id), {})
    if build is not None:
        pr["build"] = re.sub(r"\s+", " ", build).strip()[:40] or None
    if ovr is not None:
        pr["ovr"] = ovr
    if activity is not None:
        pr["activity"] = activity
    if position is not None:
        s.setdefault("positions", {})[str(target.id)] = position
    pr["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    save_data(data)
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send("Profile saved." + (" Your free agent card in #free-agents is updated."
                                                        if target.id in s["free_agents"] else ""),
                                    embed=await profile_embed(guild, s, target), ephemeral=True)
    await update_board(guild, data)


# ---- end of season: ask every player if they're staying

class StayOrLeave(discord.ui.View):
    """Buttons for the end-of-season message. Clicks are handled in on_interaction, so they work after restarts."""

    def __init__(self, guild_id: int, key: str, user_id: int):
        super().__init__(timeout=None)
        base = f"{guild_id}:{key}:{user_id}"
        self.add_item(discord.ui.Button(label="Stay on the team", style=discord.ButtonStyle.success,
                                        custom_id=f"pbl:stay:{base}"))
        self.add_item(discord.ui.Button(label="Leave the team", style=discord.ButtonStyle.danger,
                                        custom_id=f"pbl:leave:{base}"))


async def season_end(guild: discord.Guild):
    """DM every rostered player and ask if they're staying. Falls back to the team channel if DMs are closed."""
    s = guild_signups(load_data(), guild.id)
    tname = (s.get("tourney") or {}).get("name", "The tournament")
    asked = failed = 0
    for key, t in team_list(s):
        ch = guild.get_channel(t.get("channel") or 0)
        for uid in list(t["roster"]):
            text = (f"**{tname}** is over. Thanks for playing with **{t['name']}**!\n"
                    f"Do you want to stay on the team, or leave it? If fewer than {CORE_MIN} of the players "
                    "who earned your team's RISER POINTS stay, the team loses its points.")
            view = StayOrLeave(guild.id, key, int(uid))
            try:
                user = await bot.fetch_user(int(uid))
                await post(user, text, title="Stay or leave?", color=GOLD, view=view, file=logo_file(t))
                asked += 1
            except discord.HTTPException:
                failed += 1
                if ch:
                    await post(ch, text, title="Stay or leave?", color=GOLD, view=view, ping=f"<@{uid}>")
            await asyncio.sleep(0.5)  # go easy on Discord's rate limits
    ann = chan(guild, "announcements")
    if ann:
        await post(ann, f"**{tname} is over!** Every player has been asked in DMs whether they're staying "
                       "with their team. Check your DMs (or your team channel).")
    print(f"[season end] asked {asked} players by DM, {failed} in team channels")


@bot.listen("on_interaction")
async def stay_or_leave_click(interaction: discord.Interaction):
    cid = (interaction.data or {}).get("custom_id", "") if interaction.type == discord.InteractionType.component else ""
    if not cid.startswith("pbl:"):
        return
    try:
        _p, action, gid, key, uid = cid.split(":")
    except ValueError:
        return
    if interaction.user.id != int(uid):
        return await interaction.response.send_message("These buttons are for someone else.", ephemeral=True)
    guild = bot.get_guild(int(gid))
    if guild is None:
        return await interaction.response.send_message("I can't find that server any more.", ephemeral=True)
    if action in ("accept", "decline"):
        return await answer_offer(interaction, guild, action, key, int(uid))
    data = load_data()
    s = guild_signups(data, guild.id)
    t = s["teams"].get(key)
    if not t or uid not in t["roster"]:
        return await interaction.response.edit_message(content="You're no longer on that team.", view=None)
    if action == "stay":
        await interaction.response.edit_message(content=f"You're staying with **{t['name']}**. See you next tournament!",
                                                view=None)
        ch = guild.get_channel(t.get("channel") or 0)
        if ch:
            await post(ch, f"<@{uid}> is staying on the team.", title="Staying", color=GOOD)
    elif action == "leave":
        await interaction.response.edit_message(content=f"You've left **{t['name']}**. Thanks for playing!",
                                                view=None)
        await remove_member(guild, data, key, int(uid), "left")
        await update_board(guild, data)


@bot.tree.command(description="Staff: end the tournament early and ask every player (by DM) if they're staying.")
@app_commands.describe(confirm="Set to True to send the DMs")
@app_commands.default_permissions(manage_roles=True)
async def endseason(interaction: discord.Interaction, confirm: bool = False):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can end a tournament.", ephemeral=True)
    if not confirm:
        return await interaction.response.send_message(
            "This DMs every player asking if they'll stay with their team. Run /endseason confirm:True to send.",
            ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    if s["event"] and s["event"]["stage"] != "done":
        s["event"]["stage"] = "done"  # unlock rosters
        save_data(data)
    await interaction.response.send_message("Sending the stay-or-leave DMs now.", ephemeral=True)
    await season_end(interaction.guild)


# ---------------------------------------------------------------- RISER POINTS circuit
#
# s["tourney"]  the tournament currently taking entries / being played:
#               {"name", "kind": "event" | "major", "spec": {"1": 100, ...}, "spec_text", "entrants": [team keys]}
# s["circuit"]  {"needed": RISER POINTS needed for the Major, "qualified": [team keys that won an event]}
# each team:    "points" (RISER POINTS) and "core" (Discord IDs on the roster when it last earned points).
#               If fewer than CORE_MIN of the core are still on the team, its points (and Major spot) are lost.

CORE_MIN = 3
DEFAULT_SPEC = "1:300, 2:210, 3:150, 4:120, 5-6:75, 7-8:45, 9-12:30, 13-16:15, 17-24:10, 25-32:5"
# Teams tied in a placement group (5th-6th, 9th-12th...) all get the same points.
OLD_DEFAULT_SPEC = "1:100, 2:70, 3:50, 4:40, 5-6:25, 7-8:15, 9-12:10, 13-16:5"


def default_payout(s: dict) -> dict:
    """The saved /payout table, or the default. A table saved before the default went to 300 is upgraded."""
    saved = circuit(s).get("payout")
    if saved and saved != parse_spec(OLD_DEFAULT_SPEC)[0]:
        return dict(saved)
    return parse_spec(DEFAULT_SPEC)[0]
TEST_NAMES: dict[int, str] = {}  # fake teams used by /testtournament


def parse_spec(text: str) -> tuple[dict, str | None]:
    """'1:100, 2:70, 5-6:25' -> {'1': 100, '2': 70, '5': 25, '6': 25}. Returns (spec, problem)."""
    spec = {}
    parts = [p.strip() for p in re.split(r"[,\n;]", text or "") if p.strip()]
    if not parts:
        return {}, "Give points like: 1:300, 2:210, 3:150, 4:120, 5-6:75"
    for p in parts:
        m = re.fullmatch(r"(\d+)(?:\s*-\s*(\d+))?\s*(?:st|nd|rd|th)?\s*[:=]\s*(\d+)", p, re.I)
        if not m:
            return {}, f"Couldn't read '{p}'. Use place:points, like 1:100 or 5-6:25."
        a, b, pts = int(m.group(1)), int(m.group(2) or m.group(1)), int(m.group(3))
        if a < 1 or b < a or b > 128:
            return {}, f"'{p}' isn't a valid placement range."
        for place in range(a, b + 1):
            spec[str(place)] = pts
    return spec, None


def spec_text(spec: dict) -> str:
    """{'1':100,'5':25,'6':25} -> '1st: 100 · 5th-6th: 25'"""
    def nth(n):
        return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"
    places = sorted(int(k) for k in spec)
    out, i = [], 0
    while i < len(places):
        j = i
        while j + 1 < len(places) and places[j + 1] == places[j] + 1 and spec[str(places[j + 1])] == spec[str(places[i])]:
            j += 1
        label = nth(places[i]) if i == j else f"{nth(places[i])}-{nth(places[j])}"
        out.append(f"{label}: {spec[str(places[i])]}")
        i = j + 1
    return " · ".join(out)


MAJOR_TARGET = 600  # RISER POINTS needed for the Major (change any time with /tournament major_target:)


def circuit(s: dict) -> dict:
    c = s.setdefault("circuit", {})
    c.setdefault("needed", MAJOR_TARGET)
    c.setdefault("qualified", [])
    if not c.get("target_600"):  # the Major target is now 600 (was unset, or 700)
        if c["needed"] in (None, 700):
            c["needed"] = MAJOR_TARGET
        c["target_600"] = True
    return c


def is_complete(t: dict) -> bool:
    return len(t["roster"]) >= ROSTER_MIN


def major_qualified(s: dict, key: str) -> bool:
    c = circuit(s)
    t = s["teams"].get(key, {})
    return key in c["qualified"] or (c["needed"] is not None and t.get("points", 0) >= c["needed"])


# ---- Last Chance Qualifier (LCQ)
#
# /opensignups kind:LCQ invites the next LCQ_INVITES teams that haven't qualified for the Major (most RISER POINTS
# first, complete rosters only). It's invite-only: no /register. Run the bracket as usual (/startmain); the top
# LCQ_SPOTS finishers qualify for the Major. No RISER POINTS are given.

LCQ_INVITES = 8
LCQ_SPOTS = 4


def lcq_invites(s: dict) -> tuple[list[str], list[str], int]:
    """(teams straight in, teams tied at the cutoff, spots left for them). When more teams are tied at the
    cutoff than there are spots, ALL of them are invited to a single-elimination play-in for those spots."""
    pool = [(k, t) for k, t in team_list(s) if is_complete(t) and not major_qualified(s, k)]
    pool.sort(key=lambda kt: (-kt[1].get("points", 0), kt[1]["name"].lower()))
    if len(pool) <= LCQ_INVITES:
        return [k for k, _t in pool], [], 0
    cut = pool[LCQ_INVITES - 1][1].get("points", 0)
    above = [k for k, t in pool if t.get("points", 0) > cut]
    tied = [k for k, t in pool if t.get("points", 0) == cut]
    spots = LCQ_INVITES - len(above)
    if len(tied) <= spots:
        return above + tied, [], 0
    return above, tied, spots


def playin_round(ev: dict) -> list[dict]:
    """Make the next play-in round: only as many games as needed so exactly `spots` teams are left."""
    pi = ev["playin"]
    alive, spots = pi["alive"], pi["spots"]
    games = min(len(alive) // 2, len(alive) - spots)
    if games <= 0:
        return []
    pi["round"] += 1
    playing = alive[len(alive) - 2 * games:]  # lowest seeds play, the rest get a bye this round
    new = []
    for i in range(games):
        a, b = playing[i], playing[-1 - i]
        mid = ev["next_id"]
        ev["next_id"] += 1
        new.append({"id": mid, "round": pi["round"], "label": f"LCQ play-in round {pi['round']}", "a": int(a),
                    "b": int(b), "winner": None, "score": None, "pts": None})
    pi["matches"] += new
    return new


def playin_ready(ev: dict | None) -> list[dict]:
    pi = (ev or {}).get("playin")
    if not pi or pi.get("done"):
        return []
    return [m for m in pi["matches"] if not m["winner"]]


def playin_start(s: dict, tied: list[str], spots: int) -> dict:
    ev = new_event("playin")
    order = list(tied)
    RNG.shuffle(order)  # tied on points, so the play-in seeding is a coin flip
    ev["playin"] = {"teams": order, "alive": list(order), "spots": spots, "round": 0, "matches": [], "done": False,
                    "out": []}
    playin_round(ev)
    s["event"] = ev
    return ev


def lcq_line(s: dict) -> list[str]:
    """Eligible teams not in the LCQ yet, best first: the waiting list."""
    tz = s.get("tourney") or {}
    info = tz.get("lcq") or {}
    done_with = set(tz.get("entrants", [])) | set(info.get("invited", [])) | set(info.get("next_up", []))
    pi = (s.get("event") or {}).get("playin") or {}
    if pi and not pi.get("done"):
        done_with |= {str(t) for t in pi.get("teams", [])}
    pool = [(k, t) for k, t in team_list(s) if is_complete(t) and not major_qualified(s, k)
            and k not in done_with]  # teams that dropped out aren't invited back
    pool.sort(key=lambda kt: (-kt[1].get("points", 0), kt[1]["name"].lower()))
    return [k for k, _t in pool]


def lcq_fill(s: dict) -> list[str]:
    """Odd number of LCQ teams (someone dropped out, or not enough invites)? The next man up is invited."""
    tz = s.get("tourney") or {}
    if tz.get("kind") != "lcq" or (s.get("event") or {}).get("stage") == "playin":
        return []
    info = tz.setdefault("lcq", {"invited": list(tz.get("entrants", [])), "next_up": []})
    added = []
    while len(tz["entrants"]) % 2 == 1:
        line = lcq_line(s)
        if not line:
            break
        tz["entrants"].append(line[0])
        info["next_up"].append(line[0])
        added.append(line[0])
    return added


async def lcq_announce_next_up(guild: discord.Guild, s: dict, added: list[str]):
    tz = s.get("tourney") or {}
    for k in added:
        t = s["teams"].get(k, {})
        ann = chan(guild, "announcements")
        if ann:
            await post(ann, f"**{t.get('name', 'A team')}** ({t.get('points', 0)} RISER POINTS) is the **next man up** "
                            f"and is now in **{tz.get('name', 'the LCQ')}**.", title="LCQ: next man up", color=GOLD)
        for uid in captains_of(s, k):
            await dm(uid, brand_embed(f"A spot opened in **{tz.get('name', 'the LCQ')}** and **{t.get('name', 'your team')}** "
                                      f"is next in line, so you're in! The top {LCQ_SPOTS} qualify for the Major. "
                                      "No /register needed. Watch #bracket for the draw.", "🎟️ Next man up: you're in",
                                      GOLD))


def points_line(s: dict, key: str) -> str:
    t = s["teams"][key]
    c = circuit(s)
    pts = t.get("points", 0)
    if key in c["qualified"]:
        return f"**{pts} RISER POINTS** · already qualified for the Major (tournament winner)"
    if c["needed"] is None:
        return f"**{pts} RISER POINTS**"
    if pts >= c["needed"]:
        return f"**{pts} RISER POINTS** · qualified for the Major ({c['needed']} needed)"
    return f"**{pts} RISER POINTS** · needs {c['needed'] - pts} more ({c['needed']} to qualify for the Major)"


def entrant_roles(guild: discord.Guild) -> list[discord.Role]:
    """The teams entered in the current tournament."""
    s = guild_signups(load_data(), guild.id)
    tz = s.get("tourney") or {}
    return [r for k in tz.get("entrants", []) if k in s["teams"] and (r := guild.get_role(int(k)))]


def check_core(s: dict, key: str) -> str | None:
    """After someone leaves: if fewer than CORE_MIN of the players who earned the points remain, wipe them."""
    t = s["teams"].get(key)
    c = circuit(s)
    if not t or (not t.get("points") and key not in c["qualified"]):
        return None
    remaining = [u for u in t.get("core", []) if str(u) in t["roster"]]
    if len(remaining) >= CORE_MIN:
        return None
    lost = t.get("points", 0)
    t["points"], t["core"] = 0, []
    had_spot = key in c["qualified"]
    if had_spot:
        c["qualified"].remove(key)
    extra = " and its automatic Major spot" if had_spot else ""
    return (f"**{t['name']}** has fewer than {CORE_MIN} of the players who earned its points, "
            f"so it lost its {lost} RISER POINTS{extra}.")


def de_record(ev: dict, m: dict, winner: int, loser: int):
    """Record a main-draw result, including the Grand Final reset."""
    main = ev["main"]
    m.update(winner=winner, loser=loser, done=True)
    reset = False
    if m["gf"] == 1 and winner == m["b"]:
        mid = ev["next_id"]
        ev["next_id"] += 1
        main["matches"].append({"id": mid, "label": "Grand Final Reset", "gf": 2,
                                "a_src": ["team", m["a"]], "b_src": ["team", m["b"]],
                                "a": None, "b": None, "a_ok": False, "b_ok": False,
                                "winner": None, "loser": None, "done": False, "posted": False})
        reset = True
    elif m["gf"]:
        main["champion"] = winner
    de_resolve(main)
    return reset


def final_standings(ev: dict) -> list[tuple[int, list[int]]]:
    """[(placement, [team ids tied there]), ...] from the champion down, then non-qualifiers.
    Disqualified teams are left out (no placement, no points)."""
    dq = set(ev.get("dq") or [])
    return [(p, [t for t in ts if t not in dq]) for p, ts in _final_standings(ev) if [t for t in ts if t not in dq]]


def _final_standings(ev: dict) -> list[tuple[int, list[int]]]:
    main = ev["main"]
    out, placed = [], set()
    if main.get("champion"):
        out.append((1, [main["champion"]]))
        placed.add(main["champion"])
    gfs = [m for m in main["matches"] if m["gf"] and m["done"] and m["loser"] is not None]
    if gfs and gfs[-1]["loser"] not in placed:
        out.append((2, [gfs[-1]["loser"]]))
        placed.add(gfs[-1]["loser"])
    rounds = []
    for m in main["matches"]:
        if m["label"].startswith("Losers"):
            if not rounds or rounds[-1][0] != m["label"]:
                rounds.append((m["label"], []))
            rounds[-1][1].append(m)
    place = len(placed) + 1
    for _label, ms in reversed(rounds):
        gone = [m["loser"] for m in ms if m["done"] and m["loser"] is not None and m["loser"] not in placed]
        if gone:
            out.append((place, gone))
            placed.update(gone)
            place += len(gone)
    # teams knocked out in the qualifier, ranked by wins
    wins = {}
    if ev.get("swiss"):
        wins = {int(t): r["w"] for t, r in ev["swiss"]["rec"].items()}
    elif ev.get("groups"):
        for gi in range(len(ev["groups"]["groups"])):
            _order, st = group_table(ev["groups"], gi)
            wins.update({t: r["w"] for t, r in st.items()})
    rest = [t for t in wins if t not in placed]
    for w in sorted({wins[t] for t in rest}, reverse=True):
        tied = [t for t in rest if wins[t] == w]
        out.append((place, tied))
        place += len(tied)
    return out


def nth(n: int) -> str:
    return f"{n}{'th' if 10 <= n % 100 <= 20 else {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')}"


def place_label(place: int, count: int) -> str:
    return nth(place) if count == 1 else f"{nth(place)}-{nth(place + count - 1)}"


def award_points(s: dict, ev: dict) -> list[str]:
    """Give RISER POINTS for the finished tournament, qualify the winner, or reset everything after a Major."""
    tz = s.get("tourney") or {}
    c = circuit(s)
    standings = final_standings(ev)
    lines = []
    if tz.get("kind") == "major":
        for t in s["teams"].values():
            t["points"], t["core"] = 0, []
        c["qualified"] = []
        lines.append("# Major complete\nAll RISER POINTS are reset to 0 for the next circuit.")
        for place, teams in standings[:4]:
            lines.append(f"{place_label(place, len(teams))}: " + ", ".join(tag(t) for t in teams))
        return lines
    if tz.get("kind") == "lcq":
        lines.append(f"# {tz.get('name', 'LCQ')}: final standings\nThe top {LCQ_SPOTS} qualify for the Major.")
        got = 0
        for place, teams in standings:
            for tid in teams:
                key = str(tid)
                if got < LCQ_SPOTS and key in s["teams"]:
                    got += 1
                    if key not in c["qualified"]:
                        c["qualified"].append(key)
            mark = " → **qualified for the Major**" if place <= LCQ_SPOTS else ""
            lines.append(f"{place_label(place, len(teams))}: " + ", ".join(tag(t) for t in teams) + mark)
        return lines
    spec = tz.get("spec") or default_payout(s)
    lines.append(f"# {tz.get('name', 'Tournament')}: final standings and RISER POINTS")
    for place, teams in standings:
        pts = spec.get(str(place), 0)
        for tid in teams:
            t = s["teams"].get(str(tid))
            if t is not None and pts:
                t["points"] = t.get("points", 0) + pts
                t["core"] = [int(u) for u in t["roster"]]  # these players have to stick together to keep them
        lines.append(f"{place_label(place, len(teams))}: " + ", ".join(tag(t) for t in teams) + f"  +{pts}")
    champ = str(ev["main"].get("champion"))
    if not tz.get("winner_qualifies", True):
        if champ in s["teams"]:
            lines.append(f"{tag(int(champ))} won the tournament. (This one doesn't give the winner a Major spot.)")
    elif champ in s["teams"] and champ not in c["qualified"]:
        c["qualified"].append(champ)
        lines.append(f"{tag(int(champ))} won the tournament and **qualified for the Major**.")
    return lines


PLACEMENT_GROUPS = [("place_1", 1, 1), ("place_2", 2, 2), ("place_3", 3, 3), ("place_4", 4, 4),
                    ("place_5_6", 5, 6), ("place_7_8", 7, 8), ("place_9_12", 9, 12), ("place_13_16", 13, 16),
                    ("place_17_24", 17, 24), ("place_25_32", 25, 32), ("place_33_48", 33, 48),
                    ("place_49_64", 49, 64)]


@bot.tree.command(description="Staff: set how many RISER POINTS each finishing position is worth.")
@app_commands.describe(place_1="Points for 1st", place_2="Points for 2nd", place_3="Points for 3rd",
                       place_4="Points for 4th", place_5_6="Points for 5th-6th", place_7_8="Points for 7th-8th",
                       place_9_12="Points for 9th-12th", place_13_16="Points for 13th-16th",
                       place_17_24="Points for 17th-24th", place_25_32="Points for 25th-32nd",
                       place_33_48="Points for 33rd-48th", place_49_64="Points for 49th-64th",
                       save_as_default="Also use this table for future tournaments (default yes)")
@app_commands.default_permissions(manage_roles=True)
async def payout(interaction: discord.Interaction,
                 place_1: app_commands.Range[int, 0, 100000] | None = None,
                 place_2: app_commands.Range[int, 0, 100000] | None = None,
                 place_3: app_commands.Range[int, 0, 100000] | None = None,
                 place_4: app_commands.Range[int, 0, 100000] | None = None,
                 place_5_6: app_commands.Range[int, 0, 100000] | None = None,
                 place_7_8: app_commands.Range[int, 0, 100000] | None = None,
                 place_9_12: app_commands.Range[int, 0, 100000] | None = None,
                 place_13_16: app_commands.Range[int, 0, 100000] | None = None,
                 place_17_24: app_commands.Range[int, 0, 100000] | None = None,
                 place_25_32: app_commands.Range[int, 0, 100000] | None = None,
                 place_33_48: app_commands.Range[int, 0, 100000] | None = None,
                 place_49_64: app_commands.Range[int, 0, 100000] | None = None,
                 save_as_default: bool = True):
    """Fill in only the positions you want to change; the rest keep their current value."""
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can set payouts.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    tz = s.get("tourney")
    live = tz and tz.get("kind") != "major" and not (s["event"] and s["event"]["stage"] == "done")
    base = dict((tz or {}).get("spec") or {}) if live else {}
    base = base or default_payout(s)
    given = {name: v for name, v in locals().items() if name.startswith("place_") and v is not None}
    for name, lo, hi in PLACEMENT_GROUPS:
        if name in given:
            for place in range(lo, hi + 1):
                base[str(place)] = given[name]
    base = {k: v for k, v in base.items() if v}  # 0 points = leave it out
    where = []
    if live:
        tz["spec"] = base
        where.append(f"**{tz['name']}**")
    if save_as_default or not live:
        circuit(s)["payout"] = base
        where.append("future tournaments")
    save_data(data)
    await interaction.response.defer(ephemeral=True)
    table = "\n".join(f"**{place_label(lo, hi - lo + 1)}:** {base.get(str(lo), 0)}"
                      for _n, lo, hi in PLACEMENT_GROUPS if any(str(p) in base for p in range(lo, hi + 1))
                      or _n in given)
    await update_board(interaction.guild, data)
    if live and given:
        await post(chan(interaction.guild, "announcements"),
                   f"RISER POINTS for **{tz['name']}** by finishing position:\n{table}",
                   title="Points table updated", color=GOLD)
    note = "" if given else "\n*(Nothing changed: add the positions you want to set, e.g. place_1:150.)*"
    await interaction.followup.send(f"Points table for {' and '.join(where)}:\n{table}{note}", ephemeral=True)


# ---- commands

@app_commands.describe(points_needed="RISER POINTS needed (tournament winners qualify automatically)")
@app_commands.default_permissions(manage_roles=True)
async def setmajor(interaction: discord.Interaction, points_needed: app_commands.Range[int, 0, 100000]):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    circuit(s)["needed"] = points_needed
    save_data(data)
    await update_board(interaction.guild, data)
    ann = chan(interaction.guild, "announcements")
    if ann:
        await post(ann, f"**Major qualification:** teams need **{points_needed} RISER POINTS** to qualify. "
                       "Tournament winners qualify automatically.")
    await interaction.response.send_message(f"Teams now need {points_needed} RISER POINTS for the Major.",
                                            ephemeral=True)


@bot.tree.command(description="See the RISER POINTS standings.")
async def points(interaction: discord.Interaction):
    s = guild_signups(load_data(), interaction.guild.id)
    c = circuit(s)
    rows = sorted(s["teams"].items(), key=lambda kv: -kv[1].get("points", 0))
    head = "**RISER POINTS**" + (f" · {c['needed']} needed for the Major" if c["needed"] is not None else "")
    lines = [f"`{t.get('points', 0):>5}` **{t['name']}**{' · Major qualified' if major_qualified(s, k) else ''}"
             for k, t in rows] or ["No teams yet."]
    await interaction.response.send_message((head + "\n" + "\n".join(lines))[:1990], ephemeral=True)


@app_commands.describe(team="The team's role", points="Their new RISER POINTS total")
@app_commands.default_permissions(manage_roles=True)
async def setpoints(interaction: discord.Interaction, team: discord.Role, points: app_commands.Range[int, 0, 100000]):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    t = s["teams"].get(str(team.id))
    if not t:
        return await interaction.response.send_message("That isn't a league team.", ephemeral=True)
    t["points"] = points
    t["core"] = [int(u) for u in t["roster"]] if points else []
    save_data(data)
    await update_board(interaction.guild, data)
    await log_transaction(interaction.guild, f"Staff set **{t['name']}** to {points} RISER POINTS", t)
    await interaction.response.send_message(f"**{t['name']}** now has {points} RISER POINTS.", ephemeral=True)


@app_commands.describe(confirm="Set to True to confirm")
@app_commands.default_permissions(manage_roles=True)
async def resetpoints(interaction: discord.Interaction, confirm: bool = False):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    if not confirm:
        return await interaction.response.send_message("Run /setpoints reset_all:True confirm:True to reset everything.",
                                                       ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    for t in s["teams"].values():
        t["points"], t["core"] = 0, []
    circuit(s)["qualified"] = []
    save_data(data)
    await update_board(interaction.guild, data)
    await interaction.response.send_message("All RISER POINTS and Major spots reset.", ephemeral=True)


@bot.tree.command(description="Captains/co-captains: enter your team. Staff: enter any team with the team option.")
@app_commands.describe(team="Commissioner/admin only: the team to enter (captains leave this empty)",
                       ignore_roster="Staff only: enter the team even if its roster isn't full yet",
                       late="Staff only: enter the team even though entries are closed")
async def register(interaction: discord.Interaction, team: discord.Role | None = None, ignore_roster: bool = False,
                   late: bool = False):
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    staff = is_staff(interaction.user)
    if team is not None and not is_commissioner(interaction.user):
        return await interaction.response.send_message("Only the Commissioner or an admin can sign up a team for someone else. "
                                                       "Captains just type /register.", ephemeral=True)
    if (ignore_roster or late) and not staff:
        return await interaction.response.send_message("Only staff can use those options. Captains just type /register.",
                                                       ephemeral=True)
    if team is None and suspended_from(s, interaction.user.id, "league"):
        return await interaction.response.send_message(suspended_from(s, interaction.user.id, "league"), ephemeral=True)
    tz, open_, is_next = signup_target(s)  # while one is played, entries go to the next tournament
    key = str(team.id) if team is not None else signer_team(s, interaction.user.id)  # captain or co-captain
    who = "That team" if team is not None else "Your team"
    started = (not is_next) and bool(s.get("event")) and s["event"].get("stage") not in (None, "done", "playin",
                                                                                         "playin_done")
    problem = None
    if key is None or key not in s["teams"]:
        problem = ("Only team captains and co-captains can register. Start a team with /signup." if team is None
                   else f"{team.mention} isn't a league team.")
    elif not tz:
        problem = "No tournament is taking entries right now. Watch #announcements."
    elif started:
        problem = "That tournament has already started, so teams can't be added to the draw."
    elif not open_ and not late:
        problem = ("No tournament is taking entries right now. Watch #announcements." if team is None
                   else "Entries are closed. Add `late:True` to enter them anyway.")
    elif key in tz["entrants"]:
        problem = f"{who} is already registered."
    elif not is_complete(s["teams"][key]) and not ignore_roster:
        n = len(s["teams"][key]["roster"])
        problem = (f"Your roster needs at least {ROSTER_MIN} players (you have {n}). Send offers with /offer."
                   if team is None else f"That roster has {n}/{ROSTER_MIN} players. Add `ignore_roster:True` to enter "
                                        "them anyway.")
    elif tz["kind"] == "lcq" and team is None:
        problem = "The LCQ is invite-only: the invited teams are already entered. Ask staff if something's wrong."
    elif tz["kind"] == "lcq" and major_qualified(s, key):
        problem = f"{who} already qualified for the Major, so they can't play the LCQ."
    elif tz["kind"] == "major" and not major_qualified(s, key):
        problem = f"Only qualified teams can enter the Major. {who} has {points_line(s, key)}."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True, allowed_mentions=NO_PINGS)
    tz["entrants"].append(key)
    added = lcq_fill(s) if tz["kind"] == "lcq" else []  # staff added one: keep the LCQ even
    save_data(data)
    await interaction.response.defer(ephemeral=True)
    if added:
        await lcq_announce_next_up(interaction.guild, s, added)
    t = s["teams"][key]
    line = points_line(s, key)
    by = " (entered by staff)" if team is not None else ""
    await log_transaction(guild, f"**{t['name']}** registered for **{tz['name']}**{by} · {line}", t)
    await update_board(guild, data)
    if team is not None:  # let the captain (and co-captain) know staff entered them
        for uid in [t["captain"]] + ([t["co"]] if t.get("co") else []):
            try:
                mem = guild.get_member(uid) or await bot.fetch_user(uid)
                await mem.send(embed=brand_embed(f"League staff entered **{t['name']}** in **{tz['name']}** "
                                                 f"(team #{len(tz['entrants'])}). Good luck!", "You're registered", GOOD))
            except (discord.HTTPException, AttributeError):
                pass
    await interaction.followup.send(f"**{t['name']}** is registered for **{tz['name']}** "
                                    f"(team #{len(tz['entrants'])}).\n{line}", ephemeral=True)


@bot.tree.command(description="Captains/co-captains: take your team out. Staff: remove any team with the team option.")
@app_commands.describe(team="Staff only: the team to take out (captains leave this empty)")
async def unregister(interaction: discord.Interaction, team: discord.Role | None = None):
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    tz, open_, is_next = signup_target(s)
    if team is not None and not is_staff(interaction.user):
        return await interaction.response.send_message("Only staff can pick a team. Captains just type /unregister.",
                                                       ephemeral=True)
    key = str(team.id) if team is not None else signer_team(s, interaction.user.id)  # captain or co-captain
    started = (not is_next) and bool(s.get("event")) and s["event"].get("stage") not in (None, "done", "playin",
                                                                                         "playin_done")
    lcq = bool(tz) and tz.get("kind") == "lcq"
    if not tz or started or (not open_ and team is None and not lcq) or key not in (tz or {}).get("entrants", []):
        return await interaction.response.send_message(
            "That team isn't registered for a tournament that's taking entries." if team is not None else
            "You're not registered for an open tournament.", ephemeral=True)
    tz["entrants"].remove(key)
    added = lcq_fill(s) if lcq else []
    save_data(data)
    t = s["teams"].get(key, {})
    if team is not None:
        await log_transaction(interaction.guild, f"**{t.get('name', 'A team')}** was taken out of **{tz['name']}** by staff", t)
    if added:
        await lcq_announce_next_up(interaction.guild, s, added)
    await update_board(interaction.guild, data)
    await interaction.response.send_message(f"**{t.get('name', 'The team')}** has been taken out of the tournament.",
                                            ephemeral=True)


# ---- test tournament

def simulate(ids: list[int], fmt: str, rng: random.Random, box=None) -> dict:
    """Play a whole tournament with random results. Returns the finished event.
    box(m, winner, loser, winner_points, loser_points) is called after every game if given."""
    ev = new_event(fmt if fmt != "none" else "main")

    def play(m):
        w = rng.choice([m["a"], m["b"]])
        lo = m["b"] if w == m["a"] else m["a"]
        hi = rng.randint(38, 66)
        pts = [hi, hi - rng.randint(1, 15)]
        m["score"] = f"{pts[0]}-{pts[1]}"
        if box:
            box(m, w, lo, pts[0], pts[1])
        return w, lo, pts

    if fmt == "swiss":
        ev["swiss"] = sw = swiss_new(list(ids), 3, 3)
        swiss_next_round(ev)
        while True:
            for m in sw["matches"]:
                if not m["winner"]:
                    w, lo, _pts = play(m)
                    m["winner"] = w
                    swiss_record(sw, w, lo)
            if not swiss_active(sw):
                break
            swiss_next_round(ev)
        ev["stage"] = "swiss_done"
        seeds = list(sw["qualified"])
    elif fmt == "groups":
        ev["groups"] = gs = groups_new(ev, list(ids), 2)
        for m in gs["matches"]:
            w, _lo, pts = play(m)
            m["winner"], m["pts"] = w, pts
        for gi in range(len(gs["groups"])):
            order, _st = group_table(gs, gi)
            gs["qualified"] += order[:gs["advance"]]
        ev["stage"] = "groups_done"
        seeds = groups_seeds(gs)
    else:
        seeds = list(ids)
        rng.shuffle(seeds)
    if len(seeds) == 1:
        ev["main"] = {"matches": [], "champion": seeds[0]}
    else:
        ev["main"] = de_build(ev, seeds)
        de_resolve(ev["main"])
        while not ev["main"]["champion"]:
            m = de_ready(ev["main"])[0]
            w, lo, _pts = play(m)
            de_record(ev, m, w, lo)
    ev["stage"] = "done"
    return ev


async def run_live_test(guild: discord.Guild, ids: list[int], style: str, rng: random.Random, box, spec: dict,
                        reporter: int, scorecards: bool, fallback) -> tuple[dict, list]:
    """Play a fake tournament step by step and post everything in the real channels, like a real one.
    Every post is marked TEST. Returns the finished event and the posted message IDs (for /cleartest)."""
    posted = []
    tname = "TEST Open"
    fake_s = {"tourney": {"name": tname}}

    async def tp(chname, text, color=BRAND, title=None):
        msg = await post(chan(guild, chname) or fallback, text, title=title, color=color)
        if msg:
            posted.append([msg.channel.id, msg.id])

    async def tb(chname, parts, color=BRAND):
        for chunk in pack(parts, limit=3800):
            await tp(chname, chunk, color)

    live_pic = {}

    async def test_bracket_pic(ev, game=None):
        done = rounds_just_done(ev["main"])
        champ = ev["main"].get("champion")
        what = ", ".join(done)
        pic_s = {"teams": {str(t): {"name": n} for t, n in TEST_NAMES.items()}, "tourney": {"name": tname}}
        try:
            png = await asyncio.to_thread(bracket_picture, pic_s, ev,
                                          "Final bracket" if champ else
                                          f"Live · after M{game['id']} ({game['label']})" if game else "Live bracket",
                                          set(done), None if champ or not game else game["id"])
        except Exception as e:  # no Pillow, or the picture failed: the text updates still go out
            print(f"[test bracket picture] {e}")
            return
        live_pic["png"] = png  # the test website shows the last one
        ch = chan(guild, "bracket") or fallback
        if live_pic.get("msg"):  # one live picture at a time, like the real thing
            try:
                await live_pic["msg"].delete()
                posted[:] = [p_ for p_ in posted if p_[1] != live_pic["msg"].id]
            except Exception:
                pass
        g = ""
        if game and game.get("loser") is not None:
            g = (f"**{TEST_NAMES.get(game['winner'])}** beat **{TEST_NAMES.get(game['loser'])}**"
                 + (f" {game['score']}" if game.get("score") else "") + f" in M{game['id']}.")
        if done:
            g += f"\n**{what}** is complete."
        e = brand_embed(f"**{TEST_NAMES.get(champ, 'The champions')}** win {tname}!" if champ else
                        (g or "Here's the bracket.") + "\n*Updates after every reported game. Practice run: nothing here is real.*",
                        "TEST · " + ("🏆 FINAL BRACKET" if champ else "📊 LIVE BRACKET" + (f" · {what} complete" if done else "")),
                        GOLD)
        e.set_image(url="attachment://bracket.png")
        msg = await ch.send(embed=e, file=discord.File(io.BytesIO(png), filename="bracket.png"),
                            allowed_mentions=NO_PINGS)
        live_pic["msg"] = None if champ else msg
        posted.append([msg.channel.id, msg.id])

    async def card(ev, m):
        if not scorecards:
            return
        ch = chan(guild, "score-reports") or fallback
        e = score_card(fake_s, ev, m, reporter)
        e.title = "TEST · " + (e.title or "")
        e.url = f"{site_url()}test/#m{m['id']}" if site_url() else None
        msg = await ch.send(embed=e, allowed_mentions=NO_PINGS)
        posted.append([ch.id, msg.id])

    def play(m):
        w = rng.choice([m["a"], m["b"]])
        lo = m["b"] if w == m["a"] else m["a"]
        hi = rng.randint(38, 66)
        pts = [hi, hi - rng.randint(1, 15)]
        m["score"] = f"{pts[0]}-{pts[1]}"
        box(m, w, lo, pts[0], pts[1])
        return w, lo, pts

    def line(m, extra=""):
        return f"**M{m['id']} result**: {tag(m['winner'])} beat {tag(m['b'] if m['winner'] == m['a'] else m['a'])} {m['score']}{extra}"

    # 1. entries open, registrations, entries close
    await tp("announcements", f"# TEST · {tname} is open for entries!\n**RISER POINTS:** {spec_text(spec)}\n"
                              "The winner qualifies for the Major automatically.\n*This is a practice run with fake "
                              "teams. Nothing here is real.*")
    for tid in ids:
        await tp("transactions", f"**{TEST_NAMES[tid]}** registered for **{tname}** · **0 RISER POINTS**",
                 INFO, "TEST · Transaction")
    await tp("announcements", f"# TEST · Entries for {tname} are closed: {len(ids)} teams.\n"
             + ", ".join(f"**{TEST_NAMES[t]}**" for t in ids))

    ev = new_event(style if style != "none" else "main")

    # 2. qualifier
    if style == "swiss":
        ev["swiss"] = sw = swiss_new(list(ids), 3, 3)
        await tb("schedule", [f"# TEST · Swiss qualifier\n{len(ids)} teams. **3 wins** = into the main draw. "
                              "**3 losses** = out.", "\n".join(swiss_next_round(ev))])
        await tb("standings", ["# TEST · " + swiss_table(sw)[0].lstrip("# ")] + swiss_table(sw)[1:])
        await tp("announcements", "# TEST · The Swiss qualifier has started!\nRound 1 matchups are in #schedule.")
        while True:
            for m in [x for x in sw["matches"] if not x["winner"]]:
                w, lo, _pts = play(m)
                m["winner"] = w
                swiss_record(sw, w, lo)
                await card(ev, m)
                parts = [line(m)]
                if all(x["winner"] for x in sw["matches"] if x["round"] == sw["round"]):
                    t = swiss_table(sw)
                    await tb("standings", ["# TEST · " + t[0].lstrip("# ")] + t[1:])
                    if swiss_active(sw):
                        parts.append("\n".join(swiss_next_round(ev)))
                    else:
                        parts.append(f"# Swiss stage complete\n**Into the main draw ({len(sw['qualified'])}):** "
                                     + ", ".join(tag(q) for q in sw["qualified"]))
                await tb("schedule", parts, GOOD)
            if not swiss_active(sw):
                break
        seeds = list(sw["qualified"])
        note = f"{len(seeds)} teams qualified from the Swiss stage, seeded by record."
    elif style == "groups":
        ev["groups"] = gs = groups_new(ev, list(ids), 2)
        await tb("standings", [f"# TEST · Group stage draw\n{len(ids)} teams in {len(gs['groups'])} group(s). "
                               "Top 2 in each group go to the main draw."]
                 + [group_blocks(gs, gi) for gi in range(len(gs["groups"]))])
        rounds = max(m["round"] for m in gs["matches"])
        sched = [f"# TEST · Group stage schedule\n{rounds} rounds."]
        for r in range(1, rounds + 1):
            sched.append(f"## Round {r}\n" + "\n".join(
                f"**M{m['id']}** Group {group_letter(m['group'])}: {tag(m['a'])} vs {tag(m['b'])}"
                for m in gs["matches"] if m["round"] == r))
        await tb("schedule", sched)
        await tp("announcements", "# TEST · The group stage draw is out!\nGroups are in #standings, matchups in "
                                  "#schedule.")
        for m in gs["matches"]:
            w, _lo, pts = play(m)
            m["winner"], m["pts"] = w, pts
            await card(ev, m)
            await tb("schedule", [line(m, f" (Group {group_letter(m['group'])})")], GOOD)
            await tb("standings", [group_blocks(gs, m["group"])])
        for gi in range(len(gs["groups"])):
            order, _st = group_table(gs, gi)
            gs["qualified"] += order[:gs["advance"]]
        await tb("standings", ["# TEST · Final group standings"] + [group_blocks(gs, gi) for gi in range(len(gs["groups"]))])
        seeds = groups_seeds(gs)
        note = f"{len(seeds)} teams qualified from the group stage."
    else:
        seeds = list(ids)
        rng.shuffle(seeds)
        note = f"{len(seeds)} teams, no qualifier, seeded at random."

    # 3. main draw
    if len(seeds) == 1:
        ev["main"] = {"matches": [], "champion": seeds[0]}
    else:
        ev["main"] = main = de_build(ev, seeds)
        ev["stage"] = "main"
        de_resolve(main)
        parts = [f"# TEST · Main draw: double elimination\n{note}\nLose twice and you're out.",
                 "**Seeds**\n" + "\n".join(f"#{i}: {tag(t)}" for i, t in enumerate(seeds, 1))]
        parts += de_overview(main)
        nxt = up_next(main)
        if nxt:
            parts.append("# Play now\n" + "\n".join(nxt))
        await tb("bracket", parts)
        await tp("announcements", "# TEST · The main draw has started!\nCheck #bracket.")
        while not main["champion"]:
            m = de_ready(main)[0]
            w, lo, _pts = play(m)
            parts = [line(m, f" ({m['label']})")]
            if de_record(ev, m, w, lo):
                parts.append("The Losers bracket team won, so the Grand Final resets: one more game decides it!")
            await card(ev, m)
            if main["champion"]:
                parts.append(f"# {tag(main['champion'])} win {tname}!")
            else:
                nxt = up_next(main)
                if nxt:
                    parts.append("**Up next**\n" + "\n".join(nxt))
            await tb("bracket", parts, GOOD)
            await test_bracket_pic(ev, m)  # every game: the TEST live bracket picture, like a real tournament
    ev["stage"] = "done"

    # 4. champion + final standings (points are only previewed)
    champ = ev["main"]["champion"]
    standing = [f"# TEST · {tname}: final standings and RISER POINTS\n*Preview only: no real points were given.*"]
    for place, tids in final_standings(ev):
        standing.append(f"{place_label(place, len(tids))}: " + ", ".join(tag(t) for t in tids)
                        + f"  +{spec.get(str(place), 0)}")
    standing.append(f"{tag(champ)} won the tournament and would **qualify for the Major**.")
    await tb("standings", ["\n".join(standing[i:i + 30]) for i in range(0, len(standing), 30)], GOLD)
    await tp("announcements", f"**{TEST_NAMES[champ]}** are the champions of **{tname}**! Final standings and "
                              "RISER POINTS are in #standings.\n*Practice run: no real results.*", GOLD,
             f"TEST · {tname} champions")
    return ev, posted


@bot.tree.command(description="Staff: run a whole practice tournament with fake teams, posted in every channel.")
@app_commands.describe(teams="How many fake teams (2 to 68)", style="Qualifier to test",
                       publish="Also publish it to the website's /test/ page",
                       channels="Post it in all the tournament channels like a real one (default yes)",
                       scorecards="Post a Final Score card for every game in #score-reports (default yes)",
                       place_1="Test points for 1st", place_2="Test points for 2nd", place_3="Test points for 3rd",
                       place_4="Test points for 4th", place_5_6="Test points for 5th-6th",
                       place_7_8="Test points for 7th-8th", place_9_12="Test points for 9th-12th",
                       place_13_16="Test points for 13th-16th", place_17_24="Test points for 17th-24th",
                       place_25_32="Test points for 25th-32nd", place_33_48="Test points for 33rd-48th",
                       place_49_64="Test points for 49th-64th")
@app_commands.choices(style=[
    app_commands.Choice(name="Group stage then double elimination", value="groups"),
    app_commands.Choice(name="Swiss then double elimination", value="swiss"),
    app_commands.Choice(name="Double elimination only", value="none"),
])
@app_commands.default_permissions(manage_roles=True)
async def testtournament(interaction: discord.Interaction, teams: app_commands.Range[int, 2, 68] = 16,
                         style: str = "groups", publish: bool = False, channels: bool = True,
                         scorecards: bool = True,
                         place_1: app_commands.Range[int, 0, 100000] | None = None,
                         place_2: app_commands.Range[int, 0, 100000] | None = None,
                         place_3: app_commands.Range[int, 0, 100000] | None = None,
                         place_4: app_commands.Range[int, 0, 100000] | None = None,
                         place_5_6: app_commands.Range[int, 0, 100000] | None = None,
                         place_7_8: app_commands.Range[int, 0, 100000] | None = None,
                         place_9_12: app_commands.Range[int, 0, 100000] | None = None,
                         place_13_16: app_commands.Range[int, 0, 100000] | None = None,
                         place_17_24: app_commands.Range[int, 0, 100000] | None = None,
                         place_25_32: app_commands.Range[int, 0, 100000] | None = None,
                         place_33_48: app_commands.Range[int, 0, 100000] | None = None,
                         place_49_64: app_commands.Range[int, 0, 100000] | None = None):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can run tests.", ephemeral=True)
    # test-only points, set the same way as /payout (only for this test, nothing is saved)
    given = {name: v for name, v in locals().items() if name.startswith("place_") and v is not None}
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    rng = random.Random()
    ids = [9_000_000_000_000_000 + i for i in range(1, teams + 1)]
    names, rosters = fake_league(teams, rng)
    TEST_NAMES.clear()
    TEST_NAMES.update(dict(zip(ids, names)))

    def box(m, w, lo, wp, lp):
        m["box"] = {**fake_box(w, rosters[TEST_NAMES[w]], wp, wp - lp, rng),
                    **fake_box(lo, rosters[TEST_NAMES[lo]], lp, lp - wp, rng)}

    s = guild_signups(load_data(), guild.id)
    tz = s.get("tourney") or {}
    spec = dict(tz.get("spec") or default_payout(s))
    for name, lo, hi in PLACEMENT_GROUPS:
        if name in given:
            for place in range(lo, hi + 1):
                spec[str(place)] = given[name]
    spec = {k: v for k, v in spec.items() if v}
    staff = chan(guild, "staff-chat") or interaction.channel

    posted = []
    if channels:
        await interaction.followup.send("Test tournament running. Watch #announcements, #transactions, "
                                        "#schedule, #standings, #bracket and #score-reports. Big tests take a few "
                                        "minutes because Discord limits how fast bots can post.", ephemeral=True)
        try:
            ev, posted = await run_live_test(guild, ids, style, rng, box, spec, interaction.user.id, scorecards,
                                             staff)
        finally:
            data = load_data()  # remember every test post so /cleartest can delete them
            guild_signups(data, guild.id).setdefault("test_msgs", []).extend(posted)
            save_data(data)
    else:
        ev = simulate(ids, style, rng, box)

    # summary for staff
    totals = player_totals(ev, str, lambda tid: TEST_NAMES.get(tid, "?"))
    top = sorted(totals.values(), key=lambda r: -r["pts"] / max(1, r["gp"]))[:5]
    parts = [f"# TEST TOURNAMENT finished ({teams} teams, {style})\nNothing real was changed. "
             f"Champion: {tag(ev['main']['champion'])}. Main draw: {len(ev['main']['matches'])} matches.",
             "**Top scorers (points per game)**\n" + "\n".join(
                 f"{i}. {r['player']} ({r['team']}): {r['pts'] / r['gp']:.1f} PPG over {r['gp']} games"
                 for i, r in enumerate(top, 1)),
             f"Clean up the {len(posted)} test posts with `/cleartest`." if posted else ""]
    if not channels:
        standing = ["**Final standings and RISER POINTS they would earn**"]
        for place, tids in final_standings(ev):
            standing.append(f"{place_label(place, len(tids))}: " + ", ".join(tag(t) for t in tids)
                            + f"  +{spec.get(str(place), 0)}")
        parts += ["\n".join(standing[i:i + 25]) for i in range(0, len(standing), 25)]
    await send_blocks(staff, [p for p in parts if p])

    note = ""
    if publish:
        note = "\n" + await publish_test_site(guild, ev, spec, rosters, rng)
    TEST_NAMES.clear()
    await interaction.followup.send(f"Test tournament finished: champion **{names[ids.index(ev['main']['champion'])]}**."
                                    f"{' Remove the test posts any time with /cleartest.' if posted else ''}{note}",
                                    ephemeral=True)


@app_commands.default_permissions(manage_roles=True)
async def cleartest(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    by_channel = {}
    for ch_id, msg_id in s.get("test_msgs", []):
        by_channel.setdefault(ch_id, []).append(msg_id)
    gone = 0
    for ch_id, ids in by_channel.items():
        ch = guild.get_channel(ch_id)
        if ch is None:
            continue
        for i in range(0, len(ids), 100):
            chunk = [discord.Object(id=x) for x in ids[i:i + 100]]
            try:
                if len(chunk) > 1:
                    await ch.delete_messages(chunk)  # bulk delete (messages under 14 days old)
                else:
                    await ch.get_partial_message(chunk[0].id).delete()
                gone += len(chunk)
            except discord.HTTPException:
                for o in chunk:  # older messages have to go one at a time
                    try:
                        await ch.get_partial_message(o.id).delete()
                        gone += 1
                    except discord.HTTPException:
                        pass
    s["test_msgs"] = []
    save_data(data)
    await interaction.followup.send(f"Deleted {gone} test message(s).", ephemeral=True)


# ---------------------------------------------------------------- player stats
#
# A match can carry a box score: m["box"] = {player key: {"team": team id, "pts", "reb", "ast", "stl", "blk"}}
# (player key = Discord ID for real games, a made-up name in test tournaments).
# When a new tournament opens, the finished one's player totals are saved in s["history"] for the year table.

STAT_KEYS = ["pts", "fg2m", "fg2a", "fg3m", "fg3a", "ftm", "fta", "orb", "drb", "reb", "ast", "stl", "blk",
             "to", "pf", "pm", "min", "pt"]
STAT_LABELS = {"pts": "PTS", "fg2m": "2FGM", "fg2a": "2FGA", "fg3m": "3FGM", "fg3a": "3FGA", "ftm": "FTM",
               "fta": "FTA", "orb": "ORB", "drb": "DRB", "reb": "REB", "ast": "AST", "stl": "STL", "blk": "BLK",
               "to": "TO", "pf": "FOUL", "pm": "+/-", "min": "MIN", "pt": "PT"}


# ---- Consolation bracket (optional: /startgroups or /startswiss with consolation:True)
#
# Teams knocked out in the qualifier play a single-elimination bracket while the main draw runs. Seeded by
# qualifier record (wins, then point difference); top seeds get byes when the count isn't a power of 2.
# Bonus RISER POINTS: once both the main draw and the consolation bracket are finished, the consolation winner
# gets enough to finish CONS_GAP points BEHIND the last-place team in the main draw (so a main-draw finish is
# always worth more), and the runner-up gets half the winner's bonus. No bonus in a Major or LCQ.

CONS_GAP = 15
CONS_NOTE = (f"The winner gets bonus RISER POINTS that put them **{CONS_GAP} points behind last place in the main "
             "draw**; the runner-up gets half that bonus.")


def cons_bonus(s: dict, ev: dict) -> tuple[int, int, int, dict] | None:
    """(winner bonus, runner-up bonus, main-draw floor, {team: points}) or None until the main draw and the
    consolation are both finished. The consolation winner ends on max(main-draw last place - CONS_GAP, what
    they already had); any main-draw team below that + CONS_GAP is topped up so a main-draw finish always wins."""
    cons, main = ev.get("consolation") or {}, ev.get("main") or {}
    if not cons.get("champion") or not main.get("champion"):
        return None
    tz = s.get("tourney") or {}
    spec = tz.get("spec") or default_payout(s)
    in_main = {x for m in main.get("matches", []) for x in (m.get("a"), m.get("b")) if x is not None}
    place_of = {t: p for p, ts_ in final_standings(ev) for t in ts_}
    got = {t: spec.get(str(place_of.get(t, 0)), 0) for t in place_of}
    main_last = min((got.get(t, 0) for t in in_main), default=0)
    w_had, r_had = got.get(cons["champion"], 0), got.get(cons["runner_up"], 0)
    w_total = max(main_last - CONS_GAP, w_had)
    win = w_total - w_had
    runner = max(0, min(win // 2, w_total - 1 - r_had))
    return win, runner, w_total + CONS_GAP, {t: got.get(t, 0) for t in in_main}


async def give_cons_bonus(guild: discord.Guild, s: dict, ev: dict) -> list[str]:
    """Pay the consolation bonus once both brackets are done. Returns lines to post (empty if not yet)."""
    cons = ev.get("consolation")
    if not cons or cons.get("bonus_paid") or (s.get("tourney") or {}).get("kind") in ("major", "lcq"):
        return []
    b = cons_bonus(s, ev)
    if b is None:
        return []
    win, runner, floor, main_pts = b
    cons["bonus_paid"] = [win, runner]
    lines = ["# Consolation bonus"]
    for tid, bonus, what in ((cons["champion"], win, "won the consolation bracket"),
                             (cons["runner_up"], runner, "were consolation runner-up")):
        t_ = s["teams"].get(str(tid))
        if t_ is not None and bonus:
            t_["points"] = t_.get("points", 0) + bonus
        lines.append(f"{tag(tid)} {what}: **+{bonus} RISER POINTS**")
    topped = []
    for tid, had in main_pts.items():  # a main-draw finish is always worth more than winning the consolation
        if had < floor:
            t_ = s["teams"].get(str(tid))
            if t_ is not None:
                t_["points"] = t_.get("points", 0) + (floor - had)
            topped.append(tid)
    if topped:
        lines.append(f"Main-draw teams raised to **{floor} RISER POINTS** for this tournament so they stay ahead of "
                     "the consolation winner: " + ", ".join(tag(t) for t in topped))
    lines.append(f"*(Last place in the main draw always finishes at least {CONS_GAP} points ahead of the "
                 "consolation winner.)*")
    return lines


def bracket_order(size: int) -> list[int]:
    """Seed positions for a bracket of `size`: 1 v 8, 4 v 5, 2 v 7, 3 v 6 for 8 teams."""
    order = [1, 2]
    while len(order) < size:
        n = len(order) * 2 + 1
        order = [x for s_ in order for x in (s_, n - s_)]
    return order


def cons_round_name(r: int, rounds: int) -> str:
    left = rounds - r
    return "Consolation " + ("Final" if left == 0 else "Semifinal" if left == 1 else "Quarterfinal" if left == 2
                             else f"Round {r}")


def cons_build(ev: dict, teams: list[int]) -> dict:
    """Single elimination for `teams` (best seed first)."""
    size = 1
    while size < len(teams):
        size *= 2
    rounds = max(1, size.bit_length() - 1)
    slots = [teams[s_ - 1] if s_ <= len(teams) else None for s_ in bracket_order(size)]
    by_round = []
    for r in range(1, rounds + 1):
        lst = []
        for i in range(size >> r):
            mid = ev["next_id"]
            ev["next_id"] += 1
            lst.append({"id": mid, "round": r, "label": cons_round_name(r, rounds), "a": None, "b": None,
                        "winner": None, "score": None, "pts": None, "bye": False, "next": None})
        by_round.append(lst)
    for r, lst in enumerate(by_round[:-1]):
        for i, m in enumerate(lst):
            m["next"] = [by_round[r + 1][i // 2]["id"], "a" if i % 2 == 0 else "b"]
    for i, m in enumerate(by_round[0]):
        m["a"], m["b"] = slots[2 * i], slots[2 * i + 1]
    cons = {"matches": [m for lst in by_round for m in lst], "champion": None, "runner_up": None,
            "seeds": list(teams)}
    for m in by_round[0]:  # byes: the team goes straight through
        if (m["a"] is None) != (m["b"] is None):
            m["bye"] = True
            cons_advance(cons, m, m["a"] if m["a"] is not None else m["b"])
    return cons


def cons_advance(cons: dict, m: dict, winner: int):
    m["winner"] = winner
    if m["next"]:
        nid, side = m["next"]
        nxt = next(x for x in cons["matches"] if x["id"] == nid)
        nxt[side] = winner
        if nxt.get("forfeit") and not nxt["winner"]:  # their opponent was disqualified: straight through
            cons_advance(cons, nxt, winner)


def cons_record(cons: dict, m: dict, winner: int, loser: int) -> bool:
    """Record a result. True when this was the final."""
    cons_advance(cons, m, winner)
    if not m["next"]:
        cons["champion"], cons["runner_up"] = winner, loser
        return True
    return False


def cons_ready(cons: dict | None) -> list[dict]:
    if not cons:
        return []
    return [m for m in cons["matches"] if not m["winner"] and not m["bye"] and m["a"] is not None
            and m["b"] is not None]


def cons_running(ev: dict | None) -> bool:
    return bool(ev and ev.get("consolation") and not ev["consolation"].get("champion"))


def qualifier_knockouts(ev: dict) -> list[int]:
    """Teams out in the qualifier, best record first (wins, then fewer losses, then point difference)."""
    pd = tournament_pd(ev)
    rec = {}
    if ev.get("swiss"):
        sw = ev["swiss"]
        rec = {int(t): (r["w"], r["l"]) for t, r in sw["rec"].items() if int(t) not in sw["qualified"]}
    elif ev.get("groups"):
        gs = ev["groups"]
        for gi in range(len(gs["groups"])):
            _order, st = group_table(gs, gi)
            rec.update({t: (r["w"], r["l"]) for t, r in st.items() if t not in gs["qualified"]})
    return sorted(rec, key=lambda t: (-rec[t][0], rec[t][1], -pd.get(t, 0)))


def cons_parts(cons: dict, tagf=None) -> list[str]:
    tagf = tagf or tag
    seeds = "\n".join(f"#{i}: {tagf(t)}" for i, t in enumerate(cons["seeds"], 1))
    first = [f"**M{m['id']}** {m['label']}: {tagf(m['a'])} vs {tagf(m['b'])}" for m in cons_ready(cons)]
    byes = [f"{tagf(m['winner'])} gets a bye" for m in cons["matches"] if m["bye"]]
    return [f"# Consolation bracket\nFor teams knocked out in the qualifier. **Single elimination**: lose once and "
            f"you're out. {CONS_NOTE}",
            f"**Seeds** (by qualifier record)\n{seeds}",
            "# Play now\n" + "\n".join(first + byes)]


async def maybe_start_consolation(guild: discord.Guild, s: dict, ev: dict):
    """The qualifier just finished: start the consolation bracket if staff turned it on."""
    if not ev.get("cons_on") or ev.get("consolation"):
        return
    out = qualifier_knockouts(ev)
    if len(out) < 2:
        return
    ev["consolation"] = cons_build(ev, out)
    await send_blocks(chan(guild, "bracket"), cons_parts(ev["consolation"]))
    ann = chan(guild, "announcements")
    if ann:
        await post(ann, f"**The consolation bracket is set!** {len(out)} teams knocked out in the qualifier play "
                        "single elimination for bonus RISER POINTS. Check #bracket.",
                   title="Consolation bracket", color=GOLD)


def all_matches(ev: dict | None) -> list[dict]:
    if not ev:
        return []
    out = []
    for part in ("swiss", "groups", "main"):
        out += (ev.get(part) or {}).get("matches", [])
    out += [m for m in (ev.get("consolation") or {}).get("matches", []) if not m.get("bye")]
    out += (ev.get("playin") or {}).get("matches", [])
    return out


def player_totals(ev: dict | None, pname, tname, pavatar=None) -> dict:
    """{player key: {player, team, avatar, gp, and every stat summed}} for one tournament."""
    tot = {}
    for m in all_matches(ev):
        for key, line in (m.get("box") or {}).items():
            row = tot.setdefault(str(key), {"player": pname(key), "team": tname(line["team"]),
                                            "avatar": pavatar(key) if pavatar else None, "gp": 0,
                                            **{k: 0 for k in STAT_KEYS}})
            row["team"] = tname(line["team"])
            row["gp"] += 1
            for k in STAT_KEYS:
                row[k] += line.get(k, 0) or 0
    return tot


def merge_totals(*tables: dict) -> dict:
    out = {}
    for table in tables:
        for key, r in table.items():
            row = out.setdefault(key, {"player": r["player"], "team": r["team"], "avatar": r.get("avatar"),
                                       "gp": 0, **{k: 0 for k in STAT_KEYS}})
            row["player"], row["team"] = r["player"], r["team"]
            row["avatar"] = r.get("avatar") or row.get("avatar")
            row["gp"] += r["gp"]
            for k in STAT_KEYS:
                row[k] += r.get(k, 0) or 0
    return out


def box_rows(m: dict, pname, tname, pavatar=None) -> list[dict]:
    return [{"player": pname(k), "team": tname(v["team"]), "avatar": pavatar(k) if pavatar else None,
             **{s: v.get(s, 0) or 0 for s in STAT_KEYS}}
            for k, v in (m.get("box") or {}).items()]


def final_rows(ev: dict | None, tz: dict, tname) -> list[dict]:
    """Final standings for the website: placement, teams, RISER POINTS each earned."""
    if not ev or not (ev.get("main") or {}).get("champion"):
        return []
    spec = tz.get("spec") or {}
    major = tz.get("kind") in ("major", "lcq")
    return [{"place": place_label(place, len(tids)), "teams": [tname(t) for t in tids],
             "points": 0 if major else spec.get(str(place), 0)} for place, tids in final_standings(ev)]


def archive_event(guild: discord.Guild, s: dict):
    """Save the last tournament (bracket, results, box scores, standings, player totals) before a new one
    replaces it, so the website can still show it and the year's stats keep adding up."""
    ev = s.get("event")
    if not ev or not (ev.get("main") or ev.get("swiss") or ev.get("groups")):
        return
    tz = s.get("tourney") or {}

    def pname(k):
        mem = guild.get_member(int(k)) if str(k).isdigit() else None
        return mem.display_name if mem else str(k)

    def tname(tid):
        if tid is None:
            return "BYE"
        t = s["teams"].get(str(tid))
        return t["name"] if t else "Former team"

    def avatar(k):
        mem = guild.get_member(int(k)) if str(k).isdigit() else None
        return mem.display_avatar.url if mem else None

    hist = s.setdefault("history", [])
    year = datetime.now().year
    slug = re.sub(r"[^a-z0-9]+", "-", tz.get("name", "tournament").lower()).strip("-")[:40] or "tournament"
    site = event_site_data(ev, tname, pname, avatar)
    site["final"] = final_rows(ev, tz, tname)
    site["stats"] = list(player_totals(ev, pname, tname, avatar).values())
    site["logos"] = {t["name"]: f"logos/{t['logo']}" for t in s["teams"].values() if t.get("logo")}
    champ = (ev.get("main") or {}).get("champion")
    hist.append({"id": f"{year}-{len(hist) + 1}-{slug}", "name": tz.get("name", "Tournament"),
                 "kind": tz.get("kind", "event"), "year": year,
                 "date": datetime.now(timezone.utc).date().isoformat(),
                 "champion": tname(champ) if champ else None, "teams": len(tz.get("entrants", [])),
                 "points": spec_text(tz["spec"]) if tz.get("spec") else None,
                 "logo": f"logos/{tz['logo']}" if tz.get("logo") else None,
                 "players": player_totals(ev, pname, tname), "site": site})


def made_att(text: str | None) -> tuple[int, int] | None:
    """'11/15' -> (11, 15). Empty -> (0, 0). Bad input -> None."""
    if not text or not text.strip():
        return 0, 0
    m = re.fullmatch(r"\s*(\d+)\s*[/-]\s*(\d+)\s*", text)
    if not m or int(m.group(1)) > int(m.group(2)):
        return None
    return int(m.group(1)), int(m.group(2))


@bot.tree.command(description="Referees/staff: enter one player's box score for a match.")
@app_commands.describe(match="Match number, e.g. 7 for M7", player="The player",
                       fg2="2-point shots made/attempted, e.g. 11/15", fg3="3-pointers made/attempted, e.g. 9/16",
                       ft="Free throws made/attempted, e.g. 1/1", orb="Offensive rebounds", drb="Defensive rebounds",
                       ast="Assists", stl="Steals", blk="Blocks", turnovers="Turnovers", fouls="Fouls",
                       plusminus="Plus/minus, e.g. -12", minutes="Minutes played", pt="PT from the game's stat screen",
                       points="Only if you don't have shooting splits: total points")
async def stat(interaction: discord.Interaction, match: int, player: discord.Member,
               fg2: str | None = None, fg3: str | None = None, ft: str | None = None,
               orb: app_commands.Range[int, 0, 200] = 0, drb: app_commands.Range[int, 0, 200] = 0,
               ast: app_commands.Range[int, 0, 200] = 0, stl: app_commands.Range[int, 0, 200] = 0,
               blk: app_commands.Range[int, 0, 200] = 0, turnovers: app_commands.Range[int, 0, 200] = 0,
               fouls: app_commands.Range[int, 0, 50] = 0, plusminus: app_commands.Range[int, -500, 500] = 0,
               minutes: app_commands.Range[int, 0, 200] = 0, pt: app_commands.Range[int, -1000, 1000] = 0,
               points: app_commands.Range[int, 0, 500] | None = None):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only Referees and league staff can enter stats.",
                                                       ephemeral=True)
    shots = {"2FG": made_att(fg2), "3FG": made_att(fg3), "FT": made_att(ft)}
    bad = [k for k, v in shots.items() if v is None]
    if bad:
        return await interaction.response.send_message(
            f"Couldn't read {', '.join(bad)}. Use made/attempted, like 11/15 (made can't be more than attempted).",
            ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    m = next((x for x in all_matches(s["event"]) if x["id"] == match), None)
    if m is None or m.get("a") is None or m.get("b") is None:
        return await interaction.response.send_message(f"There's no playable match M{match}.", ephemeral=True)
    team = next((tid for tid in (m["a"], m["b"]) if str(player.id) in s["teams"].get(str(tid), {}).get("roster", {})),
                None)
    if team is None:
        return await interaction.response.send_message(f"{player.mention} isn't on either team in M{match}.",
                                                       ephemeral=True, allowed_mentions=NO_PINGS)
    (f2m, f2a), (f3m, f3a), (ftm, fta) = shots["2FG"], shots["3FG"], shots["FT"]
    pts = 2 * f2m + 3 * f3m + ftm
    if points is not None and not (f2a or f3a or fta):
        pts = points  # no shooting splits given, so use the total they typed
    line = {"team": team, "pts": pts, "fg2m": f2m, "fg2a": f2a, "fg3m": f3m, "fg3a": f3a, "ftm": ftm, "fta": fta,
            "orb": orb, "drb": drb, "reb": orb + drb, "ast": ast, "stl": stl, "blk": blk, "to": turnovers,
            "pf": fouls, "pm": plusminus, "min": minutes, "pt": pt}
    m.setdefault("box", {})[str(player.id)] = line
    save_data(data)
    schedule_publish(interaction.guild)
    await interaction.response.send_message(
        f"M{match}: {player.mention} · {pts} PTS · 2FG {f2m}/{f2a} · 3FG {f3m}/{f3a} · FT {ftm}/{fta} · "
        f"{orb + drb} REB ({orb} OFF / {drb} DEF) · {ast} AST · {stl} STL · {blk} BLK · {turnovers} TO · "
        f"{fouls} FOUL · {plusminus:+d} · {minutes} MIN · PT {pt}\nRun it again for the same player to correct it.",
        ephemeral=True, allowed_mentions=NO_PINGS)
    if m.get("winner"):
        await refresh_score_card(interaction.guild, s, s["event"], m)  # add Players of the Game to the card


@bot.tree.command(description="Download player stats as a spreadsheet file (CSV).")
@app_commands.describe(scope="This tournament, or every tournament this year")
@app_commands.choices(scope=[app_commands.Choice(name="This tournament", value="tournament"),
                             app_commands.Choice(name="All year", value="year")])
async def exportstats(interaction: discord.Interaction, scope: str = "tournament"):
    guild = interaction.guild
    s = guild_signups(load_data(), guild.id)

    def pname(k):
        mem = guild.get_member(int(k)) if str(k).isdigit() else None
        return mem.display_name if mem else str(k)

    def tname(tid):
        t = s["teams"].get(str(tid))
        return t["name"] if t else "Former team"

    current = player_totals(s["event"], pname, tname)
    if scope == "year":
        year = datetime.now().year
        rows = merge_totals(*[h["players"] for h in s.get("history", []) if h.get("year") == year], current)
        label = f"all-year-{year}"
    else:
        rows = current
        label = re.sub(r"[^A-Za-z0-9]+", "-", (s.get("tourney") or {}).get("name", "tournament")).strip("-").lower()
    if not rows:
        return await interaction.response.send_message("No stats have been entered yet.", ephemeral=True)
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["Player", "Team", "GP"] + [STAT_LABELS[k] for k in STAT_KEYS]
               + ["PPG", "RPG", "APG", "2FG%", "3FG%", "FT%"])
    pct = lambda a, b: f"{100 * a / b:.1f}" if b else ""
    for r in sorted(rows.values(), key=lambda r: -r["pts"]):
        gp = max(1, r["gp"])
        w.writerow([r["player"], r["team"], r["gp"]] + [r.get(k, 0) for k in STAT_KEYS]
                   + [f"{r['pts'] / gp:.1f}", f"{r['reb'] / gp:.1f}", f"{r['ast'] / gp:.1f}",
                      pct(r["fg2m"], r["fg2a"]), pct(r["fg3m"], r["fg3a"]), pct(r["ftm"], r["fta"])])
    f = discord.File(io.BytesIO(out.getvalue().encode("utf-8-sig")), filename=f"pb-circuit-stats-{label}.csv")
    await interaction.response.send_message(f"Stats for {len(rows)} players. Opens in Excel or Google Sheets.",
                                            file=f, ephemeral=True)


STAT_HEADER = ["Discord ID", "Player", "Team", "2FG", "3FG", "FT", "ORB", "DRB", "REB", "AST", "STL", "BLK",
               "TO", "FOUL", "+/-", "MIN", "PT", "PTS"]


def sheet_key(h: str) -> str:
    """Turn a column heading into a field name, accepting common spellings."""
    raw = h.strip().lower()
    if raw in ("+/-", "+-", "plus/minus", "plusminus", "pm"):
        return "pm"
    k = re.sub(r"[^a-z0-9]", "", raw)
    return {"discordid": "id", "id": "id", "userid": "id", "player": "player", "name": "player",
            "team": "team", "2fg": "fg2", "fg2": "fg2", "2pt": "fg2", "2p": "fg2", "3fg": "fg3", "fg3": "fg3",
            "3pt": "fg3", "3p": "fg3", "ft": "ft", "freethrows": "ft", "orb": "orb", "oreb": "orb", "drb": "drb",
            "dreb": "drb", "reb": "reb", "rebounds": "reb", "ast": "ast", "assists": "ast", "stl": "stl",
            "steals": "stl", "blk": "blk", "blocks": "blk", "to": "to", "tov": "to", "turnovers": "to",
            "foul": "pf", "fouls": "pf", "pf": "pf", "min": "min", "mins": "min", "minutes": "min", "pt": "pt",
            "pts": "pts", "points": "pts"}.get(k, "")


def cell_int(v: str | None) -> int:
    v = (v or "").strip().replace("—", "").replace("–", "-").replace("−", "-").replace(" ", "")
    if v in ("", "-", "--"):
        return 0
    try:
        return int(float(v))
    except ValueError:
        raise ValueError(v)


@app_commands.describe(match="Match number, e.g. 7 for M7")
async def statstemplate(interaction: discord.Interaction, match: int):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only Referees and league staff can do that.", ephemeral=True)
    guild = interaction.guild
    s = guild_signups(load_data(), guild.id)
    m = next((x for x in all_matches(s["event"]) if x["id"] == match), None)
    if m is None or m.get("a") is None or m.get("b") is None:
        return await interaction.response.send_message(f"There's no playable match M{match}.", ephemeral=True)
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(STAT_HEADER)
    for tid in (m["a"], m["b"]):
        t = s["teams"].get(str(tid), {})
        for uid in t.get("roster", {}):
            mem = guild.get_member(int(uid))
            old = (m.get("box") or {}).get(uid)
            fill = ([f"{old['fg2m']}/{old['fg2a']}", f"{old['fg3m']}/{old['fg3a']}", f"{old['ftm']}/{old['fta']}",
                     old["orb"], old["drb"], old["reb"], old["ast"], old["stl"], old["blk"], old["to"], old["pf"],
                     old["pm"], old["min"], old["pt"], old["pts"]] if old and "fg2m" in old else [""] * 15)
            w.writerow([uid, mem.display_name if mem else uid, t.get("name", "")] + fill)
    f = discord.File(io.BytesIO(out.getvalue().encode("utf-8-sig")), filename=f"M{match}-stats.csv")
    await interaction.response.send_message(
        f"Here's the stats sheet for M{match}. Open it in Excel or Google Sheets, fill in each player's row "
        "(shots as made/attempted, like 11/15), save it as **CSV**, then upload it with `/importstats`. "
        "Leave a row blank for anyone who didn't play.", file=f, ephemeral=True)


async def import_tourney_csv(guild: discord.Guild, match: int, text: str) -> str:
    """Save a tournament match's stats from CSV text. Returns a message for the user."""
    data = load_data()
    s = guild_signups(data, guild.id)
    m = next((x for x in all_matches(s["event"]) if x["id"] == match), None)
    if m is None or m.get("a") is None or m.get("b") is None:
        return f"There's no playable match M{match}."

    # everyone on both rosters, findable by ID, mention, display name or username
    lookup, owner = {}, {}
    for tid in (m["a"], m["b"]):
        for uid in s["teams"].get(str(tid), {}).get("roster", {}):
            owner[uid] = tid
            lookup[uid] = uid
            mem = guild.get_member(int(uid))
            if mem:
                for nm in {mem.display_name, mem.name, mem.global_name or ""} - {""}:
                    lookup[nm.lower()] = uid

    try:
        dialect = csv.Sniffer().sniff(text[:2000], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    rows = list(csv.reader(io.StringIO(text), dialect))
    if not rows:
        return "That file is empty."
    keys = [sheet_key(h) for h in rows[0]]
    if "player" not in keys and "id" not in keys:
        return ("I couldn't find a **Player** (or **Discord ID**) column. Use `/importstats` to get a sheet in the "
                "right layout.")

    imported, unknown, problems = [], [], []
    for n, row in enumerate(rows[1:], start=2):
        cell = {k: (row[i] if i < len(row) else "") for i, k in enumerate(keys) if k}
        stat_cells = [cell.get(k, "") for k in ("fg2", "fg3", "ft", "orb", "drb", "reb", "ast", "stl", "blk",
                                                 "to", "pf", "pm", "min", "pt", "pts")]
        if not any(c.strip().strip("—-") for c in stat_cells):
            continue  # blank row: didn't play
        who_raw = (cell.get("id") or "").strip() or (cell.get("player") or "").strip()
        mention = re.fullmatch(r"<@!?(\d+)>", who_raw)
        uid = lookup.get(mention.group(1) if mention else who_raw) or lookup.get(who_raw.lower())
        if uid is None and cell.get("player"):
            uid = lookup.get(cell["player"].strip().lower())
        if uid is None:
            unknown.append(cell.get("player") or who_raw or f"row {n}")
            continue
        shots = {k: made_att(cell.get(k)) for k in ("fg2", "fg3", "ft")}
        if None in shots.values():
            problems.append(f"row {n}: shots must look like 11/15")
            continue
        try:
            nums = {k: cell_int(cell.get(k)) for k in ("orb", "drb", "reb", "ast", "stl", "blk", "to", "pf", "pm",
                                                       "min", "pt", "pts")}
        except ValueError as e:
            problems.append(f"row {n}: '{e}' isn't a number")
            continue
        (f2m, f2a), (f3m, f3a), (ftm, fta) = shots["fg2"], shots["fg3"], shots["ft"]
        pts = 2 * f2m + 3 * f3m + ftm if (f2a or f3a or fta) else nums["pts"]
        reb = nums["orb"] + nums["drb"] if (nums["orb"] or nums["drb"]) else nums["reb"]
        m.setdefault("box", {})[uid] = {
            "team": owner[uid], "pts": pts, "fg2m": f2m, "fg2a": f2a, "fg3m": f3m, "fg3a": f3a, "ftm": ftm,
            "fta": fta, "orb": nums["orb"], "drb": nums["drb"], "reb": reb, "ast": nums["ast"], "stl": nums["stl"],
            "blk": nums["blk"], "to": nums["to"], "pf": nums["pf"], "pm": nums["pm"], "min": nums["min"],
            "pt": nums["pt"]}
        imported.append(uid)

    if imported:
        save_data(data)
        schedule_publish(guild)
        if m.get("winner"):
            await refresh_score_card(guild, s, s["event"], m)
    msg = f"Imported stats for **{len(imported)}** player(s) in M{match}. The website updates in a minute or two."
    if unknown:
        msg += ("\nCouldn't match these names to either roster: " + ", ".join(unknown[:15])
                + ". Use their Discord name, or the Discord ID column from `/importstats`.")
    if problems:
        msg += "\nSkipped: " + "; ".join(problems[:10])
    return msg


# The game's own stats export (league gym): {"Home": {player: {TwosMade, ThreesAttempted, ...}}, "Away": {...}}
JSON_KEYS = {"TwosMade": "fg2m", "TwosAttempted": "fg2a", "ThreesMade": "fg3m", "ThreesAttempted": "fg3a",
             "FreeThrowsMade": "ftm", "FreeThrowsAttempted": "fta", "OffensiveRebounds": "orb",
             "DefensiveRebounds": "drb", "Assists": "ast", "Steals": "stl", "Blocks": "blk", "Turnovers": "to",
             "Fouls": "pf", "PlusMinus": "pm"}


def export_totals(raw: dict) -> dict:
    """Points per side in a game export: {'Home': 8, 'Away': 13}."""
    out = {}
    for side in ("Home", "Away"):
        out[side] = sum(2 * int(v.get("TwosMade", 0)) + 3 * int(v.get("ThreesMade", 0)) + int(v.get("FreeThrowsMade", 0))
                        for v in (raw.get(side) or {}).values() if isinstance(v, dict))
    return out


async def import_tourney_json(guild: discord.Guild, match: int, text: str, home_tid: int | None = None) -> str:
    """Save a match's box score from the game's JSON export. Players are matched to the rosters by Roblox name
    (server names are Roblox names), so Home/Away sort themselves out. Returns a message for the user."""
    try:
        raw = json.loads(text)
    except json.JSONDecodeError:
        return "That file isn't valid JSON. Upload the export exactly as the game made it."
    if not isinstance(raw, dict) or not any(isinstance(raw.get(k), dict) for k in ("Home", "Away")):
        return "That doesn't look like a game stats export (it needs **Home** and **Away** sections)."
    data = load_data()
    s = guild_signups(data, guild.id)
    m = next((x for x in all_matches(s["event"]) if x["id"] == match), None)
    if m is None or m.get("a") is None or m.get("b") is None:
        return f"There's no playable match M{match}."
    lookup, owner = {}, {}
    for tid in (m["a"], m["b"]):
        for uid in s["teams"].get(str(tid), {}).get("roster", {}):
            owner[uid] = tid
            mem = guild.get_member(int(uid))
            if mem:
                for nm in {roblox_name(mem), mem.display_name, mem.name, mem.global_name or ""} - {""}:
                    lookup[nm.strip().lower()] = uid
    # which side is which team: from the players we recognise (or the home option)
    side_team = {}
    for side in ("Home", "Away"):
        votes = {}
        for name in (raw.get(side) or {}):
            uid = lookup.get(str(name).strip().lower())
            if uid:
                votes[owner[uid]] = votes.get(owner[uid], 0) + 1
        if votes:
            side_team[side] = max(votes, key=votes.get)
    if home_tid in (m["a"], m["b"]):
        side_team["Home"] = home_tid
        side_team["Away"] = m["b"] if home_tid == m["a"] else m["a"]
    if len(side_team) == 1:  # only one side recognised: the other side is the other team
        known = next(iter(side_team.values()))
        side_team["Away" if "Home" in side_team else "Home"] = m["b"] if known == m["a"] else m["a"]
    imported, unknown = [], []
    for side in ("Home", "Away"):
        for name, st in (raw.get(side) or {}).items():
            if not isinstance(st, dict):
                continue
            uid = lookup.get(str(name).strip().lower())
            if uid is None:
                unknown.append(f"{name} ({side})")
                continue
            v = {k2: int(st.get(k1, 0) or 0) for k1, k2 in JSON_KEYS.items()}
            m.setdefault("box", {})[uid] = {
                "team": owner[uid], "pts": 2 * v["fg2m"] + 3 * v["fg3m"] + v["ftm"], **v,
                "reb": v["orb"] + v["drb"], "min": 0, "pt": 0}
            imported.append(uid)
    tot = export_totals(raw)
    if imported:
        save_data(data)
        schedule_publish(guild)
        if m.get("winner"):
            await refresh_score_card(guild, s, s["event"], m)
    score_line = " · ".join(f"{team_name(s, side_team[sd]) if sd in side_team else sd} {tot[sd]}"
                            for sd in ("Home", "Away"))
    msg = (f"Imported stats for **{len(imported)}** player(s) in M{match} from the game export ({score_line}). "
           "The website updates in a minute or two.")
    if unknown:
        msg += ("\nThese names aren't on either roster, so they were skipped: " + ", ".join(unknown[:15])
                + ". Their server name has to be their Roblox name.")
    return msg


async def import_export_url(guild: discord.Guild, match: int, url: str) -> str | None:
    """Download a game export attached to /game_score and import it. Returns a note, or None if it isn't JSON."""
    if not url or ".json" not in url.lower().split("?")[0]:
        return None
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            async with session.get(url) as r:
                if r.status != 200:
                    return f"Couldn't download the stats export (error {r.status}). Upload it with `/importstats`."
                text = await r.text(encoding="utf-8", errors="replace")
    except Exception as e:
        return f"Couldn't download the stats export ({e}). Upload it with `/importstats`."
    return await import_tourney_json(guild, match, text)


@app_commands.describe(match="Match number, e.g. 7 for M7", file="The game's stats export (.json) or a stats sheet (.csv)",
                       home="JSON only, if needed: the team that was Home in the export (usually worked out by itself)")
async def importstats(interaction: discord.Interaction, match: int, file: discord.Attachment,
                      home: discord.Role | None = None):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only Referees and league staff can import stats.",
                                                       ephemeral=True)
    fname = file.filename.lower()
    if not fname.endswith((".csv", ".txt", ".json")) or file.size > 500_000:
        return await interaction.response.send_message(
            "Upload the game's stats export (**.json**), or a sheet saved as **CSV**.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    text = (await file.read()).decode("utf-8-sig", errors="replace")
    if fname.endswith(".json") or text.lstrip().startswith("{"):
        msg = await import_tourney_json(interaction.guild, match, text, home.id if home else None)
    else:
        msg = await import_tourney_csv(interaction.guild, match, text)
    await interaction.followup.send(msg, ephemeral=True)

FAKE_FIRST = ["Neon", "Midnight", "Crimson", "Golden", "Frozen", "Thunder", "Shadow", "Iron", "Solar", "Rapid",
              "Electric", "Savage", "Silent", "Royal", "Toxic", "Cosmic", "Wild", "Atomic", "Blazing", "Phantom",
              "Lunar", "Storm", "Velvet", "Turbo", "Nova", "Venom", "Arctic", "Rogue", "Prime", "Hyper"]
FAKE_SECOND = ["Hoopers", "Dunkers", "Ballers", "Wolves", "Hawks", "Kings", "Vipers", "Titans", "Ravens", "Bulls",
               "Sharks", "Comets", "Knights", "Raptors", "Phoenix", "Giants", "Falcons", "Panthers", "Rockets",
               "Cobras", "Spartans", "Mavericks", "Lynx", "Owls", "Dragons", "Jets", "Rhinos", "Foxes", "Bears",
               "Saints"]
FAKE_HANDLES = ["Ace", "Blitz", "Cruz", "Dash", "Echo", "Flash", "Ghost", "Haze", "Ivy", "Jett", "Kairo", "Lux",
                "Mav", "Nox", "Onyx", "Pike", "Quill", "Rex", "Sage", "Tank", "Uzi", "Vex", "Wolfie", "Xeno", "Yuki",
                "Zed", "Kobe", "Drip", "Swish", "Clutch", "Handles", "Splash", "Bucket", "Lefty", "Stretch", "Boogie"]
FAKE_COLORS = ["#ef4444", "#f97316", "#eab308", "#22c55e", "#14b8a6", "#06b6d4", "#3b82f6", "#6366f1", "#8b5cf6",
               "#d946ef", "#ec4899", "#f43f5e", "#84cc16", "#0ea5e9", "#a855f7", "#f59e0b"]


def fake_league(n: int, rng: random.Random) -> tuple[list[str], dict[str, list[str]]]:
    """n unique team names, each with a roster of 6 made-up player names."""
    combos = [f"{a} {b}" for a in FAKE_FIRST for b in FAKE_SECOND]
    names = rng.sample(combos, n)
    rosters, used = {}, set()
    for nm in names:
        players = []
        while len(players) < 6:
            p = f"{rng.choice(FAKE_HANDLES)}{rng.choice(['', '', str(rng.randint(1, 99)), 'x', '_'])}"
            if p not in used:
                used.add(p)
                players.append(p)
        rosters[nm] = players
    return names, rosters


def fake_logo_svg(name: str, rng: random.Random) -> str:
    c1, c2 = rng.sample(FAKE_COLORS, 2)
    initials = "".join(w[0] for w in name.split()[:2]).upper()
    shape = rng.choice([
        '<circle cx="64" cy="64" r="56"/>',
        '<path d="M64 8 L116 30 V70 C116 98 92 116 64 122 C36 116 12 98 12 70 V30 Z"/>',
        '<path d="M64 6 L118 37 V91 L64 122 L10 91 V37 Z"/>',
        '<rect x="12" y="12" width="104" height="104" rx="24"/>',
        '<path d="M64 6 L122 64 L64 122 L6 64 Z"/>',
    ])
    stripe = rng.choice(['<path d="M0 88 L128 40 V58 L0 106 Z" fill="{c}" opacity=".35"/>',
                         '<circle cx="64" cy="64" r="40" fill="none" stroke="{c}" stroke-width="6" opacity=".5"/>',
                         '']).format(c=c2)
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128">'
            f'<defs><clipPath id="s">{shape}</clipPath></defs>'
            f'<g clip-path="url(#s)"><rect width="128" height="128" fill="{c1}"/>{stripe}</g>'
            f'<g fill="none" stroke="{c2}" stroke-width="5">{shape}</g>'
            f'<text x="64" y="80" text-anchor="middle" font-family="Arial Black, Arial, sans-serif" '
            f'font-weight="900" font-size="44" fill="#fff">{initials}</text></svg>')


def fake_box(team_id: int, players: list[str], points: int, margin: int, rng: random.Random) -> dict:
    """Split a team's points across 5 or 6 players with full shooting splits and the other stats."""
    used = players[:rng.choice([5, 6])]
    weights = [rng.uniform(0.4, 1.0) * (2.2 if i == 0 else 1.4 if i == 1 else 1) for i in range(len(used))]
    rng.shuffle(weights)
    raw = [points * w / sum(weights) for w in weights]
    pts = [int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - pts[i], reverse=True)[:points - sum(pts)]:
        pts[i] += 1
    box = {}
    for p, total in zip(used, pts):
        fg3m = rng.randint(0, total // 3 // 2 + (1 if total >= 9 else 0))
        rest = total - 3 * fg3m
        ftm = rest % 2 + 2 * rng.randint(0, min(1, rest // 2))  # same odd/even as `rest`, so 2s fill the gap
        fg2m = (rest - ftm) // 2
        orb, drb = rng.randint(0, 4), rng.randint(0, 7)
        box[p] = {"team": team_id, "pts": 2 * fg2m + 3 * fg3m + ftm,
                  "fg2m": fg2m, "fg2a": fg2m + rng.randint(0, 5), "fg3m": fg3m, "fg3a": fg3m + rng.randint(0, 6),
                  "ftm": ftm, "fta": ftm + rng.randint(0, 2), "orb": orb, "drb": drb, "reb": orb + drb,
                  "ast": rng.randint(0, 10), "stl": rng.randint(0, 4), "blk": rng.randint(0, 3),
                  "to": rng.randint(0, 4), "pf": rng.randint(0, 4), "pm": margin, "min": 0,
                  "pt": 2 * fg2m + 3 * fg3m + ftm + rng.randint(0, 14)}
    return box


# ---------------------------------------------------------------- pickups (ranked queue with RR)
#
# Players queue in #pickups with buttons. When the queue fills, the bot balances two teams by RR,
# opens two voice channels and posts the match. A player from each team confirms the winner
# (or staff force it), and everyone's RR goes up or down. Ranks: Iron, Bronze, Silver, Gold, Platinum,
# Diamond, Amethyst, Ruby, Vibrant, each with divisions 1-3 of 100 RR. Saved in s["pug"].

RANKS = [("Iron", 0x8B8B8B), ("Bronze", 0xB0723C), ("Silver", 0xC0C7CF), ("Gold", 0xE0B44A),
         ("Platinum", 0x2DD4BF), ("Diamond", 0x7DD3FC), ("Amethyst", 0x9B5DE5), ("Ruby", 0xE0115F),
         ("Vibrant", 0xFF4FD8)]
VIBRANT_AT = (len(RANKS) - 1) * 300  # 2400: Vibrant is the top rank, a single tier with no ceiling


def pug(s: dict) -> dict:
    p = s.setdefault("pug", {})
    p.setdefault("size", 10)          # players per match (10 = 5v5)
    p.setdefault("start", 900)        # hidden starting RR (Gold 1); 3 placement games set the real rank
    p.setdefault("k", 40)             # how much RR a match can move (about +/-20 between even teams)
    p.setdefault("mode", "draft")     # "draft": 2 random captains pick players; "balanced": bot splits by RR
    p.setdefault("queue", [])
    p.setdefault("panel", None)       # [channel id, message id] of the queue card
    p.setdefault("next", 1)
    p.setdefault("matches", {})
    p.setdefault("players", {})
    p.setdefault("qpos", {})          # the position each queued player picked for this game
    p["_pos"] = {**s.get("positions", {}), **p["qpos"]}  # shown on pickup cards and in the draft menu
    return p


def pug_player(p: dict, uid: int) -> dict:
    pl = p["players"].setdefault(str(uid), {"rr": p["start"], "w": 0, "l": 0})
    pl["rr"] = int(round(pl["rr"]))  # RR is always a whole number
    return pl


def rank_of(rr: float) -> tuple[str, int, int, int]:
    """RR -> (rank name, division 1-3 (0 for Vibrant), RR inside the division, rank index)."""
    rr = max(0, int(rr))
    if rr >= VIBRANT_AT:
        return RANKS[-1][0], 0, rr - VIBRANT_AT, len(RANKS) - 1
    idx = rr // 300
    return RANKS[idx][0], (rr % 300) // 100 + 1, rr % 100, idx


def rank_text(rr: int) -> str:
    name, div, inside, _i = rank_of(rr)
    return f"{name} {div} · {inside} RR" if div else f"{name} · {inside} RR"


PLACEMENTS = 3               # games before you get a rank
PLACE_RANGE = (600, 1499)    # placements land you somewhere from Silver 1 to Platinum 3
PLACE_BOOST = 4              # placement games move your hidden RR 4x as much, so 3 games can sort you out


def games_played(pl: dict) -> int:
    return pl.get("w", 0) + pl.get("l", 0)


def is_placed(pl: dict) -> bool:
    return games_played(pl) >= PLACEMENTS


def show_rank(pl: dict) -> str:
    """'Gold 2 · 40 RR', or 'Unranked · placements 1/3' while someone is still placing."""
    return rank_text(pl["rr"]) if is_placed(pl) else f"Unranked · placements {games_played(pl)}/{PLACEMENTS}"


def show_rr(pl: dict) -> str:
    return f"{pl['rr']} RR" if is_placed(pl) else f"placements {games_played(pl)}/{PLACEMENTS}"


def balance(players: list[int], p: dict) -> tuple[list[int], list[int]]:
    """Snake draft by RR (A B B A A B ...) so both teams have similar strength."""
    order = sorted(players, key=lambda u: -pug_player(p, u)["rr"])
    a, b = [], []
    for i, u in enumerate(order):
        (a if i % 4 in (0, 3) else b).append(u)
    return a, b


def avg_rr(p: dict, team: list[int]) -> float:
    return sum(pug_player(p, u)["rr"] for u in team) / max(1, len(team))




RR_MIN, RR_MAX = 10, 32  # base: every win is +10 to +32, every loss -10 to -32
GREAT_GAME = 0.8         # top 20% of the lobby on the winning team = great game, gains doubled
STREAK_MULT = {3: 1.25, 4: 1.5, 5: 1.75, 6: 2.0, 7: 2.5, 8: 3.0, 9: 3.0}  # 10+ wins in a row = x4


def streak_mult(n: int) -> float:
    return 4.0 if n >= 10 else STREAK_MULT.get(n, 1.0)


def perf_score(line: dict) -> float:
    """One number for how well someone played, from their pickup box score."""
    return (line.get("pts", 0) + 1.2 * line.get("ast", 0) + 0.9 * line.get("reb", 0)
            + 2 * line.get("stl", 0) + 2 * line.get("blk", 0) - 1.5 * line.get("to", 0))


def rr_change(p: dict, m: dict, winners: list[int], losers: list[int]) -> tuple[dict, dict]:
    """Each player's base RR change from how well they played compared with everyone else in the game.
    Best player in the game: win +32 / lose -10. Worst: win +10 / lose -32.
    Until stats are entered everyone gets the middle (+21 / -21); entering stats later adjusts it.
    Returns (base change, performance 0..1 or None without stats)."""
    box = m.get("box") or {}
    players = winners + losers
    scored = {u: perf_score(box[str(u)]) for u in players if str(u) in box}
    out, perf = {}, {}
    for u in players:
        won = u in winners
        if str(u) in box and len(scored) > 1:
            below = sum(1 for v in scored.values() if v < scored[u])
            ties = sum(1 for v in scored.values() if v == scored[u]) - 1
            pct = (below + ties / 2) / (len(scored) - 1)  # 0 = played worst, 1 = played best
            perf[u] = pct
        else:
            pct, perf[u] = 0.5, None
        spread = RR_MAX - RR_MIN
        out[u] = round(RR_MIN + spread * pct) if won else -round(RR_MAX - spread * pct)
    return out, perf


def div_index(rr: int) -> int:
    """Which division someone is in, counting up from Iron 1 (Vibrant is one division)."""
    return min(max(0, int(rr)), VIBRANT_AT) // 100


class QueueView(discord.ui.View):
    """Join / Leave buttons, plus links to the website's leaderboard and live queue."""

    def __init__(self, guild_id: int):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Join Queue", style=discord.ButtonStyle.primary,
                                        custom_id=f"pug:join:{guild_id}:0:0"))
        self.add_item(discord.ui.Button(label="Leave Queue", style=discord.ButtonStyle.danger,
                                        custom_id=f"pug:leave:{guild_id}:0:0"))
        if site_url():
            self.add_item(discord.ui.Button(label="Leaderboard", style=discord.ButtonStyle.link, row=1,
                                            url=f"{site_url()}#leaderboard"))
            self.add_item(discord.ui.Button(label="Web Queue", style=discord.ButtonStyle.link, row=1,
                                            url=f"{site_url()}#queue"))


class ReportView(discord.ui.View):
    def __init__(self, guild_id: int, mid: str):
        super().__init__(timeout=None)
        for side in ("A", "B"):
            self.add_item(discord.ui.Button(label=f"Team {side} won", style=discord.ButtonStyle.primary,
                                            custom_id=f"pug:win:{guild_id}:{mid}:{side}"))
        self.add_item(discord.ui.Button(label="Share server code", emoji="🔑", style=discord.ButtonStyle.success,
                                        custom_id=f"pug:code:{guild_id}:{mid}:0"))
        self.add_item(discord.ui.Button(label="Cancel match (staff)", style=discord.ButtonStyle.danger,
                                        custom_id=f"pug:cancel:{guild_id}:{mid}:0"))


def queue_card(s: dict) -> discord.Embed:
    """Looks like a classic queue bot: what just happened, then the queue count and who's in it."""
    p = pug(s)
    n = p["size"] // 2
    lines = []
    last = p.get("last_event")
    if last:
        lines += [f"**{last[0]}**", f"<@{last[1]}>", ""]
    lines.append(f"**Queue {len(p['queue'])}/{p['size']}**")
    if p["queue"]:
        lines += [f"<@{u}>{' · ' + p['qpos'][str(u)] if p['qpos'].get(str(u)) else ''} · **{show_rr(pug_player(p, u))}**"
                  for u in p["queue"]]
        counts = {v: sum(1 for u in p["queue"] if p["qpos"].get(str(u)) == v) for v, _n in POSITIONS}
        lines.append("\n" + " · ".join(f"{v} {c}" for v, c in counts.items()))
    else:
        lines.append("*Empty. Click **Join Queue** and pick your position.*")
    live = [m for m in p["matches"].values() if m["status"] in ("live", "draft")]
    if live:
        lines.append("\n**In progress:** " + ", ".join(f"Queue#P{m['id']}" for m in live))
    how = "captains' draft" if p.get("mode", "draft") == "draft" else "auto-balanced"
    e = discord.Embed(title=f"OTR Ranked {n}v{n} Queue", description="\n".join(lines), colour=BRAND,
                      timestamp=datetime.now(timezone.utc))
    e.set_footer(text=f"{how} · Iron to Vibrant · win +10 to +32 RR, lose -10 to -32 RR")
    return e


async def refresh_queue(guild: discord.Guild, data: dict):
    s = guild_signups(data, guild.id)
    p = pug(s)
    if not p["panel"]:
        return
    ch = guild.get_channel(p["panel"][0])
    if ch is None:
        return
    try:
        msg = await ch.fetch_message(p["panel"][1])
        await msg.edit(embed=queue_card(s), view=QueueView(guild.id))
    except discord.HTTPException:
        msg = await ch.send(embed=queue_card(s), view=QueueView(guild.id))
        p["panel"] = [ch.id, msg.id]
        save_data(data)
    schedule_publish(guild, 6.0, quick=True)  # live queue on the website's Ranked tab


async def sync_rank_role(guild: discord.Guild, uid: int, rr: int, ranked: bool = True):
    """Give the player the role for their rank (Iron ... Vibrant) and remove the others.
    Players still in placements get no rank role."""
    want = rank_of(rr)[0] if ranked else None
    roles = {name: role(guild, name) for name, _c in RANKS}
    try:
        mem = await guild.fetch_member(uid)
    except discord.HTTPException:
        return
    remove = [r for n, r in roles.items() if r and n != want and r in mem.roles]
    try:
        if remove:
            await mem.remove_roles(*remove)
        if roles.get(want) and roles[want] not in mem.roles:
            await mem.add_roles(roles[want])
    except discord.HTTPException:
        pass


def snake(n: int) -> list[str]:
    """Pick order for n picks: A B B A A B B A ..."""
    return ["A" if i % 4 in (0, 3) else "B" for i in range(n)]


class DraftView(discord.ui.View):
    """Dropdown of players still to be picked, plus a staff cancel button. Handled in on_interaction."""

    def __init__(self, guild: discord.Guild, p: dict, m: dict):
        super().__init__(timeout=None)
        opts = []
        for u in m["pool"][:25]:
            mem = guild.get_member(u)
            pos = p.get("_pos", {}).get(str(u))
            opts.append(discord.SelectOption(label=(mem.display_name if mem else str(u))[:100], value=str(u),
                                             description=(f"{pos} · " if pos else "") + show_rank(pug_player(p, u))))
        side = m["order"][m["turn"]]
        cap = m["a"][0] if side == "A" else m["b"][0]
        mem = guild.get_member(cap)
        self.add_item(discord.ui.Select(custom_id=f"pug:pick:{guild.id}:{m['id']}:0", options=opts,
                                        placeholder=f"Captain {(mem.display_name if mem else 'Team ' + side)[:60]}: pick a player",
                                        min_values=1, max_values=1))
        self.add_item(discord.ui.Button(label="Cancel draft (staff)", style=discord.ButtonStyle.danger,
                                        custom_id=f"pug:cancel:{guild.id}:{m['id']}:0"))


def draft_card(p: dict, m: dict) -> discord.Embed:
    side = m["order"][m["turn"]] if m["pool"] else None
    lines = [f"**Captains** (picked at random): <@{m['a'][0]}> for Team A, <@{m['b'][0]}> for Team B", ""]
    for name, team in (("A", m["a"]), ("B", m["b"])):
        lines.append(f"**Team {name}** · avg {avg_rr(p, team):.0f} RR")
        lines += [f"{'(C) ' if i == 0 else ''}<@{u}>{(' · ' + p['_pos'][str(u)]) if str(u) in p.get('_pos', {}) else ''}"
                  f" · {show_rank(pug_player(p, u))}" for i, u in enumerate(team)]
        lines.append("")
    if side:
        cap = m["a"][0] if side == "A" else m["b"][0]
        lines.append(f"**On the clock:** <@{cap}> (Team {side}) · pick from the menu below. "
                     f"{len(m['pool'])} player(s) left.")
    return brand_embed("\n".join(lines), f"Pickup P{m['id']} · captains' draft", GOLD)


def waiting_vc(guild: discord.Guild, p: dict):
    """The 🔊 waiting room players must sit in to queue (made by /setupbot part:ranked)."""
    return guild.get_channel(p.get("chans", {}).get("waiting") or 0)


PICKUP_NEEDS_VC = False  # True = players must sit in the waiting room to queue (and lose their spot if they leave)


def in_waiting(guild: discord.Guild, p: dict, uid) -> bool:
    if not PICKUP_NEEDS_VC:
        return True  # voice isn't required to queue
    vc = waiting_vc(guild, p)
    if vc is None:
        return True  # no waiting room set up yet: don't block anyone
    mem = guild.get_member(int(uid))
    return bool(mem and mem.voice and mem.voice.channel and mem.voice.channel.id == vc.id)


def need_vc_text(guild: discord.Guild, p: dict) -> str:
    vc = waiting_vc(guild, p)
    return (f"Join the {vc.mention if vc else 'waiting room'} voice channel first. You have to be in voice to "
            "queue, and stay there until the queue pops.")


async def close_match_vcs(guild: discord.Guild, p: dict, m: dict, reason: str):
    """Send everyone in the match's team calls back to the waiting room, then delete the calls."""
    back = waiting_vc(guild, p)
    for vc_id in m.get("vcs", []):
        vc = guild.get_channel(vc_id)
        if not vc:
            continue
        for mem in list(getattr(vc, "members", [])):
            try:
                if back:
                    await mem.move_to(back, reason=reason)
            except discord.HTTPException:
                pass
        try:
            await vc.delete(reason=reason)
        except discord.HTTPException:
            pass


async def start_pickup(guild: discord.Guild, data: dict):
    """The queue is full: either draft (two random captains pick from a menu) or auto-balance by RR."""
    s = guild_signups(data, guild.id)
    p = pug(s)
    gone = [u for u in p["queue"][:p["size"]] if not in_waiting(guild, p, u)]
    if gone:  # anyone who left the waiting room loses their spot, and the queue waits for more players
        for u in gone:
            p["queue"].remove(u)
            p["qpos"].pop(str(u), None)
        p["last_event"] = ["Removed: not in voice", gone[0]]
        save_data(data)
        ch = pug_ch(guild, p, "queue")
        if ch:
            await post(ch, " ".join(f"<@{u}>" for u in gone) + " left the waiting room, so they were taken out of "
                       f"the queue. Queue: **{len(p['queue'])}/{p['size']}**.", title="Queue held", color=MUTED,
                       ping=" ".join(f"<@{u}>" for u in gone))
        if len(p["queue"]) < p["size"]:
            return
    players, p["queue"] = p["queue"][:p["size"]], p["queue"][p["size"]:]
    mid = str(p["next"])
    p["next"] += 1
    if p.get("mode", "draft") == "draft" and len(players) >= 4:
        caps = random.sample(players, 2)
        pool = [u for u in players if u not in caps]
        m = {"id": mid, "a": [caps[0]], "b": [caps[1]], "pool": pool, "order": snake(len(pool)), "turn": 0,
             "status": "draft", "claims": {}, "vcs": [], "date": datetime.now(timezone.utc).isoformat(timespec="seconds")}
        p["matches"][mid] = m
        save_data(data)
        ch = pug_ch(guild, p, "queue")
        if ch:
            msg = await ch.send(content=" ".join(f"<@{u}>" for u in players), embed=draft_card(p, m),
                                view=DraftView(guild, p, m), allowed_mentions=discord.AllowedMentions(users=True))
            m["draft_card"] = [ch.id, msg.id]
            save_data(data)
        return
    a, b = balance(players, p)
    m = {"id": mid, "a": a, "b": b, "status": "live", "claims": {}, "vcs": [],
         "date": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    p["matches"][mid] = m
    await go_live(guild, data, m)


async def go_live(guild: discord.Guild, data: dict, m: dict):
    """Teams are set: open voice channels and post the match card with the report buttons."""
    p = pug(guild_signups(data, guild.id))
    m["status"] = "live"
    a, b, mid = m["a"], m["b"], m["id"]
    cat = pug_ch(guild, p, "category") or await get_or_make_category(guild, f"{p['size']} MANS")
    # captains: the drafting captains, or the highest-RR player on each auto-balanced team
    if m.get("pool") is not None:
        caps = [a[0], b[0]]
    else:
        caps = [max(t, key=lambda u: pug_player(p, u)["rr"]) for t in (a, b)]
    m["caps"] = caps
    host = max(caps, key=lambda u: pug_player(p, u)["rr"])  # the higher-rated captain makes the server
    m["host"] = host
    staff_roles = [r for r in (role(guild, "Commissioner"), role(guild, DOE), role(guild, "League Staff"), role(guild, "Referee")) if r]
    missing = []
    for side, team in (("A", a), ("B", b)):
        ow = {guild.default_role: discord.PermissionOverwrite(view_channel=True, connect=False),
              guild.me: discord.PermissionOverwrite(view_channel=True, connect=True, move_members=True,
                                                    manage_channels=True)}
        for r in staff_roles:
            ow[r] = discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)
        for u in team:
            mem = guild.get_member(u)
            if mem:
                ow[mem] = discord.PermissionOverwrite(view_channel=True, connect=True, speak=True, stream=True)
        try:
            vc = await guild.create_voice_channel(f"🔒 P{mid} · Team {side}", category=cat, overwrites=ow,
                                                  user_limit=len(team) + 2, reason=f"Pickup P{mid}")
            m["vcs"].append(vc.id)
        except discord.HTTPException:
            vc = None
        for u in team:  # drag everyone into their team's call
            mem = guild.get_member(u)
            try:
                if vc and mem and mem.voice and mem.voice.channel:
                    await mem.move_to(vc, reason=f"Pickup P{mid}")
                else:
                    missing.append(u)
            except discord.HTTPException:
                missing.append(u)
    save_data(data)
    ch = pug_ch(guild, p, "queue")
    cap = lambda team, u: "(C) " if u in caps else ""
    pz = lambda u: f" · {p['_pos'][str(u)]}" if str(u) in p.get("_pos", {}) else ""
    desc = (f"**Team A** · avg {avg_rr(p, a):.0f} RR\n" + "\n".join(f"{cap(a, u)}<@{u}>{pz(u)} · {show_rank(pug_player(p, u))}" for u in a)
            + f"\n\n**Team B** · avg {avg_rr(p, b):.0f} RR\n" + "\n".join(f"{cap(b, u)}<@{u}>{pz(u)} · {show_rank(pug_player(p, u))}" for u in b)
            + f"\n\n**Host:** <@{host}> (captain) makes the private server, then clicks **Share server code** "
              "so the bot sends it to all 10 players."
            + (f"\n**Voice:** " + " · ".join(f"<#{v}>" for v in m["vcs"]) + " are locked to each team and staff."
               if m["vcs"] else "")
            + (f"\nCouldn't move " + ", ".join(f"<@{u}>" for u in missing) + " (not in voice): join your team's call."
               if missing else "")
            + "\nWhen it's done, one player from **each** team clicks who won. Both have to agree."
            + "\nThen the host (or staff) enters stats with `/pickupstats` or `/pickupstat`: each win is "
              "+10 to +32 RR and each loss -10 to -32, depending on how well you played.")
    e = brand_embed(desc, f"Pickup P{mid} is ready", GOOD)
    if ch:
        msg = await ch.send(content=" ".join(f"<@{u}>" for u in a + b), embed=e, view=ReportView(guild.id, mid),
                            allowed_mentions=discord.AllowedMentions(users=True))
        m["card"] = [ch.id, msg.id]
        save_data(data)
    try:
        hm = guild.get_member(host)
        if hm:
            await hm.send(embed=brand_embed(
                f"You're the **host** of pickup **P{mid}** in {guild.name}.\n1. Make the private server in Practical "
                "Basketball.\n2. Click **Share server code** on the match card and type the code.\nThe bot sends it "
                "to every player in the match.", "You're hosting", GOLD))
    except discord.HTTPException:
        pass


async def draft_pick(interaction: discord.Interaction, guild: discord.Guild, data: dict, m: dict):
    p = pug(guild_signups(data, guild.id))
    side = m["order"][m["turn"]]
    cap = m["a"][0] if side == "A" else m["b"][0]
    if interaction.user.id != cap:
        return await interaction.response.send_message(f"It's <@{cap}>'s pick right now.", ephemeral=True,
                                                       allowed_mentions=NO_PINGS)
    pick = int((interaction.data or {}).get("values", ["0"])[0])
    if pick not in m["pool"]:
        return await interaction.response.send_message("That player was already picked.", ephemeral=True)
    m["pool"].remove(pick)
    (m["a"] if side == "A" else m["b"]).append(pick)
    m["turn"] += 1
    if len(m["pool"]) == 1:  # last player goes to whoever's turn it is
        last = m["pool"].pop()
        (m["a"] if m["order"][m["turn"]] == "A" else m["b"]).append(last)
        m["turn"] += 1
    save_data(data)
    if m["pool"]:
        return await interaction.response.edit_message(embed=draft_card(p, m), view=DraftView(guild, p, m))
    done = draft_card(p, m)
    done.title = f"Pickup P{m['id']} · draft complete"
    await interaction.response.edit_message(embed=done, view=None)
    await go_live(guild, data, m)


def winner_card(p: dict, m: dict) -> discord.Embed:
    deltas = m.get("deltas", {})
    ups = m.get("ups", {})
    words = {1: "⬆ RANK UP", 2: "⬆⬆ DOUBLE RANK UP", 3: "⬆⬆⬆ TRIPLE RANK UP"}

    def col(team):
        out = []
        for u in team:
            k = str(u)
            d, rr = deltas.get(k, 0), int(pug_player(p, u)["rr"])
            pg = m.get("pgame", {}).get(k, 0)
            if pg and pg < PLACEMENTS:
                out.append(f"<@{u}> *placement {pg}/{PLACEMENTS}*")
                continue
            if pg == PLACEMENTS:
                out.append(f"<@{u}> **placed: {rank_text(m['after'][k]).split(' · ')[0]}** ({m['after'][k]})")
                continue
            line = f"<@{u}> *{'+' if d > 0 else ''}{d}* **({m.get('after', {}).get(k, rr)})**"
            n = ups.get(k, 0)
            if n > 0:
                line += f" {words.get(n, f'⬆ x{n} RANK UP')} → {rank_text(m['after'][k]).split(' · ')[0]}"
            elif n < 0:
                line += f" ⬇ {rank_text(m['after'][k]).split(' · ')[0]}"
            if m.get("bonus", {}).get(k):
                line += "\n  " + " · ".join(m["bonus"][k])
            out.append(line)
        return "\n".join(out)

    w = m["winner"]
    e = discord.Embed(title=f"🏆 Winner For Queue#P{m['id']} 🏆", colour=BRAND, timestamp=datetime.now(timezone.utc))
    e.add_field(name=f"Team A{' 🏆' if w == 'A' else ''}", value=col(m["a"])[:1024], inline=True)
    e.add_field(name=f"Team B{' 🏆' if w == 'B' else ''}", value=col(m["b"])[:1024], inline=True)
    note = ("RR from each player's stats: +10 to +32 a win, -10 to -32 a loss. Great games double it, "
            "win streaks of 3+ multiply it." if m.get("box") else
            "Everyone got the middle amount (±21) for now. When stats are entered with /pickupstats, RR is "
            "adjusted for how each player played (great games x2, win streaks multiply).")
    e.set_footer(text=note)
    return e


async def apply_pickup_rr(guild: discord.Guild, data: dict, m: dict):
    """Give (or correct) everyone's RR for a finished pickup, then sync rank roles and the result card.
    - Base: +10 to +32 for a win, -10 to -32 for a loss, from how well you played.
    - Great game (top of the lobby on the winning team): gains doubled.
    - Win streaks: 3 in a row x1.25, 4 x1.5, 5 x1.75, 6 x2, 7 x2.5, 8-9 x3, 10+ x4 (stacks with great game).
    - Big gains can jump several divisions at once: double and triple rank-ups.
    - Placement games (a player's first 3) count 4x; after the 3rd you're placed Silver 1 to Platinum 3."""
    p = pug(guild_signups(data, guild.id))
    win, lose = (m["a"], m["b"]) if m["winner"] == "A" else (m["b"], m["a"])
    base, perf = rr_change(p, m, win, lose)
    before, after, pgame = m.setdefault("before", {}), m.setdefault("after", {}), m.setdefault("pgame", {})
    streak = m.setdefault("streak", {})
    bonus, ups, final = m.setdefault("bonus", {}), m.setdefault("ups", {}), {}
    for u in win + lose:
        k = str(u)
        pl = pug_player(p, u)
        if k not in before:  # first time this result is applied (w/l are already counted)
            before[k] = pl["rr"]
            after[k] = pl["rr"]
            pgame[k] = games_played(pl) if games_played(pl) <= PLACEMENTS else 0
            pl["streak"] = pl.get("streak", 0) + 1 if u in win else 0
            streak[k] = pl["streak"]
        d = base[u]
        tags = []
        if pgame[k]:
            d *= PLACE_BOOST
        elif u in win:
            if perf[u] is not None and perf[u] >= GREAT_GAME:
                d *= 2
                tags.append("GREAT GAME x2")
            sm = streak_mult(streak[k])
            if sm > 1:
                d *= sm
                tags.append(f"🔥{streak[k]} streak x{sm:g}")
        d = int(round(d))
        target = before[k] + d
        if pgame[k] == PLACEMENTS:
            target = min(max(target, PLACE_RANGE[0]), PLACE_RANGE[1])
        target = max(0, int(target))
        pl["rr"] = max(0, pl["rr"] + target - after[k])  # also keeps any games played since
        after[k] = target
        final[k] = target - before[k]
        bonus[k] = tags
        ups[k] = 0 if pgame[k] else div_index(target) - div_index(before[k])
    m["deltas"] = final
    m["gain"] = round(sum(final[str(u)] for u in win) / len(win))
    m["loss"] = round(-sum(final[str(u)] for u in lose) / len(lose))
    save_data(data)
    for u in win + lose:
        pl = pug_player(p, u)
        await sync_rank_role(guild, u, pl["rr"], is_placed(pl))
    await ranked_highlights(guild, p, m)
    save_data(data)
    if m.get("result_card"):
        ch = guild.get_channel(m["result_card"][0])
        if ch:
            try:
                await (await ch.fetch_message(m["result_card"][1])).edit(embed=winner_card(p, m))
            except discord.HTTPException:
                pass
    schedule_publish(guild)


async def finish_pickup(guild: discord.Guild, data: dict, mid: str, winner: str, by: int) -> str:
    s = guild_signups(data, guild.id)
    p = pug(s)
    m = p["matches"][mid]
    win, lose = (m["a"], m["b"]) if winner == "A" else (m["b"], m["a"])
    for u in win:
        pug_player(p, u)["w"] += 1
    for u in lose:
        pug_player(p, u)["l"] += 1
    m["positions"] = {str(u): p["qpos"].pop(str(u), None) for u in m["a"] + m["b"]}  # keep a record on the match
    m.update(status="done", winner=winner, reported_by=by, finished=datetime.now(timezone.utc).isoformat(timespec="seconds"))
    await close_match_vcs(guild, p, m, f"Pickup P{mid} finished")
    await apply_pickup_rr(guild, data, m)
    if m.get("card"):
        ch = guild.get_channel(m["card"][0])
        if ch:
            try:
                msg = await ch.fetch_message(m["card"][1])
                await msg.edit(view=None)
            except discord.HTTPException:
                pass
            sent = await ch.send(embed=winner_card(p, m), allowed_mentions=NO_PINGS)
            m["result_card"] = [ch.id, sent.id]
            save_data(data)
    return f"Team {winner} won Queue#P{mid}"


def can_enter_pickup_stats(member: discord.Member, m: dict) -> bool:
    return is_official(member) or member.id == m.get("host")


async def save_pickup_lines(guild: discord.Guild, data: dict, m: dict):
    save_data(data)
    if m["status"] == "done":
        await apply_pickup_rr(guild, data, m)  # re-rate everyone now that we know how they played


@bot.tree.command(description="Enter one player's stats for a pickup (sets how much RR they win or lose).")
@app_commands.describe(match="Pickup number, e.g. 12 for P12", player="The player", points="Points",
                       rebounds="Rebounds", assists="Assists", steals="Steals", blocks="Blocks",
                       turnovers="Turnovers")
async def pickupstat(interaction: discord.Interaction, match: int, player: discord.Member,
                     points: app_commands.Range[int, 0, 300], rebounds: app_commands.Range[int, 0, 200] = 0,
                     assists: app_commands.Range[int, 0, 200] = 0, steals: app_commands.Range[int, 0, 200] = 0,
                     blocks: app_commands.Range[int, 0, 200] = 0, turnovers: app_commands.Range[int, 0, 200] = 0):
    data = load_data()
    p = pug(guild_signups(data, interaction.guild.id))
    m = p["matches"].get(str(match))
    if not m or m["status"] not in ("live", "done"):
        return await interaction.response.send_message(f"There's no pickup P{match} to enter stats for.",
                                                       ephemeral=True)
    if not can_enter_pickup_stats(interaction.user, m):
        return await interaction.response.send_message("Only the host of that pickup or staff/Referees can enter stats.",
                                                       ephemeral=True)
    if player.id not in m["a"] + m["b"]:
        return await interaction.response.send_message(f"{player.mention} didn't play in P{match}.", ephemeral=True,
                                                       allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    m.setdefault("box", {})[str(player.id)] = {"team": "A" if player.id in m["a"] else "B", "pts": points,
                                               "reb": rebounds, "ast": assists, "stl": steals, "blk": blocks,
                                               "to": turnovers}
    await save_pickup_lines(interaction.guild, data, m)
    left = len(m["a"] + m["b"]) - len(m["box"])
    await interaction.followup.send(
        f"P{match}: saved {player.mention}'s stats.{f' {left} player(s) still need stats.' if left else ' All stats are in.'}"
        + (" RR has been updated for how everyone played." if m["status"] == "done" else ""),
        ephemeral=True, allowed_mentions=NO_PINGS)


@app_commands.describe(match="Pickup number, e.g. 12 for P12")
async def pickuptemplate(interaction: discord.Interaction, match: int):
    guild = interaction.guild
    p = pug(guild_signups(load_data(), guild.id))
    m = p["matches"].get(str(match))
    if not m:
        return await interaction.response.send_message(f"There's no pickup P{match}.", ephemeral=True)
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["Discord ID", "Player", "Team", "PTS", "REB", "AST", "STL", "BLK", "TO"])
    for side in ("a", "b"):
        for u in m[side]:
            mem = guild.get_member(u)
            old = (m.get("box") or {}).get(str(u), {})
            w.writerow([u, mem.display_name if mem else u, side.upper()]
                       + [old.get(k, "") for k in ("pts", "reb", "ast", "stl", "blk", "to")])
    f = discord.File(io.BytesIO(out.getvalue().encode("utf-8-sig")), filename=f"P{match}-stats.csv")
    await interaction.response.send_message("Fill it in, save as CSV, then upload it with `/pickupstats`.",
                                            file=f, ephemeral=True)


async def import_pickup_csv(guild: discord.Guild, data: dict, m: dict, match: int, text: str) -> str:
    """Save a pickup's stats from CSV text (and re-rate RR). Returns a message for the user."""
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return "That file is empty."
    keys = [sheet_key(h) for h in rows[0]]
    lookup = {}
    for u in m["a"] + m["b"]:
        lookup[str(u)] = u
        mem = guild.get_member(u)
        if mem:
            for nm in {mem.display_name, mem.name, mem.global_name or ""} - {""}:
                lookup[nm.lower()] = u
    done, unknown = 0, []
    for row in rows[1:]:
        cell = {k: (row[i] if i < len(row) else "") for i, k in enumerate(keys) if k}
        if not any((cell.get(k) or "").strip() for k in ("pts", "reb", "ast", "stl", "blk", "to", "fg2", "fg3", "ft")):
            continue
        who_raw = (cell.get("id") or cell.get("player") or "").strip()
        u = lookup.get(who_raw) or lookup.get(who_raw.lower()) or lookup.get((cell.get("player") or "").strip().lower())
        if u is None:
            unknown.append(who_raw or "?")
            continue
        try:
            n = {k: cell_int(cell.get(k)) for k in ("pts", "reb", "ast", "stl", "blk", "to", "orb", "drb")}
        except ValueError:
            unknown.append(f"{who_raw} (bad number)")
            continue
        shots = [made_att(cell.get(k)) or (0, 0) for k in ("fg2", "fg3", "ft")]
        pts = 2 * shots[0][0] + 3 * shots[1][0] + shots[2][0] if any(a for _m, a in shots) else n["pts"]
        m.setdefault("box", {})[str(u)] = {"team": "A" if u in m["a"] else "B", "pts": pts,
                                           "reb": n["reb"] or n["orb"] + n["drb"], "ast": n["ast"],
                                           "stl": n["stl"], "blk": n["blk"], "to": n["to"]}
        done += 1
    if done:
        await save_pickup_lines(guild, data, m)
    msg = f"Saved stats for **{done}** player(s) in P{match}."
    if m["status"] == "done" and done:
        msg += " RR has been updated for how everyone played."
    if unknown:
        msg += "\nCouldn't match: " + ", ".join(unknown[:12])
    return msg


@app_commands.describe(match="Pickup number, e.g. 12 for P12", file="The stats sheet saved as CSV")
async def pickupstats(interaction: discord.Interaction, match: int, file: discord.Attachment):
    guild = interaction.guild
    data = load_data()
    p = pug(guild_signups(data, guild.id))
    m = p["matches"].get(str(match))
    if not m or m["status"] not in ("live", "done"):
        return await interaction.response.send_message(f"There's no pickup P{match} to enter stats for.",
                                                       ephemeral=True)
    if not can_enter_pickup_stats(interaction.user, m):
        return await interaction.response.send_message("Only the host of that pickup or staff/Referees can enter stats.",
                                                       ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    text = (await file.read()).decode("utf-8-sig", errors="replace")
    msg = await import_pickup_csv(guild, data, m, match, text)
    await interaction.followup.send(msg, ephemeral=True)


@bot.listen("on_interaction")
async def pickup_buttons(interaction: discord.Interaction):
    cid = (interaction.data or {}).get("custom_id", "") if interaction.type == discord.InteractionType.component else ""
    if not cid.startswith("pug:"):
        return
    try:
        _p, action, gid, mid, side = cid.split(":")
    except ValueError:
        return
    guild = bot.get_guild(int(gid))
    if guild is None:
        return
    data = load_data()
    s = guild_signups(data, guild.id)
    p = pug(s)
    uid = interaction.user.id
    busy = any(uid in m["a"] + m["b"] + m.get("pool", []) for m in p["matches"].values()
               if m["status"] in ("live", "draft"))

    picked = None
    if action == "setpos":
        val = (interaction.data or {}).get("values", [""])[0]
        if val not in dict(POSITIONS):
            return
        s.setdefault("positions", {})[str(uid)] = val  # also becomes their usual position
        save_data(data)
        if mid != "join":
            return await interaction.response.edit_message(content=f"Position set: **{val}**.", view=None)
        action, picked = "join", val
    if action == "join" and not in_waiting(guild, p, uid):
        return await interaction.response.send_message(need_vc_text(guild, p), ephemeral=True) if picked is None else \
            await interaction.response.edit_message(content=need_vc_text(guild, p), view=None)
    if action == "join":
        blocked = suspended_from(s, uid, "queue")
        if blocked:
            return await interaction.response.send_message(blocked, ephemeral=True) if picked is None else \
                await interaction.response.edit_message(content=blocked, view=None)
    if action == "join" and picked is None:
        # everyone lists the position they're playing before they get in the queue
        usual = pos_of(s, uid)
        hint = f" (usually **{usual}**)" if usual else ""
        if busy:
            return await interaction.response.send_message("You're already in a live pickup.", ephemeral=True)
        if uid in p["queue"]:
            return await interaction.response.send_message("You're already in the queue.", ephemeral=True)
        return await interaction.response.send_message(f"What position are you playing this game{hint}?",
                                                       view=PositionPick(guild.id, "join"), ephemeral=True)
    if action == "join":
        if busy:
            return await interaction.response.send_message("You're already in a live pickup.", ephemeral=True)
        if uid in p["queue"]:
            return await interaction.response.send_message("You're already in the queue.", ephemeral=True)
        p["queue"].append(uid)
        p["qpos"][str(uid)] = picked
        p["last_event"] = ["Player Joined Queue!", uid]
        pug_player(p, uid)
        save_data(data)
        await interaction.response.edit_message(
            content=f"You're in the queue as **{picked}** ({len(p['queue'])}/{p['size']}) · "
                    f"**{show_rr(pug_player(p, uid))}** ({show_rank(pug_player(p, uid)).split(' · ')[0]})", view=None)
        if len(p["queue"]) >= p["size"]:
            await start_pickup(guild, data)
        await refresh_queue(guild, data)
        return
    if action == "leave":
        if uid in p["queue"]:
            p["queue"].remove(uid)
            p["qpos"].pop(str(uid), None)
            p["last_event"] = ["Player Left Queue!", uid]
            save_data(data)
            await interaction.response.send_message("You left the queue.", ephemeral=True)
            await refresh_queue(guild, data)
        else:
            await interaction.response.send_message("You're not in the queue.", ephemeral=True)
        return

    m = p["matches"].get(mid)
    if not m or m["status"] not in ("live", "draft"):
        return await interaction.response.send_message("That pickup is already finished.", ephemeral=True)
    if action == "pick":
        if m["status"] != "draft":
            return await interaction.response.send_message("The draft is already done.", ephemeral=True)
        return await draft_pick(interaction, guild, data, m)
    if action == "win" and m["status"] != "live":
        return await interaction.response.send_message("The teams aren't picked yet.", ephemeral=True)
    member = guild.get_member(uid)
    staff = member is not None and is_staff(member)
    if action == "code":
        if uid not in m.get("caps", [m.get("host")]) and not staff:
            return await interaction.response.send_message(f"Only the host <@{m.get('host')}> (or the other captain, "
                                                           "or staff) can share the code.", ephemeral=True,
                                                           allowed_mentions=NO_PINGS)
        modal = discord.ui.Modal(title=f"P{mid} server code", custom_id=f"pugcode:{gid}:{mid}")
        modal.add_item(discord.ui.TextInput(label="Private server code or link", max_length=200,
                                            placeholder="Paste the code or the private server link"))
        return await interaction.response.send_modal(modal)
    if action == "cancel":
        if not staff:
            return await interaction.response.send_message("Only staff can cancel a pickup.", ephemeral=True)
        m["status"] = "cancelled"
        for u in m["a"] + m["b"] + m.get("pool", []):
            p["qpos"].pop(str(u), None)
        m["pool"] = []
        save_data(data)
        await interaction.response.edit_message(view=None)
        await close_match_vcs(guild, p, m, f"Pickup P{mid} cancelled")
        await post(interaction.channel, f"Pickup P{mid} was cancelled by staff. No RR changed.",
                   title="Pickup cancelled", color=MUTED)
        await refresh_queue(guild, data)
        return
    if action == "win":
        team_of_user = "A" if uid in m["a"] else "B" if uid in m["b"] else None
        if team_of_user is None and not staff:
            return await interaction.response.send_message("Only players in this pickup (or staff) can report it.",
                                                           ephemeral=True)
        if staff and team_of_user is None:
            await interaction.response.send_message(f"Recorded: Team {side} won P{mid}.", ephemeral=True)
            await finish_pickup(guild, data, mid, side, uid)
            return await refresh_queue(guild, data)
        m["claims"][team_of_user] = side
        save_data(data)
        claims = m["claims"]
        if len(claims) == 2 and claims["A"] == claims["B"]:
            await interaction.response.send_message(f"Both teams agree: Team {side} won. Updating RR...",
                                                    ephemeral=True)
            await finish_pickup(guild, data, mid, side, uid)
            return await refresh_queue(guild, data)
        if len(claims) == 2:
            return await interaction.response.send_message(
                "The two teams reported different winners. Sort it out, click again, or ask staff to settle it.",
                ephemeral=True)
        other = "B" if team_of_user == "A" else "A"
        await interaction.response.send_message(
            f"Got it: Team {team_of_user} says Team {side} won. Waiting for a Team {other} player to confirm.",
            ephemeral=True)


def pug_ch(guild: discord.Guild, p: dict, key: str):
    """One of the ranked channels the bot made (announcements, info, general, queue, category)."""
    cid = p.get("chans", {}).get(key)
    ch = guild.get_channel(cid) if cid else None
    if ch is None and key == "queue":
        ch = chan(guild, "pickups")  # servers set up before the 10 MANS category existed
    return ch


def info_cards(p: dict) -> list[discord.Embed]:
    """Everything players need to know, posted in the info channel."""
    n = p["size"] // 2
    draft = p.get("mode", "draft") == "draft"
    how = brand_embed("\n".join([
        "1. Click **Join Queue** and pick the position you're playing (PG, SG, SF, PF, C). You don't need to be "
        "in voice to queue. Hang out in the **🔊 Waiting Room** if you want to be moved into your team's call "
        "automatically.",
        f"2. When **{p['size']}** players are in, " + (
            "the bot picks **2 random captains**. They take turns picking players from a dropdown "
            "(A, B, B, A, A, B, B, A); the last player is placed automatically."
            if draft else "the bot splits everyone into **two balanced teams** by RR."),
        "3. Each team gets its own **locked voice call** (only that team and staff can join) and the bot moves "
        "you in. One captain hosts: they make the private server and click **Share server code**, and the bot "
        "DMs it to everyone.",
        "4. When the game ends, **one player from each team** clicks who won. Both have to agree, or staff settle it.",
        "5. The host (or staff) enters everyone's stats with `/pickupstats` (sheet from `/pickupstats`) or "
        "`/pickupstat`. Your RR is set from how well you played.",
    ]), f"How {n}v{n} ranked works", BRAND)

    ladder = []
    for i, (name, _c) in enumerate(RANKS[:-1]):
        ladder.append(f"**{name}** 1 · 2 · 3 — from **{i * 300}** RR")
    ladder.append(f"**{RANKS[-1][0]}** — **{VIBRANT_AT}+** RR, the top rank (one tier, no ceiling)")
    ranks = brand_embed("\n".join(ladder) + "\n\nEach division is **100 RR**. Your rank role updates automatically.",
                        "Ranks", GOLD)

    rr = brand_embed("\n".join([
        f"**Placements:** your first **{PLACEMENTS} games** are placement games. You're Unranked until then, "
        f"they count extra, and you're placed somewhere from **Silver 1 to Platinum 3**.",
        "",
        f"**Every win:** +{RR_MIN} to +{RR_MAX} RR. **Every loss:** -{RR_MIN} to -{RR_MAX} RR. "
        "Where you land depends on how you played compared with everyone else in the game: the best player "
        f"wins +{RR_MAX} or only loses -{RR_MIN}; the worst wins +{RR_MIN} or loses -{RR_MAX}.",
        "Until stats are entered everyone gets ±21, then it's corrected.",
        "",
        "**Great game:** top of the lobby on the winning team = gains **x2**.",
        "**Win streaks:** 3 in a row x1.25 · 4 x1.5 · 5 x1.75 · 6 x2 · 7 x2.5 · 8-9 x3 · 10+ x4. "
        "Streaks stack with great games and reset when you lose.",
        "Big wins can jump several divisions at once: **double and triple rank-ups**.",
    ]), "RR (rank rating)", GOOD)

    cmds = brand_embed("\n".join([
        "`/rank` your rank, RR, record and streak · `/rank player:@name` someone else's",
        "`/leaderboard` top 20 by RR",
        "`/position` set your usual position",
        "`/pickupstat` · `/pickupstats` · `/pickupstats` enter a game's stats (host or staff)",
        "Website: the **Leaderboard** tab has every ranked player (filter by rank or position); **Ranked** shows the live queue and recent games.",
    ]), "Commands", INFO)

    rules = brand_embed("\n".join([
        "1. Only queue if you can play the whole game.",
        "2. Don't leave or throw a game. Staff can take away RR for it.",
        "3. Report the result honestly. Fake reports can get you banned from the queue.",
        "4. Play the position you queued as, or agree a swap with your captain.",
        "5. Respect captains' picks. No complaining in chat about who got drafted when.",
        "6. Disputes go to staff with a clip or screenshot. Staff decisions are final.",
    ]), f"{p['size']} mans rules", BRAND)
    return [how, ranks, rr, cmds, rules]


async def build_tens_channels(guild: discord.Guild, p: dict) -> dict:
    """Make the category and channels, like:  10 MANS / 📢｜10s-announcements / ℹ️｜10s-info /
    🏠・10s-general / 🎮｜10s-queue. Reuses any that already exist."""
    size = p["size"]
    chans = p.setdefault("chans", {})
    cat = guild.get_channel(chans.get("category") or 0)
    if cat is None:
        cat = discord.utils.get(guild.categories, name=f"{size} MANS") or await guild.create_category(f"{size} MANS")
        chans["category"] = cat.id
    elif cat.name != f"{size} MANS":
        try:
            await cat.edit(name=f"{size} MANS")
        except discord.HTTPException:
            pass
    wanted = [("announcements", f"📢｜{size}s-announcements", "ro"), ("info", f"ℹ️｜{size}s-info", "ro"),
              ("general", f"🏠・{size}s-general", "open"), ("queue", f"🎮｜{size}s-queue", "ro")]
    wname = f"🔊 {size}s Waiting Room"
    vc = guild.get_channel(chans.get("waiting") or 0)
    if vc is None:
        vc = discord.utils.get(cat.voice_channels, name=wname) or await guild.create_voice_channel(wname, category=cat)
        chans["waiting"] = vc.id
    elif vc.name != wname:
        try:
            await vc.edit(name=wname)
        except discord.HTTPException:
            pass
    for key, name, access in wanted:
        ch = guild.get_channel(chans.get(key) or 0)
        if ch is None:
            ch = discord.utils.get(cat.text_channels, name=name) or await guild.create_text_channel(
                name, category=cat, overwrites=overwrites_for(guild, access))
            chans[key] = ch.id
        elif ch.name != name:  # e.g. switched from 10 mans to 6 mans
            try:
                await ch.edit(name=name)
            except discord.HTTPException:
                pass
    return chans


async def refresh_info(guild: discord.Guild, p: dict):
    """Clear the bot's old posts in the info channel and post the current info cards."""
    ch = pug_ch(guild, p, "info")
    if ch is None:
        return
    try:
        async for msg in ch.history(limit=50):
            if msg.author.id == guild.me.id:
                await msg.delete()
    except discord.HTTPException:
        pass
    for e in info_cards(p):
        await ch.send(embed=e)


# one-time setup: run with /setupbot part:ranked
async def pickupsetup(interaction: discord.Interaction, players: int = 10,
                      start_rr: app_commands.Range[int, 0, 2000] = 900,
                      rr_swing: app_commands.Range[int, 10, 100] = 40, teams: str = "draft"):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can set up pickups.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    for name, color in reversed(RANKS):
        if role(guild, name) is None:
            try:
                await guild.create_role(name=name, colour=discord.Colour(color), hoist=False, reason="Pickup ranks")
            except discord.HTTPException:
                pass
    data = load_data()
    s = guild_signups(data, guild.id)
    p = pug(s)
    p["size"], p["start"], p["k"], p["mode"] = players, start_rr, rr_swing, teams
    first_time = not p.get("chans", {}).get("announcements")
    await build_tens_channels(guild, p)
    save_data(data)
    try:
        await ensure_pickup_host(guild)
    except Exception as e:
        print(f"[pickup host] {e}")

    # queue card
    ch = pug_ch(guild, p, "queue")
    old = p["panel"]
    msg = await ch.send(embed=queue_card(s), view=QueueView(guild.id))
    p["panel"] = [ch.id, msg.id]
    save_data(data)
    if old and old[1] != msg.id:
        try:
            await (await guild.get_channel(old[0]).fetch_message(old[1])).delete()
        except Exception:
            pass

    await refresh_info(guild, p)
    ann = pug_ch(guild, p, "announcements")
    if ann and first_time:
        await post(ann, "\n".join([
            f"Ranked **{players // 2}v{players // 2}** pickups are live!",
            f"Jump in from <#{p['chans']['queue']}>: click **Join Queue** and pick your position.",
            f"Your first **{PLACEMENTS} games** are placements, then you get your rank (Iron to Vibrant).",
            "Great games double your RR, win streaks multiply it, and you can double or triple rank up.",
            f"Read <#{p['chans']['info']}> for how it all works. Chat in <#{p['chans']['general']}>.",
        ]), title=f"{players} MANS is open", color=GOLD)
    await interaction.followup.send(
        f"{players} MANS is set up: announcements, info (filled in), general chat and the queue in {ch.mention}. "
        f"{players // 2}v{players // 2}, {'captains draft' if teams == 'draft' else 'auto-balanced teams'}. "
        "Rank roles Iron to Vibrant are ready.", ephemeral=True)


async def ranked_highlights(guild: discord.Guild, p: dict, m: dict):
    """Post big moments in the announcements channel: double/triple rank-ups, 5+ win streaks, placements done."""
    ann = pug_ch(guild, p, "announcements")
    if ann is None:
        return
    said = m.setdefault("announced", [])
    lines = []
    for k, n in m.get("ups", {}).items():
        if n >= 2 and f"up{k}" not in said:
            word = "TRIPLE" if n >= 3 else "DOUBLE"
            lines.append(f"⬆ **{word} RANK UP!** <@{k}> jumped to **{rank_text(m['after'][k]).split(' · ')[0]}** "
                         f"(+{m['deltas'][k]} RR)")
            said.append(f"up{k}")
    for k, st in m.get("streak", {}).items():
        if st >= 5 and f"st{k}" not in said and k in [str(u) for u in (m["a"] if m["winner"] == "A" else m["b"])]:
            lines.append(f"🔥 <@{k}> is on a **{st}-game win streak** (x{streak_mult(st):g} RR)")
            said.append(f"st{k}")
    for k, g in m.get("pgame", {}).items():
        if g == PLACEMENTS and f"pl{k}" not in said:
            lines.append(f"🎯 <@{k}> finished placements: **{rank_text(m['after'][k]).split(' · ')[0]}**")
            said.append(f"pl{k}")
    if lines:
        await post(ann, "\n".join(lines), title=f"Queue#P{m['id']} highlights", color=GOLD)


@bot.tree.command(description="See a player's pickup rank, RR and record.")
@app_commands.describe(player="Leave empty for yourself")
async def rank(interaction: discord.Interaction, player: discord.Member | None = None):
    who_ = player or interaction.user
    p = pug(guild_signups(load_data(), interaction.guild.id))
    pl = p["players"].get(str(who_.id))
    if not pl:
        return await interaction.response.send_message(f"{who_.display_name} hasn't played a pickup yet.",
                                                       ephemeral=True)
    name, div, inside, idx = rank_of(pl["rr"])
    games = pl["w"] + pl["l"]
    if not is_placed(pl):
        e = brand_embed(f"**Unranked** · placements **{games}/{PLACEMENTS}**\n"
                        f"Play {PLACEMENTS - games} more game(s) to get your rank. Placements put you somewhere "
                        f"from Silver 1 to Platinum 3, and count extra.\n\n**Record:** {pl['w']}W - {pl['l']}L",
                        f"{who_.display_name}", MUTED)
        e.set_thumbnail(url=who_.display_avatar.url)
        return await interaction.response.send_message(embed=e, ephemeral=True)
    streak_txt = f"\n🔥 **{pl.get('streak', 0)} win streak** (next win x{streak_mult(pl.get('streak', 0) + 1):g})" \
        if pl.get("streak", 0) >= 2 else ""
    bar = "█" * min(10, inside // 10) + "░" * (10 - min(10, inside // 10))
    nxt = "top rank" if not div else f"{100 - inside} RR to the next division"
    pos = sorted(((k, v) for k, v in p["players"].items() if is_placed(v)), key=lambda kv: -kv[1]["rr"])
    place = next(i for i, (k, _v) in enumerate(pos, 1) if k == str(who_.id))
    title_rank = f"{name} {div}" if div else name
    e = brand_embed(f"**{title_rank}** · {inside} RR\n`{bar}` {nxt}\n\n**Record:** {pl['w']}W - {pl['l']}L"
                    f" ({100 * pl['w'] / games:.0f}% wins){streak_txt}\n**Leaderboard:** #{place} of {len(pos)}" if games else
                    f"**{title_rank}** · {inside} RR\nNo games yet.", f"{who_.display_name}", RANKS[idx][1])
    e.set_thumbnail(url=who_.display_avatar.url)
    await interaction.response.send_message(embed=e, ephemeral=True)


@bot.tree.command(description="Top pickup players by RR.")
async def leaderboard(interaction: discord.Interaction):
    p = pug(guild_signups(load_data(), interaction.guild.id))
    rows = sorted(((k, v) for k, v in p["players"].items() if is_placed(v)), key=lambda kv: -kv[1]["rr"])[:20]
    if not rows:
        return await interaction.response.send_message("No pickups played yet.", ephemeral=True)
    lines = [f"`{i:>2}.` <@{k}> · **{int(v['rr'])} RR** · {rank_text(v['rr']).split(' · ')[0]} · {v['w']}W-{v['l']}L"
             for i, (k, v) in enumerate(rows, 1)]
    await interaction.response.send_message(embed=brand_embed("\n".join(lines), "Pickup leaderboard", GOLD),
                                            ephemeral=True)


@bot.tree.command(description="Staff: record a pickup result (overrides player reports).")
@app_commands.describe(match="Pickup number, e.g. 12 for P12", winner="Which team won")
@app_commands.choices(winner=[app_commands.Choice(name="Team A", value="A"), app_commands.Choice(name="Team B", value="B")])
@app_commands.default_permissions(manage_roles=True)
async def pickupresult(interaction: discord.Interaction, match: int, winner: str):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only staff can do that.", ephemeral=True)
    data = load_data()
    p = pug(guild_signups(data, interaction.guild.id))
    m = p["matches"].get(str(match))
    if not m or m["status"] != "live":
        return await interaction.response.send_message(f"P{match} isn't a live pickup.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    await finish_pickup(interaction.guild, data, str(match), winner, interaction.user.id)
    await refresh_queue(interaction.guild, data)
    await interaction.followup.send(f"P{match}: Team {winner} won. RR updated.", ephemeral=True)


@app_commands.describe(player="The player", rr="New RR: Iron 0, Bronze 300, Silver 600, Gold 900, Platinum 1200, "
                                               "Diamond 1500, Amethyst 1800, Ruby 2100, Vibrant 2400")
@app_commands.default_permissions(manage_roles=True)
async def setrr(interaction: discord.Interaction, player: discord.Member, rr: app_commands.Range[int, 0, 10000]):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only staff can do that.", ephemeral=True)
    data = load_data()
    p = pug(guild_signups(data, interaction.guild.id))
    pug_player(p, player.id)["rr"] = rr
    save_data(data)
    await interaction.response.send_message(f"{player.mention} is now {rank_text(rr)}.", ephemeral=True,
                                            allowed_mentions=NO_PINGS)
    await sync_rank_role(interaction.guild, player.id, rr)
    schedule_publish(interaction.guild)


@app_commands.describe(confirm="Set to True to reset every player's RR and record")
@app_commands.default_permissions(manage_roles=True)
async def resetrr(interaction: discord.Interaction, confirm: bool = False):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only staff can do that.", ephemeral=True)
    if not confirm:
        return await interaction.response.send_message("Run /setrr reset_all:True confirm:True to reset everyone.", ephemeral=True)
    data = load_data()
    p = pug(guild_signups(data, interaction.guild.id))
    p["players"] = {}
    save_data(data)
    await interaction.response.send_message("Pickup season reset: everyone starts again at "
                                            f"{rank_text(p['start'])}. Rank roles update after their next game.",
                                            ephemeral=True)
    schedule_publish(interaction.guild)


# ---------------------------------------------------------------- tickets
#
# /setupbot part:tickets makes a SUPPORT category with 🎫｜open-a-ticket (a card with a dropdown) and a staff-only
# 📁｜ticket-logs. Picking a topic opens a short form, then a private channel only that player and staff
# can see. Staff can Claim it; the player or staff can Close it, which saves a transcript to the logs
# (and DMs it to the player) and deletes the channel. Saved in s["tickets"].

TICKET_TYPES = [
    ("stats", "📊", "Stats", "Wrong or missing stats, box scores, RR from stats",
     "Which match (e.g. M7 or P12), which player, what's wrong, and a screenshot of the in-game stats."),
    ("cheater", "🚨", "Report a cheater", "Exploits, scripts, alt accounts, playing on two teams",
     "Who (Discord and Roblox name), which match and when, and a clip or screenshot. Reports without proof "
     "are hard to act on."),
    ("ranked", "🏆", "Ranked / RR", "Pickup result disputes, RR or rank problems",
     "The Queue# (e.g. P12), what happened, and any screenshots."),
    ("team", "👥", "Team / roster", "Roster changes, captaincy, logos, team disputes",
     "Your team name and what you need changed."),
    ("roles", "🏷️", "Roles", "Missing or wrong roles",
     "Which role you need and why (e.g. you're a captain, a referee, a content creator)."),
    ("media", "🎥", "Media", "Content creators, streams, highlights, partnerships",
     "Your channel or socials, what you make, and what you'd like to do with the circuit."),
    ("appeal", "⚖️", "Appeal", "Appeal a ban, timeout or penalty",
     "What the penalty was, when it happened, and why it should be changed."),
    ("general", "💬", "General support", "Anything else",
     "Tell us what you need help with."),
]
TICKET_INFO = {t[0]: t for t in TICKET_TYPES}


def tickets(s: dict) -> dict:
    t = s.setdefault("tickets", {})
    t.setdefault("next", 1)
    t.setdefault("open", {})   # channel id -> {user, type, num, claimed, opened}
    t.setdefault("chans", {})  # category, panel, logs
    return t


class TicketPanel(discord.ui.View):
    def __init__(self, guild_id: int):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Select(
            custom_id=f"tkt:open:{guild_id}:0", placeholder="Choose what your ticket is about",
            options=[discord.SelectOption(label=name, value=key, emoji=emoji, description=desc[:100])
                     for key, emoji, name, desc, _help in TICKET_TYPES]))


class TicketForm(discord.ui.Modal):
    def __init__(self, guild_id: int, kind: str):
        _k, emoji, name, _desc, help_ = TICKET_INFO[kind]
        super().__init__(title=f"{name} ticket"[:45], custom_id=f"tkt:form:{guild_id}:{kind}")
        self.add_item(discord.ui.TextInput(label="What's this about?", style=discord.TextStyle.paragraph,
                                           placeholder=help_[:100], max_length=1000, required=True))


class TicketButtons(discord.ui.View):
    def __init__(self, guild_id: int):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Claim (staff)", style=discord.ButtonStyle.primary, emoji="🙋",
                                        custom_id=f"tkt:claim:{guild_id}:0"))
        self.add_item(discord.ui.Button(label="Close ticket", style=discord.ButtonStyle.danger, emoji="🔒",
                                        custom_id=f"tkt:close:{guild_id}:0"))


def ticket_staff_roles(guild: discord.Guild) -> list:
    return [r for r in (role(guild, "Commissioner"), role(guild, DOE), role(guild, "League Staff"), role(guild, "Referee")) if r]


def panel_card() -> discord.Embed:
    lines = ["Need help from staff? Pick a topic from the menu below. A private channel opens that only you and "
             "staff can see.", ""]
    lines += [f"{emoji} **{name}** · {desc}" for _k, emoji, name, desc, _h in TICKET_TYPES]
    lines += ["", "Please open one ticket per issue and include proof (clips or screenshots) where you can."]
    return brand_embed("\n".join(lines), "Support tickets", BRAND)


async def open_ticket(interaction: discord.Interaction, guild: discord.Guild, kind: str, details: str):
    data = load_data()
    s = guild_signups(data, guild.id)
    t = tickets(s)
    user = interaction.user
    mine = [c for c, info in t["open"].items() if info["user"] == user.id and guild.get_channel(int(c))]
    if any(t["open"][c]["type"] == kind for c in mine):
        c = next(c for c in mine if t["open"][c]["type"] == kind)
        return await interaction.response.send_message(f"You already have an open {TICKET_INFO[kind][2]} ticket: <#{c}>",
                                                       ephemeral=True)
    if len(mine) >= 3:
        return await interaction.response.send_message("You have 3 tickets open already. Close one first.",
                                                       ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    num = t["next"]
    t["next"] += 1
    cat = guild.get_channel(t["chans"].get("category") or 0) or await get_or_make_category(guild, "SUPPORT")
    ow = {guild.default_role: discord.PermissionOverwrite(view_channel=False),
          guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True,
                                                manage_messages=True),
          user: discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True,
                                            embed_links=True, read_message_history=True)}
    for r in ticket_staff_roles(guild):
        ow[r] = discord.PermissionOverwrite(view_channel=True, send_messages=True, attach_files=True,
                                            read_message_history=True)
    _k, emoji, name, _desc, help_ = TICKET_INFO[kind]
    slug = re.sub(r"[^a-z0-9]+", "-", user.name.lower()).strip("-")[:20] or "player"
    ch = await guild.create_text_channel(f"{kind}-{num:04d}-{slug}", category=cat, overwrites=ow,
                                         topic=f"{name} ticket #{num:04d} opened by {user} ({user.id})")
    t["open"][str(ch.id)] = {"user": user.id, "type": kind, "num": num, "claimed": None,
                             "opened": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    save_data(data)
    e = brand_embed(f"**Opened by:** {user.mention}\n**Topic:** {emoji} {name}\n\n**Details**\n{details}\n\n"
                    f"*To help staff:* {help_}\nYou can add screenshots or clips here. Staff will reply soon.",
                    f"Ticket #{num:04d} · {name}", BRAND)
    ls = role(guild, "League Staff")
    staff_ping = ls.mention if ls else ""  # ping League Staff once
    await ch.send(content=f"{user.mention} {staff_ping}".strip(), embed=e, view=TicketButtons(guild.id),
                  allowed_mentions=discord.AllowedMentions(users=True, roles=True))
    await interaction.followup.send(f"Your ticket is open: {ch.mention}", ephemeral=True)


async def close_ticket(guild: discord.Guild, ch, closer, reason: str | None = None):
    data = load_data()
    s = guild_signups(data, guild.id)
    t = tickets(s)
    info = t["open"].pop(str(ch.id), None)
    save_data(data)
    if not info:
        return
    _k, emoji, name, _d, _h = TICKET_INFO.get(info["type"], TICKET_INFO["general"])
    lines = [f"Ticket #{info['num']:04d} · {name}", f"Opened by {info['user']} at {info['opened']}",
             f"Closed by {closer} ({getattr(closer, 'id', '')}) at {datetime.now(timezone.utc).isoformat(timespec='seconds')}",
             f"Reason: {reason or '-'}", "-" * 60]
    try:
        async for msg in ch.history(limit=1000, oldest_first=True):
            text = msg.content or ""
            for e in msg.embeds:
                text += f" [embed: {e.title or ''} {(e.description or '')[:300]}]"
            for a in msg.attachments:
                text += f" [file: {a.url}]"
            lines.append(f"[{msg.created_at:%Y-%m-%d %H:%M}] {msg.author.display_name}: {text.strip()}")
    except discord.HTTPException:
        lines.append("(couldn't read the messages)")
    transcript = "\n".join(lines)
    fname = f"ticket-{info['num']:04d}-{info['type']}.txt"
    summary = (f"**Topic:** {emoji} {name}\n**Opened by:** <@{info['user']}>\n**Claimed by:** "
               f"{'<@' + str(info['claimed']) + '>' if info.get('claimed') else 'nobody'}\n"
               f"**Closed by:** {getattr(closer, 'mention', closer)}\n**Reason:** {reason or '-'}")
    logs = guild.get_channel(t["chans"].get("logs") or 0)
    if logs:
        await logs.send(embed=brand_embed(summary, f"Ticket #{info['num']:04d} closed", MUTED),
                        file=discord.File(io.BytesIO(transcript.encode("utf-8")), filename=fname),
                        allowed_mentions=NO_PINGS)
    try:
        opener = await bot.fetch_user(info["user"])
        await opener.send(embed=brand_embed(summary, f"Your ticket #{info['num']:04d} was closed", MUTED),
                          file=discord.File(io.BytesIO(transcript.encode("utf-8")), filename=fname))
    except discord.HTTPException:
        pass
    try:
        await ch.send(embed=brand_embed(f"Closed by {getattr(closer, 'mention', closer)}. This channel will be "
                                        "deleted in 5 seconds.", "Ticket closed", MUTED))
        await asyncio.sleep(5)
        await ch.delete(reason=f"Ticket #{info['num']:04d} closed")
    except discord.HTTPException:
        pass


@bot.listen("on_interaction")
async def ticket_events(interaction: discord.Interaction):
    if interaction.type not in (discord.InteractionType.component, discord.InteractionType.modal_submit):
        return
    cid = (interaction.data or {}).get("custom_id", "")
    if not cid.startswith("tkt:"):
        return
    _p, action, gid, kind = cid.split(":")
    guild = bot.get_guild(int(gid))
    if guild is None:
        return
    if action == "open":
        kind = (interaction.data.get("values") or ["general"])[0]
        if kind not in TICKET_INFO:
            return
        await interaction.response.send_modal(TicketForm(guild.id, kind))
        try:  # reset the dropdown so the same topic can be picked again
            await interaction.message.edit(embed=panel_card(), view=TicketPanel(guild.id))
        except discord.HTTPException:
            pass
        return
    if action == "form":
        rows = interaction.data.get("components") or []
        details = ""
        for row in rows:
            for comp in row.get("components", []):
                details = comp.get("value") or details
        return await open_ticket(interaction, guild, kind if kind in TICKET_INFO else "general", details or "-")

    data = load_data()
    t = tickets(guild_signups(data, guild.id))
    info = t["open"].get(str(interaction.channel.id)) if interaction.channel else None
    if not info:
        return await interaction.response.send_message("This ticket is already closed.", ephemeral=True)
    member = guild.get_member(interaction.user.id)
    staff = member is not None and (is_staff(member) or any(r.name == "Referee" for r in member.roles))
    if action == "claim":
        if not staff:
            return await interaction.response.send_message("Only staff can claim tickets.", ephemeral=True)
        info["claimed"] = interaction.user.id
        save_data(data)
        await interaction.response.send_message(embed=brand_embed(f"{interaction.user.mention} is handling this ticket.",
                                                                  "Ticket claimed", GOOD))
    elif action == "close":
        if not staff and interaction.user.id != info["user"]:
            return await interaction.response.send_message("Only the person who opened it or staff can close it.",
                                                           ephemeral=True)
        await interaction.response.send_message("Closing the ticket and saving a transcript...", ephemeral=True)
        await close_ticket(guild, interaction.channel, interaction.user)


# one-time setup: run with /setupbot part:tickets
async def ticketsetup(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can set up tickets.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    data = load_data()
    t = tickets(guild_signups(data, guild.id))
    ch = t["chans"]
    cat = guild.get_channel(ch.get("category") or 0)
    if cat is None:
        cat = discord.utils.get(guild.categories, name="SUPPORT") or await guild.create_category("SUPPORT")
        ch["category"] = cat.id
    panel = guild.get_channel(ch.get("panel") or 0)
    if panel is None:
        panel = await guild.create_text_channel("🎫｜open-a-ticket", category=cat,
                                                overwrites=overwrites_for(guild, "ro"))
        ch["panel"] = panel.id
    logs = guild.get_channel(ch.get("logs") or 0)
    if logs is None:
        logs = await guild.create_text_channel("📁｜ticket-logs", category=cat,
                                               overwrites=overwrites_for(guild, "staff"))
        ch["logs"] = logs.id
    if t.get("panel_msg"):
        try:
            await (await panel.fetch_message(t["panel_msg"])).delete()
        except discord.HTTPException:
            pass
    msg = await panel.send(embed=panel_card(), view=TicketPanel(guild.id))
    t["panel_msg"] = msg.id
    save_data(data)
    await interaction.followup.send(f"Tickets are ready: players open them in {panel.mention}. Transcripts go to "
                                    f"{logs.mention} (staff only).", ephemeral=True)


async def ticket_here(interaction: discord.Interaction):
    data = load_data()
    t = tickets(guild_signups(data, interaction.guild.id))
    return data, t, t["open"].get(str(interaction.channel.id))


@app_commands.describe(member="Who to add")
@app_commands.default_permissions(manage_messages=True)
async def ticketadd(interaction: discord.Interaction, member: discord.Member):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only staff can do that.", ephemeral=True)
    _d, _t, info = await ticket_here(interaction)
    if not info:
        return await interaction.response.send_message("Use this inside a ticket channel.", ephemeral=True)
    await interaction.channel.set_permissions(member, view_channel=True, send_messages=True, attach_files=True,
                                              read_message_history=True)
    await interaction.response.send_message(f"Added {member.mention} to the ticket.")


@app_commands.describe(member="Who to remove")
@app_commands.default_permissions(manage_messages=True)
async def ticketremove(interaction: discord.Interaction, member: discord.Member):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only staff can do that.", ephemeral=True)
    _d, _t, info = await ticket_here(interaction)
    if not info:
        return await interaction.response.send_message("Use this inside a ticket channel.", ephemeral=True)
    await interaction.channel.set_permissions(member, overwrite=None)
    await interaction.response.send_message(f"Removed {member.mention} from the ticket.", allowed_mentions=NO_PINGS)


@app_commands.describe(reason="Why it's being closed (optional)")
async def ticketclose(interaction: discord.Interaction, reason: str | None = None):
    _d, _t, info = await ticket_here(interaction)
    if not info:
        return await interaction.response.send_message("Use this inside a ticket channel.", ephemeral=True)
    if not is_official(interaction.user) and interaction.user.id != info["user"]:
        return await interaction.response.send_message("Only the person who opened it or staff can close it.",
                                                       ephemeral=True)
    await interaction.response.send_message("Closing the ticket and saving a transcript...", ephemeral=True)
    await close_ticket(interaction.guild, interaction.channel, interaction.user, reason)


# ---------------------------------------------------------------- suspensions + welcome
#
# /setupbot part:moderation makes a MODERATION category with ⛔｜suspensions (public, read-only log of every suspension)
# and 📥｜join-log (staff only: every join/leave with account age, flags brand-new accounts), plus a
# 👋｜welcome channel at the top of the server where the bot greets every new member.
# /suspend blocks a player from the ranked queue, from league activity, or times them out server-wide,
# for a set time or permanently. Suspensions lift on their own. Saved in s["mod"].

SUSPEND_SCOPES = {"queue": "Ranked queue", "league": "League (queue, teams, tournaments)",
                  "server": "Server timeout + league"}
SCOPE_LEVEL = {"queue": 1, "league": 2, "server": 3}


def mod(s: dict) -> dict:
    m = s.setdefault("mod", {})
    m.setdefault("suspensions", {})  # user id -> {scope, reason, by, start, until (iso or None), case}
    m.setdefault("history", [])
    m.setdefault("chans", {})
    m.setdefault("case", 1)
    m.setdefault("welcome_text", "")
    return m


def parse_duration(text: str) -> tuple[timedelta | None, str | None]:
    """'3d', '12h', '1w', '30m', '2d12h', 'perm' -> (timedelta or None for permanent, problem)."""
    t = (text or "").strip().lower()
    if t in ("perm", "permanent", "forever", "p"):
        return None, None
    parts = re.findall(r"(\d+)\s*(w|d|h|m)", t)
    if not parts or re.sub(r"(\d+)\s*(w|d|h|m)", "", t).strip():
        return None, "Use a length like 30m, 12h, 3d, 1w, 2d12h, or perm."
    mult = {"w": 7 * 86400, "d": 86400, "h": 3600, "m": 60}
    secs = sum(int(n) * mult[u] for n, u in parts)
    if secs <= 0:
        return None, "The length has to be more than 0."
    return timedelta(seconds=secs), None


def human(td: timedelta | None) -> str:
    if td is None:
        return "permanent"
    secs = int(td.total_seconds())
    out = []
    for name, size in (("week", 604800), ("day", 86400), ("hour", 3600), ("minute", 60)):
        n, secs = divmod(secs, size)
        if n:
            out.append(f"{n} {name}{'s' if n > 1 else ''}")
    return ", ".join(out[:2]) or "under a minute"


def sp_length(tournaments: int | None, td: timedelta | None) -> str:
    if tournaments:
        return f"{tournaments} tournament{'s' if tournaments > 1 else ''}"
    return human(td)


def sp_ends(sp: dict) -> str:
    if sp.get("tournaments"):
        n = sp.get("left", sp["tournaments"])
        return f"for {n} more tournament{'s' if n > 1 else ''}"
    if sp.get("until"):
        return f"until <t:{int(datetime.fromisoformat(sp['until']).timestamp())}:f>"
    return "permanently"


async def serve_tournament(guild: discord.Guild, tname: str):
    """A real tournament just finished: everyone on a tournament suspension has served one."""
    data = load_data()
    s = guild_signups(data, guild.id)
    done, still = [], []
    for uid, sp in mod(s)["suspensions"].items():
        if sp.get("tournaments"):
            sp["left"] = sp.get("left", sp["tournaments"]) - 1
            (done if sp["left"] <= 0 else still).append((uid, sp))
    save_data(data)
    for uid, _sp in done:
        await lift_suspension(guild, load_data(), int(uid), f"automatically (served after {tname})", "Suspension served")
    if still:
        await mod_post(guild, s, "suspensions", brand_embed("\n".join(
            f"<@{uid}> · {sp['left']} more tournament{'s' if sp['left'] > 1 else ''} · case #{sp['case']}"
            for uid, sp in still), f"{tname} is over · suspensions still running", MUTED))


def active_suspension(s: dict, uid: int) -> dict | None:
    sp = mod(s)["suspensions"].get(str(uid))
    if not sp:
        return None
    if sp.get("until") and datetime.fromisoformat(sp["until"]) <= datetime.now(timezone.utc):
        return None  # expired; the background check will tidy it up
    return sp


def suspended_from(s: dict, uid: int, need: str) -> str | None:
    """A message if the user is suspended from `need` ('queue' or 'league'), else None."""
    sp = active_suspension(s, uid)
    if not sp or SCOPE_LEVEL[sp["scope"]] < SCOPE_LEVEL[need]:
        return None
    return f"You're suspended {sp_ends(sp)} ({SUSPEND_SCOPES[sp['scope']]}). Reason: {sp['reason']}. Appeal with a ticket."


async def mod_post(guild: discord.Guild, s: dict, key: str, embed: discord.Embed):
    ch = guild.get_channel(mod(s)["chans"].get(key) or 0)
    if ch:
        await ch.send(embed=embed, allowed_mentions=NO_PINGS)


async def lift_suspension(guild: discord.Guild, data: dict, uid: int, by: str, note: str):
    s = guild_signups(data, guild.id)
    m = mod(s)
    sp = m["suspensions"].pop(str(uid), None)
    save_data(data)
    if not sp:
        return False
    r = role(guild, "Suspended")
    avatar = None
    try:
        mem = await guild.fetch_member(uid)
        avatar = mem.display_avatar.url
        if r and r in mem.roles:
            await mem.remove_roles(r, reason=note)
        if sp["scope"] == "server" and mem.is_timed_out():
            await mem.timeout(None, reason=note)
    except discord.HTTPException:
        pass
    length = sp_length(sp.get("tournaments"), None) if sp.get("tournaments") else (
        human(datetime.fromisoformat(sp["until"]) - datetime.fromisoformat(sp["start"])) if sp.get("until") else "permanent")
    e = brand_embed(f"**Player:** <@{uid}>\n**Was suspended from:** {SUSPEND_SCOPES[sp['scope']]}\n"
                    f"**Length:** {length}\n**Reason:** {sp['reason']}\n**Lifted:** {by}\n\n"
                    "They're free to join teams, sign up and queue again.",
                    f"✅ Unsuspended · Case #{sp['case']}", GOOD)
    if avatar:
        e.set_thumbnail(url=avatar)
    await mod_post(guild, s, "suspensions", e)
    try:
        u = await bot.fetch_user(uid)
        await u.send(embed=brand_embed(f"Your suspension in **{guild.name}** has ended. Welcome back!",
                                       "Suspension lifted", GOOD))
    except discord.HTTPException:
        pass
    return True


async def suspension_watch():
    """Every minute: lift suspensions whose time is up, and keep long server timeouts going."""
    await bot.wait_until_ready()
    while not bot.is_closed():
        try:
            for guild in bot.guilds:
                data = load_data()
                s = guild_signups(data, guild.id)
                now = datetime.now(timezone.utc)
                for uid, sp in list(mod(s)["suspensions"].items()):
                    until = datetime.fromisoformat(sp["until"]) if sp.get("until") else None
                    if until and until <= now:
                        await lift_suspension(guild, data, int(uid), "automatically (time served)", "Suspension ended")
                        data = load_data()
                    elif sp["scope"] == "server":
                        # Discord timeouts last at most 28 days, so re-apply for long or permanent ones
                        try:
                            mem = guild.get_member(int(uid))
                            if mem and not mem.is_timed_out():
                                end = min(until or now + timedelta(days=27), now + timedelta(days=27))
                                await mem.timeout(end, reason=f"Suspension case #{sp['case']}")
                        except discord.HTTPException:
                            pass
        except Exception as e:  # keep watching even if one pass fails
            print(f"[suspensions] {e}")
        await asyncio.sleep(60)


# What a player can be suspended for. "doe": only the Director of Enforcement (and Commissioner+) can use it.
# Everything else League Staff can use too.
SUSPEND_REASONS = {
    "hacks": ("Hacks / exploits", True),
    "alting": ("Alting / account sharing", True),
    "throwing": ("Throwing games", False),
    "threats": ("Threats", False),
    "toxicity": ("Discord: toxicity / harassment", False),
    "spam": ("Discord: spam / advertising", False),
    "nsfw": ("Discord: NSFW / inappropriate content", False),
    "discord": ("Discord: other rule break", False),
}


def can_suspend_for(member, cat: str) -> bool:
    return is_enforcer(member) if SUSPEND_REASONS.get(cat, ("", True))[1] else is_staff(member)


@bot.tree.command(description="Staff: suspend a player for tournaments or a set time (pick the reason from the list).")
@app_commands.describe(member="Who to suspend",
                       reason="What for. Hacks/exploits and alting/account sharing: Director of Enforcement only",
                       details="Extra info (optional): what happened, clip link, etc.",
                       tournaments="How many tournaments they sit out (the current/next one counts as the first)",
                       length="Or a set time instead: 30m, 12h, 3d, 1w, 2d12h, or perm",
                       scope="What they're blocked from (tournament suspensions are always at least League)")
@app_commands.choices(scope=[app_commands.Choice(name="Ranked queue only", value="queue"),
                             app_commands.Choice(name="League: queue, teams, tournaments", value="league"),
                             app_commands.Choice(name="Server timeout (can't chat) + league", value="server")],
                      reason=[app_commands.Choice(name=lbl + (" (Director of Enforcement)" if doe else ""), value=k)
                              for k, (lbl, doe) in SUSPEND_REASONS.items()])
@app_commands.default_permissions(moderate_members=True)
async def suspend(interaction: discord.Interaction, member: discord.Member, reason: str,
                  tournaments: app_commands.Range[int, 1, 10] | None = None, length: str | None = None,
                  scope: str = "league", details: str | None = None):
    cat = reason
    if cat not in SUSPEND_REASONS:
        return await interaction.response.send_message("Pick a reason from the list.", ephemeral=True)
    if not can_suspend_for(interaction.user, cat):
        if not is_staff(interaction.user):
            return await interaction.response.send_message("Only league staff can suspend players.", ephemeral=True)
        return await interaction.response.send_message(
            f"Only the **Director of Enforcement** or the Commissioner can suspend for **{SUSPEND_REASONS[cat][0]}**. "
            "Send them the details (or open a ticket).", ephemeral=True)
    reason = SUSPEND_REASONS[cat][0] + (f": {details.strip()}" if details and details.strip() else "")
    if member.bot or member.id == interaction.user.id:
        return await interaction.response.send_message("You can't suspend that account.", ephemeral=True)
    if tournaments and length:
        return await interaction.response.send_message("Pick either `tournaments` or `length`, not both.",
                                                       ephemeral=True)
    if not tournaments and not length:
        return await interaction.response.send_message("Say how long: `tournaments` (e.g. 2) or `length` "
                                                       "(e.g. 3d or perm).", ephemeral=True)
    td, problem = (None, None) if tournaments else parse_duration(length)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    if tournaments and scope == "queue":
        scope = "league"  # sitting out tournaments means no teams and no sign-ups
    await interaction.response.defer(ephemeral=True)
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    m = mod(s)
    now = datetime.now(timezone.utc)
    until = now + td if td else None
    case = m["case"]
    m["case"] += 1
    m["suspensions"][str(member.id)] = {"scope": scope, "reason": reason[:300], "cat": cat, "by": interaction.user.id,
                                        "start": now.isoformat(timespec="seconds"),
                                        "until": until.isoformat(timespec="seconds") if until else None,
                                        "tournaments": tournaments, "left": tournaments, "case": case}
    m["history"].append({"user": member.id, "scope": scope, "reason": reason[:300], "cat": cat, "by": interaction.user.id,
                         "start": now.isoformat(timespec="seconds"), "length": sp_length(tournaments, td),
                         "case": case})
    # take them out of the queue if they're in it
    p = pug(s)
    if member.id in p["queue"]:
        p["queue"].remove(member.id)
        p["qpos"].pop(str(member.id), None)
    save_data(data)

    r = role(guild, "Suspended")
    if r is None:
        try:
            r = await guild.create_role(name="Suspended", colour=discord.Colour(0x52525B), reason="Suspensions")
        except discord.HTTPException:
            r = None
    try:
        if r:
            await member.add_roles(r, reason=f"Case #{case}: {reason}")
        if scope == "server":
            await member.timeout(min(until or now + timedelta(days=27), now + timedelta(days=27)),
                                 reason=f"Case #{case}: {reason}")
    except discord.HTTPException:
        pass
    tz = s.get("tourney")
    ends = (f"after {tournaments} more tournament{'s' if tournaments > 1 else ''} finish"
            + (f" (starting with **{tz['name']}**)" if tz else "") if tournaments else
            f"<t:{int(until.timestamp())}:f> (<t:{int(until.timestamp())}:R>)" if until else "never (permanent)")
    on_team = team_of(s, member.id)
    team_note = (f"\n**Team:** still on **{s['teams'][on_team]['name']}** but can't play for them until it ends."
                 if on_team else "")
    e = brand_embed(f"**Player:** {member.mention}\n**Suspended from:** {SUSPEND_SCOPES[scope]}\n"
                    f"**Length:** {sp_length(tournaments, td)}\n**Ends:** {ends}{team_note}\n**Reason:** {reason}\n**By:** {interaction.user.mention}",
                    f"⛔ Suspension · Case #{case}", BRAND)
    e.set_thumbnail(url=member.display_avatar.url)
    await mod_post(guild, s, "suspensions", e)
    try:
        await member.send(embed=brand_embed(
            f"You've been suspended in **{guild.name}**.\n**From:** {SUSPEND_SCOPES[scope]}\n"
            f"**Length:** {sp_length(tournaments, td)}\n**Ends:** {ends}\n**Reason:** {reason}\n\n"
            "While suspended you can't create, join or be signed to a team, register for tournaments or play in "
            "them.\n\nTo appeal, open an **Appeal** ticket in the server.",
            f"Suspension · Case #{case}", BRAND))
    except discord.HTTPException:
        pass
    await refresh_queue(guild, data)
    await interaction.followup.send(f"{member.mention} is suspended ({sp_length(tournaments, td)}, {SUSPEND_SCOPES[scope]}). "
                                    f"Case #{case}.", ephemeral=True, allowed_mentions=NO_PINGS)


@app_commands.describe(member="Who to unsuspend")
@app_commands.default_permissions(moderate_members=True)
async def unsuspend(interaction: discord.Interaction, member: discord.Member):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    cur = mod(guild_signups(load_data(), interaction.guild.id))["suspensions"].get(str(member.id)) or {}
    cat = cur.get("cat")
    if cur and not (can_suspend_for(interaction.user, cat) if cat else is_enforcer(interaction.user)):
        return await interaction.response.send_message(
            f"This suspension is for **{SUSPEND_REASONS.get(cat, ('an enforcement reason',))[0]}**. Only the "
            "Director of Enforcement or the Commissioner can lift it.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    ok = await lift_suspension(interaction.guild, load_data(), member.id, interaction.user.mention, "Lifted early")
    await interaction.followup.send(f"Lifted {member.mention}'s suspension." if ok else
                                    f"{member.mention} isn't suspended.", ephemeral=True, allowed_mentions=NO_PINGS)


@app_commands.describe(member="Show this player's full suspension history (optional)")
@app_commands.default_permissions(moderate_members=True)
async def suspensions(interaction: discord.Interaction, member: discord.Member | None = None):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only staff can do that.", ephemeral=True)
    m = mod(guild_signups(load_data(), interaction.guild.id))
    if member:
        rows = [h for h in m["history"] if h["user"] == member.id]
        text = "\n".join(f"#{h['case']} · {h['start'][:10]} · {h['length']} · {SUSPEND_SCOPES[h['scope']]} · {h['reason']}"
                         for h in rows[-15:]) or "No suspensions on record."
        return await interaction.response.send_message(embed=brand_embed(text, f"{member.display_name}: history", MUTED),
                                                       ephemeral=True)
    rows = []
    for uid, sp in m["suspensions"].items():
        rows.append(f"#{sp['case']} <@{uid}> · {SUSPEND_SCOPES[sp['scope']]} · {sp_ends(sp)} · {sp['reason']}")
    await interaction.response.send_message(embed=brand_embed("\n".join(rows) or "Nobody is suspended.",
                                                              "Current suspensions", MUTED), ephemeral=True)


# ---- welcome + join log

def welcome_card(member: discord.Member, s: dict) -> discord.Embed:
    m = mod(s)
    custom = m.get("welcome_text") or ""
    links = []
    for name in ("rules", "welcome", "get-roles", "announcements"):
        ch = discord.utils.get(member.guild.text_channels, name=name)
        if ch and name != "welcome":
            links.append(ch.mention)
    p = pug(s)
    q = pug_ch(member.guild, p, "queue")
    lines = [f"Hey {member.mention}, welcome to **{member.guild.name}**! You're member **#{member.guild.member_count}**."]
    if custom:
        lines += ["", custom]
    lines += ["", "**Get started**",
              f"• Read the rules{(' in ' + links[0]) if links else ''}",
              "• Start a team with `/signup`, or `/freeagent` to get found by captains",
              f"• Play ranked pickups{(' in ' + q.mention) if q else ''}: pick your position and join the queue",
              "• Need help? Open a ticket"]
    e = brand_embed("\n".join(lines), f"Welcome to {LEAGUE_NAME}!", GOLD)
    e.set_thumbnail(url=member.display_avatar.url)
    return e


@bot.listen("on_member_join")
async def welcome_new_member(member: discord.Member):
    if member.bot:
        return
    data = load_data()
    s = guild_signups(data, member.guild.id)
    m = mod(s)
    ch = member.guild.get_channel(m["chans"].get("welcome") or 0)
    if ch:
        try:
            await ch.send(content=member.mention, embed=welcome_card(member, s),
                          allowed_mentions=discord.AllowedMentions(users=True))
        except discord.HTTPException:
            pass
    age = datetime.now(timezone.utc) - member.created_at
    flag = " ⚠️ **NEW ACCOUNT**" if age < timedelta(days=7) else ""
    sp = active_suspension(s, member.id)
    note = f"\n⛔ **Rejoined while suspended** (case #{sp['case']})" if sp else ""
    e = brand_embed(f"{member.mention} · `{member}` · ID {member.id}\n**Account created:** "
                    f"<t:{int(member.created_at.timestamp())}:D> ({human(age)} ago){flag}{note}\n"
                    f"**Members now:** {member.guild.member_count}", "📥 Member joined", GOOD)
    e.set_thumbnail(url=member.display_avatar.url)
    await mod_post(member.guild, s, "joinlog", e)
    if sp:  # put the suspension back on if they left and rejoined to dodge it
        r = role(member.guild, "Suspended")
        try:
            if r:
                await member.add_roles(r, reason="Rejoined while suspended")
        except discord.HTTPException:
            pass


@bot.listen("on_member_remove")
async def log_member_leave(member: discord.Member):
    s = guild_signups(load_data(), member.guild.id)
    joined = f"<t:{int(member.joined_at.timestamp())}:R>" if member.joined_at else "unknown"
    team = team_of(s, member.id)
    extra = f"\n**Was on:** {s['teams'][team]['name']}" if team else ""
    await mod_post(member.guild, s, "joinlog", brand_embed(
        f"{member.mention} · `{member}` · ID {member.id}\n**Joined:** {joined}{extra}\n"
        f"**Members now:** {member.guild.member_count}", "📤 Member left", MUTED))


async def release_gone_player(guild: discord.Guild, uid: int, label: str | None = None) -> str | None:
    """Someone left the server: take them off their team, the free agent list, open offers and the queue."""
    data = load_data()
    s = guild_signups(data, guild.id)
    note = None
    key = team_of(s, uid)
    if uid in s["free_agents"]:
        s["free_agents"].remove(uid)
    for oid in [k for k, o in s.get("offers", {}).items() if o.get("player") == uid]:
        s["offers"].pop(oid, None)
    p = pug(s)
    if uid in p.get("queue", []):
        p["queue"].remove(uid)
        p.get("qpos", {}).pop(str(uid), None)
    save_data(data)
    if key:
        note = await remove_member(guild, data, key, uid, "left the server, so they were released from")
    return note


@bot.listen("on_member_remove")
async def release_on_leave(member: discord.Member):
    """Leaving the server = released from your team automatically (captaincy passes on, like /leaveteam)."""
    if member.bot:
        return
    await asyncio.sleep(2)  # let the other leave handlers (join log, invite tracker) save first
    try:
        if await release_gone_player(member.guild, member.id) is not None:
            await update_board(member.guild)
    except Exception as e:
        print(f"[release on leave] {e}")


async def sweep_gone_players(guild: discord.Guild) -> int:
    """On startup: anyone on a roster who isn't in the server any more (left while the bot was off) is released.
    Each one is double-checked with Discord first, so a slow member list never releases someone by mistake."""
    s = guild_signups(load_data(), guild.id)
    suspects = {int(u) for _k, t in s["teams"].items() for u in t.get("roster", {}) if guild.get_member(int(u)) is None}
    gone = 0
    for uid in suspects:
        try:
            await guild.fetch_member(uid)
            continue  # still here
        except discord.NotFound:
            pass
        except discord.HTTPException:
            continue  # Discord hiccup: leave them for next time
        if await release_gone_player(guild, uid) is not None:
            gone += 1
        await asyncio.sleep(0.5)
    if gone:
        await update_board(guild)
        print(f"[{guild.name}] Released {gone} player(s) who had left the server.")
    return gone


# one-time setup: run with /setupbot part:moderation
async def modsetup(interaction: discord.Interaction, welcome_message: str | None = None):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    m = mod(s)
    if welcome_message is not None:
        m["welcome_text"] = welcome_message[:500]
    c = m["chans"]
    welcome_cat = await get_or_make_category(guild, "WELCOME")
    if not guild.get_channel(c.get("welcome") or 0) and chan(guild, "welcome"):
        c["welcome"] = chan(guild, "welcome").id  # use the welcome channel the server already has
        try:
            await chan(guild, "welcome").edit(name="👋｜welcome")
        except discord.HTTPException:
            pass
    if not guild.get_channel(c.get("welcome") or 0):
        ch = await guild.create_text_channel("👋｜welcome", category=welcome_cat, position=0,
                                             overwrites=overwrites_for(guild, "ro"))
        c["welcome"] = ch.id
    modcat = guild.get_channel(c.get("category") or 0) or discord.utils.get(guild.categories, name="MODERATION") \
        or await guild.create_category("MODERATION")
    c["category"] = modcat.id
    if not guild.get_channel(c.get("suspensions") or 0):
        ch = await guild.create_text_channel("⛔｜suspensions", category=modcat, overwrites=overwrites_for(guild, "ro"))
        c["suspensions"] = ch.id
        await post(ch, "Every suspension is posted here with the reason, length and when it ends. Suspensions lift "
                       "on their own when time is up.\n\n**Ranked queue:** can't join pickups.\n**League:** can't "
                       "join the queue, sign up or join a team, register for tournaments or be a free agent.\n"
                       "**Server timeout:** can't chat at all, plus the league block.\n\nThink a suspension is "
                       "wrong? Open an **Appeal** ticket.", title="Suspensions", color=BRAND)
    if not guild.get_channel(c.get("joinlog") or 0):
        ch = await guild.create_text_channel("📥｜join-log", category=modcat, overwrites=overwrites_for(guild, "staff"))
        c["joinlog"] = ch.id
    if role(guild, "Suspended") is None:
        try:
            await guild.create_role(name="Suspended", colour=discord.Colour(0x52525B), reason="Suspensions")
        except discord.HTTPException:
            pass
    save_data(data)
    # show staff what a welcome looks like
    preview = welcome_card(interaction.user, s)
    await interaction.followup.send(
        f"Done: <#{c['welcome']}> greets every new member, <#{c['joinlog']}> (staff only) logs joins and leaves "
        f"with account age, and <#{c['suspensions']}> logs suspensions. Here's what a welcome looks like:",
        embed=preview, ephemeral=True)


# ---------------------------------------------------------------- media
#
# /setupbot part:media makes a MEDIA category:
#   📌｜media-info       how media works, who can post where, the Stream Pings button
#   📊｜stat-leaders     bot-only: tournament + season leaders and ranked leaders, kept up to date
#   🔴｜live-now         Media/Streamer: /golive posts a "LIVE" card and pings people who opted in
#   🎙️｜media-shows      Media: podcasts, personal shows, recaps, interviews
#   📰｜power-rankings   Media + staff: weekly rankings, previews, articles
#   🎬｜highlights       everyone: clips and plays (the old #highlights moves here)
#   🎨｜edits-and-gfx    everyone: edits, thumbnails, graphics
#   💬｜media-chat       Media/Streamer: talk to each other, plan collabs
#   🎙️ Media Booth      voice, Media/Streamer can talk, everyone can listen
# Roles: Media (content creators), Streamer, Stream Pings (opt-in notifications).

MEDIA_ROLES = [("Media", 0xA855F7), ("Streamer", 0x9146FF), ("Stream Pings", 0x6B7280)]
LEADER_STATS = [("pts", "Points", "PPG"), ("reb", "Rebounds", "RPG"), ("ast", "Assists", "APG"),
                ("stl", "Steals", "SPG"), ("blk", "Blocks", "BPG"), ("fg3m", "3-pointers", "3PM")]


def media(s: dict) -> dict:
    m = s.setdefault("media", {})
    m.setdefault("chans", {})
    m.setdefault("leaders_msgs", [])
    return m


def leader_tables(guild: discord.Guild, s: dict) -> tuple[dict, dict, str]:
    def name(tid):
        t = s["teams"].get(str(tid))
        return t["name"] if t else "—"

    def player(uid):
        mem = guild.get_member(int(uid)) if str(uid).isdigit() else None
        return mem.mention if mem else str(uid)

    current = player_totals(s.get("event"), player, name)
    year = datetime.now().year
    past = [h["players"] for h in s.get("history", []) if h.get("year") == year]
    tz = s.get("tourney")
    return current, merge_totals(*past, current), (tz["name"] if tz else "Current tournament")


def leaders_embed(table: dict, title: str, color: int, min_gp: int = 1, logos: dict | None = None) -> discord.Embed:
    logos = logos or {}
    rows = [dict(r, player=logos.get(r.get("team"), "") + r["player"]) for r in table.values() if r["gp"] >= min_gp]
    e = brand_embed(None if rows else "No stats entered yet.", title, color)
    for key, label, short in LEADER_STATS:
        top = sorted(rows, key=lambda r: -(r[key] / r["gp"]))[:5]
        if top:
            e.add_field(name=f"{label} ({short})", inline=True, value="\n".join(
                f"{'🥇🥈🥉'[i] if i < 3 else f'`{i + 1}.`'} {r['player']} **{r[key] / r['gp']:.1f}**"
                for i, r in enumerate(top)))
    shooters = [r for r in rows if r["fg2a"] + r["fg3a"] >= 10]
    if shooters:
        top = sorted(shooters, key=lambda r: -((r["fg2m"] + r["fg3m"]) / (r["fg2a"] + r["fg3a"])))[:5]
        e.add_field(name="Field goal % (10+ shots)", inline=True, value="\n".join(
            f"`{i + 1}.` {r['player']} **{100 * (r['fg2m'] + r['fg3m']) / (r['fg2a'] + r['fg3a']):.0f}%**"
            for i, r in enumerate(top)))
    return e


def ranked_leaders_embed(s: dict) -> discord.Embed:
    p = pug(s)
    placed = [(k, v) for k, v in p["players"].items() if is_placed(v)]
    e = brand_embed(None if placed else "Nobody has finished placements yet.", "Ranked leaders", INFO)
    if placed:
        top = sorted(placed, key=lambda kv: -kv[1]["rr"])[:5]
        e.add_field(name="Highest RR", inline=True, value="\n".join(
            f"`{i + 1}.` {player_team_emoji(s, k)}<@{k}> **{int(v['rr'])}** {rank_of(v['rr'])[0]}"
            for i, (k, v) in enumerate(top)))
        wins = sorted(placed, key=lambda kv: -kv[1]["w"])[:5]
        e.add_field(name="Most wins", inline=True, value="\n".join(
            f"`{i + 1}.` {player_team_emoji(s, k)}<@{k}> **{v['w']}W**-{v['l']}L" for i, (k, v) in enumerate(wins)))
        hot = sorted((kv for kv in placed if kv[1].get("streak", 0) >= 2), key=lambda kv: -kv[1]["streak"])[:5]
        if hot:
            e.add_field(name="Hottest streaks", inline=True, value="\n".join(
                f"🔥 {player_team_emoji(s, k)}<@{k}> **{v['streak']}W**" for k, v in hot))
    return e


async def refresh_leaders(guild: discord.Guild, data: dict | None = None):
    """Edit the stat-leaders cards in place (or post them if they're gone)."""
    data = data or load_data()
    s = guild_signups(data, guild.id)
    md = media(s)
    ch = guild.get_channel(md["chans"].get("leaders") or 0)
    if ch is None:
        return
    current, year, tname = leader_tables(guild, s)
    logos = emoji_by_team_name(s)  # team logo emoji left of each player
    cards = [leaders_embed(current, f"{tname}: stat leaders (per game)", GOLD, logos=logos),
             leaders_embed(year, f"{datetime.now().year} season leaders (per game, 2+ games)", BRAND, min_gp=2,
                           logos=logos),
             ranked_leaders_embed(s)]
    url = site_url()
    if url:
        cards[-1].description = (cards[-1].description or "") + f"\nFull stats: {url}#stats"
    msgs = md["leaders_msgs"]
    for i, card in enumerate(cards):
        try:
            if i < len(msgs):
                await (await ch.fetch_message(msgs[i])).edit(embed=card)
                continue
        except discord.HTTPException:
            pass
        sent = await ch.send(embed=card, allowed_mentions=NO_PINGS)
        msgs[i:i + 1] = [sent.id]
    save_data(data)


async def leaders_watch():
    """Refresh stat leaders every 30 minutes, so imports and pickups show up without anyone asking."""
    await bot.wait_until_ready()
    while not bot.is_closed():
        await asyncio.sleep(1800)
        for guild in bot.guilds:
            try:
                await refresh_leaders(guild)
            except Exception as e:
                print(f"[stat leaders] {e}")


class MediaInfoView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Stream Pings on/off", emoji="🔔", style=discord.ButtonStyle.primary,
                                        custom_id="med:pings"))
        self.add_item(discord.ui.Button(label="Apply for Media", emoji="🎥", style=discord.ButtonStyle.secondary,
                                        custom_id="med:apply"))


def media_info_cards(guild: discord.Guild, c: dict) -> list[discord.Embed]:
    def at(k):
        return f"<#{c[k]}>" if c.get(k) else k
    where = brand_embed("\n".join([
        f"{at('leaders')} Stat leaders and ranked leaders, updated by the bot automatically.",
        f"{at('live')} Streaming PB? Use `/golive` with your link. Media and Streamer roles only.",
        f"{at('report')} **The OTR Report**: the league's media show. Episodes, podcasts, recaps, interviews and "
        "breakdowns (Media role).",
        f"{at('yt')} Official highlight videos posted to YouTube (Media role).",
        f"{at('gfx')} Official league graphics: matchups, results, announcements (Media + staff).",
        f"{at('rankings')} Power rankings: posted automatically after each stage (top 8), plus previews "
        "and articles (Media + staff).",
        f"{at('analysis')} A written breakdown of every game with stats: who starred, who struggled (automatic).",
        f"{at('highlights')} Everyone: post your clips and best plays.",
        f"{at('edits')} Everyone: edits, thumbnails and graphics.",
        f"{at('chat')} Media and streamers: plan collabs and coverage.",
        "**🎙️ Media Booth** voice: Media and Streamers talk, everyone can listen in.",
    ]), "Media channels", BRAND)
    roles = brand_embed("\n".join([
        "**Media** — content creators who cover the circuit: the OTR Report, recaps, rankings, interviews.",
        "**Streamer** — you stream PB circuit games or ranked. Lets you use `/golive`.",
        "**Stream Pings** — get notified when someone goes live. Toggle it with the button below.",
        "",
        "**How to get Media or Streamer:** click **Apply for Media** (or open a Media ticket) with links "
        "to your channel or past content. Staff will review it.",
    ]), "Media roles", GOLD)
    rules = brand_embed("\n".join([
        "1. Keep it about PB and the circuit. No unrelated self-promo.",
        "2. Credit other people's clips and edits.",
        "3. No leaking private server codes on stream. Use a delay in pickups if you can.",
        "4. Stats you quote should match the official box scores and the website.",
        "5. Banter is fine. Harassing players or teams isn't, and costs you the role.",
        "6. Staff can remove posts or roles that break these rules.",
    ]), "Media rules", MUTED)
    return [where, roles, rules]


# one-time setup: run with /setupbot part:media
async def mediasetup(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    for name, color in MEDIA_ROLES:
        if role(guild, name) is None:
            try:
                await guild.create_role(name=name, colour=discord.Colour(color), mentionable=name == "Stream Pings",
                                        reason="Media setup")
            except discord.HTTPException:
                pass
    try:
        await lock_everyone_pings(guild)
    except Exception as e:
        print(f"[everyone pings] {e}")
    data = load_data()
    s = guild_signups(data, guild.id)
    c = media(s)["chans"]
    cat = guild.get_channel(c.get("category") or 0) or discord.utils.get(guild.categories, name="MEDIA") \
        or await guild.create_category("MEDIA")
    c["category"] = cat.id
    wanted = [("info", "📌｜media-info", "ro"), ("leaders", "📊｜stat-leaders", "ro"),
              ("live", "🔴｜live-now", ["Media", "Streamer"]), ("report", "📰｜otr-report", ["Media"]),
              ("shows", "🎙️｜media-shows", ["Media"]), ("yt", "▶️｜yt-highlights", ["Media"]),
              ("gfx", "🖼️｜official-gfx", ["Media"]),
              ("rankings", "📰｜power-rankings", ["Media"]), ("analysis", "🧠｜game-analysis", ["Media"]), ("highlights", "🎬｜highlights", "open"),
              ("edits", "🎨｜edits-and-gfx", "open"), ("chat", "💬｜media-chat", None)]
    for key, name, access in wanted:
        ch = guild.get_channel(c.get(key) or 0)
        if ch is None and key == "highlights":
            ch = chan(guild, "highlights")  # move the existing highlights channel instead of making a second one
            if ch:
                try:
                    await ch.edit(name=name, category=cat)
                except discord.HTTPException:
                    pass
        if ch is None:
            if access is None:  # media-chat: only Media, Streamer and staff can see it
                ow = overwrites_for(guild, "staff")
                for rn in ("Media", "Streamer"):
                    r = role(guild, rn)
                    if r:
                        ow[r] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
            else:
                ow = overwrites_for(guild, access)
            ch = await guild.create_text_channel(name, category=cat, overwrites=ow)
        c[key] = ch.id
    if not guild.get_channel(c.get("booth") or 0):
        ow = {guild.default_role: discord.PermissionOverwrite(connect=True, speak=False)}
        for rn in ("Media", "Streamer", "League Staff"):
            r = role(guild, rn)
            if r:
                ow[r] = discord.PermissionOverwrite(connect=True, speak=True)
        c["booth"] = (await guild.create_voice_channel("🎙️ Media Booth", category=cat, overwrites=ow)).id
    save_data(data)

    info = guild.get_channel(c["info"])
    try:
        async for msg in info.history(limit=20):
            if msg.author.id == guild.me.id:
                await msg.delete()
    except discord.HTTPException:
        pass
    cards = media_info_cards(guild, c)
    for e in cards[:-1]:
        await info.send(embed=e)
    await info.send(embed=cards[-1], view=MediaInfoView())
    await refresh_leaders(guild, data)
    await interaction.followup.send(
        f"MEDIA is set up. Stat leaders are live in <#{c['leaders']}> and refresh every 30 minutes "
        f"(or `/refresh what:leaders`). Give creators the **Media** or **Streamer** role so they can post shows and "
        "use `/golive`.", ephemeral=True)


async def statleaders(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await refresh_leaders(interaction.guild)
    c = media(guild_signups(load_data(), interaction.guild.id))["chans"]
    await interaction.followup.send(f"Updated <#{c['leaders']}>." if c.get("leaders") else
                                    "Run /setupbot part:media first.", ephemeral=True)


@bot.tree.command(description="Media/Streamers: announce that you're live, with your stream link.")
@app_commands.describe(link="Your stream link (Twitch, YouTube, TikTok, Kick...)",
                       title="What you're streaming, e.g. 'Ranked grind' or 'Week 3 watch party'")
async def golive(interaction: discord.Interaction, link: str, title: str = "Live now"):
    user = interaction.user
    if not (is_staff(user) or any(r.name in ("Media", "Streamer") for r in user.roles)):
        return await interaction.response.send_message("You need the Media or Streamer role. Click **Apply for "
                                                       "Media** in the media info channel.", ephemeral=True)
    if not re.match(r"^https?://\S+$", link.strip()):
        return await interaction.response.send_message("That doesn't look like a link. Paste the full https:// URL.",
                                                       ephemeral=True)
    s = guild_signups(load_data(), interaction.guild.id)
    ch = interaction.guild.get_channel(media(s)["chans"].get("live") or 0)
    if ch is None:
        return await interaction.response.send_message("Staff need to run /setupbot part:media first.", ephemeral=True)
    host = re.sub(r"^https?://(www\.)?", "", link).split("/")[0]
    e = brand_embed(f"{user.mention} is streaming **{title[:100]}**\n\n▶ **[Watch on {host}]({link.strip()})**",
                    "🔴 LIVE NOW", 0xEF4444, url=link.strip())
    e.set_thumbnail(url=user.display_avatar.url)
    pings = role(interaction.guild, "Stream Pings")
    view = discord.ui.View()
    view.add_item(discord.ui.Button(label="Watch", emoji="▶", url=link.strip()))
    await ch.send(content=pings.mention if pings else None, embed=e, view=view,
                  allowed_mentions=discord.AllowedMentions(roles=True, users=False, everyone=False))
    await interaction.response.send_message(f"Posted in {ch.mention}. Have a good stream!", ephemeral=True)


@app_commands.describe(member="Who", kind="Which role", remove="Take it away instead")
@app_commands.choices(kind=[app_commands.Choice(name="Media", value="Media"),
                            app_commands.Choice(name="Streamer", value="Streamer")])
@app_commands.default_permissions(manage_roles=True)
async def mediarole(interaction: discord.Interaction, member: discord.Member, kind: str, remove: bool = False):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    r = role(interaction.guild, kind)
    if r is None:
        return await interaction.response.send_message("Run /setupbot part:media first.", ephemeral=True)
    try:
        await (member.remove_roles if remove else member.add_roles)(r, reason=f"By {interaction.user}")
    except discord.HTTPException:
        return await interaction.response.send_message("I couldn't change that role. Is my role above it?",
                                                       ephemeral=True)
    await interaction.response.send_message(f"{'Removed' if remove else 'Gave'} **{kind}** "
                                            f"{'from' if remove else 'to'} {member.mention}.", ephemeral=True,
                                            allowed_mentions=NO_PINGS)


@bot.listen("on_interaction")
async def media_buttons(interaction: discord.Interaction):
    cid = (interaction.data or {}).get("custom_id", "") if interaction.type == discord.InteractionType.component else ""
    if not cid.startswith("med:"):
        return
    if cid == "med:pings":
        r = role(interaction.guild, "Stream Pings")
        if r is None:
            return await interaction.response.send_message("Stream Pings isn't set up.", ephemeral=True)
        on = r not in interaction.user.roles
        try:
            await (interaction.user.add_roles if on else interaction.user.remove_roles)(r, reason="Stream Pings toggle")
        except discord.HTTPException:
            return await interaction.response.send_message("I couldn't change your roles.", ephemeral=True)
        await interaction.response.send_message("🔔 You'll be pinged when someone goes live." if on else
                                                "🔕 Stream Pings off.", ephemeral=True)
    elif cid == "med:apply":
        await interaction.response.send_modal(ApplyModal("media"))


# ---------------------------------------------------------------- /apply: apply for a league role
#
# /apply role:<Media / Streamer / Referee / Arena Host / Pickup Host / League Staff>
# A short form, then an application card in 📝｜applications (staff only) with Accept / Deny.
# League Staff can only be approved by the Commissioner (or an admin);
# the rest by any staff member. Accepted = the role is given and the applicant gets a DM.

APPLY_ROLES = {"media": ("Media", "🎥"), "streamer": ("Streamer", "📺"), "referee": ("Referee", "🦓"),
               "host": ("Arena Host", "🎮"), "pickup": ("Pickup Host", "🏀"), "staff": ("League Staff", "🛡️")}
# Commissioner and Director of Enforcement are appointed, never applied for.
APPLY_TOP = {"staff"}  # Commissioner+ approves these
APPLY_COOLDOWN = timedelta(days=7)  # after a denied application for the same role


def applications(s: dict) -> dict:
    return s.setdefault("applications", {})  # id -> {user, role, answers, status, at, by}


class ApplyModal(discord.ui.Modal):
    def __init__(self, key: str):
        name, _icon = APPLY_ROLES[key]
        super().__init__(title=f"Apply: {name}"[:45], timeout=900)
        self.key = key
        self.why = discord.ui.TextInput(label=f"Why do you want {name}?"[:45], style=discord.TextStyle.paragraph,
                                        max_length=600)
        self.exp = discord.ui.TextInput(label="Relevant experience", style=discord.TextStyle.paragraph,
                                        max_length=600, placeholder="Other leagues, roles you've had, what you're good at")
        self.avail = discord.ui.TextInput(label="When are you usually available?", max_length=200,
                                          placeholder="e.g. weeknights 7-11 PM ET, weekends")
        self.links = discord.ui.TextInput(label="Links (channel, past work)", required=key in ("media", "streamer"),
                                          max_length=400, style=discord.TextStyle.paragraph,
                                          placeholder="YouTube / Twitch / TikTok / portfolio" if key in ("media", "streamer")
                                          else "Optional")
        for x in (self.why, self.exp, self.avail, self.links):
            self.add_item(x)

    async def on_submit(self, interaction: discord.Interaction):
        await submit_application(interaction, self.key, {"Why": str(self.why), "Experience": str(self.exp),
                                                         "Availability": str(self.avail), "Links": str(self.links)})


def apply_problem(guild: discord.Guild, s: dict, member, key: str) -> str | None:
    name = APPLY_ROLES[key][0]
    if any(r.name == name for r in getattr(member, "roles", [])):
        return f"You already have **{name}**."
    now = datetime.now(timezone.utc)
    for a in applications(s).values():
        if a["user"] == member.id and a["role"] == key:
            if a["status"] == "open":
                return f"You already have a **{name}** application waiting for staff."
            if a["status"] == "denied" and now - datetime.fromisoformat(a.get("decided") or a["at"]) < APPLY_COOLDOWN:
                again = datetime.fromisoformat(a.get("decided") or a["at"]) + APPLY_COOLDOWN
                return f"Your last **{name}** application was declined. You can apply again {ts(again, 'R')}."
    if suspended_from(s, member.id, "league"):
        return "You can't apply while you're suspended."
    return None


async def applications_channel(guild: discord.Guild):
    ch = discord.utils.get(guild.text_channels, name="📝｜applications") or chan(guild, "applications")
    if ch is None:
        try:
            cat = discord.utils.get(guild.categories, name="STAFF") or await get_or_make_category(
                guild, "STAFF", overwrites_for(guild, "staff"))
            ch = await guild.create_text_channel("📝｜applications", category=cat, overwrites=overwrites_for(guild, "staff"),
                                                 topic="Role applications from /apply. Accept or deny with the buttons.")
        except discord.HTTPException:
            return None
    return ch


async def submit_application(interaction: discord.Interaction, key: str, answers: dict):
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    problem = apply_problem(guild, s, user, key)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    ch = await applications_channel(guild)
    if ch is None:
        return await interaction.response.send_message("Applications aren't set up yet. Ask staff.", ephemeral=True)
    name, icon = APPLY_ROLES[key]
    aid = secrets.token_hex(4)
    applications(s)[aid] = {"user": user.id, "role": key, "answers": answers, "status": "open",
                            "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    save_data(data)
    team = team_of(s, user.id)
    joined = f"<t:{int(user.joined_at.timestamp())}:R>" if getattr(user, "joined_at", None) else "unknown"
    e = brand_embed(f"{user.mention} · `{user}`\n**Joined the server:** {joined}"
                    + (f"\n**Team:** {s['teams'][team]['name']}" if team else "")
                    + ("\n*Commissioner or admin approval needed.*" if key in APPLY_TOP else ""),
                    f"{icon} Application: {name}", GOLD)
    for k, v in answers.items():
        if v and v.strip():
            e.add_field(name=k, value=v[:1000], inline=False)
    try:
        e.set_thumbnail(url=user.display_avatar.url)
    except AttributeError:
        pass
    v = discord.ui.View(timeout=None)
    v.add_item(discord.ui.Button(label="Accept", emoji="✅", style=discord.ButtonStyle.success,
                                 custom_id=f"app:ok:{guild.id}:{aid}"))
    v.add_item(discord.ui.Button(label="Deny", emoji="✖", style=discord.ButtonStyle.danger,
                                 custom_id=f"app:no:{guild.id}:{aid}"))
    msg = await ch.send(embed=e, view=v, allowed_mentions=NO_PINGS)
    applications(s)[aid]["msg"] = [ch.id, msg.id]
    save_data(data)
    await interaction.response.send_message(f"Your **{name}** application was sent to staff. You'll get a DM when "
                                            "they decide.", ephemeral=True)


@bot.tree.command(description="Apply for a league role: Media, Streamer, Referee, Arena Host, Pickup Host or staff.")
@app_commands.describe(role="The role you want")
@app_commands.choices(role=[app_commands.Choice(name=v[0], value=k) for k, v in APPLY_ROLES.items()])
async def apply(interaction: discord.Interaction, role: str):
    problem = apply_problem(interaction.guild, guild_signups(load_data(), interaction.guild.id), interaction.user, role)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    await interaction.response.send_modal(ApplyModal(role))


@bot.listen("on_interaction")
async def application_buttons(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return
    cid = (interaction.data or {}).get("custom_id", "")
    if not cid.startswith("app:"):
        return
    _, action, gid, aid = cid.split(":", 3)
    guild = bot.get_guild(int(gid))
    data = load_data()
    s = guild_signups(data, int(gid))
    a = applications(s).get(aid)
    if guild is None or a is None:
        return await interaction.response.send_message("That application doesn't exist any more.", ephemeral=True)
    if a["status"] != "open":
        return await interaction.response.send_message("This application was already handled.", ephemeral=True)
    if a["role"] not in APPLY_ROLES:  # a role you can't apply for any more
        a["status"] = "closed"
        save_data(data)
        return await interaction.response.edit_message(content="Closed: you can't apply for that role any more.",
                                                       view=None)
    staffer = interaction.user
    if a["role"] in APPLY_TOP and not is_commissioner(staffer):
        return await interaction.response.send_message("Only the Commissioner or an admin can decide staff applications.",
                                                       ephemeral=True)
    if not is_staff(staffer):
        return await interaction.response.send_message("Only league staff can decide applications.", ephemeral=True)
    name, icon = APPLY_ROLES[a["role"]]
    a["status"] = "accepted" if action == "ok" else "denied"
    a["by"], a["decided"] = staffer.id, datetime.now(timezone.utc).isoformat(timespec="seconds")
    save_data(data)
    note = ""
    if action == "ok":
        r = role(guild, name)
        if r is None:
            try:
                r = await guild.create_role(name=name, reason="Role applications")
            except discord.HTTPException:
                r = None
        member = guild.get_member(a["user"])
        try:
            if r and member:
                await member.add_roles(r, reason=f"Application accepted by {staffer}")
            elif not member:
                note = " (they've left the server)"
        except discord.HTTPException:
            note = " (couldn't give the role: move the bot's role above it)"
        await dm(a["user"], brand_embed(f"Your application for **{name}** in **{guild.name}** was accepted. Welcome aboard!",
                                        f"{icon} Application accepted", GOOD))
    else:
        await dm(a["user"], brand_embed(f"Your application for **{name}** in **{guild.name}** wasn't accepted this time. "
                                        f"You can apply again in {APPLY_COOLDOWN.days} days.", "Application update", MUTED))
    e = interaction.message.embeds[0] if interaction.message and interaction.message.embeds else None
    content = f"{'✅ Accepted' if action == 'ok' else '✖ Denied'} by {staffer.mention}{note}."
    try:
        await interaction.response.edit_message(content=content, embed=e, view=None, allowed_mentions=NO_PINGS)
    except discord.HTTPException:
        await interaction.response.send_message(content, ephemeral=True)


class MediaApply(discord.ui.Modal, title="Apply for Media / Streamer"):
    kind = discord.ui.TextInput(label="Media, Streamer, or both?", max_length=30)
    links = discord.ui.TextInput(label="Links to your channel / past content", style=discord.TextStyle.paragraph,
                                 max_length=500)
    plan = discord.ui.TextInput(label="What would you make for the circuit?", style=discord.TextStyle.paragraph,
                                max_length=500, required=False)

    async def on_submit(self, interaction: discord.Interaction):
        guild = interaction.guild
        s = guild_signups(load_data(), guild.id)
        c = media(s)["chans"]
        staff_ch = guild.get_channel(mod(s)["chans"].get("joinlog") or 0) or chan(guild, "staff-chat") \
            or guild.get_channel(c.get("chat") or 0)
        e = brand_embed(f"**From:** {interaction.user.mention}\n**Wants:** {self.kind.value}\n**Links:** "
                        f"{self.links.value}\n**Plan:** {self.plan.value or '—'}\n\nApprove with "
                        f"`/giverole member:@{interaction.user.name} kind:...`", "🎥 Media application", INFO)
        e.set_thumbnail(url=interaction.user.display_avatar.url)
        if staff_ch:
            await staff_ch.send(embed=e, allowed_mentions=NO_PINGS)
        await interaction.response.send_message("Application sent to staff. You'll hear back soon!", ephemeral=True)


# ---------------------------------------------------------------- game times + match reminders
#
# When a tournament match becomes playable (a new Swiss round, the group schedule, a bracket match),
# the captain and co-captain of both teams get a DM: "YOUR NEXT ON THE RISE PB: TOURNAMENT MATCH IS ...", and both
# captains get pinged in #scheduling. The captains have 48 HOURS to agree a game time:
#   1. One captain runs /gametime match:12 and picks one or more times (dropdowns, next 48 hours).
#   2. The request posts in #scheduling pinging both captains, and the other captain gets a DM with a
#      dropdown: pick one of the offered times (confirmed), or pick a different time (sent back to the
#      first captain to accept or decline).
#   3. Once confirmed, both rosters get DMs, then reminders 24 hours, 1 hour and at game time.
# If 48 hours pass with no time, both captains and staff are pinged; staff use /reschedule.

SCHED_HOURS = 72   # whole scheduling window for a match
AGREE_HOURS = 48   # captains agree a time in this long, or the bot sets the preset time
TIMEZONES = {"ET": ("America/New_York", -5), "CT": ("America/Chicago", -6), "MT": ("America/Denver", -7),
             "PT": ("America/Los_Angeles", -8), "UK": ("Europe/London", 0), "CET": ("Europe/Paris", 1),
             "AEST": ("Australia/Sydney", 10)}
TZ_CHOICES = [app_commands.Choice(name=k, value=k) for k in TIMEZONES]


def tzinfo(code: str):
    name, fixed = TIMEZONES.get(code or "ET", TIMEZONES["ET"])
    try:
        from zoneinfo import ZoneInfo
        return ZoneInfo(name)
    except Exception:  # Windows without the tzdata package: fixed offset (pip install tzdata fixes DST)
        return timezone(timedelta(hours=fixed))


def sched(s: dict) -> dict:
    sc = s.setdefault("sched", {})
    sc.setdefault("matches", {})   # match id -> {a, b, label, opened, deadline, time, reminded: [], done}
    sc.setdefault("requests", {})  # request id -> {match, from, to, from_team, to_team, times, status}
    sc.setdefault("drafts", {})    # user id -> {match, tz, picks}
    sc.setdefault("tz", {})        # user id -> timezone code
    sc.setdefault("next", 1)
    sc.setdefault("muted", [])     # users who turned match DMs off
    sc.setdefault("preset", {"time": "20:00", "tz": "ET"})  # first evening slot (8 PM ET), /presettime changes it
    if not sc.get("preset_v2"):  # servers still on the old 6 PM default move to 8 PM
        if sc["preset"] == {"time": "18:00", "tz": "ET"}:
            sc["preset"] = {"time": "20:00", "tz": "ET"}
        sc["preset_v2"] = True
    return sc


STAGE_DAYS = 3          # group stages under 16 teams, and every main draw, are played inside 3 days
FAST_GROUP_MAX = 16     # group stages with FEWER teams than this get the 3-day clock
PRESET_SLOTS = 8        # evening preset slots every 30 minutes: 8:00 PM ... 11:30 PM ET
SLOT_STEP = timedelta(minutes=30)


def preset_text(sc: dict) -> str:
    hh, mm = (int(x) for x in sc["preset"]["time"].split(":"))
    return f"{(hh + 11) % 12 + 1}:{mm:02d} {'AM' if hh < 12 else 'PM'} {sc['preset']['tz']}"


def evening_slot(sc: dict, start: datetime, busy: list[datetime] | None = None,
                 others: list[tuple[datetime, bool]] | None = None) -> datetime:
    """The first evening slot at or after `start` (8:00 PM ET, then every 30 minutes until 11:30 PM; the start is
    /presettime) that works for both teams (`busy`: their other games). Games are spread out: first try a slot
    where no other game starts, then one shared only with other bot-set games, never on top of a time captains
    set themselves (`others`: (start, set by captains?)). Rolls to the next evening when tonight is full."""
    hh, mm = (int(x) for x in sc["preset"]["time"].split(":"))
    tz = tzinfo(sc["preset"]["tz"])
    others = others or []
    day = start.astimezone(tz).replace(hour=0, minute=0, second=0, microsecond=0)
    near = lambda t, pool: any(abs(t - o) < SLOT_STEP for o in pool)
    user_set = [o for o, mine in others if mine]
    every = [o for o, _m in others]
    fallback = None
    for _d in range(14):
        first = day.replace(hour=hh, minute=mm)
        slots = [(first + SLOT_STEP * k).astimezone(timezone.utc) for k in range(PRESET_SLOTS)]
        slots = [t for t in slots if t >= start and clear_of(t, busy or [])]
        for t in slots:  # 1. nobody else starts then
            if not near(t, every):
                return t
        for t in slots:  # 2. only other bot-set games start then
            if not near(t, user_set):
                return t
        if slots and fallback is None:
            fallback = slots[0]
        day = (day + timedelta(days=1, hours=3)).replace(hour=0, minute=0)  # +3h: safe across clock changes
    return fallback or (start + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)

def stage_clock(s: dict, label: str, now: datetime) -> tuple[int, datetime | None]:
    """(hours captains get to agree a time, when the whole stage has to be finished or None).
    Group stages under 16 teams and main draws get a 3-day clock that starts when their first game opens."""
    ev = s.get("event") or {}
    lab = (label or "").lower()
    clock = ev.setdefault("clock", {})
    if lab.startswith("group"):
        n = sum(len(g) for g in (ev.get("groups") or {}).get("groups", []))
        if n and n < FAST_GROUP_MAX:
            clock.setdefault("group", (now + timedelta(days=STAGE_DAYS)).isoformat(timespec="seconds"))
            return 24, datetime.fromisoformat(clock["group"])
        return AGREE_HOURS, None
    if lab.startswith(("winners", "losers", "grand", "consolation")):
        clock.setdefault("main", (now + timedelta(days=STAGE_DAYS)).isoformat(timespec="seconds"))
        return 12, datetime.fromisoformat(clock["main"])
    return AGREE_HOURS, None


def preset_time(sc: dict, base: datetime) -> datetime:
    """The preset game time: the day after `base` (the 48-hour mark) at the preset clock time, 6:00 PM ET
    unless staff change it with /presettime."""
    hh, mm = (int(x) for x in sc["preset"]["time"].split(":"))
    tz = tzinfo(sc["preset"]["tz"])
    day = base.astimezone(tz) + timedelta(days=1)
    return day.replace(hour=hh, minute=mm, second=0, microsecond=0).astimezone(timezone.utc)


def can_override(e_: dict) -> bool:
    """The game time can still be changed (both captains confirming) until the game starts."""
    if e_.get("done"):
        return False
    return not e_.get("time") or datetime.now(timezone.utc) < datetime.fromisoformat(e_["time"])


def window_end(e_: dict) -> datetime:
    end = datetime.fromisoformat(e_.get("window_end") or e_["deadline"])
    if e_.get("time"):  # a set time can move earlier or up to a day later
        end = max(end, datetime.fromisoformat(e_["time"]) + timedelta(hours=24))
    return end


def open_matches(ev: dict | None) -> list[dict]:
    """Tournament matches that can be played right now: {id, a, b, label}."""
    if not ev or ev.get("drawing"):  # nothing is playable (or DMed) until the live draw is over
        return []
    out = []
    if ev.get("stage") == "swiss" and ev.get("swiss"):
        sw = ev["swiss"]
        out += [{"id": m["id"], "a": m["a"], "b": m["b"], "label": f"Swiss round {m['round']}"}
                for m in sw["matches"] if m["round"] == sw["round"] and not m["winner"] and m.get("b")]
    if ev.get("stage") == "groups" and ev.get("groups"):
        gs = ev["groups"]
        for gi in range(len(gs["groups"])):  # every group game is open at once: schedule them all straight away
            out += [{"id": m["id"], "a": m["a"], "b": m["b"], "label": f"Group {group_letter(gi)} · round {m['round']}"}
                    for m in gs["matches"] if m["group"] == gi and not m["winner"]]
    if ev.get("main"):
        out += [{"id": m["id"], "a": m["a"], "b": m["b"], "label": m["label"]} for m in de_ready(ev["main"])]
    out += [{"id": m["id"], "a": m["a"], "b": m["b"], "label": m["label"]} for m in cons_ready(ev.get("consolation"))]
    out += [{"id": m["id"], "a": m["a"], "b": m["b"], "label": m["label"]} for m in playin_ready(ev)]
    return out


def team_name(s: dict, tid) -> str:
    t = s["teams"].get(str(tid))
    return t["name"] if t else "TBD"


def ts(dt: datetime, style: str = "F") -> str:
    return f"<t:{int(dt.timestamp())}:{style}>"


GAME_GAP = timedelta(minutes=60)  # one team's games start at least this far apart (a game + getting set up)


def team_busy(sc: dict, teams, skip_mid: str | None = None) -> list[datetime]:
    """Game times already set for any of these teams (other matches that aren't played yet)."""
    ts_ = {str(t) for t in teams}
    return [datetime.fromisoformat(e_["time"]) for mid, e_ in sc["matches"].items()
            if mid != skip_mid and not e_["done"] and e_.get("time") and {str(e_["a"]), str(e_["b"])} & ts_]


def clear_of(when: datetime, busy: list[datetime]) -> bool:
    return all(abs(when - b) >= GAME_GAP for b in busy)


def slot_options(start: datetime, end: datetime, tz_code: str, taken: list[int] | None = None,
                 busy: list[datetime] | None = None) -> list[list]:
    """Hourly game times from the next full hour until `end`, as up to two lists of 24 select options.
    Times too close to another game of either team (`busy`) are left out."""
    tz = tzinfo(tz_code)
    t = (start + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    opts = []
    while t <= end and len(opts) < 48:
        if int(t.timestamp()) not in (taken or []) and clear_of(t, busy or []):
            local = t.astimezone(tz)
            label = local.strftime("%a %b %d · %I:%M %p").replace(" 0", " ") + f" {tz_code}"
            opts.append(discord.SelectOption(label=label, value=str(int(t.timestamp()))))
        t += timedelta(hours=1)
    return [opts[i:i + 24] for i in range(0, len(opts), 24)]


def slot_label(t: int, tz_code: str) -> str:
    local = datetime.fromtimestamp(t, timezone.utc).astimezone(tzinfo(tz_code))
    return local.strftime("%a %b %d · %I:%M %p").replace(" 0", " ") + f" {tz_code}"


async def dm(uid: int, embed: discord.Embed, view=None, _tries: int = 0) -> bool:
    try:
        u = bot.get_user(int(uid)) or await bot.fetch_user(int(uid))
        kw = {"embed": embed}
        if view is not None:
            kw["view"] = view
        await u.send(**kw)
        return True
    except Exception as ex:  # noqa: BLE001
        wait = rate_limit_wait(ex)
        if wait is not None and _tries < 3:  # rate limited: send it as soon as the limit expires
            async def later():
                await asyncio.sleep(wait + 1)
                await dm(uid, embed, view, _tries + 1)
            asyncio.create_task(later())
            return True
        if isinstance(ex, (discord.HTTPException, AttributeError)):
            return False
        raise


async def dm_teams(guild: discord.Guild, s: dict, teams: list, embed_for) -> None:
    """DM the captain and co-captain of these teams (not the whole roster): new matches, game times, reminders.
    embed_for(team_id) builds the card for that team's side."""
    muted = sched(s)["muted"]
    for tid in teams:
        t = s["teams"].get(str(tid))
        if not t:
            continue
        for uid in captains_of(s, tid):
            if int(uid) not in muted:
                await dm(int(uid), embed_for(tid))


def next_match_card(s: dict, mid: str, our, label_extra: str = "") -> discord.Embed:
    e_ = sched(s)["matches"][mid]
    other = e_["b"] if str(our) == str(e_["a"]) else e_["a"]
    tz = s.get("tourney") or {}
    when = (f"**Game time:** {ts(datetime.fromisoformat(e_['time']))} ({ts(datetime.fromisoformat(e_['time']), 'R')})"
            + (f"\n*Preset by the bot. Both captains can agree a different time with `/gametime match:{mid}`.*"
               if e_.get("preset") and can_override(e_) else "")
            if e_.get("time") else
            f"**Game time:** not set yet. Captains have until {ts(datetime.fromisoformat(e_['deadline']))} "
            f"({ts(datetime.fromisoformat(e_['deadline']), 'R')}) to agree one with `/gametime match:{mid}`, "
            f"or the bot picks one for staff to confirm (evenings from {preset_text(sched(s))}).")
    first = e_["label"] in ("Swiss round 1", "Winners R1") or e_["label"].endswith("round 1")
    e = brand_embed(f"# YOUR NEXT ON THE RISE PB: TOURNAMENT MATCH IS M{mid}\n"
                    + (f"🆚 **Your first opponent: {team_name(s, other)}**\n" if first else "")
                    + f"**{team_name(s, our)}** vs **{team_name(s, other)}**\n"
                    f"**Event:** {tz.get('name', 'Tournament')} · {e_['label']}\n{when}{label_extra}", None, GOLD)
    t = s["teams"].get(str(other))
    if t and t.get("logo"):
        url = site_url()
        if url:
            e.set_thumbnail(url=f"{url}logos/{t['logo']}")
    e.set_footer(text="Turn these DMs off with /matchdms · ON THE RISE · PB CIRCUIT")
    return e


async def scheduling_post(guild: discord.Guild, s: dict, mid: str, text: str, title: str, color=BRAND, pings=True):
    e_ = sched(s)["matches"][mid]
    caps = [s["teams"][str(t)]["captain"] for t in (e_["a"], e_["b"]) if str(t) in s["teams"]]
    ch = chan(guild, "scheduling")
    if ch:
        await ch.send(content=" ".join(f"<@{c}>" for c in caps) if pings else None,
                      embed=brand_embed(text, title, color),
                      allowed_mentions=discord.AllowedMentions(users=True, roles=False, everyone=False))


async def match_opened(guild: discord.Guild, s: dict, m: dict):
    """A new match is playable: start its 48-hour clock, DM both rosters and ping the captains."""
    sc = sched(s)
    now = datetime.now(timezone.utc)
    mid = str(m["id"])
    hours, stage_end = stage_clock(s, m["label"], now)
    deadline = now + timedelta(hours=hours)
    if stage_end:  # 3-day stage: agree in time to still play before it ends
        deadline = max(now + timedelta(hours=2), min(deadline, stage_end - timedelta(hours=6)))
    sc["matches"][mid] = {"a": m["a"], "b": m["b"], "label": m["label"], "opened": now.isoformat(timespec="seconds"),
                          "deadline": deadline.isoformat(timespec="seconds"),
                          "window_end": (stage_end or now + timedelta(hours=SCHED_HOURS)).isoformat(timespec="seconds"),
                          "stage_end": stage_end.isoformat(timespec="seconds") if stage_end else None,
                          "time": None, "preset": False, "reminded": [], "done": False}
    await dm_teams(guild, s, [m["a"], m["b"]], lambda tid: next_match_card(s, mid, tid))
    dl = datetime.fromisoformat(sc["matches"][mid]["deadline"])
    p_ = sc["preset"]
    await scheduling_post(guild, s, mid,
                          f"**M{mid}** · {m['label']}\n**{team_name(s, m['a'])}** vs **{team_name(s, m['b'])}**\n\n"
                          f"Captains, you have until {ts(dl)} ({ts(dl, 'R')}) to agree a game time. Run "
                          f"`/gametime match:{mid}` and pick the times that work; the other captain confirms in DMs.\n"
                          f"No time by then? **The bot picks one and staff confirm it** (evenings from {preset_text(sc)}), and you'll be "
                          "reminded every 6 hours until it's scheduled. A staff-set time can still move if both "
                          "captains confirm."
                          + (f"\nThis stage has to be finished by {ts(stage_end, 'f')}." if stage_end else ""),
                          f"📅 Schedule your match · M{mid}", INFO)


# ---------------------------------------------------------------- unscheduled games: staff presets + 6-hour nags
#
# The bot no longer picks a time by itself (AUTO_PRESET = False). When a game's deadline passes with no time,
# staff get a card in #staff-chat with a suggested evening slot (one click sets it) or use /reschedule.
# Every 6 hours, each team with games that still have no time is pinged in its team channel with exactly who to
# DM: every unscheduled opponent in a group stage, or the current opponent in Swiss / the main draw.

AUTO_PRESET = False       # False = the bot picks the time and staff confirm it; True = the bot sets it by itself
NAG_EVERY = timedelta(hours=6)


def pick_preset(sc: dict, mid: str, e_: dict, after: datetime) -> datetime:
    """The bot's pick: first evening slot (8 PM ET on, every 30 min) after `after` that fits both teams and is
    spread out from other games, including other picks still waiting for staff."""
    busy = team_busy(sc, (e_["a"], e_["b"]), mid)
    busy += [datetime.fromtimestamp(x["pending_preset"], timezone.utc) for k, x in sc["matches"].items()
             if k != mid and not x.get("done") and not x.get("time") and x.get("pending_preset")
             and {str(x["a"]), str(x["b"])} & {str(e_["a"]), str(e_["b"])}]
    others = [(datetime.fromisoformat(x["time"]), not x.get("preset")) for k, x in sc["matches"].items()
              if k != mid and not x.get("done") and x.get("time")]
    others += [(datetime.fromtimestamp(x["pending_preset"], timezone.utc), False) for k, x in sc["matches"].items()
               if k != mid and not x.get("done") and not x.get("time") and x.get("pending_preset")]
    return evening_slot(sc, after, busy, others)


def preset_card(guild: discord.Guild, s: dict, mid: str, e_: dict, pick: datetime):
    sc = sched(s)
    v = discord.ui.View(timeout=None)
    v.add_item(discord.ui.Button(label=f"Confirm {slot_label(int(pick.timestamp()), sc['preset']['tz'])}"[:80],
                                 emoji="✅", style=discord.ButtonStyle.success,
                                 custom_id=f"ps:set:{guild.id}:{mid}:{int(pick.timestamp())}"))
    v.add_item(discord.ui.Button(label="Pick the next slot", emoji="⏭️", style=discord.ButtonStyle.secondary,
                                 custom_id=f"ps:next:{guild.id}:{mid}:{int(pick.timestamp())}"))
    req = unanswered_request(sc, mid)
    note = (f"\n**{team_name(s, req['from_team'])}** sent times and **{team_name(s, req['to_team'])}** never answered "
            "(the first team has priority)." if req else "")
    e = brand_embed(
        f"**M{mid}** · {e_.get('label', '')}\n**{team_name(s, e_['a'])}** vs **{team_name(s, e_['b'])}**: the captains "
        f"didn't agree a time before the deadline.{note}\n\nThe bot picked **{ts(pick)}** ({ts(pick, 'R')}): the first "
        "evening slot that works for both teams without starting on top of another game.\n\n"
        f"**Confirm** to set it (both teams are told), **Pick the next slot** for a later one, or set your own with "
        f"`/reschedule match:{mid} time:...`.", f"🕗 Confirm preset · M{mid}", GOLD)
    return e, v


async def staff_preset_card(guild: discord.Guild, s: dict, mid: str, e_: dict, now: datetime, after=None):
    """Post (or refresh) the bot's picked time for staff to confirm in #staff-chat. Nothing is set until they do."""
    sc = sched(s)
    pick = pick_preset(sc, mid, e_, after or now + timedelta(minutes=30))
    e_["pending_preset"] = int(pick.timestamp())
    emb, v = preset_card(guild, s, mid, e_, pick)
    old = e_.get("preset_card")
    if old:
        try:
            msg = await guild.get_channel(int(old[0])).fetch_message(int(old[1]))
            await msg.edit(embed=emb, view=v)
            return
        except Exception:
            pass
    ch = chan(guild, "staff-chat") or chan(guild, "mod-log")
    if ch is None:
        return
    msg = await ch.send(embed=emb, view=v, allowed_mentions=NO_PINGS)
    e_["preset_card"] = [ch.id, msg.id]


@bot.listen("on_interaction")
async def preset_buttons(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return
    cid = (interaction.data or {}).get("custom_id", "")
    if not cid.startswith("ps:"):
        return
    _, action, gid, mid, t = cid.split(":", 4)
    guild = bot.get_guild(int(gid))
    if guild is None or not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can confirm preset times.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    e_ = sched(s)["matches"].get(mid)
    if not e_ or e_["done"]:
        return await interaction.response.edit_message(content="That game is already finished.", view=None)
    if e_.get("time"):
        return await interaction.response.edit_message(
            content=f"Already set: {ts(datetime.fromisoformat(e_['time']))}. Use /reschedule to move it.", view=None)
    now = datetime.now(timezone.utc)
    if action == "next" or int(t) <= now.timestamp():
        pick = pick_preset(sched(s), mid, e_, max(datetime.fromtimestamp(int(t), timezone.utc) + timedelta(minutes=1),
                                                  now + timedelta(minutes=30)))
        e_["pending_preset"] = int(pick.timestamp())
        save_data(data)
        emb, v = preset_card(guild, s, mid, e_, pick)
        return await interaction.response.edit_message(
            embed=emb, view=v, content=None if action == "next" else "That slot passed, so here's the next one.")
    e_.pop("pending_preset", None)
    e_.pop("preset_card", None)
    save_data(data)
    await interaction.response.edit_message(content=f"✅ Confirmed by {interaction.user.mention}.", view=None,
                                            allowed_mentions=NO_PINGS)
    await confirm_time(guild, data, mid, int(t), f"the bot, confirmed by staff ({interaction.user.mention})")
    d2 = load_data()
    e2 = sched(guild_signups(d2, guild.id))["matches"].get(mid)
    if e2:
        e2["preset"] = True  # still movable if both captains agree (or the priority team asks)
        save_data(d2)


def unscheduled_by_team(s: dict) -> dict[int, list]:
    """team id -> [(match id, sched entry, opponent id)] for open games with no time."""
    sc = sched(s)
    out: dict[int, list] = {}
    live = {str(m["id"]) for m in open_matches(s.get("event"))}
    for mid, e_ in sc["matches"].items():
        if e_.get("done") or e_.get("time") or mid not in live:
            continue
        for me, them in ((e_["a"], e_["b"]), (e_["b"], e_["a"])):
            out.setdefault(int(me), []).append((mid, e_, them))
    return out


def nag_due(s: dict, now: datetime) -> dict[int, list]:
    """Teams whose 6-hour ping is due: team id -> their unscheduled games."""
    last = s.setdefault("sched_nag", {})
    due = {}
    for tid, games in unscheduled_by_team(s).items():
        if str(tid) not in s["teams"]:
            continue
        prev = datetime.fromisoformat(last[str(tid)]) if last.get(str(tid)) else None
        oldest_open = min(datetime.fromisoformat(e_.get("opened") or now.isoformat()) for _m, e_, _o in games)
        if now - oldest_open >= NAG_EVERY and not (prev and now - prev < NAG_EVERY):
            due[tid] = games  # 6 hours after their first open game, then every 6 hours
    return due


def nag_embed(s: dict, tid: int, games: list, now: datetime, prefix: str = "") -> discord.Embed:
    label = (games[0][1].get("label") or "").lower()
    stage = ("group stage" if label.startswith("group") else "Swiss stage" if label.startswith("swiss") else
             "main draw" if label.startswith(("winners", "losers", "grand")) else "tournament")
    lines = []
    for mid, e_, opp in sorted(games, key=lambda x: int(x[0])):
        caps = " ".join(f"<@{u}>" for u in captains_of(s, opp)) or "their captain"
        dl = datetime.fromisoformat(e_["deadline"])
        late = (" · **deadline passed: the bot picked a time, waiting for staff to confirm**"
                if now >= dl else f" · agree by {ts(dl, 'R')}")
        lines.append(f"**M{mid}** vs **{team_name(s, opp)}** → DM {caps}{late}")
    head = (f"You have **{len(games)} {stage} game{'s' if len(games) != 1 else ''}** with no time yet. "
            "DM these captains and lock them in:" if stage == "group stage" else
            f"Your **{stage}** game still has no time. DM their captain and lock it in:")
    return brand_embed(prefix + head + "\n" + "\n".join(lines[:15]) + "\n\nUse `/gametime` (pick a few times) or "
                       "`/confirmtime` (one exact time). Times have to be agreed by both captains.",
                       "⏰ Schedule your games", GOLD)


def commissioners(guild: discord.Guild) -> list:
    return [m for m in guild.members if not m.bot and is_commissioner(m)]


async def nag_unscheduled(guild: discord.Guild, s: dict, now: datetime) -> bool:
    """Every 6 hours the bot lines up the "schedule your games" pings and asks Commissioner+ by DM first.
    Nothing is pinged until one of them clicks Send (Skip waits for the next 6 hours)."""
    last = s.setdefault("sched_nag", {})
    todo = unscheduled_by_team(s)
    changed = False
    for k in [k for k in last if int(k) not in todo]:  # all scheduled: reset their clock
        last.pop(k)
        changed = True
    batch = s.get("nag_batch")
    if batch and batch.get("status") == "open" and now - datetime.fromisoformat(batch["at"]) < NAG_EVERY:
        return changed  # still waiting on a Commissioner
    due = nag_due(s, now)
    if not due:
        return changed
    bid = secrets.token_hex(4)
    lines = []
    for tid, games in sorted(due.items(), key=lambda kv: team_name(s, kv[0]).lower()):
        lines.append(f"**{team_name(s, tid)}**: " + ", ".join(f"M{mid} vs {team_name(s, opp)}"
                                                              for mid, _e, opp in sorted(games, key=lambda x: int(x[0]))))
    e = brand_embed(f"**{len(due)} team(s)** still have games with no time. DM their captains and co-captains the "
                    "\"schedule your games\" reminder (with exactly who to DM)?\n\n"
                    + "\n".join(lines[:25]) + ("\n…" if len(lines) > 25 else ""),
                    f"⏰ 6-hour schedule pings · {guild.name}", GOLD)
    v = discord.ui.View(timeout=None)
    v.add_item(discord.ui.Button(label="Send DMs", emoji="✅", style=discord.ButtonStyle.success,
                                 custom_id=f"nag:send:{guild.id}:{bid}"))
    v.add_item(discord.ui.Button(label="Skip this time", emoji="✖", style=discord.ButtonStyle.secondary,
                                 custom_id=f"nag:skip:{guild.id}:{bid}"))
    msgs = []
    for m in commissioners(guild):
        try:
            msg = await m.send(embed=e, view=v)
            msgs.append([m.id, msg.channel.id, msg.id])
        except discord.HTTPException:
            pass
    s["nag_batch"] = {"id": bid, "teams": [str(t) for t in due], "status": "open",
                      "at": now.isoformat(timespec="seconds"), "msgs": msgs}
    return True


async def send_nags(guild: discord.Guild, team_ids: list[str]) -> int:
    """DM the reminders to each team's captain and co-captain (only for games still unscheduled right now).
    DMs only: nothing is posted in team channels."""
    data = load_data()
    s = guild_signups(data, guild.id)
    now = datetime.now(timezone.utc)
    todo = unscheduled_by_team(s)
    last = s.setdefault("sched_nag", {})
    sent = 0
    for k in team_ids:
        games = todo.get(int(k))
        t = s["teams"].get(k)
        if not games or not t:
            continue
        got = False
        for uid in captains_of(s, k):
            e = nag_embed(s, int(k), games, now, f"**{t['name']}** in **{guild.name}**\n\n")
            if await dm(uid, e):
                got = True
        if got:
            sent += 1
        last[k] = now.isoformat(timespec="seconds")
    save_data(data)
    return sent


@bot.listen("on_interaction")
async def nag_buttons(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return
    cid = (interaction.data or {}).get("custom_id", "")
    if not cid.startswith("nag:"):
        return
    _, action, gid, bid = cid.split(":", 3)
    guild = bot.get_guild(int(gid))
    member = guild.get_member(interaction.user.id) if guild else None
    if guild is None or member is None or not is_commissioner(member):
        return await interaction.response.send_message("Only the Commissioner or an admin can do that.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    batch = s.get("nag_batch")
    if not batch or batch["id"] != bid or batch["status"] != "open":
        return await interaction.response.edit_message(content="Already handled (or a newer one replaced it).",
                                                       view=None)
    batch["status"] = "sent" if action == "send" else "skipped"
    batch["by"] = member.id
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    if action == "skip":  # wait another 6 hours before asking about these teams again
        for k in batch["teams"]:
            s.setdefault("sched_nag", {})[k] = now
    save_data(data)
    await interaction.response.defer()
    n = await send_nags(guild, batch["teams"]) if action == "send" else 0
    note = (f"✅ Sent to {n} team(s) by {member.display_name}." if action == "send" else
            f"✖ Skipped by {member.display_name}. Asking again in 6 hours.")
    for uid, ch_id, msg_id in batch.get("msgs", []):  # update every Commissioner's copy
        try:
            u = bot.get_user(uid) or await bot.fetch_user(uid)
            dmch = u.dm_channel or await u.create_dm()
            await dmch.get_partial_message(msg_id).edit(content=note, view=None)
        except discord.HTTPException:
            pass


# ---------------------------------------------------------------- priority: you asked, they ghosted
#
# If one captain sent game times (/gametime or /confirmtime) and the other team never answered, the bot still sets
# the preset time, but the team that asked gets PRIORITY: they can move the game with /prioritytime without the
# other team confirming. Staff have to approve the change (Approve / Deny card in #staff-chat).

def unanswered_request(sc: dict, mid: str) -> dict | None:
    reqs = [r for r in sc["requests"].values() if r["match"] == mid and r["status"] == "open"]
    return reqs[-1] if reqs else None


async def grant_priority(guild: discord.Guild, s: dict, mid: str, e_: dict):
    sc = sched(s)
    r = unanswered_request(sc, mid)
    if not r:
        return
    r["status"] = "ignored"
    e_["priority"] = r["from_team"]
    for uid in captains_of(s, r["from_team"]):
        await dm(uid, brand_embed(
            f"**{team_name(s, r['to_team'])}** never answered your game time request for **M{mid}**"
            + (f", so the game is set for {ts(datetime.fromisoformat(e_['time']))}." if e_.get("time") else ".")
            + f"\n\nYour team has **priority**: run `/prioritytime match:{mid} time:...` to "
            + ("move it" if e_.get("time") else "set the time") + " without their confirmation. Staff approve it, "
            "then both teams are told.", f"⭐ Priority · M{mid}", GOLD))


@bot.tree.command(description="Captains with priority (the other team never answered): move the preset game time.")
@app_commands.describe(match="Match number, e.g. 12 for M12",
                       time="The new time: 8pm, 8:30pm, tomorrow 9pm, sat 8pm", timezone="Timezone of that time")
@app_commands.choices(timezone=TZ_CHOICES)
async def prioritytime(interaction: discord.Interaction, match: int, time: str, timezone: str | None = None):
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    sc = sched(s)
    mid = str(match)
    e_ = sc["matches"].get(mid)
    if not e_ or e_["done"]:
        return await interaction.response.send_message(f"M{match} isn't an open match.", ephemeral=True)
    if not e_.get("priority"):
        return await interaction.response.send_message(
            f"Nobody has priority on M{match}. Use `/gametime` and let the other captain confirm.", ephemeral=True)
    if user.id not in captains_of(s, e_["priority"]):
        return await interaction.response.send_message(
            f"Only **{team_name(s, e_['priority'])}**'s captain or co-captain has priority on M{match}.", ephemeral=True)
    if not can_override(e_):
        return await interaction.response.send_message(f"M{match} has already started.", ephemeral=True)
    tz_code = timezone or sc["tz"].get(str(user.id), "ET")
    when, problem = parse_when(time, tz_code)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    now = datetime.now(timezone_utc())
    if when <= now + timedelta(minutes=30):
        return await interaction.response.send_message("Pick a time at least 30 minutes from now.", ephemeral=True)
    end = datetime.fromisoformat(e_.get("stage_end") or e_.get("window_end") or e_["deadline"])
    if e_.get("stage_end") and when > end:
        return await interaction.response.send_message(f"This stage has to be done by {ts(end)}. Pick an earlier time.",
                                                       ephemeral=True)
    if not clear_of(when, team_busy(sc, (e_["a"], e_["b"]), mid)):
        return await interaction.response.send_message("One of the teams has another game within an hour of that time.",
                                                       ephemeral=True)
    staff_ch = chan(guild, "staff-chat") or chan(guild, "mod-log")
    if staff_ch is None:
        return await interaction.response.send_message("There's no #staff-chat for staff to approve it. Ask staff.",
                                                       ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    pid = secrets.token_hex(4)
    sc.setdefault("priority_reqs", {})[pid] = {"match": mid, "team": e_["priority"], "by": user.id,
                                              "time": int(when.timestamp()), "status": "open"}
    save_data(data)
    other = e_["b"] if str(e_["a"]) == str(e_["priority"]) else e_["a"]
    old = datetime.fromisoformat(e_["time"]) if e_.get("time") else None
    v = discord.ui.View(timeout=None)
    v.add_item(discord.ui.Button(label="Approve", emoji="✅", style=discord.ButtonStyle.success,
                                 custom_id=f"pt:ok:{guild.id}:{pid}"))
    v.add_item(discord.ui.Button(label="Deny", emoji="✖", style=discord.ButtonStyle.danger,
                                 custom_id=f"pt:no:{guild.id}:{pid}"))
    await staff_ch.send(embed=brand_embed(
        f"**{team_name(s, e_['priority'])}** sent game times for **M{mid}** and **{team_name(s, other)}** never answered, "
        f"so they have priority.\n\n{user.mention} wants to move it"
        + (f" from {ts(old)}" if old else "") + f" to **{ts(when)}** ({ts(when, 'R')}).\n\nApprove to set it "
        "(both teams are told), or deny to keep the current time.", f"⭐ Priority override · M{mid}", GOLD),
        view=v, allowed_mentions=NO_PINGS)
    await interaction.followup.send(f"Sent to staff to approve: M{mid} at {ts(when)}. You'll get a DM when they decide.",
                                    ephemeral=True)


@bot.listen("on_interaction")
async def priority_buttons(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return
    cid = (interaction.data or {}).get("custom_id", "")
    if not cid.startswith("pt:"):
        return
    _, action, gid, pid = cid.split(":", 3)
    guild = bot.get_guild(int(gid))
    if guild is None or not is_official(interaction.user):
        return await interaction.response.send_message("Only staff can approve priority overrides.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    sc = sched(s)
    pr = sc.get("priority_reqs", {}).get(pid)
    if not pr or pr["status"] != "open":
        return await interaction.response.send_message("This request was already handled.", ephemeral=True)
    e_ = sc["matches"].get(pr["match"])
    if not e_ or e_["done"] or not can_override(e_):
        pr["status"] = "expired"
        save_data(data)
        return await interaction.response.edit_message(content="Expired: the game has started or finished.", view=None)
    pr["status"] = "approved" if action == "ok" else "denied"
    pr["staff"] = interaction.user.id
    save_data(data)
    when = datetime.fromtimestamp(pr["time"], timezone.utc)
    await interaction.response.edit_message(
        content=f"{'✅ Approved' if action == 'ok' else '✖ Denied'} by {interaction.user.mention}.", view=None,
        allowed_mentions=NO_PINGS)
    if action == "ok":
        await confirm_time(guild, data, pr["match"], pr["time"],
                           f"<@{pr['by']}> (priority, approved by staff)")
        d2 = load_data()
        e2 = sched(guild_signups(d2, guild.id))["matches"].get(pr["match"])
        if e2:
            e2.pop("priority", None)  # priority is used up
            save_data(d2)
        await dm(pr["by"], brand_embed(f"Staff approved it: **M{pr['match']}** is now {ts(when)}.", "✅ Priority approved", GOOD))
    else:
        await dm(pr["by"], brand_embed(f"Staff kept **M{pr['match']}** at its current time. You still have priority if "
                                       "you want to ask for a different time.", "Priority not approved", MUTED))


# ---------------------------------------------------------------- #game-announcements: matchup graphic
#
# When a game time is confirmed (both captains, or staff), the bot posts a matchup graphic in #game-announcements:
# both logos facing off, each half tinted with that team's logo colour, the stage, and the game time.

def logo_colour(path, fallback):
    """The main colour of a logo (ignores transparent, near-black and near-white pixels)."""
    from PIL import Image
    import colorsys
    try:
        im = Image.open(path).convert("RGBA")
        im.thumbnail((64, 64))
        px = [p[:3] for p in im.getdata() if p[3] > 128 and 40 < sum(p[:3]) / 3 < 225]
        if not px:
            return fallback
        # weight colourful pixels more than grey ones
        best, score = None, -1
        buckets = {}
        for r, g, b in px:
            k = (r // 32, g // 32, b // 32)
            buckets.setdefault(k, []).append((r, g, b))
        for k, v in buckets.items():
            r, g, b = (sum(c[i] for c in v) / len(v) for i in range(3))
            sat = colorsys.rgb_to_hsv(r / 255, g / 255, b / 255)[1]
            sc_ = len(v) * (0.3 + sat)
            if sc_ > score:
                best, score = (r, g, b), sc_
        h, s_, v_ = colorsys.rgb_to_hsv(*(c / 255 for c in best))
        r, g, b = colorsys.hsv_to_rgb(h, max(s_, .55), min(max(v_, .55), .85))
        return int(r * 255), int(g * 255), int(b * 255)
    except Exception:
        return fallback


def matchup_picture(s: dict, mid: str, e_: dict | None = None, tz_codes=("ET", "CT", "PT")) -> bytes:
    """Game announcement graphic: two logos face off over their team colours, VS in the middle, the game time."""
    from PIL import Image, ImageDraw, ImageFilter
    e_ = e_ or sched(s)["matches"][mid]
    W, H = 1600, 900
    tz = s.get("tourney") or {}
    ta, tb = (s["teams"].get(str(e_[k]), {}) for k in ("a", "b"))
    pa = LOGO_DIR / ta["logo"] if ta.get("logo") else None
    pb_ = LOGO_DIR / tb["logo"] if tb.get("logo") else None
    ca = logo_colour(pa, (220, 60, 60)) if pa and pa.exists() else (220, 60, 60)
    cb = logo_colour(pb_, (50, 110, 220)) if pb_ and pb_.exists() else (50, 110, 220)
    img = Image.new("RGB", (W, H), (9, 9, 11))
    d = ImageDraw.Draw(img)
    # two halves split by a slanted line, each fading to black toward the edges
    left = Image.new("RGB", (W, H), ca)
    right = Image.new("RGB", (W, H), cb)
    mask = Image.new("L", (W, H), 0)
    ImageDraw.Draw(mask).polygon([(0, 0), (W // 2 + 90, 0), (W // 2 - 90, H), (0, H)], fill=255)
    halves = Image.composite(left, right, mask)
    shade = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(shade)
    for y in range(H):  # darker at the top and bottom, brightest across the middle
        k = 1 - abs(y - H * .48) / (H * .62)
        sd.line([(0, y), (W, y)], fill=int(40 + 120 * max(0, k)))
    img = Image.composite(halves, img, shade)
    d = ImageDraw.Draw(img)
    # the split line
    d.line([(W // 2 + 90, 0), (W // 2 - 90, H)], fill=(255, 122, 0), width=10)
    # logos with a soft glow
    for path, col, team, cx in ((pa, ca, ta, W * .25), (pb_, cb, tb, W * .75)):
        size = 360
        glow = Image.new("RGBA", (size + 360, size + 360), (0, 0, 0, 0))
        ImageDraw.Draw(glow).ellipse((140, 140, size + 220, size + 220), fill=col + (200,))
        glow = glow.filter(ImageFilter.GaussianBlur(40))
        y = 230
        img.paste(glow, (int(cx - size / 2 - 180), y - 180), glow)
        ring = Image.new("RGBA", (size + 16, size + 16), (0, 0, 0, 0))
        ImageDraw.Draw(ring).ellipse((0, 0, size + 15, size + 15), fill=(245, 245, 245, 255))
        img.paste(ring, (int(cx - size / 2 - 8), y - 8), ring)
        lg = _logo(path if path and path.exists() else None, size, team.get("name", "TBD"))
        img.paste(lg, (int(cx - size / 2), y), lg)
        name = team.get("name", "TBD").upper()
        f = _fit(d, name, 560, 58, 24)
        tw = d.textlength(name, font=f)
        d.text((cx - tw / 2 + 3, 633), name, font=f, fill=(0, 0, 0))
        d.text((cx - tw / 2, 630), name, font=f, fill=(250, 250, 250))
    # VS
    fv = _font(150)
    vw = d.textlength("VS", font=fv)
    d.text((W / 2 - vw / 2 + 6, 318), "VS", font=fv, fill=(0, 0, 0))
    d.text((W / 2 - vw / 2, 312), "VS", font=fv, fill=(255, 122, 0))
    # top: league, tournament, stage
    top = Image.new("RGBA", (W, 150), (0, 0, 0, 0))
    tdraw = ImageDraw.Draw(top)
    for y in range(150):
        tdraw.line([(0, y), (W, y)], fill=(0, 0, 0, int(200 * (1 - y / 150))))
    img.paste(top, (0, 0), top)
    d = ImageDraw.Draw(img)
    d.text((50, 34), "GAME ANNOUNCEMENT", font=_font(26), fill=(255, 122, 0))
    d.text((50, 68), (tz.get("name") or "Tournament").upper(), font=_font(46), fill=(250, 250, 250))
    head = stage_heading(e_.get("label", ""), mid)
    fh = _font(26)
    d.text((W - 50 - d.textlength(head, font=fh), 40), head, font=fh, fill=(230, 230, 230))
    fl = _font(22)
    d.text((W - 50 - d.textlength("ON THE RISE: PB CIRCUIT", font=fl), 80), "ON THE RISE: PB CIRCUIT", font=fl,
           fill=(190, 190, 195))
    # bottom band: the game time
    band = Image.new("RGBA", (W, 190), (9, 9, 11, 235))
    img.paste(band, (0, H - 190), band)
    d = ImageDraw.Draw(img)
    d.line([(0, H - 190), (W, H - 190)], fill=(255, 122, 0), width=6)
    if e_.get("time"):
        when = datetime.fromisoformat(e_["time"])
        main_tz = tz_codes[0]
        lt = when.astimezone(tzinfo(main_tz))
        big = (lt.strftime("%a %b %d").upper().replace(" 0", " ") + "  ·  " +
               lt.strftime("%I:%M %p").lstrip("0") + f" {main_tz}")
        others = "   ".join(when.astimezone(tzinfo(c)).strftime("%I:%M %p").lstrip("0") + f" {c}" for c in tz_codes[1:])
    else:
        big, others = "TIME TBA", ""
    fb = _fit(d, big, W - 100, 64, 30)
    d.text((W / 2 - d.textlength(big, font=fb) / 2, H - 165), big, font=fb, fill=(250, 250, 250))
    extra = others
    if e_.get("stream"):
        extra += ("   ·   " if extra else "") + "LIVE ON STREAM"
    if extra:
        fo = _font(26, bold=False)
        d.text((W / 2 - d.textlength(extra, font=fo) / 2, H - 82), extra, font=fo, fill=(170, 170, 175))
    fs = _font(18, bold=False)
    d.text((50, H - 34), "ontherisepb.com", font=fs, fill=(120, 120, 125))
    return _png(img)


async def ensure_game_announcements(guild: discord.Guild):
    """Make #game-announcements (everyone reads, only staff and the bot post) if it isn't there."""
    if chan(guild, "game-announcements"):
        return
    try:
        sch = chan(guild, "schedule")
        cat = sch.category if sch else await get_or_make_category(guild, "LEAGUE")
        ch = await guild.create_text_channel("game-announcements", category=cat, overwrites=overwrites_for(guild, "ro"),
                                             topic="Every confirmed game: who's playing and when.")
        if sch:
            try:
                await ch.edit(position=sch.position + 1)
            except discord.HTTPException:
                pass
        print(f"[{guild.name}] Made #game-announcements.")
    except discord.HTTPException as e:
        print(f"[{guild.name}] couldn't make #game-announcements: {e}")


async def drop_game_announcement(guild: discord.Guild, e_: dict):
    old = e_.pop("announce", None)
    if old:
        try:
            ch = guild.get_channel(int(old[0]))
            await (await ch.fetch_message(int(old[1]))).delete()
        except Exception:
            pass


def announcement_text(s: dict, mid: str, e_: dict) -> str:
    when = datetime.fromisoformat(e_["time"])
    text = (f"### {stage_heading(e_.get('label', ''), mid)}\n**{team_name(s, e_['a'])}** vs **{team_name(s, e_['b'])}**\n"
            f"{ts(when)} ({ts(when, 'R')})")
    if e_.get("stream"):
        text += (f"\n📺 Streamed by **{e_.get('stream_name') or 'a streamer'}** (<@{e_['stream']}>)"
                 + (f" · [Watch]({e_['stream_link']})" if e_.get("stream_link") else ""))
    return text


async def update_announcement_stream(guild: discord.Guild, e_: dict):
    """Someone claimed (or dropped) the stream: update the line under the matchup graphic."""
    a = e_.get("announce")
    if not a:
        return
    try:
        s = guild_signups(load_data(), guild.id)
        mid = next((k for k, v in sched(s)["matches"].items() if v.get("announce") == a), None)
        if mid is None:
            return
        ch = guild.get_channel(int(a[0]))
        msg = await ch.fetch_message(int(a[1]))
        emb = brand_embed(announcement_text(s, mid, sched(s)["matches"][mid]), None, GOLD)
        emb.set_image(url="attachment://matchup.png")
        await msg.edit(embed=emb, allowed_mentions=NO_PINGS)
    except Exception as ex:
        print(f"[announcement stream] {ex}")


async def post_game_announcement(guild: discord.Guild, s: dict, mid: str):
    """The matchup graphic in #game-announcements (replaces the old one if the time moved)."""
    e_ = sched(s)["matches"].get(mid)
    ch = chan(guild, "game-announcements")
    if not e_ or not e_.get("time") or ch is None:
        return
    await drop_game_announcement(guild, e_)
    try:
        png = await asyncio.to_thread(matchup_picture, s, mid, e_)
    except Exception as ex:
        print(f"[matchup picture] {ex}")
        return
    emb = brand_embed(announcement_text(s, mid, e_), None, GOLD)
    emb.set_image(url="attachment://matchup.png")
    try:
        msg = await ch.send(embed=emb, file=discord.File(io.BytesIO(png), filename="matchup.png"),
                            allowed_mentions=NO_PINGS)
        e_["announce"] = [ch.id, msg.id]
    except discord.HTTPException as ex:
        print(f"[game announcement] {ex}")


# ---------------------------------------------------------------- PICK'EMS
# Every confirmed game gets a pick'em in #pickems: an @here, a lineup card (both full rosters with their
# season stats) and a button for each team. Picks lock at tip-off. A right pick = 1 point on the leaderboard.

def pickems(s: dict) -> dict:
    return s.setdefault("pickems", {"games": {}, "board": {}})


def pickem_for(s: dict, mid: str, e_: dict | None, create: bool = False) -> dict | None:
    """This game's pick'em. Match numbers start again each tournament, so an old one with the same number is
    replaced (its points are already on the leaderboard)."""
    games = pickems(s)["games"]
    pk = games.get(mid)
    if pk and e_ is not None and pk.get("opened") != e_.get("opened"):
        pk = None
    if pk is None and create and e_ is not None:
        pk = games[mid] = {"picks": {}, "opened": e_.get("opened")}
    return pk


async def ensure_pickems_channel(guild: discord.Guild):
    if chan(guild, "pickems"):
        return
    try:
        ga = chan(guild, "game-announcements") or chan(guild, "schedule")
        cat = ga.category if ga else await get_or_make_category(guild, "LEAGUE")
        ch = await guild.create_text_channel("pickems", category=cat, overwrites=overwrites_for(guild, "ro"),
                                             topic="Pick who wins every game. Picks lock at tip-off. /pickems for the leaderboard.")
        if ga:
            try:
                await ch.edit(position=ga.position + 1)
            except discord.HTTPException:
                pass
        print(f"[{guild.name}] Made #pickems.")
    except discord.HTTPException as e:
        print(f"[{guild.name}] couldn't make #pickems: {e}")


def lineup_rows(guild: discord.Guild | None, s: dict, tid) -> list[dict]:
    """A team's full roster with season averages (this year's past tournaments + the current one)."""
    t = s["teams"].get(str(tid)) or {}
    year = datetime.now().year
    cur = player_totals(s.get("event"), str, str)
    tot = merge_totals(*[h["players"] for h in s.get("history", []) if h.get("year") == year], cur)
    rows = []
    for u in t.get("roster", []):
        mem = guild.get_member(int(u)) if guild and str(u).isdigit() else None
        r = tot.get(str(u)) or {}
        gp = r.get("gp", 0) or 0
        fgm = (r.get("fg2m", 0) or 0) + (r.get("fg3m", 0) or 0)
        fga = (r.get("fg2a", 0) or 0) + (r.get("fg3a", 0) or 0)
        avg = (lambda k: round((r.get(k, 0) or 0) / gp, 1)) if gp else (lambda k: None)
        rows.append({"name": roblox_name(mem) if mem else str(u), "role": "C" if int(u) == t.get("captain")
                     else "CC" if int(u) == (t.get("co") or 0) else "", "gp": gp, "ppg": avg("pts"),
                     "rpg": avg("reb"), "apg": avg("ast"), "spg": avg("stl"), "bpg": avg("blk"),
                     "fg": round(100 * fgm / fga) if fga else None})
    rows.sort(key=lambda r: (r["gp"] == 0, -(r["ppg"] or 0), r["name"].lower()))
    return rows


def lineup_picture(guild: discord.Guild | None, s: dict, mid: str, e_: dict) -> bytes:
    """The lineup card: both teams side by side, every player with GP, PPG, RPG, APG, SPG, BPG and FG%."""
    from PIL import ImageDraw
    tz = s.get("tourney") or {}
    ev = s.get("event")
    sides = [(e_[k], s["teams"].get(str(e_[k]), {}), lineup_rows(guild, s, e_[k])) for k in ("a", "b")]
    n = max([len(r) for _, _, r in sides] + [ROSTER_MIN])
    W = 1600
    top, row_h = 380, 58
    H = top + 50 + n * row_h + 110
    tlogo = str(LOGO_DIR / tz["logo"]) if tz.get("logo") and (LOGO_DIR / tz["logo"]).exists() else None
    sub = "Lineups · " + stage_heading(e_.get("label", ""), mid).title().replace("Game M", "Game M")
    img, d = _canvas(W, H, tz.get("name", "Tournament"), sub, tlogo)
    WHITE, GREY, DIM, ORANGE = (245, 245, 245), (150, 150, 155), (95, 95, 100), (255, 122, 0)
    if e_.get("time"):
        when = datetime.fromisoformat(e_["time"]).astimezone(tzinfo("ET"))
        wt = when.strftime("%a %b %d · %I:%M %p ET").replace(" 0", " ")
        f = _font(24)
        d.text((W - 50 - d.textlength(wt, font=f), 80), wt, font=f, fill=WHITE)
    cols = [("GP", 50), ("PPG", 86), ("RPG", 74), ("APG", 74), ("SPG", 66), ("BPG", 66), ("FG%", 80)]
    colw = 725
    fn, fs, fh = _font(26), _font(25, bold=False), _font(17)
    for i, (tid, t, rows) in enumerate(sides):
        x0 = 50 + i * (colw + 50)
        # team header
        path = LOGO_DIR / t["logo"] if t.get("logo") else None
        lg = _logo(path if path and path.exists() else None, 110, t.get("name", "TBD"))
        img.paste(lg, (x0, 220), lg)
        name = t.get("name", "TBD").upper()
        f = _fit(d, name, colw - 140, 46, 22)
        d.text((x0 + 130, 232), name, font=f, fill=WHITE)
        w_, l_ = team_record(ev, tid)
        d.text((x0 + 130, 292), f"{w_}-{l_} this tournament · {len(rows)} players", font=_font(22, bold=False), fill=GREY)
        # column heads
        y = top
        d.line([(x0, y + 34), (x0 + colw, y + 34)], fill=(50, 50, 56), width=2)
        d.text((x0, y), "PLAYER", font=fh, fill=GREY)
        cx = x0 + colw
        xs = []
        for lab, cw in reversed(cols):
            cx -= cw
            xs.append(cx)
            d.text((cx + cw - d.textlength(lab, font=fh), y), lab, font=fh, fill=ORANGE if lab == "PPG" else GREY)
        xs = list(reversed(xs))
        name_w = xs[0] - x0 - 20
        for j, r in enumerate(rows):
            yy = top + 50 + j * row_h
            if j % 2 == 0:
                d.rectangle([x0 - 10, yy - 10, x0 + colw + 6, yy + row_h - 14], fill=(18, 18, 22))
            label = r["name"]
            fnn = _fit(d, label, name_w - (52 if r["role"] else 0), 26, 16)
            d.text((x0, yy), label, font=fnn, fill=WHITE)
            if r["role"]:
                bx = x0 + d.textlength(label, font=fnn) + 10
                d.rounded_rectangle([bx, yy + 3, bx + (38 if r["role"] == "CC" else 26), yy + 29], 6, fill=(60, 40, 12))
                d.text((bx + 6, yy + 6), r["role"], font=_font(17), fill=ORANGE)
            vals = [str(r["gp"]), *(("-" if r[k] is None else f"{r[k]:.1f}") for k in ("ppg", "rpg", "apg", "spg", "bpg")),
                    "-" if r["fg"] is None else f"{r['fg']}%"]
            for (lab, cw), xx, v in zip(cols, xs, vals):
                ff = _font(26) if lab == "PPG" else fs
                d.text((xx + cw - d.textlength(v, font=ff), yy), v, font=ff, fill=WHITE if v != "-" else DIM)
        if not rows:
            d.text((x0, top + 50), "No players on the roster", font=fs, fill=DIM)
    d.line([(W // 2, 210), (W // 2, H - 80)], fill=(40, 40, 46), width=2)
    note = f"Season averages, {datetime.now().year} · - = no stats yet · C captain, CC co-captain"
    d.text((50, H - 78), note, font=_font(19, bold=False), fill=DIM)
    return _png(img)


def pickem_locked(e_: dict | None) -> bool:
    if not e_ or e_.get("done"):
        return True
    t = e_.get("time")
    return bool(t) and datetime.now(timezone.utc) >= datetime.fromisoformat(t)


def pickem_embed(s: dict, mid: str, e_: dict, pk: dict) -> discord.Embed:
    picks = pk.get("picks", {})
    na, nb = (sum(1 for v in picks.values() if str(v) == str(e_[k])) for k in ("a", "b"))
    tot = na + nb
    a_name, b_name = team_name(s, e_["a"]), team_name(s, e_["b"])
    head = stage_heading(e_.get("label", ""), mid)
    if pk.get("result"):
        w = pk["result"]
        right = sum(1 for v in picks.values() if str(v) == str(w))
        body = (f"**FINAL:** **{team_name(s, w)}** won" + (f" {pk['score']}" if pk.get("score") else "") + ".\n"
                f"{right} of {tot} called it." if tot else f"**FINAL:** **{team_name(s, w)}** won.")
        color = GOOD
    elif pickem_locked(e_) and e_.get("time"):
        body = f"Picks are locked. The game started {ts(datetime.fromisoformat(e_['time']), 'R')}."
        color = MUTED
    else:
        when = f"{ts(datetime.fromisoformat(e_['time']))} ({ts(datetime.fromisoformat(e_['time']), 'R')})" \
            if e_.get("time") else "the new game time (TBA)"
        body = f"Who wins? Tap a button. You can change your pick until tip-off: {when}."
        color = GOLD
    pct = lambda n: f"{round(100 * n / tot)}%" if tot else "0%"
    e = brand_embed(f"### {head}\n## {a_name} vs {b_name}\n{body}\n\n"
                    f"**{a_name}:** {na} pick(s) · {pct(na)}\n**{b_name}:** {nb} pick(s) · {pct(nb)}",
                    "Pick'em", color)
    e.set_image(url="attachment://lineups.png")
    e.set_footer(text="1 point for every right pick · /pickems for the leaderboard")
    return e


def pickem_view(gid: int, mid: str, s: dict, e_: dict, disabled: bool = False) -> discord.ui.View:
    v = discord.ui.View(timeout=None)
    for k in ("a", "b"):
        v.add_item(discord.ui.Button(label=f"Pick {team_name(s, e_[k])}"[:80], style=discord.ButtonStyle.primary,
                                     custom_id=f"pk:{gid}:{mid}:{e_[k]}", disabled=disabled))
    return v


_pickem_posted: set = set()


async def post_pickem(guild: discord.Guild, s: dict, mid: str, ping: bool = True):
    """Post the game's pick'em once (a later reschedule just updates it, no second @here)."""
    e_ = sched(s)["matches"].get(mid)
    ch = chan(guild, "pickems")
    if not e_ or not e_.get("time") or ch is None:
        return
    pk = pickem_for(s, mid, e_, create=True)
    if pk.get("msg"):
        return await refresh_pickem(guild, s, mid)
    key = (guild.id, mid, e_.get("opened"))
    if key in _pickem_posted:  # already posted by another path a moment ago (data not saved yet)
        return
    _pickem_posted.add(key)
    try:
        png = await asyncio.to_thread(lineup_picture, guild, s, mid, e_)
        msg = await ch.send(content="@here" if ping else None, embed=pickem_embed(s, mid, e_, pk),
                            file=discord.File(io.BytesIO(png), filename="lineups.png"),
                            view=pickem_view(guild.id, mid, s, e_),
                            allowed_mentions=discord.AllowedMentions(everyone=True))
        pk["msg"] = [ch.id, msg.id]
    except Exception as ex:
        _pickem_posted.discard(key)  # let it try again
        print(f"[pickem] {ex}")


async def refresh_pickem(guild: discord.Guild, s: dict, mid: str):
    e_ = sched(s)["matches"].get(mid)
    pk = pickem_for(s, mid, e_)
    if not pk or not pk.get("msg") or not e_:
        return
    try:
        ch = guild.get_channel(int(pk["msg"][0]))
        msg = ch.get_partial_message(int(pk["msg"][1]))
        await msg.edit(embed=pickem_embed(s, mid, e_, pk),
                       view=pickem_view(guild.id, mid, s, e_, disabled=pickem_locked(e_) or bool(pk.get("result"))))
    except (discord.HTTPException, AttributeError) as ex:
        print(f"[pickem refresh] {ex}")


async def pickem_lock_once(guild: discord.Guild):
    """At tip-off: grey out the buttons and show the final split."""
    data = load_data()
    s = guild_signups(data, guild.id)
    changed = False
    for mid in list(pickems(s)["games"]):
        e_ = sched(s)["matches"].get(mid)
        pk = pickem_for(s, mid, e_)
        if not pk or not pk.get("msg") or pk.get("result") or not e_:
            continue
        locked = pickem_locked(e_)
        if locked != bool(pk.get("locked")):
            pk["locked"] = locked
            changed = True
            await refresh_pickem(guild, s, mid)
    # games that already had a time before pick'ems existed (or while the bot was off): post them now,
    # with a single @here for the batch
    if chan(guild, "pickems"):
        first = True
        for mid, e_ in sched(s)["matches"].items():
            if e_.get("done") or not e_.get("time") or pickem_locked(e_):
                continue
            pk = pickem_for(s, mid, e_)
            if pk and pk.get("msg"):
                continue
            await post_pickem(guild, s, mid, ping=first)
            first, changed = False, True
    if changed:
        save_data(data)


async def settle_pickem(guild: discord.Guild, s: dict, m: dict):
    """The result is in: everyone who picked the winner gets a point."""
    mid = str(m["id"])
    pk = pickem_for(s, mid, sched(s)["matches"].get(mid))
    if not pk or pk.get("result") or not m.get("winner"):
        return
    pk["result"], pk["score"] = m["winner"], m.get("score")
    board = pickems(s)["board"]
    for uid, pick in pk.get("picks", {}).items():
        row = board.setdefault(uid, {"right": 0, "picks": 0})
        row["picks"] += 1
        if str(pick) == str(m["winner"]):
            row["right"] += 1
    await refresh_pickem(guild, s, mid)


@bot.listen("on_interaction")
async def pickem_buttons(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return
    cid = (interaction.data or {}).get("custom_id", "")
    if not cid.startswith("pk:"):
        return
    _, gid, mid, tid = cid.split(":", 3)
    guild = bot.get_guild(int(gid))
    if guild is None:
        return
    data = load_data()
    s = guild_signups(data, guild.id)
    e_ = sched(s)["matches"].get(mid)
    pk = pickem_for(s, mid, e_)
    if not e_ or not pk:
        return await interaction.response.send_message("This pick'em is closed.", ephemeral=True)
    if pk.get("result") or pickem_locked(e_):
        return await interaction.response.send_message("Picks are locked: the game has started.", ephemeral=True)
    uid = str(interaction.user.id)
    if str(team_of(s, interaction.user.id) or "") in (str(e_["a"]), str(e_["b"])) and str(team_of(s, interaction.user.id)) != tid:
        return await interaction.response.send_message("You can't pick against your own team.", ephemeral=True)
    before = pk["picks"].get(uid)
    pk["picks"][uid] = tid
    save_data(data)
    name = team_name(s, int(tid) if tid.isdigit() else tid)
    await interaction.response.send_message(
        (f"Changed your pick to **{name}**." if before and before != tid else f"You picked **{name}**.")
        + " You can change it until tip-off.", ephemeral=True)
    try:
        await interaction.message.edit(embed=pickem_embed(s, mid, e_, pk))
    except discord.HTTPException:
        pass


@bot.tree.command(name="postpickem", description="Staff: post the pick'em for games that got a time before pick'ems existed.")
@app_commands.describe(match="One match (e.g. 12 for M12). Leave blank for every upcoming game that doesn't have one",
                       ping="Ping @here (default yes; one ping for the whole batch)")
@app_commands.default_permissions(manage_messages=True)
async def postpickem(interaction: discord.Interaction, match: int | None = None, ping: bool = True):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await ensure_pickems_channel(guild)
    if chan(guild, "pickems") is None:
        return await interaction.response.send_message("I couldn't find or make #pickems.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    sc = sched(s)
    if match is not None:
        mid = str(match)
        e_ = sc["matches"].get(mid)
        if not e_ or e_.get("done"):
            return await interaction.response.send_message(f"M{match} isn't an open match.", ephemeral=True)
        if not e_.get("time"):
            return await interaction.response.send_message(f"M{match} doesn't have a game time yet.", ephemeral=True)
        if pickem_locked(e_):
            return await interaction.response.send_message(f"M{match} has already started, so picks would be locked.",
                                                           ephemeral=True)
        pk = pickem_for(s, mid, e_)
        if pk and pk.get("msg"):
            return await interaction.response.send_message(f"M{match} already has a pick'em in #pickems.", ephemeral=True)
        todo = [mid]
    else:
        todo = sorted((mid for mid, e_ in sc["matches"].items()
                       if not e_.get("done") and e_.get("time") and not pickem_locked(e_)
                       and not (pickem_for(s, mid, e_) or {}).get("msg")),
                      key=lambda m_: sc["matches"][m_]["time"])
        if not todo:
            return await interaction.response.send_message(
                "Every upcoming game with a time already has a pick'em.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    for i, mid in enumerate(todo):
        await post_pickem(guild, s, mid, ping=ping and i == 0)
    save_data(data)
    await interaction.followup.send(f"Posted {len(todo)} pick'em(s) in #pickems: "
                                    + ", ".join(f"M{m_}" for m_ in todo) + ".", ephemeral=True)


@bot.tree.command(name="pickems", description="Pick'em leaderboard (and your own record).")
async def pickems_cmd(interaction: discord.Interaction):
    s = guild_signups(load_data(), interaction.guild.id)
    board = pickems(s)["board"]
    rows = sorted(board.items(), key=lambda kv: (-kv[1]["right"], kv[1]["picks"]))
    if not rows:
        return await interaction.response.send_message("No pick'ems have been settled yet. Make your picks in #pickems.",
                                                       ephemeral=True)
    lines = [f"**{i}.** <@{u}> · {r['right']}/{r['picks']} right ({round(100 * r['right'] / r['picks'])}%)"
             for i, (u, r) in enumerate(rows[:15], 1)]
    me = board.get(str(interaction.user.id))
    mine = (f"\n\n**You:** {me['right']}/{me['picks']} right, #{[u for u, _ in rows].index(str(interaction.user.id)) + 1}"
            if me else "\n\nYou haven't had a pick settled yet.")
    await interaction.response.send_message(embed=brand_embed("\n".join(lines) + mine, "Pick'em leaderboard", GOLD),
                                            ephemeral=True, allowed_mentions=NO_PINGS)


async def confirm_time(guild: discord.Guild, data: dict, mid: str, when: int, by: str):
    s = guild_signups(data, guild.id)
    sc = sched(s)
    e_ = sc["matches"].get(mid)
    if not e_:
        return
    e_["time"] = datetime.fromtimestamp(when, timezone.utc).isoformat(timespec="seconds")
    e_["preset"] = False  # agreed (or set by staff): locked
    e_["reminded"] = passed_reminders(datetime.fromtimestamp(when, timezone.utc))
    for r in sc["requests"].values():
        if r["match"] == mid and r["status"] == "open":
            r["status"] = "closed"
    save_data(data)
    dt = datetime.fromtimestamp(when, timezone.utc)
    await scheduling_post(guild, s, mid, f"**{team_name(s, e_['a'])}** vs **{team_name(s, e_['b'])}**\n"
                                         f"**Game time:** {ts(dt)} ({ts(dt, 'R')})\nSet by {by}.",
                          f"✅ M{mid} is scheduled", GOOD)
    await post_game_card(guild, s, mid)
    await post_game_announcement(guild, s, mid)  # matchup graphic in #game-announcements
    await post_pickem(guild, s, mid)  # #pickems: @here, the lineup card, vote buttons
    save_data(data)
    await dm_teams(guild, s, [e_["a"], e_["b"]], lambda tid: next_match_card(s, mid, tid))
    await dm_game_rules(guild, s, mid)
    schedule_publish(guild)


class SlotPicker(discord.ui.View):
    """Dropdowns of the next 48 hours. mode 'propose' (captain making a request), 'answer' (other captain)."""

    def __init__(self, gid: int, rid: str, groups: list[list], mode: str, offered: list[int] | None = None,
                 tz_code: str = "ET"):
        super().__init__(timeout=None)
        if offered:
            sel = discord.ui.Select(custom_id=f"gt:take:{gid}:{rid}", placeholder="✅ Pick one of their times",
                                    options=[discord.SelectOption(label=slot_label(t, tz_code), value=str(t))
                                             for t in offered[:25]])
            self.add_item(sel)
        for i, opts in enumerate(groups[:2]):
            if not opts:
                continue
            if mode == "propose":
                sel = discord.ui.Select(custom_id=f"gt:prop{i}:{gid}:{rid}", min_values=0, max_values=len(opts),
                                        placeholder=f"Times that work ({'first' if i == 0 else 'second'} 24 hours)",
                                        options=opts)
            else:
                sel = discord.ui.Select(custom_id=f"gt:counter{i}:{gid}:{rid}",
                                        placeholder=f"🔁 None work? Suggest a time ({'first' if i == 0 else 'second'} 24h)",
                                        options=opts)
            self.add_item(sel)
        if mode == "propose":
            self.add_item(discord.ui.Button(label="Send request", emoji="📨", style=discord.ButtonStyle.success,
                                            custom_id=f"gt:send:{gid}:{rid}"))


class TestTimeView(discord.ui.View):
    """/testdraw live mode: the confirm-a-game-time DM, like the real one, for the staff member playing captain.
    Picking a time resolves `fut` with ("take" | "counter", unix time)."""

    def __init__(self, fut: asyncio.Future, offered: list[int], counter: list, tz_code: str):
        super().__init__(timeout=300)
        self.fut = fut
        take = discord.ui.Select(placeholder="✅ Pick one of their times",
                                 options=[discord.SelectOption(label=slot_label(t, tz_code), value=str(t))
                                          for t in offered])
        take.callback = self._pick("take", take)
        self.add_item(take)
        if counter:
            other = discord.ui.Select(placeholder="🔁 None work? Suggest a time (next 24 hours)", options=counter[:25])
            other.callback = self._pick("counter", other)
            self.add_item(other)

    def _pick(self, kind: str, sel: discord.ui.Select):
        async def cb(interaction: discord.Interaction):
            await interaction.response.edit_message(view=None)
            if not self.fut.done():
                self.fut.set_result((kind, int(sel.values[0])))
        return cb


class CounterView(discord.ui.View):
    def __init__(self, gid: int, rid: str):
        super().__init__(timeout=None)
        self.add_item(discord.ui.Button(label="Accept", emoji="✅", style=discord.ButtonStyle.success,
                                        custom_id=f"gt:yes:{gid}:{rid}"))
        self.add_item(discord.ui.Button(label="Decline", emoji="✖", style=discord.ButtonStyle.danger,
                                        custom_id=f"gt:no:{gid}:{rid}"))


def captain_side(s: dict, uid: int, e_: dict):
    for side in ("a", "b"):
        t = s["teams"].get(str(e_[side]))
        if t and int(t["captain"]) == int(uid):
            return side
    return None


@bot.tree.command(description="Captains: request a game time for your tournament match (next 48 hours).")
@app_commands.describe(match="Match number, e.g. 12 for M12",
                       timezone="Timezone the times are shown in (saved for next time)")
@app_commands.choices(timezone=TZ_CHOICES)
async def gametime(interaction: discord.Interaction, match: int, timezone: str | None = None):
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    sc = sched(s)
    e_ = sc["matches"].get(str(match))
    if not e_ or e_["done"]:
        return await interaction.response.send_message(f"M{match} isn't waiting on a game time.", ephemeral=True)
    if e_.get("time") and not can_override(e_):
        return await interaction.response.send_message(
            f"M{match} is locked for {ts(datetime.fromisoformat(e_['time']))}. "
            + "That game has already started. Ask staff if something went wrong.", ephemeral=True)
    side = captain_side(s, interaction.user.id, e_)
    if side is None and not is_staff(interaction.user):
        return await interaction.response.send_message(f"Only the two captains in M{match} can request a time.",
                                                       ephemeral=True)
    if timezone:
        sc["tz"][str(interaction.user.id)] = timezone
    tz_code = sc["tz"].get(str(interaction.user.id), "ET")
    now = datetime.now(timezone_utc())
    end = max(window_end(e_), now + timedelta(hours=2))
    end = min(end, now + timedelta(hours=SCHED_HOURS))
    groups = slot_options(now, end, tz_code, busy=team_busy(sc, (e_["a"], e_["b"]), str(match)))
    if not groups:
        return await interaction.response.send_message("There are no times left before the deadline. Ask staff "
                                                       "to /reschedule.", ephemeral=True)
    rid = str(sc["next"])
    sc["next"] += 1
    sc["drafts"][str(interaction.user.id)] = {"match": str(match), "tz": tz_code, "picks": {}, "rid": rid,
                                              "side": side or "a"}
    save_data(data)
    await interaction.response.send_message(
        embed=brand_embed(f"Pick **every** time that works for your team (times in **{tz_code}**; change with the "
                          f"`timezone` option). Then click **Send request**. The other captain confirms one in DMs.",
                          f"Game time request · M{match}", INFO),
        view=SlotPicker(interaction.guild.id, rid, groups, "propose"), ephemeral=True)



@bot.tree.command(description="Captains: send ONE game time to the other captain to accept or decline (by DM).")
@app_commands.describe(match="Match number, e.g. 12 for M12",
                       time="The time: 8pm, 8:30pm, tomorrow 7pm, sat 6pm (8 = 8 PM)",
                       timezone="Timezone of that time (default: yours from /gametime, or ET)")
@app_commands.choices(timezone=TZ_CHOICES)
async def confirmtime(interaction: discord.Interaction, match: int, time: str, timezone: str | None = None):
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    sc = sched(s)
    mid = str(match)
    e_ = sc["matches"].get(mid)
    if not e_ or e_["done"]:
        return await interaction.response.send_message(f"M{match} isn't waiting on a game time.", ephemeral=True)
    if e_.get("time") and not can_override(e_):
        return await interaction.response.send_message(f"M{match} has already started.", ephemeral=True)
    side = captain_side(s, user.id, e_)
    if side is None:
        return await interaction.response.send_message(f"Only the two captains in M{match} can send a game time.",
                                                       ephemeral=True)
    if timezone:
        sc["tz"][str(user.id)] = timezone
    tz_code = timezone or sc["tz"].get(str(user.id), "ET")
    when, problem = parse_when(time, tz_code)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    now = datetime.now(timezone_utc())
    end = min(max(window_end(e_), now + timedelta(hours=2)), now + timedelta(hours=SCHED_HOURS))
    if when <= now + timedelta(minutes=10):
        return await interaction.response.send_message("Pick a time at least 10 minutes from now.", ephemeral=True)
    if when > end:
        return await interaction.response.send_message(
            f"That's past the scheduling window for M{match}. Pick a time before {ts(end)}.", ephemeral=True)
    if not clear_of(when, team_busy(sc, (e_["a"], e_["b"]), mid)):
        return await interaction.response.send_message(
            "One of the teams already has a game within an hour of that time. Pick another.", ephemeral=True)
    other_side = "b" if side == "a" else "a"
    to_team = s["teams"].get(str(e_[other_side]))
    if not to_team:
        return await interaction.response.send_message("The other team isn't in the server any more. Ask staff.",
                                                       ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    rid = str(sc["next"])
    sc["next"] += 1
    t = int(when.timestamp())
    sc["requests"][rid] = {"match": mid, "from": user.id, "to": int(to_team["captain"]), "from_team": e_[side],
                           "to_team": e_[other_side], "times": [t], "status": "open", "tz": tz_code}
    save_data(data)
    ok = await dm(int(to_team["captain"]), brand_embed(
        f"**{team_name(s, e_[side])}** want to play **M{mid}** ({e_.get('label', '')}) at:\n"
        f"## {ts(when)}\n({ts(when, 'R')}, shown in your local time)\n\n"
        f"Accept to lock it in, or decline and send your own times with `/gametime match:{mid}`.",
        f"Confirm your game time · {guild.name}", GOLD), CounterView(guild.id, rid))
    await interaction.followup.send(
        (f"Sent {ts(when)} to the other captain to confirm. You'll get a DM when they answer." if ok else
         "I couldn't DM the other captain (their DMs are closed). Ask them to open DMs from server members."),
        ephemeral=True)

def timezone_utc():
    return timezone.utc


async def gt_send(guild: discord.Guild, data: dict, user: discord.abc.User, draft: dict):
    s = guild_signups(data, guild.id)
    sc = sched(s)
    mid = draft["match"]
    e_ = sc["matches"][mid]
    times = sorted({int(t) for g in draft["picks"].values() for t in g})
    side = draft["side"]
    other_side = "b" if side == "a" else "a"
    to_team = s["teams"].get(str(e_[other_side]))
    if not to_team:
        return "The other team isn't in the server any more. Ask staff."
    rid = draft["rid"]
    sc["requests"][rid] = {"match": mid, "from": user.id, "to": int(to_team["captain"]), "from_team": e_[side],
                           "to_team": e_[other_side], "times": times, "status": "open", "tz": draft["tz"]}
    sc["drafts"].pop(str(user.id), None)
    save_data(data)
    listing = "\n".join(f"• {ts(datetime.fromtimestamp(t, timezone.utc))}" for t in times)
    # game time requests go by DM only: nothing is posted or pinged in #scheduling
    tz_to = sc["tz"].get(str(to_team["captain"]), draft["tz"])
    now = datetime.now(timezone.utc)
    end = min(max(window_end(e_), now + timedelta(hours=2)), now + timedelta(hours=SCHED_HOURS))
    e = brand_embed(f"**{team_name(s, e_[side])}** want to play **M{mid}** ({e_['label']}) at one of these times "
                    f"(shown in your local time):\n{listing}\n\nPick one below to lock it in. If none work, "
                    f"suggest another time from the other dropdowns.\nDeadline: {ts(datetime.fromisoformat(e_['deadline']))}",
                    f"Confirm your game time · {guild.name}", GOLD)
    ok = await dm(int(to_team["captain"]), e,
                  SlotPicker(guild.id, rid, slot_options(now, end, tz_to, times, team_busy(sc, (e_["a"], e_["b"]), mid)),
                             "answer", [t for t in times if clear_of(datetime.fromtimestamp(t, timezone.utc),
                                                                     team_busy(sc, (e_["a"], e_["b"]), mid))] or times,
                             tz_to))
    return ("Request sent! The other captain got a DM to confirm." if ok else
            "I couldn't DM the other captain (their DMs are closed). Ask them to open DMs from server members, "
            f"or they can send you their own times with `/gametime match:{mid}`.")


@bot.listen("on_interaction")
async def gametime_events(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return
    cid = (interaction.data or {}).get("custom_id", "")
    if not cid.startswith("gt:"):
        return
    _, action, gid, rid = cid.split(":", 3)
    guild = bot.get_guild(int(gid))
    if guild is None:
        return await interaction.response.send_message("I can't find that server any more.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    sc = sched(s)
    values = (interaction.data or {}).get("values", [])
    uid = interaction.user.id

    if action.startswith("prop"):
        d = sc["drafts"].get(str(uid))
        if not d or d["rid"] != rid:
            return await interaction.response.send_message("That request expired. Run /gametime again.", ephemeral=True)
        d["picks"][action] = values
        save_data(data)
        return await interaction.response.defer()
    if action == "send":
        d = sc["drafts"].get(str(uid))
        if not d or d["rid"] != rid:
            return await interaction.response.send_message("That request expired. Run /gametime again.", ephemeral=True)
        if not any(d["picks"].values()):
            return await interaction.response.send_message("Pick at least one time first.", ephemeral=True)
        await interaction.response.defer(ephemeral=True)
        msg = await gt_send(guild, data, interaction.user, d)
        try:
            await interaction.edit_original_response(view=None)
        except discord.HTTPException:
            pass
        return await interaction.followup.send(msg, ephemeral=True)

    r = sc["requests"].get(rid)
    e_ = sc["matches"].get(r["match"], {}) if r else {}
    if not r or r["status"] != "open" or (e_.get("time") and not can_override(e_)):
        return await interaction.response.send_message("This request is closed (the time may already be set).",
                                                       ephemeral=True)
    if action == "take" and uid == r["to"]:
        await interaction.response.edit_message(view=None)
        await confirm_time(guild, data, r["match"], int(values[0]), f"<@{r['from']}> and <@{r['to']}>")
        return await interaction.followup.send(f"✅ Locked in: {ts(datetime.fromtimestamp(int(values[0]), timezone.utc))}. "
                                               "Both teams have been told.")
    if action.startswith("counter") and uid == r["to"]:
        t = int(values[0])
        r["status"] = "countered"
        nid = str(sc["next"])
        sc["next"] += 1
        sc["requests"][nid] = {"match": r["match"], "from": r["to"], "to": r["from"], "from_team": r["to_team"],
                               "to_team": r["from_team"], "times": [t], "status": "open", "tz": r["tz"]}
        save_data(data)
        await interaction.response.edit_message(view=None)
        when = ts(datetime.fromtimestamp(t, timezone.utc))
        await dm(r["from"], brand_embed(f"**{team_name(s, r['to_team'])}** can't do your times for **M{r['match']}**. "
                                        f"They suggested **{when}** instead.", "New time suggested", GOLD),
                 CounterView(guild.id, nid))
        return await interaction.followup.send(f"Sent {when} to the other captain. You'll hear back here.")
    if action == "yes" and uid == r["to"]:
        await interaction.response.edit_message(view=None)
        await confirm_time(guild, data, r["match"], r["times"][0], f"<@{r['from']}> and <@{r['to']}>")
        return await interaction.followup.send("✅ Locked in. Both teams have been told.")
    if action == "no" and uid == r["to"]:
        r["status"] = "declined"
        save_data(data)
        await interaction.response.edit_message(view=None)
        await dm(r["from"], brand_embed(f"**{team_name(s, r['to_team'])}** declined your times for **M{r['match']}**. "
                                        f"Send new ones with `/gametime match:{r['match']}`.",
                                        f"Time declined · M{r['match']}", MUTED))
        return await interaction.followup.send(f"Declined. Send your own times with `/gametime match:{r['match']}`.")
    await interaction.response.send_message("This isn't your request to answer.", ephemeral=True)


# ---------------------------------------------------------------- game settings (#game-rules + match DMs)
#
# The in-game settings every league game uses, and how to report the score. Posted in #game-rules
# (/setupbot part:gamerules) and DMed to both teams' captains and co-captains when a game time is confirmed.
# Change a setting here and run /setupbot part:gamerules to repost.

GAME_SETTINGS = [("Court", "1"), ("Quarters", "2"), ("Quarter Length", "10:00"), ("Half Time", "true"),
                 ("Fouls", "true"), ("Free Throws", "false"), ("Shotclock", "24 sec"), ("Intros", "true")]

REPORT_STEPS = [
    "**Public gym:** take a **screenshot of the stats** at the end of the game.",
    "**League gym:** **export the stats** from the game.",
    "Within **1 hour**, a captain or co-captain runs **`/game_score`** with the match number, the winning team and "
    "the score (winner's points first, e.g. 52-44), and attaches the screenshot or export.",
    "The **other team's** captain or co-captain confirms it with the button (in #score-reports or their DMs). "
    "Once both teams agree, the result is final.",
    "Don't agree? Hit **Dispute** and an admin decides. Admins can also record or fix a score directly.",
]


def game_settings_text() -> str:
    return "\n".join(f"**{k}:** `{v}`" for k, v in GAME_SETTINGS)


def game_rules_embed(title: str = "🏀 Game settings & score reports", intro: str | None = None) -> discord.Embed:
    e = brand_embed((intro + "\n\n" if intro else "")
                    + "**Set the game up with these settings before tip-off:**\n" + game_settings_text()
                    + "\n\n**After the game: reporting the score**\n" + "\n".join(f"• {x}" for x in REPORT_STEPS)
                    + "\n\nWrong settings? Stop and restart before the first basket, or the result stands.",
                    title, 0xA855F7)
    return e


def captains_of(s: dict, tid) -> list[int]:
    t = s["teams"].get(str(tid)) or {}
    return [int(u) for u in (t.get("captain"), t.get("co")) if u]


async def dm_game_rules(guild: discord.Guild, s: dict, mid: str):
    """Game time confirmed: captains and co-captains of both teams get the settings + how to report."""
    e_ = sched(s)["matches"].get(mid)
    if not e_ or not e_.get("time"):
        return
    when = datetime.fromisoformat(e_["time"])
    for tid in (e_["a"], e_["b"]):
        other = e_["b"] if tid == e_["a"] else e_["a"]
        intro = (f"### {stage_heading(e_.get('label', ''), mid)}\n**{team_name(s, tid)}** vs **{team_name(s, other)}** · "
                 f"{ts(when)} ({ts(when, 'R')})\nYou're a captain, so you're getting the game settings and how to "
                 "report the score.")
        for uid in captains_of(s, tid):
            await dm(uid, game_rules_embed(f"Game confirmed · M{mid}", intro))


async def gamerulessetup(interaction: discord.Interaction):
    """/setupbot part:gamerules: make #game-rules if needed, clear it and post the settings as an announcement."""
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    ch = chan(guild, "game-rules")
    if ch is None:
        cat = await get_or_make_category(guild, "MATCHES")
        ch = await guild.create_text_channel("game-rules", category=cat, overwrites=overwrites_for(guild, "ro"),
                                             position=0, topic="The settings every league game uses, and how to "
                                                                "report the score.")
    try:
        await ch.purge(limit=50)
    except discord.HTTPException:
        pass
    await ch.send(embed=game_rules_embed(
        "📢 League game settings",
        "Every ON THE RISE game is played with these settings. Captains and co-captains also get them in DMs "
        "when a game time is confirmed."))
    await interaction.followup.send(f"Posted the game settings in {ch.mention}.", ephemeral=True)


# ---------------------------------------------------------------- claimed streams going live (@here in live-now)
#
# Twitch links (when TWITCH_CLIENT_ID + TWITCH_CLIENT_SECRET are set): the bot checks Twitch every minute from
# 15 minutes before the game until 3 hours after, and posts in the live-now channel with @here the moment the
# stream is actually on. The website's Watch button only shows while it's really live. When the stream ends the
# post is marked "Stream ended". Any other link (YouTube, Kick, TikTok...) or no Twitch keys: the post goes out at
# game time instead. Free keys: dev.twitch.tv/console -> Register Your Application (category: Chat Bot or
# Other, redirect URL http://localhost) -> copy the Client ID and make a New Secret.

TWITCH_CLIENT_ID = os.environ.get("TWITCH_CLIENT_ID", "").strip()
TWITCH_CLIENT_SECRET = os.environ.get("TWITCH_CLIENT_SECRET", "").strip()
if TWITCH_CLIENT_ID.startswith("PASTE") or TWITCH_CLIENT_SECRET.startswith("PASTE"):
    TWITCH_CLIENT_ID = TWITCH_CLIENT_SECRET = ""  # placeholders from start_bot.bat: Twitch checks off
_twitch_token: dict = {"token": None, "until": 0.0}


def twitch_login(link: str | None) -> str | None:
    m = re.match(r"^https?://(?:www\.|m\.)?twitch\.tv/([A-Za-z0-9_]{3,25})/?(?:\?.*)?$", (link or "").strip())
    return m.group(1).lower() if m else None


def stream_platform(link: str | None) -> str:
    l = (link or "").lower()
    return ("Twitch" if "twitch.tv" in l else "YouTube" if "youtube.com" in l or "youtu.be" in l
            else "Kick" if "kick.com" in l else "TikTok" if "tiktok.com" in l else "Stream")


def twitch_tracked(link: str | None) -> bool:
    return bool(TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET and twitch_login(link))


async def twitch_live(logins: list[str]) -> dict[str, dict] | None:
    """Which of these Twitch channels are live right now: login -> {title, viewers}. None if Twitch can't be reached."""
    if not logins:
        return {}
    import time as _time
    try:
        async with aiohttp.ClientSession() as session:
            if not _twitch_token["token"] or _time.time() > _twitch_token["until"]:
                async with session.post("https://id.twitch.tv/oauth2/token",
                                        params={"client_id": TWITCH_CLIENT_ID, "client_secret": TWITCH_CLIENT_SECRET,
                                                "grant_type": "client_credentials"}) as r:
                    if r.status != 200:
                        print(f"[twitch] login failed ({r.status}): check TWITCH_CLIENT_ID / TWITCH_CLIENT_SECRET")
                        return None
                    j = await r.json()
                    _twitch_token["token"] = j["access_token"]
                    _twitch_token["until"] = _time.time() + int(j.get("expires_in", 3600)) - 300
            out = {}
            for i in range(0, len(logins), 100):
                params = [("user_login", x) for x in logins[i:i + 100]]
                async with session.get("https://api.twitch.tv/helix/streams", params=params,
                                       headers={"Client-Id": TWITCH_CLIENT_ID,
                                                "Authorization": f"Bearer {_twitch_token['token']}"}) as r:
                    if r.status == 401:
                        _twitch_token["token"] = None
                        return None
                    if r.status != 200:
                        return None
                    for st in (await r.json()).get("data", []):
                        out[st["user_login"].lower()] = {"title": st.get("title", ""), "viewers": st.get("viewer_count", 0)}
            return out
    except Exception as e:
        print(f"[twitch] {e}")
        return None


def live_channel(guild: discord.Guild, s: dict):
    return guild.get_channel(media(s)["chans"].get("live") or 0) or discord.utils.find(
        lambda c: c.name.endswith("live-now"), guild.text_channels)


def live_post_embed(s: dict, mid: str, e_: dict, title: str | None, ended: bool = False) -> discord.Embed:
    link = e_.get("stream_link")
    host = re.sub(r"^https?://(www\.)?", "", link).split("/")[0] if link else ""
    tz = (s.get("tourney") or {}).get("name", "Tournament")
    text = (f"### {stage_heading(e_.get('label', ''), mid)}\n{team_emoji(s, e_['a'])}**{team_name(s, e_['a'])}** vs "
            f"{team_emoji(s, e_['b'])}**{team_name(s, e_['b'])}**"
            f"\n<@{e_['stream']}> is streaming it" + (f": *{title[:120]}*" if title else "") + "\n\n"
            + (f"▶ **[Watch on {host}]({link})**" if link and not ended else "The stream has ended. Thanks for watching!"))
    e = brand_embed(text, "⚫ STREAM ENDED" if ended else f"🔴 LIVE NOW · {tz}", MUTED if ended else 0xEF4444,
                    url=None if ended else link)
    return e


async def post_stream_live(guild: discord.Guild, s: dict, mid: str, e_: dict, title: str | None = None):
    ch = live_channel(guild, s)
    if ch is None:
        return
    view = None
    if e_.get("stream_link"):
        view = discord.ui.View()
        view.add_item(discord.ui.Button(label="Watch", emoji="▶", url=e_["stream_link"]))
    kw = {"content": "@here", "embed": live_post_embed(s, mid, e_, title),
          "allowed_mentions": discord.AllowedMentions(everyone=True, users=False, roles=False)}
    if view:
        kw["view"] = view
    try:
        msg = await ch.send(**kw)
        e_["live_msg"] = [ch.id, msg.id]
    except discord.HTTPException as ex:
        print(f"[stream live] {ex}")


async def stream_watch_once(guild: discord.Guild, s: dict, now: datetime) -> bool:
    """Called every minute by the match watcher. Returns True if anything changed."""
    sc = sched(s)
    changed = False
    todo = []
    for mid, e_ in sc["matches"].items():
        if not e_.get("stream") or not e_.get("time") or e_.get("done") and not e_.get("on_air"):
            continue
        gt = datetime.fromisoformat(e_["time"])
        if now < gt - timedelta(minutes=15) or now > gt + timedelta(hours=3):
            if e_.get("on_air") and now > gt + timedelta(hours=3):
                todo.append((mid, e_, None))
            continue
        todo.append((mid, e_, twitch_login(e_.get("stream_link")) if twitch_tracked(e_.get("stream_link")) else None))
    logins = sorted({lg for _m, _e, lg in todo if lg})
    live = await twitch_live(logins) if logins else {}
    for mid, e_, lg in todo:
        gt = datetime.fromisoformat(e_["time"])
        if lg and live is not None:
            on = lg in live
            if on and not e_.get("on_air"):
                e_["on_air"] = True
                changed = True
                if not e_.get("live_posted"):
                    e_["live_posted"] = True
                    await post_stream_live(guild, s, mid, e_, live[lg].get("title"))
            elif not on and e_.get("on_air"):
                e_["on_air"] = False
                changed = True
                if e_.get("live_msg"):  # mark the post as ended
                    try:
                        ch = guild.get_channel(e_["live_msg"][0])
                        await ch.get_partial_message(e_["live_msg"][1]).edit(
                            content=None, embed=live_post_embed(s, mid, e_, None, ended=True), view=None)
                    except (discord.HTTPException, AttributeError):
                        pass
        elif (not lg or live is None) and not e_.get("live_posted") and now >= gt and not e_.get("done"):
            e_["live_posted"] = True  # no live check for this link (or Twitch is down): post at game time
            changed = True
            await post_stream_live(guild, s, mid, e_)
        elif not lg and e_.get("on_air"):
            e_["on_air"] = False
            changed = True
    if changed:
        schedule_publish(guild)
    return changed


# ---------------------------------------------------------------- game cards (Arena Host + Claim Stream)
#
# When a match gets its game time, a card goes in #schedule: which stage/round/group and game it is, the
# time, and two buttons. Arena Host (staff, Referees or the "Arena Host" role) claims hosting the private
# server and can name the arena; Claim Stream (Streamer, Media or staff) claims the stream and can add a link.
# Click your own claim again to drop it. The host and streamer are DMed with the reminders too.

_test_cards: dict[str, dict] = {}  # /testdraw cards: "t<match>" -> card info (kept in memory only)


def stage_heading(label: str, mid) -> str:
    """'GROUP A · ROUND 2 · GAME M14', 'SWISS · ROUND 3 · GAME M9', 'MAIN DRAW · WINNERS R1 · GAME M23'."""
    lab = (label or "").strip()
    if lab.lower().startswith("group"):
        head = lab
    elif lab.lower().startswith("swiss"):
        head = "Swiss · " + lab[5:].strip()
    elif lab.lower().startswith("consolation"):
        head = "Consolation · " + lab[11:].strip()
    else:
        head = "Main draw · " + lab if lab else "Main draw"
    return f"{head} · Game M{mid}".upper()


def game_card(e_: dict, mid, a_txt: str, b_txt: str, tname: str) -> discord.Embed:
    when = datetime.fromisoformat(e_["time"])
    arena = e_.get("arena") or "TBD"
    e = brand_embed(f"### {stage_heading(e_.get('label', ''), mid)}\n"
                    f"## Schedule @ {ts(when, 't')}\n"
                    f"{a_txt} vs {b_txt}\n{ts(when, 'D')}\n\n"
                    f"Your game starts {ts(when, 'R')} (arena: **{arena}**). The arena host and a streamer can claim "
                    "it below; both teams get reminders before tip-off.", None, GOLD)
    host, stream = e_.get("host"), e_.get("stream")
    # the name in bold as well as the @mention, so it always shows who claimed it (even if the mention can't load)
    e.add_field(name="🎮 Game Host", value=(f"**{e_.get('host_name') or 'Claimed'}**\n<@{host}>" if host else "Not set"),
                inline=True)
    e.add_field(name="📺 Stream", value=(f"**{e_.get('stream_name') or 'Claimed'}**\n<@{stream}>"
                                        + (f"\n[Watch]({e_['stream_link']})" if e_.get("stream_link") else ""))
                if stream else "Not claimed", inline=True)
    e.set_footer(text=f"{LEAGUE_NAME}: {tname}")
    return e


def game_card_view(gid: int, key: str, e_: dict | None = None) -> discord.ui.View:
    """The claim buttons. Once claimed, the button says who has it."""
    e_ = e_ or {}
    v = discord.ui.View(timeout=None)
    host_lbl = f"Host: {e_['host_name']}"[:80] if e_.get("host") and e_.get("host_name") else "Arena Host"
    stream_lbl = f"Streamed by {e_['stream_name']}"[:80] if e_.get("stream") and e_.get("stream_name") else "Claim Stream"
    v.add_item(discord.ui.Button(label=host_lbl, emoji="🎮", style=discord.ButtonStyle.secondary,
                                 custom_id=f"gc:host:{gid}:{key}"))
    v.add_item(discord.ui.Button(label=stream_lbl, emoji="📺",
                                 style=discord.ButtonStyle.success if e_.get("stream") else discord.ButtonStyle.primary,
                                 custom_id=f"gc:stream:{gid}:{key}"))
    return v


def can_claim(member, what: str) -> bool:
    names = {r.name for r in getattr(member, "roles", [])}
    if is_staff(member):
        return True
    return bool(names & ({"Referee", "Arena Host"} if what == "host" else {"Streamer", "Media"}))


async def post_game_card(guild: discord.Guild, s: dict, mid: str):
    """Post (or update, if the time moved) the match's card in #schedule."""
    e_ = sched(s)["matches"][mid]
    ch = chan(guild, "schedule")
    if ch is None or not e_.get("time"):
        return
    tname = (s.get("tourney") or {}).get("name", "Tournament")
    emb = game_card(e_, mid, tag(e_["a"]), tag(e_["b"]), tname)
    old_card, old_time = e_.get("card"), e_.get("card_time")
    if old_card and old_time == e_["time"]:  # same time (a claim etc.): just refresh the card in place
        try:
            msg = await (guild.get_channel(int(old_card[0])) or ch).fetch_message(int(old_card[1]))
            await msg.edit(embed=emb, view=game_card_view(guild.id, mid, e_))
            return
        except discord.HTTPException:
            pass
    if old_card:  # the time moved: take the old card down and post a fresh one with the new time
        if old_time:
            emb.description = f"**🔁 Rescheduled** (was {ts(datetime.fromisoformat(old_time))})\n" + (emb.description or "")
        try:
            oc = guild.get_channel(int(old_card[0])) or ch
            await (await oc.fetch_message(int(old_card[1]))).delete()
        except (discord.HTTPException, AttributeError):
            pass
    msg = await ch.send(embed=emb, view=game_card_view(guild.id, mid, e_), allowed_mentions=NO_PINGS)
    e_["card"], e_["card_time"] = [ch.id, msg.id], e_["time"]
    if old_card:
        redo_schedule_soon(guild)


def stream_links(s: dict) -> dict:
    return s.setdefault("streamers", {})  # user id -> their stream link (asked for on their first claim)


def good_link(text: str | None) -> str | None:
    t = (text or "").strip()
    if not re.match(r"^https?://\S+\.\S+$", t):
        return None
    return t[:200]


class ClaimModal(discord.ui.Modal):
    def __init__(self, what: str, gid: int, key: str):
        super().__init__(title="Host this game" if what == "host" else "Your stream link (first time)",
                         custom_id=f"gcm:{what}:{gid}:{key}")
        self.add_item(discord.ui.TextInput(
            label="Arena / private server (optional)" if what == "host" else "Stream link (saved for next time)",
            required=what != "host", max_length=200,
            placeholder="e.g. Arena 3 or the server name" if what == "host" else "https://twitch.tv/yourname"))


async def apply_claim(interaction: discord.Interaction, what: str, gid: int, key: str, extra: str | None):
    """Claim / unclaim host or stream on a game card, then redraw the card."""
    test = key.startswith("t")
    data = None
    if test:
        info = _test_cards.get(key)
        if not info:
            return await interaction.response.send_message("That test game is over.", ephemeral=True)
        e_, a_txt, b_txt, tname = info["e"], info["a"], info["b"], info["tname"]
    else:
        data = load_data()
        s = guild_signups(data, gid)
        e_ = sched(s)["matches"].get(key)
        if not e_ or not e_.get("time"):
            return await interaction.response.send_message("That game isn't scheduled any more.", ephemeral=True)
        a_txt, b_txt, tname = tag(e_["a"]), tag(e_["b"]), (s.get("tourney") or {}).get("name", "Tournament")
    field = "host" if what == "host" else "stream"
    uid = interaction.user.id
    if field == "stream" and extra is not None:
        link = good_link(extra)
        if not link:
            return await interaction.response.send_message(
                "That doesn't look like a stream link. Use the full link, like https://twitch.tv/yourname.",
                ephemeral=True)
        extra = link
        d2 = data if data is not None else load_data()
        stream_links(guild_signups(d2, gid))[str(uid)] = link
        if data is None:
            save_data(d2)
    if e_.get(field) == uid and extra is None:  # clicked your own claim: drop it
        e_[field] = None
        e_[field + "_name"] = None
        if field == "host":
            e_["arena"] = None
        else:
            e_["stream_link"] = None
        note = "You're no longer the arena host." if field == "host" else "You dropped the stream."
    else:
        if field == "stream" and e_.get("stream") != uid:
            e_["live_posted"] = e_["on_air"] = False
        e_[field] = uid
        e_[field + "_name"] = getattr(interaction.user, "display_name", None) or interaction.user.name
        if extra:
            if field == "host":
                e_["arena"] = extra.strip()[:60]
            else:
                e_["stream_link"] = extra
        note = "You're hosting this game. Thanks!" if field == "host" else "You've got the stream. Thanks!"
    if data is not None:
        save_data(data)
        g = bot.get_guild(gid)
        if g:
            schedule_publish(g)  # the website shows who's streaming
    emb = game_card(e_, key.lstrip("t"), a_txt, b_txt, tname)
    if not test and field == "stream":
        g_ = bot.get_guild(gid)
        if g_:
            asyncio.create_task(update_announcement_stream(g_, e_))
    if interaction.type == discord.InteractionType.component:
        await interaction.response.edit_message(embed=emb, view=game_card_view(gid, key, e_))
        if field == "stream" and e_.get(field) == uid:
            note += f" Using your saved link: {e_.get('stream_link')} (change it with /streamlink)."
        await interaction.followup.send(note, ephemeral=True)
    else:  # from the modal
        await interaction.response.send_message(note, ephemeral=True)
        try:
            ch = interaction.channel
            if ch is not None and e_.get("card"):
                await ch.get_partial_message(e_["card"][1]).edit(embed=emb, view=game_card_view(gid, key, e_))
            elif interaction.message is not None:
                await interaction.message.edit(embed=emb, view=game_card_view(gid, key, e_))
        except discord.HTTPException:
            pass


@bot.listen("on_interaction")
async def game_card_events(interaction: discord.Interaction):
    cid = (interaction.data or {}).get("custom_id", "")
    if interaction.type == discord.InteractionType.component and cid.startswith("gc:"):
        _, what, gid, key = cid.split(":", 3)
        if not can_claim(interaction.user, what):
            need = "a Referee, the Arena Host role or staff" if what == "host" else "the Streamer or Media role"
            return await interaction.response.send_message(f"You need {need} to claim that.", ephemeral=True)
        if key.startswith("t"):
            e_ = (_test_cards.get(key) or {}).get("e", {})
        else:
            e_ = sched(guild_signups(load_data(), int(gid)))["matches"].get(key, {})
        field = "host" if what == "host" else "stream"
        holder = e_.get(field)
        if holder == interaction.user.id:
            return await apply_claim(interaction, what, int(gid), key, None)
        if holder and not is_staff(interaction.user):
            return await interaction.response.send_message(
                f"<@{holder}> already claimed that. Ask them or staff if it needs to change.", ephemeral=True,
                allowed_mentions=NO_PINGS)
        if what == "stream":  # streamed before? use the saved link, no form
            saved = stream_links(guild_signups(load_data(), int(gid))).get(str(interaction.user.id))
            if saved:
                return await apply_claim(interaction, what, int(gid), key, saved)
        return await interaction.response.send_modal(ClaimModal(what, int(gid), key))
    if interaction.type == discord.InteractionType.modal_submit and cid.startswith("gcm:"):
        _, what, gid, key = cid.split(":", 3)
        comps = (interaction.data or {}).get("components", [])
        val = ""
        for row in comps:
            for c in row.get("components", []):
                val = c.get("value") or ""
        return await apply_claim(interaction, what, int(gid), key, val)


@bot.tree.command(description="Streamers: set or change the stream link used when you claim a game.")
@app_commands.describe(link="Your stream link, e.g. https://twitch.tv/yourname")
async def streamlink(interaction: discord.Interaction, link: str):
    good = good_link(link)
    if not good:
        return await interaction.response.send_message("Use the full link, like https://twitch.tv/yourname.",
                                                       ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    stream_links(s)[str(interaction.user.id)] = good
    moved = 0
    for e_ in sched(s)["matches"].values():  # games you've already claimed use the new link too
        if e_.get("stream") == interaction.user.id and not e_.get("done"):
            e_["stream_link"] = good
            moved += 1
    save_data(data)
    schedule_publish(interaction.guild)
    await interaction.response.send_message(f"Saved: {good}" + (f" (updated {moved} game(s) you're streaming)."
                                                                if moved else ""), ephemeral=True)


@bot.tree.command(description="Staff: the first evening slot the bot uses when captains don't agree a time (default 8 PM ET).")
@app_commands.describe(time="Clock time as HH:MM (24-hour), e.g. 20:00 for 8 PM", timezone="Timezone (default ET)")
@app_commands.choices(timezone=TZ_CHOICES)
@app_commands.default_permissions(manage_roles=True)
async def presettime(interaction: discord.Interaction, time: str, timezone: str = "ET"):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    if not re.match(r"^([01]?\d|2[0-3]):[0-5]\d$", time.strip()):
        return await interaction.response.send_message("Use a time like 20:00 or 19:30.", ephemeral=True)
    data = load_data()
    sc = sched(guild_signups(data, interaction.guild.id))
    hh, mm = time.strip().split(":")
    sc["preset"] = {"time": f"{int(hh):02d}:{mm}", "tz": timezone}
    save_data(data)
    await interaction.response.send_message(
        f"If captains don't agree a time, the bot sets the first open slot from **{preset_text(sc)}** "
        "(then every 30 minutes until 11:30 PM, then the next evening). They can still move it with /gametime if both confirm.",
        ephemeral=True)


@bot.tree.command(description="Staff only: move a game to a new time, or cancel it (even mid-game). No captain OK needed.")
@app_commands.describe(match="Match number, e.g. 12 for M12",
                       time="New time: 8pm, 8:30pm, tomorrow 9pm, sat 8pm, or 2026-11-24 20:00",
                       timezone="Timezone of that time (default ET)", reason="Why (sent to both teams, optional)",
                       cancel="Cancel the game instead, even one being played now (back to TBA, rescheduled after)")
@app_commands.choices(timezone=TZ_CHOICES)
@app_commands.default_permissions(manage_roles=True)
async def reschedule(interaction: discord.Interaction, match: int, time: str | None = None, timezone: str = "ET",
                     reason: str | None = None, cancel: bool = False):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can reschedule games.", ephemeral=True)
    if cancel:
        return await cancel_game_time(interaction, match, reason, force=True)  # works even mid-game
    if not time:
        return await interaction.response.send_message("Give the new `time`, or set `cancel:True`.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    sc = sched(s)
    mid = str(match)
    e_ = sc["matches"].get(mid)
    if not e_ or e_["done"]:
        return await interaction.response.send_message(f"M{match} isn't an open match.", ephemeral=True)
    raw = time.strip()
    m_ = re.fullmatch(r"(\d{4}-\d{2}-\d{2})\s+(\d{1,2}:\d{2})", raw)
    if m_:
        try:
            when = datetime.strptime(f"{m_.group(1)} {m_.group(2)}", "%Y-%m-%d %H:%M").replace(
                tzinfo=tzinfo(timezone)).astimezone(timezone_utc())
        except ValueError:
            return await interaction.response.send_message("That date isn't real.", ephemeral=True)
    else:
        when, problem = parse_when(raw, timezone)
        if problem:
            return await interaction.response.send_message(problem, ephemeral=True)
    if when <= datetime.now(timezone_utc()):
        return await interaction.response.send_message("That time has already passed.", ephemeral=True)
    warn = "" if clear_of(when, team_busy(sc, (e_["a"], e_["b"]), mid)) else \
        "\n⚠️ One of the teams has another game within an hour of that time."
    old = datetime.fromisoformat(e_["time"]) if e_.get("time") else None
    e_.pop("priority", None)  # staff decided: any priority claim is settled
    await interaction.response.defer(ephemeral=True)
    by = f"staff ({interaction.user.mention})" + (f": {reason[:200]}" if reason else "")
    await confirm_time(guild, data, mid, int(when.timestamp()), by)
    for t in (e_["a"], e_["b"]):
        tc = guild.get_channel(int(s["teams"].get(str(t), {}).get("channel") or 0))
        if tc:
            try:
                await tc.send(embed=brand_embed(
                    f"Staff moved **M{mid}** vs **{team_name(s, e_['b'] if t == e_['a'] else e_['a'])}**"
                    + (f" from {ts(old)}" if old else "") + f" to **{ts(when)}** ({ts(when, 'R')})."
                    + (f"\n**Reason:** {reason[:200]}" if reason else ""), f"📅 Rescheduled · M{mid}", GOLD),
                    allowed_mentions=NO_PINGS)
            except discord.HTTPException:
                pass
    log = chan(guild, "mod-log")
    if log:
        await post(log, f"{interaction.user.mention} rescheduled **M{mid}**" + (f" from {ts(old)}" if old else "")
                   + f" to {ts(when)}." + (f"\n**Reason:** {reason[:200]}" if reason else ""), title="📅 Rescheduled",
                   color=INFO)
    await interaction.followup.send(f"M{mid} is now {ts(when)} ({ts(when, 'R')}). Both teams were told.{warn}",
                                    ephemeral=True)


@bot.tree.command(description="Captains or staff: cancel a match's game time (e.g. confirmed by accident).")
@app_commands.describe(match="Match number, e.g. 12 for M12", reason="Why (optional, sent to the other captain)")
async def canceltime(interaction: discord.Interaction, match: int, reason: str | None = None):
    await cancel_game_time(interaction, match, reason, force=False)


async def cancel_game_time(interaction: discord.Interaction, match: int, reason: str | None = None,
                           force: bool = False):
    """Clear a game's time (back to TBA). force=True (staff /reschedule cancel) also works on a game that has
    already started or is being played right now."""
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    sc = sched(s)
    mid = str(match)
    e_ = sc["matches"].get(mid)
    if not e_ or e_["done"]:
        return await interaction.response.send_message(f"M{match} isn't an open match.", ephemeral=True)
    mine = [t for t in (e_["a"], e_["b"]) if user.id in captains_of(s, t)]
    if not mine and not is_official(user):
        return await interaction.response.send_message(
            f"Only the captains and co-captains in M{match} (or staff) can cancel its game time.", ephemeral=True)
    if not e_.get("time"):
        return await interaction.response.send_message(f"M{match} doesn't have a game time yet.", ephemeral=True)
    live_now = not can_override(e_)
    if live_now and not force:
        return await interaction.response.send_message(
            f"M{match} has already started, so its time can't be cancelled. Ask staff "
            "(they can use `/reschedule cancel:True`).", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    old = datetime.fromisoformat(e_["time"])
    now = datetime.now(timezone.utc)
    e_["time"], e_["preset"], e_["reminded"] = None, False, []
    e_.pop("on_air", None)
    e_["live_posted"] = False  # the stream can be shouted again for the new time
    # a fresh 24 hours to agree a new time (more if the original deadline is still further away)
    dl = max(datetime.fromisoformat(e_["deadline"]), now + timedelta(hours=24))
    e_["deadline"] = dl.isoformat(timespec="seconds")
    if e_.get("window_end"):
        e_["window_end"] = max(datetime.fromisoformat(e_["window_end"]), dl).isoformat(timespec="seconds")
    for r in sc["requests"].values():
        if r["match"] == mid and r["status"] == "open":
            r["status"] = "closed"
    card = e_.pop("card", None)
    e_.pop("card_time", None)
    redo_schedule_soon(guild)
    asyncio.create_task(refresh_pickem(guild, s, mid))
    await drop_game_announcement(guild, e_)
    save_data(data)
    if card:  # the game card in #schedule is out of date now
        try:
            ch = guild.get_channel(int(card[0]))
            await (await ch.fetch_message(int(card[1]))).delete()
        except Exception:
            pass
    if e_.get("live_msg"):  # a "LIVE NOW" stream post: mark it over
        try:
            lc = guild.get_channel(e_["live_msg"][0])
            await lc.get_partial_message(e_["live_msg"][1]).edit(
                content=None, embed=live_post_embed(s, mid, e_, None, ended=True), view=None)
        except (discord.HTTPException, AttributeError, KeyError):
            pass
    who = (team_name(s, mine[0]) if mine else "Staff")
    text = (f"The game time for **M{mid}** ({team_name(s, e_['a'])} vs {team_name(s, e_['b'])}), "
            f"{ts(old)}, was **cancelled** by {user.mention} ({who})."
            + (" The game in progress is stopped and doesn't count." if live_now else "")
            + (f"\n**Reason:** {reason[:200]}" if reason else "")
            + f"\n\nSend new times with `/gametime match:{mid}`. Agree one by {ts(dl)} ({ts(dl, 'R')}), "
              "or the bot picks one for staff to confirm.")
    for t in (e_["a"], e_["b"]):
        for uid in captains_of(s, t):
            if uid != user.id:
                await dm(uid, brand_embed(text, f"Game time cancelled · M{mid}", MUTED))
    if force:  # staff: also tell both team channels and keep a record
        for t in (e_["a"], e_["b"]):
            tc = guild.get_channel(int(s["teams"].get(str(t), {}).get("channel") or 0))
            if tc:
                try:
                    await tc.send(content=f"<@&{t}>", embed=brand_embed(text, f"🛑 Game cancelled · M{mid}", MUTED),
                                  allowed_mentions=discord.AllowedMentions(roles=True))
                except discord.HTTPException:
                    pass
        log = chan(guild, "mod-log")
        if log:
            await post(log, f"{user.mention} cancelled **M{mid}**'s game ({ts(old)})"
                       + (" while it was being played" if live_now else "") + "."
                       + (f"\n**Reason:** {reason[:200]}" if reason else ""), title="🛑 Game cancelled", color=MUTED)
    schedule_publish(guild)
    await interaction.followup.send(
        f"M{mid}'s game time is cancelled" + (" (it was in progress)" if live_now else "") + ". Both teams were told. "
        f"They schedule it again with `/gametime match:{mid}` by {ts(dl)}, or set a new time now with "
        f"`/reschedule match:{mid} time:...`.", ephemeral=True)


@bot.tree.command(description="See your team's next tournament match and game time.")
async def nextgame(interaction: discord.Interaction):
    s = guild_signups(load_data(), interaction.guild.id)
    key = team_of(s, interaction.user.id)
    if not key:
        return await interaction.response.send_message("You're not on a team.", ephemeral=True)
    sc = sched(s)
    mine = [(mid, e_) for mid, e_ in sc["matches"].items() if not e_["done"] and key in (str(e_["a"]), str(e_["b"]))]
    if not mine:
        return await interaction.response.send_message("Your team has no match waiting right now.", ephemeral=True)
    mid, _e = min(mine, key=lambda kv: int(kv[0]))
    await interaction.response.send_message(embed=next_match_card(s, mid, key), ephemeral=True)


@bot.tree.command(description="Turn your match DMs (new matches, game times, reminders) on or off.")
async def matchdms(interaction: discord.Interaction):
    data = load_data()
    muted = sched(guild_signups(data, interaction.guild.id))["muted"]
    if interaction.user.id in muted:
        muted.remove(interaction.user.id)
        msg = "🔔 Match DMs are **on**."
    else:
        muted.append(interaction.user.id)
        msg = "🔕 Match DMs are **off**. You'll still see everything in #schedule and #scheduling."
    save_data(data)
    await interaction.response.send_message(msg, ephemeral=True)


async def five_minute_call(guild: discord.Guild, s: dict, mid: str, e_: dict, gt: datetime, minutes: int = 5,
                           by: str | None = None):
    """Before tip-off (5 minutes automatically, or /arenacall): each team's channel (team pinged) and its
    captain/co-captain DMs: join the arena host's private server now."""
    mins = f"{minutes} minute{'s' if minutes != 1 else ''}"
    host = e_.get("host")
    if host:
        who = f"**{e_.get('host_name') or 'The arena host'}** (<@{host}>)"
        line = f"Join {who}'s private server now" + (f" (arena: **{e_['arena']}**)" if e_.get("arena") else "") + \
            ". They'll share the code."
    else:
        line = ("No arena host has claimed this game, so the **higher seed hosts**: make the private server and send "
                "the code to the other captain now.")
    muted = sched(s)["muted"]
    for tid in (e_["a"], e_["b"]):
        other = e_["b"] if tid == e_["a"] else e_["a"]
        text = (f"⏰ **{mins} to tip-off:** M{mid} vs **{team_name(s, other)}** ({ts(gt, 't')} game).\n"
                f"{line}\nGet all 5 in your team voice channel and in the server. Fewer than 5 ready 15 minutes after "
                "the start is a forfeit." + (f"\n*Sent by {by}.*" if by else ""))
        emb = brand_embed(text, f"🏀 Get in the arena · M{mid}", GOLD)
        t = s["teams"].get(str(tid)) or {}
        tc = guild.get_channel(int(t.get("channel") or 0))
        if tc:
            try:
                await tc.send(content=f"<@&{tid}>", embed=emb, allowed_mentions=discord.AllowedMentions(roles=True))
            except discord.HTTPException:
                pass
        for uid in captains_of(s, tid):
            if uid not in muted:
                await dm(uid, brand_embed(text, f"🏀 Get in the arena · M{mid}", GOLD))
    if host:
        await dm(host, brand_embed(f"⏰ **{mins}:** M{mid} {team_name(s, e_['a'])} vs {team_name(s, e_['b'])} "
                                   f"({ts(gt, 't')} game). Both teams were told to join your server: share the code "
                                   "with both captains.", f"🎮 You're hosting · M{mid}", GOLD))


_arena_calls: dict[str, datetime] = {}  # "guild:match" -> last /arenacall (no spamming)


@bot.tree.command(description="Captains, arena host or staff: tell both teams to get in the arena (1-10 minutes left).")
@app_commands.describe(match="Match number, e.g. 12 for M12", minutes="Minutes until tip-off (1 to 10)")
async def arenacall(interaction: discord.Interaction, match: int, minutes: app_commands.Range[int, 1, 10]):
    guild, user = interaction.guild, interaction.user
    s = guild_signups(load_data(), guild.id)
    mid = str(match)
    e_ = sched(s)["matches"].get(mid)
    if not e_ or e_["done"]:
        return await interaction.response.send_message(f"M{match} isn't an open match.", ephemeral=True)
    if not (is_official(user) or user.id == e_.get("host") or
            any(user.id in captains_of(s, t) for t in (e_["a"], e_["b"]))):
        return await interaction.response.send_message(
            f"Only the captains in M{match}, its arena host, or staff can do that.", ephemeral=True)
    if not e_.get("time"):
        return await interaction.response.send_message(f"M{match} doesn't have a game time yet.", ephemeral=True)
    now = datetime.now(timezone.utc)
    gt = datetime.fromisoformat(e_["time"])
    if gt - now > timedelta(minutes=30):
        return await interaction.response.send_message(
            f"M{match} starts {ts(gt, 'R')}. Send the arena call when it's close (within 30 minutes).", ephemeral=True)
    key = f"{guild.id}:{mid}"
    last = _arena_calls.get(key)
    if last and now - last < timedelta(minutes=2) and not is_official(user):
        return await interaction.response.send_message("An arena call just went out for this game. Give it 2 minutes.",
                                                       ephemeral=True)
    _arena_calls[key] = now
    await interaction.response.defer(ephemeral=True)
    await five_minute_call(guild, s, mid, e_, gt, minutes, by=getattr(user, "display_name", None) or user.name)
    await interaction.followup.send(f"Sent: **{minutes} minute{'s' if minutes != 1 else ''} to tip-off** for M{mid} "
                                    "(both team channels, captains and the arena host).", ephemeral=True)


def passed_reminders(gt: datetime) -> list[str]:
    """Reminders that are already due when a time gets set (e.g. the 24-hour one for a game in 5 hours): skip
    them, the "game confirmed" DM just went out. The game-starts-now one is never skipped."""
    now = datetime.now(timezone.utc)
    return [k for secs, k, _w in REMINDERS if secs > 0 and now >= gt - timedelta(seconds=secs)]


REMINDERS = [(24 * 3600, "24h", "in 24 hours"), (3600, "1h", "in 1 hour"), (0, "now", "now")]


_watch_locks: dict[int, asyncio.Lock] = {}


async def match_watch_once(guild: discord.Guild):
    """One pass at a time per server: two passes at once (the minute loop + a command) would DM the same game twice."""
    lock = _watch_locks.setdefault(guild.id, asyncio.Lock())
    async with lock:
        await _match_watch_once(guild)


async def _match_watch_once(guild: discord.Guild):
    data = load_data()
    s = guild_signups(data, guild.id)
    sc = sched(s)
    now = datetime.now(timezone.utc)
    live = {str(m["id"]): m for m in open_matches(s.get("event"))}
    changed = False
    for mid, e_ in sc["matches"].items():
        if not e_["done"] and mid not in live:
            e_["done"] = True  # result is in (or the tournament was reset)
            changed = True
    for mid, m in live.items():
        if str(m["a"]) not in s["teams"] or str(m["b"]) not in s["teams"]:
            continue  # test tournaments with fake teams
        e_ = sc["matches"].get(mid)
        if e_ is None or e_["done"] or str(e_["a"]) != str(m["a"]) or str(e_["b"]) != str(m["b"]):
            await match_opened(guild, s, m)
            changed = True
            continue
        if e_.get("time"):
            gt = datetime.fromisoformat(e_["time"])
            if "5m" not in e_["reminded"] and gt - timedelta(minutes=5) <= now < gt + timedelta(minutes=5):
                e_["reminded"].append("5m")  # 5 minutes to go: get into the arena host's server
                changed = True
                await five_minute_call(guild, s, mid, e_, gt)
            for secs, key, words in reversed(REMINDERS):  # latest due reminder first
                if key not in e_["reminded"] and now >= gt - timedelta(seconds=secs) and now < gt + timedelta(minutes=30):
                    # only send the latest reminder that's due (no 24h reminder an hour before the game)
                    e_["reminded"] += [k for _s, k, _w in REMINDERS if _s >= secs]
                    changed = True
                    if key != "now":  # the real countdown, not the label ("in 1 hour" even if set late)
                        words = f"{ts(gt, 'R')} ({ts(gt, 't')})"
                    await dm_teams(guild, s, [e_["a"], e_["b"]], lambda tid, w=words, mm=mid: next_match_card(
                        s, mm, tid, f"\n\n⏰ **Your game starts {w}.** Be in the {team_name(s, tid)} voice channel "
                                    "and ready to join the private server."))
                    for who, role_txt in ((e_.get("host"), "hosting"), (e_.get("stream"), "streaming")):
                        if who:
                            await dm(who, brand_embed(f"⏰ **M{mid}** {team_name(s, e_['a'])} vs {team_name(s, e_['b'])} "
                                                      f"starts {words}. You're {role_txt} it"
                                                      + (f" (arena: **{e_['arena']}**)" if e_.get("arena") else "")
                                                      + (f".\nYour link: {e_['stream_link']}" if role_txt == "streaming"
                                                         and e_.get("stream_link") else "."),
                                                      stage_heading(e_.get("label", ""), mid).title(), GOLD))
                    if key == "now":
                        schedule_publish(guild)
                        await scheduling_post(guild, s, mid, f"**M{mid}** {team_name(s, e_['a'])} vs "
                                                             f"{team_name(s, e_['b'])} starts now. Good luck!",
                                              "🏀 Game time", GOOD)
                    break
        else:
            dl = datetime.fromisoformat(e_["deadline"])
            opened_ = datetime.fromisoformat(e_.get("opened") or e_["deadline"])
            warn = min(timedelta(hours=12), (dl - opened_) / 3)  # 12h before, or a third of a short window
            if "12h" not in e_["reminded"] and now >= dl - warn and now < dl:
                e_["reminded"].append("12h")
                changed = True
                await scheduling_post(guild, s, mid, f"**{human(dl - now)} left** to agree a time for M{mid}. "
                                                     f"Use `/gametime match:{mid}`.", f"⏳ M{mid} deadline soon", GOLD)
            if now >= dl and not AUTO_PRESET:
                if "overdue" not in e_["reminded"]:  # the bot picks a time, staff confirm it in #staff-chat
                    e_["reminded"].append("overdue")
                    changed = True
                    await staff_preset_card(guild, s, mid, e_, now)
                    await grant_priority(guild, s, mid, e_)
                elif e_.get("pending_preset") and e_["pending_preset"] < (now + timedelta(minutes=20)).timestamp():
                    changed = True  # nobody confirmed in time: pick the next slot on the same card
                    await staff_preset_card(guild, s, mid, e_, now)
            elif now >= dl:
                busy = team_busy(sc, (e_["a"], e_["b"]), mid)
                others = [(datetime.fromisoformat(x["time"]), not x.get("preset")) for k, x in sc["matches"].items()
                          if k != mid and not x.get("done") and x.get("time")]
                preset = evening_slot(sc, max(dl, now) + timedelta(minutes=30), busy, others)  # 8 PM ET or later
                e_["time"], e_["preset"], e_["reminded"] = preset.isoformat(timespec="seconds"), True, \
                    passed_reminders(preset)
                changed = True
                await scheduling_post(guild, s, mid, f"No time was agreed in time, so **M{mid}** "
                                                     f"({team_name(s, e_['a'])} vs {team_name(s, e_['b'])}) is set for "
                                                     f"**{ts(preset)}** ({ts(preset, 'R')}).\n\nWant it earlier or "
                                                     f"later? Use `/gametime match:{mid}`. It only changes if both "
                                                     "captains confirm.", f"🕕 M{mid} preset time", GOLD)
                await post_game_card(guild, s, mid)
                await post_pickem(guild, s, mid)
                await dm_teams(guild, s, [e_["a"], e_["b"]], lambda tid, mm=mid: next_match_card(s, mm, tid))
                await dm_game_rules(guild, s, mid)
                await grant_priority(guild, s, mid, e_)  # a team that asked and got no answer can move it (staff OK)
    try:
        if await nag_unscheduled(guild, s, now):  # every 6 hours: teams with games that still have no time
            changed = True
    except Exception as ex:
        print(f"[schedule nag] {ex}")
    try:
        if await stream_watch_once(guild, s, now):
            changed = True
    except Exception as ex:
        print(f"[stream watch] {ex}")
    if changed:
        save_data(data)


# ---------------------------------------------------------------- Game day post (#game-announcements)
#
# Every morning (10 AM ET) the bot posts today's games in #game-announcements: a GAME DAY graphic with every
# matchup and its time, plus a list with live countdowns and who's streaming. Games scheduled later in the day
# are added by editing the same post.

GAMEDAY_HOUR = 10  # ET


def todays_games(s: dict, now: datetime) -> list[tuple[str, dict]]:
    tz = tzinfo("ET")
    today = now.astimezone(tz).date()
    out = [(mid, e_) for mid, e_ in sched(s)["matches"].items()
           if not e_.get("done") and e_.get("time") and datetime.fromisoformat(e_["time"]).astimezone(tz).date() == today]
    return sorted(out, key=lambda x: (x[1]["time"], int(x[0])))


def gameday_picture(s: dict, games: list[tuple[str, dict]], day: datetime) -> bytes:
    WHITE, GREY, ORANGE, PANEL, LINE = (245, 245, 245), (150, 150, 155), (255, 122, 0), (22, 22, 26), (52, 52, 58)
    tz_ = s.get("tourney") or {}
    tlogo = str(LOGO_DIR / tz_["logo"]) if tz_.get("logo") and (LOGO_DIR / tz_["logo"]).exists() else None
    W, RH = 1600, 118
    H = 250 + RH * len(games) + 70
    img, d = _canvas(W, H, "GAME DAY", day.strftime("%A, %B %d").replace(" 0", " ") + " · "
                     + tz_.get("name", "ON THE RISE"), tlogo)
    note = f"{len(games)} game{'s' if len(games) != 1 else ''} today · times in ET"
    d.text((W - 50 - d.textlength(note, font=_font(22, bold=False)), 110), note, font=_font(22, bold=False), fill=GREY)
    y = 240
    for mid, e_ in games:
        d.rounded_rectangle((50, y, W - 50, y + RH - 16), 12, fill=PANEL, outline=LINE, width=2)
        t = datetime.fromisoformat(e_["time"]).astimezone(tzinfo("ET"))
        tt = t.strftime("%I:%M %p").lstrip("0")
        d.text((78, y + 22), tt, font=_font(40), fill=ORANGE)
        d.text((78, y + 70), stage_heading(e_.get("label", ""), mid).title()[:40], font=_font(16, bold=False), fill=GREY)
        for side, x in (("a", 470), ("b", 1010)):
            team = s["teams"].get(str(e_[side]), {})
            lg = _logo((LOGO_DIR / team["logo"]) if team.get("logo") else None, 72, team.get("name", "TBD"))
            img.paste(lg, (x, y + 15), lg)
            name = team.get("name", "TBD")
            d.text((x + 88, y + 34), name, font=_fit(d, name, 330, 32, 16), fill=WHITE)
        d.text((925, y + 30), "VS", font=_font(34), fill=ORANGE)
        if e_.get("stream"):
            lt = "LIVE ON STREAM"
            d.text((W - 80 - d.textlength(lt, font=_font(16)), y + 72), lt, font=_font(16), fill=(239, 68, 68))
        y += RH
    return _png(img)


def gameday_text(s: dict, games: list[tuple[str, dict]]) -> str:
    lines = []
    for mid, e_ in games:
        t = datetime.fromisoformat(e_["time"])
        line = (f"{ts(t, 't')} · {team_emoji(s, e_['a'])}**{team_name(s, e_['a'])}** vs "
                f"{team_emoji(s, e_['b'])}**{team_name(s, e_['b'])}** · {stage_heading(e_.get('label', ''), mid).title()}")
        if e_.get("stream"):
            line += f"\n> 📺 {e_.get('stream_name') or 'Streamed'}" + (f" · [Watch]({e_['stream_link']})" if e_.get("stream_link") else "")
        lines.append(line)
    url = site_url()
    return "\n".join(lines) + "\n\nTimes show in your own timezone." + (f" Full schedule: {url}#schedule" if url else "")


async def gameday_once(guild: discord.Guild):
    """Post today's games once in the morning; edit the post if games are added or moved later today."""
    now = datetime.now(timezone.utc)
    local = now.astimezone(tzinfo("ET"))
    data = load_data()
    s = guild_signups(data, guild.id)
    gd = s.setdefault("gameday", {})
    today = local.date().isoformat()
    if local.hour < GAMEDAY_HOUR and gd.get("date") != today:
        return
    games = todays_games(s, now)
    sig = json.dumps([(m, e_["time"], e_["a"], e_["b"], e_.get("stream")) for m, e_ in games])
    if gd.get("date") == today and gd.get("sig") == sig:
        return
    if not games and gd.get("date") != today:
        return  # no games today: nothing to post
    ch = chan(guild, "game-announcements")
    if ch is None:
        return
    emb = brand_embed(gameday_text(s, games) if games else "Today's games were moved. Check the schedule.",
                      f"🏀 GAME DAY · {local.strftime('%A, %B %d').replace(' 0', ' ')}", GOLD)
    png = None
    if games:
        try:
            png = await asyncio.to_thread(gameday_picture, s, games, local)
            emb.set_image(url="attachment://gameday.png")
        except Exception as e:
            print(f"[game day picture] {e}")
    msg = None
    if gd.get("date") == today and gd.get("msg"):
        try:
            msg = await ch.fetch_message(int(gd["msg"]))
            kw = {"embed": emb}
            if png:
                kw["attachments"] = [discord.File(io.BytesIO(png), filename="gameday.png")]
            await msg.edit(**kw)
        except discord.HTTPException:
            msg = None
    if msg is None:
        kw = {"embed": emb, "allowed_mentions": NO_PINGS}
        if png:
            kw["file"] = discord.File(io.BytesIO(png), filename="gameday.png")
        try:
            msg = await ch.send(**kw)
        except discord.HTTPException as e:
            print(f"[game day] {e}")
            return
    gd.update({"date": today, "msg": msg.id, "sig": sig})
    save_data(data)


# ---------------------------------------------------------------- /remind: tell everyone what's next
#
# /remind what:[Next up / Sign-ups closing / Live draw / Main draw / Matches / Something else] when:8pm ...
# Posts a reminder card (default #announcements) with a live countdown, pings who you pick, and can remind
# again automatically before it starts. Matches also go to each team's own channel with their game and time.

REMIND_KINDS = {"auto": "Next up (the bot works it out)", "signups": "Sign-ups closing", "draw": "Live draw",
                "main": "Main draw starting", "matches": "Matches (each team's next game)",
                "other": "Something else (write it in note)"}
REMIND_AGAIN = {"none": ("No", []), "15": ("15 minutes before", [15]), "30": ("30 minutes before", [30]),
                "60": ("1 hour before", [60]), "60+15": ("1 hour and 15 minutes before", [60, 15]),
                "1440+60": ("1 day and 1 hour before", [1440, 60])}
REMIND_PINGS = {"here": "@here", "everyone": "@everyone", "players": "Player role", "captains": "Captains + co-captains",
                "none": "No ping"}
DAYS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]


def parse_when(text: str, tz_code: str) -> tuple[datetime | None, str | None]:
    """'8pm', '8:30pm', '20:00', 'tomorrow 7pm', 'sat 6pm', 'in 2h', '45m', or a Discord timestamp <t:123:F>."""
    t = (text or "").strip().lower().replace(".", "")
    now = datetime.now(timezone.utc)
    zone = re.search(r"\s*\b(est|edt|et|cst|cdt|ct|mst|mdt|mt|pst|pdt|pt|uk|gmt|bst|cet|aest)\s*$", t)
    if zone:  # a timezone written on the end wins over the default
        tz_code = {"est": "ET", "edt": "ET", "et": "ET", "cst": "CT", "cdt": "CT", "ct": "CT", "mst": "MT",
                   "mdt": "MT", "mt": "MT", "pst": "PT", "pdt": "PT", "pt": "PT", "uk": "UK", "gmt": "UK",
                   "bst": "UK", "cet": "CET", "aest": "AEST"}[zone.group(1)]
        t = t[:zone.start()].strip()
    t = re.sub(r"\b(at|on|by|this|next)\b", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    m = re.fullmatch(r"<t:(\d+)(?::\w)?>|(\d{9,11})", t)
    if m:
        return datetime.fromtimestamp(int(m.group(1) or m.group(2)), timezone.utc), None
    rel = t[3:] if t.startswith("in ") else t
    if re.fullmatch(r"(\d+\s*[wdhm]\s*)+", rel):
        td, problem = parse_duration(rel)
        return (None, problem) if problem or td is None else (now + td, None)
    tz = tzinfo(tz_code)
    local = now.astimezone(tz)
    day, explicit = local, False
    words = t.replace(",", " ").split()
    if words and words[0] in ("today", "tonight"):
        words, explicit = words[1:], True
    elif words and words[0] in ("tomorrow", "tmrw", "tmr"):
        day, words, explicit = local + timedelta(days=1), words[1:], True
    elif words and words[0][:3] in DAYS:
        ahead = (DAYS.index(words[0][:3]) - local.weekday()) % 7
        day, words, explicit = local + timedelta(days=ahead), words[1:], True
    m = re.fullmatch(r"(\d{1,2})(?::(\d{2}))?\s*(am|pm)?", " ".join(words).replace(" ", ""))
    if not m:
        return None, ("I couldn't read that time. Try `8pm`, `8:30pm`, `20:00`, `tomorrow 7pm`, `sat 6pm` or `in 2h`.")
    hh, mm, ap = int(m.group(1)), int(m.group(2) or 0), m.group(3)
    if ap == "pm" and hh < 12:
        hh += 12
    elif ap == "am" and hh == 12:
        hh = 0
    elif not ap and 1 <= hh <= 11:
        hh += 12  # "8" means 8 PM: events are in the evening
    if hh > 23 or mm > 59:
        return None, "That isn't a real time."
    when = day.replace(hour=hh, minute=mm, second=0, microsecond=0)
    if when < local:
        if explicit and day.date() == local.date() and words and t.split()[0][:3] in DAYS:
            when += timedelta(days=7)  # "sat 6pm" said on a Saturday evening means next Saturday
        elif not explicit:
            when += timedelta(days=1)  # "8pm" after 8 PM means tomorrow
        else:
            return None, "That time has already passed."
    return when.astimezone(timezone.utc), None


def remind_next_up(s: dict) -> str | None:
    ev = s.get("event")
    now = datetime.now(timezone.utc)
    if ev and (ev.get("drawing") or (ev.get("draw_at") and datetime.fromisoformat(ev["draw_at"]) > now)):
        return "draw"
    if s.get("open"):
        return "signups"
    if ev and open_matches(ev):
        return "matches"
    if ev and ev.get("stage") in ("groups_done", "swiss_done", "playin_done"):
        return "main"
    return None


def remind_ping(guild: discord.Guild, ping: str) -> tuple[str, discord.AllowedMentions]:
    if ping == "everyone":
        return "@everyone", discord.AllowedMentions(everyone=True)
    if ping == "here":
        return "@here", discord.AllowedMentions(everyone=True)
    names = {"players": ["Player"], "captains": ["Team Captain", "Co-Captain"]}.get(ping, [])
    rs = [r for r in (role(guild, n) for n in names) if r]
    return " ".join(r.mention for r in rs), discord.AllowedMentions(roles=rs) if rs else NO_PINGS


async def send_reminder(guild: discord.Guild, s: dict, r: dict) -> str:
    """Post one reminder. r = {kind, when (iso or None), note, ping, channel, before (minutes or None)}."""
    kind, note, before = r["kind"], r.get("note"), r.get("before")
    if kind == "auto":
        kind = remind_next_up(s) or "other"
    ev = s.get("event") or {}
    tname = (s.get("tourney") or {}).get("name", "the tournament")
    when = datetime.fromisoformat(r["when"]) if r.get("when") else None
    if kind == "draw" and when is None and ev.get("draw_at"):
        when = datetime.fromisoformat(ev["draw_at"])
    at = f"{ts(when)} ({ts(when, 'R')})" if when else None
    lines, team_posts = [], []
    if kind == "signups":
        title = "📝 SIGN-UPS CLOSING"
        closes = at or (s.get("closes") and f"**{s['closes']}**") or "soon"
        lines.append(f"Sign-ups for **{tname}** close {closes}.")
        lines.append("Captains and co-captains: enter your team with `/register` before then. Need 5 players.\n"
                     "No team? Make one with `/signup` or post in free agents with `/freeagent`.")
    elif kind == "draw":
        title = "🎥 LIVE DRAW"
        lines.append(f"The **{tname}** draw goes live {at or 'soon'} in {chan_mention(guild, 'bracket')}.")
        lines.append("Seeds, groups and first opponents are revealed live. Be there when it drops!")
    elif kind == "main":
        title = "🏆 MAIN DRAW"
        lines.append(f"The **{tname}** main draw starts {at or 'soon'}. Double elimination: lose twice and you're out.")
        lines.append(f"Bracket in {chan_mention(guild, 'bracket')} and live on the website.")
    elif kind == "matches":
        title = "🏀 GAMES TO PLAY"
        sc = sched(s)
        games = open_matches(ev)
        if not games:
            return "There are no games to play right now."
        rows = []
        for g in sorted(games, key=lambda g: (sc["matches"].get(str(g["id"]), {}).get("time") or "9", g["id"])):
            e_ = sc["matches"].get(str(g["id"]), {})
            if e_.get("time"):
                gt = datetime.fromisoformat(e_["time"])
                tm = f"{ts(gt, 'f')} ({ts(gt, 'R')})"
            elif e_.get("deadline"):
                tm = f"not scheduled yet: agree a time by {ts(datetime.fromisoformat(e_['deadline']), 'f')}"
            else:
                tm = "not scheduled yet"
            rows.append(f"**M{g['id']}** {g['label']}: **{team_name(s, g['a'])}** vs **{team_name(s, g['b'])}** · {tm}")
            for me, them in ((g["a"], g["b"]), (g["b"], g["a"])):
                team_posts.append((me, f"**Your next game:** M{g['id']} ({g['label']}) vs **{team_name(s, them)}**\n"
                                       f"**When:** {tm}\nReport the score with `/game_score` when it's done."))
        lines.append(f"**{len(games)} game{'s' if len(games) != 1 else ''}** to play in **{tname}**:")
        lines += rows[:25]
        if len(rows) > 25:
            lines.append(f"…and {len(rows) - 25} more.")
        if at:
            lines.insert(0, f"Games need to be played by {at}.")
    else:
        title = "📣 REMINDER"
        if not note and not at:
            return "Nothing obvious is coming up. Pick what to remind about, or write it in `note`."
        if at:
            lines.append(f"**When:** {at}")
    if before:
        title = f"⏰ {human(timedelta(minutes=before)).upper()} TO GO · " + title.split(" ", 1)[1]
    if note:
        lines.append(f"\n**Note:** {note}")
    content, am = remind_ping(guild, r.get("ping", "none"))
    ch = guild.get_channel(int(r["channel"])) if r.get("channel") else None
    ch = ch or chan(guild, "announcements")
    if ch is None:
        return "There's no #announcements channel. Pick a channel."
    await ch.send(content=content or None, embed=brand_embed("\n".join(lines), title, GOLD), allowed_mentions=am)
    sent = 0
    for tid, text in team_posts:
        t = s["teams"].get(str(tid)) or {}
        tc = guild.get_channel(int(t.get("channel") or 0))
        if tc:
            try:
                await tc.send(content=f"<@&{tid}>" if r.get("ping", "none") != "none" else None,
                              embed=brand_embed(text, "⏰ GAME REMINDER", GOLD),
                              allowed_mentions=discord.AllowedMentions(roles=True))
                sent += 1
            except discord.HTTPException:
                pass
    return f"Posted in {ch.mention}" + (f" and {sent} team channel(s)" if sent else "") + "."


def chan_mention(guild, name: str) -> str:
    c = chan(guild, name)
    return c.mention if c else f"#{name}"


async def reminder_watch_once(guild: discord.Guild):
    data = load_data()
    s = guild_signups(data, guild.id)
    due, keep = [], []
    now = datetime.now(timezone.utc)
    for r in s.get("reminders", []):
        (due if datetime.fromisoformat(r["at"]) <= now else keep).append(r)
    if not due:
        return
    s["reminders"] = keep
    save_data(data)
    for r in due:
        if (now - datetime.fromisoformat(r["at"])) > timedelta(minutes=30):
            continue  # the bot was off when it was due: don't post a stale reminder
        try:
            await send_reminder(guild, s, r)
        except Exception as e:
            print(f"[reminders] {e}")


@bot.tree.command(description="Staff: remind everyone what's next: sign-ups closing, the draw, main draw, or games.")
@app_commands.describe(what="What to remind about (Next up = the bot picks the next thing)",
                       when="When it happens: 8pm, 8:30pm, tomorrow 7pm, sat 6pm, in 2h (8 = 8 PM)",
                       note="Extra line to add (optional)", ping="Who gets pinged (default @here)",
                       tz="Timezone for `when` (default yours from scheduling, or ET)",
                       again="Also post again automatically before it starts (needs `when`, or a scheduled draw)",
                       channel="Where to post (default #announcements)")
@app_commands.choices(what=[app_commands.Choice(name=v, value=k) for k, v in REMIND_KINDS.items()],
                      again=[app_commands.Choice(name=v[0], value=k) for k, v in REMIND_AGAIN.items()],
                      ping=[app_commands.Choice(name=v, value=k) for k, v in REMIND_PINGS.items()],
                      tz=TZ_CHOICES)
@app_commands.default_permissions(manage_messages=True)
async def remind(interaction: discord.Interaction, what: str = "auto", when: str | None = None,
                 note: str | None = None, ping: str = "here", tz: str | None = None, again: str = "none",
                 channel: discord.TextChannel | None = None):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can send reminders.", ephemeral=True)
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    tz_code = tz or sched(s)["tz"].get(str(interaction.user.id), "ET")
    at = None
    if when:
        at, problem = parse_when(when, tz_code)
        if problem:
            return await interaction.response.send_message(problem, ephemeral=True)
    kind = what if what != "auto" else (remind_next_up(s) or "other")
    if what == "auto" and kind == "other" and not note:
        return await interaction.response.send_message(
            "Nothing is coming up that I can see (no sign-ups open, draw, games or main draw waiting). "
            "Pick what to remind about, or write it in `note`.", ephemeral=True)
    if kind == "draw" and at is None and (s.get("event") or {}).get("draw_at"):
        at = datetime.fromisoformat(s["event"]["draw_at"])
    await interaction.response.defer(ephemeral=True)
    r = {"kind": kind, "when": at.isoformat(timespec="seconds") if at else None, "note": (note or "").strip()[:500] or None,
         "ping": ping, "channel": channel.id if channel else None, "by": interaction.user.id}
    msg = await send_reminder(guild, s, r)
    if at and kind in ("signups", "draw", "main", "other", "matches"):
        d_ = load_data()
        s_ = guild_signups(d_, guild.id)
        evs = [e for e in s_.get("site_events", []) if e["kind"] != kind or kind == "other"]
        evs.append({"kind": kind, "at": at.isoformat(timespec="seconds"), "note": r["note"]})
        s_["site_events"] = evs[-12:]
        save_data(d_)
    extra = ""
    mins = REMIND_AGAIN.get(again, ("", []))[1]
    if mins:
        if at is None:
            extra = "\nNo repeat set: add `when` so I know when it starts."
        else:
            data = load_data()
            s2 = guild_signups(data, guild.id)
            added = []
            for mn in mins:
                fire = at - timedelta(minutes=mn)
                if fire > datetime.now(timezone.utc):
                    s2.setdefault("reminders", []).append(dict(r, before=mn, at=fire.isoformat(timespec="seconds")))
                    added.append(f"{ts(fire, 't')} ({human(timedelta(minutes=mn))} before)")
            save_data(data)
            extra = ("\nI'll post it again at " + " and ".join(added) + ".") if added else \
                "\nToo close to the start to remind again."
    when_txt = f" for {ts(at)} ({tz_code})" if at else ""
    await interaction.followup.send(f"**{REMIND_KINDS[kind].split(' (')[0]}** reminder{when_txt}. {msg}{extra}",
                                    ephemeral=True)


@bot.tree.command(description="Staff: see the reminders waiting to go out, or cancel them all.")
@app_commands.describe(cancel="Cancel every waiting reminder")
@app_commands.default_permissions(manage_messages=True)
async def reminders(interaction: discord.Interaction, cancel: bool = False):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    rs = sorted(s.get("reminders", []), key=lambda r: r["at"])
    if cancel:
        s["reminders"] = []
        save_data(data)
        return await interaction.response.send_message(f"Cancelled {len(rs)} reminder(s).", ephemeral=True)
    if not rs:
        return await interaction.response.send_message("No reminders waiting. Set one with `/remind ... again:`.",
                                                       ephemeral=True)
    lines = [f"{ts(datetime.fromisoformat(r['at']), 'f')} ({ts(datetime.fromisoformat(r['at']), 'R')}): "
             f"**{REMIND_KINDS.get(r['kind'], r['kind']).split(' (')[0]}**, {human(timedelta(minutes=r['before']))} before"
             for r in rs]
    await interaction.response.send_message("**Waiting reminders**\n" + "\n".join(lines[:20]) +
                                            "\n\nCancel them all with `/reminders cancel:True`.", ephemeral=True)


async def match_watch():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            try:
                await match_watch_once(guild)
            except Exception as e:
                print(f"[match reminders] {e}")
            try:
                await reminder_watch_once(guild)  # /remind ... again: the "1 hour to go" posts
            except Exception as e:
                print(f"[reminders] {e}")
            try:
                await gameday_once(guild)  # #game-announcements: today's games every morning
            except Exception as e:
                print(f"[game day] {e}")
            try:
                await promote_upcoming(guild)  # the next tournament takes over when the current one ends
            except Exception as e:
                print(f"[next tournament] {e}")
            try:
                await pickem_lock_once(guild)  # pick'ems close at tip-off
            except Exception as e:
                print(f"[pickems] {e}")
            try:
                await host_cooldown_once(guild)  # Pickup Hosts get @everyone back after an hour
            except Exception as e:
                print(f"[pickup host] {e}")
        await asyncio.sleep(60)


async def post_rules(channel: discord.TextChannel):
    for i, (title, color, rules) in enumerate(RULE_CARDS):
        e = brand_embed("\n".join(f"**{n}.** {r}" for n, r in enumerate(rules, 1)), title, color)
        if i == len(RULE_CARDS) - 1:
            e.description += "\n\nBy playing in the circuit you agree to these rules. Questions? Open a ticket."
        await channel.send(embed=e)


# one-time setup: run with /setupbot part:rules
async def rulessetup(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    ch = chan(interaction.guild, "rules")
    if ch is None:
        return await interaction.response.send_message("I can't find a #rules channel.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    removed = 0
    try:
        removed = len(await ch.purge(limit=200))
    except discord.HTTPException:  # no Manage Messages, or very old messages: delete one by one
        async for msg in ch.history(limit=200):
            try:
                await msg.delete()
                removed += 1
            except discord.HTTPException:
                pass
    await post_rules(ch)
    await interaction.followup.send(f"Cleared {removed} message(s) and posted {len(RULE_CARDS)} rule cards in "
                                    f"{ch.mention}.", ephemeral=True)


# one-time setup: run with /setupbot part:teamvoices
async def teamvoices(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    cat = await get_or_make_category(guild, "TEAMS", overwrites_for(guild, "staff"))
    made = []
    for key, t in s["teams"].items():
        team = guild.get_role(int(key))
        if team and not guild.get_channel(t.get("voice") or 0):
            v = await make_team_voice(guild, cat, team, t["name"])
            if v:
                t["voice"] = v.id
                made.append(t["name"])
    save_data(data)
    await interaction.followup.send(f"Made voice channels for: {', '.join(made)}." if made else
                                    "Every team already has a voice channel.", ephemeral=True)


# ---------------------------------------------------------------- announcements
#
# /announce opens a form (title + message). Staff see a preview with Post / Cancel buttons, then the bot
# posts it as a branded card in #announcements (or any channel), with an optional ping and image.

ANNOUNCE_COLORS = {"red": BRAND, "gold": GOLD, "green": GOOD, "blue": INFO, "gray": MUTED}


def announce_card(title: str, body: str, color: str, author: discord.abc.User, image_name: str | None):
    e = brand_embed(body, title or None, ANNOUNCE_COLORS.get(color, BRAND))
    if image_name:
        e.set_image(url=f"attachment://{image_name}")
    e.set_footer(text=f"Posted by {author.display_name} · ON THE RISE · PB CIRCUIT",
                 icon_url=author.display_avatar.url)
    return e


class AnnouncePreview(discord.ui.View):
    def __init__(self, author_id: int, channel, ping: str | None, title: str, body: str, color: str,
                 image: tuple[str, bytes] | None):
        super().__init__(timeout=900)
        self.author_id, self.channel, self.ping = author_id, channel, ping
        self.title, self.body, self.color, self.image = title, body, color, image

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        return interaction.user.id == self.author_id

    @discord.ui.button(label="Post it", emoji="📣", style=discord.ButtonStyle.success)
    async def post_it(self, interaction: discord.Interaction, button: discord.ui.Button):
        kw = {"embed": announce_card(self.title, self.body, self.color, interaction.user,
                                     self.image[0] if self.image else None)}
        if self.image:
            kw["file"] = discord.File(io.BytesIO(self.image[1]), filename=self.image[0])
        if self.ping:
            kw["content"] = self.ping
            kw["allowed_mentions"] = discord.AllowedMentions(everyone=True, roles=True, users=False)
        else:
            kw["allowed_mentions"] = NO_PINGS
        try:
            msg = await self.channel.send(**kw)
        except discord.HTTPException as e:
            return await interaction.response.edit_message(content=f"Couldn't post it: {e}", embed=None, view=None,
                                                           attachments=[])
        self.stop()
        await interaction.response.edit_message(content=f"Posted in {self.channel.mention}: {msg.jump_url}",
                                                embed=None, view=None, attachments=[])

    @discord.ui.button(label="Cancel", emoji="✖", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.stop()
        await interaction.response.edit_message(content="Cancelled. Nothing was posted.", embed=None, view=None,
                                                attachments=[])


class AnnounceForm(discord.ui.Modal, title="New announcement"):
    a_title = discord.ui.TextInput(label="Title", max_length=200, required=False,
                                   placeholder="e.g. Rise Open 2 sign-ups are live!")
    a_body = discord.ui.TextInput(label="Message", style=discord.TextStyle.paragraph, max_length=4000,
                                  placeholder="Write the announcement. Discord formatting (**bold**, lists, links) works.")

    def __init__(self, channel, ping: str | None, color: str, image: tuple[str, bytes] | None,
                 title: str = "", body: str = ""):
        super().__init__()
        self.channel, self.ping, self.color, self.image = channel, ping, color, image
        self.a_title.default, self.a_body.default = title or None, body or None

    async def on_submit(self, interaction: discord.Interaction):
        view = AnnouncePreview(interaction.user.id, self.channel, self.ping, self.a_title.value.strip(),
                               self.a_body.value.strip(), self.color, self.image)
        kw = {"embed": announce_card(view.title, view.body, self.color, interaction.user,
                                     self.image[0] if self.image else None), "view": view, "ephemeral": True,
              "content": f"**Preview** · will post in {self.channel.mention}"
                         + (f" and ping {self.ping}" if self.ping else " with no ping") + "."}
        if self.image:
            kw["file"] = discord.File(io.BytesIO(self.image[1]), filename=self.image[0])
        await interaction.response.send_message(**kw)


@bot.tree.command(description="Staff: post an announcement through the bot (you get a preview first).")
@app_commands.describe(channel="Where to post it (default #announcements)",
                       ping="Who to notify (default nobody)", role="Ping this role instead (optional)",
                       image="An image to show in the announcement (optional)", color="Card color (default red)")
@app_commands.choices(ping=[app_commands.Choice(name="Nobody", value="none"),
                            app_commands.Choice(name="@everyone", value="everyone"),
                            app_commands.Choice(name="@here", value="here")],
                      color=[app_commands.Choice(name=n.title(), value=n) for n in ANNOUNCE_COLORS])
@app_commands.default_permissions(manage_messages=True)
async def announce(interaction: discord.Interaction, channel: discord.TextChannel | None = None,
                   ping: str = "none", role: discord.Role | None = None, image: discord.Attachment | None = None,
                   color: str = "red"):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can post announcements.", ephemeral=True)
    channel = channel or chan(interaction.guild, "announcements")
    if channel is None:
        return await interaction.response.send_message("I can't find #announcements. Pick a channel.", ephemeral=True)
    perms = channel.permissions_for(interaction.guild.me)
    if not (perms.send_messages and perms.embed_links):
        return await interaction.response.send_message(f"I can't post in {channel.mention}. Check my permissions there.",
                                                       ephemeral=True)
    img = None
    if image is not None:
        kind = (image.content_type or "").split(";")[0].lower()
        if kind not in LOGO_TYPES:
            return await interaction.response.send_message("The image has to be PNG, JPG, WEBP or GIF.", ephemeral=True)
        if image.size > 8_000_000:
            return await interaction.response.send_message("Keep the image under 8 MB.", ephemeral=True)
        img = (f"announcement.{LOGO_TYPES[kind]}", await image.read())
    who = role.mention if role else {"everyone": "@everyone", "here": "@here"}.get(ping)
    await interaction.response.send_modal(AnnounceForm(channel, who, color, img))


@bot.listen("on_interaction")
async def pickup_code_submit(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.modal_submit:
        return
    cid = (interaction.data or {}).get("custom_id", "")
    if not cid.startswith("pugcode:"):
        return
    _x, gid, mid = cid.split(":")
    guild = bot.get_guild(int(gid))
    data = load_data()
    p = pug(guild_signups(data, int(gid)))
    m = p["matches"].get(mid)
    if guild is None or not m or m["status"] != "live":
        return await interaction.response.send_message("That pickup isn't live any more.", ephemeral=True)
    try:
        code = interaction.data["components"][0]["components"][0]["value"].strip()
    except (KeyError, IndexError):
        return await interaction.response.send_message("I couldn't read the code. Try again.", ephemeral=True)
    m["code_shared_by"] = interaction.user.id
    save_data(data)
    await interaction.response.send_message("Sending the code to every player...", ephemeral=True)
    e = brand_embed(f"**Server code:** `{code}`\nPickup **P{mid}** · shared by {interaction.user.mention}\n"
                    "Join the private server now. Don't share this code outside the match.",
                    f"🔑 P{mid} server code", GOLD)
    failed = []
    for u in m["a"] + m["b"]:
        mem = guild.get_member(u)
        try:
            await mem.send(embed=e)
        except (discord.HTTPException, AttributeError):
            failed.append(u)
    for vc_id in m.get("vcs", []):  # also drop it in each team call's chat
        vc = guild.get_channel(vc_id)
        try:
            if vc:
                await vc.send(embed=e)
        except (discord.HTTPException, AttributeError):
            pass
    note = (" Couldn't DM " + ", ".join(f"<@{u}>" for u in failed) + " (DMs off), but it's in the team call chat."
            if failed else "")
    await interaction.followup.send(f"Code sent to all {len(m['a'] + m['b'])} players.{note}", ephemeral=True,
                                    allowed_mentions=NO_PINGS)


_vc_grace: dict[int, asyncio.Task] = {}


@bot.listen("on_voice_state_update")
async def waiting_room_watch(member: discord.Member, before, after):
    """Leave the waiting room while queued and you have 60 seconds to come back before losing your spot."""
    if member.bot or not PICKUP_NEEDS_VC:
        return
    p = pug(guild_signups(load_data(), member.guild.id))
    wid = p.get("chans", {}).get("waiting")
    if not wid or member.id not in p["queue"]:
        return
    left = before.channel is not None and before.channel.id == wid and (after.channel is None or after.channel.id != wid)
    if not left:
        return
    old = _vc_grace.pop(member.id, None)
    if old and not old.done():
        old.cancel()

    async def later():
        try:
            await asyncio.sleep(60)
        except asyncio.CancelledError:
            return
        data = load_data()
        p2 = pug(guild_signups(data, member.guild.id))
        if member.id in p2["queue"] and not in_waiting(member.guild, p2, member.id):
            p2["queue"].remove(member.id)
            p2["qpos"].pop(str(member.id), None)
            p2["last_event"] = ["Removed: left voice", member.id]
            save_data(data)
            await refresh_queue(member.guild, data)
            try:
                await member.send(embed=brand_embed(f"You left the waiting room in **{member.guild.name}**, so you "
                                                    "were taken out of the ranked queue. Rejoin voice and queue again.",
                                                    "Removed from queue", MUTED))
            except discord.HTTPException:
                pass

    _vc_grace[member.id] = asyncio.create_task(later())


# ---------------------------------------------------------------- hall of champions
#
# /setupbot part:champions makes the 🏆｜champions channel (everyone reads, only the bot posts) and the
# "Tournament Winner" role. Every time a real tournament crowns a champion, the bot:
#   - gives every player on the winning roster "Tournament Winner" plus that tournament's own role
#     (e.g. "🏆 Rise Open 1 Champions"),
#   - edits the champions list in place: one card per tournament, newest first, with the tournament
#     logo and the winning team's logo.

WINNER_ROLE = "Tournament Winner"


def hall(s: dict) -> dict:
    h = s.setdefault("hall", {})
    h.setdefault("channel", None)
    h.setdefault("msgs", [])
    h.setdefault("champions", [])  # newest last: {tournament, kind, logo, team, team_logo, players, date, role, series}
    h.setdefault("series", 1)      # a series = the circuit events leading up to (and including) one Major
    return h


def champion_role_name(tname: str) -> str:
    return f"🏆 {tname} Champions"[:100]


async def get_role(guild: discord.Guild, name: str, color: int, hoist: bool = False):
    r = role(guild, name)
    if r is None:
        try:
            r = await guild.create_role(name=name, colour=discord.Colour(color), hoist=hoist,
                                        reason="Tournament champions")
        except discord.HTTPException:
            return None
    return r


def champion_card(c: dict, n: int) -> tuple[discord.Embed, list]:
    """One tournament's card. Returns the embed and the logo files it needs."""
    files = []
    when = datetime.fromisoformat(c["date"]).strftime("%b %d, %Y") if c.get("date") else ""
    lines = [f"**Champions:** {c['team']}"]
    if c.get("players"):
        lines.append("**Roster:** " + " ".join(f"<@{u}>" for u in c["players"]))
    if c.get("role") and not c.get("role_gone"):
        lines.append(f"**Role:** <@&{c['role']}>")
    meta = " · ".join(x for x in (when, f"Series {c['series']}" if c.get("series") else "",
                                  "MAJOR" if c.get("kind") == "major" else "Circuit event") if x)
    lines.append(f"-# {meta}")
    e = brand_embed("\n".join(lines), f"🏆 {c['tournament']}", GOLD)
    if c.get("logo") and (LOGO_DIR / c["logo"]).exists():
        name = f"t{n}_{c['logo']}"
        files.append(discord.File(LOGO_DIR / c["logo"], filename=name))
        e.set_thumbnail(url=f"attachment://{name}")
    if c.get("team_logo") and (LOGO_DIR / c["team_logo"]).exists():
        name = f"w{n}_{c['team_logo']}"
        files.append(discord.File(LOGO_DIR / c["team_logo"], filename=name))
        e.set_author(name=c["team"], icon_url=f"attachment://{name}")
    else:
        e.set_author(name=c["team"])
    e.set_footer(text=f"Title #{n} · ON THE RISE · PB CIRCUIT")
    return e, files


async def refresh_hall(guild: discord.Guild, data: dict | None = None):
    """Rebuild the champions list by editing the bot's messages (posting more only when it grows)."""
    data = data or load_data()
    s = guild_signups(data, guild.id)
    h = hall(s)
    ch = guild.get_channel(h["channel"] or 0)
    if ch is None:
        return
    champs = h["champions"]
    head = brand_embed(f"Every ON THE RISE: PB CIRCUIT champion, newest first.\n**{len(champs)}** title(s) won so far."
                       if champs else "No champions yet. The first tournament winner goes here.",
                       "🏆 Hall of Champions", GOLD)
    cards = [(head, [])] + [champion_card(c, i + 1) for i, c in reversed(list(enumerate(champs)))]
    # up to 10 cards and 10 files per message
    pages, cur, nfiles = [], [], 0
    for e, fs in cards:
        if len(cur) == 10 or nfiles + len(fs) > 10:
            pages.append(cur)
            cur, nfiles = [], 0
        cur.append((e, fs))
        nfiles += len(fs)
    if cur:
        pages.append(cur)
    msgs = list(h["msgs"])
    new_ids = []
    for i, page in enumerate(pages):
        embeds = [e for e, _f in page]
        files = [f for _e, fs in page for f in fs]
        msg = None
        if i < len(msgs):
            try:
                msg = await ch.fetch_message(msgs[i])
                await msg.edit(embeds=embeds, attachments=files, allowed_mentions=NO_PINGS)
            except discord.HTTPException:
                msg = None
        if msg is None:
            msg = await ch.send(embeds=embeds, files=files, allowed_mentions=NO_PINGS)
        new_ids.append(msg.id)
    for old in msgs[len(pages):]:  # the list got shorter (a title was removed)
        try:
            await (await ch.fetch_message(old)).delete()
        except discord.HTTPException:
            pass
    h["msgs"] = new_ids
    save_data(data)


async def crown_champion(guild: discord.Guild, data: dict, champ_tid: int):
    """Called when a real tournament finishes: roles for the winners, then update the champions list."""
    s = guild_signups(data, guild.id)
    tz = s.get("tourney") or {}
    t = s["teams"].get(str(champ_tid)) or {}
    tname = tz.get("name", "Tournament")
    players = [int(u) for u in t.get("roster", {})]
    winner = await get_role(guild, WINNER_ROLE, 0xE0B44A, hoist=True)
    special = await get_role(guild, champion_role_name(tname), 0xF5C542)
    for u in players:
        await give_roles(guild, u, winner, special)
    hall(s)["champions"].append({"tournament": tname, "kind": tz.get("kind", "event"), "logo": tz.get("logo"),
                                 "team": t.get("name", "Champions"), "team_logo": t.get("logo"),
                                 "team_key": str(champ_tid), "players": players,
                                 "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                 "role": special.id if special else None, "series": hall(s)["series"]})
    save_data(data)
    if tz.get("kind") == "major":
        await end_series(guild, data, players, tname)
    await refresh_hall(guild, data)


async def end_series(guild: discord.Guild, data: dict, major_winners: list[int], major_name: str):
    """The Major is over: delete this series' tournament champion roles, take Tournament Winner off everyone
    except the Major winners, and start the next series. The Major's own champion role stays."""
    s = guild_signups(data, guild.id)
    h = hall(s)
    series = h["series"]
    deleted = 0
    for c in h["champions"]:
        if c.get("series", series) != series or c.get("kind") == "major" or c.get("role_gone"):
            continue
        r = guild.get_role(c["role"]) if c.get("role") else None
        if r:
            try:
                await r.delete(reason=f"Series {series} ended with {major_name}")
                deleted += 1
            except discord.HTTPException:
                pass
        c["role_gone"] = True
    winner = role(guild, WINNER_ROLE)
    if winner:
        for mem in list(winner.members):
            if mem.id not in major_winners:
                try:
                    await mem.remove_roles(winner, reason=f"Series {series} reset")
                except discord.HTTPException:
                    pass
    h["series"] = series + 1
    save_data(data)
    ann = chan(guild, "announcements")
    if ann:
        await post(ann, f"**Series {series} is complete** with **{major_name}**.\n"
                        f"All {deleted} tournament champion role(s) from this series have been reset. "
                        f"The {major_name} champions keep their Major role and **{WINNER_ROLE}**.\n"
                        f"**Series {series + 1}** starts now: every title is up for grabs again.",
                   title=f"Series {series} complete", color=GOLD)


# one-time setup: run with /setupbot part:champions
async def championsetup(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    await get_role(guild, WINNER_ROLE, 0xE0B44A, hoist=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    h = hall(s)
    if not guild.get_channel(h["channel"] or 0):
        cat = await get_or_make_category(guild, "LEAGUE")
        ow = overwrites_for(guild, "ro")
        ow[guild.default_role] = discord.PermissionOverwrite(view_channel=True, send_messages=False,
                                                             add_reactions=True)
        ch = await guild.create_text_channel("🏆｜champions", category=cat, overwrites=ow,
                                             topic="Every ON THE RISE: PB CIRCUIT tournament champion. Updated by the bot.")
        h["channel"], h["msgs"] = ch.id, []
    if not h["champions"]:  # bring in tournaments that finished before this existed
        for old in s.get("history", []):
            if old.get("champion"):
                h["champions"].append({"tournament": old["name"], "kind": old.get("kind", "event"),
                                       "logo": (old.get("logo") or "").replace("logos/", "") or None,
                                       "team": old["champion"], "team_logo": None, "players": [],
                                       "date": (old.get("date") or "") + "T00:00:00+00:00" if old.get("date") else None,
                                       "role": None})
    save_data(data)
    await refresh_hall(guild, data)
    await interaction.followup.send(f"Champions channel ready: <#{h['channel']}>. Winners get the "
                                    f"**{WINNER_ROLE}** role plus a role for the tournament they won.", ephemeral=True)


@app_commands.describe(tournament="Tournament name", team="The winning team's role",
                       logo="Tournament logo (optional)", give_roles_to_roster="Give the roster the winner roles")
@app_commands.default_permissions(manage_roles=True)
async def addchampion(interaction: discord.Interaction, tournament: str, team: discord.Role,
                      logo: discord.Attachment | None = None, give_roles_to_roster: bool = True):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    logo_name = None
    if logo is not None:
        logo_name, problem = await save_logo(logo)
        if problem:
            return await interaction.followup.send(problem, ephemeral=True)
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    t = s["teams"].get(str(team.id)) or {}
    players = [int(u) for u in t.get("roster", {})] or [m.id for m in team.members]
    special = None
    if give_roles_to_roster:
        winner = await get_role(guild, WINNER_ROLE, 0xE0B44A, hoist=True)
        special = await get_role(guild, champion_role_name(tournament.strip()[:60]), 0xF5C542)
        for u in players:
            await give_roles(guild, u, winner, special)
    hall(s)["champions"].append({"tournament": tournament.strip()[:60], "kind": "event", "logo": logo_name,
                                 "team": t.get("name", team.name), "team_logo": t.get("logo"),
                                 "team_key": str(team.id), "players": players,
                                 "date": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                                 "role": special.id if special else None, "series": hall(s)["series"]})
    save_data(data)
    await refresh_hall(guild, data)
    await interaction.followup.send(f"Added **{t.get('name', team.name)}** as champions of **{tournament}**.",
                                    ephemeral=True)


@app_commands.describe(number="The title number shown at the bottom of its card, e.g. 3")
@app_commands.default_permissions(manage_roles=True)
async def removechampion(interaction: discord.Interaction, number: int):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    data = load_data()
    h = hall(guild_signups(data, interaction.guild.id))
    if not 1 <= number <= len(h["champions"]):
        return await interaction.response.send_message("There's no title with that number.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    gone = h["champions"].pop(number - 1)
    save_data(data)
    await refresh_hall(interaction.guild, data)
    await interaction.followup.send(f"Removed **{gone['tournament']}** from the list. (Roles already given stay; "
                                    "remove them in Server Settings if needed.)", ephemeral=True)


# ---------------------------------------------------------------- stats from a screenshot
#
# /statsimage reads a box-score screenshot with Tesseract (free OCR), matches each name to a player on the
# rosters, shows a preview, and saves it (tournament match -> box score + website; pickup -> stats + RR).
# Setup on Windows: install Tesseract from https://github.com/UB-Mannheim/tesseract/wiki (default folder),
# then `pip install pillow`. Elsewhere: install the "tesseract" package. Set TESSERACT_CMD if it's somewhere else.
import shutil as _shutil, subprocess, tempfile
from concurrent.futures import ThreadPoolExecutor
import difflib

OCR_HEADERS = {  # what Tesseract tends to read for each heading -> our field
    "pts": "pts", "2fg": "fg2", "3fg": "fg3", "ft": "ft", "orb": "orb", "ore": "orb", "drb": "drb", "dre": "drb",
    "reb": "reb", "ree": "reb", "ast": "ast", "stl": "stl", "blk": "blk", "to": "to", "foul": "pf", "pf": "pf",
    "+/-": "pm", "+f": "pm", "+/": "pm", "+-": "pm", "min": "min", "pt": "pt", "player": "player",
}
OCR_COLS = ["player", "pts", "fg2", "fg3", "ft", "orb", "drb", "reb", "ast", "stl", "blk", "to", "pf", "pm", "min", "pt"]


def tesseract_cmd():
    env = os.environ.get("TESSERACT_CMD")
    if env and os.path.exists(env):
        return env
    for p in (r"C:\Program Files\Tesseract-OCR\tesseract.exe", r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe"):
        if os.path.exists(p):
            return p
    return _shutil.which("tesseract")


def _ocr_run(cmd, img_path, *args):
    r = subprocess.run([cmd, img_path, "stdout", *args], capture_output=True, text=True, timeout=60)
    return r.stdout


def _ocr_gray(src_bytes, scale=4):
    from PIL import Image, ImageOps
    im = Image.open(io.BytesIO(src_bytes)).convert("L")
    small = im.resize((32, 32))
    if sum(small.tobytes()) / 1024 < 128:  # dark theme: make text dark on light
        im = ImageOps.invert(im)
    return im.resize((im.width * scale, im.height * scale), Image.LANCZOS)


def _ocr_thr(im, level):
    return im.point(lambda v: 255 if v > level else 0)


def read_boxscore(src_bytes: bytes) -> list[dict]:
    """Return [{'player': name, 'pts': '50', 'fg2': '11/15', ...}, ...] for every player row found."""
    cmd = tesseract_cmd()
    if not cmd:
        raise RuntimeError("Tesseract isn't installed. Install it (see the bot's setup notes) and restart the bot.")
    gray = _ocr_gray(src_bytes)
    im = _ocr_thr(gray, 160)
    tmp = tempfile.mkdtemp(prefix="otr_ocr_")
    try:
        full = os.path.join(tmp, "full.png")
        im.save(full)
        words = []
        for line in _ocr_run(cmd, full, "--psm", "11", "tsv").splitlines()[1:]:
            f = line.split("\t")
            if len(f) == 12 and f[11].strip() and float(f[10]) > 0:
                x, y, w, h = map(int, f[6:10])
                words.append({"t": f[11].strip(), "x": x + w / 2, "y": y + h / 2, "l": x, "w": w, "h": h,
                              "c": float(f[10])})
        # header row: the line with the most known headings
        best, header = 0, []
        for wd in words:
            same = [v for v in words if abs(v["y"] - wd["y"]) < 25]
            hits = [v for v in same if v["t"].lower().strip(".,:") in OCR_HEADERS]
            if len(hits) > best:
                best, header = len(hits), hits
        if best < 6:
            raise ValueError("I couldn't find the stat headings (PTS, 2FG, 3FG...). Send a clear, uncropped box score.")
        header.sort(key=lambda v: v["x"])
        cols = []
        for v in header:
            k = OCR_HEADERS[v["t"].lower().strip(".,:")]
            if k not in [c[0] for c in cols]:
                cols.append((k, v["x"]))
        stat_cols = [c for c in cols if c[0] != "player"]
        # a heading Tesseract couldn't read (often +/-) leaves a double-wide gap: put the missing column there
        order = [c for c in OCR_COLS if c != "player"]
        if len(stat_cols) >= 3:
            gaps = sorted(b[1] - a[1] for a, b in zip(stat_cols, stat_cols[1:]))
            med = gaps[len(gaps) // 2]
            fixed = [stat_cols[0]]
            for a, b in zip(stat_cols, stat_cols[1:]):
                between = order[order.index(a[0]) + 1:order.index(b[0])] if a[0] in order and b[0] in order else []
                if between and (b[1] - a[1]) > med * 1.5:
                    n = len(between)
                    for j, k in enumerate(between):
                        fixed.append((k, a[1] + (b[1] - a[1]) * (j + 1) / (n + 1)))
                fixed.append(b)
            stat_cols = fixed
        hy = header[0]["y"]
        first_x = stat_cols[0][1]
        gap = (stat_cols[1][1] - stat_cols[0][1]) if len(stat_cols) > 1 else 200
        name_right = first_x - gap * 0.5
        bottom = min([v["y"] for v in words if v["t"].upper().startswith("TOTAL") and v["y"] > hy] or [im.height])
        # player rows: words left of the first stat column, between the header and TOTALS
        cand = [v for v in words if hy + 30 < v["y"] < bottom - 20 and v["x"] < name_right
                and v["t"].lower() not in ("top", "top.") and len(v["t"]) >= 2]
        rows = []
        for v in sorted(cand, key=lambda v: v["y"]):
            if rows and abs(rows[-1][0]["y"] - v["y"]) < 40:
                rows[-1].append(v)
            else:
                rows.append([v])
        named = []
        for r in rows:
            r = [v for v in r if v["c"] >= 40] or r
            name = max(r, key=lambda v: (len(re.sub(r"[^A-Za-z0-9_]", "", v["t"])), v["c"]))
            if len(re.sub(r"[^A-Za-z0-9_]", "", name["t"])) >= 3:
                named.append((name["t"].strip(".,:;|"), name["y"]))
        if not named:
            raise ValueError("I couldn't find any player rows.")
        ys = [y for _n, y in named]
        rowh = min([b - a for a, b in zip(ys, ys[1:])] or [140])
        bounds = []
        for i, (k, x) in enumerate(stat_cols):
            left = (stat_cols[i - 1][1] + x) / 2 if i else x - gap / 2
            right = (stat_cols[i + 1][1] + x) / 2 if i + 1 < len(stat_cols) else x + gap / 2
            bounds.append((k, int(left), int(right)))

        from PIL import ImageOps
        from collections import Counter
        jobs = []
        for ri, (name, y) in enumerate(named):
            top, bot = int(y - rowh * 0.40), int(y + rowh * 0.40)
            for k, l, r in bounds:
                box = (max(0, l), max(0, top), min(gray.width, r), min(gray.height, bot))
                paths = []
                for vi, level in enumerate((140, 175, 205, None)):
                    c = gray.crop(box)
                    c = _ocr_thr(c, level) if level else c
                    p = os.path.join(tmp, f"c{ri}_{k}_{vi}.png")
                    ImageOps.expand(c, border=24, fill=255).save(p)
                    paths.append(p)
                jobs.append((ri, k, paths))

        def cell(job):
            ri, k, paths = job
            votes = Counter()
            for psm in ("7", "10"):
                for p in paths:
                    txt = _ocr_run(cmd, p, "--psm", psm, "-c", "tessedit_char_whitelist=0123456789/-+").strip()
                    if txt and re.search(r"\d", txt):
                        for i, v in enumerate(ocr_readings(k, txt)):
                            votes[v] += 1.0 if i == 0 else 0.4
                if votes and psm == "7":
                    break  # psm 10 (single character) only when nothing was read
            ranked = [v for v, _n in votes.most_common()] or [ocr_clean_cell(k, "")]
            return ri, k, ranked

        with ThreadPoolExecutor(max_workers=8) as ex:
            out = list(ex.map(cell, jobs))
        cands = [{} for _ in named]
        for ri, k, ranked in out:
            cands[ri][k] = ranked
        result = []
        for (n, _y), c in zip(named, cands):
            row = {"player": n}
            row.update({k: v[0] for k, v in c.items()})
            ocr_fix_shots(row, c)
            result.append(row)
        return result
    finally:
        _shutil.rmtree(tmp, ignore_errors=True)


def ocr_readings(k: str, txt: str) -> list[str]:
    """Every sensible way to read a cell, best first."""
    t = txt.replace(" ", "")
    if k not in ("fg2", "fg3", "ft"):
        return [ocr_clean_cell(k, t)]
    m = re.fullmatch(r"(\d+)/(\d+)", t)
    if m and int(m.group(1)) <= int(m.group(2)):
        return [f"{int(m.group(1))}/{int(m.group(2))}"]
    m = re.fullmatch(r"/(\d+)", t)
    if m:  # the made number got lost, usually a 0
        return [f"0/{m.group(1)}"]
    d = re.sub(r"\D", "", t)
    out = []
    for i in range(1, len(d)):  # slash got lost: try every split where made <= attempted
        a, b = int(d[:i]), int(d[i:])
        if a <= b and not (len(d[i:]) > 1 and d[i] == "0"):
            out.append(f"{a}/{b}")
    if len(d) == 1:
        out.append(f"{d}/{d}")
    return out or ["0/0"]


def ocr_fix_shots(row: dict, cands: dict):
    """Use PTS = 2x2FG made + 3x3FG made + FT made to pick between shaky readings of the shooting cells."""
    import itertools
    try:
        pts = int(row.get("pts") or 0)
    except ValueError:
        return
    opts = [cands.get(k, [row.get(k, "0/0")])[:4] + ["0/0"] for k in ("fg2", "fg3", "ft")]
    best = None
    for rank, combo in enumerate(itertools.product(*opts)):
        made = [int(c.split("/")[0]) for c in combo]
        if 2 * made[0] + 3 * made[1] + made[2] == pts:
            score = sum(o.index(c) for o, c in zip(opts, combo))
            if best is None or score < best[0]:
                best = (score, combo)
    if best:
        row["fg2"], row["fg3"], row["ft"] = best[1]

def ocr_clean_cell(k: str, txt: str) -> str:
    t = txt.replace(" ", "").replace("—", "").replace("–", "-")
    if k in ("fg2", "fg3", "ft"):
        m = re.search(r"(\d+)/(\d+)", t)
        if m:
            return f"{m.group(1)}/{m.group(2)}"
        d = re.sub(r"\D", "", t)
        if len(d) >= 2:  # slash misread: split in the middle
            h = len(d) // 2
            return f"{d[:h]}/{d[h:]}"
        return "0/0"
    if k == "pm":
        m = re.search(r"[-+]?\d+", t)
        return m.group(0) if m else "0"
    m = re.search(r"\d+", t)
    return m.group(0) if m else "0"


def ocr_rows_to_csv(rows: list[dict]) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["Player", "PTS", "2FG", "3FG", "FT", "ORB", "DRB", "REB", "AST", "STL", "BLK", "TO", "FOUL", "+/-",
                "MIN", "PT"])
    for r in rows:
        w.writerow([r.get(c, "") for c in OCR_COLS])
    return out.getvalue()




_stat_drafts: dict[str, dict] = {}


def stat_lookup(guild: discord.Guild, s: dict, uids: list) -> dict:
    """name (lowercase) -> Discord ID for everyone who could be in this box score."""
    look = {}
    for u in uids:
        mem = guild.get_member(int(u))
        if mem:
            for nm in {mem.display_name, mem.name, mem.global_name or ""} - {""}:
                look[nm.lower()] = int(u)
    for alias, u in s.get("aliases", {}).items():  # names learned from earlier screenshots
        if int(u) in [int(x) for x in uids]:
            look[alias] = int(u)
    return look


def match_name(name: str, look: dict) -> int | None:
    n = (name or "").strip().lower()
    mention = re.fullmatch(r"<@!?(\d+)>", n)
    if mention:
        return int(mention.group(1))
    if n.isdigit() and len(n) > 15:
        return int(n)
    if n in look:
        return look[n]
    close = difflib.get_close_matches(n, list(look), n=1, cutoff=0.72)  # OCR slips like GhostsAntham
    return look[close[0]] if close else None


def draft_preview(guild: discord.Guild, d: dict) -> discord.Embed:
    lines = []
    for r in d["rows"]:
        who = f"<@{r['uid']}>" if r.get("uid") else "❓ **not matched**"
        stat = (f"{r.get('pts', 0)} PTS · {r.get('fg2', '0/0')} 2FG · {r.get('fg3', '0/0')} 3FG · {r.get('ft', '0/0')} FT"
                f" · {r.get('reb', 0)} REB · {r.get('ast', 0)} AST · {r.get('stl', 0)} STL · {r.get('blk', 0)} BLK"
                f" · {r.get('to', 0)} TO")
        lines.append(f"**{r['player']}** → {who}\n`{stat}`")
    missing = sum(1 for r in d["rows"] if not r.get("uid"))
    tail = ("\n\n❓ Rows that aren't matched won't be saved. Click **Fix** and replace the name with the player's "
            "@mention or Discord name (I'll remember it next time)." if missing else
            "\n\nCheck the numbers, then click **Save**.")
    label = f"M{d['match']}" if d["kind"] == "tournament" else f"P{d['match']}"
    return brand_embed("\n".join(lines)[:3800] + tail, f"Stats read from screenshot · {label}", INFO)


def draft_csv(d: dict) -> str:
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["Player", "PTS", "2FG", "3FG", "FT", "ORB", "DRB", "REB", "AST", "STL", "BLK", "TO", "FOUL", "+/-",
                "MIN", "PT"])
    for r in d["rows"]:
        w.writerow([f"<@{r['uid']}>" if r.get("uid") and r.get("fixed") else r["player"]]
                   + [r.get(c, "") for c in OCR_COLS[1:]])
    return out.getvalue()


class StatFixForm(discord.ui.Modal, title="Fix the stats"):
    sheet = discord.ui.TextInput(label="One player per line (name or @mention first)", style=discord.TextStyle.paragraph,
                                 max_length=4000)

    def __init__(self, token: str):
        super().__init__()
        self.token = token
        self.sheet.default = draft_csv(_stat_drafts[token])[:4000]

    async def on_submit(self, interaction: discord.Interaction):
        d = _stat_drafts.get(self.token)
        if not d:
            return await interaction.response.send_message("That preview expired. Run /statsimage again.", ephemeral=True)
        rows = list(csv.reader(io.StringIO(self.sheet.value)))
        if rows and sheet_key(rows[0][0]) == "player":
            rows = rows[1:]
        guild = interaction.guild
        look = d["look"]
        old = d["rows"]
        new = []
        for i, row in enumerate(r for r in rows if r and any(c.strip() for c in r)):
            r = {"player": row[0].strip()}
            for j, k in enumerate(OCR_COLS[1:], start=1):
                r[k] = row[j].strip() if j < len(row) else ""
            r["uid"] = match_name(r["player"], look)
            if r["uid"] and i < len(old) and old[i]["player"] != r["player"]:
                r["ocr"] = old[i].get("ocr") or old[i]["player"]  # remember: this screenshot name = this player
                r["fixed"] = True
            elif i < len(old):
                r["ocr"] = old[i].get("ocr") or old[i]["player"]
            if r["uid"]:
                mem = guild.get_member(r["uid"])
                if r["player"].startswith("<@") and mem:
                    r["player"] = mem.display_name
            new.append(r)
        d["rows"] = new
        await interaction.response.edit_message(embed=draft_preview(guild, d), view=StatDraftView(self.token))


class StatDraftView(discord.ui.View):
    def __init__(self, token: str):
        super().__init__(timeout=1800)
        self.token = token

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        d = _stat_drafts.get(self.token)
        return bool(d) and interaction.user.id == d["user"]

    @discord.ui.button(label="Save", emoji="💾", style=discord.ButtonStyle.success)
    async def save(self, interaction: discord.Interaction, button: discord.ui.Button):
        d = _stat_drafts.pop(self.token, None)
        if not d:
            return await interaction.response.edit_message(content="That preview expired.", embed=None, view=None)
        await interaction.response.edit_message(content="Saving...", view=None)
        guild = interaction.guild
        rows = [r for r in d["rows"] if r.get("uid")]
        out = io.StringIO()
        w = csv.writer(out)
        w.writerow(["Discord ID", "Player", "PTS", "2FG", "3FG", "FT", "ORB", "DRB", "REB", "AST", "STL", "BLK", "TO",
                    "FOUL", "+/-", "MIN", "PT"])
        for r in rows:
            w.writerow([r["uid"], r["player"]] + [r.get(c, "") for c in OCR_COLS[1:]])
        data = load_data()
        s = guild_signups(data, guild.id)
        aliases = s.setdefault("aliases", {})
        for r in rows:  # learn screenshot names so next time they match on their own
            src_name = (r.get("ocr") or r["player"]).strip().lower()
            if src_name and not src_name.startswith("<@"):
                aliases[src_name] = r["uid"]
        save_data(data)
        if d["kind"] == "tournament":
            msg = await import_tourney_csv(guild, d["match"], out.getvalue())
        else:
            data = load_data()
            m = pug(guild_signups(data, guild.id))["matches"].get(str(d["match"]))
            msg = await import_pickup_csv(guild, data, m, d["match"], out.getvalue()) if m else "That pickup is gone."
            schedule_publish(guild)
        skipped = len(d["rows"]) - len(rows)
        if skipped:
            msg += f"\nSkipped {skipped} unmatched row(s)."
        await interaction.edit_original_response(content=msg, embed=None, view=None)

    @discord.ui.button(label="Fix", emoji="✏️", style=discord.ButtonStyle.primary)
    async def fix(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.token not in _stat_drafts:
            return await interaction.response.send_message("That preview expired.", ephemeral=True)
        await interaction.response.send_modal(StatFixForm(self.token))

    @discord.ui.button(label="Cancel", emoji="✖", style=discord.ButtonStyle.secondary)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        _stat_drafts.pop(self.token, None)
        await interaction.response.edit_message(content="Cancelled. Nothing was saved.", embed=None, view=None)


@bot.tree.command(description="Referees/staff/host: read stats straight from a box-score screenshot.")
@app_commands.describe(kind="Tournament match (M#) or ranked pickup (P#)", match="Match number, e.g. 7",
                       image="Box-score screenshot (one team, or both)", image2="The other team's box score (optional)")
@app_commands.choices(kind=[app_commands.Choice(name="Tournament match", value="tournament"),
                            app_commands.Choice(name="Ranked pickup", value="pickup")])
async def statsimage(interaction: discord.Interaction, kind: str, match: int, image: discord.Attachment,
                     image2: discord.Attachment | None = None):
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    if kind == "tournament":
        if not is_official(interaction.user):
            return await interaction.response.send_message("Only Referees and league staff can enter tournament stats.",
                                                           ephemeral=True)
        m = next((x for x in all_matches(s["event"]) if x["id"] == match), None)
        if m is None or m.get("a") is None or m.get("b") is None:
            return await interaction.response.send_message(f"There's no playable match M{match}.", ephemeral=True)
        uids = [int(u) for tid in (m["a"], m["b"]) for u in s["teams"].get(str(tid), {}).get("roster", {})]
    else:
        m = pug(s)["matches"].get(str(match))
        if not m or m["status"] not in ("live", "done"):
            return await interaction.response.send_message(f"There's no pickup P{match}.", ephemeral=True)
        if not can_enter_pickup_stats(interaction.user, m):
            return await interaction.response.send_message("Only the host of that pickup or staff/Referees can.",
                                                           ephemeral=True)
        uids = list(m["a"] + m["b"])
    for att in (image, image2):
        if att is not None and (att.content_type or "").split(";")[0] not in LOGO_TYPES:
            return await interaction.response.send_message("Send the box score as a PNG or JPG screenshot.",
                                                           ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    rows = []
    try:
        for att in (image, image2):
            if att is not None:
                rows += await asyncio.to_thread(read_boxscore, await att.read())
    except ImportError:
        return await interaction.followup.send("The screenshot reader needs Pillow: run `pip install pillow` on the "
                                               "bot's computer and restart the bot.", ephemeral=True)
    except Exception as e:
        return await interaction.followup.send(f"I couldn't read that screenshot: {e}", ephemeral=True)
    look = stat_lookup(guild, s, uids)
    for r in rows:
        r["ocr"] = r["player"]
        r["uid"] = match_name(r["player"], look)
    token = secrets.token_hex(6)
    _stat_drafts[token] = {"kind": kind, "match": match, "rows": rows, "user": interaction.user.id, "look": look}
    await interaction.followup.send(embed=draft_preview(guild, _stat_drafts[token]), view=StatDraftView(token),
                                    ephemeral=True)


async def publish_stats_test(guild: discord.Guild, ev: dict, names: dict) -> str:
    """Push a one-match practice page with the box score read from a screenshot to <site>/statstest/."""
    if not (GITHUB_TOKEN and GITHUB_REPO):
        return "Website test skipped: GITHUB_TOKEN and GITHUB_REPO aren't set."
    name = lambda tid: names.get(tid, "BYE")
    pname = lambda k: str(k).split("|")[0]
    totals = list(player_totals(ev, pname, name).values())
    teams = [{"name": nm, "logo": None, "captain": "", "players": [], "points": 0, "qualified": False,
              "registered": True} for nm in names.values()]
    data = {"league": LEAGUE_NAME + " (STATS TEST)", "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "teams": teams, "circuit": {"needed": None, "standings": []},
            "tourney": {"name": "Stats screenshot test", "kind": "event", "open": False, "points": None,
                        "entrants": list(names.values())},
            "stats": {"tournament_name": "Stats screenshot test", "tournament": totals,
                      "year_label": "test", "year": totals}}
    data.update(event_site_data(ev, name, pname))
    js = "window.PBL_DATA = " + json.dumps(data) + ";\n"
    try:
        async with aiohttp.ClientSession() as session:
            await put_if_changed(session, "statstest/index.html", SITE_TEMPLATE.read_bytes(), "Update stats test page")
            await github_put(session, "statstest/data.js", js.encode("utf-8"), "Stats screenshot test")
        return f"{site_url()}statstest/"
    except Exception as e:
        return f"Test page update failed: {e}"


@app_commands.describe(image="A box-score screenshot", image2="The other team's box score (optional)",
                       team1="Name for the first screenshot's team (optional)",
                       team2="Name for the second screenshot's team (optional)")
@app_commands.default_permissions(manage_messages=True)
async def teststatsimage(interaction: discord.Interaction, image: discord.Attachment,
                         image2: discord.Attachment | None = None, team1: str | None = None, team2: str | None = None):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only staff and Referees can run the stats test.", ephemeral=True)
    for att in (image, image2):
        if att is not None and (att.content_type or "").split(";")[0] not in LOGO_TYPES:
            return await interaction.response.send_message("Send the box score as a PNG or JPG screenshot.",
                                                           ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    names = {1: (team1 or "Team 1").strip()[:40], 2: (team2 or "Team 2").strip()[:40]}
    started = datetime.now()
    sides = {}
    try:
        for tid, att in ((1, image), (2, image2)):
            if att is not None:
                sides[tid] = await asyncio.to_thread(read_boxscore, await att.read())
    except ImportError:
        return await interaction.followup.send("The screenshot reader needs Pillow: run `pip install pillow` on the "
                                               "bot's computer and restart the bot.", ephemeral=True)
    except Exception as e:
        return await interaction.followup.send(f"I couldn't read that screenshot: {e}", ephemeral=True)
    secs = (datetime.now() - started).total_seconds()

    # build a one-game practice match exactly the way /statsimage would save it
    ev = new_event("swiss")
    ev["swiss"] = swiss_new([1, 2], 1, 1)
    swiss_next_round(ev)
    m = ev["swiss"]["matches"][0]
    m["a"], m["b"] = 1, 2
    m["box"] = {}
    problems = []
    for tid, rows in sides.items():
        for r in rows:
            shots = {k: made_att(r.get(k)) or (0, 0) for k in ("fg2", "fg3", "ft")}
            try:
                n = {k: cell_int(r.get(k)) for k in ("pts", "orb", "drb", "reb", "ast", "stl", "blk", "to", "pf",
                                                     "pm", "min", "pt")}
            except ValueError as e:
                problems.append(f"{r['player']}: '{e}'")
                continue
            (f2m, f2a), (f3m, f3a), (ftm, fta) = shots["fg2"], shots["fg3"], shots["ft"]
            calc = 2 * f2m + 3 * f3m + ftm
            if (f2a or f3a or fta) and calc != n["pts"]:
                problems.append(f"{r['player']}: shots add up to {calc} but PTS says {n['pts']}")
            if (n["orb"] or n["drb"]) and n["orb"] + n["drb"] != n["reb"]:
                problems.append(f"{r['player']}: ORB+DRB = {n['orb'] + n['drb']} but REB says {n['reb']}")
            m["box"][f"{r['player']}|{tid}"] = {
                "team": tid, "pts": n["pts"], "fg2m": f2m, "fg2a": f2a, "fg3m": f3m, "fg3a": f3a, "ftm": ftm,
                "fta": fta, "orb": n["orb"], "drb": n["drb"], "reb": n["reb"], "ast": n["ast"], "stl": n["stl"],
                "blk": n["blk"], "to": n["to"], "pf": n["pf"], "pm": n["pm"], "min": n["min"], "pt": n["pt"]}
    score = {tid: sum(v["pts"] for v in m["box"].values() if v["team"] == tid) for tid in (1, 2)}
    m["winner"] = 1 if score[1] >= score[2] else 2
    m["score"] = f"{max(score.values())}-{min(score.values())}"
    m["pts"] = [score[1], score[2]]
    swiss_record(ev["swiss"], m["winner"], 2 if m["winner"] == 1 else 1)
    ev["stage"] = "swiss_done"

    # what it read, as a table in Discord
    lines = []
    for tid, rows in sides.items():
        lines.append(f"**{names[tid]}** · {score[tid]} PTS")
        lines.append("```\n" + f"{'PLAYER':<14}{'PTS':>4}{'2FG':>7}{'3FG':>7}{'FT':>6}{'REB':>4}{'AST':>4}{'STL':>4}"
                     f"{'BLK':>4}{'TO':>3}\n" + "\n".join(
                         f"{r['player'][:13]:<14}{r.get('pts', 0):>4}{r.get('fg2', ''):>7}{r.get('fg3', ''):>7}"
                         f"{r.get('ft', ''):>6}{r.get('reb', 0):>4}{r.get('ast', 0):>4}{r.get('stl', 0):>4}"
                         f"{r.get('blk', 0):>4}{r.get('to', 0):>3}" for r in rows) + "\n```")
    link = await publish_stats_test(interaction.guild, ev, names)
    checks = ("✅ Every line adds up (shots = PTS, ORB + DRB = REB)." if not problems else
              "⚠️ Check these (could be a misread):\n" + "\n".join(f"• {p}" for p in problems[:10]))
    e = brand_embed("\n".join(lines)[:3300] + f"\n{checks}\n\nRead {sum(len(r) for r in sides.values())} player(s) in "
                    f"{secs:.0f}s. **Nothing was saved to the real league.**", "Stats reader test", INFO)
    if link.startswith("http"):
        e.description += f"\n\n**Test page:** {link} (give GitHub about a minute; click the game to see the box score)"
    else:
        e.description += f"\n\n{link}"
    await interaction.followup.send(embed=e, ephemeral=True)


async def scrimssetup(interaction: discord.Interaction):
    """/setupbot part:scrims: make #scrims (captains, co-captains and staff only) and delete #lfg-scrims."""
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    old = discord.utils.get(guild.text_channels, name="lfg-scrims")
    cat = old.category if old else await get_or_make_category(guild, "COMMUNITY")
    ch = chan(guild, "scrims")
    if ch is None:
        ch = await guild.create_text_channel("scrims", category=cat, overwrites=overwrites_for(guild, "captains"),
                                             topic="Captains and co-captains: set up scrims with other teams.")
        await ch.send(embed=brand_embed(
            "Captains and co-captains only. Post when your team wants a scrim (time, region, how many games) and "
            "sort it out with the other captain here or in DMs. Keep it respectful.", "🏀 Scrims", INFO))
    else:
        await ch.edit(overwrites=overwrites_for(guild, "captains"))
    note = ""
    if old:
        try:
            await old.delete(reason="Replaced by #scrims (captains and co-captains only)")
            note = " Deleted #lfg-scrims."
        except discord.HTTPException:
            note = " I couldn't delete #lfg-scrims (I need Manage Channels), so delete it by hand."
    await interaction.followup.send(f"{ch.mention} is set up: only captains, co-captains and staff can see it.{note}",
                                    ephemeral=True)


@bot.tree.command(description="Staff: one-time setup (roles/channels, rules, ranked, tickets, media, champions...).")
@app_commands.describe(part="What to set up (safe to run again)",
                       ranked_size="Ranked only: players per match (default: keep current, or 10)",
                       welcome_message="Moderation only: an extra line in every welcome card (optional)")
@app_commands.choices(part=[app_commands.Choice(name="Server: roles, channels, rules (admin)", value="server"),
                            app_commands.Choice(name="Rules: wipe #rules and repost them", value="rules"),
                            app_commands.Choice(name="Ranked 10 mans channels + queue", value="ranked"),
                            app_commands.Choice(name="Tickets", value="tickets"),
                            app_commands.Choice(name="Welcome, join log + suspensions", value="moderation"),
                            app_commands.Choice(name="Media channels", value="media"),
                            app_commands.Choice(name="Champions channel + winner role", value="champions"),
                            app_commands.Choice(name="Team voice channels", value="teamvoices"),
                            app_commands.Choice(name="Registered-teams channel", value="registered"),
                            app_commands.Choice(name="Game settings: make #game-rules and post them", value="gamerules"),
                            app_commands.Choice(name="Scrims: captains-only #scrims (deletes #lfg-scrims)", value="scrims")],
                      ranked_size=[app_commands.Choice(name="2v2", value=4), app_commands.Choice(name="3v3", value=6),
                                   app_commands.Choice(name="4v4", value=8), app_commands.Choice(name="5v5", value=10)])
@app_commands.default_permissions(manage_roles=True)
async def setupbot(interaction: discord.Interaction, part: str, ranked_size: int | None = None,
                   welcome_message: str | None = None):
    if part == "server":
        if not interaction.user.guild_permissions.administrator:
            return await interaction.response.send_message("Only server admins can run the server setup.", ephemeral=True)
        return await setup(interaction)
    if part == "ranked":
        p = pug(guild_signups(load_data(), interaction.guild.id))
        return await pickupsetup(interaction, players=ranked_size or p.get("size", 10), start_rr=p.get("start", 900),
                                 rr_swing=p.get("k", 40), teams=p.get("mode", "draft"))
    if part == "moderation":
        return await modsetup(interaction, welcome_message)
    handler = {"rules": rulessetup, "tickets": ticketsetup, "moderation": modsetup, "media": mediasetup,
               "champions": championsetup, "teamvoices": teamvoices, "registered": registeredchannel,
               "gamerules": gamerulessetup, "scrims": scrimssetup}[part]
    await handler(interaction)


# ---------------------------------------------------------------- invite tracker
#
# Remembers how many times each invite link has been used. When someone joins, the link whose count went
# up is the one they used, so we know who invited them. Logged in 📥｜join-log; /invites and
# /invites top:True show the counts. People who invite INVITE_ROLE_AT members who stay get the Recruiter role.
# The bot needs the "Manage Server" permission to see invite links.

INVITE_ROLE_AT = 3
_invite_cache: dict[int, dict[str, tuple[int, int | None]]] = {}  # guild -> code -> (uses, inviter id)


def inv(s: dict) -> dict:
    d = s.setdefault("invites", {})
    d.setdefault("joins", {})   # member id -> {"by": inviter id or None, "code": code, "at": iso, "left": bool}
    return d


async def cache_invites(guild: discord.Guild):
    try:
        invites = await guild.invites()
    except discord.HTTPException:
        print(f"[invites] {guild.name}: give the bot 'Manage Server' to track invites.")
        return
    _invite_cache[guild.id] = {i.code: (i.uses or 0, i.inviter.id if i.inviter else None) for i in invites}


def invite_counts(s: dict, uid: int) -> tuple[int, int]:
    """(people who joined with this person's links, how many of them left)"""
    joins = [j for j in inv(s)["joins"].values() if j.get("by") == uid]
    return len(joins), sum(1 for j in joins if j.get("left"))


@bot.listen("on_invite_create")
async def invite_created(invite: discord.Invite):
    if invite.guild:
        _invite_cache.setdefault(invite.guild.id, {})[invite.code] = (invite.uses or 0,
                                                                    invite.inviter.id if invite.inviter else None)


@bot.listen("on_invite_delete")
async def invite_deleted(invite: discord.Invite):
    if invite.guild:
        _invite_cache.get(invite.guild.id, {}).pop(invite.code, None)


@bot.listen("on_member_join")
async def track_invite(member: discord.Member):
    if member.bot:
        return
    guild = member.guild
    before = _invite_cache.get(guild.id, {})
    try:
        now = {i.code: (i.uses or 0, i.inviter.id if i.inviter else None) for i in await guild.invites()}
    except discord.HTTPException:
        return
    used = [c for c, (u, _who) in now.items() if u > before.get(c, (0, None))[0]]
    if not used:  # a one-use link that just got used up disappears instead of counting up
        used = [c for c in before if c not in now and before[c][1]]
    _invite_cache[guild.id] = now
    code = used[0] if len(used) == 1 else None
    by = (now.get(code) or before.get(code) or (0, None))[1] if code else None
    data = load_data()
    s = guild_signups(data, guild.id)
    old = inv(s)["joins"].get(str(member.id))
    rejoin = old is not None
    if not rejoin or old.get("by") is None:
        inv(s)["joins"][str(member.id)] = {"by": by, "code": code,
                                           "at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "left": False}
    else:
        old["left"] = False  # came back: still counts for whoever invited them first
        by = old.get("by")
    save_data(data)
    if by:
        total, left = invite_counts(s, by)
        how = f"invited by <@{by}> (code `{code}`) · they've brought **{total - left}**" + (f" ({left} left)" if left else "")
    elif code:
        how = f"joined with code `{code}`"
    elif guild.vanity_url_code:
        how = "joined with the server's vanity link (or a link I couldn't tell apart)"
    else:
        how = "couldn't tell which invite was used"
    if rejoin:
        how += " · **rejoined**"
    await mod_post(guild, s, "joinlog", brand_embed(f"{member.mention} {how}", "📨 Invite", INFO))
    if by and invite_counts(s, by)[0] - invite_counts(s, by)[1] >= INVITE_ROLE_AT:
        r = role(guild, "Recruiter")
        if r is None:
            try:
                r = await guild.create_role(name="Recruiter", colour=discord.Colour(0x22C55E), reason="Invite tracker")
            except discord.HTTPException:
                r = None
        mem = guild.get_member(by)
        if r and mem and r not in mem.roles:
            try:
                await mem.add_roles(r, reason=f"Invited {INVITE_ROLE_AT}+ members")
                await mem.send(embed=brand_embed(f"You've brought **{INVITE_ROLE_AT}+** people to **{guild.name}**. "
                                                 "You've earned the **Recruiter** role. Thanks for growing the league!",
                                                 "Recruiter unlocked", GOOD))
            except discord.HTTPException:
                pass


@bot.listen("on_member_remove")
async def track_invite_leave(member: discord.Member):
    data = load_data()
    s = guild_signups(data, member.guild.id)
    j = inv(s)["joins"].get(str(member.id))
    if j and not j.get("left"):
        j["left"] = True
        save_data(data)


@app_commands.describe(member="Whose invites (leave empty for your own)")
async def invites(interaction: discord.Interaction, member: discord.Member | None = None):
    member = member or interaction.user
    s = guild_signups(load_data(), interaction.guild.id)
    total, left = invite_counts(s, member.id)
    who = [(k, j) for k, j in inv(s)["joins"].items() if j.get("by") == member.id]
    recent = ", ".join(f"<@{k}>" + (" (left)" if j.get("left") else "") for k, j in who[-10:])
    by = inv(s)["joins"].get(str(member.id), {}).get("by")
    e = brand_embed(f"**{total - left}** still here · {total} joined · {left} left"
                    + (f"\nMost recent: {recent}" if recent else "")
                    + (f"\n{member.mention} was invited by <@{by}>" if by else ""),
                    f"{member.display_name}'s invites", INFO)
    await interaction.response.send_message(embed=e, ephemeral=True, allowed_mentions=NO_PINGS)


async def inviteleaderboard(interaction: discord.Interaction):
    s = guild_signups(load_data(), interaction.guild.id)
    counts: dict[int, list[int]] = {}
    for j in inv(s)["joins"].values():
        if j.get("by"):
            c = counts.setdefault(j["by"], [0, 0])
            c[0] += 1
            c[1] += 1 if j.get("left") else 0
    rows = sorted(counts.items(), key=lambda kv: -(kv[1][0] - kv[1][1]))[:15]
    medal = ["🥇", "🥈", "🥉"]
    lines = [f"{medal[i] if i < 3 else f'`{i + 1}.`'} <@{u}> · **{t - l}**" + (f" ({l} left)" if l else "")
             for i, (u, (t, l)) in enumerate(rows)]
    await interaction.response.send_message(
        embed=brand_embed("\n".join(lines) or "No invites tracked yet.", "Top recruiters", GOLD)
        if lines else None, content=None if lines else "No invites tracked yet. Invite your friends!",
        allowed_mentions=NO_PINGS)


# ---------------------------------------------------------------- league website (GitHub Pages)
#
# The bot pushes two files to your GitHub repo: index.html (from pbl_site.html next to this script)
# and data.js (the current draw). GitHub Pages turns the repo into a free public website.
# The site shows team names, logos, matchups, results and standings only: no Discord or Roblox names.

LEAGUE_NAME = "ON THE RISE: PB CIRCUIT"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN")
GITHUB_REPO = os.environ.get("GITHUB_REPO")  # e.g. "yourname/pbl-league"
SITE_TEMPLATE = Path(__file__).with_name("pbl_site.html")
_publish_tasks: dict[int, asyncio.Task] = {}
_last_publish: dict[int, str] = {}
_uploaded_logos: set[str] = set()  # logo files are never changed in place (a new logo gets a new name)
_uploaded_archives: set[str] = set()  # past-tournament files already on GitHub


SITE_DOMAIN = os.environ.get("SITE_DOMAIN", "ontherisepb.com").strip().strip("/")  # set SITE_DOMAIN= to turn off
_cname_done = False


def site_url() -> str | None:
    if SITE_DOMAIN:
        return f"https://{SITE_DOMAIN}/"
    if not GITHUB_REPO or "/" not in GITHUB_REPO:
        return None
    owner, repo = GITHUB_REPO.split("/", 1)
    if repo.lower() == f"{owner.lower()}.github.io":
        return f"https://{repo}/"
    return f"https://{owner}.github.io/{repo}/"


def event_site_data(ev: dict | None, name, pname=str, pavatar=None) -> dict:
    """The tournament part of the website data. `name` turns a team ID into a display name."""
    out = {"stage": ev["stage"] if ev else None, "swiss": None, "groups": None, "main": None, "champion": None}
    if not ev:
        return out
    if ev.get("drawing"):  # the live draw is on: keep the groups/matchups secret until it's over
        out["stage"], out["draw_at"] = "drawing", ev.get("draw_at")
        return out
    sw = ev.get("swiss")
    if sw:
        rows = sorted(sw["rec"].items(), key=lambda kv: (-kv[1]["w"], kv[1]["l"]))
        out["swiss"] = {
            "wins": sw["wins"], "losses": sw["losses"], "round": sw["round"],
            "table": [{"team": name(int(t)), "w": r["w"], "l": r["l"],
                       "status": "qualified" if int(t) in sw["qualified"]
                       else "out" if int(t) in sw["eliminated"] else ""} for t, r in rows],
            "matches": [{"id": m["id"], "round": m["round"], "a": name(m["a"]), "b": name(m["b"]),
                         "winner": name(m["winner"]) if m["winner"] else None, "score": m.get("score"), "box": box_rows(m, pname, name, pavatar)}
                        for m in sw["matches"]]}
    gs = ev.get("groups")
    if gs:
        lst = []
        for gi in range(len(gs["groups"])):
            order, st = group_table(gs, gi)
            lst.append({"name": f"Group {group_letter(gi)}",
                        "table": [{"team": name(t), "w": st[t]["w"], "l": st[t]["l"], "pd": st[t]["pd"],
                                   "qualified": t in gs["qualified"]} for t in order],
                        "matches": [{"id": m["id"], "round": m["round"], "a": name(m["a"]), "b": name(m["b"]),
                                     "winner": name(m["winner"]) if m["winner"] else None,
                                     "score": m.get("score"), "box": box_rows(m, pname, name, pavatar)}
                                    for m in gs["matches"] if m["group"] == gi]})
        out["groups"] = {"advance": gs["advance"], "size": gs.get("size") or max(len(g) for g in gs["groups"]),
                         "list": lst}
    seeds = ev.get("seeds") or []
    pdm = tournament_pd(ev)
    teams_in = set(seeds)
    for m in all_matches(ev):
        teams_in.update(x for x in (m.get("a"), m.get("b")) if isinstance(x, int))
    out["draw"] = {"seeds": [name(t) for t in seeds[:ev.get("protected", len(seeds))]],  # seeded teams only
                   "pd": {name(t): pdm.get(t, 0) for t in teams_in},
                   "rec": {name(t): list(team_record(ev, t)) for t in teams_in}}
    main = ev.get("main")
    if main:
        ms = []
        for m in main["matches"]:
            if m["done"] and m["winner"] is None:
                continue
            bye = (m["a_ok"] and m["a"] is None) or (m["b_ok"] and m["b"] is None)

            def slot(side):
                if m[side + "_ok"]:
                    return name(m[side])
                kind, val = m[side + "_src"]
                return f"{'Winner' if kind == 'W' else 'Loser'} of M{val}"

            ms.append({"id": m["id"], "label": m["label"], "a": slot("a"), "b": slot("b"),
                       "winner": name(m["winner"]) if m["winner"] else None,
                       "score": m.get("score"), "box": box_rows(m, pname, name, pavatar), "done": m["done"], "bye": bye,
                       "ready": (not m["done"]) and m["a_ok"] and m["b_ok"] and not bye})
        out["main"] = {"matches": ms}
        if main.get("champion"):
            out["champion"] = name(main["champion"])
    cons = ev.get("consolation")
    if cons:
        nm_ = lambda t: name(t) if t is not None else "TBD"
        out["consolation"] = {
            "bonus": cons.get("bonus_paid"), "gap": CONS_GAP,
            "champion": nm_(cons["champion"]) if cons.get("champion") else None,
            "matches": [{"id": m["id"], "label": m["label"], "a": nm_(m["a"]), "b": nm_(m["b"]),
                         "winner": nm_(m["winner"]) if m["winner"] else None, "score": m.get("score"),
                         "box": box_rows(m, pname, name, pavatar), "done": bool(m["winner"]),
                         "ready": m in cons_ready(cons)} for m in cons["matches"] if not m["bye"]]}
    return out


def closes_iso(text: str | None) -> str | None:
    """'Friday at 1 PM EST' -> an exact time for the website countdown (None if it can't be read)."""
    if not text:
        return None
    try:
        when, problem = parse_when(text, "ET")
    except Exception:
        return None
    return when.isoformat(timespec="seconds") if when and not problem else None


async def roblox_prefetch(names: list[str]):
    """Look up many Roblox usernames at once (100 per request) so the website has avatars and profile links."""
    import time as _time
    want = []
    for n in names:
        k = (n or "").strip().lower()
        hit = _rbx_cache.get(k)
        if k and re.match(r"^[A-Za-z0-9_]{3,20}$", k) and not (hit and _time.time() - hit["at"] < 6 * 3600):
            want.append(k)
    want = list(dict.fromkeys(want))
    if not want:
        return
    try:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=15)) as session:
            ids = {}
            for i in range(0, len(want), 100):
                async with session.post("https://users.roblox.com/v1/usernames/users",
                                        json={"usernames": want[i:i + 100], "excludeBannedUsers": False}) as r:
                    for u in ((await r.json()).get("data", []) if r.status == 200 else []):
                        ids[u["requestedUsername"].lower()] = u["id"]
            imgs = {}
            idl = list(ids.values())
            for i in range(0, len(idl), 100):
                async with session.get("https://thumbnails.roblox.com/v1/users/avatar-headshot",
                                       params={"userIds": ",".join(map(str, idl[i:i + 100])), "size": "150x150",
                                               "format": "Png", "isCircular": "false"}) as r:
                    for x in ((await r.json()).get("data", []) if r.status == 200 else []):
                        imgs[x["targetId"]] = x.get("imageUrl")
        now = _time.time()
        for k in want:
            uid = ids.get(k)
            _rbx_cache[k] = {"id": uid, "img": imgs.get(uid) if uid else None, "at": now}
    except Exception as e:
        print(f"[roblox batch] {e}")


def site_names(guild: discord.Guild, s: dict) -> list[str]:
    """Roblox names of every player the website lists (rosters + free agents + anyone with a profile)."""
    uids = {int(u) for _k, t in team_list(s) for u in t["roster"]} | {int(u) for u in s["free_agents"]} | \
        {int(u) for u in profiles(s)}
    out = []
    for u in uids:
        m = guild.get_member(u)
        if m and not m.bot:
            out.append(roblox_name(m))
    return out


def site_players(guild: discord.Guild, s: dict) -> list[dict]:
    """Everyone on a roster, every free agent, and anyone with a profile: for the Free agents tab and search."""
    uids = {int(u) for _k, t in team_list(s) for u in t["roster"]} | {int(u) for u in s["free_agents"]} | \
        {int(u) for u in profiles(s)}
    out = []
    for u in uids:
        m = guild.get_member(u)
        if m is None or m.bot:
            continue
        key = team_of(s, u)
        t = s["teams"].get(key) if key else None
        pr = profiles(s).get(str(u)) or {}
        rn = roblox_name(m)
        rbx = _rbx_cache.get(rn.lower()) or {}
        out.append({"name": m.display_name, "rbx": rn, "rbx_id": rbx.get("id"),
                    "img": rbx.get("img") or m.display_avatar.url, "pos": pos_of(s, u) or "",
                    "team": t["name"] if t else None,
                    "role": ("C" if t["captain"] == u else "CC" if t.get("co") == u else "") if t else "",
                    "fa": (not t) and u in s["free_agents"], "suspended": str(u) in mod(s)["suspensions"],
                    "build": pr.get("build"), "ovr": pr.get("ovr"), "activity": pr.get("activity")})
    return sorted(out, key=lambda p: p["name"].lower())


def site_events(s: dict) -> list[dict]:
    """Upcoming things with a time, soonest first: the live draw, entries closing, /remind times."""
    now = datetime.now(timezone.utc)
    tname = (s.get("tourney") or {}).get("name", "the tournament")
    ev = s.get("event") or {}
    out = []
    if ev.get("drawing"):
        out.append({"kind": "draw", "label": f"Live draw · {tname}", "at": ev.get("draw_at") or now.isoformat(),
                    "where": "#bracket on Discord", "live": True})
    elif ev.get("draw_at") and datetime.fromisoformat(ev["draw_at"]) > now:
        out.append({"kind": "draw", "label": f"Live draw · {tname}", "at": ev["draw_at"], "where": "#bracket on Discord"})
    if s.get("open") and s.get("closes_at") and datetime.fromisoformat(s["closes_at"]) > now:
        out.append({"kind": "signups", "label": f"Entries close · {tname}", "at": s["closes_at"],
                    "where": "/register in Discord"})
    labels = {"signups": f"Entries close · {tname}", "draw": f"Live draw · {tname}",
              "main": f"Main draw starts · {tname}", "matches": "Games due", "other": "Reminder"}
    where = {"signups": "/register in Discord", "draw": "#bracket on Discord", "main": "#bracket on Discord + the Main draw tab",
             "matches": "see the games below", "other": ""}
    have = {e["kind"] for e in out}
    for e in s.get("site_events", []):
        at = datetime.fromisoformat(e["at"])
        if at <= now or (e["kind"] in have and e["kind"] != "other"):
            continue
        if e["kind"] == "signups" and not s.get("open"):
            continue
        if e["kind"] == "draw" and ev.get("stage") not in (None,) and not ev.get("draw_at") and ev.get("main"):
            continue
        out.append({"kind": e["kind"], "label": (e.get("note") if e["kind"] == "other" and e.get("note") else labels[e["kind"]]),
                    "at": e["at"], "where": where[e["kind"]], "note": e.get("note") if e["kind"] != "other" else None})
    return sorted(out, key=lambda e: e["at"])


def site_schedule(s: dict, name, player) -> dict:
    """Every game that's ready: its time (or the deadline to agree one), streamer and arena. Plus recent results."""
    ev = s.get("event")
    sc = sched(s)
    games = []
    for g in open_matches(ev):
        e_ = sc["matches"].get(str(g["id"]), {})
        games.append({"id": g["id"], "head": stage_heading(g.get("label", ""), str(g["id"])), "label": g.get("label", ""),
                      "a": name(g["a"]), "b": name(g["b"]), "time": e_.get("time"), "deadline": e_.get("deadline"),
                      "stream": player(e_["stream"]) if e_.get("stream") else None, "link": e_.get("stream_link"),
                      "tracked": twitch_tracked(e_.get("stream_link")), "on_air": bool(e_.get("on_air")),
                      "arena": e_.get("arena")})
    games.sort(key=lambda g: (g["time"] is None, g["time"] or g["deadline"] or "", g["id"]))
    recent = sorted(({"id": int(mid), "head": stage_heading(e_.get("label", ""), mid), "time": e_.get("time"),
                      "stream": player(e_["stream"]) if e_.get("stream") else None, "link": e_.get("stream_link")}
                     for mid, e_ in sc["matches"].items() if e_.get("done")),
                    key=lambda r: (r["time"] or "", r["id"]), reverse=True)[:16]
    return {"games": games, "recent": recent, "preset": sc["preset"], "agree_hours": AGREE_HOURS,
            "stage_end": next((e_.get("stage_end") for e_ in sc["matches"].values()
                               if not e_.get("done") and e_.get("stage_end")), None)}


def site_rules(s: dict) -> dict:
    c = circuit(s)
    tz = s.get("tourney") or {}
    return {"cards": [{"title": t, "items": rs} for t, _c, rs in RULE_CARDS],
            "settings": [list(x) for x in GAME_SETTINGS], "report": REPORT_STEPS,
            "points": spec_text(tz["spec"]) if tz.get("spec") else spec_text(default_payout(s)),
            "target": c["needed"], "lcq_invites": LCQ_INVITES, "lcq_spots": LCQ_SPOTS, "cons_gap": CONS_GAP,
            "suspensions": {"enforcement": [v[0] for v in SUSPEND_REASONS.values() if v[1]],
                            "staff": [v[0] for v in SUSPEND_REASONS.values() if not v[1]]}}


def site_data(guild: discord.Guild) -> dict:
    s = guild_signups(load_data(), guild.id)
    c = circuit(s)
    tz = s.get("tourney")

    def name(tid):
        if tid is None:
            return "BYE"
        t = s["teams"].get(str(tid))
        if t:
            return t["name"]
        r = guild.get_role(tid)
        return r.name if r else "Removed team"

    def player(uid):
        m = guild.get_member(int(uid))
        return m.display_name if m else "Player"

    teams = []
    for key, t in team_list(s):  # every team, complete or still building
        teams.append({"name": t["name"], "complete": is_complete(t), "size": len(t["roster"]), "logo": f"logos/{t['logo']}" if t.get("logo") else None,
                      "captain": player(t["captain"]) + pos_tag(s, t["captain"]),
                      "players": [player(u) + pos_tag(s, u) for u in t["roster"] if int(u) != t["captain"]],
                      "points": t.get("points", 0), "qualified": major_qualified(s, key),
                      "registered": bool(tz and key in tz.get("entrants", []))})
    rosters = {}
    for key, t in team_list(s):
        rosters[t["name"]] = {
            "logo": f"logos/{t['logo']}" if t.get("logo") else None, "points": t.get("points", 0),
            "complete": is_complete(t), "qualified": major_qualified(s, key),
            "players": [{"name": player(u), "pos": pos_of(s, u) or "", "cap": int(u) == t["captain"],
                         "co": int(u) == t.get("co")} for u in t["roster"]]}
    data = {"league": LEAGUE_NAME, "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "teams": teams, "rosters": rosters,
            "circuit": {"needed": c["needed"],
                        "standings": sorted(({"team": t["name"], "points": t["points"], "qualified": t["qualified"]}
                                             for t in teams), key=lambda r: -r["points"])},
            "tourney": ({"name": tz["name"], "kind": tz["kind"], "open": s["open"], "closes": s.get("closes"),
                         "logo": f"logos/{tz['logo']}" if tz.get("logo") else None,
                         "winner_qualifies": tz.get("winner_qualifies", tz.get("kind") != "major"),
                         "lcq_spots": LCQ_SPOTS if tz.get("kind") == "lcq" else None,
                         "lcq": ({"invited": [name(int(k)) for k in tz.get("lcq", {}).get("invited", []) if k in s["teams"]],
                                  "next_up": [name(int(k)) for k in tz.get("lcq", {}).get("next_up", []) if k in s["teams"]],
                                  "line": [{"name": s["teams"][k]["name"], "points": s["teams"][k].get("points", 0)}
                                           for k in lcq_line(s)[:4]],
                                  "target": circuit(s)["needed"], "size": LCQ_INVITES,
                                  "playin": ({"teams": [name(int(k)) for k in tz.get("lcq", {}).get("playin", [])],
                                              "spots": tz.get("lcq", {}).get("spots", 0),
                                              "winners": [name(int(k)) for k in tz.get("lcq", {}).get("playin_winners", [])],
                                              "matches": [{"id": m["id"], "label": m["label"], "a": name(m["a"]),
                                                           "b": name(m["b"]),
                                                           "winner": name(m["winner"]) if m["winner"] else None,
                                                           "score": m.get("score"), "ready": not m["winner"],
                                                           "box": box_rows(m, player, name)}
                                                          for m in ((s.get("event") or {}).get("playin") or {}).get("matches", [])]}
                                             if tz.get("lcq", {}).get("playin") else None)} if tz.get("kind") == "lcq" else None),
                         "points": spec_text(tz["spec"]) if tz.get("spec") else None,
                         "entrants": [name(int(k)) for k in tz["entrants"] if k in s["teams"]]} if tz else None)}
    def avatar(uid):
        m = guild.get_member(int(uid)) if str(uid).isdigit() else None
        return m.display_avatar.url if m else None

    data.update(event_site_data(s["event"], name, player, avatar))
    _main = (s["event"] or {}).get("main") or {}
    if _main.get("img_v") and BRACKET_PNG.exists():  # the live bracket picture (redrawn after every game)
        data["bracket_img"] = f"bracket.png?v={_main['img_v']}"
    # games with a time that haven't been played yet; the site shows them LIVE from tip-off until the result
    pending = {str(m["id"]) for m in open_matches(s["event"])}
    data["games"] = sorted(({"id": int(mid), "head": stage_heading(e_.get("label", ""), mid), "a": name(e_["a"]),
                             "b": name(e_["b"]), "time": e_["time"],
                             "stream": player(e_["stream"]) if e_.get("stream") else None,
                             "link": e_.get("stream_link"), "host": player(e_["host"]) if e_.get("host") else None,
                             "tracked": twitch_tracked(e_.get("stream_link")), "on_air": bool(e_.get("on_air")),
                             "arena": e_.get("arena")}
                            for mid, e_ in sched(s)["matches"].items()
                            if e_.get("time") and mid in pending and not e_.get("done")),
                           key=lambda g: g["time"])
    current = player_totals(s["event"], player, name, avatar)
    year = datetime.now().year
    past = [h["players"] for h in s.get("history", []) if h.get("year") == year]
    data["stats"] = {"tournament_name": tz["name"] if tz else "Current tournament",
                     "tournament": list(current.values()),
                     "year_label": str(year), "year": list(merge_totals(*past, current).values())}
    if s["open"] and not s["event"]:
        data["stage"] = "signups"
    data["final"] = final_rows(s["event"], tz or {}, name)
    up = s.get("upcoming")
    data["upcoming"] = ({"name": up["name"], "kind": up["kind"], "open": up.get("open", False),
                         "closes": up.get("closes"), "logo": f"logos/{up['logo']}" if up.get("logo") else None,
                         "points": spec_text(up["spec"]) if up.get("spec") else None,
                         "entrants": [name(int(k)) for k in up.get("entrants", []) if k in s["teams"]]} if up else None)
    data["byes"] = [name(t) for t in ((s.get("event") or {}).get("byes") or []) if str(t) in s["teams"]]
    data["players"] = site_players(guild, s)   # Free agents tab + search
    data["media"] = {"rankings": (s.get("power_rankings") or {}).get("latest"),
                     "analysis": s.get("analysis_feed", [])[:20], "posts": s.get("media_posts", [])[:40]}
    data["events"] = site_events(s)            # countdown banner + schedule
    data["schedule"] = site_schedule(s, name, player)
    data["rules"] = site_rules(s)
    pk = pug(s)
    data["pickups"] = {
        "size": pk["size"], "queue": len(pk["queue"]),
        "queue_list": [{"player": player(u), "pos": pk["qpos"].get(str(u)), "rr": show_rr(pug_player(pk, u)),
                        "rank": show_rank(pug_player(pk, u)).split(" · ")[0]}
                       for u in pk["queue"]],
        "ranks": [[n, f"#{c:06x}"] for n, c in RANKS],
        "placements": PLACEMENTS,
        "players": [{"player": player(k), "pos": pos_of(s, k), "avatar": avatar(k), "rr": int(v["rr"]),
                     "placed": is_placed(v), "games": games_played(v), "streak": v.get("streak", 0), "rank": rank_of(v["rr"])[0],
                     "div": rank_of(v["rr"])[1], "inside": rank_of(v["rr"])[2], "w": v["w"], "l": v["l"]}
                    for k, v in sorted(pk["players"].items(), key=lambda kv: -kv[1]["rr"])],
        "matches": [{"id": m["id"], "winner": m["winner"], "gain": m.get("gain"), "loss": m.get("loss"),
                     "date": m.get("finished"), "a": [player(u) for u in m["a"]], "b": [player(u) for u in m["b"]],
                     "da": [m.get("deltas", {}).get(str(u)) for u in m["a"]],
                     "db": [m.get("deltas", {}).get(str(u)) for u in m["b"]]}
                    for m in sorted(pk["matches"].values(), key=lambda m: -int(m["id"]))
                    if m["status"] == "done"][:20]}
    # every tournament this year (and earlier), newest first, for the website's tournament picker
    data["tournaments"] = ([{"id": "current", "name": tz["name"], "kind": tz["kind"], "year": year,
                             "logo": f"logos/{tz['logo']}" if tz.get("logo") else None,
                             "date": None, "champion": data.get("champion"), "teams": len(tz.get("entrants", [])),
                             "current": True}] if tz else []) + [
        {"id": h["id"], "name": h["name"], "kind": h.get("kind", "event"), "year": h.get("year"), "logo": h.get("logo"),
         "date": h.get("date"), "champion": h.get("champion"), "teams": h.get("teams"), "current": False}
        for h in reversed(s.get("history", [])) if h.get("site")]
    return data


async def publish_test_site(guild: discord.Guild, ev: dict, spec: dict, rosters: dict, rng: random.Random) -> str:
    """Push a practice tournament (fake logos, players and box scores) to <site>/test/."""
    if not (GITHUB_TOKEN and GITHUB_REPO):
        return "Website test skipped: GITHUB_TOKEN and GITHUB_REPO aren't set."
    name = lambda tid: "BYE" if tid is None else TEST_NAMES.get(tid, "Test team")
    # fake logos ride inside data.js as data URLs, so nothing extra has to be uploaded
    logos = {nm: "data:image/svg+xml;base64," + base64.b64encode(fake_logo_svg(nm, rng).encode()).decode()
             for nm in TEST_NAMES.values()}
    placed = {t: p for p, ts in final_standings(ev) for t in ts}
    teams = [{"name": nm, "logo": logos[nm], "captain": rosters[nm][0], "players": rosters[nm][1:],
              "points": spec.get(str(placed.get(tid, 0)), 0), "qualified": tid == ev["main"].get("champion"),
              "registered": True} for tid, nm in TEST_NAMES.items()]
    totals = list(player_totals(ev, str, name).values())
    data = {"league": LEAGUE_NAME + " (TEST)", "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "teams": teams,
            "circuit": {"needed": None, "standings": sorted(({"team": t["name"], "points": t["points"],
                                                              "qualified": t["qualified"]} for t in teams),
                                                            key=lambda r: -r["points"])},
            "tourney": {"name": "Test tournament", "kind": "event", "open": False, "points": spec_text(spec),
                        "entrants": list(TEST_NAMES.values())},
            "stats": {"tournament_name": "Test tournament", "tournament": totals,
                      "year_label": f"{datetime.now().year} (test)", "year": totals}}
    data.update(event_site_data(ev, name))
    if (ev.get("main") or {}).get("matches"):  # the bracket picture, inside data.js (test only)
        try:
            pic_s = {"teams": {str(t): {"name": n} for t, n in TEST_NAMES.items()}, "tourney": {"name": "Test tournament"}}
            png = await asyncio.to_thread(bracket_picture, pic_s, ev, "Final bracket")
            data["bracket_img"] = "data:image/png;base64," + base64.b64encode(png).decode()
        except Exception as e:
            print(f"[test bracket site] {e}")
    js = "window.PBL_DATA = " + json.dumps(data) + ";\n"
    try:
        async with aiohttp.ClientSession() as session:
            await github_put(session, "test/index.html", SITE_TEMPLATE.read_bytes(), "Update test site")
            await github_put(session, "test/data.js", js.encode("utf-8"), "Test tournament data")
        return f"Test site: {site_url()}test/ (give GitHub a minute)"
    except Exception as e:
        return f"Test site update failed: {e}"


async def github_put(session: aiohttp.ClientSession, path: str, content: bytes, message: str):
    url = f"https://api.github.com/repos/{GITHUB_REPO}/contents/{path}"
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github+json",
               "User-Agent": "pbl-bot", "X-GitHub-Api-Version": "2022-11-28"}
    sha = None
    async with session.get(url, headers=headers) as r:
        if r.status == 200:
            current = await r.json()
            sha = current.get("sha")
            if base64.b64decode(current.get("content", "")) == content:
                return  # unchanged, skip the commit
        elif r.status != 404:
            raise RuntimeError(f"GitHub said {r.status}: {(await r.text())[:200]}")
    body = {"message": message, "content": base64.b64encode(content).decode()}
    if sha:
        body["sha"] = sha
    async with session.put(url, headers=headers, json=body) as r:
        if r.status not in (200, 201):
            raise RuntimeError(f"GitHub said {r.status}: {(await r.text())[:200]}")


_uploaded_hashes: dict[str, str] = {}  # path -> sha1 of what we last uploaded, to skip unchanged files


async def put_if_changed(session, path: str, content: bytes, message: str):
    """Upload only when the file changed since our last upload (fewer GitHub commits = faster Pages)."""
    import hashlib
    h = hashlib.sha1(content).hexdigest()
    if _uploaded_hashes.get(path) == h:
        return
    await github_put(session, path, content, message)
    _uploaded_hashes[path] = h


async def publish_site(guild: discord.Guild, quick: bool = False) -> str:
    """Push index.html + data.js to GitHub. Returns a short status message.
    quick=True only pushes data.js (used for the live pickup queue)."""
    if not (GITHUB_TOKEN and GITHUB_REPO):
        return "Website is off: set GITHUB_TOKEN and GITHUB_REPO before starting the bot."
    if not SITE_TEMPLATE.exists():
        return "Website: pbl_site.html is missing. Put it in the same folder as pbl_bot.py."
    if not quick:
        try:  # Roblox avatars + profile links for the Free agents tab and search (cached 6 hours)
            await roblox_prefetch(site_names(guild, guild_signups(load_data(), guild.id)))
        except Exception as e:
            print(f"[website roblox] {e}")
    js = "window.PBL_DATA = " + json.dumps(site_data(guild), indent=1) + ";\n"
    try:
        async with aiohttp.ClientSession() as session:
            global _cname_done
            if quick:
                await put_if_changed(session, "data.js", js.encode("utf-8"), "Update queue")
                _last_publish[guild.id] = datetime.now().strftime("%H:%M:%S")
                return f"Website queue updated: {site_url()}"
            if SITE_DOMAIN and not _cname_done:  # keeps GitHub Pages serving the site on the custom domain
                await github_put(session, "CNAME", (SITE_DOMAIN + "\n").encode(), "Custom domain")
                _cname_done = True
            await put_if_changed(session, "index.html", SITE_TEMPLATE.read_bytes(), "Update site")
            gs = guild_signups(load_data(), guild.id)
            for _k, t in team_list(gs) + [("tourney", gs.get("tourney") or {}), ("next", gs.get("upcoming") or {})]:
                f = t.get("logo")
                if f and f not in _uploaded_logos and (LOGO_DIR / f).exists():
                    await github_put(session, f"logos/{f}", (LOGO_DIR / f).read_bytes(), "Add team logo")
                    _uploaded_logos.add(f)
            for h in guild_signups(load_data(), guild.id).get("history", []):
                if h.get("site") and h["id"] not in _uploaded_archives:  # past tournaments: one file each
                    body = (f"(window.PBL_ARCHIVES = window.PBL_ARCHIVES || {{}})[{json.dumps(h['id'])}] = "
                            + json.dumps({k: h[k] for k in ("id", "name", "kind", "year", "date", "champion",
                                                            "teams", "points", "logo", "site") if k in h}) + ";\n")
                    await github_put(session, f"archive/{h['id']}.js", body.encode("utf-8"), "Archive tournament")
                    _uploaded_archives.add(h["id"])
            for mp in guild_signups(load_data(), guild.id).get("media_posts", []):  # /mediapost graphics
                f_ = (mp.get("image") or "").split("/")[-1]
                if f_ and f_ not in _uploaded_media and (MEDIA_DIR / f_).exists():
                    await github_put(session, f"media/{f_}", (MEDIA_DIR / f_).read_bytes(), "Add media graphic")
                    _uploaded_media.add(f_)
            if BRACKET_PNG.exists():  # upload the picture before data.js points at it
                await put_if_changed(session, "bracket.png", BRACKET_PNG.read_bytes(), "Update bracket picture")
            await put_if_changed(session, "data.js", js.encode("utf-8"), "Update tournament data")
        _last_publish[guild.id] = datetime.now().strftime("%H:%M:%S")
        return f"Website updated: {site_url()} (GitHub can take about a minute to show changes)"
    except Exception as e:  # never let a website problem break the tournament commands
        print(f"[website] {e}")
        return f"Website update failed: {e}"


_publish_full: dict[int, bool] = {}


def schedule_publish(guild: discord.Guild, delay: float = 5.0, quick: bool = False):
    """Publish a few seconds after the last change, so a burst of results makes one update.
    quick=True only uploads the data file (queue joins/leaves), unless a full update is already waiting."""
    if not (GITHUB_TOKEN and GITHUB_REPO):
        return
    old = _publish_tasks.get(guild.id)
    full = not quick
    if old and not old.done():
        full = full or _publish_full.get(guild.id, False)
        old.cancel()
    _publish_full[guild.id] = full

    async def later():
        try:
            await asyncio.sleep(delay)
            _publish_full[guild.id] = False
            msg = await publish_site(guild, quick=not full)
            print(f"[website] {msg}")
        except asyncio.CancelledError:
            pass

    _publish_tasks[guild.id] = asyncio.create_task(later())


@bot.tree.command(description="Get the link to the league website (staff: also updates it).")
async def website(interaction: discord.Interaction):
    url = site_url() or "https://ontherisepb.com/"
    view = discord.ui.View()
    for label, emoji, frag in (("Open website", "🌐", ""), ("Ranked", "🎮", "#ranked"),
                               ("Leaderboard", "🏆", "#leaderboard")):
        view.add_item(discord.ui.Button(label=label, emoji=emoji, url=url + frag))
    e = brand_embed(f"**[{url.split('//')[1].rstrip('/')}]({url})**\n\nTournament draws, standings, RISER POINTS, "
                    "box-score stats, team rosters, and the **Ranked** tab with the live queue and leaderboard.",
                    "ON THE RISE: PB CIRCUIT website", BRAND, url)
    if not is_staff(interaction.user):
        return await interaction.response.send_message(embed=e, view=view, ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    status = await publish_site(interaction.guild)
    e.set_footer(text=status[:200])
    await interaction.followup.send(embed=e, view=view, ephemeral=True)


def is_official(member: discord.Member) -> bool:
    return is_staff(member) or any(r.name == "Referee" for r in member.roles)


def chan(guild: discord.Guild, name: str) -> discord.TextChannel | None:
    return discord.utils.get(guild.text_channels, name=name)


def event_problem(s: dict, teams: list, redraw: bool) -> str | None:
    if not s.get("tourney"):
        return "Open a tournament with /opensignups first."
    if s.get("event") and s["event"].get("stage") == "playin" and not redraw:
        return "The LCQ play-in is still being played. Start the LCQ once it's finished."
    if s["open"]:
        return "Entries are still open. Run /closesignups first."
    if len(teams) < MIN_TEAMS:
        return f"There are {len(teams)} registered team(s). A tournament needs {MIN_TEAMS}."
    if s["event"] and s["event"]["stage"] == "playin" and not redraw:
        return "The LCQ play-in is still being played. Start the LCQ once it's finished."
    if s["event"] and s["event"]["stage"] not in ("done", "playin_done") and not redraw:
        return ("A tournament is already running. To throw it away and start over, "
                "run the command again with redraw set to True.")
    return None


def fresh_event(s: dict, stage: str) -> dict:
    """A new tournament event; keeps a finished LCQ play-in (its games stay in the stats)."""
    old = s.get("event") or {}
    ev = new_event(stage)
    if old.get("playin") and old.get("stage") == "playin_done":
        ev["playin"] = old["playin"]
        ev["next_id"] = max(ev["next_id"], old.get("next_id", 1))
    s["event"] = ev
    return ev


def new_event(stage: str) -> dict:
    return {"stage": stage, "next_id": 1, "swiss": None, "groups": None, "main": None}


async def start_main(guild: discord.Guild, ev: dict, seeds: list[int], note: str, post_now: bool = True):
    """Build the double-elimination main draw, post it, and post the first matches.
    post_now=False: just build it and return the posts (they go up after the live draw)."""
    if len(seeds) == 1:
        ev["stage"] = "done"
        ev["main"] = {"matches": [], "champion": seeds[0]}
        ann = chan(guild, "announcements")
        if ann:
            await post(ann, f"**{tag(seeds[0])} are the champions!** (only team to qualify)",
                           allowed_mentions=NO_PINGS)
        return []
    ev["main"] = de_build(ev, seeds)
    ev["stage"] = "main"
    de_resolve(ev["main"])
    k = ev.get("protected", len(seeds)) if not (ev.get("swiss") or ev.get("groups")) else len(seeds)
    seed_lines = "\n".join((f"#{i}: " if i <= k else "Drawn: ") + tag(t) for i, t in enumerate(seeds, 1))
    parts = [f"# Main draw: double elimination\n{note}\nLose twice and you're out. "
             "The Grand Final has a reset if the Losers bracket team wins the first game.",
             f"**Seeds**\n{seed_lines}"]
    parts += de_overview(ev["main"])
    nxt = up_next(ev["main"])
    if nxt:
        parts.append("# Play now\n" + "\n".join(nxt))
    if post_now:
        await send_blocks(chan(guild, "bracket"), parts)
    return parts


# ---------------------------------------------------------------- seeding + the live draw show
#
# Seeds come from RISER POINTS (most points = #1 seed; ties are broken by a coin flip that's saved with the
# draw). Starting a tournament runs a "live draw" in #bracket: one card the bot edits as each seed is revealed
# (lowest seed first, #1 last), then the matchups / groups are drawn one by one, then a picture of the
# finished draw is posted. Needs Pillow for the picture (`pip install pillow`); without it the show still runs.

def points_seeds(s: dict, team_ids: list[int]) -> tuple[list[int], dict]:
    """Team ids in seed order (RISER POINTS, high to low) and each team's points."""
    pts = {t: s["teams"].get(str(t), {}).get("points", 0) for t in team_ids}
    coin = {t: RNG.random() for t in team_ids}
    return sorted(team_ids, key=lambda t: (-pts[t], coin[t])), pts


# Seeding: only the top teams are seeded by RISER POINTS, how many depends on the field (one per group: 20 teams
# in groups of 4 = the top 5 head the groups; Swiss / main draw: a quarter of the field). Everyone else is drawn
# at random. Invite-only events (LCQ, Major) are completely random.

def invite_only(s: dict) -> bool:
    return (s.get("tourney") or {}).get("kind") in ("major", "lcq")


def protected_count(s: dict, n: int, groups: int | None = None) -> int:
    if invite_only(s):
        return 0
    return min(n, groups if groups else max(1, -(-n // 4)))


BYE_MIN_TEAMS = 13  # main-draw byes (top teams skip the qualifier) need more than 12 teams


def split_byes(s: dict, ids: list[int], byes: int) -> tuple[list[int], list[int], str | None]:
    """(teams that skip straight to the main draw, teams that play the qualifier, problem). The byes go to the top
    teams by RISER POINTS."""
    if not byes:
        return [], ids, None
    if len(ids) < BYE_MIN_TEAMS:
        return [], ids, f"Byes are only for tournaments with more than 12 teams (this one has {len(ids)})."
    if len(ids) - byes < MIN_TEAMS:
        return [], ids, f"That leaves only {len(ids) - byes} teams for the qualifier. Give fewer byes."
    order, _pts = points_seeds(s, ids)
    return order[:byes], [t for t in ids if t not in order[:byes]], None


async def notify_byes(guild: discord.Guild, s: dict, bye_ids: list[int], tname: str):
    for t in bye_ids:
        for uid in captains_of(s, t):
            await dm(uid, brand_embed(f"**{team_name(s, t)}** has a **bye** in **{tname}**: you skip the qualifier and go "
                                      "straight into the main draw as one of its top seeds. Watch #bracket for when it "
                                      "starts.", "🎟️ Bye to the main draw", GOLD))


def byes_note(s: dict, bye_ids: list[int]) -> str:
    if not bye_ids:
        return ""
    return (f"\n**Byes to the main draw ({len(bye_ids)}):** " + ", ".join(f"**{team_name(s, t)}**" for t in bye_ids)
            + ". The top teams by RISER POINTS skip the qualifier and go straight into the main draw as its top seeds.")


def draw_seeds(s: dict, team_ids: list[int], protected: int) -> tuple[list[int], dict]:
    """Top `protected` teams by RISER POINTS (in order), then everyone else in a random order."""
    order, pts = points_seeds(s, team_ids)
    rest = order[protected:]
    RNG.shuffle(rest)
    return order[:protected] + rest, pts


def seed_numbers(seeds: list, protected: int | None = None) -> dict:
    """{team: seed number} for the seeded teams only (unseeded teams were drawn at random)."""
    k = len(seeds) if protected is None else protected
    return {t: i for i, t in enumerate(seeds, 1) if i <= k}


def seeded_groups(seeds: list[int], count: int) -> tuple[list[list[int]], list[tuple[int, int, int]]]:
    """Pot draw: the top `count` seeds are pot 1 (one per group), the next `count` pot 2, and so on.
    Inside each pot the order is random. Returns the groups and the draw log [(team, group, pot)]."""
    groups = [[] for _ in range(count)]
    log = []
    for pot_i in range(0, len(seeds), count):
        pot = seeds[pot_i:pot_i + count]
        RNG.shuffle(pot)
        free = [gi for gi in range(count) if len(groups[gi]) == pot_i // count]
        RNG.shuffle(free)
        for t, gi in zip(pot, free):
            groups[gi].append(t)
            log.append((t, gi, pot_i // count + 1))
    return groups, log


def _font(size: int, bold: bool = True):
    from PIL import ImageFont
    names = (["ariblk.ttf", "arialbd.ttf", "seguibl.ttf", "segoeuib.ttf", "DejaVuSans-Bold.ttf",
              "Inter-Black.ttf", "LiberationSans-Bold.ttf"] if bold else
             ["arial.ttf", "segoeui.ttf", "DejaVuSans.ttf", "LiberationSans-Regular.ttf"])
    dirs = ["", "C:/Windows/Fonts/", "/usr/share/fonts/truetype/dejavu/", "/usr/share/fonts/truetype/liberation/",
            "/usr/share/fonts/TTF/", "/Library/Fonts/", "/System/Library/Fonts/Supplemental/"]
    for n in names:
        for d in dirs:
            try:
                return ImageFont.truetype(d + n, size)
            except OSError:
                continue
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def _logo(path, size: int, label: str):
    """A team's logo as a round badge (or its initials if there's no logo)."""
    from PIL import Image, ImageDraw
    im = None
    if path and Path(path).exists():
        try:
            im = Image.open(path).convert("RGBA")
            im.thumbnail((size * 2, size * 2))
            side = min(im.size)
            im = im.crop(((im.width - side) // 2, (im.height - side) // 2,
                          (im.width + side) // 2, (im.height + side) // 2)).resize((size, size))
        except Exception:
            im = None
    if im is None:
        im = Image.new("RGBA", (size, size), (40, 40, 44, 255))
        d = ImageDraw.Draw(im)
        ini = "".join(w[0] for w in label.split()[:2]).upper() or "?"
        f = _font(int(size * .38))
        w = d.textlength(ini, font=f)
        d.text(((size - w) / 2, size * .28), ini, font=f, fill=(220, 220, 220))
    mask = Image.new("L", (size, size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, size - 1, size - 1), fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(im, (0, 0), mask)
    return out


def tournament_pd(ev: dict | None) -> dict:
    """Point differential per team for this tournament (every match with a score)."""
    pd: dict[int, int] = {}
    for m in all_matches(ev):
        w = m.get("winner")
        if not w or m.get("a") is None or m.get("b") is None:
            continue
        sc = m.get("pts") or parse_score(m.get("score"))
        if not sc:
            continue
        lo = m["b"] if w == m["a"] else m["a"]
        d = int(sc[0]) - int(sc[1])
        pd[w] = pd.get(w, 0) + d
        pd[lo] = pd.get(lo, 0) - d
    return pd


def team_record(ev: dict | None, t) -> tuple[int, int]:
    """Wins and losses so far in this tournament."""
    w = l = 0
    for m in all_matches(ev):
        if m.get("winner") and t in (m.get("a"), m.get("b")):
            if m["winner"] == t:
                w += 1
            else:
                l += 1
    return w, l


def _canvas(W: int, H: int, title: str, subtitle: str, tlogo: str | None):
    from PIL import Image, ImageDraw
    img = Image.new("RGB", (W, H), (9, 9, 11))
    d = ImageDraw.Draw(img)
    for y in range(190):
        a_ = 1 - y / 190
        d.line([(0, y), (W, y)], fill=(int(9 + 60 * a_), int(9 + 22 * a_), 11))
    d.polygon([(0, 186), (W, 150), (W, 158), (0, 194)], fill=(255, 122, 0))
    x0 = 50
    if tlogo and Path(tlogo).exists():
        lg = _logo(tlogo, 130, title)
        img.paste(lg, (50, 28), lg)
        x0 = 205
    d.text((x0, 34), title.upper(), font=_font(54), fill=(245, 245, 245))
    d.text((x0, 102), subtitle.upper(), font=_font(28), fill=(255, 122, 0))
    f = _font(22)
    d.text((W - 50 - d.textlength("ON THE RISE: PB CIRCUIT", font=f), 40), "ON THE RISE: PB CIRCUIT", font=f,
           fill=(150, 150, 155))
    d.text((50, H - 40), "ontherisepb.com · ON THE RISE: PB CIRCUIT", font=_font(20, bold=False), fill=(150, 150, 155))
    return img, d


def _png(img) -> bytes:
    buf = io.BytesIO()
    img.save(buf, "PNG", optimize=True)
    return buf.getvalue()


def _team_row(img, d, x, y, w, t, s, seed_no, right, h=60):
    WHITE, GREY, ORANGE = (245, 245, 245), (150, 150, 155), (255, 122, 0)
    if t is None:
        d.text((x + 16, y + h / 2 - 14), "BYE", font=_font(26), fill=GREY)
        return
    tm = s["teams"].get(str(t), {})
    name = tm.get("name", "TBD")
    lg = _logo((LOGO_DIR / tm["logo"]) if tm.get("logo") else None, h - 10, name)
    img.paste(lg, (x + 8, y + 5), lg)
    if w < 640:  # narrow boxes: "#1 Name" on top, the stats underneath
        sd = f"#{seed_no[t]} " if seed_no.get(t) else ""
        nf = _font(24)
        sw_ = d.textlength(sd, font=nf)
        nm = name
        while d.textlength(nm, font=nf) > w - h - 30 - sw_ and len(nm) > 4:
            nm = nm[:-1]
        d.text((x + h + 12, y + 4), sd, font=nf, fill=ORANGE)
        d.text((x + h + 12 + sw_, y + 4), nm if nm == name else nm[:-1] + "…", font=nf, fill=WHITE)
        d.text((x + h + 12, y + 34), right, font=_font(18), fill=GREY)
        return
    if seed_no.get(t):
        d.text((x + h + 12, y + 6), f"#{seed_no[t]}", font=_font(20), fill=ORANGE)
    rf = _font(19)
    rw = d.textlength(right, font=rf)
    nf = _font(26)
    nm = name
    while d.textlength(nm, font=nf) > w - h - rw - 40 and len(nm) > 4:
        nm = nm[:-1]
    d.text((x + h + 12, y + 28 if seed_no.get(t) else y + 16), nm if nm == name else nm[:-1] + "…", font=nf, fill=WHITE)
    d.text((x + w - 14 - rw, y + h / 2 - 10), right, font=rf, fill=GREY)


def pair_picture(title: str, subtitle: str, sections: list, s: dict, seed_no: dict, right, tlogo) -> bytes:
    """Matchup cards. sections = [(heading or None, [(team a, team b), ...]), ...]."""
    n = sum(len(pairs) for _h, pairs in sections)
    cols = 2 if n <= 16 else 3 if n <= 36 else 4
    W = {2: 1600, 3: 2300, 4: 3000}[cols]
    cw = (W - 100 - (cols - 1) * 30) // cols
    rows_h = 0
    for head, pairs in sections:
        rows_h += (60 if head else 0) + -(-len(pairs) // cols) * 150
    H = 230 + rows_h + 60
    img, d = _canvas(W, H, title, subtitle, tlogo)
    PANEL, LINE, ORANGE = (22, 22, 26), (52, 52, 58), (255, 122, 0)
    y = 230
    for head, pairs in sections:
        if head:
            d.text((50, y + 8), head, font=_font(30), fill=ORANGE)
            y += 60
        for k, (ta, tb) in enumerate(pairs):
            cx = 50 + (k % cols) * (cw + 30)
            cy = y + (k // cols) * 150
            d.rounded_rectangle((cx, cy, cx + cw, cy + 132), 14, fill=PANEL, outline=LINE, width=2)
            _team_row(img, d, cx + 8, cy + 4, cw - 16, ta, s, seed_no, right(ta) if ta else "")
            d.line([(cx + 16, cy + 66), (cx + cw - 16, cy + 66)], fill=LINE, width=2)
            _team_row(img, d, cx + 8, cy + 68, cw - 16, tb, s, seed_no, right(tb) if tb else "")
            vs = _font(20)
            vw = d.textlength("VS", font=vs)
            d.rectangle((cx + cw / 2 - vw / 2 - 12, cy + 54, cx + cw / 2 + vw / 2 + 12, cy + 78), fill=PANEL)
            d.text((cx + cw / 2 - vw / 2, cy + 55), "VS", font=vs, fill=ORANGE)
        y += -(-len(pairs) // cols) * 150
    return _png(img)


def group_picture(title: str, subtitle: str, groups: list, s: dict, seed_no: dict, right, tlogo,
                  advance: int = 0) -> bytes:
    """Group boxes. groups = [(heading, [team, ...]), ...]; the top `advance` rows get an orange marker."""
    cols = min(4, len(groups)) if len(groups) <= 8 else 5 if len(groups) <= 15 else 6
    W = 1600 if cols <= 3 else 2200 if cols == 4 else 2700 if cols == 5 else 3200
    gw = (W - 100 - (cols - 1) * 24) // cols
    box_h = 70 + 74 * max(len(g) for _h, g in groups)
    rows = -(-len(groups) // cols)
    H = 230 + rows * (box_h + 30) + 40
    img, d = _canvas(W, H, title, subtitle, tlogo)
    PANEL, LINE, ORANGE = (22, 22, 26), (52, 52, 58), (255, 122, 0)
    for gi, (head, members) in enumerate(groups):
        cx = 50 + (gi % cols) * (gw + 24)
        cy = 230 + (gi // cols) * (box_h + 30)
        d.rounded_rectangle((cx, cy, cx + gw, cy + box_h), 14, fill=PANEL, outline=LINE, width=2)
        d.text((cx + 18, cy + 14), head, font=_font(34), fill=ORANGE)
        for k, t in enumerate(members):
            if advance and k < advance:
                d.rectangle((cx + 2, cy + 66 + k * 74 + 6, cx + 6, cy + 66 + k * 74 + 58), fill=ORANGE)
            _team_row(img, d, cx + 8, cy + 66 + k * 74, gw - 16, t, s, seed_no, right(t))
    return _png(img)


def group_schedule_text(s: dict, ev: dict, restart: str = "") -> list[str]:
    """#schedule: every group game, each with its time (TBA until the captains set one). No rounds, no byes."""
    gs = ev["groups"]
    sc = sched(s)
    parts = [f"# Group stage schedule{restart}\nEvery group game is open now. Captains: set a time for each one with "
             "`/gametime`, play, then report the score with `/game_score` (the other captain confirms it)."]
    for gi, _g in enumerate(gs["groups"]):
        lines = [f"## Group {group_letter(gi)}"]
        for m in sorted((m for m in gs["matches"] if m["group"] == gi), key=lambda m: m["id"]):
            if m["winner"]:
                lines.append(f"**M{m['id']}** {tag(m['a'])} vs {tag(m['b'])} · **Final** {m.get('score') or ''}".rstrip())
                continue
            e_ = sc["matches"].get(str(m["id"])) or {}
            when = ts(datetime.fromisoformat(e_["time"]), "f") if e_.get("time") else "**Time TBA**"
            lines.append(f"**M{m['id']}** {tag(m['a'])} vs {tag(m['b'])} · {when}")
        parts.append("\n".join(lines))
    return parts


async def post_group_schedule(guild: discord.Guild, s: dict, ev: dict, restart: str = ""):
    """Post the group schedule (text + picture) in #schedule."""
    sch = chan(guild, "schedule")
    if sch is None or not ev.get("groups"):
        return
    ids = []
    for chunk in pack(group_schedule_text(s, ev, restart), limit=3800):
        m_ = await post(sch, chunk, color=0xEF4444)
        if m_:
            ids.append(m_.id)
    try:
        png = await asyncio.to_thread(group_schedule_picture, s, ev)
        m_ = await sch.send(embed=brand_embed("Every group game, with its time once the captains set it (TBA until then).",
                                              "🗓️ Group stage schedule", INFO),
                            file=discord.File(io.BytesIO(png), filename="schedule.png"), allowed_mentions=NO_PINGS)
        ids.append(m_.id)
    except Exception as e:
        print(f"[schedule picture] {e}")
    try:  # remember them, so a reschedule can swap them for an up-to-date copy
        d2 = load_data()
        e2 = guild_signups(d2, guild.id).get("event") or {}
        if e2.get("groups"):
            e2["gs_posts"] = [sch.id, ids]
            save_data(d2)
    except Exception as e:
        print(f"[schedule posts] {e}")


async def clear_group_schedule_posts(guild: discord.Guild, ev: dict | None = None) -> int:
    """Delete the bot's group schedule posts in #schedule (the remembered ones, else found by their look)."""
    sch = chan(guild, "schedule")
    if sch is None:
        return 0
    removed = 0
    known = (ev or {}).get("gs_posts")
    if known and known[1]:
        ch = guild.get_channel(int(known[0])) or sch
        for mid_ in known[1]:
            try:
                await ch.get_partial_message(int(mid_)).delete()
                removed += 1
                await asyncio.sleep(0.4)
            except discord.HTTPException:
                pass
    # also sweep by look, in case a copy wasn't remembered
    marks = ("Group stage schedule", "## Round ", "has a bye", "tentative schedule")
    try:
        async for msg in sch.history(limit=300):
            if msg.author.id != guild.me.id:
                continue
            text = " ".join(f"{e.title or ''} {e.description or ''}" for e in msg.embeds)
            if any(k in text for k in marks) or any(a.filename == "schedule.png" for a in msg.attachments):
                try:
                    await msg.delete()
                    removed += 1
                    await asyncio.sleep(0.4)
                except discord.HTTPException:
                    pass
    except discord.HTTPException:
        pass
    return removed


_redo_tasks: dict[int, asyncio.Task] = {}


def redo_schedule_soon(guild: discord.Guild, delay: float = 30):
    """A game time moved: repost the group schedule in #schedule. Waits a little so a few changes in a row
    only redo it once."""
    old = _redo_tasks.get(guild.id)
    if old and not old.done():
        old.cancel()

    async def run():
        try:
            await asyncio.sleep(delay)
            s = guild_signups(load_data(), guild.id)
            ev = s.get("event") or {}
            if not ev.get("groups") or ev.get("stage") != "groups" or ev.get("drawing"):
                return
            await clear_group_schedule_posts(guild, ev)
            await post_group_schedule(guild, s, ev)
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[redo schedule] {e}")
    try:
        _redo_tasks[guild.id] = asyncio.get_running_loop().create_task(run())
    except RuntimeError:
        pass


@app_commands.describe(clear_old="Delete the old group schedule posts in #schedule first (default yes)")
@app_commands.default_permissions(manage_roles=True)
async def refreshschedule(interaction: discord.Interaction, clear_old: bool = True):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    s = guild_signups(load_data(), guild.id)
    ev = s.get("event") or {}
    if not ev.get("groups") or ev.get("stage") != "groups":
        return await interaction.response.send_message("There's no group stage being played right now.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    info = _show_tasks.get(guild.id)
    if ev.get("drawing") and not (info and not info["task"].done()):
        finish_drawing(guild)  # the bot restarted during the live draw: make the draw public now
    removed = 0
    if clear_old:
        removed += await clear_group_schedule_posts(guild, ev)
    try:
        await match_watch_once(guild)  # opens every group game (DMs each team their opponents)
    except Exception as e:
        print(f"[refresh schedule] {e}")
    s = guild_signups(load_data(), guild.id)
    await post_group_schedule(guild, s, s["event"])
    schedule_publish(guild)
    await interaction.followup.send(f"Group schedule reposted in #schedule"
                                    + (f" ({removed} old post(s) removed)" if removed else "")
                                    + ". Every game is open for /gametime.", ephemeral=True)


def group_schedule_picture(s: dict, ev: dict, title: str | None = None) -> bytes:
    """Tentative group stage schedule: one box per group, every round's matchups with logos (times TBD)."""
    from PIL import Image
    gs = ev["groups"]
    tz = s.get("tourney") or {}
    tlogo = str(LOGO_DIR / tz["logo"]) if tz.get("logo") and (LOGO_DIR / tz["logo"]).exists() else None
    G = len(gs["groups"])
    cols = 1 if G == 1 else 2 if G <= 4 else 3 if G <= 9 else 4
    BW = 760
    W = 100 + cols * BW + (cols - 1) * 24
    WHITE, GREY, ORANGE, PANEL, LINE = (245, 245, 245), (150, 150, 155), (255, 122, 0), (22, 22, 26), (52, 52, 58)
    GOLDC = (250, 204, 21)
    nm = lambda t: s["teams"].get(str(t), {}).get("name", "TBD")
    sc = sched(s)
    pre_tz = tzinfo(sc["preset"].get("tz", "ET"))
    tzc = sc["preset"].get("tz", "ET")

    def when_txt(m):
        if m["winner"]:
            return "FINAL " + (m.get("score") or ""), GREY
        e_ = sc["matches"].get(str(m["id"])) or {}
        if e_.get("time"):
            t = datetime.fromisoformat(e_["time"]).astimezone(pre_tz)
            return t.strftime("%a %I:%M %p").replace(" 0", " ") + f" {tzc}", WHITE
        return "TIME TBA", GOLDC
    boxes = [sorted((m for m in gs["matches"] if m["group"] == gi), key=lambda m: m["id"]) for gi in range(G)]
    RH = 56
    box_h = [86 + RH * len(ms) for ms in boxes]
    row_h = [max(box_h[i:i + cols]) for i in range(0, G, cols)]
    H = 230 + sum(h + 26 for h in row_h) + 60
    img, d = _canvas(W, H, title or tz.get("name", "Tournament"), "Group stage · schedule", tlogo)
    note = "Captains set each game's time with /gametime"
    d.text((W - 50 - d.textlength(note, font=_font(22, bold=False)), 110), note, font=_font(22, bold=False), fill=GREY)
    y0 = 230
    NAME_W = 200
    for ri in range(0, G, cols):
        for ci, gi in enumerate(range(ri, min(G, ri + cols))):
            x = 50 + ci * (BW + 24)
            h = box_h[gi]
            d.rounded_rectangle((x, y0, x + BW, y0 + h), 14, fill=PANEL, outline=LINE, width=2)
            d.text((x + 20, y0 + 16), f"GROUP {group_letter(gi)}", font=_font(34), fill=ORANGE)
            y = y0 + 72
            for m in boxes[gi]:
                d.line((x + 18, y, x + BW - 18, y), fill=(36, 36, 42), width=1)
                d.text((x + 20, y + 16), f"M{m['id']}", font=_font(18, bold=False), fill=GREY)
                for t, xx in ((m["a"], x + 74), (m["b"], x + 74 + NAME_W + 84)):
                    lg = _logo((LOGO_DIR / s["teams"][str(t)]["logo"]) if s["teams"].get(str(t), {}).get("logo")
                               else None, 36, nm(t))
                    if m["winner"] and m["winner"] != t:
                        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * .45)))
                    img.paste(lg, (xx, y + 10), lg)
                    name = nm(t)
                    d.text((xx + 44, y + 15), name, font=_fit(d, name, NAME_W - 50, 22, 13),
                           fill=GREY if m["winner"] and m["winner"] != t else WHITE)
                d.text((x + 74 + NAME_W + 30, y + 15), "vs", font=_font(20), fill=ORANGE)
                txt, col = when_txt(m)
                f = _font(20)
                d.text((x + BW - 22 - d.textlength(txt, font=f), y + 16), txt, font=f, fill=col)
                y += RH
        y0 += row_h[ri // cols] + 26
    return _png(img)


def de_round_order(main: dict) -> list[str]:
    """Round labels in play order: Winners R1, Winners R2... then Losers..., then the Grand Final(s)."""
    labels = []
    for m in main["matches"]:
        if m["label"] not in labels:
            labels.append(m["label"])
    return labels


def bracket_picture(s: dict, ev: dict, subtitle: str = "Main draw", highlight: set | None = None,
                    last: int | None = None) -> bytes:
    """The whole double-elimination bracket as a picture: upper bracket on top, lower bracket underneath,
    Grand Final on the right. Logos, scores, winners in white, losers greyed out, TBD slots named."""
    from PIL import Image
    main = ev["main"]
    tz = s.get("tourney") or {}
    tlogo = str(LOGO_DIR / tz["logo"]) if tz.get("logo") and (LOGO_DIR / tz["logo"]).exists() else None
    highlight = highlight or set()
    WHITE, GREY, DIM, ORANGE, PANEL, LINE = (245, 245, 245), (150, 150, 155), (95, 95, 102), (255, 122, 0), \
        (22, 22, 26), (60, 60, 66)
    nm = lambda t: s["teams"].get(str(t), {}).get("name", "TBD")
    show = lambda m: not (m["done"] and m["winner"] is None)  # empty slot vs empty slot: nothing to draw
    labels = de_round_order(main)
    up = [l for l in labels if l.startswith("Winners")]
    lo = [l for l in labels if l.startswith("Losers")]
    gf = [l for l in labels if l.startswith("Grand")]
    col = {l: [m for m in main["matches"] if m["label"] == l] for l in labels}
    BW, BH, GAP_X, SLOT = 330, 88, 54, 124
    up_n = max((len(col[l]) for l in up), default=1)
    lo_n = max((len(col[l]) for l in lo), default=0)
    UP_H = up_n * SLOT
    LO_H = lo_n * SLOT
    W = 100 + (max(len(up) + len(gf), len(lo)) or 1) * (BW + GAP_X)
    TOP = 250
    H = TOP + UP_H + (90 + LO_H if lo else 0) + 90
    img, d = _canvas(W, H, tz.get("name", "Tournament"), subtitle, tlogo)
    pos = {}

    def place(labels_, y0, h):
        for ci, l in enumerate(labels_):
            ms = col[l]
            x = 50 + ci * (BW + GAP_X)
            hl = l in highlight
            d.text((x, y0 - 44), l.upper() + ("  ✓" if hl else ""), font=_font(22), fill=ORANGE if hl else GREY)
            for i, m in enumerate(ms):
                cy = y0 + (i + 0.5) * (h / max(1, len(ms)))
                pos[m["id"]] = (x, cy)
    place(up, TOP + 40, UP_H)
    if gf:
        gx = 50 + len(up) * (BW + GAP_X)
        for i, l in enumerate(gf):
            for m in col[l]:
                pos[m["id"]] = (gx + i * 0, TOP + 40 + UP_H / 2 + i * (BH + 40))
        d.text((gx, TOP - 4), "GRAND FINAL" + ("  ✓" if set(gf) & highlight else ""), font=_font(22),
               fill=ORANGE if set(gf) & highlight else GREY)
    if lo:
        ly = TOP + 40 + UP_H + 90
        d.text((50, ly - 86), "LOWER BRACKET", font=_font(26), fill=(200, 200, 205))
        d.line((50, ly - 54, W - 50, ly - 54), fill=LINE, width=2)
        place(lo, ly, LO_H)
    # connector lines inside each bracket half (drop-downs from upper to lower are left out)
    by_id = {m["id"]: m for m in main["matches"]}
    for m in main["matches"]:
        if m["id"] not in pos or not show(m):
            continue
        x, cy = pos[m["id"]]
        for side, src in (("a", m["a_src"]), ("b", m["b_src"])):
            if src[0] != "W" or src[1] not in pos or not show(by_id[src[1]]):
                continue
            sx, sy = pos[src[1]]
            if sx >= x:
                continue
            ty = cy - BH / 4 if side == "a" else cy + BH / 4
            mx = sx + BW + GAP_X / 2
            d.line((sx + BW, sy, mx, sy), fill=LINE, width=3)
            d.line((mx, sy, mx, ty), fill=LINE, width=3)
            d.line((mx, ty, x, ty), fill=LINE, width=3)
    for m in main["matches"]:
        if m["id"] not in pos or not show(m):
            continue
        x, cy = pos[m["id"]]
        y = cy - BH / 2
        live = not m["done"] and m["a_ok"] and m["b_ok"]
        just = last is not None and m["id"] == last
        GOLDC = (250, 204, 21)
        d.rounded_rectangle((x, y, x + BW, y + BH), 10, fill=PANEL,
                            outline=GOLDC if just else ORANGE if live else LINE, width=4 if just else 2)
        d.text((x + 10, y - 2 - 20), f"M{m['id']}" + ("  · JUST FINISHED" if just else "  · PLAY NOW" if live else ""),
               font=_font(16, bold=just), fill=GOLDC if just else ORANGE if live else DIM)
        sc = parse_score(m.get("score"))
        for k, side in enumerate(("a", "b")):
            ry = y + 6 + k * (BH / 2 - 2)
            if m[side + "_ok"]:
                t = m[side]
                if t is None:
                    d.text((x + 50, ry + 8), "BYE", font=_font(20, bold=False), fill=DIM)
                    continue
                won = m["done"] and m["winner"] == t
                lost = m["done"] and m["loser"] == t
                lg = _logo((LOGO_DIR / s["teams"][str(t)]["logo"]) if s["teams"].get(str(t), {}).get("logo") else None,
                           32, nm(t))
                if lost:
                    lg.putalpha(lg.getchannel("A").point(lambda v: int(v * .45)))
                img.paste(lg, (int(x + 10), int(ry + 4)), lg)
                name = nm(t)
                d.text((x + 50, ry + 7), name, font=_fit(d, name, BW - 110, 21, 13),
                       fill=WHITE if won or not m["done"] else GREY)
                if m["done"] and m["loser"] is not None:
                    pts_ = (max(sc) if won else min(sc)) if sc else ("W" if won else "L")
                    f = _font(22)
                    d.text((x + BW - 14 - d.textlength(str(pts_), font=f), ry + 6), str(pts_), font=f,
                           fill=ORANGE if won else DIM)
            else:
                kind, val = m[side + "_src"]
                d.text((x + 50, ry + 9), f"{'Winner' if kind == 'W' else 'Loser'} of M{val}", font=_font(18, bold=False),
                       fill=DIM)
        d.line((x + 8, y + BH / 2, x + BW - 8, y + BH / 2), fill=(40, 40, 46), width=1)
    if main.get("champion"):
        c = main["champion"]
        msg = f"CHAMPIONS: {nm(c).upper()}"
        f = _font(34)
        d.text((W - 50 - d.textlength(msg, font=f), 110), msg, font=f, fill=ORANGE)
    return _png(img)


def rounds_just_done(main: dict) -> list[str]:
    """Main-draw rounds that are now fully played and haven't had a bracket picture yet (marks them posted)."""
    posted = main.setdefault("rounds_posted", [])
    done = [l for l in de_round_order(main)
            if l not in posted and all(m["done"] for m in main["matches"] if m["label"] == l)
            and any(m["done"] and m["loser"] is not None for m in main["matches"] if m["label"] == l)]
    posted += done
    return done


BRACKET_PNG = Path(__file__).with_name("bracket_live.png")  # the live bracket picture for the website


def _keep_live_fields(gid: int, fields: dict):
    """Write the live-picture bookkeeping straight to disk too (some callers have already saved)."""
    try:
        d2 = load_data()
        m2 = ((guild_signups(d2, gid).get("event") or {}).get("main"))
        if m2 is not None:
            m2.update(fields)
            save_data(d2)
    except Exception as e:
        print(f"[bracket live] {e}")


async def post_bracket_update(guild: discord.Guild, s: dict, ev: dict, game: dict | None = None):
    """After EVERY reported main-draw game: redraw the bracket picture, put it on the website, and replace the
    live bracket post in #bracket (the old picture is deleted, so there's only ever one, always at the bottom).
    The final bracket stays up for good."""
    main = ev.get("main") or {}
    if not main.get("matches"):
        return
    done = rounds_just_done(main)  # rounds finished by this game get a ✓ on the picture
    champ = main.get("champion")
    if game:
        sub = f"Live · after M{game['id']} ({game['label']})"
    else:
        sub = "Live bracket"
    try:
        png = await asyncio.to_thread(bracket_picture, s, ev, "Final bracket" if champ else sub, set(done),
                                      None if champ or not game else game["id"])
    except ImportError:
        return
    except Exception as e:
        print(f"[bracket picture] {e}")
        return
    import hashlib
    try:  # the website shows the same picture
        BRACKET_PNG.write_bytes(png)
        main["img_v"] = hashlib.sha1(png).hexdigest()[:10]
        schedule_publish(guild)
    except Exception as e:
        print(f"[bracket website] {e}")
    ch = chan(guild, "bracket")
    if ch is None:
        return _keep_live_fields(guild.id, {"img_v": main.get("img_v"), "rounds_posted": main.get("rounds_posted", [])})
    old = main.get("live_msg")
    if old:  # one live picture at a time
        try:
            oc = guild.get_channel(int(old[0])) or ch
            await (await oc.fetch_message(int(old[1]))).delete()
        except Exception:
            pass
    if champ:
        title, text = "🏆 FINAL BRACKET", f"**{team_name(s, champ)}** are the champions!"
    else:
        what = ""
        if game and game.get("done") and game.get("winner") is not None and game.get("loser") is not None:
            what = (f"**{team_name(s, game['winner'])}** beat **{team_name(s, game['loser'])}**"
                    + (f" {game['score']}" if game.get("score") else "") + f" in M{game['id']} ({game['label']}).")
        if done:
            what += f"\n**{', '.join(done)}** is complete."
        title = "📊 LIVE BRACKET" + (f" · {', '.join(done)} complete" if done else "")
        nxt = up_next(main)
        text = (what or "Here's the bracket right now.") + \
            ("\n\n**Up next**\n" + "\n".join(nxt[:12]) if nxt else "") + \
            "\n\n*Updates after every reported game.*"
    url = site_url()
    if url:
        text += f"\n[Live bracket on the website]({url}#bracket)"
    e = brand_embed(text, title, GOLD)
    e.set_image(url="attachment://bracket.png")
    try:
        msg = await ch.send(embed=e, file=discord.File(io.BytesIO(png), filename="bracket.png"),
                            allowed_mentions=NO_PINGS)
        main["live_msg"] = None if champ else [ch.id, msg.id]  # the final bracket is never deleted
    except Exception as e_:
        print(f"[bracket post] {e_}")
    _keep_live_fields(guild.id, {"img_v": main.get("img_v"), "live_msg": main.get("live_msg"),
                                 "rounds_posted": main.get("rounds_posted", [])})


def draw_picture(title: str, subtitle: str, kind: str, s: dict, ev: dict, seeds: list[int], pts: dict,
                 tlogo: str | None, protected: int | None = None) -> bytes:
    """The picture for a live draw: group boxes, Swiss round 1, or the main draw's first round.
    Every team shows its seed (seeded teams only), RISER POINTS and point differential (PD) in this tournament."""
    seed_no = seed_numbers(seeds, protected)
    pd = tournament_pd(ev)
    right = lambda t: f"{pts.get(t, 0)} RP · PD {pd.get(t, 0):+d}"
    if kind == "groups":
        groups = [(f"GROUP {group_letter(gi)}", g) for gi, g in enumerate(ev["groups"]["groups"])]
        return group_picture(title, subtitle, groups, s, seed_no, right, tlogo)
    if kind == "swiss":
        pairs = [(m["a"], m["b"]) for m in ev["swiss"]["matches"] if m["round"] == 1]
        pairs += [(int(t), None) for t, r in ev["swiss"]["rec"].items() if r["bye"]]
    else:
        pairs = [(m["a"] if m["a_ok"] else None, m["b"] if m["b_ok"] else None)
                 for m in ev["main"]["matches"] if m.get("label") == "Winners R1"]
        pairs = [pr for pr in pairs if pr[0] or pr[1]]
    return pair_picture(title, subtitle, [(None, pairs)], s, seed_no, right, tlogo)


def group_standings_picture(s: dict, ev: dict) -> bytes:
    """Live group tables: order, W-L, PD and RISER POINTS. Top teams (going through) are marked."""
    gs = ev["groups"]
    tz = s.get("tourney") or {}
    tlogo = str(LOGO_DIR / tz["logo"]) if tz.get("logo") and (LOGO_DIR / tz["logo"]).exists() else None
    seed_no = seed_numbers(ev.get("seeds") or [], ev.get("protected"))
    stats = {}
    groups = []
    for gi in range(len(gs["groups"])):
        order, st = group_table(gs, gi)
        stats.update(st)
        groups.append((f"GROUP {group_letter(gi)}", order))
    right = lambda t: (f"{stats[t]['w']}-{stats[t]['l']} · PD {stats[t]['pd']:+d} · "
                       f"{s['teams'].get(str(t), {}).get('points', 0)} RP")
    played = sum(1 for m in gs["matches"] if m["winner"])
    return group_picture(tz.get("name", "Tournament"), f"Group standings · {played}/{len(gs['matches'])} games played",
                         groups, s, seed_no, right, tlogo, advance=gs["advance"])


def swiss_round_picture(s: dict, ev: dict) -> bytes:
    """This Swiss round's matchups, grouped by record (2-0 pool, 1-1 pool...), with W-L, PD and RISER POINTS."""
    sw = ev["swiss"]
    tz = s.get("tourney") or {}
    tlogo = str(LOGO_DIR / tz["logo"]) if tz.get("logo") and (LOGO_DIR / tz["logo"]).exists() else None
    pd = tournament_pd(ev)
    rec = sw["rec"]
    rnd = sw["round"]
    ms = [m for m in sw["matches"] if m["round"] == rnd]

    def before(t):  # the record each team had going into this round
        r = rec[str(t)]
        w, l = r["w"], r["l"]
        for m in ms:
            if m["winner"] and t in (m["a"], m["b"]):
                w, l = (w - 1, l) if m["winner"] == t else (w, l - 1)
        return w, l
    pools: dict[tuple, list] = {}
    for m in ms:
        pools.setdefault(before(m["a"]), []).append((m["a"], m["b"]))
    sections = [(f"{w}-{l} POOL", pools[(w, l)]) for (w, l) in sorted(pools, key=lambda k: (-k[0], k[1]))]
    right = lambda t: (f"{rec[str(t)]['w']}-{rec[str(t)]['l']} · PD {pd.get(t, 0):+d} · "
                       f"{s['teams'].get(str(t), {}).get('points', 0)} RP")
    return pair_picture(tz.get("name", "Tournament"), f"Swiss · round {rnd} · teams drawn at random within each record",
                        sections, s, {}, right, tlogo)


async def post_picture(guild: discord.Guild, channel_name: str, pic_fn, *args, edit_key: tuple | None = None):
    """Make a picture (needs Pillow) and post it. With edit_key=(dict, key) the same message is edited each time."""
    ch = chan(guild, channel_name)
    if ch is None:
        return
    try:
        png = await asyncio.to_thread(pic_fn, *args)
    except ImportError:
        return
    except Exception as e:
        print(f"[picture] {e}")
        return
    f = discord.File(io.BytesIO(png), filename="standings.png")
    if edit_key:
        holder, key = edit_key
        if holder.get(key):
            try:
                msg = await ch.fetch_message(holder[key])
                await msg.edit(attachments=[f])
                return
            except discord.HTTPException:
                pass
        msg = await ch.send(file=f)
        holder[key] = msg.id
    else:
        await ch.send(file=f)


DRAW_COUNTDOWN_MIN = 5  # default minutes between starting a tournament and the live draw (0 = right away)


def _countdown_text(left: int) -> str:
    if left >= 60:
        mins, secs = divmod(left, 60)
        return f"{mins}:{secs:02d}"
    return f"{left}"


async def draw_show(guild: discord.Guild, kind: str, seeds: list[int], pts: dict, extra: list[str], note: str,
                    by_points: bool = True, test: dict | None = None, countdown: int = 0,
                    protected: int | None = None):
    """The LIVE DRAW in #bracket, built to be watched (and re-watched):
      0. countdown: an @here in #announcements, then a ticking countdown card in #bracket
      1. intro card with the tournament logo
      2. seeds: lower seeds revealed on one card, the top 8 each get their own reveal, drum roll for #1
      3. the draw: one card per group (filled pot by pot, with a live ticker) or the matchups, one at a time
      4. DRAW COMPLETE with a link back to the start, the picture, and the announcement
    Every step is its own message, so scrolling up replays the whole show.
    test = {"s": fake league data, "ev": fake event, "channel": where to post}: a practice draw, nothing saved."""
    ch = test["channel"] if test else chan(guild, "bracket")
    if ch is None:
        return
    if test:
        s, ev = test["s"], test["ev"]
    else:
        data = load_data()
        s = guild_signups(data, guild.id)
        ev = s.get("event") or {}
    tz = s.get("tourney") or {}
    tname = ("TEST · " if test else "") + tz.get("name", "Tournament")
    name = lambda t: s["teams"].get(str(t), {}).get("name", "TBD")
    label = lambda t: f"**{name(t)}**"
    tlogo_path = (LOGO_DIR / tz["logo"]) if tz.get("logo") and (LOGO_DIR / tz["logo"]).exists() else None
    n = len(seeds)
    pace = max(1.0, min(2.6, 140 / max(1, n)))
    pd = tournament_pd(ev)
    k_seeded = len(seeds) if protected is None else protected  # the rest were drawn at random
    no = seed_numbers(seeds, k_seeded)
    RED = 0xEF4444

    async def send(**kw):
        msg = await ch.send(allowed_mentions=NO_PINGS, **kw)
        if test:
            remember_test_msg(guild, msg)
        return msg

    def tfile():
        return discord.File(tlogo_path, filename=tlogo_path.name) if tlogo_path else None

    def team_line(t) -> str:
        pdt = f" · PD {pd[t]:+d}" if pd.get(t) else ""
        return (f"**#{no[t]}** " if t in no else "🎲 ") + f"{label(t)} · {pts.get(t, 0)} RP{pdt}"

    # 0. countdown
    if countdown > 0:
        at = datetime.now(timezone.utc) + timedelta(seconds=countdown)
        ann = None if test else chan(guild, "announcements")
        if ann:
            await ann.send(content="@here", embed=brand_embed(
                f"The **LIVE DRAW** for **{tname}** starts {ts(at, 'R')} in {ch.mention}.\n"
                "Seeds, groups and matchups are revealed one by one. Tune in!", "🎥 LIVE DRAW INCOMING", GOLD),
                allowed_mentions=discord.AllowedMentions(everyone=True, users=False, roles=False))
        cd = await send(embed=brand_embed(f"# ⏳ {_countdown_text(countdown)}\nThe draw starts {ts(at, 'R')}. "
                                          f"Stay right here.", f"🎥 LIVE DRAW · {tname}", GOLD))
        left = countdown
        while left > 0:
            step = 30 if left > 90 else 15 if left > 30 else 5 if left > 10 else 1
            step = min(step, left)
            await asyncio.sleep(step)
            left -= step
            try:
                await cd.edit(embed=brand_embed(
                    (f"# ⏳ {_countdown_text(left)}" if left > 0 else "# 🔴 WE'RE LIVE") +
                    (f"\nThe draw starts {ts(at, 'R')}. Stay right here." if left > 0 else ""),
                    f"🎥 LIVE DRAW · {tname}", RED if left <= 10 else GOLD))
            except discord.HTTPException:
                pass

    # 1. intro
    fmt = {"groups": "Group stage draw", "swiss": "Swiss qualifier · round 1", "main": "Main draw · first round"}[kind]
    seeding = ("Seeds come from the **qualifier results**." if not by_points else
               "🎲 **Completely random draw**: invite-only event, nobody is seeded." if k_seeded == 0 else
               f"The top **{k_seeded}** by **RISER POINTS** are seeded; the other {n - k_seeded} are drawn **at random** 🎲."
               if k_seeded < n else "Seeds are set by **RISER POINTS** (most points = #1 seed).")
    intro = brand_embed(f"# 🎥 IT'S DRAW TIME\n**{n} teams** · {fmt}\n\n{seeding}\n{note}", tname, GOLD)
    f = tfile()
    if f:
        intro.set_image(url=f"attachment://{tlogo_path.name}")
    imsg = await send(embed=intro, **({"file": f} if f else {}))
    await asyncio.sleep(4)

    # 2. seeds
    top = min(8, k_seeded) if k_seeded > 4 else k_seeded
    lower = list(range(k_seeded, top, -1))  # seed numbers, lowest first
    batch = 1 if n <= 12 else 2 if n <= 24 else 4
    shown = []
    seeds_card = None
    if lower:
        seeds_card = await send(embed=brand_embed("🥁 Revealing the seeds...", f"📋 SEEDS · {tname}", GOLD))
        await asyncio.sleep(2)
        for i in range(0, len(lower), batch):
            for k in lower[i:i + batch]:
                shown.insert(0, team_line(seeds[k - 1]))
            body = "\n".join(shown[:30]) + (f"\n*...and {len(shown) - 30} more*" if len(shown) > 30 else "")
            await seeds_card.edit(embed=brand_embed(body + f"\n\n*Top {top} coming up...*", f"📋 SEEDS · {tname}", GOLD))
            await asyncio.sleep(pace)
        await asyncio.sleep(2)
    unseeded = seeds[k_seeded:]
    if unseeded:  # everyone else goes in the hat
        await send(embed=brand_embed(", ".join(label(t) for t in sorted(unseeded, key=name))[:3900],
                                     f"🎲 IN THE HAT · {len(unseeded)} teams drawn at random", INFO))
        await asyncio.sleep(3)
    for k in range(top, 0, -1):  # the top seeds each get their own moment
        t = seeds[k - 1]
        tf = logo_file(s["teams"].get(str(t), {})) if not test else None
        pdt = f" · PD {pd[t]:+d}" if pd.get(t) else ""
        reveal = brand_embed(f"## {'👑 THE #1 SEED' if k == 1 else f'🔥 #{k} SEED'}\n# {name(t)}\n"
                             f"{pts.get(t, 0)} RISER POINTS{pdt}", None, 0xF5C542 if k == 1 else GOLD)
        if tf:
            reveal.set_thumbnail(url=f"attachment://{tf.filename}")
        if k == 1:
            drum = await send(embed=brand_embed("# 🥁 And the #1 seed is...", None, RED))
            await asyncio.sleep(3.5)
            try:
                await drum.edit(embed=reveal, **({"attachments": [tf]} if tf else {}))
            except discord.HTTPException:
                await send(embed=reveal, **({"file": tf} if tf else {}))
        else:
            await send(embed=reveal, **({"file": tf} if tf else {}))
            await asyncio.sleep(pace * 1.4)
    await asyncio.sleep(3)

    # 3. the draw
    if kind == "groups" and ev.get("groups"):
        groups = ev["groups"]["groups"]
        G = len(groups)
        placed = [[] for _ in range(G)]
        await send(embed=brand_embed(f"# 🎱 THE GROUP DRAW\n{note}", tname, GOLD))
        def gcard(gi):
            lines = [team_line(t) for t in placed[gi]] or ["*waiting...*"]
            return brand_embed("\n".join(lines), f"GROUP {group_letter(gi)}", INFO)
        gmsgs = []  # up to 4 group cards per message
        for i in range(0, G, 4):
            gmsgs.append(await send(embeds=[gcard(gi) for gi in range(i, min(G, i + 4))]))
        ticker = await send(embed=brand_embed("Drawing pot 1...", "🎱 LIVE", RED))
        pots = max(len(g) for g in groups)
        rnd = random.Random(sum(seeds))
        for pk in range(pots):
            in_pot = [(gi, g[pk]) for gi, g in enumerate(groups) if len(g) > pk]
            rnd.shuffle(in_pot)
            lo_, hi_ = pk * G + 1, pk * G + len(in_pot)
            what = (f"Seeds #{lo_}-#{hi_}, one per group." if hi_ <= k_seeded else
                    "Drawn at random, one per group." if lo_ > k_seeded else "One per group.")
            await ticker.edit(embed=brand_embed(f"# POT {pk + 1}\n{what}", "🎱 LIVE", RED))
            await asyncio.sleep(pace * 1.5)
            for gi, t in in_pot:
                placed[gi].append(t)
                await ticker.edit(embed=brand_embed(f"# POT {pk + 1}\n{team_line(t)}\n## ➜ GROUP {group_letter(gi)}",
                                                    "🎱 LIVE", RED))
                gm = gmsgs[gi // 4]
                try:
                    await gm.edit(embeds=[gcard(x) for x in range(gi // 4 * 4, min(G, gi // 4 * 4 + 4))])
                except discord.HTTPException:
                    pass
                await asyncio.sleep(pace)
        await ticker.edit(embed=brand_embed("Every group is set.", "🎱 DONE", GOOD))
    else:
        if kind == "swiss" and ev.get("swiss"):
            pairs = [(m["a"], m["b"], m["id"]) for m in ev["swiss"]["matches"] if m["round"] == 1]
            pairs += [(int(t), None, None) for t, r in ev["swiss"]["rec"].items() if r["bye"]]
        elif ev.get("main"):
            pairs = [((m["a"] if m["a_ok"] else None), (m["b"] if m["b_ok"] else None), m["id"])
                     for m in ev["main"]["matches"] if m.get("label") == "Winners R1"]
            pairs = [x for x in pairs if x[0] or x[1]]
        else:
            pairs = []
        await send(embed=brand_embed(f"# 🏀 THE MATCHUPS\n{note}", tname, GOLD))
        page, lines = None, []
        for i, (x, y, mid) in enumerate(pairs):
            if i % 8 == 0:
                lines = []
                page = await send(embed=brand_embed("*drawing...*", f"MATCHUPS {i + 1}-{min(len(pairs), i + 8)}", INFO))
            if x and y:
                lines.append(f"**M{mid}** {team_line(x)}\n　vs {team_line(y)}")
            else:
                lines.append(f"{team_line(x or y)} · **bye**")
            await page.edit(embed=brand_embed("\n\n".join(lines), f"MATCHUPS {i // 8 * 8 + 1}-{min(len(pairs), i // 8 * 8 + 8)}",
                                              INFO))
            await asyncio.sleep(pace)
        if not pairs and extra:
            await send(embed=brand_embed("\n".join(extra[:40]), "MATCHUPS", INFO))

    # 4. done
    await asyncio.sleep(2)
    await send(embed=brand_embed(f"# ✅ DRAW COMPLETE\nGood luck to every team!\n\n"
                                 f"Missed it? [Watch the draw from the start]({imsg.jump_url})", tname, GOOD))
    try:
        pic = await asyncio.to_thread(draw_picture, tname, {"groups": "Final groups", "swiss": "Swiss · round 1",
                                                            "main": "Main draw · first round"}[kind],
                                      kind, s, ev, seeds, pts, str(tlogo_path) if tlogo_path else None, k_seeded)
        await send(embed=brand_embed(None, {"groups": "📋 FINAL GROUPS", "swiss": "📋 ROUND 1 MATCHUPS",
                                            "main": "📋 FIRST ROUND"}[kind] + f" · {tname}", GOLD),
                   file=discord.File(io.BytesIO(pic), filename="draw.png"))
        if kind == "groups" and ev.get("groups"):
            sched_pic = await asyncio.to_thread(group_schedule_picture, s, ev, tname)
            await send(embed=brand_embed("Every group's games, round by round. **Times are TBD:** captains agree them "
                                         "in #scheduling once each round opens (you'll get a DM).",
                                         f"🗓️ TENTATIVE SCHEDULE · {tname}", INFO),
                       file=discord.File(io.BytesIO(sched_pic), filename="schedule.png"))
        ann = (chan(guild, "announcements") if test.get("announce") else None) if test else chan(guild, "announcements")
        if ann:
            amsg = await ann.send(embed=brand_embed(
                f"The draw for **{tname}** is out! Missed it? [Watch the replay from the start]({imsg.jump_url}) "
                f"in {ch.mention}." + ("\n*Practice run: nothing here is real.*" if test else ""),
                ("TEST · " if test else "") + "The draw is out", GOLD),
                file=discord.File(io.BytesIO(pic), filename="draw.png"), allowed_mentions=NO_PINGS)
            if test:
                remember_test_msg(guild, amsg)
    except ImportError:
        await send(content="(Install Pillow on the bot's computer, `pip install pillow`, to get a picture of the draw.)")
    except Exception as e:
        print(f"[draw picture] {e}")


def main_r1_lines(ev: dict, no: dict, nm) -> list[str]:
    """The main draw's first-round matchups (and byes) as lines for the live draw card."""
    out = []
    for m in ev["main"]["matches"]:
        if m.get("label") != "Winners R1":
            continue
        a, b = (m["a"] if m["a_ok"] else None), (m["b"] if m["b_ok"] else None)
        if a and b:
            out.append(f"**M{m['id']}** #{no[a]} {nm(a)} vs #{no[b]} {nm(b)}")
        elif a or b:
            out.append(f"#{no[a or b]} {nm(a or b)} gets a bye")
    return out


async def publish_testdraw_site(guild: discord.Guild, s: dict, ev: dict, players: dict, rng: random.Random) -> str:
    """Put a practice draw on <site>/testdraw/ so staff can see what the real website will look like.
    players = team id -> [player names] (first = captain, second = co-captain)."""
    if not (GITHUB_TOKEN and GITHUB_REPO):
        return "Website preview skipped: GITHUB_TOKEN and GITHUB_REPO aren't set on the bot."
    if not SITE_TEMPLATE.exists():
        return "Website preview skipped: pbl_site.html is missing next to pbl_bot.py."
    name = lambda t: "BYE" if t is None else s["teams"].get(str(t), {}).get("name", "TBD")

    def logo(t):
        f = s["teams"][str(t)].get("logo")
        if f:  # real team: its logo is already on the main site
            return f"../logos/{f}"
        return "data:image/svg+xml;base64," + base64.b64encode(fake_logo_svg(name(t), rng).encode()).decode()
    ids = [int(k) for k in s["teams"]]
    logos = {t: logo(t) for t in ids}
    positions = ["PG", "SG", "SF", "PF", "C", "SF"]
    teams = [{"name": name(t), "logo": logos[t], "captain": players[t][0], "players": players[t][1:],
              "points": s["teams"][str(t)].get("points", 0), "qualified": False, "registered": True} for t in ids]
    rosters = {name(t): {"logo": logos[t], "points": s["teams"][str(t)].get("points", 0), "complete": True,
                         "qualified": False,
                         "players": [{"name": pl, "pos": positions[i % 6], "cap": i == 0, "co": i == 1}
                                     for i, pl in enumerate(players[t])]} for t in ids}
    totals = list(player_totals(ev, str, name).values())
    tname = "TEST · " + (s.get("tourney") or {}).get("name", "Practice draw")
    data = {"league": LEAGUE_NAME + " (TEST DRAW)", "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "teams": teams, "rosters": rosters,
            "circuit": {"needed": None, "standings": sorted(({"team": t["name"], "points": t["points"],
                                                              "qualified": False} for t in teams),
                                                            key=lambda r: -r["points"])},
            "tourney": {"name": tname, "kind": "event", "open": False, "points": None,
                        "entrants": [t["name"] for t in teams]},
            "stats": {"tournament_name": tname, "tournament": totals, "year_label": "test", "year": totals}}
    data.update(event_site_data(ev, name))
    js = "window.PBL_DATA = " + json.dumps(data) + ";\n"
    try:
        async with aiohttp.ClientSession() as session:
            await put_if_changed(session, "testdraw/index.html", SITE_TEMPLATE.read_bytes(), "Update test draw page")
            await github_put(session, "testdraw/data.js", js.encode("utf-8"), "Test draw data")
        return f"{site_url()}testdraw/"
    except Exception as e:
        return f"Website preview failed: {e}"



async def advance_choices(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[int]]:
    """/startgroups and /testdraw: once a group size is picked, offer 1 up to (group size - 1)."""
    size = getattr(interaction.namespace, "group_size", None) or 4
    try:
        size = max(GROUP_SIZE_MIN, min(GROUP_SIZE_MAX, int(size)))
    except (TypeError, ValueError):
        size = 4
    return [app_commands.Choice(name=f"Top {k} of {size} in each group", value=k)
            for k in range(1, size) if not current or str(k).startswith(current.strip())]


@bot.tree.command(description="Staff: practice a draw, play it to the main bracket, and preview the website.")
@app_commands.describe(kind="Which draw to practice", teams="How many fake teams, 2 to 68 (default 10)",
                       real_teams="Use your real league teams and their RISER POINTS instead of fake ones",
                       group_size="Group stage only: teams per group, 3-8 (default 4)",
                       advance="Group stage only: teams from each group that go through (default 2)",
                       play_through="Play the qualifier with random results, then draw the main bracket (default yes)",
                       website="Also put it on <site>/testdraw/ to preview the website (default yes)",
                       channels="Post in the real channels like a real tournament, marked TEST (default yes)",
                       scorecards="Post a TEST Final Score card in #score-reports for every game (default yes)",
                       live="Games get times and finish one by one; you confirm your team's times in DMs (default yes)",
                       consolation="After the qualifier, also draw the consolation bracket for knocked-out teams",
                       draw_in="Practice the countdown: minutes before the draw starts (default 0)")
@app_commands.autocomplete(advance=advance_choices)
@app_commands.choices(kind=[app_commands.Choice(name="Swiss round 1", value="swiss"),
                            app_commands.Choice(name="Group stage", value="groups"),
                            app_commands.Choice(name="Main draw (no qualifier)", value="main")])
@app_commands.default_permissions(manage_roles=True)
async def testdraw(interaction: discord.Interaction, kind: str = "groups",
                   teams: app_commands.Range[int, 2, 68] = 10, real_teams: bool = False,
                   group_size: app_commands.Range[int, 3, 8] = 4, advance: app_commands.Range[int, 1, 7] = 2,
                   play_through: bool = True, website: bool = True, channels: bool = True,
                   scorecards: bool = True, live: bool = True, consolation: bool = False,
                   draw_in: app_commands.Range[int, 0, 10] = 0):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can run a test draw.", ephemeral=True)
    guild = interaction.guild
    real = guild_signups(load_data(), interaction.guild.id)
    rng = random.Random()
    if real_teams:
        keys = [k for k, _t in team_list(real)][:teams]
        if len(keys) < 2:
            return await interaction.response.send_message("You need at least 2 teams for that.", ephemeral=True)
        fake_teams = {k: dict(real["teams"][k]) for k in keys}
    else:
        names = set()
        while len(names) < teams:
            names.add(f"{rng.choice(FAKE_FIRST)} {rng.choice(FAKE_SECOND)}")
        fake_teams = {str(990000 + i): {"name": n, "points": rng.choice([0, 0, 5, 15, 25, 40, 50, 75, 100, 150, 225]),
                                        "roster": {}, "captain": 0} for i, n in enumerate(sorted(names))}
    tz = dict(real.get("tourney") or {"name": "Practice draw"})
    s = {"teams": fake_teams, "tourney": {"name": tz.get("name", "Practice draw"), "logo": tz.get("logo")}}
    ids = [int(k) for k in fake_teams]
    if kind == "groups":
        test_prot = protected_count(s, len(ids), group_plan(len(ids), group_size)[0])
    else:
        test_prot = protected_count(s, len(ids))
    seeds, pts = draw_seeds(s, ids, test_prot)
    nm = lambda t: f"**{fake_teams[str(t)]['name']}**"
    no = {t: i for i, t in enumerate(seeds, 1)}
    if kind == "swiss":
        ev = new_event("swiss")
        ev["swiss"] = swiss_new(ids, 3, 3)
        ev["seeds"] = seeds
        swiss_next_round(ev)
        show = [f"**M{m['id']}** #{no[m['a']]} {nm(m['a'])} vs #{no[m['b']]} {nm(m['b'])}" for m in ev["swiss"]["matches"]]
        show += [f"#{no[int(t)]} {nm(int(t))} gets a bye" for t, r in ev["swiss"]["rec"].items() if r["bye"]]
        note = "Round 1: the top half of the seeds plays the bottom half."
    elif kind == "groups":
        problem = group_advance_problem(len(ids), group_size, advance)
        if problem:
            return await interaction.response.send_message(problem, ephemeral=True)
        ev = new_event("groups")
        count = group_plan(len(ids), group_size)[0]
        drawn, log = seeded_groups(list(seeds), count)
        ev["groups"] = groups_new(ev, ids, advance, drawn)
        show = [f"Pot {pot} · #{no[t]} {nm(t)} → **Group {group_letter(gi)}**" for t, gi, pot in log]
        big, small = max(map(len, drawn)), min(map(len, drawn))
        note = (f"Groups of {big if big == small else f'{big} and {small}'} · **top {advance}** in each group go through. "
                f"Pot 1 is the top {count} seeds (one per group), pot 2 the next {count}, and so on.")
    else:
        ev = new_event("main")
        ev["main"] = de_build(ev, seeds)
        de_resolve(ev["main"])
        show = main_r1_lines(ev, no, nm)
        note = f"{len(ids)} teams, no qualifier."
    ev["seeds"] = seeds

    # players for box scores and the website preview: real names for real teams, made-up ones otherwise
    made_up = iter(fake_league(len(ids), rng)[1].values())
    players = {}
    for t in ids:
        tm = fake_teams[str(t)]
        real_names = []
        for u in sorted(tm.get("roster") or {}, key=lambda u: int(u) != tm.get("captain")):
            mem = guild.get_member(int(u))
            real_names.append(mem.display_name if mem else f"Player {str(u)[-4:]}")
        filler = next(made_up)
        players[t] = real_names or filler
    ch = interaction.channel  # where staff ran the command: progress notes + the website link
    live_on = live and channels and play_through and kind in ("groups", "swiss")
    tname = "TEST · " + s["tourney"]["name"]
    show_ch = (chan(guild, "bracket") or ch) if channels else ch
    reporter = interaction.user.id

    def dest(where: str | None):
        """The real channel a tournament would use (when channels is on), otherwise the command's channel."""
        return (chan(guild, where) or ch) if (channels and where) else ch

    async def say(text: str | None = None, pic: bytes | None = None, fname: str = "draw.png",
                  title: str | None = None, where: str | None = None, color: int = INFO):
        kw = {}
        if text:
            kw["embed"] = brand_embed(text, title or tname, color)
        if pic:
            kw["file"] = discord.File(io.BytesIO(pic), filename=fname)
        msg = await dest(where).send(**kw, allowed_mentions=NO_PINGS)
        remember_test_msg(guild, msg)
        return msg

    async def blocks(where: str, parts: list[str], color: int = 0xEF4444):
        """Like send_blocks (the real tournament posts), but tracked so /cleartest what:draw can remove them."""
        for chunk in pack(parts, limit=3800):
            await say(chunk, where=where, color=color, title=None)

    async def card(m):
        if not (channels and scorecards):
            return
        e = score_card({"tourney": {"name": tname}}, ev, m, reporter)
        e.title = "TEST · " + (e.title or "").replace(f" · {tname}", "")
        e.url = f"{site_url()}testdraw/#m{m['id']}" if (website and site_url()) else None
        msg = await dest("score-reports").send(embed=e, allowed_mentions=NO_PINGS)
        remember_test_msg(guild, msg)

    def play(m):
        w = rng.choice([m["a"], m["b"]])
        lo = m["b"] if w == m["a"] else m["a"]
        hi = rng.randint(38, 66)
        pts_ = [hi, hi - rng.randint(1, 15)]
        m["winner"], m["score"] = w, f"{pts_[0]}-{pts_[1]}"
        m["box"] = {**fake_box(w, players[w], pts_[0], pts_[0] - pts_[1], rng),
                    **fake_box(lo, players[lo], pts_[1], pts_[1] - pts_[0], rng)}
        return w, lo, pts_

    def result_line(m, extra=""):
        lo = m["b"] if m["winner"] == m["a"] else m["a"]
        return f"**M{m['id']} result**: {tag(m['winner'])} beat {tag(lo)} {m['score']}{extra}"

    async def stage_posts():
        """What the real /startgroups, /startswiss or /startmain posts besides the live draw."""
        if kind == "groups":
            gs = ev["groups"]
            sizes = sorted({len(g) for g in gs["groups"]}, reverse=True)
            await blocks("standings", [
                f"# TEST · Group stage draw\n{len(ids)} teams drawn by RISER POINTS pots into {len(gs['groups'])} "
                f"group(s) of {' and '.join(map(str, sizes))}. Everyone plays everyone in their group once. "
                f"**Top {gs['advance']}** in each group go to the double-elimination main draw.\n"
                "Tiebreakers: wins, then head-to-head, then point difference."]
                + [group_blocks(gs, gi) for gi in range(len(gs["groups"]))])
            gs_msg[0] = await say(pic=await asyncio.to_thread(group_standings_picture, s, ev),
                                  fname="standings.png", where="standings")
            rounds = max(m["round"] for m in gs["matches"])
            sched = [f"# TEST · Group stage schedule\n{rounds} rounds. Captains: agree a time in #scheduling, play, "
                     "then report the score with /game_score; the other captain confirms it."]
            for r in range(1, rounds + 1):
                sched.append(f"## Round {r}\n" + "\n".join(
                    f"**M{m['id']}** Group {group_letter(m['group'])}: {tag(m['a'])} vs {tag(m['b'])}"
                    for m in gs["matches"] if m["round"] == r))
            await blocks("schedule", sched)
            await say("**The group stage draw is out!** Groups are in #standings, matchups in #schedule.\n"
                      "*Practice run: nothing here is real.*", where="announcements", color=GOLD)
        elif kind == "swiss":
            sw = ev["swiss"]
            r1 = [f"**M{m['id']}**: #{no[m['a']]} {tag(m['a'])} vs #{no[m['b']]} {tag(m['b'])}"
                  for m in sw["matches"] if m["round"] == 1]
            r1 += [f"{tag(int(t))} gets a bye as the #1 seed (counts as a win)" for t, r in sw["rec"].items() if r["bye"]]
            await blocks("schedule", [f"# TEST · Swiss qualifier\n{len(ids)} teams. **{sw['wins']} wins** = into the "
                                      f"main draw. **{sw['losses']} losses** = out.", "## Swiss round 1\n" + "\n".join(r1)])
            t = swiss_table(sw)
            await blocks("standings", ["# TEST · " + t[0].lstrip("# ")] + t[1:])
            await say("**The Swiss qualifier has started!** Round 1 matchups are in #schedule.\n"
                      "*Practice run: nothing here is real.*", where="announcements", color=GOLD)
        else:
            await main_posts(seeds, f"{len(seeds)} teams, no qualifier, seeded by RISER POINTS.")

    async def main_posts(mseeds, mnote):
        """What /startmain posts in #bracket (plus an announcement)."""
        parts = [f"# TEST · Main draw: double elimination\n{mnote}\nLose twice and you're out. "
                 "The Grand Final has a reset if the Losers bracket team wins the first game.",
                 "**Seeds**\n" + "\n".join(f"#{i}: {tag(t)}" for i, t in enumerate(mseeds, 1))]
        parts += de_overview(ev["main"])
        nxt = up_next(ev["main"])
        if nxt:
            parts.append("# Play now\n" + "\n".join(nxt))
        await blocks("bracket", parts)
        await say("**The main draw is set!** Check #bracket for the bracket and the first matches.\n"
                  "*Practice run: nothing here is real.*", where="announcements", color=GOLD)

    gs_msg = [None]

    async def update_gs_picture():
        pic = await asyncio.to_thread(group_standings_picture, s, ev)
        if gs_msg[0] is not None:
            try:
                await gs_msg[0].edit(attachments=[discord.File(io.BytesIO(pic), filename="standings.png")])
                return
            except discord.HTTPException:
                pass
        gs_msg[0] = await say(pic=pic, fname="standings.png", where="standings")

    tester = interaction.user
    my_team = seeds[0]  # the staff member running the test plays captain of the #1 seed
    tsc = sched(s)      # a scheduling book just for this test (nothing touches the real one)
    tz_code = sched(real)["tz"].get(str(tester.id), "ET")

    async def dm_tester(embed: discord.Embed, view=None):
        embed.set_footer(text="🧪 TEST · /testdraw · nothing here is real")
        try:
            msg = await tester.send(embed=embed, view=view) if view else await tester.send(embed=embed)
            remember_test_msg(guild, msg)
            return msg
        except discord.HTTPException:
            return None

    def pace_for(n_matches: int) -> float:
        """Seconds between events so a whole qualifier takes a few minutes, not hours."""
        return max(1.0, min(6.0, 200 / max(1, n_matches * 3)))

    async def set_time(m, when: datetime, by: str):
        mid = str(m["id"])
        e_ = tsc["matches"][mid]
        e_["time"] = when.isoformat(timespec="seconds")
        await say(f"**{name_of(m['a'])}** vs **{name_of(m['b'])}**\n**Game time:** {ts(when)} ({ts(when, 'R')})\n"
                  f"Set by {by}.", title=f"✅ TEST · M{mid} is scheduled", where="scheduling", color=GOOD)
        key = f"t{mid}"
        _test_cards[key] = {"e": e_, "a": f"**{name_of(m['a'])}**", "b": f"**{name_of(m['b'])}**", "tname": tname}
        emb = game_card(e_, mid, f"**{name_of(m['a'])}**", f"**{name_of(m['b'])}**", tname)
        cmsg = await dest("schedule").send(embed=emb, view=game_card_view(guild.id, key), allowed_mentions=NO_PINGS)
        e_["card"] = [cmsg.channel.id, cmsg.id]
        remember_test_msg(guild, cmsg)

    async def tester_pick(m) -> datetime:
        """The other captain sends times; you confirm one in DMs (or suggest your own), like a real match."""
        mid = str(m["id"])
        opp = m["b"] if m["a"] == my_team else m["a"]
        now = datetime.now(timezone.utc)
        hours = sorted(rng.sample(range(2, 47), 3))
        base = now.replace(minute=0, second=0, microsecond=0)
        offered = [int((base + timedelta(hours=h)).timestamp()) for h in hours]
        listing = "\n".join(f"• {ts(datetime.fromtimestamp(t, timezone.utc))}" for t in offered)
        fut = asyncio.get_running_loop().create_future()
        counter = (slot_options(now, now + timedelta(hours=24), tz_code, offered) or [[]])[0]
        e = brand_embed(f"**{name_of(opp)}** want to play **M{mid}** ({tsc['matches'][mid]['label']}) at one of these "
                        f"times (shown in your local time):\n{listing}\n\nPick one below to lock it in. If none work, "
                        f"suggest another time from the other dropdown.\n"
                        f"Deadline: {ts(datetime.fromisoformat(tsc['matches'][mid]['deadline']))}\n\n"
                        "*Test: you have 2 minutes, then the bot sets the preset time like it would when the deadline passes.*",
                        f"🧪 TEST · Confirm your game time · {guild.name}", GOLD)
        if not await dm_tester(e, TestTimeView(fut, offered, counter, tz_code)):
            await say(f"I couldn't DM {tester.mention} (DMs closed?), so M{mid} gets a time automatically.")
            return datetime.fromtimestamp(offered[0], timezone.utc)
        try:
            kind_, t = await asyncio.wait_for(fut, timeout=120)
        except asyncio.TimeoutError:
            when = evening_slot(tsc, now)
            await say(f"No game time agreed for M{mid} in time, so the bot set the preset: {ts(when)}.\n"
                      "*(In a real match this happens when the deadline passes.)*", title=f"⏳ TEST · M{mid} preset time",
                      where="scheduling", color=MUTED)
            await dm_tester(brand_embed(f"No time was picked for **M{mid}**, so the bot set it for {ts(when)}. "
                                        f"Both captains can still move it with `/gametime match:{mid}`.",
                                        "⏳ Preset game time", MUTED))
            return when
        when = datetime.fromtimestamp(t, timezone.utc)
        if kind_ == "take":
            await dm_tester(brand_embed(f"✅ Locked in: {ts(when)}. Both teams have been told.", "Game time confirmed",
                                        GOOD))
            return when
        await asyncio.sleep(4)
        await dm_tester(brand_embed(f"**{name_of(opp)}** accepted your time for **M{mid}**: {ts(when)}.",
                                    "✅ Your time was accepted", GOOD))
        return when

    async def live_round(ms: list, label_of, on_result):
        """One round, like real life: matches open, captains set times one by one, then games finish at
        different times (in game-time order). Every step is its own message in its own channel."""
        if not ms:
            return
        d = pace_for(qual_matches)
        now = datetime.now(timezone.utc)
        for m in ms:
            mid = str(m["id"])
            tsc["matches"][mid] = {"a": m["a"], "b": m["b"], "label": label_of(m), "opened": now.isoformat(timespec="seconds"),
                                   "deadline": (now + timedelta(hours=AGREE_HOURS)).isoformat(timespec="seconds"),
                                   "time": None, "preset": False, "reminded": [], "done": False}
            await say(f"**M{mid}** · {label_of(m)}\n**{name_of(m['a'])}** vs **{name_of(m['b'])}**\n\n"
                      f"Captains, you have **48 hours** to agree a game time with `/gametime match:{mid}`. "
                      "The other captain confirms in DMs.", title=f"📅 TEST · Schedule your match · M{mid}",
                      where="scheduling")
            if my_team in (m["a"], m["b"]):
                await dm_tester(next_match_card(s, mid, my_team))
            await asyncio.sleep(d / 3)
        mine = [m for m in ms if my_team in (m["a"], m["b"])]
        pick = asyncio.create_task(tester_pick(mine[0])) if mine else None
        times = {}
        base = now.replace(minute=0, second=0, microsecond=0)
        for m in ms:
            if m in mine:
                continue
            when = base + timedelta(hours=rng.randint(2, 47))
            times[m["id"]] = when
            await asyncio.sleep(d)
            await set_time(m, when, "both captains")
        if pick:
            when = await pick
            times[mine[0]["id"]] = when
            await set_time(mine[0], when, f"{tester.mention} and the other captain")
            await dm_tester(next_match_card(s, str(mine[0]["id"]), my_team))
            mid0 = str(mine[0]["id"])
            other0 = mine[0]["b"] if mine[0]["a"] == my_team else mine[0]["a"]
            await dm_tester(game_rules_embed(
                f"🧪 TEST · Game confirmed · M{mid0}",
                f"### {stage_heading(tsc['matches'][mid0]['label'], mid0)}\n**{name_of(my_team)}** vs "
                f"**{name_of(other0)}** · {ts(when)} ({ts(when, 'R')})\nYou're a captain, so you're getting the game "
                "settings and how to report the score. (Co-captains get this too.)"))
        for m in sorted(ms, key=lambda x: times[x["id"]]):  # games end in the order they were played
            await asyncio.sleep(d)
            if m in mine:
                await dm_tester(brand_embed(f"⏰ **M{m['id']}** is starting now: **{name_of(m['a'])}** vs "
                                            f"**{name_of(m['b'])}**. Get your team in the voice channel.\n"
                                            "*(Test: skipped ahead to game time.)*", "⏰ Game time", GOLD))
            w, lo, pts_ = play(m)
            tsc["matches"][str(m["id"])]["done"] = True
            await report(m, w, lo)
            await on_result(m, w, lo, pts_)

    async def report(m, w, lo):
        """Where a score report goes: the winning captain posts it in #score-reports, then the bot records it
        (/result) and posts the Final Score card there too, and the result line in #schedule."""
        cap = players.get(w, ["Captain"])[0]
        await say(f"**{name_of(w)}** {m['score'].split('-')[0]} - {m['score'].split('-')[1]} **{name_of(lo)}**\n"
                  f"Reported by **{cap}** (captain of {name_of(w)}) with the scoreboard screenshot / game export.",
                  title=f"📝 TEST · Score report · M{m['id']}", where="score-reports", color=MUTED)
        await say(result_line(m), title=None, where="schedule", color=GOOD)
        await card(m)

    def name_of(t) -> str:
        return fake_teams.get(str(t), {}).get("name", "TBD")

    qual_matches = (len(ev["groups"]["matches"]) if kind == "groups" else
                    max(1, len(ids) // 2) * (ev["swiss"]["wins"] + ev["swiss"]["losses"] - 1) if kind == "swiss" else 1)

    async def after():
        """After the draw: the stage posts, then play the qualifier with random results, draw the main bracket,
        and preview the website. Team names are shown in bold instead of role pings while this runs."""
        added = {t: fake_teams[str(t)]["name"] for t in ids if t not in TEST_NAMES}
        TEST_NAMES.update(added)
        try:
            if channels:
                await stage_posts()
            if play_through and kind in ("groups", "swiss"):
                await asyncio.sleep(3)
                if live_on:
                    await say(f"🎮 **Live test:** {tester.mention}, you're playing captain of **{name_of(my_team)}** "
                              "(the #1 seed). Watch your DMs: you'll get your match cards and a request to confirm "
                              "a game time each round. Other matches get their times and finish one by one.",
                              title=f"{tname} · live mode")
                if kind == "groups":
                    gs = ev["groups"]
                    if not live_on:
                        await say(f"▶️ Playing all **{len(gs['matches'])}** group games with random results...",
                                  title=f"{tname} · group stage")
                    rounds = max(m["round"] for m in gs["matches"])
                    for r in range(1, rounds + 1):
                        if live_on:
                            async def g_done(m, w, lo, pts_):
                                m["pts"] = pts_
                                await blocks("standings", [group_blocks(gs, m["group"])])
                                await update_gs_picture()
                            await live_round([x for x in gs["matches"] if x["round"] == r],
                                             lambda m, r=r: f"Group {group_letter(m['group'])} · round {r}", g_done)
                            continue
                        res = []
                        for m in [x for x in gs["matches"] if x["round"] == r]:
                            _w, _lo, m["pts"] = play(m)
                            res.append(result_line(m, f" (Group {group_letter(m['group'])})"))
                            await card(m)
                        if channels:
                            await blocks("schedule", [f"## TEST · Group stage round {r} results"] + res, GOOD)
                            await update_gs_picture()
                        await asyncio.sleep(1)
                    for gi in range(len(gs["groups"])):
                        order, _st = group_table(gs, gi)
                        gs["qualified"] += order[:gs["advance"]]
                    ev["stage"] = "groups_done"
                    main_seeds = groups_seeds(gs)
                    if channels:
                        await update_gs_picture()
                        await blocks("standings", ["# TEST · Final group standings"]
                                     + [group_blocks(gs, gi) for gi in range(len(gs["groups"]))])
                        await blocks("schedule", [f"# Group stage complete\n**Into the main draw ({len(gs['qualified'])}):** "
                                                  + ", ".join(tag(t) for t in gs["qualified"])], GOOD)
                    else:
                        await say(pic=await asyncio.to_thread(group_standings_picture, s, ev), fname="groups.png")
                    how = (f"the top {gs['advance']} from each group. Group winners are seeded first, and teams from "
                           "the same group avoid each other in round 1 where possible")
                    mnote = (f"{len(main_seeds)} teams qualified from the group stage. Group winners are seeded first, "
                             "and teams from the same group don't meet in round 1 where possible.")
                else:
                    sw = ev["swiss"]
                    await say(f"▶️ Playing the Swiss stage with random results: **{sw['wins']} wins** qualifies, "
                              f"**{sw['losses']} losses** is out.", title=f"{tname} · Swiss stage")
                    while True:
                        res = []
                        if live_on:
                            async def s_done(m, w, lo, pts_):
                                swiss_record(sw, w, lo)
                            await live_round([x for x in sw["matches"] if not x["winner"]],
                                             lambda m: f"Swiss round {m['round']}", s_done)
                        for m in sw["matches"]:
                            if not m["winner"]:
                                w, lo, _p = play(m)
                                swiss_record(sw, w, lo)
                                res.append(result_line(m))
                                await card(m)
                        await asyncio.sleep(1)
                        done_round = sw["round"]
                        pic = await asyncio.to_thread(swiss_round_picture, s, ev)
                        if channels:
                            t = swiss_table(sw)
                            await blocks("standings", ["# TEST · " + t[0].lstrip("# ")] + t[1:])
                        parts = ([f"## TEST · Swiss round {done_round} results"] + res) if res else \
                            [f"## TEST · Swiss round {done_round} complete"]
                        more = bool(swiss_active(sw))
                        if more:
                            parts.append("\n".join(swiss_next_round(ev)))
                        else:
                            parts.append(f"# Swiss stage complete\n**Into the main draw ({len(sw['qualified'])}):** "
                                         + ", ".join(tag(q) for q in sw["qualified"]))
                        if channels:
                            await blocks("schedule", parts, GOOD)
                        await say(pic=pic, fname=f"swiss_r{done_round}.png", where="schedule")
                        if not more:
                            break
                    ev["stage"] = "swiss_done"
                    main_seeds = list(sw["qualified"])
                    how = f"everyone who reached {sw['wins']} wins, seeded by how fast they got there"
                    mnote = f"{len(main_seeds)} teams qualified from the Swiss stage, seeded by record."
                if len(main_seeds) < 2:
                    await say(f"Only {len(main_seeds)} team qualified, so there's no main draw to make.")
                else:
                    await say(f"✅ **{len(main_seeds)} teams** made the main draw: {how}.\n"
                              "Drawing the double-elimination bracket next...",
                              title=f"{tname} · qualifier finished", where="bracket")
                    await asyncio.sleep(4)
                    ev["main"] = de_build(ev, main_seeds)
                    de_resolve(ev["main"])
                    ev["stage"] = "main"
                    no2 = {t: i for i, t in enumerate(main_seeds, 1)}
                    await draw_show(guild, "main", main_seeds, pts, main_r1_lines(ev, no2, nm),
                                    "🧪 **PRACTICE DRAW** · nothing here is real.\n"
                                    f"{len(main_seeds)} teams from the {'group stage' if kind == 'groups' else 'Swiss stage'}.",
                                    by_points=False, test=test)
                    if channels:
                        await main_posts(main_seeds, mnote)
                if consolation:
                    out_ = qualifier_knockouts(ev)
                    if len(out_) >= 2:
                        ev["consolation"] = cons_build(ev, out_)
                        await blocks("bracket", ["# TEST · " + cons_parts(ev["consolation"])[0].lstrip("# ")]
                                     + cons_parts(ev["consolation"])[1:])
            if website:
                link = await publish_testdraw_site(guild, s, ev, players, rng)
                if link.startswith("http"):
                    await say(f"🌐 **Website preview:** {link}\nThis is exactly how the site will look for this draw: "
                              "open the **Draw** tab and click any team for its roster. Give GitHub a minute to update.",
                              title=f"{tname} · website preview")
                else:
                    await say(link, title=f"{tname} · website preview")
        finally:
            for t in added:
                TEST_NAMES.pop(t, None)

    extra_txt = (" It then plays the qualifier with random results and draws the main bracket."
                 if play_through and kind != "main" else "")
    extra_txt += " A website preview link comes at the end." if website else ""
    where_txt = ("in the real channels (#bracket, #standings, #schedule, #score-reports, #announcements), "
                 "every post marked TEST" if channels else "in this channel")
    await interaction.response.send_message(
        f"Running a **test {kind} draw** with {len(ids)} {'real' if real_teams else 'fake'} teams {where_txt}."
        f"{extra_txt} Nothing is saved and nobody is pinged. Clean up with /cleartest what:draw.",
        ephemeral=True)
    note = "🧪 **PRACTICE DRAW** · nothing here is real.\n" + note
    test = {"s": s, "ev": ev, "channel": show_ch, "after": after, "announce": channels}
    ev["protected"] = test_prot
    start_show(guild, kind, seeds, pts, show, note, test=test, countdown=draw_in * 60, protected=test_prot)


def _is_test_draw_msg(m) -> bool:
    """Old practice draws (from before message tracking): the live card says TEST / PRACTICE DRAW."""
    for e in getattr(m, "embeds", []) or []:
        if "TEST ·" in (e.title or "") or "PRACTICE DRAW" in (e.description or ""):
            return True
    return False


@app_commands.describe(everything="True = delete every test draw, not just the most recent one")
@app_commands.default_permissions(manage_roles=True)
async def deletetestdraw(interaction: discord.Interaction, everything: bool = False):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    for task in list(_test_tasks.get(guild.id, set())):  # stop a draw that's still running
        task.cancel()
    data = load_data()
    s = guild_signups(data, guild.id)
    runs = [r for r in s.get("test_draws", []) if r]
    targets = [m for r in runs for m in r] if everything else (runs[-1] if runs else [])
    deleted = 0
    for ch_id, msg_id in targets:
        ch = guild.get_channel(ch_id) or bot.get_channel(ch_id)  # bot.get_channel finds test DMs too
        if ch is None:
            try:
                ch = await bot.fetch_channel(ch_id)
            except discord.HTTPException:
                continue
        try:
            await ch.get_partial_message(msg_id).delete()
            deleted += 1
        except discord.HTTPException:
            pass  # already gone
    s["test_draws"] = [] if everything else ([r for r in s.get("test_draws", []) if r][:-1])
    save_data(data)
    swept = 0
    if not targets or everything:  # also clean up older test draws in this channel that weren't tracked
        last_test = False
        try:
            async for m in interaction.channel.history(limit=300):
                if m.author.id != bot.user.id:
                    last_test = False
                    continue
                pic = any(a.filename == "draw.png" for a in m.attachments)
                if _is_test_draw_msg(m):
                    await m.delete()
                    swept += 1
                    last_test = False
                elif pic and not last_test:
                    # history runs newest first, so a picture comes before its card. Only delete it if
                    # the very next (older) bot message is a test card.
                    older = [x async for x in interaction.channel.history(limit=1, before=m)]
                    if older and older[0].author.id == bot.user.id and _is_test_draw_msg(older[0]):
                        await m.delete()
                        swept += 1
        except discord.HTTPException:
            pass
    total = deleted + swept
    if total == 0:
        return await interaction.followup.send("No test draws to delete. (Older ones only get found in the "
                                               "channel you run this in.)", ephemeral=True)
    await interaction.followup.send(f"🧹 Deleted {total} test draw message(s)"
                                    + (" (every test draw)." if everything else "."), ephemeral=True)


# Test draws: every message they post is remembered (in signups.json) so /cleartest what:draw can remove them.
_test_tasks: dict[int, set] = {}  # guild id -> running test-draw shows
_show_tasks: dict[int, dict] = {}  # guild id -> the real live draw running now: {task, started, skip}


def remember_test_msg(guild: discord.Guild, msg) -> None:
    if msg is None or not hasattr(msg, "id"):
        return
    data = load_data()
    s = guild_signups(data, guild.id)
    runs = s.setdefault("test_draws", [])
    if not runs:
        runs.append([])
    runs[-1].append([msg.channel.id, msg.id])
    save_data(data)


def finish_drawing(guild: discord.Guild):
    """The live draw is over: let the schedule, DMs and website show it."""
    data = load_data()
    ev = guild_signups(data, guild.id).get("event")
    if ev and ev.get("drawing"):
        ev["drawing"] = False
        ev.pop("draw_at", None)
        save_data(data)
    schedule_publish(guild)


def start_show(guild, kind, seeds, pts, extra, note, by_points: bool = True, test: dict | None = None,
               after=None, countdown: int = 0, protected: int | None = None):
    """Run the live draw in the background. For a real tournament the event is marked "drawing" until the show
    ends (no match DMs, no schedule, the website keeps it secret), then `after()` posts standings/schedule."""
    if test:  # a new practice draw = a new group of messages to delete later
        data = load_data()
        guild_signups(data, guild.id).setdefault("test_draws", []).append([])
        save_data(data)

    async def run():
        try:
            await draw_show(guild, kind, seeds, pts, extra, note, by_points, test, countdown=countdown,
                            protected=protected)
        except asyncio.CancelledError:
            if test or not (_show_tasks.get(guild.id) or {}).get("skip"):
                if not test:
                    finish_drawing(guild)
                return
            # /stopdraw action:skip: end the show now and post the results straight away (below)
        except Exception as e:
            print(f"[draw show] {e}")
        try:
            if not test:
                finish_drawing(guild)
            if after:
                await after()
            if not test:
                try:  # round 1 is playable now: DM the captains their first opponent right away
                    await match_watch_once(guild)
                except Exception as e:
                    print(f"[first match DMs] {e}")
            if test and test.get("after"):
                await test["after"]()
        except asyncio.CancelledError:
            pass
        except Exception as e:
            print(f"[after draw] {e}")
    task = asyncio.create_task(run())
    if test:
        _test_tasks.setdefault(guild.id, set()).add(task)
        task.add_done_callback(lambda t: _test_tasks.get(guild.id, set()).discard(t))
    else:
        _show_tasks[guild.id] = {"task": task, "started": datetime.now(timezone.utc), "skip": False}
        task.add_done_callback(lambda t: _show_tasks.pop(guild.id, None)
                               if (_show_tasks.get(guild.id) or {}).get("task") is t else None)


@bot.tree.command(description="Staff: stop the live draw: skip to the results, or cancel it and start over.")
@app_commands.describe(action="Skip = end the show now and post the final draw. Cancel = throw this draw away.",
                       clear_posts="Cancel only: delete the draw's posts in #bracket (default yes)")
@app_commands.choices(action=[app_commands.Choice(name="Skip to the results (keep this draw)", value="skip"),
                              app_commands.Choice(name="Cancel the draw (start over after)", value="cancel")])
@app_commands.default_permissions(manage_roles=True)
async def stopdraw(interaction: discord.Interaction, action: str, clear_posts: bool = True):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can stop a draw.", ephemeral=True)
    info = _show_tasks.get(guild.id)
    data = load_data()
    s = guild_signups(data, guild.id)
    ev = s.get("event") or {}
    running = info and not info["task"].done()
    if not running and not ev.get("drawing"):
        return await interaction.response.send_message("There's no live draw running right now.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    if action == "skip":
        if running:
            info["skip"] = True
            info["task"].cancel()
            try:
                await asyncio.wait_for(asyncio.shield(info["task"]), timeout=60)
            except Exception:
                pass
            return await interaction.followup.send("Draw skipped. The final draw, the schedule and the first-opponent "
                                                   "DMs are going out now.", ephemeral=True)
        finish_drawing(guild)  # the bot restarted mid-show: just reveal it
        return await interaction.followup.send("The draw is now public (the show had already stopped). Check what's "
                                               "ready to play with /matches.", ephemeral=True)
    # cancel: stop the show and throw the draw away, entries stay as they are
    started = info["started"] if info else None
    if running:
        info["task"].cancel()
        try:
            await asyncio.wait_for(asyncio.shield(info["task"]), timeout=10)
        except Exception:
            pass
    data = load_data()
    s = guild_signups(data, guild.id)
    s["event"] = None
    save_data(data)
    removed = 0
    ch = chan(guild, "bracket")
    if ch and clear_posts and started:
        try:
            async for msg in ch.history(limit=200, after=started - timedelta(seconds=5)):
                if msg.author.id == guild.me.id:
                    try:
                        await msg.delete()
                        removed += 1
                        await asyncio.sleep(0.4)
                    except discord.HTTPException:
                        pass
        except discord.HTTPException:
            pass
    if ch:
        await post(ch, "The live draw was stopped by staff. It will be redone shortly.", title="Draw cancelled",
                   color=MUTED)
    schedule_publish(guild)
    await interaction.followup.send(
        f"Draw cancelled{f' and {removed} post(s) removed from #bracket' if removed else ''}. Entries are unchanged: "
        "start it again with /startgroups, /startswiss or /startmain.", ephemeral=True)

@bot.tree.command(description="Start a Swiss qualifier: win enough to make the main draw, lose enough and you're out.")
@app_commands.describe(wins="Wins needed to qualify (default 3)", losses="Losses that knock a team out (default 3)",
                       redraw="Set to True to throw away a running tournament and start over",
                       consolation="Teams knocked out of the Swiss play a single-elimination consolation bracket",
                       byes="Top teams by RISER POINTS that skip this and go straight to the main draw (13+ teams)",
                       draw_in="Minutes until the live draw starts, so people can tune in (default 5, 0 = now)")
@app_commands.default_permissions(manage_roles=True)
async def startswiss(interaction: discord.Interaction, wins: app_commands.Range[int, 1, 5] = 3,
                     losses: app_commands.Range[int, 1, 5] = 3, redraw: bool = False, consolation: bool = False,
                     draw_in: app_commands.Range[int, 0, 60] = DRAW_COUNTDOWN_MIN,
                     byes: app_commands.Range[int, 0, 16] = 0):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can start a tournament.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    teams = entrant_roles(guild)
    problem = event_problem(s, teams, redraw)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    bye_ids, ids, problem = split_byes(s, [t.id for t in teams], byes)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)

    ev = fresh_event(s, "swiss")
    ev["byes"] = bye_ids  # straight into the main draw
    asyncio.create_task(notify_byes(guild, s, bye_ids, (s.get("tourney") or {}).get("name", "the tournament")))
    ev["cons_on"] = consolation
    ev["swiss"] = swiss_new(ids, wins, losses)
    ev["protected"] = protected_count(s, len(ids))
    ev["seeds"], pts = draw_seeds(s, ids, ev["protected"])
    round_lines = swiss_next_round(ev)
    ev["drawing"] = True  # secret until the live draw ends
    ev["draw_at"] = (datetime.now(timezone.utc) + timedelta(minutes=draw_in)).isoformat(timespec="seconds")
    save_data(data)
    schedule_publish(guild)
    restart = " (RESTARTED: ignore the earlier draw)" if redraw else ""

    async def after():  # posted once the live draw is over, so nothing is spoiled
        d2 = load_data()
        ev2 = guild_signups(d2, guild.id).get("event") or {}
        await send_blocks(chan(guild, "schedule"), [
            f"# Swiss qualifier{restart}\n{len(ids)} teams. **{wins} wins** = into the double-elimination main draw. "
            + byes_note(guild_signups(d2, guild.id), bye_ids).strip() + " "
            f"**{losses} losses** = out. Each round you play a team with the same record.\n"
            "Captains: agree a time in #scheduling, play, then report the score with /game_score; the other "
            "captain confirms it.",
            "\n".join(round_lines)])
        if ev2.get("swiss"):
            await send_blocks(chan(guild, "standings"), swiss_table(ev2["swiss"]))
        ann = chan(guild, "announcements")
        if ann:
            await post(ann, f"**The Swiss qualifier has started!**{restart} Round 1 matchups are in #schedule.")
    start_show(guild, "swiss", ev["seeds"], pts, [],
               ("Round 1: the seeds are kept apart." if ev["protected"] else "Round 1 matchups are fully random.")
               + byes_note(s, bye_ids),
               after=after, countdown=draw_in * 60, protected=ev["protected"])
    await interaction.followup.send(
        f"Swiss stage set. The live draw starts in #bracket {'now' if not draw_in else f'in {draw_in} min'}; "
        "the schedule and standings post when it ends.", ephemeral=True)


@bot.tree.command(description="Start a group stage: pick the group size and how many from each group go through.")
@app_commands.describe(group_size="Teams per group, 3-8 (default 4). Pick this first.",
                       advance="Teams from each group that make the main draw (1 up to group size - 1, default 2)",
                       redraw="Set to True to throw away a running tournament and start over",
                       consolation="Teams knocked out in the groups play a single-elimination consolation bracket",
                       byes="Top teams by RISER POINTS that skip this and go straight to the main draw (13+ teams)",
                       draw_in="Minutes until the live draw starts, so people can tune in (default 5, 0 = now)")
@app_commands.autocomplete(advance=advance_choices)
@app_commands.default_permissions(manage_roles=True)
async def startgroups(interaction: discord.Interaction, group_size: app_commands.Range[int, 3, 8] = 4,
                      advance: app_commands.Range[int, 1, 7] = 2, redraw: bool = False, consolation: bool = False,
                      draw_in: app_commands.Range[int, 0, 60] = DRAW_COUNTDOWN_MIN,
                      byes: app_commands.Range[int, 0, 16] = 0):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can start a tournament.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    teams = entrant_roles(guild)
    problem = event_problem(s, teams, redraw)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    bye_ids, ids, problem = split_byes(s, [t.id for t in teams], byes)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    problem = group_advance_problem(len(ids), group_size, advance)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)

    ev = fresh_event(s, "groups")
    ev["byes"] = bye_ids  # straight into the main draw
    asyncio.create_task(notify_byes(guild, s, bye_ids, (s.get("tourney") or {}).get("name", "the tournament")))
    ev["cons_on"] = consolation
    count = group_plan(len(ids), group_size)[0]
    ev["protected"] = protected_count(s, len(ids), count)  # the top seeds head the groups
    ev["seeds"], pts = draw_seeds(s, ids, ev["protected"])
    drawn, draw_log = seeded_groups(list(ev["seeds"]), count)
    gs = ev["groups"] = groups_new(ev, ids, advance, drawn)
    big, small = max(map(len, gs["groups"])), min(map(len, gs["groups"]))
    sizes_txt = f"{big}" if big == small else f"{big} and {small}"
    ev["drawing"] = True  # secret until the live draw ends
    ev["draw_at"] = (datetime.now(timezone.utc) + timedelta(minutes=draw_in)).isoformat(timespec="seconds")
    save_data(data)
    schedule_publish(guild)
    restart = " (RESTARTED: ignore the earlier draw)" if redraw else ""
    n_teams = len(teams)

    async def after():  # posted once the live draw is over, so nothing is spoiled
        d2 = load_data()
        s2 = guild_signups(d2, guild.id)
        ev2 = s2.get("event") or {}
        gs2 = ev2.get("groups")
        if not gs2:
            return
        await post_picture(guild, "standings", group_standings_picture, s2, ev2, edit_key=(ev2, "gs_pic"))
        save_data(d2)  # remember the standings picture so results edit it
        n_groups = len(gs2["groups"])
        await send_blocks(chan(guild, "standings"), [
            f"# Group stage draw{restart}\n{len(ids)} teams drawn by RISER POINTS pots into {n_groups} group(s) "
            f"of {sizes_txt}. "
            f"Everyone plays everyone in their group once. **Top {advance}** in each group go to the "
            "double-elimination main draw.\nTiebreakers: wins, then head-to-head, then point difference."
            + byes_note(s2, bye_ids)]
            + [group_blocks(gs2, gi) for gi in range(n_groups)])
        await post_group_schedule(guild, s2, ev2, restart)
        ann = chan(guild, "announcements")
        if ann:
            await post(ann, f"**The group stage draw is out!**{restart} Groups are in #standings, "
                           "matchups in #schedule.")
    start_show(guild, "groups", ev["seeds"], pts, [],
               f"Groups of {sizes_txt} · **top {advance}** in each group go through. "
               + ("The seeds head the groups (pot 1)." if ev["protected"] else "") + byes_note(s, bye_ids),
               after=after, countdown=draw_in * 60, protected=ev["protected"])
    await interaction.followup.send(
        f"Group stage set. The live draw starts in #bracket {'now' if not draw_in else f'in {draw_in} min'}; "
        "groups and the schedule post when it ends.", ephemeral=True)


@bot.tree.command(description="Start the double-elimination main draw.")
@app_commands.describe(redraw="Set to True to throw away a running main draw and start over",
                       draw_in="Minutes until the live draw starts, so people can tune in (default 5, 0 = now)")
@app_commands.default_permissions(manage_roles=True)
async def startmain(interaction: discord.Interaction, redraw: bool = False,
                    draw_in: app_commands.Range[int, 0, 60] = DRAW_COUNTDOWN_MIN):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can start a tournament.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    ev = s["event"]

    if ev and ev["stage"] in ("swiss", "groups"):
        stage = "Swiss stage" if ev["stage"] == "swiss" else "group stage"
        return await interaction.response.send_message(
            f"The {stage} is still running. The main draw can start once it's finished.", ephemeral=True)
    if ev and (ev.get("swiss") or ev.get("groups")):
        if ev["stage"] not in ("swiss_done", "groups_done") and not redraw:
            return await interaction.response.send_message(
                "The main draw has already started. Run /startmain with redraw set to True to re-seed it.",
                ephemeral=True)
        if ev.get("swiss"):
            seeds = list(ev["swiss"]["qualified"])  # earlier qualifiers (better records) get better seeds
            ev["stage"] = "swiss_done"
            note = f"{len(seeds)} teams qualified from the Swiss stage, seeded by record."
        else:
            seeds = groups_seeds(ev["groups"])
            ev["stage"] = "groups_done"
            note = (f"{len(seeds)} teams qualified from the group stage. Group winners are seeded first, "
                    "and teams from the same group don't meet in round 1 where possible.")
        if not seeds:
            return await interaction.response.send_message("No teams qualified.", ephemeral=True)
        byes_ = [t for t in ev.get("byes", []) if str(t) in s["teams"]]
        if byes_:  # the teams that skipped the qualifier are the main draw's top seeds
            seeds = byes_ + [t for t in seeds if t not in byes_]
            note += f" Plus {len(byes_)} team(s) with a bye straight into the main draw, seeded first."
        ev["main"] = None
    else:
        teams = entrant_roles(guild)
        problem = event_problem(s, teams, redraw)
        if problem:
            return await interaction.response.send_message(problem, ephemeral=True)
        k = protected_count(s, len(teams))
        seeds, pts = draw_seeds(s, [t.id for t in teams], k)
        ev = fresh_event(s, "main")
        ev["seeds"], ev["protected"] = seeds, k
        note = (f"{len(seeds)} teams, no qualifier. The top {k} by RISER POINTS are seeded, the rest drawn at random."
                if k else f"{len(seeds)} teams, completely random draw (invite-only event).")

    await interaction.response.defer(ephemeral=True, thinking=True)
    parts = await start_main(guild, ev, seeds, note, post_now=False)
    pts = {t: s["teams"].get(str(t), {}).get("points", 0) for t in seeds}
    if (ev.get("main") or {}).get("matches"):
        ev["drawing"] = True  # secret until the live draw ends
        ev["draw_at"] = (datetime.now(timezone.utc) + timedelta(minutes=draw_in)).isoformat(timespec="seconds")
    save_data(data)
    schedule_publish(guild)
    if not parts:  # one team: no draw
        return await interaction.followup.send("Only one team qualified, so they're the champions.", ephemeral=True)

    async def after():  # the bracket posts once the live draw is over
        await send_blocks(chan(guild, "bracket"), parts)
        ann = chan(guild, "announcements")
        if ann:
            await post(ann, "**The main draw has started!** Check #bracket for your first match.")
    from_qualifier = bool(ev.get("swiss") or ev.get("groups"))
    start_show(guild, "main", seeds, pts, [], note, by_points=not from_qualifier, after=after,
               countdown=draw_in * 60, protected=None if from_qualifier else ev.get("protected", len(seeds)))
    await interaction.followup.send(
        f"Main draw set. The live draw starts in #bracket {'now' if not draw_in else f'in {draw_in} min'}; "
        "the bracket posts when it ends.", ephemeral=True)


@bot.tree.command(description="Staff/Referees: record who won a match (override). Captains use /game_score.")
@app_commands.describe(match="Match number, e.g. 7 for M7", winner="The winning team's role",
                       score="Final score, e.g. 42-38 (optional, used for group tiebreakers)")
async def result(interaction: discord.Interaction, match: int, winner: discord.Role, score: str | None = None):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only Referees and league staff can record results. "
                                                       "Captains: use /game_score.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    ok, msg = await record_result(interaction.guild, match, winner_id, score, interaction.user.id)
    await interaction.followup.send(msg, ephemeral=True, allowed_mentions=NO_PINGS)


async def record_result(guild: discord.Guild, match: int, winner_id: int, score: str | None,
                        reporter: int | None) -> tuple[bool, str]:
    """Record a match result (from /result, a confirmed /game_score, or an admin override).
    Returns (recorded?, message)."""
    data = load_data()
    s = guild_signups(data, guild.id)
    ev = s["event"]
    if not ev or (ev["stage"] == "done" and not cons_running(ev)):
        return False, "No tournament is running."

    cn_match = next((m for m in (ev.get("consolation") or {}).get("matches", []) if m["id"] == match), None)
    pi_match = next((m for m in (ev.get("playin") or {}).get("matches", []) if m["id"] == match), None)
    sw_match = next((m for m in (ev.get("swiss") or {}).get("matches", []) if m["id"] == match), None)
    gr_match = next((m for m in (ev.get("groups") or {}).get("matches", []) if m["id"] == match), None)
    de_match = next((m for m in (ev.get("main") or {}).get("matches", []) if m["id"] == match), None)
    m = sw_match or gr_match or de_match or cn_match or pi_match
    problem = None
    if m is None:
        problem = f"There's no match M{match}."
    elif ((sw_match or gr_match or cn_match or pi_match) and m["winner"]) or (de_match and de_match["done"]):
        problem = f"M{match} already has a result. Ask staff if it needs fixing."
    elif cn_match and (cn_match["a"] is None or cn_match["b"] is None):
        problem = f"M{match} can't be played yet: it's still waiting on earlier consolation matches."
    elif de_match and not (de_match["a_ok"] and de_match["b_ok"]):
        problem = f"M{match} can't be played yet: it's still waiting on earlier matches."
    elif sw_match and ev["stage"] != "swiss":
        problem = f"M{match} is from the finished Swiss stage."
    elif gr_match and ev["stage"] != "groups":
        problem = f"M{match} is from the finished group stage."
    elif winner_id not in (m["a"], m["b"]):
        problem = f"<@&{winner_id}> isn't playing in M{match}."
    if problem:
        return False, problem

    loser = m["b"] if winner_id == m["a"] else m["a"]
    season_over = False
    pts = parse_score(score)
    m["score"] = f"{pts[0]}-{pts[1]}" if pts else (score or None)
    score_txt = f" {m['score']}" if m["score"] else ""
    result_line = f"**M{match} result**: {tag(winner_id)} beat {tag(loser)}{score_txt}"

    if sw_match:
        sw = ev["swiss"]
        sw_match["winner"] = winner_id
        swiss_record(sw, winner_id, loser)
        parts = [result_line]
        if all(x["winner"] for x in sw["matches"] if x["round"] == sw["round"]):
            await send_blocks(chan(guild, "standings"), swiss_table(sw))
            if swiss_active(sw):
                parts.append("\n".join(swiss_next_round(ev)))
                asyncio.create_task(post_picture(guild, "schedule", swiss_round_picture, s, ev))
            else:
                ev["stage"] = "swiss_done"
                q = ", ".join(tag(t) for t in sw["qualified"]) or "none"
                parts.append(f"# Swiss stage complete\n**Into the main draw ({len(sw['qualified'])}):** {q}\n"
                             "Staff: run /startmain to post the double-elimination bracket.")
        await send_blocks(chan(guild, "schedule"), parts)
        if ev["stage"] == "swiss_done":
            await maybe_start_consolation(guild, s, ev)

    elif gr_match:
        gs = ev["groups"]
        gr_match["winner"], gr_match["pts"] = winner_id, list(pts) if pts else None
        parts = [result_line + f" (Group {group_letter(gr_match['group'])})"]
        if groups_finished(gs):
            ev["stage"] = "groups_done"
            for gi in range(len(gs["groups"])):
                order, _st = group_table(gs, gi)
                gs["qualified"] += order[:gs["advance"]]
            q = ", ".join(tag(t) for t in gs["qualified"])
            parts.append(f"# Group stage complete\n**Into the main draw ({len(gs['qualified'])}):** {q}\n"
                         "Staff: run /startmain to post the double-elimination bracket.")
            await send_blocks(chan(guild, "standings"),
                              ["# Final group standings"] + [group_blocks(gs, gi) for gi in range(len(gs["groups"]))])
        else:
            await send_blocks(chan(guild, "standings"), [group_blocks(gs, gr_match["group"])])
        await post_picture(guild, "standings", group_standings_picture, s, ev, edit_key=(ev, "gs_pic"))
        await send_blocks(chan(guild, "schedule"), parts)
        if ev["stage"] == "groups_done":
            await maybe_start_consolation(guild, s, ev)

    elif pi_match:
        pi = ev["playin"]
        pi_match["winner"], pi_match["pts"] = winner_id, list(pts) if pts else None
        pi["alive"] = [t for t in pi["alive"] if int(t) != loser]
        pi["out"].append(str(loser))
        parts = [result_line + f" ({pi_match['label']})"]
        if all(x["winner"] for x in pi["matches"]):
            if len(pi["alive"]) <= pi["spots"]:
                pi["done"] = True
                ev["stage"] = "playin_done"
                tz_ = s.get("tourney") or {}
                tz_["entrants"] += [str(t) for t in pi["alive"] if str(t) not in tz_["entrants"]]
                tz_.setdefault("lcq", {})["playin_winners"] = [str(t) for t in pi["alive"]]
                won = ", ".join(tag(int(t)) for t in pi["alive"])
                parts.append(f"# LCQ play-in complete\n**Into the LCQ:** {won}\nStaff: start the LCQ with /startmain.")
                ann = chan(guild, "announcements")
                if ann:
                    await post(ann, f"The LCQ play-in is done: {won} made it into **{tz_.get('name', 'the LCQ')}**.",
                               title="LCQ play-in", color=GOLD, allowed_mentions=NO_PINGS)
            else:
                nxt = playin_round(ev)
                parts.append(f"## LCQ play-in round {pi['round']}\n" + "\n".join(
                    f"**M{x['id']}**: {tag(x['a'])} vs {tag(x['b'])}" for x in nxt))
        await send_blocks(chan(guild, "schedule"), parts)

    elif cn_match:
        cons = ev["consolation"]
        parts = [result_line + f" ({cn_match['label']})"]
        if cons_record(cons, cn_match, winner_id, loser):
            tz_ = s.get("tourney") or {}
            parts.append(f"# {tag(winner_id)} win the consolation bracket!")
            bonus_lines = await give_cons_bonus(guild, s, ev)
            if bonus_lines:
                await send_blocks(chan(guild, "standings"), bonus_lines)
            elif tz_.get("kind") not in ("major", "lcq"):
                parts.append("Their bonus RISER POINTS are paid when the main draw finishes.")
            ann = chan(guild, "announcements")
            if ann:
                await post(ann, f"**{tag(winner_id)}** won the consolation bracket of **{tz_.get('name', 'the tournament')}**!",
                           title="Consolation champions", color=GOLD, allowed_mentions=NO_PINGS)
            asyncio.create_task(update_board(guild))
        else:
            nxt = [f"**M{x['id']}** {x['label']}: {tag(x['a'])} vs {tag(x['b'])}" for x in cons_ready(cons)]
            if nxt:
                parts.append("**Consolation, up next**\n" + "\n".join(nxt))
        await send_blocks(chan(guild, "bracket"), parts)

    else:
        main = ev["main"]
        parts = [result_line + f" ({de_match['label']})"]
        if de_record(ev, de_match, winner_id, loser):
            parts.append("The Losers bracket team won, so the Grand Final resets: one more game decides it!")
        if main["champion"]:
            ev["stage"] = "done"
            tz = s.get("tourney") or {}
            tname = tz.get("name", "the tournament")
            parts.append(f"# {tag(main['champion'])} win {tname}!")
            await send_blocks(chan(guild, "standings"), award_points(s, ev) + await give_cons_bonus(guild, s, ev))
            ann = chan(guild, "announcements")
            if ann:
                await post(ann, f"**{tag(main['champion'])}** are the champions of **{tname}**! Congratulations!\n"
                               "Final standings and RISER POINTS are in #standings.", title=f"{tname} champions",
                           color=GOLD, file=logo_file(s["teams"].get(str(main["champion"]), {})))
            season_over = True
            champ_tid = main["champion"]
        else:
            nxt = up_next(main)
            if nxt:
                parts.append("**Up next**\n" + "\n".join(nxt))
        await send_blocks(chan(guild, "bracket"), parts)
        await post_bracket_update(guild, s, ev, de_match)  # every game: the live bracket picture + website

    await post_score_card(guild, s, ev, m, reporter)  # the Final Score card in #score-reports
    await post_game_final(guild, s, ev, m)  # #game-finals: the graphic and a recap of the game
    try:
        await settle_pickem(guild, s, m)  # #pickems: who called it, points to the leaderboard
    except Exception as ex:
        print(f"[pickems settle] {ex}")
    if m.get("box"):
        try:
            await post_game_analysis(guild, s, ev, m)  # #game-analysis: the stats were already in
        except Exception as ex:
            print(f"[game analysis] {ex}")
    await post_next_up(guild, s, ev, m)  # each team's channel: the final and who they play next
    save_data(data)
    schedule_publish(guild)
    asyncio.create_task(sync_team_hoist(guild))  # a team knocked out drops out of the member-list groups
    asyncio.create_task(sync_captains_channel(guild))  # tournament over = captains channel deleted
    try:  # #power-rankings: once when the qualifier ends, once when the champion is crowned
        await auto_power_rankings(guild)
    except Exception as e:
        print(f"[power rankings] {e}")
    if season_over:
        try:  # winner roles + the champions list (needs the tournament info, so before anything resets it)
            await crown_champion(guild, load_data(), champ_tid)
        except Exception as e:
            print(f"[champions] {e}")
        await serve_tournament(guild, tname)  # tournament suspensions count down by one
        await update_board(guild)  # new RISER POINTS on the team cards and website
        asyncio.create_task(season_end(guild))  # DM every player: stay or leave?
    return True, f"Recorded: M{match} won by <@&{winner_id}>."


# ---------------------------------------------------------------- team logo emojis
#
# Discord text can only show a picture inline as an emoji, so every team's logo is uploaded as a server emoji
# (named otr_<team>). Media posts (power rankings, stat leaders, live-now) put it left of the team/player name.
# Needs the bot's "Manage Expressions" permission and free emoji slots (50 on an unboosted server).

_emoji_lock: dict[int, asyncio.Lock] = {}


def team_emoji(s: dict, tid) -> str:
    """The team's logo emoji followed by a space, or "" if it doesn't have one."""
    t = s["teams"].get(str(tid)) or {}
    e = t.get("emoji")
    return f"<:{e[1]}:{e[0]}> " if e and t.get("emoji_ok", True) else ""  # new ones wait for a Commissioner's OK


def emoji_by_team_name(s: dict) -> dict:
    return {t["name"]: team_emoji(s, k) for k, t in s["teams"].items()}


def player_team_emoji(s: dict, uid) -> str:
    key = team_of(s, int(uid)) if str(uid).isdigit() else None
    return team_emoji(s, key) if key else ""


EMOJI_STYLE = 3  # bump to remake every team emoji (3 = better background removal, logo trimmed to fill it)


def cut_background(im, tol: int = 48):
    """Make a logo's background transparent: find the background colour from the corners (or the edges), then
    remove every pixel connected to the edge that's close to it. The logo itself stays, even where it uses the
    same colour inside. Copes with JPG noise and logos that touch the edges."""
    from collections import deque
    im = im.convert("RGBA")
    w, h = im.size
    px = im.load()
    edge = [px[x, y] for x in range(w) for y in (0, h - 1)] + [px[x, y] for y in range(h) for x in (0, w - 1)]
    if sum(1 for p in edge if p[3] < 40) > len(edge) * 0.6:
        return im  # already transparent around the edges
    k = max(2, min(w, h) // 25)

    def patch(x0, y0):
        ps = [px[x, y] for x in range(x0, x0 + k) for y in range(y0, y0 + k) if px[x, y][3] >= 40]
        if len(ps) < k * k * 0.6:
            return None
        return tuple(sum(p[i] for p in ps) / len(ps) for i in range(3))
    corners = [c for c in (patch(0, 0), patch(w - k, 0), patch(0, h - k), patch(w - k, h - k)) if c]
    near = lambda a, b: max(abs(a[i] - b[i]) for i in range(3)) <= tol
    bg = None
    for c in corners:  # a colour shared by at least 2 corners is the background
        agree = [d for d in corners if near(c, d)]
        if len(agree) >= 2:
            bg = tuple(sum(d[i] for d in agree) / len(agree) for i in range(3))
            break
    if bg is None:  # fall back to the most common edge colour
        solid = [p[:3] for p in edge if p[3] >= 40]
        buckets = {}
        for r, g, b_ in solid:
            buckets.setdefault((r // 24, g // 24, b_ // 24), []).append((r, g, b_))
        top = max(buckets.values(), key=len) if buckets else []
        if top and len(top) >= len(solid) * 0.35:
            bg = tuple(sum(c[i] for c in top) / len(top) for i in range(3))
    # bg known: remove pixels close to it. No clear colour (gradient, texture): always try anyway, following the
    # background outward step by step (each pixel compared with the one next to it). Commissioners deny bad cuts.
    step = 22
    seen = bytearray(w * h)
    q = deque(((x, y), px[x, y]) for x in range(w) for y in (0, h - 1))
    q.extend(((x, y), px[x, y]) for y in range(h) for x in (0, w - 1))
    while q:
        (x, y), ref = q.popleft()
        i = y * w + x
        if seen[i]:
            continue
        p = px[x, y]
        ok = p[3] < 40 or (bg is not None and near(p, bg)) or (
            max(abs(p[c] - ref[c]) for c in range(3)) <= step  # a gradient: drift slowly with the background...
            and (bg is None or max(abs(p[c] - bg[c]) for c in range(3)) <= 3 * tol))  # ...but never into the logo
        if not ok:
            continue
        seen[i] = 1
        px[x, y] = (p[0], p[1], p[2], 0)
        for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
            if 0 <= nx < w and 0 <= ny < h and not seen[ny * w + nx]:
                q.append(((nx, ny), p))
    if bg is None:  # for the soft edge below: the average of what was removed along the border
        gone = [px[x, y] for x in range(w) for y in (0, h - 1) if px[x, y][3] == 0]
        bg = tuple(sum(g_[c] for g_ in gone) / len(gone) for c in range(3)) if gone else (0, 0, 0)
    # soft edge: pixels touching the cut that are partly background colour get partly see-through
    for y in range(h):
        for x in range(w):
            p = px[x, y]
            if p[3] == 0:
                continue
            if any(0 <= nx < w and 0 <= ny < h and px[nx, ny][3] == 0
                   for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1))):
                d = max(abs(p[i] - bg[i]) for i in range(3))
                if d <= tol * 2:
                    px[x, y] = (p[0], p[1], p[2], int(p[3] * min(1, (d - tol) / tol if d > tol else 0.35)))
    return im

def _emoji_png(path, cut: bool = True) -> bytes | None:
    from PIL import Image
    try:
        im = Image.open(path).convert("RGBA")
        im.thumbnail((256, 256))
        if cut:
            im = cut_background(im)
        from PIL import ImageFilter
        solid = im.getchannel("A").point(lambda v: 255 if v > 20 else 0)
        core = solid.filter(ImageFilter.MinFilter(5)).filter(ImageFilter.MaxFilter(5))  # ignore leftover specks
        box = core.getbbox() or solid.getbbox()
        if box:  # trim the empty space so the logo fills the emoji
            pad = 2
            box = (max(0, box[0] - pad), max(0, box[1] - pad), min(im.width, box[2] + pad), min(im.height, box[3] + pad))
            im = im.crop(box)
        side = max(im.size)
        sq = Image.new("RGBA", (side, side), (0, 0, 0, 0))
        sq.paste(im, ((side - im.width) // 2, (side - im.height) // 2), im)
        sq = sq.resize((128, 128), Image.LANCZOS)
        buf = io.BytesIO()
        sq.save(buf, "PNG", optimize=True)
        return buf.getvalue() if buf.tell() < 250_000 else None
    except Exception:
        return None

async def sync_team_emojis(guild: discord.Guild) -> int:
    """Make a logo emoji for every team that has a logo (and redo it when the logo changes);
    delete emojis of teams that are gone. Returns how many were made."""
    lock = _emoji_lock.setdefault(guild.id, asyncio.Lock())
    async with lock:  # a second call waits for the first one, then sees its emojis
        data = load_data()
        s = guild_signups(data, guild.id)
        made, changed = 0, False
        live_ids = set()
        new_imgs = []  # (team key, name, png) for the Commissioner preview
        _emoji_report[guild.id] = report = {"made": [], "failed": [], "no_logo": [], "no_slots": []}
        for key, t in s["teams"].items():
            e = t.get("emoji")
            have = guild.get_emoji(int(e[0])) if e else None
            if have and t.get("emoji_logo") == t.get("logo") and t.get("emoji_v") == EMOJI_STYLE:
                live_ids.add(have.id)
                continue
            if have:  # the logo changed: replace the emoji
                try:
                    await have.delete(reason="Team logo changed")
                except discord.HTTPException:
                    pass
            if t.get("emoji_logo") and t.get("emoji_logo") != t.get("logo"):  # a new logo: start fresh
                t.pop("emoji_nocut", None)
                t.pop("emoji_denied", None)
            if t.get("emoji_denied"):
                continue  # denied twice: this team shows without a logo emoji
            t["emoji"] = t["emoji_logo"] = None
            changed = True
            path = LOGO_DIR / t["logo"] if t.get("logo") else None
            if not path or not path.exists():
                report["no_logo"].append(t["name"])
                continue
            if len([x for x in guild.emojis if not x.animated]) >= guild.emoji_limit:
                report["no_slots"].append(t["name"])
                continue  # no free emoji slots
            img = await asyncio.to_thread(_emoji_png, path, not t.get("emoji_nocut"))
            if not img:
                report["failed"].append(f"{t['name']} (couldn't read the logo)")
                continue
            nm = ("otr_" + re.sub(r"[^A-Za-z0-9_]", "", t["name"].replace(" ", "_")))[:32]
            if len(nm) < 5:
                nm = f"otr_team{key[-4:]}"
            try:
                em = await guild.create_custom_emoji(name=nm, image=img, reason=f"Logo for {t['name']}")
            except Exception as ex:  # noqa: BLE001
                wait = rate_limit_wait(ex)
                if wait is not None:  # Discord's emoji limit: carry on by itself when it expires
                    report["waiting"] = when_free(wait + 5)
                    if not _emoji_retry.get(guild.id):
                        async def resume(g=guild, w=wait):
                            await asyncio.sleep(w + 5)
                            _emoji_retry.pop(g.id, None)
                            await sync_team_emojis(g)
                        _emoji_retry[guild.id] = asyncio.create_task(resume())
                    print(f"[team emoji] rate limited for {int(wait)}s; finishing then")
                    break
                if not isinstance(ex, discord.HTTPException):
                    raise
                print(f"[team emoji] {t['name']}: {ex}")
                report["failed"].append(f"{t['name']} ({'the bot needs Manage Expressions' if getattr(ex, 'status', 0) == 403 else ex})")
                continue
            report["made"].append(t["name"])
            new_imgs.append((key, t["name"], img))
            t["emoji"], t["emoji_logo"], t["emoji_v"] = [em.id, em.name], t.get("logo"), EMOJI_STYLE
            t["emoji_ok"] = False  # not used in posts until a Commissioner confirms it
            live_ids.add(em.id)
            made += 1
            await asyncio.sleep(1)
        ours = set(s.get("team_emoji_ids", [])) | live_ids  # only ever delete emojis the bot made for teams
        for em in guild.emojis:
            if em.id in ours and em.id not in live_ids:  # that team is gone
                try:
                    await em.delete(reason="Team no longer exists")
                except discord.HTTPException:
                    pass
        if changed or made:
            d2 = load_data()  # merge into fresh data (other things may have saved meanwhile)
            s2 = guild_signups(d2, guild.id)
            for key, t in s["teams"].items():
                if key in s2["teams"]:
                    s2["teams"][key]["emoji"], s2["teams"][key]["emoji_logo"] = t.get("emoji"), t.get("emoji_logo")
                    s2["teams"][key]["emoji_v"] = t.get("emoji_v")
                    s2["teams"][key]["emoji_ok"] = t.get("emoji_ok", True)
                    for f_ in ("emoji_nocut", "emoji_denied"):
                        if t.get(f_):
                            s2["teams"][key][f_] = True
                        else:
                            s2["teams"][key].pop(f_, None)
            s2["team_emoji_ids"] = sorted(live_ids)
            save_data(d2)
        if made:
            print(f"[{guild.name}] Made {made} team logo emoji(s).")
            try:
                await refresh_leaders(guild)  # stat leaders pick up the new logos
            except Exception as ex:
                print(f"[leaders] {ex}")
            try:
                await send_emoji_preview(guild, new_imgs)  # Commissioner+ check the cut-outs
            except Exception as ex:
                print(f"[emoji preview] {ex}")
        return made


def emoji_preview_png(items: list) -> bytes:
    """A sheet of new team emojis: each on Discord's dark background (how people will see it) and on a
    checkerboard (so you can tell what's see-through)."""
    from PIL import Image, ImageDraw
    cols = min(4, max(1, len(items)))
    rows = (len(items) + cols - 1) // cols
    CW, CH = 300, 190
    img = Image.new("RGB", (cols * CW + 20, rows * CH + 70), (30, 31, 34))
    d = ImageDraw.Draw(img)
    d.text((20, 18), "NEW TEAM LOGO EMOJIS  (left: Discord dark mode · right: see-through check)", font=_font(18),
           fill=(230, 230, 230))
    for i, (_k, name, png) in enumerate(items):
        x, y = 10 + (i % cols) * CW, 60 + (i // cols) * CH
        em = Image.open(io.BytesIO(png)).convert("RGBA").resize((110, 110), Image.LANCZOS)
        dark = Image.new("RGBA", (130, 130), (49, 51, 56, 255))
        dark.alpha_composite(em, (10, 10))
        chk = Image.new("RGBA", (130, 130), (255, 255, 255, 255))
        cd = ImageDraw.Draw(chk)
        for yy in range(0, 130, 13):
            for xx in range(0, 130, 13):
                if (xx // 13 + yy // 13) % 2:
                    cd.rectangle((xx, yy, xx + 12, yy + 12), fill=(205, 205, 210, 255))
        chk.alpha_composite(em, (10, 10))
        img.paste(dark.convert("RGB"), (x + 10, y))
        img.paste(chk.convert("RGB"), (x + 150, y))
        d.text((x + 10, y + 138), name[:28], font=_fit(d, name[:28], 270, 18, 12), fill=(245, 245, 245))
    return _png(img)


async def send_emoji_preview(guild: discord.Guild, items: list, review: bool = False):
    """DM Commissioner+ each team emoji ONE BY ONE, each with its own Confirm / Deny. review=True: emojis that are
    already in use (from /refresh what:emojis) keep showing unless denied."""
    for key, name, png in items:
        sheet = await asyncio.to_thread(emoji_preview_png, [(key, name, png)])
        v = discord.ui.View(timeout=None)
        v.add_item(discord.ui.Button(label="Confirm", emoji="✅", style=discord.ButtonStyle.success,
                                     custom_id=f"emo:ok:{guild.id}:{key}"))
        v.add_item(discord.ui.Button(label="Deny", emoji="✖", style=discord.ButtonStyle.danger,
                                     custom_id=f"emo:no:{guild.id}:{key}"))
        text = (f"Logo emoji for **{name}**. Still look right?" if review else
                f"New logo emoji for **{name}**, background removed. It shows in the media posts once you confirm.")
        for m in commissioners(guild):
            for _try in range(3):
                try:
                    e = brand_embed(text, f"🖼️ {name}", GOLD)
                    e.set_image(url="attachment://emoji.png")
                    await m.send(embed=e, file=discord.File(io.BytesIO(sheet), filename="emoji.png"), view=v)
                    break
                except Exception as ex:  # noqa: BLE001
                    wait = rate_limit_wait(ex)
                    if wait is None:
                        break
                    await asyncio.sleep(wait + 1)  # rate limited: send it when the limit expires
        await asyncio.sleep(1)  # one at a time, without hitting Discord's rate limits

@bot.listen("on_interaction")
async def emoji_preview_buttons(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return
    cid = (interaction.data or {}).get("custom_id", "")
    if not cid.startswith("emo:"):
        return
    parts = cid.split(":")
    action, gid = parts[1], int(parts[2])
    guild = bot.get_guild(gid)
    member = guild.get_member(interaction.user.id) if guild else None
    if guild is None or member is None or not is_commissioner(member):
        return await interaction.response.send_message("Only the Commissioner or an admin can do that.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, gid)
    if len(parts) > 3 and parts[3] in s["teams"]:
        keys = [parts[3]]  # this one team
    else:
        keys = [k for k, t in s["teams"].items() if not t.get("emoji_ok", True) and not t.get("emoji_denied")]
    if action == "no":  # denied: try again from the original logo (background kept); denied twice = no emoji shown
        redo = []
        for k in keys:
            t = s["teams"][k]
            if not t.get("emoji_nocut"):
                t["emoji_nocut"], t["emoji_v"] = True, None
                redo.append(t["name"])
            else:
                t["emoji_denied"] = True
        save_data(data)
        await interaction.response.edit_message(
            content=f"✖ Denied by {member.display_name}."
                    + (" Remaking from the original logo (background kept) for you to check: " + ", ".join(redo)
                       if redo else " Those teams show without a logo."), view=None)
        if redo:
            asyncio.create_task(sync_team_emojis(guild))
        return
    for k in keys:
        if k in s["teams"]:
            s["teams"][k]["emoji_ok"] = True
    save_data(data)
    await interaction.response.edit_message(content=f"✅ Confirmed by {member.display_name}.", view=None)
    try:
        await refresh_leaders(guild)  # the logos show up right away
    except Exception as ex:
        print(f"[leaders] {ex}")


_emoji_report: dict[int, dict] = {}
_emoji_retry: dict[int, asyncio.Task] = {}


@app_commands.default_permissions(manage_messages=True)
async def teamemojis(interaction: discord.Interaction):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    perms = guild.me.guild_permissions
    can = getattr(perms, "manage_expressions", False) or getattr(perms, "manage_emojis", False) or perms.administrator
    data = load_data()
    for t in guild_signups(data, guild.id)["teams"].values():  # start over: background removal for every team
        t.pop("emoji_nocut", None)
        t.pop("emoji_denied", None)
        t["emoji_v"] = None
    save_data(data)
    await sync_team_emojis(guild)  # remakes them all and DMs them to Commissioner+ one by one
    s = guild_signups(load_data(), guild.id)
    rep_ = _emoji_report.get(guild.id, {})
    have = [team_emoji(s, k) + t["name"] for k, t in s["teams"].items() if t.get("emoji")]
    used = len([x for x in guild.emojis if not x.animated])
    lines = [f"**{len(have)}/{len(s['teams'])} teams have a logo emoji.** Emoji slots used: {used}/{guild.emoji_limit}."]
    if not can:
        lines.append("⚠️ **The bot doesn't have Manage Expressions.** Server Settings → Roles → the bot's role → turn on "
                     "**Manage Expressions**, then run this again.")
    if rep_.get("made"):
        lines.append("Made now: " + ", ".join(rep_["made"]))
    if rep_.get("failed"):
        lines.append("Failed: " + "; ".join(rep_["failed"][:10]))
    if rep_.get("waiting"):
        lines.append(f"⏳ Discord's emoji limit was hit. The bot finishes the rest by itself at {rep_['waiting']}.")
    if rep_.get("no_slots"):
        lines.append(f"No free emoji slots for: {', '.join(rep_['no_slots'][:15])}. Delete unused emojis or boost the server.")
    if rep_.get("no_logo"):
        lines.append("No logo uploaded: " + ", ".join(rep_["no_logo"][:15]))
    if have:
        lines.append("\n" + " · ".join(have[:40]))
    if rep_.get("made"):
        lines.append(f"\nRemade {len(rep_['made'])} emoji(s) with the background removed. They're in Commissioner+ "
                     "DMs one by one: Confirm or Deny each.")
    await interaction.followup.send("\n".join(lines)[:1990], ephemeral=True)


# ---------------------------------------------------------------- /mediapost: Media posts that also go on the website
#
# The bot can't read people's messages (no message-content permission), so Media members post through the bot:
# /mediapost kind:OTR Report / YouTube highlight / Official GFX title:... link:... image:...
# It goes in the right Discord channel AND on the website's Media tab.

MEDIA_DIR = Path(__file__).with_name("media_uploads")
_uploaded_media: set[str] = set()
MEDIA_KINDS = {"report": ("OTR Report", "report", "📰"), "yt": ("YouTube highlight", "yt", "▶️"),
               "gfx": ("Official GFX", "gfx", "🖼️")}


def youtube_id(link: str | None) -> str | None:
    m = re.search(r"(?:youtu\.be/|youtube\.com/(?:watch\?v=|shorts/|embed/|live/))([A-Za-z0-9_-]{11})", link or "")
    return m.group(1) if m else None


@bot.tree.command(description="Media/staff: post an OTR Report, a YouTube highlight or an official GFX (Discord + website).")
@app_commands.describe(kind="What it is", title="Title, e.g. 'OTR Report Ep. 3: Week 6 recap'",
                       link="Link (YouTube, TikTok, a stream VOD...). Needed for YouTube highlights.",
                       description="A line or two about it (optional)", image="The graphic (Official GFX) or a thumbnail")
@app_commands.choices(kind=[app_commands.Choice(name=v[0], value=k) for k, v in MEDIA_KINDS.items()])
async def mediapost(interaction: discord.Interaction, kind: str, title: str, link: str | None = None,
                    description: str | None = None, image: discord.Attachment | None = None):
    user, guild = interaction.user, interaction.guild
    if not (is_staff(user) or any(r.name == "Media" for r in user.roles)):
        return await interaction.response.send_message("Only the Media role or staff can post media.", ephemeral=True)
    label, key, icon = MEDIA_KINDS[kind]
    link = good_link(link) if link else None
    yid = youtube_id(link)
    if kind == "yt" and not yid:
        return await interaction.response.send_message("Add the YouTube link (youtube.com/watch?v=... or youtu.be/...).",
                                                       ephemeral=True)
    if kind == "gfx" and image is None:
        return await interaction.response.send_message("Attach the graphic with the `image` option.", ephemeral=True)
    if image is not None:
        kind_ = (image.content_type or "").split(";")[0].lower()
        if kind_ not in LOGO_TYPES or image.size > 8_000_000:
            return await interaction.response.send_message("The image has to be a PNG, JPG, WEBP or GIF under 8 MB.",
                                                           ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    fname = None
    if image is not None:
        MEDIA_DIR.mkdir(exist_ok=True)
        fname = f"{secrets.token_hex(6)}.{LOGO_TYPES[(image.content_type or '').split(';')[0].lower()]}"
        (MEDIA_DIR / fname).write_bytes(await image.read())
    c = media(s)["chans"]
    ch = guild.get_channel(c.get(key) or 0)
    if ch is None:
        return await interaction.followup.send("That media channel doesn't exist yet. Run `/setupbot part:media`.",
                                               ephemeral=True)
    e = brand_embed((description or "")[:1500] + (f"\n\n▶ **[Watch]({link})**" if link and kind != "gfx" else
                                                   f"\n\n[Link]({link})" if link else ""),
                    f"{icon} {title[:200]}", GOLD if kind == "report" else 0xEF4444 if kind == "yt" else INFO,
                    url=link)
    e.set_author(name=f"{label} · by {getattr(user, 'display_name', user.name)}")
    kw = {"embed": e, "allowed_mentions": NO_PINGS}
    if fname:
        f = discord.File(MEDIA_DIR / fname, filename=fname)
        e.set_image(url=f"attachment://{fname}")
        kw["file"] = f
    elif yid:
        e.set_image(url=f"https://img.youtube.com/vi/{yid}/hqdefault.jpg")
    msg = await ch.send(**kw)
    posts = s.setdefault("media_posts", [])
    posts.insert(0, {"id": msg.id, "kind": kind, "title": title[:200], "desc": (description or "")[:1500],
                     "link": link, "yt": yid, "image": f"media/{fname}" if fname else None,
                     "by": getattr(user, "display_name", user.name),
                     "at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    s["media_posts"] = posts[:60]
    save_data(data)
    schedule_publish(guild)
    await interaction.followup.send(f"Posted in {ch.mention} and on the website's Media tab.", ephemeral=True)


@bot.tree.command(description="Media/staff: take one of your media posts off the website (and Discord).")
@app_commands.describe(title="Start of the post's title")
async def mediaremove(interaction: discord.Interaction, title: str):
    user, guild = interaction.user, interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    posts = s.get("media_posts", [])
    hit = next((p_ for p_ in posts if p_["title"].lower().startswith(title.lower().strip())), None)
    if hit is None:
        return await interaction.response.send_message("No media post starts with that title.", ephemeral=True)
    if not (is_staff(user) or hit.get("by") == getattr(user, "display_name", None)):
        return await interaction.response.send_message("Only staff or the person who posted it can remove it.",
                                                       ephemeral=True)
    posts.remove(hit)
    save_data(data)
    ch = guild.get_channel(media(s)["chans"].get(MEDIA_KINDS[hit["kind"]][1]) or 0)
    if ch:
        try:
            await (await ch.fetch_message(hit["id"])).delete()
        except discord.HTTPException:
            pass
    schedule_publish(guild)
    await interaction.response.send_message(f"Removed **{hit['title']}**.", ephemeral=True)


# ---------------------------------------------------------------- automatic power rankings (#power-rankings)
#
# Posted by the bot when the qualifier (groups / Swiss) finishes and when the champion is crowned, or any time with
# /refresh what:rankings. Top 8 only. Score = win % + point differential per game + strength of schedule; once the main
# draw is over, final placement comes first. Each team gets a one-line synopsis, plus a recap of the stage.

PR_TOP = 8


def power_table(s: dict, ev: dict, final: bool = False) -> list[dict]:
    """Every team that played in this tournament, best first, with the numbers behind it."""
    rec: dict[int, dict] = {}
    games = [m for m in all_matches(ev) if m.get("winner") and m.get("a") is not None and m.get("b") is not None]
    for m in games:
        w = m["winner"]
        lo = m["b"] if w == m["a"] else m["a"]
        sc = m.get("pts") or parse_score(m.get("score"))
        d = int(sc[0]) - int(sc[1]) if sc else 0
        for t, won, opp in ((w, True, lo), (lo, False, w)):
            r = rec.setdefault(t, {"tid": t, "w": 0, "l": 0, "pd": 0, "opps": [], "wins_over": [], "losses_to": [],
                                   "games": []})
            r["w" if won else "l"] += 1
            r["pd"] += d if won else -d
            r["opps"].append(opp)
            r["games"].append((m["id"], won, opp, d))
            (r["wins_over"] if won else r["losses_to"]).append((opp, d))
    if not rec:
        return []
    pct = {t: r["w"] / max(1, r["w"] + r["l"]) for t, r in rec.items()}
    placed = {}
    if final and (ev.get("main") or {}).get("champion"):
        placed = {t: p for p, ts in final_standings(ev) for t in ts}
    qualified = set((ev.get("groups") or {}).get("qualified", []) + (ev.get("swiss") or {}).get("qualified", []))
    if ev.get("main"):
        qualified |= {x for m in ev["main"]["matches"] for x in (m.get("a"), m.get("b")) if x and m.get("a_ok")}
    for t, r in rec.items():
        gp = r["w"] + r["l"]
        r["gp"], r["pdpg"] = gp, r["pd"] / max(1, gp)
        r["sos"] = sum(pct[o] for o in r["opps"]) / max(1, len(r["opps"]))
        r["rp"] = s["teams"].get(str(t), {}).get("points", 0)
        r["score"] = (100 * pct[t] + 2 * max(-20, min(20, r["pdpg"])) + 30 * r["sos"]
                      + (15 if t in qualified else 0) + min(10, r["rp"] / 60))
        r["place"] = placed.get(t)
        r["qualified"] = t in qualified
    dq = set(ev.get("dq") or [])
    rows = [r for t, r in rec.items() if t not in dq and str(t) in s["teams"]]
    rows.sort(key=lambda r: ((r["place"] or 999) if placed else 0, -r["score"]))
    return rows


def player_take(players: dict, w: int, l: int, pname, top_ppg: float, pick) -> str | None:
    """An honest line about one player: who's cold, careless or invisible on a team that's losing,
    or who's carrying a team that's winning."""
    cold = [(a["fgm"] / a["fga"], u, a) for u, a in players.items() if a["fga"] >= 10 and a["fgm"] / a["fga"] < 0.36]
    sloppy = [(a["to"] / a["gp"], u, a) for u, a in players.items() if a["gp"] and a["to"] / a["gp"] >= 3]
    if l >= w and cold:
        pct_, u, a = min(cold)
        three = f", {a['fg3m']}/{a['fg3a']} from three" if a["fg3a"] >= 6 else ""
        return pick([f"{pname(u)} has been ice cold, shooting {100 * pct_:.0f}% ({a['fgm']}/{a['fga']}{three}), and they can't "
                     "win like that.",
                     f"Somebody needs to talk to {pname(u)}: {a['fgm']}/{a['fga']} from the field{three} is killing them.",
                     f"{pname(u)} has to be better. {100 * pct_:.0f}% shooting isn't going to cut it."])
    if l >= w and sloppy:
        tpg, u, a = max(sloppy)
        return pick([f"{pname(u)} is turning it over {tpg:.1f} times a game, and that's costing them.",
                     f"Ball security is a problem, starting with {pname(u)} ({tpg:.1f} turnovers a game)."])
    if w > l and players:
        u, a = max(players.items(), key=lambda kv: kv[1]["pts"] / max(1, kv[1]["gp"]))
        ppg = a["pts"] / max(1, a["gp"])
        if ppg >= top_ppg - 0.05 and ppg > 0:
            return f"{pname(u)} has been the best scorer in the tournament ({ppg:.1f} PPG), and it isn't close."
        if a["fga"] >= 10 and a["fgm"] / a["fga"] >= 0.55:
            return f"{pname(u)} is cooking: {ppg:.1f} PPG on {100 * a['fgm'] / a['fga']:.0f}% shooting."
    return None


def team_story(s: dict, ev: dict, r: dict, stage: str, star: tuple | None, pname, players: dict | None = None,
               top_ppg: float = 0) -> str:
    """Up to 3 sentences about a team's tournament so far: hot, steady or struggling, their streak or
    signature result, and where it leaves them (or who's carrying them)."""
    t = r["tid"]
    T = f"**{team_name(s, t)}**"
    nm = lambda x: team_name(s, x)
    w, l, pdpg = r["w"], r["l"], r["pdpg"]
    import zlib
    seed_ = zlib.crc32(team_name(s, t).encode()) + w * 7 + l * 3
    used = [0]

    def pick(opts):  # varied wording between teams, but the same team gets the same line on a re-post
        used[0] += 1
        return opts[(seed_ + used[0] * 5) % len(opts)]
    games = sorted(r["games"])
    streak, last = 0, None
    for _id, won, _o, _d in reversed(games):
        if last is None or won == last:
            streak, last = streak + 1, won
        else:
            break
    champ = (ev.get("main") or {}).get("champion")
    out = []
    # 1. how they're doing
    if t == champ:
        out.append(pick([f"{T} won it all, finishing {w}-{l} and winning by {pdpg:+.1f} a game.",
                         f"{T} are your champions: {w}-{l} and {pdpg:+.1f} per game when it counted."]))
    elif l == 0 and w >= 2:
        out.append(pick([f"{T} are rolling: unbeaten at {w}-0 and winning by {pdpg:.1f} a game.",
                         f"Nobody has figured out {T} yet. They're {w}-0 with a {pdpg:+.1f} point differential."]))
    elif w == 0:
        out.append(pick([f"It's been a rough run for {T}: still looking for their first win at 0-{l}.",
                         f"{T} are struggling, sitting at 0-{l} and getting outscored by {abs(pdpg):.1f} a game."]))
    elif w > l:
        out.append(pick([f"{T} are trending up at {w}-{l}" + (f", winning by {pdpg:.1f} a game." if pdpg > 0 else "."),
                         f"{T} have been steady, {w}-{l} with a {pdpg:+.1f} point differential.",
                         f"At {w}-{l}, {T} are one of the teams to beat right now.",
                         f"{T} keep stacking wins and sit at {w}-{l}."]))
    elif w == l:
        out.append(pick([f"{T} are hanging around at {w}-{l}" + (", but they're getting outscored." if pdpg < 0 else "."),
                         f"{T} sit at {w}-{l}: good enough to stay in it, not yet good enough to scare anyone.",
                         f"{T} have been up and down, splitting their games at {w}-{l}.",
                         f"It's been a coin flip for {T} so far ({w}-{l})."]))
    else:
        out.append(pick([f"{T} are struggling at {w}-{l}" + (f", getting outscored by {abs(pdpg):.1f} a game." if pdpg < 0 else "."),
                         f"Things haven't clicked for {T}, who are {w}-{l} so far.",
                         f"{T} are in a tough spot at {w}-{l}.",
                         f"It's been a struggle for {T}: {w}-{l} with a {pdpg:+.1f} point differential."]))
    # 2. momentum or the result that defines them
    if streak >= 2 and last:
        out.append(f"They've won {streak} straight" + (f", including a {max(d for *_x, d in games[-streak:])}-point blowout."
                                                        if max(d for *_x, d in games[-streak:]) >= 15 else "."))
    elif streak >= 2 and not last:
        out.append(pick([f"They've dropped {streak} in a row and need an answer fast.",
                         f"{streak} straight losses have them searching for answers."]))
    elif r["losses_to"] and (l >= w or max(d for _o, d in r["losses_to"]) >= 15):
        o, d = max(r["losses_to"], key=lambda x: x[1])
        out.append(pick([f"The {d}-point loss to {nm(o)} stung.", f"The {d}-point loss to {nm(o)} is the one they'd want back.",
                         f"{nm(o)} beat them by {d}, and it showed some holes."]) if d else f"Losing to {nm(o)} hurt.")
    elif r["wins_over"]:
        o, d = max(r["wins_over"], key=lambda x: (s["teams"].get(str(x[0]), {}).get("points", 0), x[1]))
        out.append(pick([f"Their statement win came against {nm(o)}" + (f", by {d}." if d else "."),
                         f"Beating {nm(o)}" + (f" by {d}" if d else "") + " is the result that stands out."]))
    # 3. where it leaves them, or who's carrying them
    elimd = set((ev.get("swiss") or {}).get("eliminated", []))
    if stage == "qual" and (ev.get("groups") or ev.get("swiss")):
        elimd |= {x for x in [r_["tid"] for r_ in [r]] if not r.get("qualified") and
                  ev.get("stage") in ("groups_done", "swiss_done", "main")}
    if t == champ:
        if star:
            out.append(f"{pname(star[0])} led the way with {star[1]:.1f} PPG.")
    elif stage == "final" and r.get("place"):
        out.append(f"They finish {place_label(r['place'], 1)}." + (f" {pname(star[0])} averaged {star[1]:.1f} PPG."
                                                                    if star and len(out) < 3 else ""))
    elif t in elimd:
        out.append(pick(["Their run ends in the qualifier.", "They're out, and it's back to the drawing board."]))
    elif stage == "qual" and r.get("qualified"):
        out.append(f"They're into the main draw" + (f", with {pname(star[0])} averaging {star[1]:.1f} PPG." if star else "."))
    elif (take := player_take(players or {}, w, l, pname, top_ppg, pick)):
        out.append(take)
    elif w > l:
        out.append(pick(["Everyone's chasing them right now.", "They look like a real threat to win it.",
                         "Keep this up and they'll be a tough out."]))
    elif w == l:
        out.append(pick(["The next game could swing their whole tournament.", "They need to string some wins together.",
                         "A big win would change the conversation."]))
    else:
        out.append(pick(["They need wins, and they need them now.", "The pressure is on.",
                         "Time is running out to turn it around."]))
    return " ".join(out[:3])


def site_text(t: str) -> str:
    """Discord text -> website text: drop custom emoji tags (the site shows real logos) and spare spaces."""
    return re.sub(r"<a?:\w+:\d+>\s?", "", t or "").strip()


def power_rankings_embeds(guild: discord.Guild, s: dict, ev: dict, stage: str,
                          collect: dict | None = None) -> list[discord.Embed]:
    final = stage == "final"
    rows = power_table(s, ev, final)
    if not rows:
        return []
    tz = s.get("tourney") or {}
    tname = tz.get("name", "the tournament")
    nm = lambda t: team_emoji(s, t) + team_name(s, t)  # logo emoji left of the name
    seeds = ev.get("seeds") or []
    seed_of = {t: i + 1 for i, t in enumerate(seeds)}
    last = (s.get("power_rankings") or {}).get("last", [])
    # top player per team (PPG) from the box scores
    best: dict[int, tuple] = {}
    lines_by: dict[str, dict] = {}
    for m in all_matches(ev):
        for uid, ln in (m.get("box") or {}).items():
            a = lines_by.setdefault(uid, {"team": ln["team"], "gp": 0, "pts": 0, "reb": 0, "ast": 0, "fgm": 0, "fga": 0,
                                          "fg3m": 0, "fg3a": 0, "to": 0})
            a["gp"] += 1
            for k in ("pts", "reb", "ast", "fg3m", "fg3a", "to"):
                a[k] += ln.get(k, 0) or 0
            a["fgm"] += (ln.get("fg2m", 0) or 0) + (ln.get("fg3m", 0) or 0)
            a["fga"] += (ln.get("fg2a", 0) or 0) + (ln.get("fg3a", 0) or 0)
    for uid, a in lines_by.items():
        ppg = a["pts"] / max(1, a["gp"])
        if ppg > best.get(a["team"], (None, -1))[1]:
            best[a["team"]] = (uid, ppg, a["reb"] / max(1, a["gp"]), a["ast"] / max(1, a["gp"]))

    def pname(uid):
        mem = guild.get_member(int(uid)) if str(uid).isdigit() else None
        return mem.display_name if mem else "a player"

    top_ppg = max((a["pts"] / max(1, a["gp"]) for a in lines_by.values()), default=0)
    out_lines = []
    for i, r in enumerate(rows[:PR_TOP], 1):
        t = r["tid"]
        move = ""
        if last:
            if t in last:
                diff = last.index(t) + 1 - i
                move = f" ▲{diff}" if diff > 0 else f" ▼{-diff}" if diff < 0 else " ="
            else:
                move = " 🆕"
        bits = [f"**{r['w']}-{r['l']}**", f"{r['pdpg']:+.1f} PD/game"]
        if r.get("place"):
            bits.insert(0, f"**{place_label(r['place'], 1)}**")
        if r["wins_over"]:
            o, d = max(r["wins_over"], key=lambda x: (s["teams"].get(str(x[0]), {}).get("points", 0), x[1]))
            bits.append(f"best win: {nm(o)}" + (f" by {d}" if d else ""))
        star = best.get(t)
        star_txt = (f"\n> ⭐ {team_emoji(s, t)}{pname(star[0])}: {star[1]:.1f} PPG · {star[2]:.1f} RPG · "
                    f"{star[3]:.1f} APG" if star else "")
        story = team_story(s, ev, r, stage, star, pname,
                           {u: a for u, a in lines_by.items() if a["team"] == t}, top_ppg)
        if collect is not None:
            collect.setdefault("rows", []).append({
                "rank": i, "team": team_name(s, t), "move": move.strip(), "record": f"{r['w']}-{r['l']}",
                "pd": round(r["pdpg"], 1), "place": place_label(r["place"], 1) if r.get("place") else None,
                "best_win": site_text(next((b for b in bits if b.startswith("best win")), "")) or None,
                "star": ({"name": pname(star[0]), "ppg": round(star[1], 1), "rpg": round(star[2], 1),
                          "apg": round(star[3], 1)} if star else None),
                "story": site_text(story)})
        out_lines.append(f"**{i}.** {team_emoji(s, t)}**{team_name(s, t)}**{move}\n> " + " · ".join(bits) + star_txt
                         + (f"\n{story}" if story else ""))

    # the stage recap: upset, best game, top scorer
    games = [m for m in all_matches(ev) if m.get("winner") and m.get("a") is not None and m.get("b") is not None]
    recap = []
    played = len(games)
    stage_txt = {"qual": "the " + ("group stage" if ev.get("groups") else "Swiss stage" if ev.get("swiss") else "qualifier"),
                 "final": "the tournament", "now": "the latest results"}[stage]
    recap.append(f"{played} games into {stage_txt} of **{tname}**." if stage == "now" else
                 f"**{stage_txt[0].upper() + stage_txt[1:]}** of **{tname}** is done: {played} games played.")
    if final and (ev.get("main") or {}).get("champion"):
        recap.append(f"🏆 **{nm(ev['main']['champion'])}** are the champions.")
    ups = []
    for m in games:
        w = m["winner"]
        lo = m["b"] if w == m["a"] else m["a"]
        if w in seed_of and lo in seed_of and seed_of[w] - seed_of[lo] >= 3:
            ups.append((seed_of[w] - seed_of[lo], m, w, lo))
    if ups:
        gap, m, w, lo = max(ups, key=lambda x: x[0])
        recap.append(f"**Biggest upset:** #{seed_of[w]} seed {nm(w)} beat #{seed_of[lo]} seed {nm(lo)}"
                     + (f" {m['score']}" if m.get("score") and m["score"] != "FF" else "") + ".")
    scored = [(sum(m.get("pts") or parse_score(m.get("score")) or (0, 0)), m) for m in games]
    scored = [x for x in scored if x[0]]
    if scored:
        tot, m = max(scored, key=lambda x: x[0])
        recap.append(f"**Highest-scoring game:** {nm(m['a'])} vs {nm(m['b'])}, {m.get('score')} ({tot} total points).")
    close = [(abs(int(x[0]) - int(x[1])), m) for m in games if (x := (m.get("pts") or parse_score(m.get("score"))))]
    if close:
        d, m = min(close, key=lambda x: x[0])
        if d <= 5:
            recap.append(f"**Closest game:** {nm(m['winner'])} edged {nm(m['b'] if m['winner'] == m['a'] else m['a'])} "
                         f"{m.get('score')}.")
    if lines_by:
        uid, a = max(lines_by.items(), key=lambda kv: (kv[1]["pts"] / max(1, kv[1]["gp"]), kv[1]["gp"]))
        recap.append(f"**Top scorer:** {team_emoji(s, a['team'])}{pname(uid)} ({team_name(s, a['team'])}), "
                     f"{a['pts'] / max(1, a['gp']):.1f} PPG over "
                     f"{a['gp']} game{'s' if a['gp'] != 1 else ''}.")
    title = {"qual": f"📰 POWER RANKINGS · {tname} · after the qualifier",
             "final": f"📰 FINAL POWER RANKINGS · {tname}",
             "now": f"📰 POWER RANKINGS · {tname}"}[stage]
    if collect is not None:
        collect.update({"title": site_text(title.replace("📰 ", "")), "recap": [site_text(x) for x in recap],
                        "stage": stage, "tournament": tname,
                        "at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    e1 = brand_embed("\n".join(recap), title, GOLD)
    e2 = brand_embed("\n\n".join(out_lines), f"Top {min(PR_TOP, len(rows))}", BRAND)
    e2.set_footer(text="Automatic: record, point differential per game and strength of schedule"
                       + (" · final placement first" if final else "") + " · ▲▼ = change since the last rankings")
    return [e1, e2]


async def post_power_rankings(guild: discord.Guild, stage: str) -> str:
    data = load_data()
    s = guild_signups(data, guild.id)
    ev = s.get("event")
    if not ev:
        return "There's no tournament to rank."
    try:
        if await sync_team_emojis(guild):  # logos for teams that don't have one yet
            data = load_data()
            s = guild_signups(data, guild.id)
            ev = s.get("event")
    except Exception as ex:
        print(f"[team emoji] {ex}")
    web = {}
    embeds = power_rankings_embeds(guild, s, ev, stage, web)
    if not embeds:
        return "No results yet, so there's nothing to rank."
    c = media(s)["chans"]
    ch = guild.get_channel(c.get("rankings") or 0) or discord.utils.get(guild.text_channels, name="📰｜power-rankings") \
        or chan(guild, "power-rankings")
    if ch is None:
        return "There's no power rankings channel. Run `/setupbot part:media` first."
    await ch.send(embeds=embeds, allowed_mentions=NO_PINGS)
    rows = power_table(s, ev, stage == "final")
    s.setdefault("power_rankings", {})["last"] = [r["tid"] for r in rows[:PR_TOP]]
    s["power_rankings"]["latest"] = web  # the website's Media tab shows the same rankings
    if stage in ("qual", "final"):
        ev.setdefault("pr_posted", []).append(stage)
    save_data(data)
    schedule_publish(guild)
    return f"Power rankings posted in {ch.mention}."


async def auto_power_rankings(guild: discord.Guild):
    """After every result: post the rankings once when the qualifier ends and once when the champion is crowned."""
    s = guild_signups(load_data(), guild.id)
    ev = s.get("event") or {}
    done = ev.get("pr_posted") or []
    if (ev.get("main") or {}).get("champion"):
        if "final" not in done:
            await post_power_rankings(guild, "final")
    elif ev.get("stage") in ("groups_done", "swiss_done", "main") and (ev.get("groups") or ev.get("swiss")) \
            and "qual" not in done:
        await post_power_rankings(guild, "qual")


@app_commands.default_permissions(manage_messages=True)
async def powerrankings(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    await interaction.followup.send(await post_power_rankings(interaction.guild, "now"), ephemeral=True)


# ---------------------------------------------------------------- /game_score: both teams agree on the score
#
# A captain or co-captain reports: /game_score match:12 winner:@Team score:52-44 (+ the stats screenshot/export).
# The OTHER team's captain or co-captain gets a Confirm / Dispute card (in #score-reports and by DM).
# Confirm = the result is recorded (same as /result). Dispute = staff are told and an admin decides.
# Admins (Commissioner, Admin/Owner roles, Administrator permission) record it straight away: their report is
# an override and needs no confirmation. Staff/Referees can still use /result too.

def score_reports(s: dict) -> dict:
    return s.setdefault("score_reports", {})  # match id -> {winner, score, by, team, status, msgs, stats}


def team_side(s: dict, uid: int, m: dict) -> str | None:
    """The team key this user captains or co-captains in match m."""
    for tid in (m["a"], m["b"]):
        t = s["teams"].get(str(tid))
        if t and uid in (t.get("captain"), t.get("co")):
            return str(tid)
    return None


def report_card(s: dict, mid: str, rep_: dict) -> discord.Embed:
    win, lose = int(rep_["winner"]), int(rep_["loser"])
    status = {"pending": "⏳ Waiting for the other team to confirm",
              "confirmed": "✅ Confirmed by both teams. Result recorded.",
              "disputed": "⚠️ Disputed. An admin will decide.",
              "override": "🛡️ Recorded by an admin.",
              "rejected": "✖ Withdrawn"}[rep_["status"]]
    desc = (f"**{team_name(s, win)}** {rep_['score'].split('-')[0]} - {rep_['score'].split('-')[1]} "
            f"**{team_name(s, lose)}**\nWinner: **{team_name(s, win)}**\n\nReported by <@{rep_['by']}>"
            + (f" for **{team_name(s, rep_['team'])}**" if rep_.get("team") else "")
            + (f"\nConfirmed by <@{rep_['confirmed_by']}>" if rep_.get("confirmed_by") else "")
            + (f"\nDisputed by <@{rep_['disputed_by']}>" if rep_.get("disputed_by") else "")
            + f"\n\n**{status}**")
    e = brand_embed(desc, f"📝 Score report · M{mid}", GOOD if rep_["status"] in ("confirmed", "override")
                    else MUTED if rep_["status"] == "rejected" else 0xF59E0B if rep_["status"] == "disputed" else INFO)
    if rep_.get("stats"):
        e.set_image(url=rep_["stats"])
    return e


def report_view(gid: int, mid: str) -> discord.ui.View:
    v = discord.ui.View(timeout=None)
    v.add_item(discord.ui.Button(label="Confirm score", emoji="✅", style=discord.ButtonStyle.success,
                                 custom_id=f"gs:ok:{gid}:{mid}"))
    v.add_item(discord.ui.Button(label="Dispute", emoji="⚠️", style=discord.ButtonStyle.danger,
                                 custom_id=f"gs:no:{gid}:{mid}"))
    return v


async def refresh_report_msgs(guild: discord.Guild, s: dict, mid: str, rep_: dict, keep_buttons: bool):
    for ch_id, msg_id in rep_.get("msgs", []):
        try:
            ch = guild.get_channel(ch_id) or bot.get_channel(ch_id) or await bot.fetch_channel(ch_id)
            await ch.get_partial_message(msg_id).edit(embed=report_card(s, mid, rep_),
                                                      view=report_view(guild.id, mid) if keep_buttons else None)
        except (discord.HTTPException, AttributeError):
            pass


@bot.tree.command(name="game_score", description="Captains/co-captains: report a game's score. The other team confirms it.")
@app_commands.describe(match="Match number, e.g. 12 for M12", winner="The team that won",
                       score="Final score, winner's points first, e.g. 52-44",
                       stats="Stats screenshot (public gym) or the stats export (league gym)")
async def game_score(interaction: discord.Interaction, match: int, winner: discord.Role, score: str,
                     stats: discord.Attachment | None = None):
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    ev = s.get("event")
    pts = parse_score(score)
    if not pts or pts[0] == pts[1]:
        return await interaction.response.send_message("Give the score like 52-44 (winner's points first, no ties).",
                                                       ephemeral=True)
    if pts[0] < pts[1]:
        pts = (pts[1], pts[0])
    score_txt = f"{pts[0]}-{pts[1]}"
    m = next((x for x in open_matches(ev) if x["id"] == match), None)
    if m is None:
        return await interaction.response.send_message(f"M{match} isn't waiting on a result.", ephemeral=True)
    if winner.id not in (m["a"], m["b"]):
        return await interaction.response.send_message(f"{winner.mention} isn't playing in M{match}.", ephemeral=True,
                                                       allowed_mentions=NO_PINGS)
    admin = is_commissioner(user)
    side = team_side(s, user.id, m)
    if side is None and not admin:
        return await interaction.response.send_message(
            f"Only the captains and co-captains in M{match} can report its score.", ephemeral=True)
    loser = m["b"] if winner.id == m["a"] else m["a"]
    mid = str(match)
    old = score_reports(s).get(mid)
    if old and old["status"] == "pending" and not admin and old.get("team") == side:
        return await interaction.response.send_message(
            "You already reported this one. Waiting on the other team to confirm.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    rep_ = {"winner": winner.id, "loser": loser, "score": score_txt, "by": user.id, "team": side,
            "status": "override" if admin and side is None else "pending", "msgs": [],
            "stats": stats.url if stats and (stats.content_type or "").startswith("image/") else None,
            "file": stats.url if stats and not (stats.content_type or "").startswith("image/") else None,
            "at": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    if old and old.get("msgs") and old["status"] == "pending":  # a new report replaces the old one
        old["status"] = "rejected"
        await refresh_report_msgs(guild, s, mid, old, keep_buttons=False)
    score_reports(s)[mid] = rep_
    save_data(data)
    ch = chan(guild, "score-reports")
    if rep_["status"] == "override":  # admin: recorded right away
        if ch:
            msg = await ch.send(embed=report_card(s, mid, rep_), allowed_mentions=NO_PINGS)
            rep_["msgs"].append([ch.id, msg.id])
            if rep_["file"]:
                await ch.send(f"Stats export for M{mid}: {rep_['file']}", allowed_mentions=NO_PINGS)
        stat_note = await import_export_url(guild, match, rep_["file"])  # league gym: box score from the export
        ok, text = await record_result(guild, match, winner.id, score_txt, user.id)
        if stat_note:
            text += "\n" + stat_note
        data = load_data()
        score_reports(guild_signups(data, guild.id))[mid] = rep_
        save_data(data)
        return await interaction.followup.send(("🛡️ Admin override. " if ok else "") + text, ephemeral=True,
                                               allowed_mentions=NO_PINGS)
    other = str(m["b"] if side == str(m["a"]) else m["a"]) if side else str(loser)
    to_ping = captains_of(s, other)
    if ch:  # the record in #score-reports, no pings
        msg = await ch.send(embed=report_card(s, mid, rep_), view=report_view(guild.id, mid), allowed_mentions=NO_PINGS)
        rep_["msgs"].append([ch.id, msg.id])
        if rep_["file"]:
            await ch.send(f"Stats export for M{mid}: {rep_['file']}", allowed_mentions=NO_PINGS)
    team_ch = guild.get_channel(int(s["teams"].get(other, {}).get("channel") or 0))
    if team_ch:  # the other team's own channel: captains, check your DMs
        tmsg = await team_ch.send(
            content=" ".join(f"<@{u}>" for u in to_ping) or None,
            embed=brand_embed(f"**{team_name(s, side)}** reported the score for **M{mid}**: "
                              f"**{team_name(s, winner.id)}** won **{score_txt}**.\n\nCaptain / co-captain: check your "
                              "DMs to **confirm** it (or use the buttons here). Not right? Hit **Dispute**.",
                              f"📝 Confirm your score · M{mid}", GOLD),
            view=report_view(guild.id, mid),
            allowed_mentions=discord.AllowedMentions(users=True, roles=False, everyone=False))
        rep_["msgs"].append([team_ch.id, tmsg.id])
    for uid in to_ping:
        try:
            u = bot.get_user(uid) or await bot.fetch_user(uid)
            dmsg = await u.send(embed=report_card(s, mid, rep_), view=report_view(guild.id, mid))
            rep_["msgs"].append([dmsg.channel.id, dmsg.id])
        except (discord.HTTPException, AttributeError):
            pass
    save_data(data)
    await interaction.followup.send(f"Score sent: **{team_name(s, winner.id)}** won M{match} {score_txt}. "
                                    f"Waiting for **{team_name(s, other)}** to confirm.", ephemeral=True)


@bot.listen("on_interaction")
async def game_score_buttons(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return
    cid = (interaction.data or {}).get("custom_id", "")
    if not cid.startswith("gs:"):
        return
    _, action, gid, mid = cid.split(":", 3)
    guild = bot.get_guild(int(gid))
    if guild is None:
        return await interaction.response.send_message("I can't find that server any more.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    rep_ = score_reports(s).get(mid)
    if not rep_ or rep_["status"] != "pending":
        return await interaction.response.send_message("This score report is already settled.", ephemeral=True)
    member = guild.get_member(interaction.user.id)
    uid = interaction.user.id
    other_team = [str(rep_["winner"]), str(rep_["loser"])]
    other_team.remove(rep_["team"]) if rep_.get("team") in other_team else None
    allowed = any(uid in captains_of(s, k) for k in other_team) or (member is not None and is_commissioner(member))
    if not allowed:
        return await interaction.response.send_message(
            "Only the other team's captain or co-captain (or an admin) can answer this report.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    if action == "ok":
        stat_note = await import_export_url(guild, int(mid), rep_.get("file"))  # league gym: stats from the export
        ok, text = await record_result(guild, int(mid), int(rep_["winner"]), rep_["score"], rep_["by"])
        if stat_note:
            text += "\n" + stat_note
        data = load_data()
        s = guild_signups(data, guild.id)
        rep_ = score_reports(s)[mid]
        if ok:
            rep_["status"], rep_["confirmed_by"] = "confirmed", uid
        save_data(data)
        await refresh_report_msgs(guild, s, mid, rep_, keep_buttons=not ok)
        return await interaction.followup.send(("✅ Confirmed. " if ok else "Couldn't record it: ") + text,
                                               ephemeral=True, allowed_mentions=NO_PINGS)
    rep_["status"], rep_["disputed_by"] = "disputed", uid
    save_data(data)
    await refresh_report_msgs(guild, s, mid, rep_, keep_buttons=False)
    dch = chan(guild, "match-disputes") or chan(guild, "staff-chat")
    if dch:
        await dch.send(embed=brand_embed(
            f"<@{uid}> disputed the score report for **M{mid}**: {team_name(s, rep_['winner'])} won "
            f"{rep_['score']} (reported by <@{rep_['by']}>).\n\nAdmins: record the right result with "
            f"`/game_score match:{mid} winner:@Team score:..` (admin reports count straight away).",
            f"⚠️ Disputed score · M{mid}", 0xF59E0B), allowed_mentions=NO_PINGS)
    await interaction.followup.send("Disputed. An admin will look at it. Post your evidence in #match-disputes.",
                                    ephemeral=True)


# ---------------------------------------------------------------- /disqualify
#
# DURING a tournament: the team is out. Their unplayed games are forfeits (opponents go through).
#   rewind: pick one of their wins. The team they beat in that game is reinstated and takes the disqualified
#   team's place in the bracket from there (main draw / consolation). In groups and Swiss, every win of theirs
#   from that round on is flipped to their opponent.
# AFTER a tournament (or not in the current one): their RISER POINTS are halved and any Major spot is removed.
# 2+ players caught cheating on the same team: their RISER POINTS go to 0 (during or after).
# Always shows a preview first; add confirm:True to do it.

def dq_wins(ev: dict | None, tid: int) -> list[dict]:
    """Every game this team won (on the court, not by forfeit) in the current event, in play order."""
    out = []
    for part in ("playin", "groups", "swiss", "main", "consolation"):
        for m in ((ev or {}).get(part) or {}).get("matches", []):
            if m.get("winner") != tid or tid not in (m.get("a"), m.get("b")) or m.get("forfeit"):
                continue
            if part == "main" and m.get("loser") is None:
                continue  # a bye
            out.append(dict(m, part=part))
    return out


def dq_rewind_label(s: dict, ev: dict, m: dict, tid: int) -> str:
    other = m["b"] if m["a"] == tid else m["a"]
    where = match_heading(ev, m)
    if m["part"] in ("main", "consolation"):
        return f"M{m['id']} · {where}: reinstate {team_name(s, other)}"[:100]
    return f"M{m['id']} · {where}: flip their wins from here (beat {team_name(s, other)})"[:100]


def dq_apply_event(s: dict, ev: dict, tid: int, rewind: int | None) -> list[str]:
    """Take the team out of the running event. Returns lines describing what happened."""
    lines = []
    ev.setdefault("dq", [])
    if tid not in ev["dq"]:
        ev["dq"].append(tid)
    nm = lambda t: f"**{team_name(s, t)}**"
    r_match = None
    if rewind:
        r_match = next((m for m in dq_wins(ev, tid) if m["id"] == rewind), None)
    # groups
    gs = ev.get("groups")
    if gs:
        from_round = r_match["round"] if r_match and r_match["part"] == "groups" else None
        for m in gs["matches"]:
            if tid not in (m["a"], m["b"]):
                continue
            other = m["b"] if m["a"] == tid else m["a"]
            if not m["winner"]:
                m.update(winner=other, score="FF", pts=None, forfeit=True)
                lines.append(f"M{m['id']}: {nm(other)} win by forfeit.")
            elif m["winner"] == tid and from_round and m["round"] >= from_round:
                m.update(winner=other, score="FF", pts=None, forfeit=True)
                lines.append(f"M{m['id']}: result flipped, {nm(other)} get the win.")
        if groups_finished(gs) and ev["stage"] in ("groups", "groups_done"):
            ev["stage"] = "groups_done"
            gs["qualified"] = []
            for gi in range(len(gs["groups"])):
                order, _st = group_table(gs, gi)
                gs["qualified"] += [t for t in order if t not in ev["dq"]][:gs["advance"]]
    # swiss
    sw = ev.get("swiss")
    if sw and str(tid) in sw["rec"]:
        from_round = r_match["round"] if r_match and r_match["part"] == "swiss" else None
        rec = sw["rec"]
        for m in sw["matches"]:
            if tid not in (m["a"], m["b"]) or m.get("b") is None:
                continue
            other = m["b"] if m["a"] == tid else m["a"]
            if not m["winner"]:
                m.update(winner=other, score="FF", forfeit=True)
                swiss_record(sw, other, tid)
                lines.append(f"M{m['id']}: {nm(other)} win by forfeit.")
            elif m["winner"] == tid and from_round and m["round"] >= from_round:
                m.update(winner=other, score="FF", forfeit=True)
                rec[str(tid)]["w"] -= 1
                rec[str(tid)]["l"] += 1
                rec[str(other)]["w"] += 1
                rec[str(other)]["l"] -= 1
                if other in sw["eliminated"] and rec[str(other)]["l"] < sw["losses"]:
                    sw["eliminated"].remove(other)
                if rec[str(other)]["w"] >= sw["wins"] and other not in sw["qualified"]:
                    sw["qualified"].append(other)
                lines.append(f"M{m['id']}: result flipped, {nm(other)} get the win.")
        if tid in sw["qualified"]:
            sw["qualified"].remove(tid)
        rec[str(tid)]["l"] = max(rec[str(tid)]["l"], sw["losses"])
        if tid not in sw["eliminated"]:
            sw["eliminated"].append(tid)
    # main draw (double elimination)
    main = ev.get("main")
    if main and any(tid in (m["a"], m["b"]) for m in main["matches"]):
        x = (r_match["b"] if r_match["a"] == tid else r_match["a"]) if r_match and r_match["part"] == "main" else None
        if x:  # the team they beat takes their place from here on
            for m in main["matches"]:
                if m["done"]:
                    continue
                for side in ("a", "b"):
                    if m[side + "_ok"] and m[side] == x:
                        m[side] = None  # leave their other spot (that opponent goes through)
            for m in main["matches"]:
                if not m["done"]:
                    for side in ("a", "b"):
                        if m[side + "_ok"] and m[side] == tid:
                            m[side] = x
            lines.append(f"{nm(x)} are reinstated in {nm(tid)}'s place in the main draw.")
        else:
            for m in main["matches"]:
                if not m["done"]:
                    for side in ("a", "b"):
                        if m[side + "_ok"] and m[side] == tid:
                            m[side] = None
            lines.append(f"{nm(tid)}'s remaining main-draw games are forfeits.")
        de_resolve(main)
        if main.get("champion"):
            lines.append(f"🏆 That leaves {nm(main['champion'])} as champions.")
    # consolation
    cons = ev.get("consolation")
    if cons:
        x = (r_match["b"] if r_match["a"] == tid else r_match["a"]) if r_match and r_match["part"] == "consolation" else None
        for m in cons["matches"]:
            if m["winner"] or tid not in (m["a"], m["b"]):
                continue
            side = "a" if m["a"] == tid else "b"
            if x:
                m[side] = x
                lines.append(f"{nm(x)} are reinstated in the consolation bracket (M{m['id']}).")
                x = None
                continue
            other = m["b"] if side == "a" else m["a"]
            m[side] = None
            m["forfeit"] = True
            if other is not None:
                cons_advance(cons, m, other)
                lines.append(f"M{m['id']}: {nm(other)} go through by forfeit.")
    return lines


async def dq_rewind_choices(interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
    team = getattr(interaction.namespace, "team", None)
    tid = getattr(team, "id", None)
    out = [app_commands.Choice(name="No rewind: just forfeit their remaining games", value="none")]
    if not tid:
        return out
    s = guild_signups(load_data(), interaction.guild.id)
    ev = s.get("event")
    for m in dq_wins(ev, tid)[-24:]:
        lab = dq_rewind_label(s, ev, m, tid)
        if not current or current.lower() in lab.lower():
            out.append(app_commands.Choice(name=lab, value=str(m["id"])))
    return out[:25]


@bot.tree.command(description="Staff: disqualify a team for cheating (during a tournament or after one).")
@app_commands.describe(team="The team to disqualify", reason="What happened (shown in the announcement)",
                       cheaters="How many of their players were caught (2+ = their RISER POINTS go to 0)",
                       rewind="During a tournament: which win of theirs to rewind to (see the list)",
                       confirm="Leave off to see a preview first. True = do it.")
@app_commands.autocomplete(rewind=dq_rewind_choices)
@app_commands.default_permissions(manage_roles=True)
async def disqualify(interaction: discord.Interaction, team: discord.Role, reason: str,
                     cheaters: app_commands.Range[int, 1, 8] = 1, rewind: str | None = None, confirm: bool = False):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can disqualify teams.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    key = str(team.id)
    t = s["teams"].get(key)
    if t is None:
        return await interaction.response.send_message(f"{team.mention} isn't a league team.", ephemeral=True,
                                                       allowed_mentions=NO_PINGS)
    ev = s.get("event")
    tz = s.get("tourney") or {}
    in_event = bool(ev and ev.get("stage") not in (None, "done") and
                    any(team.id in (m.get("a"), m.get("b")) for m in all_matches(ev))
                    and team.id not in (ev.get("dq") or []))
    rw = int(rewind) if rewind and rewind.isdigit() else None
    if rw and in_event and rw not in [m["id"] for m in dq_wins(ev, team.id)]:
        return await interaction.response.send_message("That rewind point isn't one of their wins. Pick one from "
                                                       "the list.", ephemeral=True)
    old_pts = t.get("points", 0)
    if cheaters >= 2:
        new_pts, pts_txt = 0, f"RISER POINTS: {old_pts} → **0** ({cheaters} players caught)"
    elif in_event:
        new_pts, pts_txt = old_pts, "No points from this tournament."
    else:
        new_pts, pts_txt = old_pts // 2, f"RISER POINTS halved: {old_pts} → **{old_pts // 2}**"
    major = key in circuit(s)["qualified"] and not in_event
    what = (f"**During {tz.get('name', 'the tournament')}:** {t['name']} are removed. Their unplayed games are "
            "forfeits." + (f" Rewind to M{rw}: " + dq_rewind_label(s, ev, next(m for m in dq_wins(ev, team.id)
                                                                               if m["id"] == rw), team.id).split(": ", 1)[1]
                           if rw else "") if in_event else
            "**After the tournament:** no bracket changes.") + f"\n{pts_txt}" + ("\nTheir **Major spot is removed**."
                                                                                 if major else "")
    if not confirm:
        return await interaction.response.send_message(
            embed=brand_embed(f"**Team:** {team.mention}\n**Reason:** {reason}\n\n{what}\n\n"
                              "Run the same command with `confirm:True` to do it.", "🚫 Disqualify: preview",
                              0xF59E0B), ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    lines = []
    if in_event:
        lines = dq_apply_event(s, ev, team.id, rw)
    t["points"] = new_pts
    if major:
        circuit(s)["qualified"].remove(key)
    s.setdefault("dq_log", []).append({"team": key, "name": t["name"], "reason": reason[:300], "cheaters": cheaters,
                                       "during": in_event, "tournament": tz.get("name"), "by": interaction.user.id,
                                       "points_before": old_pts, "points_after": new_pts,
                                       "at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    save_data(data)
    text = (f"**{t['name']}** have been **disqualified**" + (f" from **{tz.get('name')}**" if in_event else "")
            + f" for cheating.\n**Reason:** {reason}\n{pts_txt}" + ("\nTheir Major spot has been removed." if major else ""))
    if lines:
        text += "\n\n" + "\n".join(lines[:15])
    for chname in ("announcements",) + (("bracket",) if in_event else ()):
        ch = chan(guild, chname)
        if ch:
            await post(ch, text, title="🚫 Disqualification", color=0xEF4444)
    team_ch = guild.get_channel(int(t.get("channel") or 0))
    if team_ch:
        await post(team_ch, text, title="🚫 Your team has been disqualified", color=0xEF4444)
    log = chan(guild, "mod-log")
    if log:
        await post(log, text + f"\n\nBy {interaction.user.mention}", title="🚫 Disqualification", color=0xEF4444)
    if in_event:
        try:
            await post_bracket_update(guild, s, ev)
        except Exception as e:
            print(f"[dq bracket] {e}")
        try:
            await match_watch_once(guild)  # opponents' next games open / DMs go out
        except Exception as e:
            print(f"[dq matches] {e}")
    await update_board(guild, data)
    await interaction.followup.send(f"Done. **{t['name']}** disqualified." + (f" {len(lines)} bracket change(s)."
                                                                             if lines else ""), ephemeral=True)


@bot.tree.command(description="List the matches waiting to be played.")
async def matches(interaction: discord.Interaction):
    ev = guild_signups(load_data(), interaction.guild.id)["event"]
    stage = ev["stage"] if ev else None
    lines = []
    if stage == "swiss":
        sw = ev["swiss"]
        lines = [f"Swiss round {sw['round']}:"] + [
            f"M{m['id']}: {tag(m['a'])} vs {tag(m['b'])}" for m in sw["matches"] if not m["winner"]]
    elif stage == "groups":
        lines = ["Group stage:"] + [
            f"M{m['id']} (Group {group_letter(m['group'])}, round {m['round']}): {tag(m['a'])} vs {tag(m['b'])}"
            for m in ev["groups"]["matches"] if not m["winner"]]
    elif stage == "main":
        lines = ["Main draw:"] + [f"M{m['id']} ({m['label']}): {tag(m['a'])} vs {tag(m['b'])}"
                                  for m in de_ready(ev["main"])]
    elif stage in ("swiss_done", "groups_done"):
        lines = ["The qualifier is done. Staff need to run /startmain.", ""]
    if ev and cons_ready(ev.get("consolation")):
        lines = (lines if len(lines) > 1 else []) + ["Consolation:"] + [
            f"M{m['id']} ({m['label']}): {tag(m['a'])} vs {tag(m['b'])}" for m in cons_ready(ev["consolation"])]
    if len(lines) <= 1:
        lines = ["No matches are waiting right now."]
    await interaction.response.send_message("\n".join(lines).strip()[:1990], ephemeral=True,
                                            allowed_mentions=NO_PINGS)


@bot.tree.command(description="Delete the current tournament so you can start again.")
@app_commands.describe(confirm="Set to True to confirm. This can't be undone.")
@app_commands.default_permissions(manage_roles=True)
async def resetevent(interaction: discord.Interaction, confirm: bool = False):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can reset the tournament.", ephemeral=True)
    if not confirm:
        return await interaction.response.send_message(
            "This deletes every result in the current tournament. Run /resetevent confirm:True to do it.",
            ephemeral=True)
    info = _show_tasks.get(interaction.guild.id)
    if info and not info["task"].done():
        info["task"].cancel()  # a live draw was running: stop it too
    data = load_data()
    guild_signups(data, interaction.guild.id)["event"] = None
    save_data(data)
    schedule_publish(interaction.guild)
    await interaction.response.send_message(
        "Tournament cleared. Start again with /startswiss, /startgroups or /startmain.", ephemeral=True)



# ---------------------------------------------------------------- /replaceteam: swap a team out of the tournament
#
# A team drops out (or is removed) and another takes its place: the new team inherits the old team's spot, seed,
# group, record and bracket position. Games already played stay on the books (the old team's players keep their
# own stats). Games still to play are re-opened for scheduling, so the new team's captains get the DMs.

_SKIP_KEYS = {"box", "msgs", "card", "final_post", "analysis_post", "announce", "live_msg", "by", "from", "to",
              "stream", "host", "reporter", "confirmed_by", "disputed_by"}


def swap_team_ids(obj, old: int, new: int, key: str | None = None):
    """Replace a team id everywhere in the tournament data (ints, strings and dict keys), but never inside
    box scores or message/user references."""
    if key in _SKIP_KEYS:
        return obj
    if isinstance(obj, dict):
        return {(str(new) if k == str(old) else new if k == old else k): swap_team_ids(v, old, new, k)
                for k, v in obj.items()}
    if isinstance(obj, list):
        return [swap_team_ids(v, old, new, key) for v in obj]
    if obj == old and isinstance(obj, int) and not isinstance(obj, bool):
        return new
    if obj == str(old):
        return str(new)
    return obj


@bot.tree.command(description="Staff: replace a team in the tournament. The new team takes its spot, seed and record.")
@app_commands.describe(old="The team leaving the tournament", new="The team taking its place",
                       reason="Why (posted with the announcement)", ignore_roster="Allow a new team without 5 players",
                       confirm="Set True to do it (without it you see a preview)")
@app_commands.default_permissions(manage_roles=True)
async def replaceteam(interaction: discord.Interaction, old: discord.Role, new: discord.Role,
                      reason: str | None = None, ignore_roster: bool = False, confirm: bool = False):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can replace teams.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    tz = s.get("tourney") or {}
    ev = s.get("event")
    ko, kn = str(old.id), str(new.id)
    problem = None
    if not tz:
        problem = "There's no tournament right now."
    elif ko not in tz.get("entrants", []):
        problem = f"{old.mention} isn't in **{tz.get('name', 'the tournament')}**."
    elif kn not in s["teams"]:
        problem = f"{new.mention} isn't a league team."
    elif kn in tz.get("entrants", []):
        problem = f"{new.mention} is already in the tournament."
    elif not is_complete(s["teams"][kn]) and not ignore_roster:
        problem = f"{new.mention} doesn't have a full roster. Add `ignore_roster:True` to use them anyway."
    elif ev and (ev.get("main") or {}).get("champion"):
        problem = "The tournament is already over."
    elif ev and old.id in (ev.get("dq") or []):
        problem = f"{old.mention} were disqualified. Their spot can't be handed on."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True, allowed_mentions=NO_PINGS)
    on, nn = s["teams"][ko]["name"] if ko in s["teams"] else old.name, s["teams"][kn]["name"]
    if ev:
        rec = {r["tid"]: r for r in power_table(s, ev)}.get(old.id)
        stage_txt = STAGE_TXT.get(ev.get("stage"), ev.get("stage") or "the draw")
        inherit = f" They inherit {on}'s **{rec['w']}-{rec['l']}** record and spot." if rec else \
            f" They take {on}'s spot in {stage_txt}."
    else:
        inherit = " The draw hasn't happened yet, so they simply take the place in the entries."
    if not confirm:
        return await interaction.response.send_message(
            f"**Preview:** **{nn}** replace **{on}** in **{tz.get('name')}**.{inherit}\n"
            "Games already played stay as they are; games still to play are re-opened so the new team's captains "
            "can schedule them.\n\nRun it again with `confirm:True` to do it.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    tz["entrants"] = [kn if k == ko else k for k in tz["entrants"]]
    reopened = 0
    if ev:
        s["event"] = ev = swap_team_ids(ev, old.id, new.id)
        sc = sched(s)
        for mid, e_ in list(sc["matches"].items()):
            if e_.get("done"):
                continue
            if str(e_.get("a")) == ko or str(e_.get("b")) == ko:
                sc["matches"].pop(mid)  # the match watcher re-opens it with the new team (fresh DMs + deadline)
                reopened += 1
        for r in sc["requests"].values():
            if r["status"] == "open" and ko in (str(r.get("from_team")), str(r.get("to_team"))):
                r["status"] = "closed"
    s.setdefault("replacements", []).append({"tournament": tz.get("name"), "old": ko, "new": kn, "reason": reason,
                                            "by": interaction.user.id,
                                            "at": datetime.now(timezone.utc).isoformat(timespec="seconds")})
    save_data(data)
    text = (f"**{nn}** replace **{on}** in **{tz.get('name')}**.{inherit}"
            + (f"\n**Reason:** {reason}" if reason else ""))
    ann = chan(guild, "announcements")
    if ann:
        await post(ann, text, title="🔁 Team replaced", color=INFO)
    for k, msg_ in ((kn, f"You're in! **{nn}** take **{on}**'s place in **{tz.get('name')}**.{inherit}\n"
                         "Check your DMs: captains get your next game to schedule."),
                    (ko, f"**{on}** have been replaced in **{tz.get('name')}** by **{nn}**."
                         + (f"\n**Reason:** {reason}" if reason else ""))):
        tc = guild.get_channel(int(s["teams"].get(k, {}).get("channel") or 0))
        if tc:
            await post(tc, msg_, title="🔁 Tournament update", color=INFO)
    log = chan(guild, "mod-log")
    if log:
        await post(log, text + f"\nBy {interaction.user.mention}", title="🔁 Team replaced", color=INFO)
    try:
        await match_watch_once(guild)  # re-open their games right away
    except Exception as e:
        print(f"[replace team] {e}")
    try:
        await refresh_registered(guild, load_data())
    except Exception:
        pass
    await update_board(guild)
    if ev and ev.get("main"):
        try:
            s2 = guild_signups(load_data(), guild.id)
            await post_bracket_update(guild, s2, s2["event"])
        except Exception as e:
            print(f"[replace bracket] {e}")
    await interaction.followup.send(f"Done: **{nn}** replaced **{on}**."
                                    + (f" {reopened} game(s) re-opened for scheduling." if reopened else ""),
                                    ephemeral=True)


STAGE_TXT = {"groups": "the group stage", "swiss": "the Swiss stage", "main": "the main draw",
             "groups_done": "the qualifier", "swiss_done": "the qualifier"}


# ---------------------------------------------------------------- combined commands
#
# Several small commands were folded into these (Discord allows 100 slash commands). The old functions below
# still do the work; these just pick the right one.

@bot.tree.command(name="refresh", description="Staff: redo a board now: rosters, stat leaders, logos, group schedule, power rankings.")
@app_commands.describe(what="What to refresh")
@app_commands.choices(what=[app_commands.Choice(name="Team cards in #rosters", value="rosters"),
                            app_commands.Choice(name="Stat leaders", value="leaders"),
                            app_commands.Choice(name="Team logo emojis (and why a team has none)", value="emojis"),
                            app_commands.Choice(name="Group stage schedule in #schedule", value="schedule"),
                            app_commands.Choice(name="Post the power rankings now", value="rankings")])
@app_commands.default_permissions(manage_messages=True)
async def refresh_cmd(interaction: discord.Interaction, what: str):
    if what == "rosters":
        return await rosterboard(interaction)
    if what == "leaders":
        return await statleaders(interaction)
    if what == "emojis":
        return await teamemojis(interaction)
    if what == "schedule":
        return await refreshschedule(interaction, True)
    return await powerrankings(interaction)


@bot.tree.command(name="position", description="Set the position you play. Staff: set anyone's with the player option.")
@app_commands.describe(position="The position", player="Staff only: whose position to change")
@app_commands.choices(position=[app_commands.Choice(name=n, value=v) for v, n in POSITIONS])
async def position_cmd(interaction: discord.Interaction, position: str, player: discord.Member | None = None):
    if player is not None and player.id != interaction.user.id:
        return await setposition(interaction, player, position)
    return await globals()["position"](interaction, position)  # the parameter hides the function's name


@bot.tree.command(name="ticket", description="Tickets: add or remove someone (staff), or close this ticket.")
@app_commands.describe(action="What to do", member="Who to add or remove", reason="Why it's being closed (optional)")
@app_commands.choices(action=[app_commands.Choice(name="Close this ticket", value="close"),
                              app_commands.Choice(name="Add someone (staff)", value="add"),
                              app_commands.Choice(name="Remove someone (staff)", value="remove")])
async def ticket_cmd(interaction: discord.Interaction, action: str, member: discord.Member | None = None,
                     reason: str | None = None):
    if action == "close":
        return await ticketclose(interaction, reason)
    if member is None:
        return await interaction.response.send_message("Pick the `member` to add or remove.", ephemeral=True)
    return await (ticketadd if action == "add" else ticketremove)(interaction, member)


@bot.tree.command(name="suspensions", description="Staff: current suspensions, one player's history, or lift one early.")
@app_commands.describe(member="A player (their history)", lift="Lift this player's suspension early")
@app_commands.default_permissions(moderate_members=True)
async def suspensions_cmd(interaction: discord.Interaction, member: discord.Member | None = None, lift: bool = False):
    if lift:
        if member is None:
            return await interaction.response.send_message("Pick the `member` whose suspension to lift.", ephemeral=True)
        return await unsuspend(interaction, member)
    return await suspensions(interaction, member)


@bot.tree.command(name="invites", description="See how many people someone invited, or the top inviters.")
@app_commands.describe(member="Whose invites (leave empty for your own)", top="Show the top inviters instead")
async def invites_cmd(interaction: discord.Interaction, member: discord.Member | None = None, top: bool = False):
    return await (inviteleaderboard(interaction) if top else invites(interaction, member))


@bot.tree.command(name="setpoints", description="Staff: set a team's RISER POINTS, or reset everyone's to 0.")
@app_commands.describe(team="The team", points="Their new RISER POINTS",
                       reset_all="Reset EVERY team's RISER POINTS and Major spots to 0", confirm="Needed with reset_all")
@app_commands.default_permissions(manage_roles=True)
async def setpoints_cmd(interaction: discord.Interaction, team: discord.Role | None = None,
                        points: app_commands.Range[int, 0, 100000] | None = None, reset_all: bool = False,
                        confirm: bool = False):
    if reset_all:
        return await resetpoints(interaction, confirm)
    if team is None or points is None:
        return await interaction.response.send_message("Pick the `team` and its `points` (or use `reset_all`).",
                                                       ephemeral=True)
    return await setpoints(interaction, team, points)


@bot.tree.command(name="tournament", description="Staff: change the tournament's close time, logo, Major spot, or the Major target.")
@app_commands.describe(closes="When entries close, e.g. 'Friday at 1 PM EST'", logo="A new tournament logo",
                       winner_qualifies="Does the winner get a Major spot?",
                       major_target="RISER POINTS needed to qualify for the Major",
                       remind="With closes: DM captains of full teams that haven't registered (default yes)")
@app_commands.default_permissions(manage_roles=True)
async def tournament_cmd(interaction: discord.Interaction, closes: str | None = None,
                         logo: discord.Attachment | None = None, winner_qualifies: bool | None = None,
                         major_target: app_commands.Range[int, 0, 100000] | None = None, remind: bool = True):
    picked = [x for x in (closes, logo, winner_qualifies, major_target) if x is not None]
    if len(picked) != 1:
        return await interaction.response.send_message("Change one thing at a time: `closes`, `logo`, "
                                                       "`winner_qualifies` or `major_target`.", ephemeral=True)
    if closes is not None:
        return await setcloses(interaction, closes, remind)
    if logo is not None:
        return await tournamentlogo(interaction, logo)
    if winner_qualifies is not None:
        return await majorspot(interaction, winner_qualifies)
    return await setmajor(interaction, major_target)


@bot.tree.command(name="pickupstats", description="Upload a pickup's stats sheet (CSV), or leave the file empty to get the sheet.")
@app_commands.describe(match="Pickup number", file="The filled-in sheet (CSV). Leave empty to get a blank sheet.")
async def pickupstats_cmd(interaction: discord.Interaction, match: int, file: discord.Attachment | None = None):
    return await (pickupstats(interaction, match, file) if file else pickuptemplate(interaction, match))


@bot.tree.command(name="setrr", description="Staff: set a player's pickup RR, or start a new pickup season.")
@app_commands.describe(player="The player", rr="Their new RR", reset_all="New season: everyone back to the starting RR",
                       confirm="Needed with reset_all")
@app_commands.default_permissions(manage_roles=True)
async def setrr_cmd(interaction: discord.Interaction, player: discord.Member | None = None,
                    rr: app_commands.Range[int, 0, 10000] | None = None, reset_all: bool = False, confirm: bool = False):
    if reset_all:
        return await resetrr(interaction, confirm)
    if player is None or rr is None:
        return await interaction.response.send_message("Pick the `player` and their `rr` (or use `reset_all`).",
                                                       ephemeral=True)
    return await setrr(interaction, player, rr)


@bot.tree.command(name="importstats", description="Referees/staff: upload a match's stats (JSON export or CSV). No file = get a blank sheet.")
@app_commands.describe(match="Match number, e.g. 7 for M7", file="The game's stats export (.json) or a sheet (.csv)",
                       home="JSON only, if needed: the team that was Home in the export")
async def importstats_cmd(interaction: discord.Interaction, match: int, file: discord.Attachment | None = None,
                          home: discord.Role | None = None):
    return await (importstats(interaction, match, file, home) if file else statstemplate(interaction, match))


@bot.tree.command(name="cleartest", description="Staff: delete test posts: a practice tournament's, or practice draws.")
@app_commands.describe(what="What to delete")
@app_commands.choices(what=[app_commands.Choice(name="Practice tournament posts (/testtournament)", value="tournament"),
                            app_commands.Choice(name="The last practice draw (/testdraw)", value="draw"),
                            app_commands.Choice(name="Every practice draw", value="draws")])
@app_commands.default_permissions(manage_roles=True)
async def cleartest_cmd(interaction: discord.Interaction, what: str = "tournament"):
    if what == "tournament":
        return await cleartest(interaction)
    return await deletetestdraw(interaction, what == "draws")


@bot.tree.command(name="champion", description="Staff: add or fix a champion in the champions list, or remove one.")
@app_commands.describe(action="Add/fix or remove", tournament="Add: the tournament's name", team="Add: the winning team",
                       logo="Add: the tournament logo (optional)", give_roles_to_roster="Add: give the winner roles (default yes)",
                       number="Remove: its number in the champions list")
@app_commands.choices(action=[app_commands.Choice(name="Add or fix", value="add"),
                              app_commands.Choice(name="Remove", value="remove")])
@app_commands.default_permissions(manage_roles=True)
async def champion_cmd(interaction: discord.Interaction, action: str, tournament: str | None = None,
                       team: discord.Role | None = None, logo: discord.Attachment | None = None,
                       give_roles_to_roster: bool = True, number: int | None = None):
    if action == "remove":
        if number is None:
            return await interaction.response.send_message("Give the `number` to remove.", ephemeral=True)
        return await removechampion(interaction, number)
    if not tournament or team is None:
        return await interaction.response.send_message("Give the `tournament` name and the `team`.", ephemeral=True)
    return await addchampion(interaction, tournament, team, logo, give_roles_to_roster)


@bot.tree.command(name="giverole", description="Staff: give or take Media, Streamer or Pickup Host.")
@app_commands.describe(role="Which role", member="Who", remove="Take it away instead")
@app_commands.choices(role=[app_commands.Choice(name="Media", value="Media"),
                            app_commands.Choice(name="Streamer", value="Streamer"),
                            app_commands.Choice(name="Pickup Host", value="pickup")])
@app_commands.default_permissions(manage_roles=True)
async def giverole_cmd(interaction: discord.Interaction, role: str, member: discord.Member, remove: bool = False):
    if role == "pickup":
        return await pickuphost(interaction, member, remove)
    return await mediarole(interaction, member, role, remove)


@bot.tree.command(name="captain", description="Captains: hand over the captaincy, or add/remove a co-captain (staff: any team).")
@app_commands.describe(player="The teammate", role="Make them captain or co-captain",
                       remove="Co-captain only: take it away", team="Staff only: which team")
@app_commands.choices(role=[app_commands.Choice(name="Co-captain", value="co"),
                            app_commands.Choice(name="Captain (you stop being captain)", value="captain")])
async def captain_cmd(interaction: discord.Interaction, player: discord.Member, role: str = "co", remove: bool = False,
                      team: discord.Role | None = None):
    if role == "captain":
        return await makecaptain(interaction, player)
    return await cocaptain(interaction, player, remove, team)


def only_one_copy():
    """Stop if the bot is already running on this computer. Two copies answer the same command,
    and Discord rejects the second answer with 'Unknown interaction' (error 10062)."""
    import socket
    lock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        lock.bind(("127.0.0.1", 47321))
    except OSError:
        raise SystemExit("The bot is already running in another window. Close that window (or press Ctrl+C "
                         "in it) before starting it again.")
    return lock  # keep it open for as long as the bot runs


if __name__ == "__main__":
    _lock = only_one_copy()
    if not TOKEN:
        raise SystemExit("Set the DISCORD_TOKEN environment variable first (see the steps at the top of this file).")
    try:
        bot.run(TOKEN)
    except discord.PrivilegedIntentsRequired:
        raise SystemExit("Turn on 'Server Members Intent': Discord Developer Portal -> your app -> Bot -> "
                         "Privileged Gateway Intents -> Server Members Intent -> Save. Then start the bot again.")
