const WIDGET = 0;
const POS = 1;
const COLOR = 2;
const ID = 3;
const SENSOR = 4;

const TEXT_STR = 3;
const TEXT_ID = 4;
const TEXT_SENSOR = 5;

const IMG_SRC = 2;

const RECT = 0;
const LINE = 1;
const CIRCLE = 2;
const ELLIPSE = 3;
const TEXT = 4;
const IMG = 5;
const COORD = 6;
const LINEAR = 7;
const PAGES = 8;

const X = 0;
const Y = 1;
const WIDTH = 2;
const HEIGHT = 3;

const TEXT_SIZE = 2;

function pixelfy(value: number | string, other: number){
    if (typeof value === "string" && value[value.length-1] == "%"){
        value = Number(value.slice(0, -1)) / 100 * other;
    }
    value = Number(value);
    return value < 0 ? value + other : value;
}

function draw(DOM: any[], base: [number, number, number, number] = [0, 0, 0, 0]){
    let xPos   = pixelfy(DOM[POS][X], base[WIDTH] ) + base[X];
    let yPos   = pixelfy(DOM[POS][Y], base[HEIGHT]) + base[Y];
    let width  = -1;
    let height = -1;
    if (DOM[WIDGET] != IMG && DOM[COLOR] == "transparent"){
        return;
    }
    if (DOM[WIDGET] != IMG){
        console.log("fillStyle", DOM[COLOR] ? DOM[COLOR] : "black")
    }
    if (DOM[WIDGET] != LINE || DOM[WIDGET] != TEXT){
        width  = pixelfy(DOM[POS][WIDTH] , base[WIDTH]);
        height = pixelfy(DOM[POS][HEIGHT], base[HEIGHT]);
    }
    if (DOM[WIDGET] == LINE){
        console.log("Line MoveTo", xPos, yPos);
        for (let i = 2; i < DOM[POS].length; i = i + 2){
            let xPos = pixelfy(DOM[POS][i]  , base[WIDTH] ) + base[X];
            let yPos = pixelfy(DOM[POS][i+1], base[HEIGHT]) + base[Y];
            console.log("Line LineTo", xPos, yPos);
        }
    }
    if (DOM[WIDGET] == RECT || DOM[WIDGET] == COORD){
        console.log("FillRect", xPos, yPos, width, height);
    }
    if (DOM[WIDGET] == CIRCLE){
        console.log("Draw circle", xPos, yPos, width)
    }
    if (DOM[WIDGET] == ELLIPSE){
        console.log("Draw Ellipse", xPos, yPos, width, height);
    }
    if (DOM[WIDGET] == TEXT){
        console.log("Draw Text", xPos, yPos, DOM[POS][TEXT_SIZE], DOM[TEXT_STR])
    }
    if (DOM[WIDGET] == IMG){
        console.log("Draw image", xPos, yPos, width, height, DOM[IMG_SRC]);
    }
    if (DOM[WIDGET] == COORD){
        for (let subDOM of DOM[DOM.length-1]){
            draw(subDOM, [xPos, yPos, width, height])
        }
    }
}

console.clear();
let layout = [COORD, [5, 9, 203, 179], "orange", [
    [RECT, [2, -8, "30%", "-40%"], "yellow"]
]];

draw(layout)