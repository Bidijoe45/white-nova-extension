
function get_user_login() {
    return document.getElementsByClassName("login")[0].dataset.login;
}

function remove_element_content(element) {
    element.innerHTML = " ";
}

function create_title_element() {
    let title_element = document.createElement("p"); 
    title_element.style.fontSize = "24px";
    title_element.innerHTML = "White Nova 💫";

    return title_element;
}

function create_subtitle_element() {
    let subtitle_element = document.createElement("div"); 
    subtitle_element.style.fontSize = "12px";
    subtitle_element.style.marginBottom = "5px";

    return subtitle_element;
}

function create_hours_element(hours, minutes, real_percent) {
    let hours_element = document.createElement("div");
    hours_element.innerHTML = hours + " hrs " + minutes + " mins - " + real_percent + "%";
    hours_element.style.position = "absolute";
    hours_element.style.width = "100%";
    hours_element.style.height = "100%";
    hours_element.style.textAlign = "center";
    hours_element.style.lineHeight = 2;

    return hours_element;
}

function create_progress_bar_container_element() {
    let progress_bar_container = document.createElement('div');
    progress_bar_container.style.width = "80%";
    progress_bar_container.style.height = "35px";
    progress_bar_container.style.backgroundColor = "black";
    progress_bar_container.style.borderRadius = "5px";
    progress_bar_container.style.position = "relative";

    return progress_bar_container;
}

function create_progress_bar_element(percent, coalition_color) {
    let progress_bar = document.createElement('div');
    progress_bar.style.width = percent + "%";
    progress_bar.style.height = "35px";
    progress_bar.style.backgroundColor = coalition_color;
    progress_bar.style.borderRadius = "5px 0 0 5px";

    return progress_bar;
}

async function main() {

    let user_login = get_user_login(); 

    let response = await fetch("https://intranet-white-nova-kesbd7iw5q-ew.a.run.app?login=" + user_login, {
        method: "GET",
    }); 

    let payload = await response.json();

    if (payload.ok == 0)
        return;

    let blackhole_container = document.getElementById("goals_container");
    remove_element_content(blackhole_container);

    title_element = create_title_element();
    subtitle_element = create_subtitle_element();

    blackhole_container.append(title_element);
    blackhole_container.append(subtitle_element);

    subtitle_element.innerHTML = payload.start + " - " + payload.end;
    
    let percent = payload.raw_hours * 100 / 12;
    let real_percent = Math.floor(percent); 
    
    if (percent >= 100)
        percent = 100;

    let hours_element = create_hours_element(payload.hours, payload.minutes, real_percent);
    
    let coalition_color = document.getElementsByClassName("progress-bar")[0].style.backgroundColor;

    let progress_bar_container = create_progress_bar_container_element();

    let progress_bar = create_progress_bar_element(percent, coalition_color); 

    if (percent == 100) 
        progress_bar.style.borderRadius = "5px";

    blackhole_container.append(progress_bar_container);
    progress_bar_container.append(hours_element);
    progress_bar_container.append(progress_bar);
}

main();

