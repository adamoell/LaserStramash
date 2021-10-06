# Game Types

This section describes the game types available in the prototype.

Due to a limitation of the prototype hardware, IR hit recognition does
not work well while the network interface is active. The following
prototype games have been designed to work with the constraint that the
network connection will be *switched off* at game start, and switched on
again only when the game time is completed.

## Free-For-All

ID: ffa

Each player is their own 'team'. Players accumulate hits and kills until
the end of the game, when the guns all send their data to the server.

Game setup:

-   Time limit
-   SFX Server
-   Ammo clip size (max ammo) default=10
-   Reload Time default=5
-   Players

Game rules:
-   At game start, player has ammo=MAX
-   Usual state: gun is active, RGB solid light blue
-   On fire:
    -   If ammo:
        -   strobe RGB yellow
        -   decrease ammo
    -   else:
        -   strobe RGB pink
-   On reload:
    -   Player is inactive (can't fire) for n seconds
    -   RGB from black to full brightness solid light blue, then flash
        quickly to indicate complete
    -   Player reactivated, ammo set to MAX

-   When a player is killed:
    -   he is 'down' -- gun inactive for 10 sec
    -   RGB from black to white over 10 sec, then quick flash to
        indicate completed
    -   Player is reactivated and then shielded - 'bulletproof' - for 5
        sec (this is to stop someone 'standing over' a dead guy and
        rekilling)
    -   RGB solid red for this time, then back to light blue

At the end of the game, the guns all upload their hits and numbers of
shots fired. Score is computed as (kills -- deaths) + (kills /
shotsfired) -- that is, an integer 'net kills' with accuracy providing a
decimal 'tiebreaker'.

## Teams

ID: teams

Play is as per free-for-all above, except players are organised into
teams. 'Friendly fire' is ignored (ie doesn't count as a hit). Instead
of showing light blue in the default state, the RGB shows the team
colour.

Game setup:

-   Time limit
-   SFX Server
-   Ammo clip size (max ammo) default=10
-   Reload Time default=5
-   Teams
-   Players

## Stramash Royale

ID: royale

Play is as per free-for-all above, except that when a player is hit,
they are out -- gun disabled, RGB off, go sit on the bench until the
end. Last man standing is the winner; or if the time limit is reached,
the surviving players are ranked by score. Score is computed as (kills
-- deaths) + (kills / shotsfired) -- that is, an integer 'net kills'
with accuracy providing a decimal 'tiebreaker'.

Game setup:

-   Time limit
-   SFX Server
-   Ammo clip size (max ammo) default=10
-   Reload Time default=5
-   Players

Issue: the last man's gun won't know that he's the last man. May need to
manually trigger victory condition -- using a 'master blaster' game-over
transmitter?
