$(document).ready(function () {
  var $cal = $("#calendar-doctor");
  if ($cal.length === 0 || typeof $.fn.simpleCalendar !== 'function') {
    return;
  }
  function iso(hoursFromNow) {
    var d = new Date();
    d.setHours(d.getHours() + hoursFromNow);
    return d.toISOString();
  }
  $cal.simpleCalendar({
    fixedStartDay: 0,
    disableEmptyDetails: true,
    events: [
      { startDate: iso(24), endDate: iso(25), summary: 'Conference with teachers' },
      { startDate: iso(-12), endDate: iso(-11), summary: 'Old classes' },
      { startDate: iso(-48), endDate: iso(-24), summary: 'Old Lessons' }
    ],
  });
}); 
