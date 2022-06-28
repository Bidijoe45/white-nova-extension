
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
    constructor(container, progress, text) {
        this.container_ = container;
        this.progress_bar_ = this.container_.querySelector("#progress-bar-nova");
        this.progress_bar_text_ = this.container_.querySelector("#progress-bar-text");
        this.progress = progress;
        this.text = text;
    }

    get progress() {
        return this.progress_;
    }

    set progress(value) {
        if (value >= 100) {
            this.progress_ = 100;
            this.progress_bar_.style.borderRadius = "5px";
        }

        this.progress_bar_.style.width = this.progress_ + "%";
    }

    get text() {
        return this.text_;
    }

    set text(value) {
        this.text_ = value;
        this.progress_bar_text_.innerHTML = this.text_;
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

        //switch button

        this.switch_blackhole = document.getElementById("switch-blackhole");
        this.blackhole_body = document.getElementById("blackhole-date");

        this.switch_nova = document.getElementById("switch-nova");
        this.nova_body = document.getElementById("nova-body");

        this.switch_blackhole.style.display = "none";
        this.blackhole_body.style.display = "none";

        this.switch = new Switch(this.switch_nova, this.nova_body, this.switch_blackhole, this.blackhole_body);
        
        //progress bar
        const progress_bar_container = document.getElementById("progress-bar-container");
        this.progres_bar = new ProgressBar(progress_bar_container, 50, "White Nova");

    }

}

app = new Application();

