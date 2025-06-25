const sketch4 = (p) => {
  let angle;

  p.setup = () => {
    p.createCanvas(710, 400);
    p.colorMode(p.HSB);
    p.angleMode(p.DEGREES);
  };

  p.draw = () => {
    p.background(0);

    angle = (p.mouseX / p.width) * 90;
    angle = p.min(angle, 90);

    p.translate(p.width / 2, p.height);
    p.stroke(0, 255, 255);
    p.line(0, 0, 0, -120);
    p.translate(0, -120);

    branch(120, 0);
    p.describe('A tree drawn by recursively drawing branches, with angle determined by the user mouse position.');
  };

  function branch(h, level) {
    p.stroke(level * 25, 255, 255);
    h *= 0.66;

    if (h > 2) {
      p.push();
      p.rotate(angle);
      p.line(0, 0, 0, -h);
      p.translate(0, -h);
      branch(h, level + 1);
      p.pop();

      p.push();
      p.rotate(-angle);
      p.line(0, 0, 0, -h);
      p.translate(0, -h);
      branch(h, level + 1);
      p.pop();
    }
  }
};

new p5(sketch4, 'sketch4');
