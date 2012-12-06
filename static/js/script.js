function jQueryEffects() {
	// Rejected Courses & Times
	$("li.rejected.collapsible").toggle(
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
	$("li.optimal.collapsible").toggle(
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
		$("li.rejected.collapsible").toggle(
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
		$("li.optimal.collapsible").toggle(
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

function addThisCourseToSession(classId) {
	Dajaxice.scheduler.addThisCourseToSession(Dajax.process, {'classId': classId});
	return false;
}

function addCourseToSession() {
	data = $('#addCourseForm').serializeObject();
	Dajaxice.scheduler.addCourseToSession(Dajax.process, {'form': data});
	Dajaxice.scheduler.determineNumberTakingField(Dajax.process);
	return false;
}

function addCourseByProfToSession() {
	data = $('#addCourseByProfForm').serializeObject();
	Dajaxice.scheduler.addCourseByProfToSession(Dajax.process, {'form': data});
	Dajaxice.scheduler.determineNumberTakingField(Dajax.process);
	return false;
}

function addUnavailableToSession() {
	data = $('#addUnavailableForm').serializeObject();
	Dajaxice.scheduler.addUnavailableToSession(Dajax.process, {'form': data});
	return false;
}

function deleteCourseFromSession(course, number, title) {
	Dajaxice.scheduler.deleteCourseFromSession(Dajax.process, {'course':course, 'number':number, 'title':title});
	Dajaxice.scheduler.determineNumberTakingField(Dajax.process);
	return false;
}

function deleteCourseByProfFromSession(course, prof, number, title, firstName, lastName) {
	Dajaxice.scheduler.deleteCourseByProfFromSession(Dajax.process, {'course':course, 'prof':prof, 'number':number, 'title':title, 'firstName':firstName, 'lastName':lastName});
	Dajaxice.scheduler.determineNumberTakingField(Dajax.process);
	return false;
}

function deleteCourseByIDFromSession(courseID, subject, number, title, section) {
	Dajaxice.scheduler.deleteCourseByIDFromSession(Dajax.process, {'courseID':courseID, 'subj':subject, 'numb':number, 'titl':title, 'sect':section});
	Dajaxice.scheduler.determineNumberTakingField(Dajax.process);
	return false;
}

function flushSessionData() {
	Dajaxice.scheduler.flushSessionData(Dajax.process);
	return false;
}
