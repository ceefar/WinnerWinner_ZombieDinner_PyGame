# v1.00 - 4/11
[playground-tests-tho]
- minimap for player
    - zombies works but huge map size lags so will find an alternative to initial simple functionality
- minimap toggle with m key    
- [update] improved minimap efficiencies to now show zombies at 60fps on huge map size (tested @ 16 total zombies)
- initial basic implementation of day and night cycle
    - includes time int ui, rising and lowering sun icon and 7am daily
    - small optimisation for minimap class again, back to 60fps

# v1.00 5/11
[still-playground-mvp-finalisation-tests]
- smoothed out day night cycle
- added functionality to manually change speed of the cycle
- added ability to set start time of the cycle
[in-another-side-playground-lol]
- overhaulted menu ui and functionality
- menu and item optimisations and improvements
- updated chargebar and moved it to this new action ui with randomised info text
- added rarity and rarity ui elements
- added lock difficulty
- added locked functionality and ui for it
- added player ability : lockpicking
- ux improvement, previously unlocked boxes open instantly when reopening the same box (for whatever reason idk but it makes sense lol)
- added simple line between current box and menu for visual clarity
- added red/green visual clarity for lootable box highlights to show if they can be opened or not based on current lockpicking level

# v1.01 6/11
[part-playground-part-final]
- images concept and ui formatting improved again
- rarity system at item level overhauled
- proper item types concept
- stacking logic (not implemented)
- realised that need to just start this to final so doing that now starting at lootables

# v1.01 7/11
[starting-final]
- now lootables clean and working, multiple images n ting
- drastically improved lootable locking, rarity, and opening time difficulty logic
- added c to close and other minor ux improvements to final version
- finalised lootable proximity menu with subtext etc
- starting menus with improved ui
- added basic player inventory styling 
- upgrading player inventory from simple list to complex dict array structure, is a laaaarge overhaul 
- delete items from player inventory properly using ids
- undo functionality
- undo ui button
- parent child and super implementation for inventory menu system that is shared between the players inventory and the lootable boxes

# v1.02 8/11
[final-doing-loot-x-lootables-x-inventorymenus]
- sorted lootable menu to base level
- properly working tho basic af new dynamic loot creation system, with dictionary data structure pretty much all hooked up

# v1.03 8/11
[final-doing-loot-x-lootables-x-inventorymenus]
- fixed bug when clicking items in lootable menu where item rects and ids were not correct, caused by unique id duplication issue during testing
- configured undo for lootable menu via super and parent class and works a treat, am very pleased with that
- loot placement and removing and NEW! undo now working all as excepted :D
- very much means we have a dynamic lootable system with rarities and lots of diversity 
- plus custom ui menus for them which are VERY lightweight and have barely impacted the fps at all
- stackable items now implemented, with proper use of sub class too as want to include other stackable types, tho only just done gold for now
- separated logic for gold in ui to improve stacking ui + add incrementing display string for gold "size"
- faux achievements concept, very very basic but will give it some nice polish when finalising everything at the end
- gold now always stays at the top of the players inventory, if the player has gold anyways
- very kewl functionality tho with custom key function to sort the dict that is being blit to menu, very dynamic, much wow

# v1.04 9/11
[absolutely-slapping-the-gui-now-lawd]
- min and max height for menus based on dynamic sizing working nicely
- generally fixed some things to be more dynamic (e.g. undo box size, etc)
- first working implementation of scroll, using only buttons, works well tho <3
- scrolling with locking in x and y based on dynamic true scroll position
- hiding scroll buttons when not relevant (cant scroll up or down as at top or bottom)
- reverted slightly due to scrollbar issues
- tested out a `grappling` concept that i will now be adding later on as it can be implemented quite easily

# v1.05 x v1.051 x v1.052 10/11
[half-day-as-had-drs-apt-n-ting]
- absolutely just had a load of things about classes and oop class structure twig in my head
- started on a concept gui but only partly doing it as is diminising returns
- new mobile gui minimap
- added player
- added loot using the setup/init loop to avoid excess reptition 
- home page toggle initial setup
- home page clickable setup working
- clean home button function x functionality working across all pages 
- fixed some bugs with mouse click state issues across multiple menu types
- basic store front layout mockup

# v1.052 - v1.07 11/11
[clapping]
- feel like ive had huge learning breakthroughs, particularly in oop, over the last two days
- added maps and home icons and polished the mobile menu functionality a tad
- basic test af implementation of changing zone at map edge, tho implemented on button press while testing 
    - when doing this properly obvs need to have the player stats persisting so will need to refactor to pass the player between levels (which is fine)
- improved the minimap display to gta style icons

# v1.07 and v1.071
[still-clapping-main-flow-plus-testing-branches-too]
- tested concept for new full screen minimap, will be implementing shortly
- delivery locker initial test implementation
- refactoring Lootable class structure into Menuable parent child class based structure
    - with first child being the delivery locker (rest will be lootable and workbench)
- delivery locker menu first implementation added, still much clean very wow
- added lockers to the (soon to be updated) minimap, no unique icon yet tho just using the workbench one for now 
- added locker temp image
- hover state and clicked trigger flag for buy now button in mobile store
- drone lawd


sunday title stuff
- updated locker image to have open or closed top depending on loading
- small rework of how images are loading based on states for lockers n drone
- drone now going "inside" the locker
- can now tap and "collect" the item, tho not actually done the inventory or true item yet
- update onclick functionality, need to overhaul this now i understand its limitations better
- onclick buy now drone now working
- sending specific item brought from the mobile store <3
- collecting item to inventory <3
- delivery item box highlighting based on rarity (well menu is but box soon)
- new map lawd, and legit the most minor changes to get it to work from small mobile map to full screen which always makes me proud when stuff like dis happen :D
