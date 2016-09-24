@admin-boundaries: desaturate(#ac46ac, 100%);

#nature-reserve-text[zoom >= 13][way_pixels > 192000] {
  text-name: "[name]";
  text-face-name: @book-fonts;
  text-fill: desaturate(green, 100%);
  text-halo-radius: @standard-halo-radius;
  text-halo-fill: @standard-halo-fill;
  text-placement: line;
  text-clip: true;
  text-vertical-alignment: middle;
  text-dy: -10;
}

#nature-reserve-boundaries {
  [way_pixels > 100][zoom >= 7] {
    [zoom < 10] {
      ::fill {
        opacity: 0.05;
        polygon-fill: desaturate(green, 100%);
      }
    }
    a/line-width: 1;
    a/line-offset: -0.5;
    a/line-color: desaturate(green, 100%);
    a/line-opacity: 0.15;
    a/line-join: round;
    a/line-cap: round;
    b/line-width: 2;
    b/line-offset: -1;
    b/line-color: desaturate(green, 100%);
    b/line-opacity: 0.15;
    b/line-join: round;
    b/line-cap: round;
    [zoom >= 10] {
      a/line-width: 2;
      a/line-offset: -1;
      b/line-width: 4;
      b/line-offset: -2;
    }
    [zoom >= 14] {
      b/line-width: 6;
      b/line-offset: -3;
    }
  }
}
