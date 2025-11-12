function setup() {
  createCanvas(400, 400);
  
  allCircles = []
  
  
  class myCircle {
    constructor(x, y, r) {
      this.x = x;
      this.y = y;
      this.r = r;
    }

    within() {
      if ((mouseX - this.x) ** 2 + (this.y - mouseY) ** 2 <= this.r ** 2) {
        return true;
      }
    }

    show() {
      circle(this.x, this.y, 2 * this.r);
    }
    
    createCopy() {
      let newCirk = new myCircle(this.x + 42, this.y, this.r)
      append(allCircles, newCirk)
    }
  }
  
   let cirk = new myCircle(50,50,25)
  append(allCircles, cirk)
  
}

function draw() {
  background(220);
  
  //allCircles[0].show()
  for(let i = 0; i<allCircles.length; i++) {
    allCircles[i].show()
  }

}

function mouseClicked() {
  for(let i = 0; i<allCircles.length; i++) {
    if(allCircles[i].within) {
      allCircles[i].createCopy()
      console.log(allCircles[i])
    }
  }
}








