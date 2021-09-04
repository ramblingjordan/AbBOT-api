// a function to simulate adding typos to a string

export const fatFinger = (input: string): string => {
    const lengthOfString = input.length
    const randomIndex = Math.floor(Math.random() * lengthOfString)
    var letters = []
    const randomCharacter = input.charAt(randomIndex)
    switch (randomCharacter) {
        case 'a':
            letters = [`q`, `w`, `s`, `z`]
            break
        case 'b':
            letters = [`v`, `g`, `h`, `n`, ` `]
            break
        case 'c':
            letters = [`x`, `d`, `f`, `v`, ` `]
            break
        case 'd':
            letters = [`s`, `e`, `r`, `f`, `c`, `x`]
            break
        case 'e':
            letters = [`w`, `3`, `4`, `r`, `d`, `s`]
            break
        case 'f':
            letters = [`d`, `r`, `t`, `g`, `v`, `c`]
            break
        case 'g':
            letters = [`f`, `t`, `y`, `h`, `b`, `v`]
            break
        case 'h':
            letters = [`g`, `y`, `u`, `j`, `n`, `b`]
            break
        case 'i':
            letters = [`u`, `8`, `9`, `o`, `k`, `j`]
            break
        case 'j':
            letters = [`h`, `u`, `i`, `k`, `m`, `n`]
            break
        case 'k':
            letters = [`j`, `i`, `o`, `l`, `,`, `m`]
            break
        case 'l':
            letters = [`k`, `o`, `p`, `;`, `.`, `,`]
            break
        case 'm':
            letters = [`n`, `j`, `k`, `,`, ` `]
            break
        case 'n':
            letters = [`b`, `h`, `j`, `m`, ` `]
            break
        case 'o':
            letters = [`i`, `9`, `0`, `p`, `l`, `k`]
            break
        case 'p':
            letters = [`o`, `0`, `-`, `[`, `;`, `l`]
            break
        case 'q':
            letters = [`1`, `2`, `w`, `a`]
            break
        case 'r':
            letters = [`e`, `4`, `5`, `t`, `f`, `d`]
            break
        case 's':
            letters = [`a`, `w`, `e`, `d`, `x`, `z`]
            break
        case 't':
            letters = [`r`, `5`, `6`, `y`, `g`, `f`]
            break
        case 'u':
            letters = [`y`, `7`, `8`, `i`, `j`, `h`]
            break
        case 'v':
            letters = [`c`, `f`, `g`, `b`, ` `]
            break
        case 'w':
            letters = [`q`, `2`, `3`, `e`, `s`, `a`]
            break
        case 'x':
            letters = [`z`, `s`, `d`, `c`, ` `]
            break
        case 'y':
            letters = [`t`, `6`, `7`, `u`, `g`, `h`]
            break
        case 'z':
            letters = [`a`, `s`, `x`]
            break
        case '1':
            letters = [`q`, `2`, '`']
            break
        case '2':
            letters = [`1`, `3`, `w`, `q`]
            break
        case '3':
            letters = [`2`, `4`, `e`, `w`]
            break
        case '4':
            letters = [`3`, `5`, `r`, `e`]
            break
        case '5':
            letters = [`4`, `6`, `t`, `r`]
            break
        case '6':
            letters = [`5`, `7`, `y`, `t`]
            break
        case '7':
            letters = [`6`, `8`, `u`, `y`]
            break
        case '8':
            letters = [`7`, `9`, `i`, `u`]
            break
        case '9':
            letters = [`8`, `0`, `o`, `i`]
            break
        case '0':
            letters = [`9`, `-`, `p`, `o`]
            break
        case `'`:
            letters = [`;`, `[`, `]`, `/`]
    }
    // replace the character at the random index with a random letter
    const output = input.replace(randomCharacter, letters[Math.floor(Math.random() * letters.length)])
    return output
}