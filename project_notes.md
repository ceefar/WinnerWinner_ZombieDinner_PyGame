** Personal Notes - stored in .md files as it breaks down well visually in vscode by default... yes i realise this probably looks insane in markdown on github **


[saturday-flow]
- lockers with the requirement to go thru phone and use a code to unlock
- refactor Workbench to make it a child of Menuable

[today]
- first
- locker and drones and ordering
    - you 100% should be able to follow the drone on the map omg <3
    - its guna be near the camera so add a faux depth by using transform.scale on the drone image
- and then
- zones and minimap new concept
- and then
- get the drone on that too moving and showing up as a waypoint on where it will be going to
- then <3

[quick-notes]
 - have amazon prime drones deliver ur product to random drop zone lockers (it glitches out)
    - actually really like this, adds a lot of polish and completeness too, and can do a lot with the drone via transform.scale 
    - things u buy can be things that u can also craft duh, i mean just generally makes it easier 
 - make workbench simple, just upgrades, use parts like steel, other things can be broken down to parts like steel maybe

[so-for-amazon-prime-lockers-and-drones-lol]
- last major addition but tbf had been considering it for a while, now have cut some other stuff guna add it
- would be good to have the zone too obvs but probs wont have implemented that by then
- ok also maybe companion too but thats already done so imo its free, just needs a refactor

[start-this-asap]
- start semi documenting things in sections in a private repo for the readme, just keep running notes like the changelog

[oh-snap]
- right align the wallet in store!
    - just figure out how to actually use align for this bosh
- skooch the minimap display down as its now clipping at the top where its capped but its too high - go to the workbench and see... or move the building down lmao

[so-for-workbench]
- new unique workbench ui with clothing slots and player stats x abilities x whatever else 
- obvs also only the valid items showing idea
- the smaller tighter ui for it but still finding space for the other stuff or add/try menu page toggle
- some super basic crafting

[rn-rn-rn]
- do a bit on workbench since youve started now and it is kinda fun
- then day and night
- then finish up workbench
- then try a proper zone?!
    - oooOooOOoOOoOoo
- then that menu fix

[current-updated-todo]
- day and night working
    - added to phone too with simple alarm screen tho not rnrn lol, do timezones, the lot, fuck it lmao 
- moving menu issue
- omg 100% asap test
    - different zones with different maps loading, if this is even possible which obvs it is but i mean can i do it myself easily enough
    - add this to phone minimap
        - the name of ur zone and the next zone name on the edge of the map vertically (rotated not literally vertically)
        - would then plan to just do the area in faux style
            - tho a refactor too get it to do properly with scrolling, masked map would be amazing ngl, but soooo long and unnecessary lmao
    - if the arrows work use them for this too, pointing to the mid point or any specific entry point, e.g. a building doors oooo 
- workbench 
- on screen objective x workbench arrow/s concept
- mobile icons need text and obvs the rest of the icons lol
- mobile transitions like on and off, booting, battery, etc

[to-finish-store]
- 100% guna want click and throw/flick to scroll the store items, this is easier than it shoulds but does need improved tracking of mouse click states
- add offer to store

[rn-rn]
just guna finish minimap by...
- store
- zombies to minimap 
    - the lightweight way
- then dynamic time
    - then make battery empty slowly and add it to the time functionality
- then add day night
- add remaining top icons & else light polish
- then remaining ui then imo its just the polish
- maybe companion too
    - gives a nice added polish with the conversations ngl
        - and could randomise these at the start bosh

[part-done-x-done]
- toggle between map and home 
    - maps transition [skipped]
- amazon, just started
- dumb af for minimap use images or letters with outline like gta

[oof-try-later-tho-not-rn]
- hate to say it but id love to test this quickly in v1.061 again
    - draw the arrow on the workbench
    - set the pos to update all time to max screen height screen width -/+ image size (so its on screen at the edges)
        - i swear that should just work tho


# random side project
# some bot that updates my profile readme.md based on my most recent commits would be giga kewl
# could use some kinda pillow for images too ngl


[to-finish-scroll-arrows-for-now]
- do little images / arrows on them
- increase to 15 or more?
- hover colour effect?
    - also the old grey when at zero ting?
- add a alpha'd bg bar for them undernearth
- then continue

[for-blokia]
- you know im considering saying do a dynamic super basic google coloured map generator for the phone and just blit it to the shape of the screen area (image mask)
- for an insanely kewl effect
- imo this adds a massive amount of polish
- is super dynamic so kewl to showcase
- and could even be made full screen on button press too
- yeah aite lets just try this
- implement phone first
- then do this in a new playground
- legit even if just day night, boxes, etc (i.e. remaining ui stuff only) + this blokia stuff i would be happy to leave it, do another project, and then come back 

[then]
- the remaining ui, blokia, wepaon, daynight etc

[also-maybe-now-or-not]
- ngl massively do need to do this and is guna be really kewl and could actually do some fun stuff and learn a lot depending on how its done but it also could be kinda long...
- need to do if player is standing on top of the menu it positions the player inventory in the empty right hand place instead
    - the player should then be able to "catch" it by moving back in range again - oooooo

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

[do-reeeeally-wanna-add-this]
- wanna test an trigger for zombie in range enters a grappling animation with the player until X button presses
- can zoom in for this too and have a ui with screen shake omg <3
- because that will look sick af for video preview, which is in all seriousness the only way you can truly show the functionality
- and you can do it sickly in aftereffects 2 min vid bosh

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