function generateSchedule() {
	$('#scheduleViewDiv').html('');
	$('#scheduleViewDiv').removeClass('fullSchedule');
	$('#scheduleViewDiv').addClass('emptySchedule');
	$('#scheduleViewDiv').activity();
	data = $('#scheduleForm').serializeObject();
	Dajaxice.scheduler.generateSchedule(Dajax.process, {'form': data});
	return false;
}
