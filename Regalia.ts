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

function getBlockWidth(DOM: any[], base: [number, number, number, number] = [0, 0, 0, 0]){
    if (DOM[WIDGET] == LINE){
        return Math.max(...DOM[POS].filter(function(_: any, i: number){
            return i % 2 == 0
        }).map(function(e: number | string){
            return pixelfy(e, base[WIDTH])
        }))
    }
    else{
        return pixelfy(DOM[POS][X], base[WIDTH]) + pixelfy(DOM[POS][WIDTH], base[WIDTH])
    }
}

function getBlockHeight(DOM: any[], base: [number, number, number, number] = [0, 0, 0, 0]){
    if (DOM[WIDGET] == LINE){
        return Math.max(...DOM[POS].filter(function(_: any, i: number){
            return i % 2 == 1
        }).map(function(e: number | string){
            return pixelfy(e, base[HEIGHT])
        }))
    }
    else if (DOM[WIDGET] == CIRCLE){
        return pixelfy(DOM[POS][Y], base[HEIGHT]) + pixelfy(DOM[POS][WIDTH], base[WIDTH]);
    }
    else{
        return pixelfy(DOM[POS][Y], base[HEIGHT]) + pixelfy(DOM[POS][HEIGHT], base[HEIGHT]);
    }
}

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
    if (DOM[WIDGET] == RECT || DOM[WIDGET] == COORD || DOM[WIDGET] == LINEAR){
        console.log("FillRect", xPos, yPos, width, height);
    }
    if (DOM[WIDGET] == CIRCLE){
        console.log("Draw circle", xPos, yPos, width)
    }
    if (DOM[WIDGET] == ELLIPSE){
        console.log("Draw Ellipse", xPos, yPos, width, height);
    }
    if (DOM[WIDGET] == TEXT){
        console.log("Draw Text", xPos, yPos, DOM[POS][TEXT_SIZE], DOM[TEXT_STR]);
    }
    if (DOM[WIDGET] == IMG){
        console.log("Draw image", xPos, yPos, width, height, DOM[IMG_SRC]);
    }
    if (DOM[WIDGET] == COORD){
        for (let subDOM of DOM[DOM.length-1]){
            draw(subDOM, [xPos, yPos, width, height]);
        }
    }
    if (DOM[WIDGET] == LINEAR){
        let yOffset = 0;
        for (let subDOM of DOM[DOM.length-1]){
            draw(subDOM, [xPos, yPos + yOffset, width, height])
            yOffset = yOffset + getBlockHeight(subDOM, [xPos, yPos, width, height])
        }
    }
}

console.clear();


let layout = [LINEAR, [5, 9, 203, 179], "orange", [
    [RECT, [2, -8, "30%", "-40%"], "yellow"],
    [CIRCLE, ["5%", 70, "20%"], "purple"],
    [LINE, [3, -9, 2, "-8%", "31%", 17], "blue"],
    [IMG, [-10, "9%", 7, 17], "a.png"],
    [COORD, ["7%", 7, "50%", "50%"], "green", [
        [RECT, [12, "2%", "3%", 4], "aquamarine"],
        [LINE, [3, 8, "5%", "3%", "7%", 10], "marron"],
        [IMG, [40, 5, 10, 10], "a.png"]
    ]],
    [CIRCLE, ["2%", "3%", 20], "red"]
]];

draw(layout)
