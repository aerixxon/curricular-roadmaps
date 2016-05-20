# curricular-roadmaps

entirely client side

index.html holds all of the code for the site including D3 visualization (mapping for D3 is hardcoded in the JS)

uap.py - original data processing and exploration, also cleans raw data and saves it to a new JSON file which I then use everywhere else

uapd3precompute.py - populates the D3 data structure for all of the mappings e.g. {"nodes":[{"node":0, "name":"6.004"}, etc..], "links":[{"source":0, "target":1, "value": 34}]}

