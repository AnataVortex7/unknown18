import sys
import os

if len(sys.argv) < 2:
    print("Usage: python trackpad_patch.py <path_to_vnc_html>")
    sys.exit(1)

filepath = sys.argv[1]
if not os.path.exists(filepath):
    print(f"File not found: {filepath}")
    sys.exit(1)

trackpad_js = """
// --- VIRTUAL TRACKPAD WIDGET ---
setTimeout(function() {
    var pad = document.createElement("div");
    pad.id = "virtual-trackpad";
    pad.style.position = "fixed";
    pad.style.bottom = "20px";
    pad.style.right = "20px";
    pad.style.width = "220px";
    pad.style.height = "280px";
    pad.style.backgroundColor = "rgba(50, 50, 50, 0.6)";
    pad.style.borderRadius = "10px";
    pad.style.zIndex = "999999";
    pad.style.display = "flex";
    pad.style.flexDirection = "column";
    pad.style.boxShadow = "0 4px 10px rgba(0,0,0,0.5)";
    pad.style.touchAction = "none";

    // Header (Draggable)
    var header = document.createElement("div");
    header.style.height = "30px";
    header.style.backgroundColor = "rgba(0,0,0,0.7)";
    header.style.borderTopLeftRadius = "10px";
    header.style.borderTopRightRadius = "10px";
    header.style.color = "white";
    header.style.textAlign = "center";
    header.style.lineHeight = "30px";
    header.style.fontSize = "14px";
    header.style.cursor = "move";
    header.style.userSelect = "none";
    header.innerHTML = "🖱️ Trackpad <span id='pad-close' style='float:right;margin-right:10px;cursor:pointer;color:red;'>✖</span>";
    pad.appendChild(header);

    // Settings Controls
    var controls = document.createElement("div");
    controls.style.display = "flex";
    controls.style.justifyContent = "space-around";
    controls.style.padding = "5px 0";

    // Opacity Slider
    var sliderCont = document.createElement("div");
    sliderCont.style.textAlign = "center";
    sliderCont.style.color = "white";
    sliderCont.style.fontSize = "11px";
    sliderCont.style.padding = "2px";
    sliderCont.innerHTML = "Opacity: ";
    var slider = document.createElement("input");
    slider.type = "range";
    slider.min = "0.1";
    slider.max = "1.0";
    slider.step = "0.1";
    slider.value = "0.6";
    slider.style.width = "90px";
    slider.style.verticalAlign = "middle";
    slider.addEventListener("input", function(e) {
        pad.style.backgroundColor = "rgba(50, 50, 50, " + e.target.value + ")";
    });
    sliderCont.appendChild(slider);
    controls.appendChild(sliderCont);

    // Size Slider
    var sizeCont = document.createElement("div");
    sizeCont.style.textAlign = "center";
    sizeCont.style.color = "white";
    sizeCont.style.fontSize = "11px";
    sizeCont.style.padding = "2px";
    sizeCont.innerHTML = "Size: &nbsp;&nbsp;&nbsp;&nbsp;";
    var sizeSlider = document.createElement("input");
    sizeSlider.type = "range";
    sizeSlider.min = "120";
    sizeSlider.max = "450";
    sizeSlider.step = "10";
    sizeSlider.value = "220";
    sizeSlider.style.width = "90px";
    sizeSlider.style.verticalAlign = "middle";
    sizeSlider.addEventListener("input", function(e) {
        var w = parseInt(e.target.value);
        pad.style.width = w + "px";
        pad.style.height = (w * 1.25) + "px";
    });
    sizeCont.appendChild(sizeSlider);
    controls.appendChild(sizeCont);

    pad.appendChild(controls);

    // Touch Area
    var touchArea = document.createElement("div");
    touchArea.style.flex = "1";
    touchArea.style.border = "2px dashed rgba(255,255,255,0.4)";
    touchArea.style.margin = "5px";
    touchArea.style.borderRadius = "5px";
    touchArea.style.backgroundColor = "rgba(255,255,255,0.1)";
    touchArea.innerHTML = "<div style='color:white;text-align:center;margin-top:30%;opacity:0.7;user-select:none;pointer-events:none;'>👆 Slide (2 Fingers = Scroll)</div>";
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
    var touchMoved = false;
    var isTwoFinger = false;
    var initialDist = 0;

    function sendEvent(type, button, cx, cy, deltaY, isZoom) {
        var canvas = document.querySelector("#noVNC_canvas canvas") || document.querySelector("canvas");
        if(!canvas) return;
        if (type === "wheel") {
            var e = new WheelEvent("wheel", {
                bubbles: true, cancelable: true,
                clientX: cx, clientY: cy,
                deltaY: deltaY, deltaMode: 0,
                ctrlKey: isZoom === true
            });
            canvas.dispatchEvent(e);
            return;
        }
        var e = new MouseEvent(type, {
            bubbles: true, cancelable: true,
            clientX: cx, clientY: cy,
            button: button,
            buttons: button === 0 ? 1 : (button === 2 ? 2 : 0)
        });
        canvas.dispatchEvent(e);
    }

    touchArea.addEventListener("touchstart", function(e) {
        touchMoved = false;
        if (e.touches.length === 2) {
            isTwoFinger = true;
            lastTouchY = e.touches[0].clientY;
            var dx = e.touches[0].clientX - e.touches[1].clientX;
            var dy = e.touches[0].clientY - e.touches[1].clientY;
            initialDist = Math.sqrt(dx*dx + dy*dy);
        } else if (e.touches.length === 1) {
            isTwoFinger = false;
            initialDist = 0;
            lastTouchX = e.touches[0].clientX;
            lastTouchY = e.touches[0].clientY;
        }
        e.preventDefault();
    }, {passive: false});

    touchArea.addEventListener("touchmove", function(e) {
        touchMoved = true;
        if (isTwoFinger && e.touches.length === 2) {
            var dx = e.touches[0].clientX - e.touches[1].clientX;
            var dy = e.touches[0].clientY - e.touches[1].clientY;
            var currentDist = Math.sqrt(dx*dx + dy*dy);
            
            // Check if it's a pinch (zoom) or a scroll
            if (Math.abs(currentDist - initialDist) > 30) {
                // Zoom
                var zoomDir = (currentDist > initialDist) ? -100 : 100; // Pinch out = zoom in (-), Pinch in = zoom out (+)
                sendEvent("wheel", 0, vCursorX, vCursorY, zoomDir, true);
                initialDist = currentDist;
            } else {
                // Normal Two finger scroll
                var scrolldy = e.touches[0].clientY - lastTouchY;
                lastTouchY = e.touches[0].clientY;
                if (Math.abs(scrolldy) > 2) {
                    sendEvent("wheel", 0, vCursorX, vCursorY, scrolldy > 0 ? 100 : -100, false);
                }
            }
        } else if (e.touches.length === 1 && !isTwoFinger) {
            // Normal cursor move
            var dx = e.touches[0].clientX - lastTouchX;
            var dy = e.touches[0].clientY - lastTouchY;
            lastTouchX = e.touches[0].clientX;
            lastTouchY = e.touches[0].clientY;
            
            vCursorX += dx * 1.5; 
            vCursorY += dy * 1.5;
            
            if(vCursorX < 0) vCursorX = 0;
            if(vCursorX > window.innerWidth) vCursorX = window.innerWidth;
            if(vCursorY < 0) vCursorY = 0;
            if(vCursorY > window.innerHeight) vCursorY = window.innerHeight;

            sendEvent("mousemove", -1, vCursorX, vCursorY, 0, false);
        }
        e.preventDefault();
    }, {passive: false});

    touchArea.addEventListener("touchend", function(e) {
        if (!isTwoFinger && !touchMoved) {
            // It was a clean Tap -> Send Click
            sendEvent("mousedown", 0, vCursorX, vCursorY, 0, false);
            sendEvent("mouseup", 0, vCursorX, vCursorY, 0, false);
        }
        if (e.touches.length === 0) {
            isTwoFinger = false;
            initialDist = 0;
        }
        e.preventDefault();
    }, {passive: false});

    function addBtnLogic(btn, btnCode) {
        btn.addEventListener("touchstart", function(e) {
            sendEvent("mousedown", btnCode, vCursorX, vCursorY, 0);
            btn.style.backgroundColor = "white";
            btn.style.color = "black";
            e.preventDefault();
        }, {passive: false});
        btn.addEventListener("touchend", function(e) {
            sendEvent("mouseup", btnCode, vCursorX, vCursorY, 0);
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

with open(filepath, 'r') as f:
    content = f.read()
    
if "<script>\n// --- VIRTUAL TRACKPAD WIDGET ---" in content:
    content = content.split("<script>\n// --- VIRTUAL TRACKPAD WIDGET ---")[0] + "</body>\n</html>"

script_tag = f"\\n<script>\\n{trackpad_js}\\n</script>\\n</body>"
content = content.replace("</body>", script_tag)

with open(filepath, 'w') as f:
    f.write(content)
