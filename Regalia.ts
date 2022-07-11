const WIDGET = 0;
const POS = 1;
const COLOR = 2;
const SENSOR = 3;

const TEXT_STR = 3;
const TEXT_SENSOR = 4;

const IMG_SRC = 2;

const PAGES_ACTIVE_PAGE_INDEX = 2;

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

function createCanvas(){
    let canvas = document.getElementById("myCanvas");
    if (!canvas){
        canvas = document.createElement("canvas");
        canvas.id = "myCanvas";
        canvas.style.padding = "0";
        document.body.insertBefore(canvas, document.body.childNodes[0]);
    }
    return canvas
}

const canvas = createCanvas();
const ctx = canvas.getContext("2d");
ctx.textBaseline = "hanging";

var mouse = {x: -1, y: -1};

canvas.addEventListener("mousemove", function(evt: any){
    mouse.x = evt.x;
    mouse.y = evt.y;
    //console.log(evt.x, evt.y, mouse.x, mouse.y)
})

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
    if (!(DOM[WIDGET] == IMG || DOM[WIDGET] == PAGES)){
        //console.log("fillStyle", DOM[COLOR] ? DOM[COLOR] : "black");
        ctx.fillStyle = DOM[COLOR] ? DOM[COLOR] : "black";
    }
    if (DOM[WIDGET] != LINE || DOM[WIDGET] != TEXT){
        width  = pixelfy(DOM[POS][WIDTH] , base[WIDTH]);
        height = pixelfy(DOM[POS][HEIGHT], base[HEIGHT]);
    }
    if (DOM[WIDGET] == LINE){
        ctx.strokeStyle = DOM[COLOR] ? DOM[COLOR] : "black";
        //console.log("Line MoveTo", xPos, yPos);
        ctx.beginPath();
        ctx.moveTo(xPos, yPos);
        for (let i = 2; i < DOM[POS].length; i = i + 2){
            let xPos = pixelfy(DOM[POS][i]  , base[WIDTH] ) + base[X];
            let yPos = pixelfy(DOM[POS][i+1], base[HEIGHT]) + base[Y];
            //console.log("Line LineTo", xPos, yPos);
            ctx.lineTo(xPos, yPos)
        }
        ctx.stroke();
    }
    if (DOM[WIDGET] == RECT || DOM[WIDGET] == COORD || DOM[WIDGET] == LINEAR){
        ctx.fillRect(xPos, yPos, width, height);
        //console.log("FillRect", xPos, yPos, width, height);
    }
    if (DOM[WIDGET] == CIRCLE){
        ctx.beginPath();
        ctx.arc(xPos, yPos, width, 0, 2 * Math.PI);
        ctx.fill();
        //console.log("Draw circle", xPos, yPos, width);
    }
    if (DOM[WIDGET] == ELLIPSE){
        ctx.beginPath();
        ctx.ellipse(xPos, yPos, width, height, 0, 0, 2 * Math.PI);
        ctx.fill();
        //console.log("Draw Ellipse", xPos, yPos, width, height);
    }
    if (DOM[WIDGET] == TEXT){
        //console.log("Draw Text", xPos, yPos, DOM[POS][TEXT_SIZE], DOM[TEXT_STR]);
        ctx.font = DOM[POS][TEXT_SIZE].toString() + "px Arial";
        ctx.fillText(DOM[TEXT_STR], xPos, yPos);
    }
    if (DOM[WIDGET] == IMG){
        //console.log("Draw image", xPos, yPos, width, height, DOM[IMG_SRC]);
        var img = document.createElement("img");
        img.src = DOM[IMG_SRC];
        ctx.drawImage(img, xPos, yPos, width, height);
    }
    if (DOM[WIDGET] == COORD){
        for (let subDOM of DOM[DOM.length-1]){
            draw(subDOM, [xPos, yPos, width, height]);
        }
    }
    if (DOM[WIDGET] == LINEAR){
        let yOffset = 0;
        for (let subDOM of DOM[DOM.length-1]){
            draw(subDOM, [xPos, yPos + yOffset, width, height]);
            yOffset = yOffset + getBlockHeight(subDOM, [xPos, yPos, width, height]);
        }
    }
    if (DOM[WIDGET] == PAGES){
        draw(DOM[DOM.length-1][DOM[PAGES_ACTIVE_PAGE_INDEX]], [xPos, yPos, width, height]);
    }
}

function sensor(DOM: any[], mouseXPos: number, mouseYPos: number, base: [number, number, number, number] = [0, 0, 0, 0]){
    let isInside = false;
    let xPos   = pixelfy(DOM[POS][X], base[WIDTH] ) + base[X];
    let yPos   = pixelfy(DOM[POS][Y], base[HEIGHT]) + base[Y];
    let width  = -1;
    let height = -1;
    if (DOM[WIDGET] != LINE || DOM[WIDGET] != TEXT){
        width  = pixelfy(DOM[POS][WIDTH] , base[WIDTH]);
        height = pixelfy(DOM[POS][HEIGHT], base[HEIGHT]);
    }
    if (DOM[WIDGET] == CIRCLE){
        if ((mouseXPos-xPos)**2 + (mouseYPos-yPos)**2 < width**2){
            isInside = true;
        }
    }
    if (DOM[WIDGET] == ELLIPSE){
        return;
    }
    if (DOM[WIDGET] == RECT || DOM[WIDGET] == IMG){
        if (xPos < mouseXPos && mouseXPos < xPos + width && yPos < mouseYPos && mouseYPos < yPos + height){
            isInside = true;
        }
    }
    if (DOM[WIDGET] == COORD || DOM[WIDGET] == LINEAR){
        if (xPos < mouseXPos && mouseXPos < xPos + width && yPos < mouseYPos && mouseYPos < yPos + height && DOM.length > 4){
            isInside = true;
        }
    }
    if (isInside){
        if (typeof DOM[SENSOR][0] === "function"){
            DOM[SENSOR][0](mouseXPos, mouseYPos);
        }
    }

    if (!isInside){
        if (DOM[SENSOR]){
            if (typeof DOM[SENSOR][1] === "function"){
                DOM[SENSOR][1](mouseXPos, mouseYPos)
            }
        }
    }

    if (DOM[WIDGET] == COORD){
        for (let subDOM of DOM[DOM.length-1]){
            sensor(subDOM, mouseXPos, mouseYPos, [xPos, yPos, width, height]);
        }
    }
    if (DOM[WIDGET] == LINEAR){
        let yOffset = 0;
        for (let subDOM of DOM[DOM.length-1]){
            sensor(subDOM, mouseXPos, mouseYPos, [xPos, yPos + yOffset, width, height]);
            yOffset = yOffset + getBlockHeight(subDOM, [xPos, yPos, width, height]);
        }
    }
    if (DOM[WIDGET] == PAGES){
        sensor(DOM[DOM.length-1][DOM[PAGES_ACTIVE_PAGE_INDEX]], mouseXPos, mouseYPos, [xPos, yPos, width, height]);
    }
}

console.clear();

var refresh = true;
var layout = [PAGES, [0, 0, 500, 500], 0, [
    [COORD, [0, 0, "100%", "100%"], "white", [
        [RECT, ["5%", 10, 10, 10], "red", [function(x:number,y:number){
            layout[3][0][3][0][2] = "green";
            refresh = true;
        }, function(x:number,y:number){
            layout[3][0][3][0][2] = "red";
            refresh = true;
        }]],
        [CIRCLE, [50, 30, 10], "green", [function(x:number,y:number){
            layout[3][0][3][1][2] = "purple";
            refresh = true;
        }]],
        [LINE, [50, 10, 20, 10, 70, 20], "orange"],
        [LINE, [150, 10, 120, 10, 170, 20], "yellow"],
        [ELLIPSE, [100, 100, 20, 30], "aquamarine"],
        [TEXT, [10, 20, 10], "blue", "AAA"],
        [IMG, [200, 100, 100, 100], "https://framtida.no/wp-content/uploads/2020/08/edvin1.jpg"]
    ]]
]]

ctx.clearRect(0, 0, canvas.width, canvas.height);
draw(layout);

setInterval(function(){
    if (refresh){
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        draw(layout);
        refresh = false;
    }
    sensor(layout, mouse.x, mouse.y);
}, 100);
