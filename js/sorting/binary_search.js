function find(Array, number) {
    let bottom = 0
    let top = Array.length
    let Searching = true

    while(Searching) {
        let mid = ~~(( top - bottom ) / 2) + bottom
        if(Array[mid] == number) {
            Searching = false
            console.log("found number at " + mid)
            return mid
        } else if(Array[mid] < number) {
            console.log(Array[mid] + " is smaller " + number)
            console.log("bottom now: " + bottom)
            console.log("mid now: " + mid)
            console.log("top now: " + top)
            bottom = mid
            console.log("bottom new: " + bottom)
        } else {
            console.log(Array[mid] + " is bigger " + number)
            console.log("top now: " + top )
            top = mid
            console.log("top new: " + top )
        }
    }
}


Array = [1]
new_number = Math.Floor(Math.random() * 10))
append(Array, )
console.log(find(Array, 234))
