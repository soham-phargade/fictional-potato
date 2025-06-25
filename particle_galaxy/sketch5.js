const sketch5 = (p) => {
  let symmetry = 6;
  let angle = 360 / symmetry;

  p.setup = () => {
    p.describe(
      `Dark grey canvas that reflects the lines drawn within it in ${symmetry} sections.`
    );
    p.createCanvas(720, 400);
    p.angleMode(p.DEGREES);
    p.background(50);
  };

  p.draw = () => {
    p.translate(p.width / 2, p.height / 2);

    if (
      p.mouseX > 0 &&
      p.mouseX < p.width &&
      p.mouseY > 0 &&
      p.mouseY < p.height
    ) {
      let lineStartX = p.mouseX - p.width / 2;
      let lineStartY = p.mouseY - p.height / 2;
      let lineEndX = p.pmouseX - p.width / 2;
      let lineEndY = p.pmouseY - p.height / 2;

      if (p.mouseIsPressed) {
        for (let i = 0; i < symmetry; i++) {
          p.rotate(angle);
          p.stroke(255);
          p.strokeWeight(3);
          p.line(lineStartX, lineStartY, lineEndX, lineEndY);

          p.push();
          p.scale(1, -1);
          p.line(lineStartX, lineStartY, lineEndX, lineEndY);
          p.pop();
        }
      }
    }
  };
};

new p5(sketch5, 'sketch5');
