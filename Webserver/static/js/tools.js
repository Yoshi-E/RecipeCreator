function debounce(callback, delay) {
	var timeout
	return function() {
		var args = arguments
		clearTimeout(timeout)
		timeout = setTimeout(function() {
			callback.apply(this, args)
		}.bind(this), delay)
	}
}

function debounce2(func, wait, immediate) {
	var timeout;
	return function() {
		var context = this, args = arguments;
		var later = function() {
			timeout = null;
			if (!immediate) func.apply(context, args);
		};
		var callNow = immediate && !timeout;
		clearTimeout(timeout);
		timeout = setTimeout(later, wait);
		if (callNow) func.apply(context, args);
	};
};

function throttle(func, interval) {
    var lastCall = 0;
    return function() {
        var now = Date.now();
        if (lastCall + interval < now) {
            lastCall = now;
            return func.apply(this, arguments);
        }
    };
}

function post_json(json, callback, xhrError = 0) {
		
		var xmlhttp = new XMLHttpRequest();   // new HttpRequest instance 
		var theUrl = "/setData.json";
		xmlhttp.open("POST", theUrl);
		xmlhttp.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
			if(xhrError != 0) {
		xmlhttp.onerror = xhrError;
		}
		xmlhttp.onload = function (e) {
			json = JSON.parse(e.target.response);
			callback(json);
		};
		xmlhttp.send(JSON.stringify(json))
};


function getColorForPercentage(pct) {
	var percentColors = [
    { pct: 0.0, color: { r: 0xff, g: 0x00, b: 0 } },
    { pct: 0.5, color: { r: 0xff, g: 0xff, b: 0 } },
    { pct: 1.0, color: { r: 0x00, g: 0xff, b: 0 } } ];

	
    for (var i = 1; i < percentColors.length - 1; i++) {
        if (pct < percentColors[i].pct) {
            break;
        }
    }
    var lower = percentColors[i - 1];
    var upper = percentColors[i];
    var range = upper.pct - lower.pct;
    var rangePct = (pct - lower.pct) / range;
    var pctLower = 1 - rangePct;
    var pctUpper = rangePct;
    var color = {
        r: Math.floor(lower.color.r * pctLower + upper.color.r * pctUpper),
        g: Math.floor(lower.color.g * pctLower + upper.color.g * pctUpper),
        b: Math.floor(lower.color.b * pctLower + upper.color.b * pctUpper)
    };
    return 'rgb(' + [color.r, color.g, color.b].join(',') + ')';
    // or output as hex if preferred
};

