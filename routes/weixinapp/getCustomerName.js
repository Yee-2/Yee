var express = require('express');
var router = express.Router();
var sql = require('../../config/mysql')


/* GET home page. */
router.get('/', function(req, res, next) {
  sql.query('SELECT State_Province, COUNT(CustomerName) FROM supermarket GROUP BY State_Province ORDER BY COUNT(CustomerName) DESC LIMIT 0,6', function(err, data){
        res.send(data) //data是从数据库中查找到的数据
        })
});

module.exports = router;


