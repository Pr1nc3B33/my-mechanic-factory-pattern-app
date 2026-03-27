function topThreeWords(text) {
    const wordy = text.toLowerCase().match(/[a-z]+(?:'[a-z]*)*/g) //regex to match words
    const occurMap = {};

    for (let wordys of wordy) // loops through every word in wordy array then stored temp in wordys
        occurMap[wordys] = (occurMap[wordys] || 0)+1; // adds 1 to count when word is seen 
                                                     // "|| 0" used to say "if undefined, use 0"

    return Object.keys(occurMap) // this takes occurMap objects and retruns an arrays of just its keys(words found)
        .sort((a, b) => occurMap[b] - occurMap[a])
        .slice(0, 3);
}


function productFib(prod) {
    let a = 0, b = 1;   // start with Fibonacci numbers 

    while (a * b < prod) {  // each loop shifts a pair forward stop soon as a*b no longer less than prod
        [a, b] = [b, a+b];
    }
    return [a, b, a*b === prod];
}


