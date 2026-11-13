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
  /freeagent                     Turn the Free Agent role on or off

  RISER POINTS
  - Each circuit event gives points by placement (set per tournament in /opensignups).
  - Tournament winners qualify for the Major automatically; others need the target set with /setmajor.
  - If fewer than 3 of the players who earned a team's points are still on it, the points are lost.
  - When a Major finishes, everyone's points reset to 0.

  Staff
  /setup                         Build roles, channels, permissions, rules + welcome posts (safe to run again)
  /giveplayerrole                Give the Player role to everyone already in the server
                                 (new members get it automatically when they join)
  /setmajor points_needed        RISER POINTS needed to qualify for the Major
  /opensignups name kind points [closes]
                                 Open entries for a tournament. kind = Circuit event or Major.
                                 points = placement table, e.g. "1:100, 2:70, 3:50, 4:40, 5-6:25, 7-8:15"
  /closesignups                  Close entries (needs 6+ complete teams)
  /setpoints team points, /resetpoints confirm:True
  /setlogo team logo, /addteam, /removeteam, and /sign and /release with a team option
  /signuplist, /rosterboard      Registered teams / re-send the team cards in #rosters
  /endseason confirm:True        End a tournament early and send the stay-or-leave DMs
  /testtournament [teams] [style] [publish]
                                 Play a whole fake tournament (2 to 64 teams) with made-up team names, logos,
                                 players and box scores, and random results. Posts it
                                 in #staff-chat. Real teams and points aren't touched. publish:True also puts
                                 it on the website's /test/ page.

  Tournament
  /startswiss [wins] [losses]   Optional Swiss qualifier (default: 3 wins = qualify, 3 losses = out).
  /startgroups [advance]        Optional group stage: random groups of 4, top 2 (or 1 or 3) qualify.
  /startmain                    The main draw, always double elimination, posted in #bracket.
  /result match winner [score]  Referees/staff: record a result. Next matches post automatically. When the
                                  champion is crowned, RISER POINTS are awarded (or reset after a Major) and
                                  every player is DMed with Stay / Leave buttons.
  /stat match player points [rebounds] [assists] [steals] [blocks]
                                Referees/staff: enter a player's box score for a game (run again to fix it).
                                The website shows box scores when you click a game, plus tournament and
                                full-year stat leaders.
  /matches                      List the matches waiting to be played
  /resetevent confirm:True      Delete the current tournament and start over
  /website                      Push the circuit website now and show its link

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
import json
import os
import random
import re
import secrets
from datetime import datetime, timezone
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

RULES_TEXT = """**Server rules**
1. Be respectful. No harassment, slurs, or targeting other players.
2. No cheating, exploits, or scripts in circuit games.
3. Keep chat in the right channel.
4. No spam, self-promo, or DM advertising.
5. Follow Discord's Terms of Service and Roblox's Community Standards.
6. Staff decisions are final. Appeal politely in #match-disputes.

**Circuit rules**
1. Rosters: 5 to 8 players. Roster changes lock while a main draw is being played.
2. One team per player. Playing on two teams gets both accounts suspended.
3. Scheduling: captains agree on a time in #scheduling. Play by the deadline staff set.
4. Forfeits: a team that doesn't show within 15 minutes of the agreed time forfeits. Two forfeits = removed.
5. Score reports: the winning captain posts the final score and a screenshot in #score-reports within 1 hour.
6. Disputes: post in #match-disputes within 24 hours with evidence (clip or screenshot). A Referee decides.
7. Game settings: the same settings for every circuit game. Staff set them before each tournament.
8. A tournament needs at least 6 teams.

**RISER POINTS**
1. Every circuit event awards RISER POINTS by final placement. Staff post the points table when entries open.
2. Tournament winners qualify for the Major automatically. Other teams qualify by reaching the points target.
3. Points belong to the players who earned them: if fewer than 3 of them stay on the team, the points are lost.
4. After each Major, every team's RISER POINTS reset to 0."""

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
    await post_once(discord.utils.get(guild.text_channels, name="rules"), RULES_TEXT)

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


async def log_transaction(guild: discord.Guild, text: str):
    ch = discord.utils.get(guild.text_channels, name="transactions")
    if ch:
        await post(ch, text, title="Transaction", color=INFO)


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
    s["teams"][key] = {"name": name, "captain": captain.id, "logo": logo, "channel": channel.id,
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
    ch = guild.get_channel(t.get("channel") or 0)
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
    await log_transaction(guild, f"Team removed: **{t['name']}** ({reason})")


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
    await log_transaction(guild, text)
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
        lines.append(f"**Major:** {c['needed']} RISER POINTS to qualify. Tournament winners qualify automatically.")
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
    players = [f"<@{u}>{' (C)' if int(u) == t['captain'] else ''}" for u in t["roster"]]
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
                       kind="Circuit event (awards RISER POINTS) or Major (qualified teams only)",
                       points="Points per placement, e.g. 1:100, 2:70, 3:50, 4:40, 5-6:25, 7-8:15",
                       closes="When entries close, e.g. 'Friday at 8pm' (optional)")
@app_commands.choices(kind=[
    app_commands.Choice(name="Circuit event (awards RISER POINTS)", value="event"),
    app_commands.Choice(name="Major (qualified teams only, points reset after)", value="major"),
])
@app_commands.default_permissions(manage_roles=True)
async def opensignups(interaction: discord.Interaction, name: str, kind: str = "event",
                      points: str | None = None, closes: str | None = None):
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
        spec, problem = parse_spec(points or DEFAULT_SPEC)
        if problem:
            return await interaction.response.send_message(problem, ephemeral=True)
    await interaction.response.defer(ephemeral=True)
    archive_event(guild, s)  # keep last tournament's player stats for the year table
    s["tourney"] = {"name": name.strip()[:60], "kind": kind, "spec": spec, "entrants": []}
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
                "The winner qualifies for the Major automatically.")
        if c["needed"] is not None:
            text += f" Everyone else needs **{c['needed']} RISER POINTS**."
    text += (f"\nCaptains: type `/register` to enter (you need {ROSTER_MIN}+ players). "
             "Your points and what you still need are shown when you register.")
    if closes:
        text += f"\nEntries close **{closes}**."
    text += "\nNo team yet? `/signup` to start one, or `/freeagent` to get found."
    ann = chan(guild, "announcements")
    if ann:
        await post(ann, text)
    await interaction.followup.send(f"**{name}** is open for entries and announced.", ephemeral=True)


@bot.tree.command(description="Anyone: start a team. You become its captain.")
@app_commands.describe(team_name="Your team's name", logo="Your team logo (PNG, JPG, WEBP or GIF, under 1 MB)")
async def signup(interaction: discord.Interaction, team_name: str, logo: discord.Attachment):
    guild, user = interaction.guild, interaction.user
    data = load_data()
    s = guild_signups(data, guild.id)
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
    await interaction.response.defer(ephemeral=True, thinking=True)
    filename, problem = await save_logo(logo)
    if problem:
        return await interaction.followup.send(problem, ephemeral=True)
    key = await create_team(guild, data, team_name, user, filename)
    await log_transaction(guild, f"New team: **{team_name}**, captain {user.mention}")
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
    await log_transaction(guild, f"**{t['name']}** signed <@{uid}>")
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
    await log_transaction(guild, f"{player.mention} is now captain of **{t['name']}**")
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
    await create_team(guild, data, name, captain, filename)
    await log_transaction(guild, f"New team: **{name}**, captain {captain.mention} (added by staff)")
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
async def freeagent(interaction: discord.Interaction):
    guild, user = interaction.guild, interaction.user
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
    spec = tz.get("spec") or parse_spec(DEFAULT_SPEC)[0]
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
    if champ in s["teams"] and champ not in c["qualified"]:
        c["qualified"].append(champ)
        lines.append(f"{tag(int(champ))} won the tournament and **qualified for the Major**.")
    return lines


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
    await log_transaction(interaction.guild, f"Staff set **{t['name']}** to {points} RISER POINTS")
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
    await log_transaction(guild, f"**{t['name']}** registered for **{tz['name']}** · {line}")
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


@bot.tree.command(description="Staff: run a whole practice tournament with fake teams. Real teams aren't touched.")
@app_commands.describe(teams="How many fake teams (2 to 64)", style="Qualifier to test",
                       publish="Also publish it to the website's /test/ page")
@app_commands.choices(style=[
    app_commands.Choice(name="Group stage then double elimination", value="groups"),
    app_commands.Choice(name="Swiss then double elimination", value="swiss"),
    app_commands.Choice(name="Double elimination only", value="none"),
])
@bot.tree.command(description="Staff: run a whole practice tournament with fake teams. Real teams aren't touched.")
@app_commands.describe(teams="How many fake teams (2 to 64)", style="Qualifier to test",
                       publish="Also publish it to the website's /test/ page")
@app_commands.choices(style=[
    app_commands.Choice(name="Group stage then double elimination", value="groups"),
    app_commands.Choice(name="Swiss then double elimination", value="swiss"),
    app_commands.Choice(name="Double elimination only", value="none"),
])
@app_commands.default_permissions(manage_roles=True)
async def testtournament(interaction: discord.Interaction, teams: app_commands.Range[int, 2, 64] = 16,
                         style: str = "groups", publish: bool = False):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can run tests.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    guild = interaction.guild
    rng = random.Random()
    ids = [9_000_000_000_000_000 + i for i in range(1, teams + 1)]
    names, rosters = fake_league(teams, rng)
    TEST_NAMES.clear()
    TEST_NAMES.update(dict(zip(ids, names)))

    def box(m, w, lo, wp, lp):
        m["box"] = {**fake_box(w, rosters[TEST_NAMES[w]], wp, rng), **fake_box(lo, rosters[TEST_NAMES[lo]], lp, rng)}

    ev = simulate(ids, style, rng, box)

    s = guild_signups(load_data(), guild.id)
    tz = s.get("tourney") or {}
    spec = tz.get("spec") or parse_spec(DEFAULT_SPEC)[0]
    parts = [f"# TEST TOURNAMENT ({teams} fake teams)\nNothing here is real: no teams, points or results were "
             f"changed. Points table used: {spec_text(spec)}"]
    if ev.get("swiss"):
        sw = ev["swiss"]
        parts.append(f"**Swiss:** {sw['round']} rounds, {len(sw['matches'])} games. Qualified: "
                     + ", ".join(tag(t) for t in sw["qualified"]))
    if ev.get("groups"):
        gs = ev["groups"]
        parts += [group_blocks(gs, gi) for gi in range(len(gs["groups"]))]
    lines = ["**Main draw (double elimination)**"]
    for m in ev["main"]["matches"]:
        if m["done"] and m["loser"] is not None:
            lines.append(f"M{m['id']} {m['label']}: {tag(m['winner'])} beat {tag(m['loser'])} {m.get('score') or ''}")
    for i in range(0, len(lines), 25):
        parts.append("\n".join(lines[i:i + 25]))
    standing = ["**Final standings and RISER POINTS they would earn**"]
    for place, tids in final_standings(ev):
        standing.append(f"{place_label(place, len(tids))}: " + ", ".join(tag(t) for t in tids)
                        + f"  +{spec.get(str(place), 0)}")
    standing.append(f"Champion: {tag(ev['main']['champion'])} (would qualify for the Major)")
    for i in range(0, len(standing), 25):
        parts.append("\n".join(standing[i:i + 25]))
    totals = player_totals(ev, str, lambda tid: TEST_NAMES.get(tid, "?"))
    top = sorted(totals.values(), key=lambda r: -r["pts"] / max(1, r["gp"]))[:5]
    parts.append("**Top scorers (points per game)**\n" + "\n".join(
        f"{i}. {r['player']} ({r['team']}): {r['pts'] / r['gp']:.1f} PPG over {r['gp']} games"
        for i, r in enumerate(top, 1)))
    await send_blocks(chan(guild, "staff-chat") or interaction.channel, parts)
    gf = [m for m in ev["main"]["matches"] if m["gf"] and m["done"] and m["loser"] is not None]
    if gf:  # a sample Final Score card, so you can see what result posts look like
        card = score_card({"tourney": {"name": "TEST tournament"}}, ev, gf[-1], interaction.user.id)
        card.url = f"{site_url()}test/#m{gf[-1]['id']}" if site_url() else None
        await (chan(guild, "staff-chat") or interaction.channel).send(embed=card, allowed_mentions=NO_PINGS)

    note = ""
    if publish:
        note = "\n" + await publish_test_site(guild, ev, spec, rosters, rng)
    TEST_NAMES.clear()
    await interaction.followup.send(f"Test tournament finished: {len(ev['main']['matches'])} main-draw matches. "
                                    f"Full results are in #staff-chat.{note}", ephemeral=True)


# ---------------------------------------------------------------- player stats
#
# A match can carry a box score: m["box"] = {player key: {"team": team id, "pts", "reb", "ast", "stl", "blk"}}
# (player key = Discord ID for real games, a made-up name in test tournaments).
# When a new tournament opens, the finished one's player totals are saved in s["history"] for the year table.

STAT_KEYS = ["pts", "reb", "ast", "stl", "blk"]


def all_matches(ev: dict | None) -> list[dict]:
    if not ev:
        return []
    out = []
    for part in ("swiss", "groups", "main"):
        out += (ev.get(part) or {}).get("matches", [])
    return out


def player_totals(ev: dict | None, pname, tname) -> dict:
    """{player key: {player, team, gp, pts, reb, ast, stl, blk}} for one tournament."""
    tot = {}
    for m in all_matches(ev):
        for key, line in (m.get("box") or {}).items():
            row = tot.setdefault(str(key), {"player": pname(key), "team": tname(line["team"]), "gp": 0,
                                            **{k: 0 for k in STAT_KEYS}})
            row["team"] = tname(line["team"])
            row["gp"] += 1
            for k in STAT_KEYS:
                row[k] += line.get(k, 0)
    return tot


def merge_totals(*tables: dict) -> dict:
    out = {}
    for table in tables:
        for key, r in table.items():
            row = out.setdefault(key, {"player": r["player"], "team": r["team"], "gp": 0, **{k: 0 for k in STAT_KEYS}})
            row["player"], row["team"] = r["player"], r["team"]
            row["gp"] += r["gp"]
            for k in STAT_KEYS:
                row[k] += r[k]
    return out


def box_rows(m: dict, pname, tname) -> list[dict]:
    return [{"player": pname(k), "team": tname(v["team"]), **{s: v.get(s, 0) for s in STAT_KEYS}}
            for k, v in (m.get("box") or {}).items()]


def archive_event(guild: discord.Guild, s: dict):
    """Save the last tournament's player totals before a new one replaces it."""
    ev = s.get("event")
    if not ev or not any(m.get("box") for m in all_matches(ev)):
        return
    tz = s.get("tourney") or {}

    def pname(k):
        mem = guild.get_member(int(k)) if str(k).isdigit() else None
        return mem.display_name if mem else str(k)

    def tname(tid):
        t = s["teams"].get(str(tid))
        return t["name"] if t else "Former team"

    s.setdefault("history", []).append({
        "name": tz.get("name", "Tournament"), "kind": tz.get("kind", "event"),
        "year": datetime.now().year, "date": datetime.now(timezone.utc).date().isoformat(),
        "players": player_totals(ev, pname, tname)})


@bot.tree.command(description="Referees/staff: enter one player's stats for a match.")
@app_commands.describe(match="Match number, e.g. 7 for M7", player="The player",
                       points="Points", rebounds="Rebounds", assists="Assists", steals="Steals", blocks="Blocks")
async def stat(interaction: discord.Interaction, match: int, player: discord.Member,
               points: app_commands.Range[int, 0, 300], rebounds: app_commands.Range[int, 0, 200] = 0,
               assists: app_commands.Range[int, 0, 200] = 0, steals: app_commands.Range[int, 0, 200] = 0,
               blocks: app_commands.Range[int, 0, 200] = 0):
    if not is_official(interaction.user):
        return await interaction.response.send_message("Only Referees and league staff can enter stats.",
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
    m.setdefault("box", {})[str(player.id)] = {"team": team, "pts": points, "reb": rebounds, "ast": assists,
                                               "stl": steals, "blk": blocks}
    save_data(data)
    schedule_publish(interaction.guild)
    await interaction.response.send_message(
        f"M{match}: {player.mention} {points} PTS, {rebounds} REB, {assists} AST, {steals} STL, {blocks} BLK. "
        "Run it again for the same player to correct it.", ephemeral=True, allowed_mentions=NO_PINGS)
    if m.get("winner"):
        await refresh_score_card(interaction.guild, s, s["event"], m)  # add Players of the Game to the card


# ---- fake teams for /testtournament

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


def fake_box(team_id: int, players: list[str], points: int, rng: random.Random) -> dict:
    """Split a team's points across 5 or 6 players and make up the other stats."""
    used = players[:rng.choice([5, 6])]
    weights = [rng.uniform(0.4, 1.0) * (2.2 if i == 0 else 1.4 if i == 1 else 1) for i in range(len(used))]
    rng.shuffle(weights)
    raw = [points * w / sum(weights) for w in weights]
    pts = [int(x) for x in raw]
    for i in sorted(range(len(raw)), key=lambda i: raw[i] - pts[i], reverse=True)[:points - sum(pts)]:
        pts[i] += 1
    return {p: {"team": team_id, "pts": pts[i], "reb": rng.randint(0, 12), "ast": rng.randint(0, 9),
                "stl": rng.randint(0, 4), "blk": rng.randint(0, 3)} for i, p in enumerate(used)}


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


def site_url() -> str | None:
    if not GITHUB_REPO or "/" not in GITHUB_REPO:
        return None
    owner, repo = GITHUB_REPO.split("/", 1)
    if repo.lower() == f"{owner.lower()}.github.io":
        return f"https://{repo}/"
    return f"https://{owner}.github.io/{repo}/"


def event_site_data(ev: dict | None, name, pname=str) -> dict:
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
                         "winner": name(m["winner"]) if m["winner"] else None, "score": m.get("score"), "box": box_rows(m, pname, name)}
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
                                     "score": m.get("score"), "box": box_rows(m, pname, name)}
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
                       "score": m.get("score"), "box": box_rows(m, pname, name), "done": m["done"], "bye": bye,
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
                      "captain": player(t["captain"]),
                      "players": [player(u) for u in t["roster"] if int(u) != t["captain"]],
                      "points": t.get("points", 0), "qualified": major_qualified(s, key),
                      "registered": bool(tz and key in tz.get("entrants", []))})
    data = {"league": LEAGUE_NAME, "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "teams": teams,
            "circuit": {"needed": c["needed"],
                        "standings": sorted(({"team": t["name"], "points": t["points"], "qualified": t["qualified"]}
                                             for t in teams), key=lambda r: -r["points"])},
            "tourney": ({"name": tz["name"], "kind": tz["kind"], "open": s["open"],
                         "points": spec_text(tz["spec"]) if tz.get("spec") else None,
                         "entrants": [name(int(k)) for k in tz["entrants"] if k in s["teams"]]} if tz else None)}
    data.update(event_site_data(s["event"], name, player))
    current = player_totals(s["event"], player, name)
    year = datetime.now().year
    past = [h["players"] for h in s.get("history", []) if h.get("year") == year]
    data["stats"] = {"tournament_name": tz["name"] if tz else "Current tournament",
                     "tournament": list(current.values()),
                     "year_label": str(year), "year": list(merge_totals(*past, current).values())}
    if s["open"] and not s["event"]:
        data["stage"] = "signups"
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
            await github_put(session, "index.html", SITE_TEMPLATE.read_bytes(), "Update site")
            for _k, t in team_list(guild_signups(load_data(), guild.id)):
                f = t.get("logo")
                if f and f not in _uploaded_logos and (LOGO_DIR / f).exists():
                    await github_put(session, f"logos/{f}", (LOGO_DIR / f).read_bytes(), "Add team logo")
                    _uploaded_logos.add(f)
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


@bot.tree.command(description="Update the league website now and show its link.")
@app_commands.default_permissions(manage_roles=True)
async def website(interaction: discord.Interaction):
    if not is_staff(interaction.user):
        return await interaction.response.send_message("Only league staff can update the website.", ephemeral=True)
    await interaction.response.defer(ephemeral=True, thinking=True)
    await interaction.followup.send(await publish_site(interaction.guild), ephemeral=True)


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
