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

# from other folder but
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
- finishing up opening logic, c to close, etc