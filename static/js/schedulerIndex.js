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