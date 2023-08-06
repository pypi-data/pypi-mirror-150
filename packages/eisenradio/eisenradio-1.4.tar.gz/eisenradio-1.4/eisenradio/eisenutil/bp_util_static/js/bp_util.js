const div_toolsExportUrl = document.getElementById("div_toolsExportUrl");
const div_toolsExportTracLists = document.getElementById("div_toolsExportTracLists");
const div_toolsImport = document.getElementById("div_toolsImport");
const div_toolsImportTraceLists = document.getElementById("div_toolsImportTraceLists");
const fadeIn = [
    {opacity: 0},
    {opacity: 1}
];
const faderTiming = {
    duration: 1000,
    iterations: 1,
};


function delFromBlacklist(counter, radioName) {
        /*
    tell server to del items or the whole list
    */
    const checkbox_whole_radio_blacklist = document.getElementById('checkbox_whole_radio_blacklist');
    var delDictIndexes = {};
    var delAll = false;

    if(checkbox_whole_radio_blacklist.checked){
        delAll = true;
        for(let i = 1; i <= counter; i++){
            let checkBox = document.getElementById("check_radio_blacklist_" + i);
            delDictIndexes[i - 1] = checkBox.value;
        }
    } else {
        // loopIndex in template starts with 1
        for(let i = 1; i <= counter; i++){
            let checkBox = document.getElementById("check_radio_blacklist_" + i);
            if(checkBox.checked){
                delDictIndexes[i - 1] = checkBox.value;
            }
        }
    }
    let radioInfoDict = {
                        'radio_name': radioName,
                        'delAll': delAll,
                        'del_dict': delDictIndexes
                        }
    let req = $.ajax({
        type: 'Post',
        dataType: 'json',
        url: "/tools_radio_blacklist_del_from_list",
        cache: false,
        data:  radioInfoDict
    });

    req.done(function (data) {
        if (data.delFromBlacklist == "_ok_") {

            // disable all boxes and buttons
            checkbox_whole_radio_blacklist.disabled = true;
            const button_radio_blacklist = document.getElementById("button_radio_blacklist");
            button_radio_blacklist.disabled = true;
            const button_radio_skipped = document.getElementById("button_radio_skipped");
            button_radio_skipped.disabled = true;
            for(let i = 1; i <= counter; i++){
                let checkBox = document.getElementById("check_radio_blacklist_" + i);
                checkBox.disabled = true;
            }
            //var delAll
            if(delAll)
                {alert("Done")}
            else {
                // java dict Object.keys is list of key names
                if(Object.keys(delDictIndexes).length > 0){
                    alert(Object.keys(delDictIndexes).length + " items deleted. Linux/Windows can check Terminal Window.")
                } else {
                    alert("You burned 0.001 kcal by pressing a button.")
                }
            }


        } else {
            alert("Failure. Linux/Windows can check Terminal Window.")
        }
    });
}
;


function exportUrls(){
        /*
    Show or hide Export/Import selected choice
    */
    div_toolsExportUrl.style.display = "block";
    div_toolsExportTracLists.style.display = "none";
}
;

function exportTraceLists(){
    div_toolsExportUrl.style.display = "none";
    div_toolsExportTracLists.style.display = "block";
}
;

function importUrls(){
    div_toolsImport.style.display = "block";
    div_toolsImportTraceLists.style.display = "none";
}
;

function importTraceLists(){
    div_toolsImport.style.display = "none";
    div_toolsImportTraceLists.style.display = "block";
}
;

function aacpRepairDivShow(){
        /*
    Show or hide a Tool section
    */
    const showDiv = document.getElementById("aacpRepairDiv");
    const headLine = document.getElementById("aacpRepairHeadline");
    toggleHeadlines(showDiv);
    toggleHeadlineChoice(showDiv, headLine);
}
;

function monitorRecordsShow(){
    const showDiv = document.getElementById("monitorRecordsDiv");
    const headLine = document.getElementById("monitorRecordsHeadline");
    toggleHeadlines(showDiv);
    toggleHeadlineChoice(showDiv, headLine);
}
;

function exportShow(){
    const showDiv = document.getElementById("exportDiv");
    const headLine = document.getElementById("exportHeadline");
    toggleHeadlines(showDiv);
    toggleHeadlineChoice(showDiv, headLine);
}
;

function importShow(){
    const showDiv = document.getElementById("importDiv");
    const headLine = document.getElementById("importHeadline");
    toggleHeadlines(showDiv);
    toggleHeadlineChoice(showDiv, headLine);
}
;

function deleteShow(){
    const showDiv = document.getElementById("deleteDiv");
    const headLine = document.getElementById("deleteHeadline");
    toggleHeadlines(showDiv);
    toggleHeadlineChoice(showDiv, headLine);
}
;

function toggleHeadlineChoice(divElem, headLine){
        /*
    move headline of tool to right or middle for better separation
    */

    if(divElem.style.display == "block"){
        headLine.style.textAlign = "start";
        headLine.animate(fadeIn, faderTiming);
    } else {
       headLine.style.textAlign = "center";
    }
}
;

function toggleHeadlines(element, headLine){
        /*
    show or hide the tool if headline is clicked
    */
    const showDiv = element;
    if(showDiv.style.display == "" || showDiv.style.display == "none"){
        showDiv.style.display = "block";
    } else {
       showDiv.style.display = "none";
    }
}
;

function toolsExportIni() {
        /*
   export ini file with radio names and URLs
    */
    let req = $.ajax({
        type: 'GET',
        url: "/tools_export_ini",
        cache: false
    });

    req.done(function (data) {
        if (data.toolsExportIni !== "-empty-") {
            let result = data.toolsExportIni
            if (result){
                alert("OK Ini");
                } else {
                alert("Ini Failed")
                }
        }
    });
}
;

function toolsExportBlacklists() {
        /*
   export Blacklists file feedback
    */
    let req = $.ajax({
        type: 'GET',
        url: "/tools_export_blacklists",
        cache: false
    });

    req.done(function (data) {
        if (data.toolsExportBlacklists !== "-empty-") {
            let result = data.toolsExportBlacklists
            if (result){
                alert("OK Blacklists");
                } else {
                alert("Failed")
                }
        }
    });
}
;

