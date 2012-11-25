$(document).ready(
	function() {
		// Rejected Courses
		$("a.rejectedCourse").toggle(
			function() {$(this).parents("li").next().show('fast');},
			function() {$(this).parents("li").next().hide('slow');}
	 	);
		$("a.rejectedTime").toggle(
			function() {$(this).parents("li").next().hide('slow');},
			function() {$(this).parents("li").next().show('fast');}
	 	);
	 	
	 	// Optimal Courses
		$("a.optimalCourse").toggle(
			function() {$(this).parents("li").next().hide('slow');},
			function() {$(this).parents("li").next().show('fast');}
	 	);
		$("a.optimalTime").toggle(
			function() {$(this).parents("li").next().hide('slow');},
			function() {$(this).parents("li").next().show('fast');}
	 	);
	}
);
