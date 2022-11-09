

[rn-rn]
- scrolling and max height oooo, lawd i wanna do this so badly ngl 100% we are doing it lol

[then]
- time implementation and fog
- time ui and minimap hud
    - doing this properly so you can hide and it replays the loading screen ting 100, even have it dark at the start?
- else remaining for the actual on-screen ui
    - weapon, ammo, gold, zombies remaining, else?
- the player on screen ui bars stuff
- get weapons and ammo working
- reeeeally want a ui objective map triangle thing, you should be able to do this without too much difficulty tbf
    - because if you can get this you can get companion events
    - and then imo if you have all that stuff added in too (really just companion and companion / survivor events) its a complete game 100

[actually-do-need-to-do]
- refactoring menu to parent class
    - use this as the perf time to really get into super class and advanced methods and concepts here
    - plus also for the decorator idea too
    - use this as a page and code to highlight in a seperate explainer ting! <3 luv it

[consider]
- on get hit screen shake

[then]
- by now you must have a repo for this as i believe its good enough to showcase
- so clean tf up and screenshots n post up shit sickly


[extras]
- do the zombie out of range thing...
- zombie noise hearing range and just doing zombie pathfinding stuff now (its easy dw and exciting oooooo - as then we *really* got a game)
    - for a super basic and quick intital implementation
    - based on the noise rating or whatever there is a small chance to trigger and it checks it x times every frame or whatever (like my blocking print with modulo)
    - if it triggers a mob is randomly spawned with sight range of the player and just outside of range!
        - omg i love this so much

- do dee new menu as a child class and set it up in tiled as a workbench
    - then you can have items that are clothes and can have upgrades and skill points dere, its easy af its just the player inventory but subclass++
    - basically means do items here... can also start adding in below too
        - and generally should keep things clean as you go

[bugs]
- small bug to fix after a g>g (gold > gold) stack in menu, adding a non stackable item will invalidate the next undo (which it shouldn't)
    - tho it will continue working fine afterwards



# [ SKIP THIS 100%! ] - yanno what 100% skip this
# the logic x pseudocode is...
# save everythings y position to some kind of self var anchor, that will be attached to the scroll bar
# when you move the scroll bar, it will move the text by an amount vs how much the bar moved by, to make this easier buttons may be best first off
# as long as you are blitting to the surface it will just auto mask
# the only real consideration would be an actual scroll bar
#   - need to know length of all combined text, then size of bar for offset then just a fair amount bar size vs scroll bar size (which is basically the scroll bar container) and just sort it all as a percent, is simple enough on paper but is first time so bet its a ballache lol
# imo just get the text working with buttons first
# then come back to that in future