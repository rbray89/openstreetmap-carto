#world-water::area {
  [zoom >= 0][zoom < 10] {
    polygon-fill: @water-color;
  }
}

#world-coast-poly::area [zoom >= 10] {
  polygon-fill: @water-color;
}

#icesheet-poly {
  [zoom >= 8] {
    polygon-fill: @glacier;
  }
}

#icesheet-outlines {
  [zoom >= 8] {
    [ice_edge = 'ice_ocean'],
    [ice_edge = 'ice_land'] {
      line-width: 0.375;
      line-color: @glacier-line;
      [zoom >= 8] {
        line-width: 0.5;
      }
      [zoom >= 10] {
        line-dasharray: 4,2;
        line-width: 0.75;
      }
    }
  }
}


#world-hd-hydropolys::area[zoom>=7][zoom<=11]["Type"!="Ocean"] {
  line-color: @water-color;
  line-width: .75;
  polygon-fill: @water-color;
  [zoom=7]{
    line-color: mix(@land-color, @water-color,60%);
    polygon-fill: mix(@land-color, @water-color,60%);}
  [zoom=8]{
    line-color: mix(@land-color, @water-color,30%);
    polygon-fill: mix(@land-color, @water-color,30%);}
  [zoom=9]{
    line-color: mix(@land-color, @water-color,15%);
    polygon-fill: mix(@land-color, @water-color,15%);}
  [zoom=10]{
    line-color: mix(@land-color, @water-color,10%);
    polygon-fill: mix(@land-color, @water-color,10%);}
}

#world-nelakes::area [zoom<=11]{
  [zoom>=0][ScaleRank=0],
  [zoom>=1][ScaleRank<=1],
  [zoom>=2][ScaleRank<=2],
  [zoom>=3][ScaleRank<=3],
  [zoom>=4][ScaleRank<=4],
  [zoom>=5][ScaleRank<=5],
  [zoom>=6][ScaleRank<=6],{
    line-width: 0;
    polygon-fill: @water-color;
  }
}

#world-nerivers::line [zoom>=4] [zoom<7]{
  [zoom>=0][ScaleRank=0],
  [zoom>=1][ScaleRank<=1],
  [zoom>=2][ScaleRank<=2],
  [zoom>=3][ScaleRank<=3],
  [zoom>=4][ScaleRank<=4],
  [zoom>=5][ScaleRank<=5],
  [zoom>=6][ScaleRank<=6]{
    line-width: .5;
    [zoom>=6]{line-width: 1;}
    [zoom=4]{line-color: mix(@land-color, @water-color,50%);}
    [zoom=5]{line-color: mix(@land-color, @water-color,40%);}
    [zoom=6]{line-color: mix(@land-color, @water-color,30%);}
  }
}

#world-nepopulated::label {
  [zoom >= 5][zoom <= 11] {
    [SCALERANK = 0],
    [SCALERANK = 1],
    [zoom>=4][SCALERANK<=2],
    [zoom>=5][SCALERANK<=3],
    [zoom>=6][SCALERANK<=3],
    [zoom>=7][SCALERANK<=5],
    [zoom>=8][SCALERANK=6],
    [zoom>=9][SCALERANK=7],
    [zoom>=10][SCALERANK=8],
    [zoom>=11][SCALERANK=9],
  	[zoom>=11][SCALERANK=10]{
      text-allow-overlap: false;
      text-placement: point;
      text-placement-type: simple;
      text-placements: "W,E";
      text-name: "[NAME]";
      text-size: 8;
      text-fill: grey;
      text-face-name: @book-fonts;
      text-halo-radius: 1.5;
      text-wrap-width: 75;
      [zoom<=7]{
        text-size:10;
        text-character-spacing:2;
        dot-fill: grey;
        dot-width: 4;
        dot-height: 4;
        text-dx: -6;
      }
      [zoom>=7]{
        text-size:12;
        text-character-spacing:2;
      }
    }
  }
}

#world-neprovinces::line[zoom>=4][zoom<=11]{
  [zoom>=4][SCALERANK<=3],
  [zoom>=5][SCALERANK<=4],
  [zoom>=6][SCALERANK<=5],
  [zoom>=8][SCALERANK<=6],
  [zoom>=8][SCALERANK>=7]{
    line-color: grey;
    line-dasharray:2,2;
    line-cap:butt;
    line-width: .5;
   }
}

#world-neprovinces-p::label[adm0_sr=1][zoom>=6][zoom<=11]{
  [zoom>=6][zoom<8][scalerank<=2],
  [zoom>=7][zoom<9][scalerank>2][scalerank<=4],
  [zoom>=8][zoom<10][scalerank>4][scalerank<=6],
  [zoom>=9][scalerank>6][scalerank<=8],
  [zoom>=10][scalerank>=9]{
    text-allow-overlap: false;
    text-face-name:@book-fonts;
    text-fill:grey;
    text-halo-radius:1.5;
    text-transform:uppercase;
    text-name:"[name]";
    text-size:12;
    text-character-spacing:2;
    text-wrap-width: 75;
    [zoom>=8]{
      text-size:13;
      text-character-spacing:2;
    }
  }
}


#world-necountries::line {
  [zoom >= 2][zoom <= 11] {
    line-width: 0.5;
    [zoom = 2]{line-width: 0.25;}
    [zoom = 3]{line-width: 0.3;}
    line-color: grey;
  }
}

#world-necountries-p::label [zoom>2][zoom<=7]{
  [zoom<=6][zoom>=2][ScaleRank<=1],
  [zoom>=4][ScaleRank=2],
  [zoom>=5][ScaleRank=3],
  [zoom>=8][ScaleRank=4],
  [zoom>=9][ScaleRank=4],
  [zoom>=11][ScaleRank>=5]{
    text-wrap-before: true;
    text-wrap-width: 75;
    text-face-name:@book-fonts;
    text-fill:grey;
    text-halo-radius:2;
    text-transform:uppercase;
    text-name:"[ADMIN]";
      text-size:13;
      text-character-spacing:2;
    }
}

#world-builtup::area [zoom >= 6][zoom <= 11]{
  polygon-comp-op: multiply;
  [zoom=6]{polygon-fill: lighten(black,99%);}
  [zoom=7]{polygon-fill: lighten(black,98%);}
  [zoom=8]{polygon-fill: lighten(black,97%);}
  [zoom=9]{polygon-fill: lighten(black,96%);}
  [zoom=10]{polygon-fill: lighten(black,95%);}
  [zoom=11]{polygon-fill: lighten(black,94%);}
}

#world-neroads-na::line [zoom>=9][zoom<12]{
  [zoom>=6][ScaleRank<=7],
  [zoom>=7][ScaleRank<=8],
  [zoom>=8][ScaleRank<=9],
  [zoom>=9][ScaleRank<=11],
  [zoom>=10][ScaleRank<=11],
  [zoom>=11][ScaleRank<=12],
  [zoom>=11][ScaleRank>=13], {
    line-color:@motorway-fill;
    line-cap:round;
    line-join:round;
  [zoom=9]{line-width: .25;}
  [zoom=10]{line-width: .5;}
  [zoom=11]{line-width: .75;}
    line-width:1;
  }
}

#world-roads::line [zoom>=6][zoom<=11]{
  [zoom>=6][RANK<=1],
  [zoom>=7][RANK<=1],
  [zoom>=8][RANK<=2],
  [zoom>=9][RANK<=2],
  [zoom>=10][RANK<=3],
  [zoom>=11][RANK<=4],
  [zoom>=11][RANK>=5], {
    line-color:@motorway-fill;
    line-cap:round;
    line-join:round;
    line-width:.1;
    [zoom=7]{line-width: .15;}
    [zoom=8]{line-width: .25;}
    [zoom=9]{line-width: .5;}
    [zoom=10]{line-width: .75;}
    [zoom=11]{line-width: 1;}
  }
}
