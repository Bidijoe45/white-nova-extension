Feature: White nova module
	Scenario: User can change the selected tab
		Given User is in the "mainIntra" page
		When User clicks on a "novaObjective" tab
		And User clicks on a different "novaObjective" tab
		And User clicks back on the first "novaObjective" tab
		Then The first "novaObjective" tab "content" is displayed 

	Scenario: For "Piscine" users "WhiteNovaCompleted_ProgressBar" element has a black background
		Given User has a "Piscine" account
		And User is in the "PiscineCursus" page
		And User has completed the metrics for "hours"
		When User clicks on "CursusSelection" selector
		And User clicks on "42Cursus" button
		Then "WhiteNovaCompleted_ProgressBar" element has a "black" background
