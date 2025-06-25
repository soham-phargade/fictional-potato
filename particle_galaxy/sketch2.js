const sketch1 = (p) => {
  p.setup = () => {
    
    p.createCanvas(400, 400);
    p.background(0)
};

  p.draw = () => {
    
    if (p.mouseIsPressed) {
      p.fill(255);
    } else {
      p.fill(100);
    }
    p.circle(p.mouseX, p.mouseY, 100);
  };
};

new p5(sketch1, 'sketch1');