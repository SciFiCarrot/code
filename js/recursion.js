function fak(t) {
    if(t == 1 || t == 2) {
        return 1
    }
    return fak(t-1) + fak(t-2)
}

console.log(fak(3))
console.log(fak(2))
console.log(fak(1))
console.log(fak(0))
