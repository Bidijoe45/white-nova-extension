
class Switch {
    constructor(a_icon, a, b_icon, b) {
        this.a_ = a;
        this.a_icon_ = a_icon;
        this.b_ = b;
        this.b_icon_ = b_icon;
        this.addIconsEvents();
    }

    addIconsEvents() {
        this.a_icon_.addEventListener("click", () => {this.switch()});
        this.b_icon_.addEventListener("click", () => {this.switch()});
    }

    switch() {
        this.swap_display(this.a_, this.b_);
        this.swap_display(this.a_icon_, this.b_icon_);
    }
    
    swap_display(a, b) {
        let c = a.style.display;
        a.style.display = b.style.display;
        b.style.display = c;
    }

}

class ProgressBar {
    constructor() {

    }


}

class Application {

    constructor() {
        this.init();
    }

    async init() {
        const HTML_file = await fetch(chrome.runtime.getURL("layout.html"));
        const HTML_text = await HTML_file.text();
        const goals_container = document.getElementById("goals_container");

        goals_container.innerHTML = goals_container.innerHTML + HTML_text;
        goals_container.style.position = "relative";

        this.switch_blackhole = document.getElementById("switch-blackhole");
        this.blackhole_body = document.getElementById("blackhole-date");

        this.switch_nova = document.getElementById("switch-nova");
        this.nova_body = document.getElementById("nova-body");

        this.switch_blackhole.style.display = "none";
        this.blackhole_body.style.display = "none";

        this.switch = new Switch(this.switch_nova, this.nova_body, this.switch_blackhole, this.blackhole_body);
    }

}

app = new Application();

