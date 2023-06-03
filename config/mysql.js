var mysql = require('mysql');
//创建链接
var connection = mysql.createConnection({
	//主机名
	host:'127.0.0.1',
	port:'3306',
	//用户名
	user:'root',
	//密码
	password :'123456',
	//数据库名称
	database :'jsouptest',
	multipleStatements:true
});
connection.connect();
module.exports = connection
