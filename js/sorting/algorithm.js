from p5 import *


function setup() {
  reversedArray = revArr(10000)
  ms1 = millis()
  sorted = bubbleSort(reversedArray)
  ms2 = millis()
  console.log(sorted)
  
  console.log(ms2-ms1)
}

function draw() {
  
}

function revArr(length) {
  array = [];
  for (let i = 0; i < length; i++) {
    num =  length  - i
    array.push(num);
  }
  return array;
}

//console.log(revArr(100));
function swapValue(x, y) {
  let temp
  temp = x
  y = temp
  x = y
  return x
  
}

function bubbleSort(array) {
  tries = 1;
  while (tries > 0) {
    tries = 0
    for (let i = 0; i < array.length - 1; i++) {
      if(array[i] > array[i + 1]) {
        x = array[i];
        y = array[i + 1];
        array[i] = y;
        array[i + 1] = x;
        tries += 1;
      }
    }
    if(tries  == 0){
      return array;
    }
  }
}





