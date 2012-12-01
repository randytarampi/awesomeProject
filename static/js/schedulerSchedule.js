$(document).ready(
	function() {
		// Rejected Courses & Times
		$("li.rejected").toggle(
			function() {
				$(this).next().show('fast');
				$(this).removeClass('toggleExpand');
				$(this).addClass('toggleCollapse');
			},
			function() {
				$(this).next().hide('slow');
				$(this).removeClass('toggleCollapse');
				$(this).addClass('toggleExpand');
			}
	 	);
	 	
	 	// Optimal Courses
		$("li.optimal").toggle(
			function() {
				$(this).next().hide('slow');
				$(this).removeClass('toggleCollapse');
				$(this).addClass('toggleExpand');
			},
			function() {
				$(this).next().show('fast');
				$(this).removeClass('toggleExpand');
				$(this).addClass('toggleCollapse');
			}
	 	);
	}
);
