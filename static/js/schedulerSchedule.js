$(document).ready(
	function() {
		// Rejected Courses
		$("li.rejectedCourse").toggle(
			function() {
				$(this).next().show('fast');
				$(this).addClass('toggleExpand');
				$(this).removeClass('toggleCollapse');
			},
			function() {
				$(this).next().hide('slow');
				$(this).addClass('toggleCollapse');
				$(this).removeClass('toggleExpand');
			}
	 	);
		$("li.rejectedTime").toggle(
			function() {
				$(this).next().hide('slow');
				$(this).addClass('toggleExpand');
				$(this).removeClass('toggleCollapse');
			},
			function() {
				$(this).next().show('fast');
				$(this).addClass('toggleCollapse');
				$(this).removeClass('toggleExpand');
			}
	 	);
	 	
	 	// Optimal Courses
		$("li.optimalCourse").toggle(
			function() {
				$(this).next().hide('slow');
				$(this).addClass('toggleExpand');
				$(this).removeClass('toggleCollapse');
			},
			function() {
				$(this).next().show('fast');
				$(this).addClass('toggleCollapse');
				$(this).removeClass('toggleExpand');
			}
	 	);
		$("li.optimalTime").toggle(
			function() {
				$(this).next().hide('slow');
				$(this).addClass('toggleExpand');
				$(this).removeClass('toggleCollapse');
			},
			function() {
				$(this).next().show('fast');
				$(this).addClass('toggleExpand');
				$(this).removeClass('toggleCollapse');
			}
	 	);	 	
	 	
	 	// Weekly Schedule
		$("li.scheduleViewWeek").toggle(
			function() {
				$(this).next().hide('slow');
				$(this).addClass('toggleExpand');
				$(this).removeClass('toggleCollapse');
			},
			function() {
				$(this).next().show('fast');
				$(this).addClass('toggleCollapse');
				$(this).removeClass('toggleExpand');
			}
	 	);
	 	
	 	// Exam Schedule
		$("li.scheduleViewExams").toggle(
			function() {
				$(this).next().hide('slow');
				$(this).addClass('toggleExpand');
				$(this).removeClass('toggleCollapse');
			},
			function() {
				$(this).next().show('fast');
				$(this).addClass('toggleExpand');
				$(this).removeClass('toggleCollapse');
			}
	 	);
	}
);
