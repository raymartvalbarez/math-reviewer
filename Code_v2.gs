// v2: paste over Code.gs, then Deploy > Manage deployments > Edit (pencil) > Version: New version > Deploy (same /exec URL)
// Header row for the Scores tab (row 1):
// Timestamp (Manila) | Name | Grade Level | Subject | Section | Score | Total | Percent | Topic breakdown | Answers
function doPost(e) {
  var lock = LockService.getScriptLock(); lock.waitLock(10000);
  try {
    var d = JSON.parse(e.postData.contents);
    var sh = SpreadsheetApp.getActive().getSheetByName('Scores');
    var ts = Utilities.formatDate(new Date(), 'Asia/Manila', 'yyyy-MM-dd HH:mm:ss');
    var tb = d.topicBreakdown;
    if (!tb && d.topics) tb = Object.keys(d.topics).map(function(k){return k + ': ' + d.topics[k];}).join('; ');
    sh.appendRow([ts, String(d.name||'').slice(0,80), String(d.grade||'').slice(0,20),
      String(d.subject||'General Mathematics').slice(0,80),
      String(d.sectionOnly||d.section||'').slice(0,60),
      Number(d.score)||0, Number(d.total)||0, (Number(d.percent)||0)+'%',
      String(tb||'').slice(0,500), String(d.answers||'').slice(0,200)]);
    return ContentService.createTextOutput('{"ok":true}').setMimeType(ContentService.MimeType.JSON);
  } finally { lock.releaseLock(); }
}
function doGet() { return ContentService.createTextOutput('ok'); }
