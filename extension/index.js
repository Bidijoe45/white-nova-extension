
function get_user_login() {
    return document.getElementsByClassName("login")[0].dataset.login;
}

function remove_element_content(element) {
    element.innerHTML = " ";
}

function create_title_element(days) {
    let title_element = document.createElement("div"); 
    title_element.style.fontSize = "31px";
    title_element.style.textAlign = "center";
    title_element.style.marginBottom = "11px"
    title_element.innerHTML = days + " days until next cycle";

    return title_element;
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
    progress_bar_container.style.width = "100%";
    progress_bar_container.style.height = "35px";
    progress_bar_container.style.backgroundColor = "black";
    progress_bar_container.style.borderRadius = "5px";
    progress_bar_container.style.position = "relative";
    progress_bar_container.style.display = "none";

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

function get_coalition_color() {
    return document.getElementsByClassName("progress-bar")[0].style.backgroundColor;
}

function create_clock_icon() {
    let clock_icon = document.createElement('div');
    clock_icon.style.cursor = "pointer";
    
    clock_icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" style="height: 20px;" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"> <path stroke-linecap="round" stroke-linejoin="round" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /> </svg>';

    return clock_icon;
}

function create_evaluations_icon() {
    let evaluations_icon = document.createElement('div'); 
    evaluations_icon.style.cursor = "pointer";

    evaluations_icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" style="height: 20px;" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z" /></svg>';

    return evaluations_icon;
}

function create_events_icon() {
    let events_icon = document.createElement('div');
    events_icon.style.cursor = "pointer";
    
    events_icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" style="height: 20px;" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>';

    return events_icon;
}

function create_icons_container() {
    let icons_container = document.createElement('div');
    icons_container.style.display = "flex";
    icons_container.style.justifyContent = "space-between";
    icons_container.style.width = "50%";
    icons_container.style.margin = "0 auto 11px auto";
    

    return icons_container;
}

function create_blackhole_switch_icon() {
    let switch_icon = document.createElement('div');
    switch_icon.style.position = "absolute";
    switch_icon.style.top = "10px";
    switch_icon.style.left = "10px";
    switch_icon.style.cursor = "pointer";

    //switch_icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" style="height: 20px;" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z" clip-rule="evenodd" /></svg>';
    switch_icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" style="height: 20px" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2"><path stroke-linecap="round" stroke-linejoin="round" d="M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z" /></svg>';
    return switch_icon;
}

function create_white_nova_switch_icon() {
    let switch_icon = document.createElement('div');
    switch_icon.style.position = "absolute";
    switch_icon.style.top = "10px";
    switch_icon.style.left = "10px";
    switch_icon.style.cursor = "pointer";

    switch_icon.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" style="height: 20px;" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M5 2a1 1 0 011 1v1h1a1 1 0 010 2H6v1a1 1 0 01-2 0V6H3a1 1 0 010-2h1V3a1 1 0 011-1zm0 10a1 1 0 011 1v1h1a1 1 0 110 2H6v1a1 1 0 11-2 0v-1H3a1 1 0 110-2h1v-1a1 1 0 011-1zM12 2a1 1 0 01.967.744L14.146 7.2 17.5 9.134a1 1 0 010 1.732l-3.354 1.935-1.18 4.455a1 1 0 01-1.933 0L9.854 12.8 6.5 10.866a1 1 0 010-1.732l3.354-1.935 1.18-4.455A1 1 0 0112 2z" clip-rule="evenodd" /></svg>';
    return switch_icon;
}

function create_evaluations_element(evaluations, total) {
    let element = document.createElement('div');

    element.innerHTML = evaluations + "/"+ total + " evaluations"; 
    element.style.position = "absolute";
    element.style.width = "100%";
    element.style.height = "100%";
    element.style.textAlign = "center";
    element.style.lineHeight = 2;
    return element;
}

let layer = 0;

function create_events_element(events, total) {
    let element = document.createElement('div');

    element.innerHTML = events + "/"+ total + " events"; 
    element.style.position = "absolute";
    element.style.width = "100%";
    element.style.height = "100%";
    element.style.textAlign = "center";
    element.style.lineHeight = 2;
    return element;
}

async function main() {

    let blackhole_container = document.getElementById("goals_container");
    blackhole_container.style.position = "relative";

    let blackhole_date = document.getElementById("blackhole-date");
    blackhole_date.style.display = "none";

    let loading_text = document.createElement("div");
    loading_text.innerHTML = "loading white nova...";
    
    blackhole_container.append(loading_text);

    let user_login = get_user_login(); 

    let response = await fetch("https://intranet-white-nova-kesbd7iw5q-ew.a.run.app?login=" + user_login, {
        method: "GET",
    }); 

    let payload = await response.json();
    if (payload.ok == 0)
        return;

    let percent = payload.raw_hours * 100 / 12;
    let evaluations_icon = create_evaluations_icon();
    let events_icon = create_events_icon();
    let clock_icon = create_clock_icon();

    clock_icon.style.margin = "0 4px";
    events_icon.style.margin = "0 4px";
    evaluations_icon.style.margin = "0 4px";

    clock_icon.style.opacity = "0.4";
    events_icon.style.opacity = "0.4";
    evaluations_icon.style.opacity = "0.4";

    loading_text.style.display = "none";

    title_element = create_title_element(payload.next_cycle);

    icons_container = create_icons_container();
    

    icons_container.append(clock_icon);
    icons_container.append(evaluations_icon);
    icons_container.append(events_icon);

    let switch_icon = document.createElement('div');

    let blackhole_switch_icon = create_blackhole_switch_icon();
    let white_nova_switch_icon = create_white_nova_switch_icon();

    blackhole_switch_icon.style.display = "none";

    switch_icon.append(blackhole_switch_icon);
    switch_icon.append(white_nova_switch_icon);
    
    let white_nova_container = document.createElement("div");
    white_nova_container.style.width = "80%";
    
    blackhole_container.append(switch_icon);
    white_nova_container.append(title_element);
    white_nova_container.append(icons_container);

    blackhole_container.append(white_nova_container);
    
    let real_percent = Math.floor(percent); 
    
    if (percent >= 100)
        percent = 100;

    let hours_element = create_hours_element(payload.hours, payload.minutes, real_percent);
    let evaluations_element = create_evaluations_element(payload.evaluations, 2);
    let events_element = create_events_element(payload.events, 2);
    let coalition_color = get_coalition_color();
    
    let white_nova_progress_bar_container = create_progress_bar_container_element();
    white_nova_progress_bar_container.style.display = "block";
    white_nova_progress_bar_container.style.textAlign = "center";
    white_nova_progress_bar_container.innerHTML = "White Nova";

    let hours_progress_bar_container = create_progress_bar_container_element();

    let evaluations_progress_bar_container = create_progress_bar_container_element();

    let events_progress_bar_container = create_progress_bar_container_element();

    let active_bar = 0;

    let hours_progress_bar = create_progress_bar_element(percent, coalition_color); 
    hours_progress_bar_container.append(hours_element);
    hours_progress_bar_container.append(hours_progress_bar);

    let evaluation_percent = payload.evaluations / 2 * 100;
    if (evaluation_percent > 100)
        evaluation_percent = 100;
    let evaluations_progress_bar = create_progress_bar_element(evaluation_percent, coalition_color); 
    evaluations_progress_bar_container.append(evaluations_element);
    evaluations_progress_bar_container.append(evaluations_progress_bar);


    let events_percent = payload.events / 2 * 100;
    if (events_percent > 100)
        events_percent = 100;
    let events_progress_bar = create_progress_bar_element(events_percent, coalition_color); 
    events_progress_bar_container.append(events_element);
    events_progress_bar_container.append(events_progress_bar);
    
    if (events_percent == 100) 
        events_progress_bar.style.borderRadius = "5px";

    if (percent == 100) 
        hours_progress_bar.style.borderRadius = "5px";

    if (evaluation_percent == 100) 
        events_progress_bar.style.borderRadius = "5px";

    if (events_percent == 100 || percent == 100 || evaluation_percent == 100) {
        white_nova_progress_bar_container.style.backgroundColor = coalition_color;
        white_nova_progress_bar_container.innerHTML = "White Nova ";
    }

    white_nova_container.append(white_nova_progress_bar_container);
    white_nova_container.append(hours_progress_bar_container);
    white_nova_container.append(evaluations_progress_bar_container);
    white_nova_container.append(events_progress_bar_container);

    if (percent == 100)
        clock_icon.style.opacity = "1";

    if (events_percent == 100)
        events_icon.style.opacity = "1";

    if (evaluation_percent == 100)
        evaluations_icon.style.opacity = "1";
    


    function disable_highlight() {
        clock_icon.style.margin = "0 4px";
        if (percent < 100)
            clock_icon.style.opacity = "0.4";

        if (evaluation_percent < 100)
            evaluations_icon.style.opacity = "0.4";

        if (events_percent < 100) 
            events_icon.style.opacity = "0.4";
        
        events_icon.style.color = "white";
        evaluations_icon.style.color = "white";
        clock_icon.style.color = "white";
    }

    clock_button = 0;
    evaluations_button = 0;
    events_button = 0;

    function nisu() {
        disable_highlight();
        hours_progress_bar_container.style.display = "none";
        white_nova_progress_bar_container.style.display = "block";
        evaluations_progress_bar_container.style.display = "none";
        events_progress_bar_container.style.display = "none";

        clock_button = 0;
        evaluations_button = 0;
        events_button = 0;
    }

    clock_icon.addEventListener("click", function() {
        disable_highlight();
        clock_icon.style.opacity = "1";
        clock_icon.style.color = coalition_color;
        hours_progress_bar_container.style.display = "block";
        white_nova_progress_bar_container.style.display = "none";
        evaluations_progress_bar_container.style.display = "none";
        events_progress_bar_container.style.display = "none";

        if (clock_button == 1)
            return nisu();

        clock_button = 1;
    });
    
    evaluations_icon.addEventListener("click", function() {
        disable_highlight();
        evaluations_icon.style.opacity = "1";
        evaluations_icon.style.color = coalition_color;
        hours_progress_bar_container.style.display = "none";
        white_nova_progress_bar_container.style.display = "none";
        evaluations_progress_bar_container.style.display = "block";
        events_progress_bar_container.style.display = "none";

        if (evaluations_button == 1)
            return nisu();

        evaluations_button = 1;
    });

    events_icon.addEventListener("click", function() {
        disable_highlight();
        events_icon.style.opacity = "1";
        events_icon.style.color = coalition_color;
        hours_progress_bar_container.style.display = "none";
        white_nova_progress_bar_container.style.display = "none";
        evaluations_progress_bar_container.style.display = "none";
        events_progress_bar_container.style.display = "block";
        
        if (events_button == 1)
            return nisu();

        events_button = 1;
    });

    switch_icon.addEventListener("click", function() {
        if (layer == 0) {
            layer = 1;
            white_nova_container.style.display = "none";
            blackhole_date.style.display = "block";
            white_nova_switch_icon.style.display = "none";
            blackhole_switch_icon.style.display = "block";
        } else {
            layer = 0;
            white_nova_container.style.display = "block";
            blackhole_date.style.display = "none";
            white_nova_switch_icon.style.display = "block";
            blackhole_switch_icon.style.display = "none";
        }
    });
}

main();

