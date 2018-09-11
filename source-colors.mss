
@light:   white;
@neutral: grey;
@dark:    #444;


@dmin-text: grey;
@address-color:             desaturate(#666,100%);
@admin-boundaries:          desaturate(#ac46ac,100%);
@marina-text:               desaturate(#576ddf,100%); // also swimming_pool
@shop-icon:                 desaturate(#ac39ac,100%);
@shop-text:                 desaturate(#939,100%);
@transportation-icon:       desaturate(#0092da,100%);
@transportation-text:       desaturate(#0066ff,100%);
@airtransport:              desaturate(#8461C4,100%); //also ferry_terminal
@health-color:              desaturate(#da0092,100%);
@amenity-brown:             desaturate(#734a08,100%);
@office:                    desaturate(#4863A0,100%);
@man-made-icon:             desaturate(#555,100%);
@landform-color:            desaturate(#d08f55,100%);
@wetland-text:              darken(desaturate(#4aa5fa,100%), 25%); /* Also for marsh and mud */
@building-fill:             desaturate(#d9d0c9,100%); //Lch(84, 5, 70)
@ferry-route:               desaturate(#66f,100%);

// --- Parks, woods, other green things ---

@grass:                     desaturate(#cdebb0,100%); // also grassland, meadow, common, village_green, garden
@scrub:                     desaturate(#b5e3b5,100%);
@forest:                    desaturate(#add19e,100%);       // Lch(80,30,135)
@forest-text:               desaturate(#46673b,100%);  // Lch(40,30,135)
@park:                      desaturate(#c8facc,100%);         // Lch(94,30,145)
@orchard:                   desaturate(#aedfa3,100%); // also vineyard, plant_nursery

// --- "Base" landuses ---

@built-up-lowzoom:          desaturate(#aaaaaa,100%);
@built-up-z11:              desaturate(#c0c0c0,100%);
@built-up-z12:              desaturate(#d0d0d0,100%);
@residential:               desaturate(#e0dfdf,100%);      // Lch(89,0,0)
@residential-line:          desaturate(#b9b9b9,100%); // Lch(75,0,0)
@retail:                    desaturate(#ffd6d1,100%);           // Lch(89,16,30)
@retail-line:               desaturate(#d99c95,100%);      // Lch(70,25,30)
@commercial:                desaturate(#f2dad9,100%);       // Lch(89,8.5,25)
@commercial-line:           desaturate(#d1b2b0,100%);  // Lch(75,12,25)
@industrial:                desaturate(#ebdbe8,100%);       // Lch(89,9,330) (Also used for railway)
@industrial-line:           desaturate(#c6b3c3,100%);  // Lch(75,11,330) (Also used for railway-line)
@farmland:                  desaturate(#fbecd7,100%);         // Lch(94,12,80)
@farmland-line:             desaturate(#d6c4ab,100%);    // Lch(80,15,80)
@farmyard:                  desaturate(#f5dcba,100%);         // Lch(89,20,80)
@farmyard-line:             desaturate(#d1b48c,100%);    // Lch(75,25,80)

// --- Transport ----

@transportation-area:       desaturate(#e9e7e2,100%);
@apron:                     desaturate(#e9d1ff,100%);
@garages:                   desaturate(#dfddce,100%);
@parking:                   desaturate(#eeeeee,100%);
@rest_area:                 desaturate(#efc8c8,100%); // also services

// --- Other ----

@allotments:                desaturate(#eecfb3,100%);       // Lch(85,19,70)
@bare_ground:               desaturate(#eee5dc,100%);
@campsite:                  desaturate(#def6c0,100%); // also caravan_site, picnic_site
@cemetery:                  desaturate(#aacbaf,100%); // also grave_yard
@construction:              desaturate(#c7c7b4,100%); // also brownfield
@heath:                     desaturate(#d6d99f,100%);
@mud:                       desaturate(rgba(203,177,154,0.3),100%); // produces #e6dcd1 over @land
@place_of_worship:          desaturate(#cdccc9,100%);
@place_of_worship_outline:  desaturate(#111,100%);
@sand:                      desaturate(#f5e9c6,100%);
@societal_amenities:        desaturate(#f0f0d8,100%);
@tourism:                   desaturate(#734a08,100%);
@quarry:                    desaturate(#c5c3c3,100%);
@military:                  desaturate(#f55,100%);
@beach:                     desaturate(#fff1ba,100%);

// --- Sports ---

@pitch:                     desaturate(#aae0cb,100%); // also track
@golf_course:               desaturate(#b5e3b5,100%);

@placenames:                desaturate(#222,100%);
@placenames-light:          desaturate(#777777,100%);

@power-line-color:          desaturate(#888,100%);

@tertiary-fill:             desaturate(#ffffff,100%);
@residential-fill:          desaturate(#ffffff,100%);
@living-street-fill:        desaturate(#ededed,100%);
@pedestrian-fill:           desaturate(#dddde8,100%);
@raceway-fill:              desaturate(pink,100%);
@road-fill:                 desaturate(#ddd,100%);
@footway-fill:              desaturate(salmon,100%);
@footway-fill-noaccess:     desaturate(#bbbbbb,100%);
@steps-fill-noaccess:       desaturate(#bbbbbb,100%);
@cycleway-fill:             desaturate(blue,100%);
@cycleway-fill-noaccess:    desaturate(#9999ff,100%);
@bridleway-fill:            desaturate(green,100%);
@bridleway-fill-noaccess:   desaturate(#aaddaa,100%);
@track-fill:                desaturate(#996600,100%);
@track-fill-noaccess:       desaturate(#e2c5bb,100%);
@aeroway-fill:              desaturate(#bbc,100%);


@access-marking:            desaturate(#eaeaea,100%);
@access-marking-living-street: desaturate(#cccccc,100%);

@tertiary-casing:           desaturate(#8f8f8f,100%);
@residential-casing:        desaturate(#bbb,100%);
@pedestrian-casing:         desaturate(#999,100%);
@tertiary-shield:           desaturate(#3b3b3b,100%);

@residential-construction:  desaturate(#aaa,100%);
@service-construction:      desaturate(#aaa,100%);

@destination-marking:       desaturate(#c2e0ff,100%);
@private-marking:           desaturate(#efa9a9,100%);
@private-marking-for-red:   desaturate(#C26363,100%);

@tunnel-casing:             desaturate(grey,100%);

@junction-text-color:       desaturate(#960000,100%);
@halo-color-for-minor-road: desaturate(white,100%);
@lowzoom-halo-color:        desaturate(white,100%);

@station-color:             desaturate(#7981b0,100%);

@water-color:               desaturate(#aad3df,100%);
@land-color:                desaturate(#f2efe9,100%);

@standard-halo-fill:        desaturate(rgba(255,255,255,0.6),100%);

@breakwater-color:          desaturate(#aaa,100%); /* Also for groyne */
@dam:                       desaturate(#adadad,100%);
@dam-line:                  desaturate(#444444,100%);
@weir-line:                 desaturate(#aaa,100%);
@lock-gate:                 desaturate(#aaa,100%);
@lock-gate-line:            desaturate(#aaa,100%);

@water-text:                desaturate(#4d80b3,100%);
@glacier:                   desaturate(#ddecec,100%);
@glacier-line:              desaturate(#9cf,100%);

@marina-a-casing:           desaturate(blue,100%);
@marina-b-casing:           desaturate(blue,100%);

@tunnelfill-casing:         desaturate(#f3f7f7,100%);

@water-lines-casing:        @light;
@bridge-low-casing:         @light;
@bridge-casing:             @dark;
@bridge-fill:               @light;

@nature-reserve-casing:     desaturate(green,100%);

@arialways:                 desaturate(#808080,100%);
@quarry-casing:             grey;
@prision-casing:            desaturate(#888,100%);
@barriers-casing:           desaturate(#444,100%);
@barriers-hedge-casing:     desaturate(#aed1a0,100%);
