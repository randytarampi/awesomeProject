function jQueryEffects() {
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

$(document).ready(
	function () {
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

function generateSchedule() {
	$('#scheduleViewDiv').html('');
	$('#scheduleViewDiv').removeClass('fullSchedule');
	$('#scheduleViewDiv').addClass('emptySchedule');
	$('#scheduleViewDiv').activity();
	data = $('#scheduleForm').serializeObject();
	Dajaxice.scheduler.generateSchedule(Dajax.process, {'form': data});
	return false;
}

function addCourseToSession() {
	data = $('#addCourseForm').serializeObject();
	Dajaxice.scheduler.addCourseToSession(Dajax.process, {'form': data});
	return false;
}

function addCourseByProfToSession() {
	data = $('#addCourseByProfForm').serializeObject();
	Dajaxice.scheduler.addCourseByProfToSession(Dajax.process, {'form': data});
	return false;
}

function addUnavailableToSession() {
	data = $('#addUnavailableForm').serializeObject();
	Dajaxice.scheduler.addUnavailableToSession(Dajax.process, {'form': data});
	return false;
}
