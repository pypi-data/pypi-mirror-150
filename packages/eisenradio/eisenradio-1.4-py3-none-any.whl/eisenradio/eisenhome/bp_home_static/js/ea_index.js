const pageCover = document.getElementById("pageCover");
const pageCoverCanvas = document.getElementById("pageCoverCanvas");
const pageCoverCanvasCtx = pageCoverCanvas.getContext('2d');
const canvasMaster = document.getElementById("canvasMaster");
const canvasMasterCtx = canvasMaster.getContext('2d');
const currentRadioName = document.getElementById('currentRadioName');
const fileUpload = document.getElementById("fileUpload");
const playBtn = document.getElementById("playBtn");
const pauseBtn = document.getElementById("pauseBtn");
const audio = document.getElementById("audioWithControls");
const audioVolumeController = document.getElementById("audioVolumeController");
const audioGainController = document.getElementById("audioGainController");

var audioContext, audioSource, analyserNode, gainNode, analyserRandom;
var spectrumAnalyserActive = false;
var spectrumAnalyserShow = false;

$(document).ready(function () {

    pageCoverAnimation();
    darkModeGet();
    stationGet();
    streamerGet();

    setInterval(deleteInfo, 15005);
    setInterval(headerInfo, 10004);
    setInterval(toggleShowSelectBox, 5003);
    setInterval(updateMasterProgress, 5002);
    setInterval(updateDisplay, 5001);

    $('[data-toggle="tooltip"]').tooltip()
    $("button").click(recOrListenAction)
    pageCover.addEventListener('click', removePageCover);
    audioVolumeController.addEventListener("input", setAudioVolume);
    audioGainController.addEventListener("input", setAudioGain);
    fileUpload.addEventListener("change", playLocalAudio);
    
    audio.addEventListener("play", function () {
        playBtn.style.display = "none";
        pauseBtn.style.display = "block";
        pauseBtn.style.cursor = "pointer";
        pauseBtn.style.cursor = "hand";
        $("#pauseBtn").on('click', function () {
            audio.pause();
        });
    });
    audio.addEventListener("pause", function () {
        playBtn.style.display = "block";
        pauseBtn.style.display = "none";
        playBtn.style.cursor = "pointer";
        playBtn.style.cursor = "hand";
        $("#playBtn").on('click', function () {
            audio.play();
        });
    });

})
;

function setAudioContextVisual() {
    audioContext = new AudioContext();
    gainNode = audioContext.createGain();
    analyserNode = audioContext.createAnalyser();
    audioSource = audioContext.createMediaElementSource(audio);
    audioSource.connect(analyserNode).connect(gainNode).connect(audioContext.destination)
}
;

function countUpDownInclusiveInt(min, max) {

    if (animatedFunctionTimer >= max) {direction = 0;}
    if (animatedFunctionTimer <= min ) {direction = 1;}
    if (direction == 1) {animatedFunctionTimer++;}
    if (direction == 0) {animatedFunctionTimer--;}
    return animatedFunctionTimer;
}
;

function removePageCover() {
    stopVisualise();
    pageCover.style.display = "none";
    pageCoverCanvas.style.display = "none";
    setAudioContextVisual();
    cookie_start_set_text_show_visuals();
}
;

function setAudioVolume() {
        /*
    audioVolumeController has hardcoded safety init value of 25 (0.25 audio)
    */
    audio.volume = audioVolumeController.value / 100;
}
;

function setAudioGain() {
    gainNode.gain.value = audioGainController.value;
}
;

function stopVisualise(e) {    // had to insert this event
    try {
        window.cancelAnimationFrame(requestIdAnimationFrame);
    } catch (error) { console.error(error); }
    try {
        window.cancelAnimationFrame(requestIdFieldAnimation);
    } catch (error) { console.error(error); }
    requestIdFieldAnimation = undefined;
    requestIdAnimationFrame = undefined;
    spectrumAnalyserActive = false;
}
;

function reloadAudioElement(newAudioSource, isPlayList) {

    if (!isPlayList) {
        audio.volume = 0.25;
        audioVolumeController.value = 25;
        gainNode.gain.value = 1
        audioGainController.value = 1;
    }
    audio.src = "";
    audio.currentTime = 0;
    audio.srcObject = null;
    audio.src = newAudioSource;
    audio.load();
    audio.play();

    selectSpectrumAnalyser();
}
;

function randomOne() {
    return Math.random() >= 0.5 ? 1: -1;
}
;

function updateDisplay() {
    var req;

    req = $.ajax({
        type: 'GET',
        url: "/display_info",
        cache: false
    });

    req.done(function (data) {
        let displays_dict = data.updateDisplay
        $.each(displays_dict, function (idx, val) {
            let radioId = idx;
            let textInfo = val;
            try {
                document.getElementById("Display_" + radioId).value = textInfo;
            } catch (error) { console.error(error); }
        });
    });
}
;

function updateMasterProgress() {
    var req;

    req = $.ajax({
        type: 'POST',
        url: "/index_posts_percent",
        cache: false,
        data: { 'percent': 'percent' }
    });

    req.done(function (data) {
        var percent = '';

        percent = data.result;
        if (percent === 0) {
            $('.progress-bar').css('width', 25 + '%').attr('aria-valuenow', 25).html('Timer Off');
        }
        if (percent !== 0) {
            $('.progress-bar').css('width', percent + '%').attr('aria-valuenow', percent).html('Run, Forrest! RUN!');
            if (percent >= 100) {
                window.location.href = "/page_flash";
            }
        }

    });
}
;

function setDarkMode() {
    let req;

    req = $.ajax({
        type: 'POST',
        url: "/cookie_set_dark",
        cache: false
    });

}
;

function delDarkMode() {
    let req;

    req = $.ajax({
        type: 'POST',
        url: "/cookie_del_dark",
        cache: false
    });

}
;

function darkModeGet() {
    let req;

    req = $.ajax({
        type: 'GET',
        url: "/cookie_get_dark",
        cache: false
    });

    req.done(function (data) {
        let dark = '';

        dark = data.darkmode;
        if (dark === 'darkmode') {
            setColor('cookie_request_on_load_is_dark');
        }


    });

}
;

function stationGet() {
        /*
    the active radio name listened;
    rebuild console after page refresh
    */
    let req;
    req = $.ajax({
        type: 'GET',
        url: "/station_get",
        cache: false,
    });
    req.done(function (data) {
        if (data.stationGet) {
            let stationDict = data.stationGet
            let keyList = Object.keys(stationDict);

            if(keyList.length > 0){
                let stationName = keyList[0];
                let stationId = stationDict[stationName]
                currentRadioName.innerText = stationName; /*stationName.substring(0, 20)*/
                currentRadioName.setAttribute("id", "currentRadioName");
                currentRadioName.style.cursor = "pointer";
                currentRadioName.style.cursor = "hand";
                $("#currentRadioName").on('click', function () {
                    document.getElementById('dot_' + stationId).scrollIntoView({ behavior: "smooth" });
                });
                currentRadio = stationName;
            }
        }
    });
}
;

function streamerGet() {
        /*
    redraw dropdown dialog for streamer in console after page refresh
    "keeps track of your records"
    */
    let req;
    req = $.ajax({
        type: 'GET',
        url: "/streamer_get",
        cache: false,
    });
    req.done(function (data) {
        if (data.streamerGet) {
            $('#cacheList').find('option:not(:first)').remove();
            let streamerDict = data.streamerGet
            for(name in streamerDict){
                let table_id = streamerDict[name];
                cacheListFeed(table_id, name);
            }
        }
    });
}
;

function cookie_set_show_visuals() {
    let req;

    req = $.ajax({
        type: 'POST',
        url: "/cookie_set_show_visuals",
        cache: false
    });
}
;

function cookie_del_show_visuals() {
    let req;
    req = $.ajax({
        type: 'POST',
        url: "/cookie_del_show_visuals",
        cache: false
    });
}
;

function cookie_toggle_show_visuals() {
    let req;

    req = $.ajax({
        type: 'GET',
        url: "/cookie_get_show_visuals",
        cache: false
    });

    req.done(function (data) {
        let analyserBadge = document.getElementById('analyserBadge');
        let canvasMaster = document.getElementById('canvasMaster');
        let DivCanvasMaster = document.getElementById('DivCanvasMaster');
        let show_visuals = data.str_visuals;
        if (show_visuals !== 'show_visuals') {
            analyserBadge.textContent = "hide";
            canvasMaster.style.display = "inline-block";
            DivCanvasMaster.style.display = "inline-block";
            cookie_set_show_visuals();
            spectrumAnalyserShow = true;
            overrideSpectrumAnalyser()
        }
        if (show_visuals === 'show_visuals') {
            analyserBadge.textContent = "show";
            canvasMaster.style.display = "none";
            DivCanvasMaster.style.display = "none";
            cookie_del_show_visuals();

        }


    });

}
;
function cookie_start_set_text_show_visuals() {
    let req;

    req = $.ajax({
        type: 'GET',
        url: "/cookie_get_show_visuals",
        cache: false
    });

    req.done(function (data) {
        let analyserBadge = document.getElementById('analyserBadge');
        let DivCanvasMaster = document.getElementById('DivCanvasMaster');
        let canvasMaster = document.getElementById('canvasMaster');
        let show_visuals = data.str_visuals;
        if (show_visuals === 'show_visuals') {
            analyserBadge.textContent = "hide";
            canvasMaster.style.display = "inline-block";
            DivCanvasMaster.style.display = "inline-block";
            spectrumAnalyserShow = true;
            overrideSpectrumAnalyser()
        }
        if (show_visuals !== 'show_visuals') {
            analyserBadge.textContent = "show";
            canvasMaster.style.display = "none";
            DivCanvasMaster.style.display = "none";
            spectrumAnalyserShow = false;
        }
    });
}
;

function setTimer(val) {

    $.ajax({
        type: 'POST',
        url: "/index_posts_combo",
        cache: false,
        data: { 'timeRecordSelectAll': val }

    });
}
;

function setColor(val) {
    let req;
    var color;
    if (val === 'cookie_request_on_load_is_dark') {
        color = 'black'
    }
    if (val === 'view') {
        color = 'white'
    }

    req = $.ajax({
        type: 'GET',
        url: "/cookie_get_dark",
        cache: false
    });
    req.done(function (data) {
        let dark = '';

        dark = data.darkmode;
        if (dark !== 'darkmode') {
            color = 'black';
        }

        var bodyStyles = document.body.style;
        if (color === 'black') {
            bodyStyles.setProperty('--background-color', 'rgba(26,26,26,1)');
            bodyStyles.setProperty('--form-background', '#333333');
            bodyStyles.setProperty('--form-text', '#f1f1f1');
            bodyStyles.setProperty('--hr-color', '#777777');
            bodyStyles.setProperty('--border-color', '#202020');
            bodyStyles.setProperty('--text-color', '#bbbbbb');
            bodyStyles.setProperty('--form-edit', '#333333');
            bodyStyles.setProperty('--opacity', '0.5');
            bodyStyles.setProperty('--btn-opacity', '0.75');
            bodyStyles.setProperty('--footer-color', 'rgba(26,26,26,0.90)');
            bodyStyles.setProperty('--main-display-arrow', '#34A0DB');
            bodyStyles.setProperty('--dot-for-radio-headline', '#E74C3C');
            bodyStyles.setProperty('--lbl-div-audio', '#db6f34');
            bodyStyles.setProperty('--ghetto-measurements-bottom-color', '#FCA841');
            bodyStyles.setProperty('--radio-station-headline', '#4195fc');
            bodyStyles.setProperty('--controls-background', 'rgba(26,26,26,1)');
            bodyStyles.setProperty('--canvasMaster', 'rgba(26,26,26,0.85)');

            setDarkMode();
        }
        if (color === 'white') {
            bodyStyles.setProperty('--background-color', '#ccc');
            bodyStyles.setProperty('--form-background', '#ddd');
            bodyStyles.setProperty('--form-text', '#565454');
            bodyStyles.setProperty('--hr-color', '#eee');
            bodyStyles.setProperty('--border-color', '#eee');
            bodyStyles.setProperty('--text-color', '#f0f0f0');
            bodyStyles.setProperty('--form-edit', '#777777');
            bodyStyles.setProperty('--opacity', '1');
            bodyStyles.setProperty('--btn-opacity', '1');
            bodyStyles.setProperty('--footer-color', 'rgba(0,63,92,0.90)');
            bodyStyles.setProperty('--main-display-arrow', '#bc5090');
            bodyStyles.setProperty('--dot-for-radio-headline', '#565454');
            bodyStyles.setProperty('--lbl-div-audio', '#FCA841');
            bodyStyles.setProperty('--ghetto-measurements-bottom-color', '#d441fc');
            bodyStyles.setProperty('--radio-station-headline', '#565454');
            bodyStyles.setProperty('--controls-background', '#565454');
            bodyStyles.setProperty('--canvasMaster', '#ccc');    // rgba(240, 240, 240, 0.85)

            delDarkMode();
        }
    });
}
;

function headerInfo() {

    let req = $.ajax({
        type: 'GET',
        url: "/header_info",
        cache: false
    });

    req.done(function (data) {
        if (data.header_result !== "-empty-") {
            $.each(data.header_result, function (idx, val) {

                let response_time = val[0];
                let suffix = val[1];
                let genre = val[2];
                currentRadioGenre = genre;
                let station_name = val[3];
                let station_id = val[4];
                let bit_rate = val[5];
                let icy_url = val[6];

                document.getElementById('request_time_' + station_id).innerText = "" + response_time + " ms";
                document.getElementById('request_suffix_' + station_id).innerText = "" + suffix;
                document.getElementById('request_icy_br_' + station_id).innerText = "" + bit_rate + " kB/s";
                document.getElementById('icy_name_' + station_id).innerText = "" + station_name;
                document.getElementById('request_icy_genre_' + station_id).innerText = "" + genre;
                document.getElementById('request_icy_url_' + station_id).innerText = "" + icy_url;
                document.getElementById('request_icy_url_' + station_id).value = "" + icy_url;
            });
        }   /*data.cache_result !== ""*/
    });
}
;

function deleteInfo() {

    let req = $.ajax({
        type: 'GET',
        url: "/delete_info",
        cache: false
    });

    req.done(function (data) {

        if (data.stopped_result !== "-empty-") {
            let stopped_list = data.stopped_result;

            $.each(stopped_list, function (idx, val) {

                let station_id = val;
                document.getElementById('Display_' + station_id).value = "";
                document.getElementById('request_time_' + station_id).innerText = "";
                document.getElementById('request_suffix_' + station_id).innerText = "";
                document.getElementById('request_icy_br_' + station_id).innerText = "";
                document.getElementById('request_icy_url_' + station_id).innerText = "";
                document.getElementById('icy_name_' + station_id).innerText = "";
                document.getElementById('request_icy_genre_' + station_id).innerText = "";
                document.getElementById("canvas_" + station_id).style.display = "none";
            });/**/
        }
    });
}
;

function cacheListFeed(table_id, title) {

    if (title !== 'Null') {

        let cacheList = document.getElementById('cacheList');
        cacheList.style.color = "#db6f34";
        cacheList.style.textColor = "#db6f34";

        let opt = document.createElement('option');
        opt.id = 'opt_' + table_id;
        opt.value = '#dot_' + table_id;
        opt.innerHTML = title;
        cacheList.appendChild(opt);
    }
}
;

function toggleShowSelectBox() {
    if (document.getElementById('cacheList').style.color !== "rgb(219, 111, 52)") {
        document.getElementById("cacheList").style.display = "none";
    }
    if (document.getElementById('cacheList').style.color === "rgb(219, 111, 52)") {
        document.getElementById("cacheList").style.display = "block";
    }
}
;

// Convert base64 string to ArrayBuffer
function _base64ToArrayBuffer(base64) {
    var binary_string = window.atob(base64);
    var len = binary_string.length;
    var bytes = new Uint8Array(len);
    for (var i = 0; i < len; i++) {
        bytes[i] = binary_string.charCodeAt(i);
    }
    return bytes.buffer;
}
;

update_file_list = function () {
    var input = document.getElementById('fileUpload');
    var output = document.getElementById('file_list');
    var children = "";
    for (let i = 0; i < input.files.length; ++i) {
        children.id = "playlist_num_" + i;
        children += '<li>' + input.files.item(i).name + '</li>';
    }
    output.innerHTML = '<ul>' + children + '</ul>';
}
;

/**
 * Shuffles array in place. ES6 version
 * @param {Array} a items An array containing the items.
 * https://stackoverflow.com/questions/6274339/how-can-i-shuffle-an-array
 */
function shuffle_array(array) {
    for (let i = array.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [array[i], array[j]] = [array[j], array[i]];
    }
    return array;
}
;

function getBodyColor() {
    let bodyStyle = window.getComputedStyle(document.body, null);
    let backgroundColor = bodyStyle.backgroundColor;
    let darkBody;
    if (backgroundColor === 'rgb(26, 26, 26)') {
        darkBody = true;
    } else { darkBody = false; }
    return darkBody;
}
;

function getRandomIntInclusive(min, max) {
    min = Math.ceil(min);
    max = Math.floor(max);
    return Math.floor(Math.random() * (max - min + 1)) + min;
}
;

function playLocalAudio() {

        stopVisualise();

        const playlist_title = document.getElementById("playlist_title");
        const playlist_section = document.getElementById("playlist_section");
        playlist_title.style.display = "block";
        playlist_section.style.display = "block";

        currentRadioName.innerText = "local playlist"; /*currentRadioName.substring(0, 20)*/
        currentRadioName.style.cursor = "pointer";
        currentRadioName.style.cursor = "hand";
        $("#currentRadioName").on('click', function () {
            document.getElementById('file_list').scrollIntoView({ behavior: "smooth" });
        });

        // console.log(this.files);
        const files = this.files;

        const clone_files = [...files];
        const audio = document.getElementById("audioWithControls");
        const checkbox_shuffle = document.getElementById('checkbox_shuffle');
        var fileList = [];
        for (let i = 0; i < fileUpload.files.length; i++) {
            fileList.push(fileUpload.files[i]);
        }
        var play_list;
        play_list = fileList // for non shuffled
        if (checkbox_shuffle.checked) {
            // play_list = shuffle_array(fileList);    // destroys fileList org.
            play_list = shuffle_array(clone_files);
        }
        audio.src = URL.createObjectURL(play_list[0]);
        playlist_title.value = play_list[0].name;

        let isPlayList = false;
        reloadAudioElement(audio.src, isPlayList);

        let track = 1;
        // recalls function if audio ends
        audio.onended = function () {
            if (track < play_list.length) {

                audio.src = URL.createObjectURL(play_list[track]);
                // show title in input type="text"
                playlist_title.value = play_list[track].name;
                stopVisualise();
                let isPlayList = true;
                reloadAudioElement(audio.src, isPlayList);

                track++;
            }
        }

}
;

function recOrListenAction() {

    if ($(this).attr("class") === "navbar-toggle collapsed") {

        return;
    }
    ;

    let clicked = $(this).attr("name");
    let class_val = $(this).attr("class");
    let id = $(this).attr("id");

    if (class_val === "btn btn-primary") {
        $('#' + id).removeClass("btn btn-primary");
        $('#' + id).addClass("btn btn-danger");
    }
    ;
    if (class_val === "btn btn-danger") {
        $('#' + id).removeClass("btn btn-danger");
        $('#' + id).addClass("btn btn-primary");
    }
    ;

    let dict = {
        'name': clicked,
        'button_id': id

    };
    req = $.ajax({
        type: 'POST',
        dataType: "json",
        url: "/",
        data: dict
    });


    req.done(function (data) {
        if (data.streamer) {

            $('#cacheList').find('option:not(:first)').remove();
            let streamer = data.streamer.split(",");

            $.each(streamer, function (idx, val) {

                let stream = val;
                if (stream.length !== 0) {
                    stream = val.split("=");
                    let table_id = stream[1];
                    let title = stream[0];
                    cacheListFeed(table_id, title);

                    if (data.streamer === 'empty_json') {
                        $('#cacheList').find('option:not(:first)').remove();
                        document.getElementById('cacheList').style.color = "#696969";
                        document.getElementById('cacheList').style.textColor = "#696969";
                    }
                    console.log('data.streamer ' + data.streamer);

                }

            });    /*each*/

        }
        ;

        if (data.radio_table_id) {

        }
        ;

        /* current play station */

        if (data.table_ident) {

            let radioName = data.table_ident;
            console.log('table_ident ' + radioName);

            if (radioName !== 'Null') {

                currentRadioName.innerText = radioName; /*currentRadioName.substring(0, 20)*/
                currentRadioName.style.cursor = "pointer";
                currentRadioName.style.cursor = "hand";
                $("#currentRadioName").on('click', function () {
                    document.getElementById('dot_' + id).scrollIntoView({ behavior: "smooth" });
                });

            }
            if (data.former_button_to_switch) {
                let num = data.former_button_to_switch;
                console.log('auto_click former_button_to_switch: ' + num);
                $("#" + num).click();
            } else {
                console.log('... No button to switch');
            }

            ;
        }
        ;

        if (data.result === 'deactivate_audio') {
            console.log('deactivate_audio');
            audio.src = "";
            audio.currentTime = 0;
            audio.srcObject = null;
            currentRadioName.innerText = '';
        }
        ;

        if (data.result === 'activate_audio') {
            stopVisualise();
            let localHostSoundRoute  = data.sound_endpoint
            let radioName = data.table_ident
            let newSource = localHostSoundRoute + radioName;
            let isPlayList = false;
            reloadAudioElement(newSource, isPlayList);
        }
        ;

    });

}
;
