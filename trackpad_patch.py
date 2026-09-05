import re
import sys

filepath = sys.argv[1]

# The Trackpad JS code
trackpad_js = """
// --- VIRTUAL TRACKPAD WIDGET ---
setTimeout(function() {
    var pad = document.createElement("div");
    pad.id = "virtual-trackpad";
    pad.style.position = "fixed";
    pad.style.bottom = "20px";
    pad.style.right = "20px";
    pad.style.width = "220px";
    pad.style.height = "260px";
    pad.style.backgroundColor = "rgba(50, 50, 50, 0.6)";
    pad.style.borderRadius = "10px";
    pad.style.zIndex = "999999";
    pad.style.display = "flex";
    pad.style.flexDirection = "column";
    pad.style.touchAction = "none";
    pad.style.boxShadow = "0 4px 8px rgba(0,0,0,0.3)";
    
    // Header (Move Handle)
    var header = document.createElement("div");
    header.style.height = "35px";
    header.style.backgroundColor = "rgba(20,20,20,0.8)";
    header.style.color = "white";
    header.style.textAlign = "center";
    header.style.lineHeight = "35px";
    header.style.borderTopLeftRadius = "10px";
    header.style.borderTopRightRadius = "10px";
    header.style.cursor = "move";
    header.style.userSelect = "none";
    header.innerHTML = "↕️ Drag | <span id='pad-close' style='color:#ff4c4c;cursor:pointer;font-weight:bold;float:right;margin-right:15px;'>✖ Hide</span>";
    pad.appendChild(header);

    // Opacity Slider
    var sliderCont = document.createElement("div");
    sliderCont.style.textAlign = "center";
    sliderCont.style.color = "white";
    sliderCont.style.fontSize = "12px";
    sliderCont.style.padding = "2px";
    sliderCont.innerHTML = "Transparency: ";
    var slider = document.createElement("input");
    slider.type = "range";
    slider.min = "0.1";
    slider.max = "1.0";
    slider.step = "0.1";
    slider.value = "0.6";
    slider.style.width = "100px";
    slider.style.verticalAlign = "middle";
    slider.addEventListener("input", function(e) {
        pad.style.backgroundColor = "rgba(50, 50, 50, " + e.target.value + ")";
    });
    sliderCont.appendChild(slider);
    pad.appendChild(sliderCont);

    // Touch Area
    var touchArea = document.createElement("div");
    touchArea.style.flex = "1";
    touchArea.style.border = "2px dashed rgba(255,255,255,0.4)";
    touchArea.style.margin = "5px";
    touchArea.style.borderRadius = "5px";
    touchArea.style.backgroundColor = "rgba(255,255,255,0.1)";
    touchArea.innerHTML = "<div style='color:white;text-align:center;margin-top:30%;opacity:0.7;user-select:none;'>👆 Slide here<br><br><small>(Tap to click)</small></div>";
    pad.appendChild(touchArea);
    
    // Buttons Row
    var btnRow = document.createElement("div");
    btnRow.style.display = "flex";
    btnRow.style.height = "45px";
    btnRow.style.gap = "5px";
    btnRow.style.padding = "5px";
    
    function makeBtn(text) {
        var b = document.createElement("button");
        b.innerText = text;
        b.style.flex = "1";
        b.style.borderRadius = "5px";
        b.style.border = "none";
        b.style.backgroundColor = "rgba(100,100,255,0.8)";
        b.style.color = "white";
        b.style.fontWeight = "bold";
        return b;
    }
    
    var leftBtn = makeBtn("L-Click");
    var rightBtn = makeBtn("R-Click");
    btnRow.appendChild(leftBtn);
    btnRow.appendChild(rightBtn);
    pad.appendChild(btnRow);

    document.body.appendChild(pad);

    // Toggle Button
    var toggleBtn = document.createElement("div");
    toggleBtn.innerHTML = "🖱️ Trackpad";
    toggleBtn.style.position = "fixed";
    toggleBtn.style.top = "10px";
    toggleBtn.style.left = "50%";
    toggleBtn.style.transform = "translateX(-50%)";
    toggleBtn.style.backgroundColor = "rgba(50, 50, 50, 0.8)";
    toggleBtn.style.color = "white";
    toggleBtn.style.padding = "10px 20px";
    toggleBtn.style.borderRadius = "20px";
    toggleBtn.style.zIndex = "999999";
    toggleBtn.style.display = "none";
    toggleBtn.style.cursor = "pointer";
    toggleBtn.style.boxShadow = "0 2px 5px rgba(0,0,0,0.5)";
    toggleBtn.onclick = function() {
        pad.style.display = "flex";
        toggleBtn.style.display = "none";
    };
    document.body.appendChild(toggleBtn);

    // --- LOGIC ---
    var vCursorX = window.innerWidth / 2;
    var vCursorY = window.innerHeight / 2;
    var lastTouchX = 0, lastTouchY = 0;

    function sendEvent(type, button, cx, cy) {
        var canvas = document.querySelector("#noVNC_canvas canvas") || document.querySelector("canvas");
        if(!canvas) return;
        var e = new MouseEvent(type, {
            bubbles: true,
            cancelable: true,
            clientX: cx,
            clientY: cy,
            button: button,
            buttons: button === 0 ? 1 : (button === 2 ? 2 : 0)
        });
        canvas.dispatchEvent(e);
    }

    touchArea.addEventListener("touchstart", function(e) {
        lastTouchX = e.touches[0].clientX;
        lastTouchY = e.touches[0].clientY;
        e.preventDefault();
    }, {passive: false});

    touchArea.addEventListener("touchmove", function(e) {
        var dx = e.touches[0].clientX - lastTouchX;
        var dy = e.touches[0].clientY - lastTouchY;
        lastTouchX = e.touches[0].clientX;
        lastTouchY = e.touches[0].clientY;
        
        vCursorX += dx * 1.5; // Mouse sensitivity
        vCursorY += dy * 1.5;
        
        if(vCursorX < 0) vCursorX = 0;
        if(vCursorX > window.innerWidth) vCursorX = window.innerWidth;
        if(vCursorY < 0) vCursorY = 0;
        if(vCursorY > window.innerHeight) vCursorY = window.innerHeight;

        sendEvent("mousemove", -1, vCursorX, vCursorY);
        e.preventDefault();
    }, {passive: false});

    var lastTap = 0;
    touchArea.addEventListener("touchend", function(e) {
        var currentTime = new Date().getTime();
        var tapLength = currentTime - lastTap;
        
        if (tapLength < 300 && tapLength > 0) { // Double tap
            sendEvent("mousedown", 0, vCursorX, vCursorY);
            sendEvent("mouseup", 0, vCursorX, vCursorY);
        } else { // Single tap (Left click)
            sendEvent("mousedown", 0, vCursorX, vCursorY);
            sendEvent("mouseup", 0, vCursorX, vCursorY);
        }
        lastTap = currentTime;
        e.preventDefault();
    }, {passive: false});

    function addBtnLogic(btn, btnCode) {
        btn.addEventListener("touchstart", function(e) {
            sendEvent("mousedown", btnCode, vCursorX, vCursorY);
            btn.style.backgroundColor = "white";
            btn.style.color = "black";
            e.preventDefault();
        }, {passive: false});
        btn.addEventListener("touchend", function(e) {
            sendEvent("mouseup", btnCode, vCursorX, vCursorY);
            btn.style.backgroundColor = "rgba(100,100,255,0.8)";
            btn.style.color = "white";
            e.preventDefault();
        }, {passive: false});
    }
    addBtnLogic(leftBtn, 0);
    addBtnLogic(rightBtn, 2);

    // Draggable Pad Logic
    var dragging = false, dOffsetX, dOffsetY;
    header.addEventListener("touchstart", function(e) {
        if(e.target.id === "pad-close") {
            pad.style.display = "none";
            toggleBtn.style.display = "block";
            return;
        }
        dragging = true;
        var rect = pad.getBoundingClientRect();
        dOffsetX = e.touches[0].clientX - rect.left;
        dOffsetY = e.touches[0].clientY - rect.top;
        e.preventDefault();
    }, {passive: false});
    
    document.addEventListener("touchmove", function(e) {
        if(dragging) {
            var x = e.touches[0].clientX - dOffsetX;
            var y = e.touches[0].clientY - dOffsetY;
            pad.style.left = x + "px";
            pad.style.top = y + "px";
            pad.style.bottom = "auto";
            pad.style.right = "auto";
            e.preventDefault();
        }
    }, {passive: false});
    
    document.addEventListener("touchend", function(e) {
        if(dragging) { dragging = false; }
    });

}, 2000);
"""

# Read vnc.html and inject the script at the end of the body
with open(filepath, 'r') as f:
    content = f.read()

# Add script tag
script_tag = f"\n<script>\n{trackpad_js}\n</script>\n</body>"
content = content.replace("</body>", script_tag)

with open(filepath, 'w') as f:
    f.write(content)

