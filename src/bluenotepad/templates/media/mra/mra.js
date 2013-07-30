
var _MRA_PATH = "http://www.matrobot.com/api/log";

function _mra_send(projectId, sessionId, data){
	var params = data;
	params['project'] = projectId;
	params['session'] = sessionId;
	$.get(_MRA_PATH, params );
}

function _mra_generate_session() {
  return Math.floor(Math.random()*100000000).toString(16);
};
