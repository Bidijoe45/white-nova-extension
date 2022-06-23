
async function main() {
    let blackhole_container = document.getElementById("goals_container");

    blackhole_container.innerHTML = " ";

    let title_element = document.createElement("p"); 
    title_element.style.fontSize = "24px";
    title_element.innerHTML = "White Nova 💫";

    let subtitle_element = document.createElement("div"); 
    subtitle_element.style.fontSize = "12px";

    blackhole_container.append(title_element);
    blackhole_container.append(subtitle_element);


    let user_login = document.getElementsByClassName("login")[0].dataset.login;

    let response = await fetch("http://127.0.0.1:5000?login=" + user_login, {
        method: "GET",
    }); 

    let payload = await response.json();

    subtitle_element.innerHTML = payload.start + " - " + payload.end;
    
    let hours = payload.hours;
    let minutes = payload.minutes;
    
    let percent = payload.raw_hours * 100 / 12;
    let real_percent = Math.floor(percent); 
    
    if (percent >= 100)
        percent = 100;

    let hours_element = document.createElement("div");
    hours_element.innerHTML = hours + " hrs " + minutes + " mins - " + real_percent + "%";
    hours_element.style.position = "absolute";
    hours_element.style.width = "100%";
    hours_element.style.height = "100%";
    hours_element.style.textAlign = "center";
    hours_element.style.lineHeight = 2;
    
    let coalition_color = document.getElementsByClassName("progress-bar")[0].style.backgroundColor;

    let progress_bar_container = document.createElement('div');
    progress_bar_container.style.width = "80%";
    progress_bar_container.style.height = "35px";
    progress_bar_container.style.backgroundColor = "black";
    progress_bar_container.style.borderRadius = "5px";
    progress_bar_container.style.position = "relative";

    let progress_bar = document.createElement('div');
    progress_bar.style.width = percent + "%";
    progress_bar.style.height = "35px";
    progress_bar.style.backgroundColor = coalition_color;
    progress_bar.style.borderRadius = "5px 0 0 5px";
    if (percent == 100) 
        progress_bar.style.borderRadius = "5px";
 

    blackhole_container.append(progress_bar_container);
    progress_bar_container.append(hours_element);
    progress_bar_container.append(progress_bar);
}

main();


//<div class="profile-infos-item" data-placement="left" data-toggle="tooltip" title="" data-original-title="Primary campus">
//</div>


