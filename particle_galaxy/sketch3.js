const sketch3 = (p) => {
  let strokeHue = 20;

  p.setup = () => {
    p.createCanvas(720, 400);
    p.noFill();
    p.strokeWeight(2);
    p.colorMode(p.HSB);
  };

  p.draw = () => {
    p.describe(
      'Ten rainbow-colored lines in a bezier curve formation. The top anchors of the curves move with the cursor as it hovers over the black canvas.'
    );

    p.background(5);

    for (let i = 0; i < 200; i += 20) {
      let strokeColor = i + 10;
      p.stroke(strokeColor, 50, 60);

      p.bezier(
        p.mouseX - i / 2, 0 + i,
        410, 20,
        440, 300,
        240 - i / 16, 300 + i / 8
      );
    }
  };
};

new p5(sketch3, 'sketch3');
