"""
ON THE RISE: PB CIRCUIT bot
===========================

Builds the circuit's Discord server, runs teams and tournaments, tracks RISER POINTS,
and keeps the circuit website up to date.

Slash commands
  Players and captains
  /signup team_name logo         Anyone: start a team (logo required). You become captain.
  /sign @player                  Captains: offer a spot. They Accept / Decline in DMs
                                 (or in #free-agents if their DMs are closed). 5 to 8 per team, one team each.
  /release, /makecaptain         Captains: release a player / hand over the captaincy
  /register, /unregister         Captains: enter (or leave) the tournament that's taking entries.
                                 Shows your RISER POINTS and how many you still need for the Major.
  /leaveteam                     Players: leave your team (not while a tournament is being played)
  /disbandteam confirm:True      Captains: delete your team (not during a tournament)
  /teaminfo [team], /points      Team card / RISER POINTS standings
  /freeagent [position]          Turn the Free Agent role on or off
  /position                      Set your position: PG, SG, SF, PF or C. Required to create a team (/signup asks
                                 for it), accept a team's offer, become a free agent, or join the pickup queue.
                                 Positions show on rosters, team cards, pickup cards, the draft menu and website.

  RISER POINTS
  - Each circuit event gives points by placement (set per tournament in /opensignups).
  - Tournament winners qualify for the Major automatically (staff can turn that off per tournament with the
    winner_qualifies option or /majorspot); others need the target set with /setmajor.
  - If fewer than 3 of the players who earned a team's points are still on it, the points are lost.
  - When a Major finishes, everyone's points reset to 0.

  Staff
  /setup                         Build roles, channels, permissions, rules + welcome posts (safe to run again)
  /giveplayerrole                Give the Player role to everyone already in the server
                                 (new members get it automatically when they join)
  /setmajor points_needed        RISER POINTS needed to qualify for the Major
  /opensignups name logo [kind] [points] [closes]   (the tournament logo is required)
  /tournamentlogo logo          Staff: change the current tournament logo
  /majorspot winner_qualifies   Staff: does this tournament's winner get an automatic Major spot? (yes/no)
                                 Open entries for a tournament. kind = Circuit event or Major.
                                 points = placement table, e.g. "1:100, 2:70, 3:50, 4:40, 5-6:25, 7-8:15"
  /closesignups                  Close entries (needs 6+ complete teams)
  /payout place_1:… place_2:… place_5_6:…   Set the RISER POINTS for each finishing position
                                 (1st, 2nd, 3rd, 4th, 5th-6th, 7th-8th, 9th-12th, 13th-16th, 17th-24th, 25th-32nd,
                                 33rd-48th, 49th-64th). Only fill in the ones you want to change. Applies to the
                                 current tournament and is saved for future ones.
  /setpoints team points, /resetpoints confirm:True
  /setlogo team logo, /addteam, /removeteam, and /sign and /release with a team option
  /signuplist, /rosterboard      Registered teams / re-send the team cards in #rosters
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
  /pickupsetup [players] [start_rr] [teams]
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
                                sheet with /pickuptemplate). Best player in the game: +32 win / -10 loss; worst:
                                +10 / -32. Until stats are in, everyone gets ±21, adjusted when stats arrive.
                                Great game (top of the lobby, winning team): gains x2. Win streaks: 3 x1.25,
                                4 x1.5, 5 x1.75, 6 x2, 7 x2.5, 8-9 x3, 10+ x4 (stack with great games), so big
                                wins go well past +32 (up to +256) and give double or triple rank-ups.
                                New players play 3 placement games (unranked, count 4x) and get placed between
                                Silver 1 and Platinum 3.
  /rank [player], /leaderboard  Rank card / top 20 by RR
  /pickupresult, /setrr, /resetrr confirm:True   Staff tools

  Moderation and welcome
  /modsetup [welcome_message]   Staff: make 👋｜welcome (greets every new member with a welcome card),
                                ⛔｜suspensions (public log) and 📥｜join-log (staff only: joins/leaves with
                                account age, flags accounts under 7 days old and people rejoining while suspended)
  /suspend member reason tournaments | length [scope]
                                tournaments: sit out 1-10 tournaments (the one taking sign-ups or being played
                                counts first; counts down when a champion is crowned). Can't create, join or be
                                signed to a team, register or free-agent until it's served.
                                Or length: 30m, 12h, 3d, 1w, 2d12h or perm. scope: Ranked queue / League (queue,
                                teams, tournaments) / Server timeout + league. Posts in ⛔｜suspensions, DMs the
                                player, gives the Suspended role, and lifts itself when time is up.
  /unsuspend member, /suspensions [member]   Lift early / list current ones or a player's history

  Media
  /mediasetup                   Staff: MEDIA category: media-info (Stream Pings + Apply buttons), stat-leaders
                                (auto-updated every 30 min), live-now, media-shows, power-rankings, highlights,
                                edits-and-gfx, media-chat, and a Media Booth voice channel. Roles Media,
                                Streamer, Stream Pings.
  /golive link [title]          Media/Streamer: post a LIVE card that pings Stream Pings
  /statleaders                  Refresh the stat leaders now
  /mediarole member kind [remove]   Staff: give or take Media / Streamer

  Rules, team voice, match scheduling
  /rulessetup                   Staff: wipe #rules and post the circuit rules as cards (edit RULE_CARDS to change)
  /teamvoices                   Staff: give older teams a voice channel (new teams get one automatically)
  /presettime time [timezone]   Staff: the time the bot sets if captains don't agree one in 48 hours
                                (default 18:00 ET, on the next day).
  /gametime match [timezone]    Captains: pick the times that work; the other captain confirms one in DMs (or
                                suggests another). 48 hours to agree, then the bot sets the preset time, which
                                can still be moved earlier or later if both captains confirm (72-hour window). New matches DM every player
                                "YOUR NEXT ON THE RISE PB: TOURNAMENT MATCH IS ..." and ping both captains.
                                Reminders 24h, 1h and at game time.
  /setgametime match date time [timezone]   Staff: set the time directly
  /nextgame                     Your team's next match and time
  /matchdms                     Turn your match DMs on/off

  Tickets
  /ticketsetup                  Staff: make the SUPPORT category with 🎫｜open-a-ticket (a card with a dropdown:
                                Stats, Report a cheater, Ranked/RR, Team/roster, Roles, Media, Appeal, General)
                                and a staff-only 📁｜ticket-logs. Picking a topic asks for details, then opens a
                                private channel for that player and staff. Claim / Close buttons inside; closing
                                saves a transcript to the logs and DMs it to the player.
  /ticketadd, /ticketremove     Staff: add or remove someone from a ticket
  /ticketclose [reason]         Close the ticket you're in

  Tournament
  /startswiss [wins] [losses]   Optional Swiss qualifier (default: 3 wins = qualify, 3 losses = out).
  /startgroups [advance]        Optional group stage: random groups of 4, top 2 (or 1 or 3) qualify.
  /startmain                    The main draw, always double elimination, posted in #bracket.
  /result match winner [score]  Referees/staff: record a result. Next matches post automatically. When the
                                  champion is crowned, RISER POINTS are awarded (or reset after a Major) and
                                  every player is DMed with Stay / Leave buttons.
  /statstemplate match          Referees/staff: get a stats sheet (CSV) for a game with both rosters listed
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
  6. Optional, before /setup: Server Settings -> Enable Community. This gives you a Stage channel for Finals.
  7. Run the bot with your token:
        Windows (PowerShell):  $env:DISCORD_TOKEN="paste-token-here"; python pbl_bot.py
        Mac/Linux:             DISCORD_TOKEN="paste-token-here" python3 pbl_bot.py
  8. In Discord, type /setup. Slash commands can take a minute to appear the first time.

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
    ("League Staff", 0xE74C3C, discord.Permissions(
        manage_messages=True, kick_members=True, moderate_members=True,
        manage_roles=True, manage_nicknames=True), True),
    ("Referee", 0xE67E22, discord.Permissions.none(), True),
    ("Team Captain", 0x3498DB, discord.Permissions.none(), True),
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
    ("LEAGUE", [("standings", "ro"), ("schedule", "ro"), ("bracket", "ro"),
                ("rosters", "ro"), ("transactions", "ro")]),
    ("MATCHES", [("scheduling", ["Team Captain"]),
                 ("score-reports", ["Team Captain", "Referee"]),
                 ("match-disputes", ["Team Captain", "Referee"]),
                 ("highlights", "open")]),
    ("COMMUNITY", [("general", "open"), ("free-agents", ["Free Agent", "Team Captain"]),
                   ("lfg-scrims", ["Player"])]),
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
3. **Build your roster:** `/sign @player` sends an offer they accept or decline in DMs. 5 to 8 players, one team each.
4. **Enter tournaments:** when entries open in #announcements, captains type `/register`.
5. **No team?** Type `/freeagent` and post in #free-agents so captains can find you.

Track every team in #rosters, the brackets in #bracket, and RISER POINTS with `/points`. See you on the rise."""

# Each card is posted as its own embed in #rules by /rulessetup (edit the text here to change the rules).
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
        "Captains sign players with `/sign`; the player accepts or declines in DMs. Players can only play the "
        "position they're listed at unless their captain changes it.",
        "Roster changes **lock** once entries close and stay locked until your team is eliminated.",
        "Team names and logos must be appropriate. Staff can rename or change a logo at any time.",
    ]),
    ("🏆 Tournament formats", 0xE0B44A, [
        "Every tournament needs at least **6 teams**. Seeding is random once entries close.",
        "**Swiss qualifier:** you play a team with the same record each round. **3 wins** = into the main draw, "
        "**3 losses** = eliminated. Byes count as a win.",
        "**Group stage:** random groups of 4, everyone plays everyone once. The top teams in each group advance. "
        "Tiebreakers: wins, then head-to-head, then point difference.",
        "**Main draw:** always double elimination. Lose once and you drop to the losers bracket; lose twice "
        "and you're out. If the losers-bracket team wins the Grand Final, it **resets** for one deciding game.",
        "Every match is a single game unless staff announce otherwise for that round.",
    ]),
    ("📅 Scheduling and match day", 0x22C55E, [
        "When your match is posted, every player gets a DM and both captains are pinged in #scheduling.",
        "Captains have **48 hours** to agree a game time with `/gametime`; the other captain confirms in DMs.",
        "No time after 48 hours? The bot sets the match for the **next day at 6 PM ET**. It can still be moved "
        "earlier or later, but **both captains must confirm** the new time.",
        "Once a game time passes, it can't be changed. No-show rules apply.",
        "Be in your team voice channel **10 minutes** before game time. The higher seed hosts the private "
        "server and shares the code with the other captain only.",
        "**No-shows:** fewer than 5 players ready **15 minutes** after the set time is a forfeit. "
        "Two forfeits in one tournament and your team is removed.",
        "Reminders are sent 24 hours and 1 hour before game time. Turn match DMs off with `/matchdms`.",
    ]),
    ("🏀 Game rules", 0xA855F7, [
        "5v5 in Practical Basketball, using the settings staff post for that tournament. No changes mid-game.",
        "Only rostered, eligible players may play. Subs must come from your own roster.",
        "**Disconnects:** if a player disconnects in the first 2 minutes, the game may be restarted once. "
        "After that, play on, and they can rejoin when they can.",
        "Intentionally crashing, lagging or leaving a game to force a restart is a forfeit.",
        "Play it out. No throwing, no sitting out to make a point, no letting a team win.",
    ]),
    ("📊 Results, stats and disputes", 0x3B82F6, [
        "The winning captain posts the final score and a **screenshot of the scoreboard** in #score-reports "
        "within **1 hour**. A Referee records it with `/result`.",
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
        "Every circuit event awards RISER POINTS by final placement. The points table is posted when entries open.",
        "Winners of tournaments marked as Major qualifiers get a spot in the next Major automatically (the "
        "announcement says so). Everyone else qualifies by reaching the "
        "points target.",
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
bot = commands.Bot(command_prefix="!", intents=intents)

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


# ---- Group stage (groups of 4, round robin)

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


def groups_new(ev: dict, team_ids: list[int], advance: int) -> dict:
    """Random groups of 4 (some of 3 when the count doesn't divide evenly) and every group match."""
    RNG.shuffle(team_ids)
    count = max(1, -(-len(team_ids) // 4))  # round up
    groups = [[] for _ in range(count)]
    for i, t in enumerate(team_ids):
        groups[i % count].append(t)
    gs = {"advance": advance, "groups": groups, "matches": [], "qualified": [],
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
    staff = [r for r in (role(guild, "League Staff"), role(guild, "Referee")) if r]
    league_staff = role(guild, "League Staff")
    ow = {guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, manage_channels=True)}

    if access == "open":
        ow[everyone] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
    elif access == "ro":
        ow[everyone] = discord.PermissionOverwrite(view_channel=True, send_messages=False, add_reactions=True)
        if league_staff:
            ow[league_staff] = discord.PermissionOverwrite(send_messages=True)
    elif access == "staff":
        ow[everyone] = discord.PermissionOverwrite(view_channel=False)
        for r in staff:
            ow[r] = discord.PermissionOverwrite(view_channel=True, send_messages=True)
    else:  # list of role names that may post
        ow[everyone] = discord.PermissionOverwrite(view_channel=True, send_messages=False)
        if league_staff:
            ow[league_staff] = discord.PermissionOverwrite(send_messages=True)
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
    """Post only if the channel is empty, so /setup can be re-run safely."""
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


@bot.tree.command(description="Staff: give the Player role to everyone already in the server.")
@app_commands.default_permissions(manage_roles=True)
async def giveplayerrole(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    player_role = role(interaction.guild, "Player")
    if player_role is None:
        return await interaction.response.send_message("Run /setup first.", ephemeral=True)
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


# ---------------------------------------------------------------- /setup

@bot.tree.command(description="Build the league's roles, channels and rules (safe to run again).")
@app_commands.default_permissions(administrator=True)
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
        notes.append("Couldn't reorder roles. Drag the bot's role to the top and run /setup again.")

    # Give the person running /setup the Commissioner role
    try:
        await interaction.user.add_roles(made["Commissioner"], reason="Circuit setup")
    except discord.HTTPException:
        notes.append("Couldn't give you Commissioner. Move the bot's role above it and run /setup again.")

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

    msg = ("ON THE RISE: PB CIRCUIT is built. Next: /giveplayerrole, /setmajor to set the Major target, "
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


def players_of_the_game(m: dict) -> tuple[tuple | None, tuple | None]:
    """(POTG, DPOTG) as (player key, line) from the box score, or None."""
    box = m.get("box") or {}
    if not box:
        return None, None
    winners = {k: v for k, v in box.items() if v["team"] == m.get("winner")} or box
    potg = max(winners.items(), key=lambda kv: kv[1]["pts"] + 1.2 * kv[1]["ast"] + 0.8 * kv[1]["reb"])
    others = {k: v for k, v in box.items() if k != potg[0]} or box
    dpotg = max(others.items(), key=lambda kv: 2 * kv[1]["stl"] + 2 * kv[1]["blk"] + 0.4 * kv[1]["reb"])
    return potg, dpotg


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
    potg, dpotg = players_of_the_game(m)
    if potg:
        p = potg[1]
        d = dpotg[1]
        lines += ["", "**Players of the Game**",
                  f"**POTG:** {who(potg[0])} · {p['pts']} PTS / {p['reb']} REB / {p['ast']} AST",
                  f"**DPOTG:** {who(dpotg[0])} · {d['stl']} STL / {d['blk']} BLK / {d['reb']} REB"]
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


async def post_score_card(guild: discord.Guild, s: dict, ev: dict, m: dict, reporter: int | None):
    """Post the Final Score card in #score-reports and remember it so /stat can update it."""
    ch = chan(guild, "score-reports")
    if ch is None:
        return
    t = s["teams"].get(str(m.get("winner")), {})
    f = logo_file(t) if t else None
    e = score_card(s, ev, m, reporter)
    kw = {"embed": e, "allowed_mentions": NO_PINGS}
    if f:
        e.set_thumbnail(url=f"attachment://{f.filename}")
        kw["file"] = f
    v = box_button(m)
    if v:
        kw["view"] = v
    msg = await ch.send(**kw)
    m["card"] = [ch.id, msg.id, reporter]


async def refresh_score_card(guild: discord.Guild, s: dict, ev: dict, m: dict):
    """After /stat, redraw the card so Players of the Game shows up."""
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




def is_staff(member: discord.Member) -> bool:
    return member.guild_permissions.administrator or any(
        r.name in ("Commissioner", "League Staff") for r in member.roles)


def roster_locked(s: dict) -> bool:
    """Rosters freeze once the main draw starts, until the tournament ends."""
    ev = s["event"]
    return bool(ev and ev["stage"] == "main")


def tournament_running(s: dict) -> bool:
    ev = s["event"]
    return bool(ev and ev["stage"] != "done")


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
    for rn in ("Commissioner", "League Staff", "Referee"):
        r = role(guild, rn)
        if r:
            ow[r] = discord.PermissionOverwrite(view_channel=True, connect=True, speak=True)
    try:
        return await guild.create_voice_channel(f"🔊 {name}", category=category, overwrites=ow)
    except discord.HTTPException:
        return None


async def create_team(guild: discord.Guild, data: dict, name: str, captain: discord.Member, logo: str) -> str:
    """Make the team role + private channel, save it, and give the captain their roles. Returns the team key."""
    s = guild_signups(data, guild.id)
    color = TEAM_COLORS[len(s["teams"]) % len(TEAM_COLORS)]
    team = await guild.create_role(name=name, colour=discord.Colour(color), reason="New team")
    player_role = role(guild, "Player")
    if player_role:  # sit just above Player so the team color shows on names
        try:
            await team.edit(position=player_role.position + 1)
        except discord.HTTPException:
            pass
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
                       f"Captain, offer spots with `/sign @player`. You need {ROSTER_MIN} to {ROSTER_MAX} players "
                       "including you, and nobody can be on two teams. Once you have "
                       f"{ROSTER_MIN}, your team shows up in #rosters and on the website, and you can "
                       "`/register` for tournaments.", title=f"Welcome to {name}", file=f)
    return key


async def delete_team(guild: discord.Guild, data: dict, key: str, reason: str):
    s = guild_signups(data, guild.id)
    t = s["teams"].pop(key, None)
    if t:
        tz = s.get("tourney")
        if tz and key in tz.get("entrants", []):
            tz["entrants"].remove(key)
        if key in circuit(s)["qualified"]:
            circuit(s)["qualified"].remove(key)
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
        await give_roles(guild, int(uid), role(guild, "Team Captain"), remove=True)
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
    if t["captain"] == user_id:
        t["captain"] = int(next(iter(t["roster"])))
        await give_roles(guild, t["captain"], role(guild, "Team Captain"))
        note = f" <@{t['captain']}> is the new captain."
    lost = check_core(s, key)
    if lost:
        note += f"\n{lost}"
    save_data(data)
    await give_roles(guild, user_id, guild.get_role(int(key)), role(guild, "Team Captain"), remove=True)
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
             f"**{len(complete)} complete team(s)** shown below"
             + (f" · {building} still building their roster" if building else "") + "."]
    if c["needed"] is not None:
        lines.append(f"**Major:** {c['needed']} RISER POINTS to qualify. Winners of Major-qualifier events qualify automatically.")
    if tz:
        state = "taking entries" if s["open"] else "entries closed"
        lines.append(f"**Current tournament:** {tz['name']} ({'MAJOR' if tz['kind'] == 'major' else 'circuit event'}"
                     f", {state}) · {len([k for k in tz['entrants'] if k in s['teams']])} registered")
        if tz.get("spec") and tz["kind"] != "major":
            lines.append(f"RISER POINTS: {spec_text(tz['spec'])}")
    lines.append("Start a team: `/signup` with a name and logo. Captains: `/sign @player`, then `/register`.")
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
    players = [f"<@{u}>{pos_tag(s, u)}{' (C)' if int(u) == t['captain'] else ''}" for u in t["roster"]]
    desc = f"**Players ({len(players)}/{ROSTER_MAX})**\n" + "\n".join(players) + f"\n\n{points_line(s, key)}"
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
    """Keep #rosters current: a summary message, then one card (with logo) per COMPLETE team.
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
            if is_complete(t) and t.get("board_sig") == sig and t.get("board_msg"):
                continue
            if t.get("board_msg"):
                try:
                    await (await channel.fetch_message(t["board_msg"])).delete()
                except discord.HTTPException:
                    pass
                t["board_msg"] = None
            if is_complete(t):
                embed, f = team_embed(guild, s, key)
                sent = await channel.send(embed=embed, allowed_mentions=NO_PINGS, **({"file": f} if f else {}))
                t["board_msg"], t["board_sig"] = sent.id, sig
            else:
                t["board_sig"] = None
        save_data(data)
    schedule_publish(guild)

@bot.tree.command(description="Staff: open entries for a tournament and set its RISER POINTS.")
@app_commands.describe(name="Tournament name, e.g. 'Rise Open 1'",
                       logo="The tournament's logo (PNG, JPG, WEBP or GIF, under 1 MB). Required.",
                       kind="Circuit event (awards RISER POINTS) or Major (qualified teams only)",
                       points="Points per placement, e.g. 1:100, 2:70, 3:50, 4:40, 5-6:25, 7-8:15",
                       closes="When entries close, e.g. 'Friday at 8pm' (optional)",
                       winner_qualifies="Does the winner get an automatic Major spot? (default yes)")
@app_commands.choices(kind=[
    app_commands.Choice(name="Circuit event (awards RISER POINTS)", value="event"),
    app_commands.Choice(name="Major (qualified teams only, points reset after)", value="major"),
])
@app_commands.default_permissions(manage_roles=True)
async def opensignups(interaction: discord.Interaction, name: str, logo: discord.Attachment, kind: str = "event",
                      points: str | None = None, closes: str | None = None, winner_qualifies: bool = True):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can open a tournament.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    if tournament_running(s):
        return await interaction.response.send_message(
            "A tournament is still being played. Finish it (or /resetevent) first.", ephemeral=True)
    spec = {}
    if kind == "event":
        if points:
            spec, problem = parse_spec(points)
        else:  # the saved payout table from /payout, or the built-in one
            spec, problem = dict(circuit(s).get("payout") or parse_spec(DEFAULT_SPEC)[0]), None
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
    archive_event(guild, s)  # keep last tournament's player stats for the year table
    s["tourney"] = {"name": name.strip()[:60], "kind": kind, "spec": spec, "entrants": [], "logo": logo_name,
                    "winner_qualifies": winner_qualifies if kind == "event" else False}
    s["open"], s["closes"], s["event"] = True, closes, None
    save_data(data)
    await update_board(guild, data)

    c = circuit(s)
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
        + " Change it any time with /majorspot.", ephemeral=True)


@bot.tree.command(description="Staff: choose whether the current tournament's winner qualifies for the Major.")
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


@bot.tree.command(description="Staff: change the current tournament's logo.")
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


@bot.tree.command(description="Set the position you play: PG, SG, SF, PF or C.")
@app_commands.describe(position="Your position")
@app_commands.choices(position=[app_commands.Choice(name=n, value=v) for v, n in POSITIONS])
async def position(interaction: discord.Interaction, position: str):
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    s.setdefault("positions", {})[str(interaction.user.id)] = position
    save_data(data)
    await interaction.response.send_message(f"Your position is now **{dict(POSITIONS)[position]}**.", ephemeral=True)
    await update_board(interaction.guild, data)


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
        f"Next: offer spots with `/sign @player` ({ROSTER_MIN} to {ROSTER_MAX} players including you). "
        f"Once you have {ROSTER_MIN}, use `/register` to enter tournaments.", ephemeral=True)


@bot.tree.command(description="Captains: offer a player a spot on your team. They accept or decline in DMs.")
@app_commands.describe(player="The player to offer a spot", team="Staff only: which team (captains leave this empty)")
async def sign(interaction: discord.Interaction, player: discord.Member, team: discord.Role | None = None):
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
    key = str(team.id) if (team and is_staff(user)) else captain_team(s, user.id)
    problem = None
    if key is None or key not in s["teams"]:
        problem = ("Only team captains can sign players. Start a team with /signup."
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
        await post(player, text, title=f"Contract offer: {t['name']}", color=GOLD, view=view, file=f)
        where = "in their DMs"
    except discord.HTTPException:  # DMs closed: post it in #free-agents instead
        ch = chan(guild, "free-agents")
        if ch is None:
            s["offers"].pop(oid, None)
            save_data(data)
            return await interaction.followup.send(f"{player.mention} has DMs turned off and there's no "
                                                   "#free-agents channel to post the offer in.", ephemeral=True,
                                                   allowed_mentions=NO_PINGS)
        await post(ch, text, title=f"Contract offer: {t['name']}", color=GOLD, view=view, ping=player.mention,
                   file=logo_file(t))
        where = "in #free-agents (their DMs are closed)"
    await interaction.followup.send(f"Offer sent to {player.mention} {where}. You'll hear back in your team "
                                    "channel when they answer.", ephemeral=True, allowed_mentions=NO_PINGS)


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
        problem = "You can't release the captain. Pass it on with /makecaptain first."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True, allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)
    text = await remove_member(guild, data, key, player.id, "was released from")
    await update_board(guild, data)
    await interaction.followup.send(text, ephemeral=True, allowed_mentions=NO_PINGS)


@bot.tree.command(description="Captains: hand the captaincy to a teammate.")
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
    save_data(data)
    await give_roles(guild, interaction.user.id, role(guild, "Team Captain"), remove=True)
    await give_roles(guild, player.id, role(guild, "Team Captain"))
    await log_transaction(guild, f"{player.mention} is now captain of **{t['name']}**", t)
    await update_board(guild, data)
    await interaction.followup.send(f"{player.mention} is now the captain.", ephemeral=True,
                                    allowed_mentions=NO_PINGS)


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
    await interaction.followup.send(text, ephemeral=True, allowed_mentions=NO_PINGS)


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
    await delete_team(guild, data, key, "disbanded by the captain")
    await update_board(guild, data)
    await interaction.followup.send("Your team has been disbanded.", ephemeral=True)


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


@bot.tree.command(description="Show a team's logo, roster and RISER POINTS.")
@app_commands.describe(team="The team's role (leave empty for your own team)")
async def teaminfo(interaction: discord.Interaction, team: discord.Role | None = None):
    s = guild_signups(load_data(), interaction.guild.id)
    key = str(team.id) if team else team_of(s, interaction.user.id)
    if not key or key not in s["teams"]:
        return await interaction.response.send_message("Couldn't find that team.", ephemeral=True)
    embed, f = team_embed(interaction.guild, s, key)
    await interaction.response.send_message(embed=embed, ephemeral=True, **({"file": f} if f else {}))


@bot.tree.command(description="See the teams registered for the current tournament.")
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


@bot.tree.command(description="Staff: repost the team cards in #rosters.")
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


@bot.tree.command(description="Staff: create a team for someone (they become captain).")
@app_commands.describe(name="Team name", captain="The captain", logo="Team logo (PNG, JPG, WEBP or GIF, under 1 MB)")
@app_commands.default_permissions(manage_roles=True)
async def addteam(interaction: discord.Interaction, name: str, captain: discord.Member, logo: discord.Attachment):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can add teams.", ephemeral=True)
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
    await interaction.followup.send("Team removed.", ephemeral=True)


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
        return await interaction.response.send_message("Staff need to run /setup first.", ephemeral=True)
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
        msg = "You're now a Free Agent and listed in #rosters. Post in #free-agents too."
    await update_board(guild, data)
    await interaction.followup.send(msg, ephemeral=True)


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
DEFAULT_SPEC = "1:100, 2:70, 3:50, 4:40, 5-6:25, 7-8:15, 9-12:10, 13-16:5"
TEST_NAMES: dict[int, str] = {}  # fake teams used by /testtournament


def parse_spec(text: str) -> tuple[dict, str | None]:
    """'1:100, 2:70, 5-6:25' -> {'1': 100, '2': 70, '5': 25, '6': 25}. Returns (spec, problem)."""
    spec = {}
    parts = [p.strip() for p in re.split(r"[,\n;]", text or "") if p.strip()]
    if not parts:
        return {}, "Give points like: 1:100, 2:70, 3:50, 4:40, 5-6:25"
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


def circuit(s: dict) -> dict:
    c = s.setdefault("circuit", {})
    c.setdefault("needed", None)
    c.setdefault("qualified", [])
    return c


def is_complete(t: dict) -> bool:
    return len(t["roster"]) >= ROSTER_MIN


def major_qualified(s: dict, key: str) -> bool:
    c = circuit(s)
    t = s["teams"].get(key, {})
    return key in c["qualified"] or (c["needed"] is not None and t.get("points", 0) >= c["needed"])


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
    """[(placement, [team ids tied there]), ...] from the champion down, then non-qualifiers."""
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
    spec = tz.get("spec") or circuit(s).get("payout") or parse_spec(DEFAULT_SPEC)[0]
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
    base = base or dict(circuit(s).get("payout") or parse_spec(DEFAULT_SPEC)[0])
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

@bot.tree.command(description="Staff: set how many RISER POINTS a team needs to qualify for the Major.")
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


@bot.tree.command(description="Staff: set a team's RISER POINTS by hand.")
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


@bot.tree.command(description="Staff: reset every team's RISER POINTS and Major spots to 0.")
@app_commands.describe(confirm="Set to True to confirm")
@app_commands.default_permissions(manage_roles=True)
async def resetpoints(interaction: discord.Interaction, confirm: bool = False):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    if not confirm:
        return await interaction.response.send_message("Run /resetpoints confirm:True to reset everything.",
                                                       ephemeral=True)
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    for t in s["teams"].values():
        t["points"], t["core"] = 0, []
    circuit(s)["qualified"] = []
    save_data(data)
    await update_board(interaction.guild, data)
    await interaction.response.send_message("All RISER POINTS and Major spots reset.", ephemeral=True)


@bot.tree.command(description="Captains: enter your team in the current tournament.")
async def register(interaction: discord.Interaction):
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    if suspended_from(s, interaction.user.id, "league"):
        return await interaction.response.send_message(suspended_from(s, interaction.user.id, "league"), ephemeral=True)
    tz = s.get("tourney")
    key = captain_team(s, interaction.user.id)
    problem = None
    if key is None:
        problem = "Only team captains can register. Start a team with /signup."
    elif not tz or not s["open"]:
        problem = "No tournament is taking entries right now. Watch #announcements."
    elif key in tz["entrants"]:
        problem = "Your team is already registered."
    elif not is_complete(s["teams"][key]):
        n = len(s["teams"][key]["roster"])
        problem = f"Your roster needs at least {ROSTER_MIN} players (you have {n}). Send offers with /sign."
    elif tz["kind"] == "major" and not major_qualified(s, key):
        problem = f"Only qualified teams can enter the Major. You have {points_line(s, key)}."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    tz["entrants"].append(key)
    save_data(data)
    await interaction.response.defer(ephemeral=True)
    t = s["teams"][key]
    line = points_line(s, key)
    await log_transaction(guild, f"**{t['name']}** registered for **{tz['name']}** · {line}", t)
    await update_board(guild, data)
    await interaction.followup.send(f"**{t['name']}** is registered for **{tz['name']}** "
                                    f"(team #{len(tz['entrants'])}).\n{line}", ephemeral=True)


@bot.tree.command(description="Captains: take your team out of the current tournament.")
async def unregister(interaction: discord.Interaction):
    data = load_data()
    s = guild_signups(data, interaction.guild.id)
    tz = s.get("tourney")
    key = captain_team(s, interaction.user.id)
    if not tz or not s["open"] or key not in (tz or {}).get("entrants", []):
        return await interaction.response.send_message("You're not registered for an open tournament.",
                                                       ephemeral=True)
    tz["entrants"].remove(key)
    save_data(data)
    await update_board(interaction.guild, data)
    await interaction.response.send_message("Your team has been taken out of the tournament.", ephemeral=True)


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
@app_commands.describe(teams="How many fake teams (2 to 64)", style="Qualifier to test",
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
async def testtournament(interaction: discord.Interaction, teams: app_commands.Range[int, 2, 64] = 16,
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
    spec = dict(tz.get("spec") or circuit(s).get("payout") or parse_spec(DEFAULT_SPEC)[0])
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


@bot.tree.command(description="Staff: delete every message posted by test tournaments.")
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


def all_matches(ev: dict | None) -> list[dict]:
    if not ev:
        return []
    out = []
    for part in ("swiss", "groups", "main"):
        out += (ev.get(part) or {}).get("matches", [])
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
    major = tz.get("kind") == "major"
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


@bot.tree.command(description="Referees/staff: get a stats sheet for a match to fill in, then upload it with /importstats.")
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


@bot.tree.command(description="Referees/staff: upload a filled-in stats sheet (CSV) for a match.")
@app_commands.describe(match="Match number, e.g. 7 for M7", file="The stats sheet saved as CSV")
async def importstats(interaction: discord.Interaction, match: int, file: discord.Attachment):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only Referees and league staff can import stats.",
                                                       ephemeral=True)
    if not file.filename.lower().endswith((".csv", ".txt")) or file.size > 200_000:
        return await interaction.response.send_message(
            "Upload the sheet as a **CSV** file (in Excel: File > Save As > CSV; in Google Sheets: "
            "File > Download > CSV).", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    data = load_data()
    s = guild_signups(data, guild.id)
    m = next((x for x in all_matches(s["event"]) if x["id"] == match), None)
    if m is None or m.get("a") is None or m.get("b") is None:
        return await interaction.followup.send(f"There's no playable match M{match}.", ephemeral=True)

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

    text = (await file.read()).decode("utf-8-sig", errors="replace")
    try:
        dialect = csv.Sniffer().sniff(text[:2000], delimiters=",;\t")
    except csv.Error:
        dialect = csv.excel
    rows = list(csv.reader(io.StringIO(text), dialect))
    if not rows:
        return await interaction.followup.send("That file is empty.", ephemeral=True)
    keys = [sheet_key(h) for h in rows[0]]
    if "player" not in keys and "id" not in keys:
        return await interaction.followup.send(
            "I couldn't find a **Player** (or **Discord ID**) column. Use `/statstemplate` to get a sheet in the "
            "right layout.", ephemeral=True)

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
                + ". Use their Discord name, or the Discord ID column from `/statstemplate`.")
    if problems:
        msg += "\nSkipped: " + "; ".join(problems[:10])
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


async def start_pickup(guild: discord.Guild, data: dict):
    """The queue is full: either draft (two random captains pick from a menu) or auto-balance by RR."""
    s = guild_signups(data, guild.id)
    p = pug(s)
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
    for side in ("A", "B"):
        try:
            vc = await guild.create_voice_channel(f"P{mid} · Team {side}", category=cat)
            m["vcs"].append(vc.id)
        except discord.HTTPException:
            pass
    save_data(data)
    ch = pug_ch(guild, p, "queue")
    host = max(a + b, key=lambda u: pug_player(p, u)["rr"])
    m["host"] = host
    cap = lambda team, u: "(C) " if m.get("pool") is not None and team[0] == u else ""
    pz = lambda u: f" · {p['_pos'][str(u)]}" if str(u) in p.get("_pos", {}) else ""
    desc = (f"**Team A** · avg {avg_rr(p, a):.0f} RR\n" + "\n".join(f"{cap(a, u)}<@{u}>{pz(u)} · {show_rank(pug_player(p, u))}" for u in a)
            + f"\n\n**Team B** · avg {avg_rr(p, b):.0f} RR\n" + "\n".join(f"{cap(b, u)}<@{u}>{pz(u)} · {show_rank(pug_player(p, u))}" for u in b)
            + f"\n\n**Host:** <@{host}> (highest RR) makes the private server and shares the code."
            + "\nWhen it's done, one player from **each** team clicks who won. Both have to agree."
            + "\nThen the host (or staff) enters stats with `/pickupstats` or `/pickupstat`: each win is "
              "+10 to +32 RR and each loss -10 to -32, depending on how well you played.")
    e = brand_embed(desc, f"Pickup P{mid} is ready", GOOD)
    if ch:
        msg = await ch.send(content=" ".join(f"<@{u}>" for u in a + b), embed=e, view=ReportView(guild.id, mid),
                            allowed_mentions=discord.AllowedMentions(users=True))
        m["card"] = [ch.id, msg.id]
        save_data(data)


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
    for vc_id in m.get("vcs", []):
        vc = guild.get_channel(vc_id)
        if vc:
            try:
                await vc.delete(reason=f"Pickup P{mid} finished")
            except discord.HTTPException:
                pass
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


@bot.tree.command(description="Get a stats sheet (CSV) for a pickup to fill in, then upload it with /pickupstats.")
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


@bot.tree.command(description="Upload a pickup's stats sheet (CSV). RR is adjusted for how each player played.")
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
    rows = list(csv.reader(io.StringIO(text)))
    if not rows:
        return await interaction.followup.send("That file is empty.", ephemeral=True)
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
    if action == "cancel":
        if not staff:
            return await interaction.response.send_message("Only staff can cancel a pickup.", ephemeral=True)
        m["status"] = "cancelled"
        for u in m["a"] + m["b"] + m.get("pool", []):
            p["qpos"].pop(str(u), None)
        m["pool"] = []
        save_data(data)
        for vc_id in m.get("vcs", []):
            vc = guild.get_channel(vc_id)
            if vc:
                try:
                    await vc.delete()
                except discord.HTTPException:
                    pass
        await interaction.response.edit_message(view=None)
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
        f"1. Click **Join Queue** in the queue channel and pick the position you're playing (PG, SG, SF, PF, C).",
        f"2. When **{p['size']}** players are in, " + (
            "the bot picks **2 random captains**. They take turns picking players from a dropdown "
            "(A, B, B, A, A, B, B, A); the last player is placed automatically."
            if draft else "the bot splits everyone into **two balanced teams** by RR."),
        "3. Two voice channels open for the match. The **host** (highest RR) makes the private server and "
        "shares the code with both teams.",
        "4. When the game ends, **one player from each team** clicks who won. Both have to agree, or staff settle it.",
        "5. The host (or staff) enters everyone's stats with `/pickupstats` (sheet from `/pickuptemplate`) or "
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
        "`/pickupstat` · `/pickupstats` · `/pickuptemplate` enter a game's stats (host or staff)",
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


@bot.tree.command(description="Staff: set up ranked pickups: the 10 MANS channels, info, queue card and rank roles.")
@app_commands.describe(players="Players per match: 4 (2v2), 6 (3v3), 8 (4v4) or 10 (5v5). Default 10",
                       start_rr="Hidden RR new players start their placements at (default 900 = Gold 1)",
                       rr_swing="Old setting, kept for compatibility (gains now come from stats)",
                       teams="How teams are made (default: captains' draft)")
@app_commands.choices(teams=[app_commands.Choice(name="Captains' draft (2 random captains pick)", value="draft"),
                             app_commands.Choice(name="Auto-balance by RR", value="balanced")],
                      players=[app_commands.Choice(name="2v2", value=4), app_commands.Choice(name="3v3", value=6),
                               app_commands.Choice(name="4v4", value=8), app_commands.Choice(name="5v5", value=10)])
@app_commands.default_permissions(manage_roles=True)
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


@bot.tree.command(description="Staff: set a player's pickup RR.")
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


@bot.tree.command(description="Staff: start a new pickup season (everyone back to the starting RR).")
@app_commands.describe(confirm="Set to True to reset every player's RR and record")
@app_commands.default_permissions(manage_roles=True)
async def resetrr(interaction: discord.Interaction, confirm: bool = False):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only staff can do that.", ephemeral=True)
    if not confirm:
        return await interaction.response.send_message("Run /resetrr confirm:True to reset everyone.", ephemeral=True)
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
# /ticketsetup makes a SUPPORT category with 🎫｜open-a-ticket (a card with a dropdown) and a staff-only
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
    return [r for r in (role(guild, "Commissioner"), role(guild, "League Staff"), role(guild, "Referee")) if r]


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


@bot.tree.command(description="Staff: set up the ticket system (dropdown card, ticket category and logs).")
@app_commands.default_permissions(manage_roles=True)
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


@bot.tree.command(description="Staff: add someone to this ticket.")
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


@bot.tree.command(description="Staff: remove someone from this ticket.")
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


@bot.tree.command(description="Close this ticket (saves a transcript).")
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
# /modsetup makes a MODERATION category with ⛔｜suspensions (public, read-only log of every suspension)
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


@bot.tree.command(description="Staff: suspend a player for a number of tournaments (or a set time).")
@app_commands.describe(member="Who to suspend", reason="Why (shown in the suspensions channel and DMed to them)",
                       tournaments="How many tournaments they sit out (the current/next one counts as the first)",
                       length="Or a set time instead: 30m, 12h, 3d, 1w, 2d12h, or perm",
                       scope="What they're blocked from (tournament suspensions are always at least League)")
@app_commands.choices(scope=[app_commands.Choice(name="Ranked queue only", value="queue"),
                             app_commands.Choice(name="League: queue, teams, tournaments", value="league"),
                             app_commands.Choice(name="Server timeout (can't chat) + league", value="server")])
@app_commands.default_permissions(moderate_members=True)
async def suspend(interaction: discord.Interaction, member: discord.Member, reason: str,
                  tournaments: app_commands.Range[int, 1, 10] | None = None, length: str | None = None,
                  scope: str = "league"):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can suspend players.", ephemeral=True)
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
    m["suspensions"][str(member.id)] = {"scope": scope, "reason": reason[:300], "by": interaction.user.id,
                                        "start": now.isoformat(timespec="seconds"),
                                        "until": until.isoformat(timespec="seconds") if until else None,
                                        "tournaments": tournaments, "left": tournaments, "case": case}
    m["history"].append({"user": member.id, "scope": scope, "reason": reason[:300], "by": interaction.user.id,
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


@bot.tree.command(description="Staff: lift a player's suspension early.")
@app_commands.describe(member="Who to unsuspend")
@app_commands.default_permissions(moderate_members=True)
async def unsuspend(interaction: discord.Interaction, member: discord.Member):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    ok = await lift_suspension(interaction.guild, load_data(), member.id, interaction.user.mention, "Lifted by staff")
    await interaction.followup.send(f"Lifted {member.mention}'s suspension." if ok else
                                    f"{member.mention} isn't suspended.", ephemeral=True, allowed_mentions=NO_PINGS)


@bot.tree.command(description="Staff: list current suspensions, or one player's history.")
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


@bot.tree.command(description="Staff: set up the welcome channel, join log and suspensions channel.")
@app_commands.describe(welcome_message="Optional extra line in every welcome card (e.g. season info)")
@app_commands.default_permissions(manage_roles=True)
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
# /mediasetup makes a MEDIA category:
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


def leaders_embed(table: dict, title: str, color: int, min_gp: int = 1) -> discord.Embed:
    rows = [r for r in table.values() if r["gp"] >= min_gp]
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
            f"`{i + 1}.` <@{k}> **{int(v['rr'])}** {rank_of(v['rr'])[0]}" for i, (k, v) in enumerate(top)))
        wins = sorted(placed, key=lambda kv: -kv[1]["w"])[:5]
        e.add_field(name="Most wins", inline=True, value="\n".join(
            f"`{i + 1}.` <@{k}> **{v['w']}W**-{v['l']}L" for i, (k, v) in enumerate(wins)))
        hot = sorted((kv for kv in placed if kv[1].get("streak", 0) >= 2), key=lambda kv: -kv[1]["streak"])[:5]
        if hot:
            e.add_field(name="Hottest streaks", inline=True, value="\n".join(
                f"🔥 <@{k}> **{v['streak']}W**" for k, v in hot))
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
    cards = [leaders_embed(current, f"{tname}: stat leaders (per game)", GOLD),
             leaders_embed(year, f"{datetime.now().year} season leaders (per game, 2+ games)", BRAND, min_gp=2),
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
        f"{at('shows')} Podcasts, personal shows, recaps, interviews (Media role).",
        f"{at('rankings')} Power rankings, previews and articles (Media + staff).",
        f"{at('highlights')} Everyone: post your clips and best plays.",
        f"{at('edits')} Everyone: edits, thumbnails and graphics.",
        f"{at('chat')} Media and streamers: plan collabs and coverage.",
        "**🎙️ Media Booth** voice: Media and Streamers talk, everyone can listen in.",
    ]), "Media channels", BRAND)
    roles = brand_embed("\n".join([
        "**Media** — content creators who cover the circuit: shows, recaps, rankings, interviews.",
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


@bot.tree.command(description="Staff: set up the MEDIA category: stat leaders, streams, shows, highlights and more.")
@app_commands.default_permissions(manage_roles=True)
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
    data = load_data()
    s = guild_signups(data, guild.id)
    c = media(s)["chans"]
    cat = guild.get_channel(c.get("category") or 0) or discord.utils.get(guild.categories, name="MEDIA") \
        or await guild.create_category("MEDIA")
    c["category"] = cat.id
    wanted = [("info", "📌｜media-info", "ro"), ("leaders", "📊｜stat-leaders", "ro"),
              ("live", "🔴｜live-now", ["Media", "Streamer"]), ("shows", "🎙️｜media-shows", ["Media"]),
              ("rankings", "📰｜power-rankings", ["Media"]), ("highlights", "🎬｜highlights", "open"),
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
        f"(or `/statleaders`). Give creators the **Media** or **Streamer** role so they can post shows and "
        "use `/golive`.", ephemeral=True)


@bot.tree.command(description="Refresh the stat leaders cards in the media channel now.")
async def statleaders(interaction: discord.Interaction):
    await interaction.response.defer(ephemeral=True)
    await refresh_leaders(interaction.guild)
    c = media(guild_signups(load_data(), interaction.guild.id))["chans"]
    await interaction.followup.send(f"Updated <#{c['leaders']}>." if c.get("leaders") else
                                    "Run /mediasetup first.", ephemeral=True)


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
        return await interaction.response.send_message("Staff need to run /mediasetup first.", ephemeral=True)
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


@bot.tree.command(description="Staff: give or take the Media / Streamer role.")
@app_commands.describe(member="Who", kind="Which role", remove="Take it away instead")
@app_commands.choices(kind=[app_commands.Choice(name="Media", value="Media"),
                            app_commands.Choice(name="Streamer", value="Streamer")])
@app_commands.default_permissions(manage_roles=True)
async def mediarole(interaction: discord.Interaction, member: discord.Member, kind: str, remove: bool = False):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can do that.", ephemeral=True)
    r = role(interaction.guild, kind)
    if r is None:
        return await interaction.response.send_message("Run /mediasetup first.", ephemeral=True)
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
        await interaction.response.send_modal(MediaApply())


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
                        f"`/mediarole member:@{interaction.user.name} kind:...`", "🎥 Media application", INFO)
        e.set_thumbnail(url=interaction.user.display_avatar.url)
        if staff_ch:
            await staff_ch.send(embed=e, allowed_mentions=NO_PINGS)
        await interaction.response.send_message("Application sent to staff. You'll hear back soon!", ephemeral=True)


# ---------------------------------------------------------------- game times + match reminders
#
# When a tournament match becomes playable (a new Swiss round, the group schedule, a bracket match),
# every player on both teams gets a DM: "YOUR NEXT ON THE RISE PB: TOURNAMENT MATCH IS ...", and both
# captains get pinged in #scheduling. The captains have 48 HOURS to agree a game time:
#   1. One captain runs /gametime match:12 and picks one or more times (dropdowns, next 48 hours).
#   2. The request posts in #scheduling pinging both captains, and the other captain gets a DM with a
#      dropdown: pick one of the offered times (confirmed), or pick a different time (sent back to the
#      first captain to accept or decline).
#   3. Once confirmed, both rosters get DMs, then reminders 24 hours, 1 hour and at game time.
# If 48 hours pass with no time, both captains and staff are pinged; staff use /setgametime.

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
    sc.setdefault("preset", {"time": "18:00", "tz": "ET"})  # default game time set by /presettime
    return sc


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
    if not ev:
        return []
    out = []
    if ev.get("stage") == "swiss" and ev.get("swiss"):
        sw = ev["swiss"]
        out += [{"id": m["id"], "a": m["a"], "b": m["b"], "label": f"Swiss round {m['round']}"}
                for m in sw["matches"] if m["round"] == sw["round"] and not m["winner"] and m.get("b")]
    if ev.get("stage") == "groups" and ev.get("groups"):
        gs = ev["groups"]
        for gi in range(len(gs["groups"])):
            left = [m for m in gs["matches"] if m["group"] == gi and not m["winner"]]
            if left:
                rnd = min(m["round"] for m in left)  # one round at a time, so 48 hours means something
                out += [{"id": m["id"], "a": m["a"], "b": m["b"],
                         "label": f"Group {group_letter(gi)} · round {rnd}"} for m in left if m["round"] == rnd]
    if ev.get("main"):
        out += [{"id": m["id"], "a": m["a"], "b": m["b"], "label": m["label"]} for m in de_ready(ev["main"])]
    return out


def team_name(s: dict, tid) -> str:
    t = s["teams"].get(str(tid))
    return t["name"] if t else "TBD"


def ts(dt: datetime, style: str = "F") -> str:
    return f"<t:{int(dt.timestamp())}:{style}>"


def slot_options(start: datetime, end: datetime, tz_code: str, taken: list[int] | None = None) -> list[list]:
    """Hourly game times from the next full hour until `end`, as up to two lists of 24 select options."""
    tz = tzinfo(tz_code)
    t = (start + timedelta(hours=1)).replace(minute=0, second=0, microsecond=0)
    opts = []
    while t <= end and len(opts) < 48:
        if int(t.timestamp()) not in (taken or []):
            local = t.astimezone(tz)
            label = local.strftime("%a %b %d · %I:%M %p").replace(" 0", " ") + f" {tz_code}"
            opts.append(discord.SelectOption(label=label, value=str(int(t.timestamp()))))
        t += timedelta(hours=1)
    return [opts[i:i + 24] for i in range(0, len(opts), 24)]


def slot_label(t: int, tz_code: str) -> str:
    local = datetime.fromtimestamp(t, timezone.utc).astimezone(tzinfo(tz_code))
    return local.strftime("%a %b %d · %I:%M %p").replace(" 0", " ") + f" {tz_code}"


async def dm(uid: int, embed: discord.Embed, view=None) -> bool:
    try:
        u = bot.get_user(int(uid)) or await bot.fetch_user(int(uid))
        kw = {"embed": embed}
        if view is not None:
            kw["view"] = view
        await u.send(**kw)
        return True
    except (discord.HTTPException, AttributeError):
        return False


async def dm_teams(guild: discord.Guild, s: dict, teams: list, embed_for) -> None:
    """DM every player on these teams. embed_for(team_id) builds the card for that team's side."""
    muted = sched(s)["muted"]
    for tid in teams:
        t = s["teams"].get(str(tid))
        if not t:
            continue
        for uid in t["roster"]:
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
            f"or it's set for the next day at {sched(s)['preset']['time']} {sched(s)['preset']['tz']}.")
    e = brand_embed(f"# YOUR NEXT ON THE RISE PB: TOURNAMENT MATCH IS M{mid}\n"
                    f"**{team_name(s, our)}** vs **{team_name(s, other)}**\n"
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
    sc["matches"][mid] = {"a": m["a"], "b": m["b"], "label": m["label"], "opened": now.isoformat(timespec="seconds"),
                          "deadline": (now + timedelta(hours=AGREE_HOURS)).isoformat(timespec="seconds"),
                          "window_end": (now + timedelta(hours=SCHED_HOURS)).isoformat(timespec="seconds"),
                          "time": None, "preset": False, "reminded": [], "done": False}
    await dm_teams(guild, s, [m["a"], m["b"]], lambda tid: next_match_card(s, mid, tid))
    dl = datetime.fromisoformat(sc["matches"][mid]["deadline"])
    p_ = sc["preset"]
    await scheduling_post(guild, s, mid,
                          f"**M{mid}** · {m['label']}\n**{team_name(s, m['a'])}** vs **{team_name(s, m['b'])}**\n\n"
                          f"Captains, you have **48 hours** (until {ts(dl)}) to agree a game time. Run "
                          f"`/gametime match:{mid}` and pick the times that work; the other captain confirms in DMs.\n"
                          f"No time by then? The bot sets one for the **next day at {p_['time']} {p_['tz']}**, "
                          "which you can still move earlier or later if both captains confirm.",
                          f"📅 Schedule your match · M{mid}", INFO)


async def confirm_time(guild: discord.Guild, data: dict, mid: str, when: int, by: str):
    s = guild_signups(data, guild.id)
    sc = sched(s)
    e_ = sc["matches"].get(mid)
    if not e_:
        return
    e_["time"] = datetime.fromtimestamp(when, timezone.utc).isoformat(timespec="seconds")
    e_["preset"] = False  # agreed (or set by staff): locked
    e_["reminded"] = []
    for r in sc["requests"].values():
        if r["match"] == mid and r["status"] == "open":
            r["status"] = "closed"
    save_data(data)
    dt = datetime.fromtimestamp(when, timezone.utc)
    await scheduling_post(guild, s, mid, f"**{team_name(s, e_['a'])}** vs **{team_name(s, e_['b'])}**\n"
                                         f"**Game time:** {ts(dt)} ({ts(dt, 'R')})\nSet by {by}.",
                          f"✅ M{mid} is scheduled", GOOD)
    sch = chan(guild, "schedule")
    if sch:
        await post(sch, f"**M{mid}** · {e_['label']}: {tag(e_['a'])} vs {tag(e_['b'])} · {ts(dt)}",
                   title="Game time set", color=GOOD)
    await dm_teams(guild, s, [e_["a"], e_["b"]], lambda tid: next_match_card(s, mid, tid))
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
    groups = slot_options(now, end, tz_code)
    if not groups:
        return await interaction.response.send_message("There are no times left before the deadline. Ask staff "
                                                       "to /setgametime.", ephemeral=True)
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
    await scheduling_post(guild, s, mid, f"**{team_name(s, e_[side])}** asked **{team_name(s, e_[other_side])}** "
                                         f"to play M{mid} at one of these times:\n{listing}\n\n"
                                         f"<@{to_team['captain']}>, check your DMs to confirm.",
                          f"🕒 Game time request · M{mid}", INFO)
    tz_to = sc["tz"].get(str(to_team["captain"]), draft["tz"])
    now = datetime.now(timezone.utc)
    end = min(max(window_end(e_), now + timedelta(hours=2)), now + timedelta(hours=SCHED_HOURS))
    e = brand_embed(f"**{team_name(s, e_[side])}** want to play **M{mid}** ({e_['label']}) at one of these times "
                    f"(shown in your local time):\n{listing}\n\nPick one below to lock it in. If none work, "
                    f"suggest another time from the other dropdowns.\nDeadline: {ts(datetime.fromisoformat(e_['deadline']))}",
                    f"Confirm your game time · {guild.name}", GOLD)
    ok = await dm(int(to_team["captain"]), e,
                  SlotPicker(guild.id, rid, slot_options(now, end, tz_to, times), "answer", times, tz_to))
    return ("Request sent! The other captain got a DM to confirm." if ok else
            "Request posted in #scheduling, but I couldn't DM the other captain (DMs closed). They can still "
            f"answer with `/gametime match:{mid}`.")


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
        await scheduling_post(guild, s, r["match"], f"**{team_name(s, r['to_team'])}** suggested {when} for "
                                                    f"M{r['match']}. <@{r['from']}>, check your DMs.",
                              f"🔁 Counter-offer · M{r['match']}", INFO)
        return await interaction.followup.send(f"Sent {when} to the other captain. You'll hear back here.")
    if action == "yes" and uid == r["to"]:
        await interaction.response.edit_message(view=None)
        await confirm_time(guild, data, r["match"], r["times"][0], f"<@{r['from']}> and <@{r['to']}>")
        return await interaction.followup.send("✅ Locked in. Both teams have been told.")
    if action == "no" and uid == r["to"]:
        r["status"] = "declined"
        save_data(data)
        await interaction.response.edit_message(view=None)
        await scheduling_post(guild, s, r["match"], f"No time agreed yet for M{r['match']}. Either captain can "
                                                    f"send new times with `/gametime match:{r['match']}`.",
                              f"✖ Time declined · M{r['match']}", MUTED)
        return await interaction.followup.send(f"Declined. Send your own times with `/gametime match:{r['match']}`.")
    await interaction.response.send_message("This isn't your request to answer.", ephemeral=True)


@bot.tree.command(description="Staff: the game time the bot sets when captains don't agree one in 48 hours.")
@app_commands.describe(time="Clock time as HH:MM (24-hour), e.g. 18:00 for 6 PM", timezone="Timezone (default ET)")
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
        f"If captains don't agree a time within 48 hours, the bot sets the match for the next day at "
        f"**{sc['preset']['time']} {timezone}**. They can still move it with /gametime if both confirm.",
        ephemeral=True)


@bot.tree.command(description="Staff: set a match's game time directly.")
@app_commands.describe(match="Match number", date="Date as YYYY-MM-DD", time="Time as HH:MM (24-hour), e.g. 19:30",
                       timezone="Timezone of that time (default ET)")
@app_commands.choices(timezone=TZ_CHOICES)
@app_commands.default_permissions(manage_roles=True)
async def setgametime(interaction: discord.Interaction, match: int, date: str, time: str, timezone: str = "ET"):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only staff can do that.", ephemeral=True)
    try:
        when = datetime.strptime(f"{date.strip()} {time.strip()}", "%Y-%m-%d %H:%M").replace(tzinfo=tzinfo(timezone))
    except ValueError:
        return await interaction.response.send_message("Use date like 2026-11-14 and time like 19:30.", ephemeral=True)
    data = load_data()
    e_ = sched(guild_signups(data, interaction.guild.id))["matches"].get(str(match))
    if not e_ or e_["done"]:
        return await interaction.response.send_message(f"M{match} isn't an open match.", ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    await confirm_time(interaction.guild, data, str(match), int(when.timestamp()), interaction.user.mention)
    await interaction.followup.send(f"M{match} set for {ts(when)}.", ephemeral=True)


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


REMINDERS = [(24 * 3600, "24h", "in 24 hours"), (3600, "1h", "in 1 hour"), (0, "now", "now")]


async def match_watch_once(guild: discord.Guild):
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
            for secs, key, words in reversed(REMINDERS):  # latest due reminder first
                if key not in e_["reminded"] and now >= gt - timedelta(seconds=secs) and now < gt + timedelta(minutes=30):
                    # only send the latest reminder that's due (no 24h reminder an hour before the game)
                    e_["reminded"] += [k for _s, k, _w in REMINDERS if _s >= secs]
                    changed = True
                    await dm_teams(guild, s, [e_["a"], e_["b"]], lambda tid, w=words, mm=mid: next_match_card(
                        s, mm, tid, f"\n\n⏰ **Your game starts {w}.** Be in the {team_name(s, tid)} voice channel "
                                    "and ready to join the private server."))
                    if key == "now":
                        await scheduling_post(guild, s, mid, f"**M{mid}** {team_name(s, e_['a'])} vs "
                                                             f"{team_name(s, e_['b'])} starts now. Good luck!",
                                              "🏀 Game time", GOOD)
                    break
        else:
            dl = datetime.fromisoformat(e_["deadline"])
            if "12h" not in e_["reminded"] and now >= dl - timedelta(hours=12) and now < dl:
                e_["reminded"].append("12h")
                changed = True
                await scheduling_post(guild, s, mid, f"**12 hours left** to agree a time for M{mid}. "
                                                     f"Use `/gametime match:{mid}`.", f"⏳ M{mid} deadline soon", GOLD)
            if now >= dl:
                preset = preset_time(sc, dl)
                e_["time"], e_["preset"], e_["reminded"] = preset.isoformat(timespec="seconds"), True, []
                changed = True
                await scheduling_post(guild, s, mid, f"No time was agreed in 48 hours, so **M{mid}** "
                                                     f"({team_name(s, e_['a'])} vs {team_name(s, e_['b'])}) is set for "
                                                     f"**{ts(preset)}** ({ts(preset, 'R')}).\n\nWant it earlier or "
                                                     f"later? Use `/gametime match:{mid}`. It only changes if both "
                                                     "captains confirm.", f"🕕 M{mid} preset time", GOLD)
                await dm_teams(guild, s, [e_["a"], e_["b"]], lambda tid, mm=mid: next_match_card(s, mm, tid))
    if changed:
        save_data(data)


async def match_watch():
    await bot.wait_until_ready()
    while not bot.is_closed():
        for guild in bot.guilds:
            try:
                await match_watch_once(guild)
            except Exception as e:
                print(f"[match reminders] {e}")
        await asyncio.sleep(60)


async def post_rules(channel: discord.TextChannel):
    for i, (title, color, rules) in enumerate(RULE_CARDS):
        e = brand_embed("\n".join(f"**{n}.** {r}" for n, r in enumerate(rules, 1)), title, color)
        if i == len(RULE_CARDS) - 1:
            e.description += "\n\nBy playing in the circuit you agree to these rules. Questions? Open a ticket."
        await channel.send(embed=e)


@bot.tree.command(description="Staff: wipe #rules and post the current circuit rules.")
@app_commands.default_permissions(manage_messages=True)
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


@bot.tree.command(description="Staff: give every team that doesn't have one its own voice channel.")
@app_commands.default_permissions(manage_channels=True)
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
        out["groups"] = {"advance": gs["advance"], "list": lst}
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
    return out


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
    for key, t in team_list(s):
        if not is_complete(t):
            continue  # only complete rosters go on the website
        teams.append({"name": t["name"], "logo": f"logos/{t['logo']}" if t.get("logo") else None,
                      "captain": player(t["captain"]) + pos_tag(s, t["captain"]),
                      "players": [player(u) + pos_tag(s, u) for u in t["roster"] if int(u) != t["captain"]],
                      "points": t.get("points", 0), "qualified": major_qualified(s, key),
                      "registered": bool(tz and key in tz.get("entrants", []))})
    data = {"league": LEAGUE_NAME, "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "teams": teams,
            "circuit": {"needed": c["needed"],
                        "standings": sorted(({"team": t["name"], "points": t["points"], "qualified": t["qualified"]}
                                             for t in teams), key=lambda r: -r["points"])},
            "tourney": ({"name": tz["name"], "kind": tz["kind"], "open": s["open"], "closes": s.get("closes"),
                         "logo": f"logos/{tz['logo']}" if tz.get("logo") else None,
                         "winner_qualifies": tz.get("winner_qualifies", tz.get("kind") != "major"),
                         "points": spec_text(tz["spec"]) if tz.get("spec") else None,
                         "entrants": [name(int(k)) for k in tz["entrants"] if k in s["teams"]]} if tz else None)}
    def avatar(uid):
        m = guild.get_member(int(uid)) if str(uid).isdigit() else None
        return m.display_avatar.url if m else None

    data.update(event_site_data(s["event"], name, player, avatar))
    current = player_totals(s["event"], player, name, avatar)
    year = datetime.now().year
    past = [h["players"] for h in s.get("history", []) if h.get("year") == year]
    data["stats"] = {"tournament_name": tz["name"] if tz else "Current tournament",
                     "tournament": list(current.values()),
                     "year_label": str(year), "year": list(merge_totals(*past, current).values())}
    if s["open"] and not s["event"]:
        data["stage"] = "signups"
    data["final"] = final_rows(s["event"], tz or {}, name)
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


async def publish_site(guild: discord.Guild) -> str:
    """Push index.html + data.js to GitHub. Returns a short status message."""
    if not (GITHUB_TOKEN and GITHUB_REPO):
        return "Website is off: set GITHUB_TOKEN and GITHUB_REPO before starting the bot."
    if not SITE_TEMPLATE.exists():
        return "Website: pbl_site.html is missing. Put it in the same folder as pbl_bot.py."
    js = "window.PBL_DATA = " + json.dumps(site_data(guild), indent=1) + ";\n"
    try:
        async with aiohttp.ClientSession() as session:
            global _cname_done
            if SITE_DOMAIN and not _cname_done:  # keeps GitHub Pages serving the site on the custom domain
                await github_put(session, "CNAME", (SITE_DOMAIN + "\n").encode(), "Custom domain")
                _cname_done = True
            await github_put(session, "index.html", SITE_TEMPLATE.read_bytes(), "Update site")
            gs = guild_signups(load_data(), guild.id)
            for _k, t in team_list(gs) + [("tourney", gs.get("tourney") or {})]:
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
            await github_put(session, "data.js", js.encode("utf-8"), "Update tournament data")
        _last_publish[guild.id] = datetime.now().strftime("%H:%M:%S")
        return f"Website updated: {site_url()} (GitHub can take about a minute to show changes)"
    except Exception as e:  # never let a website problem break the tournament commands
        print(f"[website] {e}")
        return f"Website update failed: {e}"


def schedule_publish(guild: discord.Guild, delay: float = 5.0):
    """Publish a few seconds after the last change, so a burst of results makes one update."""
    if not (GITHUB_TOKEN and GITHUB_REPO):
        return
    old = _publish_tasks.get(guild.id)
    if old and not old.done():
        old.cancel()

    async def later():
        try:
            await asyncio.sleep(delay)
            msg = await publish_site(guild)
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
    if s["open"]:
        return "Entries are still open. Run /closesignups first."
    if len(teams) < MIN_TEAMS:
        return f"There are {len(teams)} registered team(s). A tournament needs {MIN_TEAMS}."
    if s["event"] and s["event"]["stage"] != "done" and not redraw:
        return ("A tournament is already running. To throw it away and start over, "
                "run the command again with redraw set to True.")
    return None


def new_event(stage: str) -> dict:
    return {"stage": stage, "next_id": 1, "swiss": None, "groups": None, "main": None}


async def start_main(guild: discord.Guild, ev: dict, seeds: list[int], note: str):
    """Build the double-elimination main draw, post it, and post the first matches."""
    if len(seeds) == 1:
        ev["stage"] = "done"
        ev["main"] = {"matches": [], "champion": seeds[0]}
        ann = chan(guild, "announcements")
        if ann:
            await post(ann, f"**{tag(seeds[0])} are the champions!** (only team to qualify)",
                           allowed_mentions=NO_PINGS)
        return
    ev["main"] = de_build(ev, seeds)
    ev["stage"] = "main"
    de_resolve(ev["main"])
    seed_lines = "\n".join(f"#{i}: {tag(t)}" for i, t in enumerate(seeds, 1))
    parts = [f"# Main draw: double elimination\n{note}\nLose twice and you're out. "
             "The Grand Final has a reset if the Losers bracket team wins the first game.",
             f"**Seeds**\n{seed_lines}"]
    parts += de_overview(ev["main"])
    nxt = up_next(ev["main"])
    if nxt:
        parts.append("# Play now\n" + "\n".join(nxt))
    await send_blocks(chan(guild, "bracket"), parts)


@bot.tree.command(description="Start a Swiss qualifier: win enough to make the main draw, lose enough and you're out.")
@app_commands.describe(wins="Wins needed to qualify (default 3)", losses="Losses that knock a team out (default 3)",
                       redraw="Set to True to throw away a running tournament and start over")
@app_commands.default_permissions(manage_roles=True)
async def startswiss(interaction: discord.Interaction, wins: app_commands.Range[int, 1, 5] = 3,
                     losses: app_commands.Range[int, 1, 5] = 3, redraw: bool = False):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can start a tournament.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    teams = entrant_roles(guild)
    problem = event_problem(s, teams, redraw)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)

    ids = [t.id for t in teams]
    s["event"] = ev = new_event("swiss")
    ev["swiss"] = swiss_new(ids, wins, losses)
    round_lines = swiss_next_round(ev)
    save_data(data)
    schedule_publish(guild)

    restart = " (RESTARTED: ignore the earlier draw)" if redraw else ""
    await send_blocks(chan(guild, "schedule"), [
        f"# Swiss qualifier{restart}\n{len(ids)} teams. **{wins} wins** = into the double-elimination main draw. "
        f"**{losses} losses** = out. Each round you play a team with the same record.\n"
        "Captains: agree a time in #scheduling, play, then post the score in #score-reports. "
        "A Referee records it with /result.",
        "\n".join(round_lines)])
    await send_blocks(chan(guild, "standings"), swiss_table(ev["swiss"]))
    ann = chan(guild, "announcements")
    if ann:
        await post(ann, f"**The Swiss qualifier has started!**{restart} Round 1 matchups are in #schedule.")
    await interaction.followup.send("Swiss stage started. Round 1 is posted in #schedule.", ephemeral=True)


@bot.tree.command(description="Start a group stage: random groups of 4, top teams go to the main draw.")
@app_commands.describe(advance="Teams from each group that make the main draw (default 2)",
                       redraw="Set to True to throw away a running tournament and start over")
@app_commands.default_permissions(manage_roles=True)
async def startgroups(interaction: discord.Interaction, advance: app_commands.Range[int, 1, 3] = 2,
                      redraw: bool = False):
    guild = interaction.guild
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can start a tournament.", ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    teams = entrant_roles(guild)
    problem = event_problem(s, teams, redraw)
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)

    s["event"] = ev = new_event("groups")
    gs = ev["groups"] = groups_new(ev, [t.id for t in teams], advance)
    save_data(data)
    schedule_publish(guild)

    restart = " (RESTARTED: ignore the earlier draw)" if redraw else ""
    n_groups = len(gs["groups"])
    await send_blocks(chan(guild, "standings"), [
        f"# Group stage draw{restart}\n{len(teams)} teams drawn at random into {n_groups} group(s). "
        f"Everyone plays everyone in their group once. **Top {advance}** in each group go to the "
        "double-elimination main draw.\nTiebreakers: wins, then head-to-head, then point difference."]
        + [group_blocks(gs, gi) for gi in range(n_groups)])

    rounds = max(m["round"] for m in gs["matches"])
    parts = [f"# Group stage schedule{restart}\n{rounds} rounds. Captains: agree a time in #scheduling, "
             "play, then post the score in #score-reports. A Referee records it with /result."]
    for r in range(1, rounds + 1):
        lines = [f"## Round {r}"]
        for gi, g in enumerate(gs["groups"]):
            playing = set()
            for m in gs["matches"]:
                if m["group"] == gi and m["round"] == r:
                    lines.append(f"**M{m['id']}** Group {group_letter(gi)}: {tag(m['a'])} vs {tag(m['b'])}")
                    playing.update((m["a"], m["b"]))
            for t in g:
                if t not in playing:
                    lines.append(f"Group {group_letter(gi)}: {tag(t)} has a bye")
        parts.append("\n".join(lines))
    await send_blocks(chan(guild, "schedule"), parts)
    ann = chan(guild, "announcements")
    if ann:
        await post(ann, f"**The group stage draw is out!**{restart} Groups are in #standings, "
                       "matchups in #schedule.")
    await interaction.followup.send("Group stage started. Groups are in #standings, schedule in #schedule.",
                                    ephemeral=True)


@bot.tree.command(description="Start the double-elimination main draw.")
@app_commands.describe(redraw="Set to True to throw away a running main draw and start over")
@app_commands.default_permissions(manage_roles=True)
async def startmain(interaction: discord.Interaction, redraw: bool = False):
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
        ev["main"] = None
    else:
        teams = entrant_roles(guild)
        problem = event_problem(s, teams, redraw)
        if problem:
            return await interaction.response.send_message(problem, ephemeral=True)
        seeds = [t.id for t in teams]
        RNG.shuffle(seeds)
        s["event"] = ev = new_event("main")
        note = f"{len(seeds)} teams, no qualifier, seeded at random."

    await interaction.response.defer(ephemeral=True, thinking=True)
    await start_main(guild, ev, seeds, note)
    save_data(data)
    schedule_publish(guild)
    ann = chan(guild, "announcements")
    if ann:
        await post(ann, "**The main draw has started!** Check #bracket for your first match.")
    await interaction.followup.send("Main draw posted in #bracket.", ephemeral=True)


@bot.tree.command(description="Record who won a match.")
@app_commands.describe(match="Match number, e.g. 7 for M7", winner="The winning team's role",
                       score="Final score, e.g. 42-38 (optional, used for group tiebreakers)")
async def result(interaction: discord.Interaction, match: int, winner: discord.Role, score: str | None = None):
    guild = interaction.guild
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only Referees and league staff can record results.",
                                                       ephemeral=True)
    data = load_data()
    s = guild_signups(data, guild.id)
    ev = s["event"]
    if not ev or ev["stage"] == "done":
        return await interaction.response.send_message("No tournament is running.", ephemeral=True)

    sw_match = next((m for m in (ev.get("swiss") or {}).get("matches", []) if m["id"] == match), None)
    gr_match = next((m for m in (ev.get("groups") or {}).get("matches", []) if m["id"] == match), None)
    de_match = next((m for m in (ev.get("main") or {}).get("matches", []) if m["id"] == match), None)
    m = sw_match or gr_match or de_match
    problem = None
    if m is None:
        problem = f"There's no match M{match}."
    elif ((sw_match or gr_match) and m["winner"]) or (de_match and de_match["done"]):
        problem = f"M{match} already has a result. Ask staff if it needs fixing."
    elif de_match and not (de_match["a_ok"] and de_match["b_ok"]):
        problem = f"M{match} can't be played yet: it's still waiting on earlier matches."
    elif sw_match and ev["stage"] != "swiss":
        problem = f"M{match} is from the finished Swiss stage."
    elif gr_match and ev["stage"] != "groups":
        problem = f"M{match} is from the finished group stage."
    elif winner.id not in (m["a"], m["b"]):
        problem = f"{winner.mention} isn't playing in M{match}."
    if problem:
        return await interaction.response.send_message(problem, ephemeral=True,
                                                       allowed_mentions=NO_PINGS)
    await interaction.response.defer(ephemeral=True)

    loser = m["b"] if winner.id == m["a"] else m["a"]
    season_over = False
    pts = parse_score(score)
    m["score"] = f"{pts[0]}-{pts[1]}" if pts else (score or None)
    score_txt = f" {m['score']}" if m["score"] else ""
    result_line = f"**M{match} result**: {tag(winner.id)} beat {tag(loser)}{score_txt}"

    if sw_match:
        sw = ev["swiss"]
        sw_match["winner"] = winner.id
        swiss_record(sw, winner.id, loser)
        parts = [result_line]
        if all(x["winner"] for x in sw["matches"] if x["round"] == sw["round"]):
            await send_blocks(chan(guild, "standings"), swiss_table(sw))
            if swiss_active(sw):
                parts.append("\n".join(swiss_next_round(ev)))
            else:
                ev["stage"] = "swiss_done"
                q = ", ".join(tag(t) for t in sw["qualified"]) or "none"
                parts.append(f"# Swiss stage complete\n**Into the main draw ({len(sw['qualified'])}):** {q}\n"
                             "Staff: run /startmain to post the double-elimination bracket.")
        await send_blocks(chan(guild, "schedule"), parts)

    elif gr_match:
        gs = ev["groups"]
        gr_match["winner"], gr_match["pts"] = winner.id, list(pts) if pts else None
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
        await send_blocks(chan(guild, "schedule"), parts)

    else:
        main = ev["main"]
        parts = [result_line + f" ({de_match['label']})"]
        if de_record(ev, de_match, winner.id, loser):
            parts.append("The Losers bracket team won, so the Grand Final resets: one more game decides it!")
        if main["champion"]:
            ev["stage"] = "done"
            tz = s.get("tourney") or {}
            tname = tz.get("name", "the tournament")
            parts.append(f"# {tag(main['champion'])} win {tname}!")
            await send_blocks(chan(guild, "standings"), award_points(s, ev))
            ann = chan(guild, "announcements")
            if ann:
                await post(ann, f"**{tag(main['champion'])}** are the champions of **{tname}**! Congratulations!\n"
                               "Final standings and RISER POINTS are in #standings.", title=f"{tname} champions",
                           color=GOLD, file=logo_file(s["teams"].get(str(main["champion"]), {})))
            season_over = True
        else:
            nxt = up_next(main)
            if nxt:
                parts.append("**Up next**\n" + "\n".join(nxt))
        await send_blocks(chan(guild, "bracket"), parts)

    await post_score_card(guild, s, ev, m, interaction.user.id)  # the Final Score card in #score-reports
    save_data(data)
    schedule_publish(guild)
    await interaction.followup.send(f"Recorded: M{match} won by {winner.mention}.", ephemeral=True,
                                    allowed_mentions=NO_PINGS)
    if season_over:
        await serve_tournament(guild, tname)  # tournament suspensions count down by one
        await update_board(guild)  # new RISER POINTS on the team cards and website
        asyncio.create_task(season_end(guild))  # DM every player: stay or leave?  # DM every player: stay or leave?


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
    data = load_data()
    guild_signups(data, interaction.guild.id)["event"] = None
    save_data(data)
    schedule_publish(interaction.guild)
    await interaction.response.send_message(
        "Tournament cleared. Start again with /startswiss, /startgroups or /startmain.", ephemeral=True)


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
