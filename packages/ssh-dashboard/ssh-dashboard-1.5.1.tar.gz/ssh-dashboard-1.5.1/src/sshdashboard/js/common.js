var FormatUptime = function(totalSeconds) {
    var days	= Math.floor(totalSeconds / 86400);
    totalSeconds %= 86400
    var hours   = Math.floor(totalSeconds / 3600);
    totalSeconds %= 3600
    var minutes = Math.floor(totalSeconds / 60);
    totalSeconds %= 60
    var seconds = totalSeconds;

    seconds = Math.round(seconds)

    var result = days + "d ";
    result += (hours < 10 ? "0" + hours : hours) + "h";
    result += " " + (minutes < 10 ? "0" + minutes : minutes) + "m";
    result += " " + (seconds  < 10 ? "0" + seconds : seconds) + "s";
    return result;
}

var FormatMemory = function(memory_kb) {
    if (memory_kb > 1073741824) return ((memory_kb / 1073741824).toFixed(2).toString()  + " TiB")
    if (memory_kb > 1048576)    return ((memory_kb / 1048576).toFixed(2).toString() 	+ " GiB")
    if (memory_kb > 1024) 		return ((memory_kb / 1024).toFixed(2).toString() 		+ " MiB")
    return (memory_kb.toFixed(2).toString() + " KiB")
}

var FormatTimestamp = function(unix_timestamp) {
    if (unix_timestamp == 0) return ""

    var timestamp = new Date(unix_timestamp * 1000);
    year    = timestamp.getFullYear();
    month   = ("0" + (timestamp.getMonth() + 1)).slice(-2);
    day     = ('0' + timestamp.getDate()).slice(-2);
    hours   = ('0' + timestamp.getHours()).slice(-2);
    minutes = ('0' + timestamp.getMinutes()).slice(-2);
    seconds = ('0' + timestamp.getSeconds()).slice(-2);
    return (day + "." + month + "." + year + " - " + hours + ":" + minutes + ":" + seconds);
}

var FormatLogEventKey = function(event) {
    switch (event.Key) {
        case "HostDown":
            if (event.Value) return "Disconnected from host"
            else             return "Connected to host"
        break;
        case "SysLoadWarning":
            if (event.Value) return "System load warning"
            else             return "System load ok"
        break;
        case "SysLoadWarning_1min":
            if (event.Value) return "System load (1 min average) warning"
            else             return "System load (1 min average) ok"
        break;
        case "SysLoadWarning_5min":
            if (event.Value) return "System load (5 min average) warning"
            else             return "System load (5 min average) ok"
        break;
        case "SysLoadWarning_15min":
            if (event.Value) return "System load (15 min average) warning"
            else             return "System load (15 min average) ok"
        break;
        case "MemLimitWarning":
            if (event.Value) return "Memory warning"
            else             return "Memory ok"
        break;
        case "SwapLimitWarning":
            if (event.Value) return "Swap warning"
            else             return "Swap ok"
        break;
        case "RootFsLimitWarning":
            if (event.Value) return "Root Filesystem warning"
            else             return "Root Filesystem ok"
        break;
        default:
            return event.Key + ": " + event.Value.toString()
    }

}

var FormatLogEvent = function(event) {
    // That's a bit dirty: every boolean value available from the metrics is indeed a warning, so show in red if it is true
    // Should be taken care on a per-key basis, or added as extra information through the REST API
    if (event.Value == true) color = "<span style='color: red'>"
    else                     color = "<span style='color: green'>"

    tablerow  = "<tr><td>" + color + FormatTimestamp(event.Timestamp) + "</span></td>"
    tablerow +="<td align='right'>" + color + FormatLogEventKey(event) + "</span></td>";
    tablerow += "</tr>"
    return tablerow
}

var ToggleFoldableContentWithButton = function(id_content, id_button, button_text_show, button_text_hide) {
    var elem = document.getElementById(id_content)
    var button = document.getElementById(id_button)
    if (elem.style.display === "block") {
        elem.style.display = "none";
        button.textContent = button_text_show;
    } else {
        elem.style.display = "block";
        button.textContent = button_text_hide;
    }
}