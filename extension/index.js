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
    constructor(container, progress, text, color) {
        this.container_ = container;
        this.progress_bar_ = this.container_.querySelector("#progress-bar-nova");
        this.progress_bar_.style.backgroundColor = color;
        this.progress_bar_text_ = this.container_.querySelector("#progress-bar-text");
        this.progress = progress;
        this.text = text;
    }

    get progress() {
        return this.progress_;
    }

    set progress(value) {
        this.progress_ = value;

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
        this.progress_bar_text_.innerHTML = (this.text_);
    }

}

class Application {

    constructor() {
        this.init();
        this.evaluations = 0;
        this.hours = 0;
        this.minutes = 0;
        this.events = 0;
        this.days_left = 0;
        this.raw_hours = 0;
        this.time_selected = false;
        this.evaluations_selected = false;
        this.events_selected = false;
        this.coalition_color = "";
    }

    async init() {
        const HTML_file = await fetch(chrome.runtime.getURL("layout.html"));
        const HTML_text = await HTML_file.text();
        const goals_container = document.getElementById("goals_container");

        this.getLogin();
        this.getCoalitionColor();
        let validUser = await this.getLoginData();

        if (!validUser)
            return 

        goals_container.innerHTML = (goals_container.innerHTML + HTML_text);
        goals_container.style.position = "relative";

        this.switch_blackhole = document.getElementById("switch-blackhole");
        this.blackhole_body = document.getElementById("blackhole-date");

        this.switch_nova = document.getElementById("switch-nova");
        this.nova_body = document.getElementById("nova-body");

        this.switch_blackhole.style.display = "none";
        this.blackhole_body.style.display = "none";

        this.switch = new Switch(this.switch_nova, this.nova_body, this.switch_blackhole, this.blackhole_body);
        
        const progress_bar_container = document.getElementById("progress-bar-container");
        this.progress_bar = new ProgressBar(progress_bar_container, 50, "White Nova", this.coalition_color);

		const contdown_text = document.getElementById('countdown-text');
		contdown_text.innerHTML = (this.days_left + " days left until next cycle");

        this.addBlackHoleLeftDays();
        this.getPanelButtons();
        this.addButtonsEvents();
        this.setWhiteNovaProgressBar();
        this.setButtonsDefault();
        this.setButtonsCompleted();
    }

    async getLoginData() {

        const url = "https://whitenova.hacku.org/" + this.login;
        const response = await fetch(url, { method: "GET"});
        const data = await response.json()

        if ("error" in data) {
            return 
        }

        this.evaluations = data.evaluations;
        this.events = data.events;
        this.hours = data.hours;
        this.minutes = data.minutes;
        this.days_left = data.next_cycle;
        this.raw_hours = data.raw_hours;

        return true;
    }

    getPanelButtons() {
        this.time_button = document.getElementById("panel-time");
        this.evaluations_button = document.getElementById("panel-evaluations");
        this.events_button = document.getElementById("panel-events");
    }

    getLogin() {
        const login_container = document.getElementsByClassName("login")[0];
        this.login = login_container.dataset.login;
    }

    getCoalitionColor() {
        const progress_bar_element = document.getElementsByClassName("coalition-span")[0];
        this.coalition_color = progress_bar_element.style.color;
    }

    addBlackHoleLeftDays() {
        const bhDate = document.getElementsByClassName("emote-bh");
        let date = null;
        
        for (var i=0; i < bhDate.length; i++)
            if ("originalTitle" in bhDate[i].dataset)
                date = bhDate[i].dataset;

        if (date == null) 
            return

        const parts = date.originalTitle.split("/");
        const dt = new Date(parseInt(parts[2], 10),
                          parseInt(parts[1], 10) - 1,
                          parseInt(parts[0], 10));

        const timestamp = dt.getTime() - new Date().getTime();
        this.blackhole_body.append(Math.ceil(timestamp / 1000 / 60 / 60 / 24) + " days left");
    }

    addButtonsEvents() {

        this.time_button.addEventListener("click", () => {
            if (this.time_selected) {
                this.resetButtons();
                this.setWhiteNovaProgressBar();
                return;
            }

            this.resetButtons();
            this.time_button.style.color = this.coalition_color;
            this.setTimeProgressBar();
            this.time_selected = true;
        });

        this.evaluations_button.addEventListener("click", () => {
            if (this.evaluations_selected) {
                this.resetButtons();
                this.setWhiteNovaProgressBar();
                return;
            }

            this.resetButtons();
            this.evaluations_button.style.color = this.coalition_color;
            this.setEvaluationsProgressBar();
            this.evaluations_selected = true;
        });

        this.events_button.addEventListener("click", () => {
            if (this.events_selected) {
                this.resetButtons();
                this.setWhiteNovaProgressBar();
                return;
            }

            this.resetButtons();
            this.events_button.style.color = this.coalition_color;
            this.setEventsProgressBar();
            this.events_selected = true;
        });
    }

    resetButtons() {
        this.time_button.style.color = "white";
        this.evaluations_button.style.color = "white";
        this.events_button.style.color = "white";

        this.time_selected = false;
        this.evaluations_selected = false;
        this.events_selected = false;
    }

    setWhiteNovaProgressBar() {

        this.progress_bar.progress = 0;
        this.progress_bar.text = "White Nova incomplete"

        if (this.isWhiteNovaCompleted()) {
            this.progress_bar.progress = 100;
            this.progress_bar.text = "White Nova complete"
        }
    }

    setTimeProgressBar() {
        const progress = this.raw_hours / 12 * 100;
        this.progress_bar.progress = progress;
        this.progress_bar.text = this.hours + "h " + this.minutes + "m / 12 hours";
    }

    setEvaluationsProgressBar() {
        const progress = this.evaluations / 2 * 100;
        this.progress_bar.progress = progress;
        this.progress_bar.text = this.evaluations + " / 2 evaluations";
    }

    setEventsProgressBar() {
        const progress = this.events / 2 * 100;
        this.progress_bar.progress = progress;
        this.progress_bar.text = this.events + " / 2 events";
    }

    isWhiteNovaCompleted() {
        if (this.hours >= 12 || this.evaluations >= 2 || this.events >= 2)
            return true;
        return false;
    }

    setButtonsDefault() {
        this.time_button.style.opacity = 0.4;
        this.evaluations_button.style.opacity = 0.4;
        this.events_button.style.opacity = 0.4;
    }

    setButtonsCompleted() {
        if (this.hours >= 12)
            this.time_button.style.opacity = 1;
        if (this.evaluations >= 2)
            this.evaluations_button.style.opacity = 1;
        if (this.events >= 2)
            this.events_button.style.opacity = 1;
    }

}

app = new Application();

