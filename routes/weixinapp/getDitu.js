var express = require('express');
var router = express.Router();
var sql = require('../../config/mysql')


/* GET home page. */
router.get('/', function(req, res, next) {
  sql.query('SELECT State_Province,SUM(quantity) FROM supermarket WHERE Country_Region="中国" GROUP BY State_Province ORDER BY SUM(quantity)', function(err, data){
        res.send(data) //data是从数据库中查找到的数据
        })
});

module.exports = router;


