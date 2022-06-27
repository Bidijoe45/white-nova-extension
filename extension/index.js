function swap_display(a, b) {

	let c = a.style.display;
	a.style.display = b.style.display;
	b.style.display = c;

}


class Switch {
	
	constructor(a, a_icon, b, b_icon) {

		a_icon.addEventListener("click", this.flip, a, a_icon, b, b_icon);
		b_icon.addEventListener("click", this.flip, a, a_icon, b, b_icon);

	}
	

	flip(e, a, a_icon, b, b_icon) {
		
		console.log("IN : ", a);
		swap_display(a, b);
		swap_display(a_icon,b_icon);
	}

}

class ProgressBar {

	constructor(element) {

		this.element_ = element;
		this.text_ = "";
		this.progress_ = 0;
	}

	set_text(text) {

		this.text_ = text;
		this.element_.querySelector("#progress-bar-text").innerHTML = this.text_;
	}

	set_progress(progress) {

		this.progress_ = progress;
		this.element_.querySelector("#progress-bar-nova").style.width = this.progress_ + "%";
	}
}

class Application {
	constructor() {
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


		//instance all objects
		this.switch_button = new Switch(this.blackhole_body, this.switch_blackhole, this.nova_body, this.switch_nova);
		this.progress_bar = new ProgressBar(document.getElementById("progress-bar-container"));

	//	this.run();
	}

	run() {

	}
}

const app = new Application();
