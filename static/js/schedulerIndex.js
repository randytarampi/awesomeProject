function generateSchedule() {
	data = $('#scheduleForm').serializeObject();
	Dajaxice.scheduler.generateSchedule(Dajax.process, {'form': data});
	return false;
}
